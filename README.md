# Sample Hardhat 3 Project (minimal)

This project has a minimal setup of Hardhat 3, without any plugins.

## What's included?

The project includes native support for TypeScript, Hardhat scripts, tasks, and support for Solidity compilation and tests.


Complete Flow
User clicks button in Streamlit
        │
        ▼
    Python (app.py)
        │
        ▼
    Web3.py (library)
        │
        ▼
    HTTP POST to http://127.0.0.1:8545
        │
        ▼
    Hardhat Node (your blockchain)
        │
        ▼
    Smart Contract (Payment.sol / Token.sol)
        │
        ▼
    Executes function (deposit/pay/withdraw)
        │
        ▼
    Updates balances in contract storage
        │
        ▼
    Emits event (Deposit/PaymentSent/Withdrawal)
        │
        ▼
    Records transaction in a block
        │
        ▼
    Returns result to Python
        │
        ▼
    Streamlit shows "Success!"