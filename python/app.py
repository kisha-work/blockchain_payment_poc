import streamlit as st
from pathlib import Path
from datetime import datetime
import json
from contract_utils import (
    get_web3, get_contract, get_deployed_addresses,
    to_ether, to_wei, get_network, get_network_config,
    get_account, get_accounts, send_contract_tx,
)

st.set_page_config(page_title="Blockchain Payment POC", layout="wide")

network = get_network()
config = get_network_config()
st.title(f"Blockchain Payment POC — {network.upper()}")

w3 = get_web3()

if not w3.is_connected():
    st.error(f"Cannot connect to {config['rpc_url']}")
    if network == "local":
        st.info("Run: npx hardhat node")
    else:
        st.info("Check your SEPOLIA_RPC_URL in .env")
    st.stop()

st.success(f"Connected to {network.upper()} (Chain ID: {config['chain_id']})")

addresses = get_deployed_addresses()
payment = get_contract(w3, "Payment", addresses["PaymentModule#Payment"])
token = get_contract(w3, "Token", addresses["PaymentModule#Token"])

if network == "sepolia":
    account = get_account(w3)
    accounts = [account.address]
    ACCOUNT_NAMES = {0: "Your Wallet"}
else:
    accounts = get_accounts(w3)
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
if network == "local":
    selected_idx = st.sidebar.selectbox(
        "Account", range(len(accounts)),
        format_func=lambda i: f"{get_name(i)} ({accounts[i][:8]}...)",
    )
    sender = accounts[selected_idx]
else:
    selected_idx = 0
    sender = accounts[0]

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
    st.metric("Token Balance", f"{token_balance:,.0f} STC")

st.divider()

tab_eth, tab_token, tab_history = st.tabs(["ETH Payments", "Token Payments", "Transaction History"])

with tab_eth:
    st.subheader("Deposit ETH to Contract")
    deposit_amount = st.number_input("Deposit amount (ETH)", min_value=0.0, step=0.1, key="deposit")
    if st.button("Deposit ETH"):
        try:
            tx = send_contract_tx(w3, payment.functions.deposit(), sender, value=to_wei(deposit_amount))
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Deposited {deposit_amount} ETH | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Deposit failed: {e}")

    st.subheader("Pay Another Account")
    if network == "local":
        other_accounts = [(i, a) for i, a in enumerate(accounts) if a != sender]
        pay_idx = st.selectbox("Receiver", other_accounts, format_func=lambda x: f"{get_name(x[0])} ({x[1][:8]}...)", key="pay_addr")
        pay_addr = pay_idx[1]
    else:
        pay_addr = st.text_input("Receiver Address (0x...)", key="pay_addr_sepolia")
    pay_amount = st.number_input("Amount (ETH)", min_value=0.0, step=0.1, key="pay_amount")
    if st.button("Send ETH Payment"):
        try:
            tx = send_contract_tx(w3, payment.functions.pay(pay_addr, to_wei(pay_amount)), sender)
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Sent {pay_amount} ETH | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Payment failed: {e}")

    st.subheader("Withdraw ETH")
    withdraw_amount = st.number_input("Withdraw amount (ETH)", min_value=0.0, step=0.1, key="withdraw")
    if st.button("Withdraw ETH"):
        try:
            tx = send_contract_tx(w3, payment.functions.withdraw(to_wei(withdraw_amount)), sender)
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Withdrew {withdraw_amount} ETH | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Withdraw failed: {e}")

with tab_token:
    st.subheader("Transfer Tokens")
    if network == "local":
        token_other = [(i, a) for i, a in enumerate(accounts) if a != sender]
        token_recv_idx = st.selectbox("Receiver", token_other, format_func=lambda x: f"{get_name(x[0])} ({x[1][:8]}...)", key="token_recv")
        token_receiver = token_recv_idx[1]
    else:
        token_receiver = st.text_input("Receiver Address (0x...)", key="token_recv_sepolia")
    token_amount = st.number_input("Amount (STC)", min_value=0, step=10, key="token_amt")
    if st.button("Send Tokens"):
        try:
            tx = send_contract_tx(w3, token.functions.transfer(token_receiver, token_amount * 10**18), sender)
            receipt = w3.eth.wait_for_transaction_receipt(tx)
            st.success(f"Sent {token_amount:,} STC | Tx: {receipt.transactionHash.hex()[:16]}...")
            st.rerun()
        except Exception as e:
            st.error(f"Token transfer failed: {e}")

    st.subheader("All Token Balances")
    if network == "local":
        for i, acc in enumerate(accounts[:5]):
            bal = token.functions.balanceOf(acc).call() / 10**18
            if bal > 0:
                st.write(f"**{get_name(i)}** ({acc[:8]}...): {bal:,.0f} STC")
    else:
        bal = token.functions.balanceOf(sender).call() / 10**18
        st.write(f"**Your Wallet** ({sender[:8]}...): {bal:,.0f} STC")

