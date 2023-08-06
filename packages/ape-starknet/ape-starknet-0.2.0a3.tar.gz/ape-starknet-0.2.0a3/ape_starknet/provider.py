import os
from typing import Any, Dict, Iterator, List, Optional, Union
from urllib.error import HTTPError
from urllib.parse import urlparse
from urllib.request import urlopen

from ape.api import BlockAPI, ProviderAPI, ReceiptAPI, SubprocessProvider, TransactionAPI
from ape.api.networks import LOCAL_NETWORK_NAME
from ape.contracts import ContractInstance
from ape.exceptions import ProviderError, ProviderNotConnectedError, VirtualMachineError
from ape.types import AddressType, BlockID, ContractLog
from ape.utils import cached_property
from ethpm_types.abi import ConstructorABI, EventABI
from hexbytes import HexBytes
from starknet_py.net import Client as StarknetClient  # type: ignore
from starknet_py.net.models import parse_address  # type: ignore
from starkware.starknet.definitions.transaction_type import TransactionType  # type: ignore
from starkware.starknet.services.api.contract_class import ContractClass  # type: ignore
from starkware.starknet.services.api.feeder_gateway.response_objects import (  # type: ignore
    DeploySpecificInfo,
    InvokeSpecificInfo,
)

from ape_starknet.config import StarknetConfig
from ape_starknet.tokens import TokenManager
from ape_starknet.transactions import InvokeFunctionTransaction, StarknetTransaction
from ape_starknet.utils import (
    ALPHA_MAINNET_WL_DEPLOY_TOKEN_KEY,
    PLUGIN_NAME,
    get_chain_id,
    get_virtual_machine_error,
    handle_client_errors,
)
from ape_starknet.utils.basemodel import StarknetMixin

DEFAULT_PORT = 8545


