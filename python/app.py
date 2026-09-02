import streamlit as st
from contract_utils import get_web3, get_contract, get_deployed_addresses, to_ether, to_wei

st.set_page_config(page_title="Blockchain Payment POC", layout="wide")
st.title("Blockchain Payment POC")

w3 = get_web3()

if not w3.is_connected():
    st.error("Cannot connect to Hardhat node at http://127.0.0.1:8545")
    st.info("Run: npx hardhat node")
    st.stop()

st.success("Connected to Hardhat node")

accounts = w3.eth.accounts
addresses = get_deployed_addresses()
payment = get_contract(w3, "Payment", addresses["PaymentModule#Payment"])
token = get_contract(w3, "Token", addresses["PaymentModule#Token"])

ACCOUNT_NAMES = {
    0: "Owner (Deployer)",
    1: "Alice",
    2: "Bob",
    3: "Charlie",
    4: "Dave",
    5: "Eve",
    6: "Frank",
    7: "Grace",
    8: "Heidi",
    9: "Ivan",
}

def get_name(idx):
    return ACCOUNT_NAMES.get(idx, f"Account {idx}")

st.sidebar.header("Select Account")
selected_idx = st.sidebar.selectbox("Account", range(len(accounts)), format_func=lambda i: f"{get_name(i)} ({accounts[i][:8]}...)")
sender = accounts[selected_idx]

st.sidebar.write(f"**Selected:** {get_name(selected_idx)}")
st.sidebar.write(f"Address: `{sender}`")

st.header("Balances")
col1, col2, col3 = st.columns(3)
with col1:
    eth_balance = to_ether(w3.eth.get_balance(sender))
    st.metric("ETH Wallet Balance", f"{eth_balance:.4f} ETH")
with col2:
    contract_eth = to_ether(payment.functions.getBalance(sender).call())
    st.metric("ETH in Contract", f"{contract_eth:.4f} ETH")
with col3:
    token_balance = token.functions.balanceOf(sender).call() / 10**18
    st.metric("Token Balance", f"{token_balance:,.0f} PMT")

st.divider()

tab_eth, tab_token, tab_history = st.tabs(["ETH Payments", "Token Payments", "Transaction History"])

with tab_eth:
    st.subheader("Deposit ETH to Contract")
    deposit_amount = st.number_input("Deposit amount (ETH)", min_value=0.0, step=0.1, key="deposit")
    if st.button("Deposit ETH"):
        try:
            tx = payment.functions.deposit().transact({"from": sender, "value": to_wei(deposit_amount)})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Deposited {deposit_amount} ETH | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Deposit failed: {e}")

    st.subheader("Pay Another Account")
    other_accounts = [(i, a) for i, a in enumerate(accounts) if a != sender]
    pay_idx = st.selectbox("Receiver", other_accounts, format_func=lambda x: f"{get_name(x[0])} ({x[1][:8]}...)", key="pay_addr")
    pay_addr = pay_idx[1]
    pay_amount = st.number_input("Amount (ETH)", min_value=0.0, step=0.1, key="pay_amount")
    if st.button("Send ETH Payment"):
        try:
            tx = payment.functions.pay(pay_addr, to_wei(pay_amount)).transact({"from": sender})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Sent {pay_amount} ETH to {get_name(pay_idx[0])} | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Payment failed: {e}")

    st.subheader("Withdraw ETH")
    withdraw_amount = st.number_input("Withdraw amount (ETH)", min_value=0.0, step=0.1, key="withdraw")
    if st.button("Withdraw ETH"):
        try:
            tx = payment.functions.withdraw(to_wei(withdraw_amount)).transact({"from": sender})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Withdrew {withdraw_amount} ETH | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Withdraw failed: {e}")

with tab_token:
    st.subheader("Transfer Tokens")
    token_other = [(i, a) for i, a in enumerate(accounts) if a != sender]
    token_recv_idx = st.selectbox("Receiver", token_other, format_func=lambda x: f"{get_name(x[0])} ({x[1][:8]}...)", key="token_recv")
    token_receiver = token_recv_idx[1]
    token_amount = st.number_input("Amount (PMT)", min_value=0, step=10, key="token_amt")
    if st.button("Send Tokens"):
        try:
            tx = token.functions.transfer(token_receiver, token_amount).transact({"from": sender})
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Sent {token_amount:,} PMT to {get_name(token_recv_idx[0])} | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Token transfer failed: {e}")

    st.subheader("All Token Balances")
    for i, acc in enumerate(accounts[:5]):
        bal = token.functions.balanceOf(acc).call() / 10**18
        if bal > 0:
            st.write(f"**{get_name(i)}** ({acc[:8]}...): {bal:,.0f} PMT")

with tab_history:
    st.subheader("Payment Contract Transaction History")

    try:
        deposit_events = payment.events.Deposit.get_logs()
        withdrawal_events = payment.events.Withdrawal.get_logs()
        payment_events = payment.events.PaymentSent.get_logs()
    except Exception as e:
        st.error(f"Error reading events: {e}")
        deposit_events = []
        withdrawal_events = []
        payment_events = []

    all_txs = []

    for e in deposit_events:
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "Deposit",
            "sender": e.args["sender"],
            "amount": to_ether(e.args["amount"]),
        })

    for e in withdrawal_events:
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "Withdrawal",
            "sender": e.args["receiver"],
            "amount": to_ether(e.args["amount"]),
        })

    for e in payment_events:
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "Payment",
            "sender": e.args["from"],
            "receiver": e.args["to"],
            "amount": to_ether(e.args["amount"]),
        })

    all_txs.sort(key=lambda x: x["block"])

    if not all_txs:
        st.info("No transactions yet")
    else:
        from datetime import datetime
        for tx in all_txs:
            sender_name = get_name(accounts.index(tx["sender"])) if tx["sender"] in accounts else "Unknown"
            ts = datetime.fromtimestamp(tx["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

            if tx["type"] == "Deposit":
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **deposited** {tx['amount']:.4f} ETH")
            elif tx["type"] == "Withdrawal":
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **withdrew** {tx['amount']:.4f} ETH")
            elif tx["type"] == "Payment":
                recv_name = get_name(accounts.index(tx["receiver"])) if tx["receiver"] in accounts else "Unknown"
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **paid** {recv_name} {tx['amount']:.4f} ETH")

    st.divider()
    st.subheader("Contract Info")
    st.write(f"Contract address: `{addresses['PaymentModule#Payment']}`")
    st.write(f"Token address: `{addresses['PaymentModule#Token']}`")
    st.write(f"Total contract ETH: {to_ether(payment.functions.getContractBalance().call())} ETH")
    total_pmt = token.functions.totalSupply().call() / 10**18
    st.write(f"Total token supply: {total_pmt:,.0f} PMT")