with tab_history:
    st.subheader("Payment Contract Transaction History")

    try:
        deposit_events = payment.events.Deposit.get_logs(from_block=0)
        withdrawal_events = payment.events.Withdrawal.get_logs(from_block=0)
        payment_events = payment.events.PaymentSent.get_logs(from_block=0)
        token_transfer_events = token.events.Transfer.get_logs(from_block=0)
    except Exception as e:
        st.error(f"Error reading events: {e}")
        deposit_events = []
        withdrawal_events = []
        payment_events = []
        token_transfer_events = []

    all_txs = []

    for e in deposit_events:
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "Deposit",
            "sender": e.args["sender"],
            "amount": to_ether(e.args["amount"]),
            "symbol": "ETH",
        })

    for e in withdrawal_events:
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "Withdrawal",
            "sender": e.args["receiver"],
            "amount": to_ether(e.args["amount"]),
            "symbol": "ETH",
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
            "symbol": "ETH",
        })

    for e in token_transfer_events:
        if e.args["from"] == "0x0000000000000000000000000000000000000000":
            continue
        block = w3.eth.get_block(e.blockNumber)
        all_txs.append({
            "block": e.blockNumber,
            "timestamp": block.timestamp,
            "type": "TokenTransfer",
            "sender": e.args["from"],
            "receiver": e.args["to"],
            "amount": str(e.args["value"] // 10**18),
            "symbol": "STC",
        })

    all_txs.sort(key=lambda x: x["block"])

    tx_log_path = Path(__file__).parent / "transaction_log.json"
    log_data = []
    for tx in all_txs:
        entry = {
            "block": tx["block"],
            "timestamp": datetime.fromtimestamp(tx["timestamp"]).strftime("%Y-%m-%d %H:%M:%S"),
            "type": tx["type"],
            "sender": tx["sender"],
            "amount": float(tx["amount"]),
            "symbol": tx["symbol"],
        }
        if "receiver" in tx:
            entry["receiver"] = tx["receiver"]
        log_data.append(entry)

    with open(tx_log_path, "w") as f:
        json.dump(log_data, f, indent=2)

    if not all_txs:
        st.info("No transactions yet")
    else:
        for tx in all_txs:
            if network == "local" and tx["sender"] in accounts:
                sender_name = get_name(accounts.index(tx["sender"]))
            else:
                sender_name = tx["sender"][:10] + "..."
            ts = datetime.fromtimestamp(tx["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

            if tx["type"] == "Deposit":
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **deposited** {tx['amount']:.4f} ETH")
            elif tx["type"] == "Withdrawal":
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **withdrew** {tx['amount']:.4f} ETH")
            elif tx["type"] == "Payment":
                if network == "local" and tx["receiver"] in accounts:
                    recv_name = get_name(accounts.index(tx["receiver"]))
                else:
                    recv_name = tx["receiver"][:10] + "..."
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **paid** {recv_name} {tx['amount']:.4f} ETH")
            elif tx["type"] == "TokenTransfer":
                if network == "local" and tx["receiver"] in accounts:
                    recv_name = get_name(accounts.index(tx["receiver"]))
                else:
                    recv_name = tx["receiver"][:10] + "..."
                st.write(f"**Block {tx['block']}** | {ts} | {sender_name} **transferred** {tx['amount']} STC to {recv_name}")

    st.divider()
    st.subheader("Contract Info")
    st.write(f"Network: `{network.upper()}`")
    st.write(f"Payment contract: `{addresses['PaymentModule#Payment']}`")
    st.write(f"Token contract: `{addresses['PaymentModule#Token']}`")
    st.write(f"Total contract ETH: {to_ether(payment.functions.getContractBalance().call())} ETH")
    total_pmt = token.functions.totalSupply().call() / 10**18
    st.write(f"Total token supply: {total_pmt:,.0f} STC")

    if network == "sepolia":
        st.write(f"[View on Etherscan](https://sepolia.etherscan.io/address/{addresses['PaymentModule#Payment']})")
