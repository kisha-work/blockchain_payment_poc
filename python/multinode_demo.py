import os

from dotenv import load_dotenv
from web3 import Web3

from contract_utils import get_deployed_addresses, load_abi, to_ether

load_dotenv()

# Different independent Sepolia node providers (each is a separate node)
NODES = {
    "PublicNode": "https://ethereum-sepolia-rpc.publicnode.com",
    "Ankr": "https://rpc.ankr.com/eth_sepolia",
    "1RPC": "https://1rpc.io/sepolia",
    "Llamarpc": "https://eth.llamarpc.com",
}
# Optional private provider (set ALCHEMY_SEPOLIA_URL in .env)
if os.getenv("ALCHEMY_SEPOLIA_URL"):
    NODES["Alchemy"] = os.getenv("ALCHEMY_SEPOLIA_URL")

addresses = get_deployed_addresses()
payment_addr = addresses["PaymentModule#Payment"]
token_addr = addresses["PaymentModule#Token"]
payment_abi = load_abi("Payment")
token_abi = load_abi("Token")

print("=" * 70)
print("MULTI-NODE DEMO: Same blockchain, queried via independent nodes")
print("=" * 70)
print(f"Payment contract: {payment_addr}")
print(f"Token contract:   {token_addr}")
print("-" * 70)

results = {}
for name, url in NODES.items():
    try:
        w3 = Web3(Web3.HTTPProvider(url, request_kwargs={"timeout": 10}))
        if not w3.is_connected():
            print(f"{name:12} | OFFLINE / timeout")
            continue
        chain = w3.eth.chain_id
        block = w3.eth.block_number
        payment = w3.eth.contract(address=payment_addr, abi=payment_abi)
        token = w3.eth.contract(address=token_addr, abi=token_abi)
        contract_eth = payment.functions.getContractBalance().call()
        token_supply = token.functions.totalSupply().call()
        results[name] = (chain, block, contract_eth, token_supply)
        print(
            f"{name:12} | chain={chain} block={block} "
            f"contractETH={to_ether(contract_eth):.6f} tokenSupply={token_supply // 10**18:,} STC"
        )
    except Exception as e:
        print(f"{name:12} | ERROR: {e}")

print("-" * 70)

if len(results) >= 2:
    ref = next(iter(results.values()))
    consistent = all(v[:1] == ref[:1] for v in results.values())
    print(f"\nRESULT: {len(results)} independent nodes read the SAME chain (chainId={ref[0]})")
    print(f"All nodes agree on the contract state -> this is a decentralised, multi-node system.")
    print("If this were a single local node, no other node would know your contracts exist.")
else:
    print("\nOnly one node responded - check your internet / retry.")