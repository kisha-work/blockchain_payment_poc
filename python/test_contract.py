from web3 import Web3
from contract_utils import (
    get_web3, get_contract, get_deployed_addresses,
    to_ether, to_wei, get_network, get_account, get_accounts,
    send_contract_tx,
)

network = get_network()
print(f"Network: {network.upper()}")

w3 = get_web3()
print("Connected:", w3.is_connected())

addresses = get_deployed_addresses()
payment_addr = addresses["PaymentModule#Payment"]
token_addr = addresses["PaymentModule#Token"]

print(f"Payment contract: {payment_addr}")
print(f"Token contract: {token_addr}")

payment = get_contract(w3, "Payment", payment_addr)
token = get_contract(w3, "Token", token_addr)

if network == "sepolia":
    account = get_account(w3)
    sender = account.address
    print(f"\nDeployer/Sender: {sender}")
    print(f"ETH balance: {to_ether(w3.eth.get_balance(sender))} ETH")
else:
    accounts = get_accounts(w3)
    sender = accounts[0]
    alice = accounts[1]
    bob = accounts[2]
    print(f"Available accounts: {accounts[:3]}")
    print(f"Deployer: {sender}")
    print(f"Alice: {alice}")
    print(f"Bob: {bob}")

print("\n--- Depositing 0.1 ETH to Payment contract ---")
tx = send_contract_tx(w3, payment.functions.deposit(), sender, value=to_wei(0.1))
w3.eth.wait_for_transaction_receipt(tx)
print(f"Contract balance: {to_ether(payment.functions.getContractBalance().call())} ETH")
print(f"Your contract balance: {to_ether(payment.functions.getBalance(sender).call())} ETH")

print("\n--- Token Info ---")
print(f"Token name: {token.functions.name().call()}")
print(f"Token symbol: {token.functions.symbol().call()}")
print(f"Token total supply: {token.functions.totalSupply().call()}")
print(f"Your token balance: {token.functions.balanceOf(sender).call()}")

if network == "local":
    print("\n--- Alice pays Bob 0.05 ETH ---")
    tx = send_contract_tx(w3, payment.functions.pay(bob, to_wei(0.05)), alice)
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"Alice contract balance: {to_ether(payment.functions.getBalance(alice).call())} ETH")
    print(f"Bob contract balance: {to_ether(payment.functions.getBalance(bob).call())} ETH")

    print("\n--- Transfer 100 tokens from Owner to Alice ---")
    tx = send_contract_tx(w3, token.functions.transfer(alice, 100 * 10**18), sender)
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"Alice token balance: {token.functions.balanceOf(alice).call()}")

    print("\n--- Alice sends 50 tokens to Bob ---")
    tx = send_contract_tx(w3, token.functions.transfer(bob, 50 * 10**18), alice)
    w3.eth.wait_for_transaction_receipt(tx)
    print(f"Alice token balance: {token.functions.balanceOf(alice).call()}")
    print(f"Bob token balance: {token.functions.balanceOf(bob).call()}")

print("\n--- Transaction History ---")
count = payment.functions.getTransactionCount().call()
print(f"Total transactions: {count}")
for i in range(count):
    addr = payment.functions.getTransaction(i).call()
    print(f"  Tx {i}: {addr}")

print("\nDone!")
