import json
from pathlib import Path
from web3 import Web3

PROJECT_ROOT = Path(__file__).parent.parent
ABI_DIR = PROJECT_ROOT / "artifacts" / "contracts"

def get_web3():
    return Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

def load_abi(contract_name):
    abi_file = ABI_DIR / f"{contract_name}.sol" / f"{contract_name}.json"
    with open(abi_file) as f:
        return json.load(f)["abi"]

def get_contract(w3, contract_name, address):
    abi = load_abi(contract_name)
    return w3.eth.contract(address=address, abi=abi)

def get_deployed_addresses():
    addr_file = PROJECT_ROOT / "ignition" / "deployments" / "chain-31337" / "deployed_addresses.json"
    with open(addr_file) as f:
        return json.load(f)

def to_ether(wei):
    return Web3.from_wei(wei, "ether")

def to_wei(ether):
    return Web3.to_wei(ether, "ether")