class StarknetProvider(SubprocessProvider, ProviderAPI, StarknetMixin):
    """
    A Starknet provider.
    """

    # Gets set when 'connect()' is called.
    client: Optional[StarknetClient] = None
    token_manager: TokenManager = TokenManager()
    default_gas_cost: int = 0

    @property
    def process_name(self) -> str:
        return "starknet-devnet"

    @property
    def is_connected(self) -> bool:
        try:
            urlopen(self.uri)
            return True
        except HTTPError as err:
            return err.code == 404  # Task failed successfully
        except Exception:
            return False

    @property
    def starknet_client(self) -> StarknetClient:
        if not self.is_connected:
            raise ProviderError("Provider is not connected to Starknet.")

        return self.client

    def build_command(self) -> List[str]:
        parts = urlparse(self.uri)
        return ["starknet-devnet", "--host", str(parts.hostname), "--port", str(parts.port)]

    @cached_property
    def plugin_config(self) -> StarknetConfig:
        return self.config_manager.get_config(PLUGIN_NAME) or StarknetConfig()  # type: ignore

    @cached_property
    def uri(self) -> str:
        network_config = self.plugin_config.providers.dict().get(self.network.name)
        if not network_config:
            raise ProviderError(f"Unknown network '{self.network.name}'.")

        return network_config.get("uri") or f"http://127.0.0.1:{DEFAULT_PORT}"

    def connect(self):
        if self.network.name == LOCAL_NETWORK_NAME:
            # Behave like a 'SubprocessProvider'
            if not self.is_connected:
                super().connect()

            self.start()

        self.client = StarknetClient(self.uri, chain=self.chain_id)

    def disconnect(self):
        self.client = None
        super().disconnect()

    def update_settings(self, new_settings: dict):
        pass

    @property
    def chain_id(self) -> int:
        return get_chain_id(self.network.name).value

    @handle_client_errors
    def get_balance(self, address: AddressType) -> int:
        network = self.network.name
        if network == LOCAL_NETWORK_NAME:
            # Fees / balances are currently not supported in local
            return 0

        account = self.account_contracts[address]
        account_contract_address = account.contract_address  # type: ignore
        return self.token_manager.get_balance(account_contract_address)

    @handle_client_errors
    def get_code(self, address: str) -> bytes:
        return self.get_code_and_abi(address)["bytecode"]  # type: ignore

    @handle_client_errors
    def get_abi(self, address: str) -> List[Dict]:
        return self.get_code_and_abi(address)["abi"]  # type: ignore

    @handle_client_errors
    def get_nonce(self, address: AddressType) -> int:
        # Check if passing a public-key address of a local account
        if address in self.account_contracts.public_key_addresses:
            contract_address = self.account_contracts.get_account(address).contract_address
            if contract_address:
                address = contract_address

        checksum_address = self.starknet.decode_address(address)
        contract = self.chain_manager.contracts.instance_at(checksum_address)

        if not isinstance(contract, ContractInstance):
            raise ProviderError(f"Account contract '{checksum_address}' not found.")

        return contract.get_nonce()

    @handle_client_errors
    def estimate_gas_cost(self, txn: TransactionAPI) -> int:
        if self.network.name == LOCAL_NETWORK_NAME:
            return self.default_gas_cost

        if not isinstance(txn, StarknetTransaction):
            raise ProviderError(
                "Unable to estimate the gas cost for a non-Starknet transaction "
                "using Starknet provider."
            )

        starknet_object = txn.as_starknet_object()

        if not self.client:
            raise ProviderNotConnectedError()

        return self.client.estimate_fee_sync(starknet_object)

    @property
    def gas_price(self) -> int:
        """
        **NOTE**: Currently, the gas price is fixed to always be 100 gwei.
        """
        return self.conversion_manager.convert("100 gwei", int)

    @handle_client_errors
    def get_block(self, block_id: BlockID) -> BlockAPI:
        if isinstance(block_id, (int, str)) and len(str(block_id)) == 76:
            kwarg = "block_hash"
        elif isinstance(block_id, int) or block_id == "pending":
            kwarg = "block_number"
        else:
            raise ValueError(f"Unsupported BlockID type '{type(block_id)}'.")

        block = self.starknet_client.get_block_sync(**{kwarg: block_id})
        return self.starknet.decode_block(block.dump())

    @handle_client_errors
    def send_call(self, txn: TransactionAPI) -> bytes:
        if not isinstance(txn, InvokeFunctionTransaction):
            type_str = f"{txn.type!r}" if isinstance(txn.type, bytes) else str(txn.type)
            raise ProviderError(
                f"Transaction must be from an invocation. Received type {type_str}."
            )

        if not self.client:
            raise ProviderNotConnectedError()

        starknet_obj = txn.as_starknet_object()
        return_value = self.client.call_contract_sync(starknet_obj)
        return self.starknet.decode_returndata(txn.method_abi, return_value)  # type: ignore

    @handle_client_errors
    def get_transaction(self, txn_hash: str) -> ReceiptAPI:
        self.starknet_client.wait_for_tx_sync(txn_hash)
        receipt = self.starknet_client.get_transaction_receipt_sync(tx_hash=txn_hash)
        receipt_dict: Dict[str, Any] = {"provider": self, **vars(receipt)}
        txn_info = self.starknet_client.get_transaction_sync(tx_hash=txn_hash).transaction

        if isinstance(txn_info, DeploySpecificInfo):
            txn_type = TransactionType.DEPLOY
        elif isinstance(txn_info, InvokeSpecificInfo):
            txn_type = TransactionType.INVOKE_FUNCTION
        else:
            raise ValueError(f"No value found for '{txn_info}'.")

        receipt_dict["contract_address"] = self.starknet.decode_address(txn_info.contract_address)
        receipt_dict["type"] = txn_type
        receipt_dict["events"] = [vars(e) for e in receipt_dict["events"]]
        return self.starknet.decode_receipt(receipt_dict)

    @handle_client_errors
    def send_transaction(self, txn: TransactionAPI, token: Optional[str] = None) -> ReceiptAPI:
        txn = self.prepare_transaction(txn)
        if not token and hasattr(txn, "token") and txn.token:  # type: ignore
            token = txn.token  # type: ignore
        else:
            token = os.environ.get(ALPHA_MAINNET_WL_DEPLOY_TOKEN_KEY)

        if not isinstance(txn, StarknetTransaction):
            raise ProviderError(
                "Unable to send non-Starknet transaction using a Starknet provider."
            )

        starknet_txn = txn.as_starknet_object()
        txn_info = self.starknet_client.add_transaction_sync(starknet_txn, token=token)

        error = txn_info.get("error", {})
        if error:
            message = error.get("message", error)
            raise ProviderError(message)

        # Return felts as ints and let calling context decide if hexstr is more appropriate.
        return_value = [
            self.starknet.encode_primitive_value(v) if isinstance(v, str) else v
            for v in txn_info.get("result", [])
        ]
        if return_value and isinstance(txn, InvokeFunctionTransaction):
            return_value = self.starknet.decode_returndata(txn.method_abi, return_value)
            if isinstance(return_value, (list, tuple)) and len(return_value) == 1:
                return_value = return_value[0]

        txn_hash = txn_info["transaction_hash"]
        receipt = self.get_transaction(txn_hash)
        receipt.return_value = return_value
        return receipt

    @handle_client_errors
    def get_contract_logs(
        self,
        address: Union[AddressType, List[AddressType]],
        abi: Union[EventABI, List[EventABI]],
        start_block: Optional[int] = None,
        stop_block: Optional[int] = None,
        block_page_size: Optional[int] = None,
        event_parameters: Optional[Dict] = None,
    ) -> Iterator[ContractLog]:
        raise NotImplementedError("TODO")

    @handle_client_errors
    def prepare_transaction(self, txn: TransactionAPI) -> TransactionAPI:
        if txn.type == TransactionType.INVOKE_FUNCTION and not txn.max_fee:
            txn.max_fee = self.estimate_gas_cost(txn)

        return txn

    def get_virtual_machine_error(self, exception: Exception) -> VirtualMachineError:
        return get_virtual_machine_error(exception) or VirtualMachineError(base_err=exception)

    def get_code_and_abi(self, address: Union[str, AddressType]):
        address_int = parse_address(address)
        return self.starknet_client.get_code_sync(address_int)

    def _deploy(self, contract_data: Union[str, Dict], *args, token: Optional[str] = None) -> str:
        """
        Helper for deploying a Starknet-compiled artifact, such as imported
        compiled account contracts from OZ.
        """
        if isinstance(contract_data, dict):
            contract = ContractClass.load(contract_data)
        else:
            contract = ContractClass.loads(contract_data)

        data: Dict = next(
            (member for member in contract.abi if member["type"] == "constructor"),
            {},
        )
        ctor_abi = ConstructorABI(**data)
        transaction = self.starknet.encode_deployment(
            HexBytes(contract.serialize()), ctor_abi, *args
        )
        wl_token = token or os.environ.get(ALPHA_MAINNET_WL_DEPLOY_TOKEN_KEY)
        receipt = self.send_transaction(transaction, token=wl_token)
        address = receipt.contract_address
        if not address:
            raise ProviderError("Failed to deploy contract.")

        return address


__all__ = ["StarknetProvider"]
