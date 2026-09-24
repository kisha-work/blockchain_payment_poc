import json
import os
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).parent.parent
ABI_DIR = PROJECT_ROOT / "artifacts" / "contracts"

load_dotenv(PROJECT_ROOT / ".env")

NETWORK = os.getenv("NETWORK", "local")

NETWORK_CONFIG = {
    "local": {
        "rpc_url": "http://127.0.0.1:8545",
        "chain_id": 31337,
        "chain_dir": "chain-31337",
    },
    "sepolia": {
        "rpc_url": os.getenv("SEPOLIA_RPC_URL", ""),
        "chain_id": 11155111,
        "chain_dir": "chain-11155111",
    },
}


def get_network():
    return NETWORK


def get_network_config():
    return NETWORK_CONFIG[NETWORK]


def get_web3():
    config = get_network_config()
    return Web3(Web3.HTTPProvider(config["rpc_url"]))


def load_abi(contract_name):
    abi_file = ABI_DIR / f"{contract_name}.sol" / f"{contract_name}.json"
    with open(abi_file) as f:
        return json.load(f)["abi"]


def get_contract(w3, contract_name, address):
    abi = load_abi(contract_name)
    return w3.eth.contract(address=address, abi=abi)


def get_deployed_addresses():
    config = get_network_config()
    addr_file = PROJECT_ROOT / "ignition" / "deployments" / config["chain_dir"] / "deployed_addresses.json"
    with open(addr_file) as f:
        return json.load(f)


def get_account(w3):
    if NETWORK == "sepolia":
        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            raise ValueError("PRIVATE_KEY not set in .env for Sepolia network")
        return w3.eth.account.from_key(private_key)
    return w3.eth.accounts[0]


def get_accounts(w3):
    if NETWORK == "sepolia":
        account = get_account(w3)
        return [account]
    return w3.eth.accounts


def send_contract_tx(w3, contract_fn, from_addr, value=0, gas=None):
    if NETWORK == "sepolia":
        account = get_account(w3)
        tx_params = {"from": account.address, "value": value}
        if gas:
            tx_params["gas"] = gas
        built = contract_fn.build_transaction(tx_params)
        signed = account.sign_transaction(built)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        return tx_hash
    return contract_fn.transact({"from": from_addr, "value": value})


def to_ether(wei):
    return Web3.from_wei(wei, "ether")


def to_wei(ether):
    return Web3.to_wei(ether, "ether")
