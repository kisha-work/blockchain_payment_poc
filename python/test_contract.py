from web3 import Web3
from contract_utils import get_web3, get_contract, get_deployed_addresses, to_ether, to_wei

w3 = get_web3()
print("Connected:", w3.is_connected())

accounts = w3.eth.accounts
print("Available accounts:", accounts[:5])

addresses = get_deployed_addresses()
payment_addr = addresses["PaymentModule#Payment"]
token_addr = addresses["PaymentModule#Token"]

print(f"Payment contract: {payment_addr}")
print(f"Token contract: {token_addr}")

payment = get_contract(w3, "Payment", payment_addr)
token = get_contract(w3, "Token", token_addr)

alice = accounts[1]
bob = accounts[2]
print(f"\nAlice: {alice}")
print(f"Bob: {bob}")

alice_balance = w3.eth.get_balance(alice)
print(f"Alice ETH balance: {to_ether(alice_balance)} ETH")

print("\n--- Sending 1 ETH from Alice to Payment contract ---")
tx = payment.functions.deposit().transact({"from": alice, "value": to_wei(1)})
w3.eth.wait_for_transaction_receipt(tx)
print(f"Alice contract balance: {to_ether(payment.functions.getBalance(alice).call())} ETH")
print(f"Contract total balance: {to_ether(payment.functions.getContractBalance().call())} ETH")

print("\n--- Alice pays Bob 0.5 ETH ---")
tx = payment.functions.pay(bob, to_wei(0.5)).transact({"from": alice})
w3.eth.wait_for_transaction_receipt(tx)
print(f"Alice contract balance: {to_ether(payment.functions.getBalance(alice).call())} ETH")
print(f"Bob contract balance: {to_ether(payment.functions.getBalance(bob).call())} ETH")

print("\n--- Alice withdraws 0.3 ETH ---")
tx = payment.functions.withdraw(to_wei(0.3)).transact({"from": alice})
w3.eth.wait_for_transaction_receipt(tx)
print(f"Alice contract balance: {to_ether(payment.functions.getBalance(alice).call())} ETH")
print(f"Alice ETH balance: {to_ether(w3.eth.get_balance(alice))} ETH")

print("\n--- Token Info ---")
print(f"Token name: {token.functions.name().call()}")
print(f"Token symbol: {token.functions.symbol().call()}")
print(f"Token total supply: {token.functions.totalSupply().call()}")
print(f"Alice token balance: {token.functions.balanceOf(alice).call()}")
print(f"Owner token balance: {token.functions.balanceOf(accounts[0]).call()}")

print("\n--- Transfer 100 tokens from Owner to Alice ---")
tx = token.functions.transfer(alice, 100 * 10**18).transact({"from": accounts[0]})
w3.eth.wait_for_transaction_receipt(tx)
print(f"Alice token balance: {token.functions.balanceOf(alice).call()}")
print(f"Owner token balance: {token.functions.balanceOf(accounts[0]).call()}")

print("\n--- Alice sends 50 tokens to Bob ---")
tx = token.functions.transfer(bob, 50 * 10**18).transact({"from": alice})
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
