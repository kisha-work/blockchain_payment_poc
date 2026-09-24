# Blockchain Payment POC

A proof-of-concept payment system built on Hardhat 3 (local EVM) with Solidity smart contracts, a Python/Web3.py backend, and a Streamlit web dashboard.

## What's included?

- Hardhat 3 with native TypeScript support and Hardhat Ignition for deployments
- Solidity compilation and tests
- Two contracts: `contracts/payment.sol` (ETH payments) and `contracts/Token.sol` (ERC-20 STC)


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




    Blockchain Payment POC - Project Flow
1. Project Overview
- Built a blockchain-based payment system proof of concept
- Uses Ethereum-compatible blockchain (Hardhat) for transaction recording
- Supports both ETH transfers and custom ERC-20 token (STC) transfers
- Interactive web dashboard for user interaction
2. Technology Stack
- Blockchain: Hardhat 3.15.0 (local Ethereum simulator)
- Smart Contracts: Solidity 0.8.34
- Backend: Python 3.11 with Web3.py 8.0
- Frontend: Streamlit 1.63.0
- Deployment: Hardhat Ignition
3. Architecture
User (Browser) → Streamlit UI → Web3.py → Hardhat Node → Smart Contracts
4. Components
Smart Contracts:
- payment.sol - Handles ETH deposits, withdrawals, and peer-to-peer payments
- Token.sol - ERC-20 token (STC) with minting and transfer capabilities
Python Integration:
- contract_utils.py - Connects to blockchain, loads contract ABIs
- app.py - Streamlit web interface for user interaction
- test_contract.py - CLI testing script
Configuration:
- hardhat.config.ts - Blockchain network configuration
- ignition/modules/payment.ts - Contract deployment script
5. How It Works
Step 1: Start Hardhat node (local blockchain) on port 8545
Step 2: Deploy smart contracts to blockchain via Ignition
Step 3: Launch Streamlit web dashboard
Step 4: Users interact through web interface:
- Select account (Alice/Bob/Charlie)
- Deposit ETH to contract
- Send ETH to other accounts
- Transfer STC tokens
- View transaction history
6. Transaction Flow
User clicks button → Python creates transaction → Web3.py signs it →
HTTP request to Hardhat → Smart contract executes → Transaction recorded in block →
Result returned to UI → User sees success
7. Key Features
- Real-time balance updates
- Transaction history with block numbers and timestamps
- Multiple account support (10 test accounts with 10,000 ETH each)
- Both ETH and token transfers
- Immutable transaction records on blockchain
8. Project Structure
blockchain_payment_poc/
├── contracts/           # Smart contracts (Solidity)
├── ignition/            # Deployment configuration
├── python/              # Python integration and UI
├── artifacts/           # Compiled contract ABIs
├── hardhat.config.ts    # Blockchain configuration
└── package.json         # Dependencies
9. How to Run
# Terminal 1: Start blockchain
npx hardhat node

# Terminal 2: Deploy contracts
npx hardhat ignition deploy ./ignition/modules/payment.ts --network localhost

# Terminal 3: Start web dashboard
cd python
streamlit run app.py
10. Current Status
- POC completed and functional
- All transactions recorded on local blockchain
- Web dashboard operational
- Ready for demo and integration discussions
11. Next Steps (If Required)
- Migrate to production blockchain (Hyperledger Fabric)
- Add REST API for system integration
- Implement multi-node network
- Add authentication and authorization
Note: This is a local development setup for demonstration purposes. Production deployment would require a proper blockchain network with multiple nodes and security considerations.