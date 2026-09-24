# Project Details - Payment POC

> This file is a live learning log. Every time we learn something new about the project,
> its tools, or its concepts, we add it here.

## Current State

- Hardhat 3 project with Hardhat Ignition
- TypeScript + Solidity
- Two contracts: `contracts/payment.sol` (ETH payments) and `contracts/Token.sol` (ERC-20 STC)
- Python backend (Web3.py) + Streamlit web dashboard
- Local Hardhat network + optional Sepolia testnet config

---

## Terminologies

### Hardhat (definition)
A JavaScript/TypeScript development environment for Ethereum smart contracts.
Built for compiling, testing, deploying, and debugging Solidity contracts.

### Solidity
The programming language used to write smart contracts that run on Ethereum and
other EVM-compatible blockchains. Code has the `.sol` extension.

### Smart contract
A program stored on a blockchain that runs when predetermined conditions are met.
It's self-executing, transparent, and can't be changed once deployed.

### Hardhat 3
The latest major version of Hardhat (this project uses `hardhat: ^3.15.0`).
Notable differences vs v2: no plugins needed for basics (TypeScript scripts and
tests are native), new `tasks` API.

### `hardhat.config.ts`
The configuration file for a Hardhat project. Controls Solidity compiler version,
deployments, networks, and plugins.

### Ethereum Sepolia

The actual blockchain network.(testing network)

### Alchemy

The gateway/API that lets your application talk to Sepolia.

### MetaMask

Your wallet and identity.

### Faucets (Zalalena, Chainlink, Google, etc.)
WE HAVE USED ZALALENA
Websites that hand out free Sepolia ETH for testing



Example from this project:
```ts
import "dotenv/config";
import { defineConfig, configVariable } from "hardhat/config";
import hardhatIgnition from "@nomicfoundation/hardhat-ignition";

export default defineConfig({
  plugins: [hardhatIgnition],
  solidity: {
    version: "0.8.34",
  },
  networks: {
    sepolia: {
      type: "http",
      chainType: "l1",
      chainId: 11155111,
      url: configVariable("SEPOLIA_RPC_URL"),
      accounts: [configVariable("PRIVATE_KEY")],
    },
  },
});
```

### `defineConfig`
A Hardhat helper that gives type-safe autocompletion when writing your config.

### pragma
A Solidity directive that specifies which compiler versions are allowed to compile
the contract. Here: `pragma solidity ^0.8.24;` means any 0.8.x version at or above 0.8.24.

### contract (keyword)
The Solidity keyword that declares a smart contract, like a class/namespace for the
state and functions it holds.

### `artifacts/` folder
Output of the Solidity compiler. Contains ABI + bytecode JSON files that other
tools (tests, deploy scripts, frontends) use to interact with the contract.

### `cache/` folder
Hardhat's internal cache used to speed up recompilation by only rebuilding
contracts whose sources changed.

### `node_modules/`
Installed npm dependencies (Hardhat, TypeScript, etc.).

---

## Folder / File Map

| Path | What it is for |
|------|----------------|
| `hardhat.config.ts` | Solidity version, Ignition plugin, Sepolia network config |
| `contracts/payment.sol` | ETH payment contract (deposit/pay/withdraw) |
| `contracts/Token.sol` | ERC-20 token contract (STC) |
| `ignition/modules/payment.ts` | Contract deployment script (Ignition) |
| `python/` | Python backend: Web3.py + Streamlit UI |
| `artifacts/` | Compiler output (ABI + bytecode) |
| `cache/` | Hardhat's recompile cache |
| `package.json` | Node project metadata + deps |
| `tsconfig.json` | TypeScript compiler settings |
| `README.md` | Project readme |
| `.env` | Secrets/local config (git-ignored; see `.env.example`) |

---

## What We're Learning Next

(TBD - this section grows as we explore)

                 OUR FINAL POC

                    Streamlit
                       │
                       ▼
                    Python
                       │
                    Web3.py
                       │
                       ▼
              ┌─────────────────┐
              │ Smart Contracts │
              │                 │
              │ Payment.sol     │
              │ Token.sol       │
              └────────┬────────┘
                       │
                       ▼
                Hardhat Network
                       │
                       ▼
                 Transactions
                       │
                       ▼
                Alice → Bob



compilation creates the executable contract artifact. Deployment creates the contract instance on a blockchain and gives it an address.

STEP 1
Write Solidity
       ✅
       ↓
STEP 2
Compile
       ✅
       ↓
STEP 3
Start local blockchain
       ✅
       ↓
STEP 4
Deploy contract
       ← WE ARE HERE
       ↓
STEP 5
Interact with contract
       ↓
STEP 6
Build actual payment logic
       ↓
STEP 7
Create token
       ↓
STEP 8
Python + Web3.py
       ↓
STEP 9
Streamlit UI
       ↓
STEP 10
Complete POC


Detailed Project Overview — Blockchain Payment POC
1. What This Project Is
A proof-of-concept payment system that simulates an Ethereum-compatible blockchain locally. Users can deposit ETH, send payments to other users, withdraw ETH, and transfer a custom ERC-20 token (STC) — all through a web dashboard backed by real smart contract execution on a local EVM.
2. Technology Stack
Layer	Technology	Purpose
Blockchain	Hardhat 3.x (local EVM)	Simulates Ethereum on localhost:8545
Smart Contracts	Solidity 0.8.34	Payment logic + ERC-20 token
Deployment	Hardhat Ignition	Deterministic contract deployment
Backend	Python 3.11 + Web3.py 8.0	Signs & sends transactions, reads blockchain state
Frontend	Streamlit 1.63	Interactive web dashboard
3. Smart Contracts — In Detail
3a. payment.sol — ETH Payment Contract
State variables:
- owner — deployer address (not enforced for user functions)
- contractBalance — total ETH held by the contract
- balances — mapping of address → uint256, tracks each user's deposited ETH
- transactionHistory — array of addresses (stores who interacted, in order)
Functions:
Function	Visibility	Mutability	What it does
deposit()	external	payable	Accepts ETH from caller, adds to their balances[sender], increments contractBalance, pushes sender to transactionHistory, emits Deposit event
pay(receiver, amount)	external	nonpayable	Deducts amount from sender's balance, adds to receiver's balance (both must be in-contract balances), emits PaymentSent
withdraw(amount)	external	nonpayable	Deducts from caller's in-contract balance, sends ETH back to caller's wallet via low-level call{value}, emits Withdrawal
getBalance(account)	external	view	Returns balances[account]
getContractBalance()	external	view	Returns contractBalance
getTransactionCount()	external	view	Returns transactionHistory.length
getTransaction(index)	external	view	Returns address at transactionHistory[index]
receive()	external	payable	Fallback — same as deposit(), catches plain ETH transfers
Events:
- Deposit(address indexed sender, uint256 amount) — emitted on deposit
- Withdrawal(address indexed receiver, uint256 amount) — emitted on withdraw
- PaymentSent(address indexed from, address indexed to, uint256 amount) — emitted on P2P pay
Key behavior notes:
- The contract acts as an escrow — users deposit ETH into the contract, then move it around internally via pay(), and can withdraw back to their wallet
- There's no access control on deposit/pay/withdraw — any address can use them
- The owner field exists but isn't used in any modifier-gated function
- withdraw uses the reentrancy-safe pattern: balance is deducted before the external call
3b. Token.sol — ERC-20 Token Contract
State variables:
- name, symbol, decimals (18) — standard ERC-20 metadata
- totalSupply — total tokens in existence
- owner — deployer address
- balanceOf — address → uint256 mapping
- allowance — owner → spender → uint256 mapping (for delegated transfers)
Constructor: Mints initialSupply * 10^18 tokens to deployer. The Ignition module passes 1000000, so 1,000,000 STC is minted at deployment.
Functions:
Function	What it does
mint(to, amount)	Owner-only: creates amount * 10^18 new tokens, adds to balanceOf[to], increases totalSupply
transfer(to, amount)	Standard ERC-20: moves amount tokens from caller to to
approve(spender, amount)	Sets allowance[caller][spender] = amount
transferFrom(from, to, amount)	Delegated transfer: deducts from from, adds to to, deducts from allowance[caller][from]
Events:
- Transfer(address indexed from, address indexed to, uint256 value)
- Approval(address indexed owner, address indexed spender, uint256 value)
- Mint(address indexed to, uint256 value)
4. Deployment — Hardhat Ignition
File: ignition/modules/payment.ts
const PaymentModule = buildModule("PaymentModule", (m) => {
  const payment = m.contract("Payment");
  const token = m.contract("Token", ["Stable Coin", "STC", 1000000]);
  return { payment, token };
});
- Deploys Payment (no constructor args) and Token (name="Stable Coin", symbol="STC", initial supply=1,000,000)
- Saves deployed addresses to ignition/deployments/chain-31337/deployed_addresses.json
- The Payment contract is deployed by accounts[0] (the owner/deployer)
- The Token contract's owner is also accounts[0] — only this account can call mint()
Deployment command:
npx hardhat ignition deploy ./ignition/modules/payment.ts --network localhost
5. Python Backend — In Detail
5a. contract_utils.py — Utility Layer
Function	Purpose
get_web3()	Returns a Web3 instance connected to http://127.0.0.1:8545
load_abi(contract_name)	Reads artifacts/contracts/{name}.sol/{name}.json, extracts the abi field
get_contract(w3, contract_name, address)	Builds a w3.eth.contract object with the ABI and address
get_deployed_addresses()	Reads ignition/deployments/chain-31337/deployed_addresses.json
to_ether(wei)	Converts wei → ETH (for display)
to_wei(ether)	Converts ETH → wei (for transactions)
Path resolution: Uses Path(__file__).parent.parent to find the project root, so it works regardless of where the script is run from.
5b. app.py — Streamlit Dashboard
Initialization:
1. Connects to Hardhat node, checks w3.is_connected()
2. Loads deployed addresses from deployed_addresses.json
3. Creates contract objects for Payment and Token
4. Defines named accounts: Owner (index 0), Alice (1), Bob (2), Charlie (3), ..., Ivan (9)
Sidebar:
- Account selector dropdown — shows name + truncated address
- Selected account becomes sender for all operations
Balances section (3 columns):
- ETH wallet balance: w3.eth.get_balance(sender) — actual ETH in the account
- ETH in contract: payment.functions.getBalance(sender).call() — deposited ETH
- Token balance: token.functions.balanceOf(sender).call() / 10**18 — STC held
Tab 1 — ETH Payments:
Action	Contract Call	Parameters
Deposit ETH	payment.functions.deposit().transact({from, value})	Amount in ETH (converted to wei)
Send ETH	payment.functions.pay(receiver, amount).transact({from})	Receiver address + amount
Withdraw ETH	payment.functions.withdraw(amount).transact({from})	Amount in wei
Each action:
1. Calls the contract function via web3.py
2. Waits for receipt with w3.eth.wait_for_transaction_receipt(tx)
3. Shows success with truncated tx hash
4. Calls st.rerun() to refresh balances
Tab 2 — Token Payments:
- Transfer STC to another account via token.functions.transfer(receiver, amount * 10**18).transact({from})
- Displays token balances for first 5 accounts
Tab 3 — Transaction History:
Reads all past events using get_logs(from_block=0):
- payment.events.Deposit.get_logs() — all deposits
- payment.events.Withdrawal.get_logs() — all withdrawals
- payment.events.PaymentSent.get_logs() — all P2P payments
- token.events.Transfer.get_logs() — all token transfers (filters out mint events from 0x0000...)
For each event:
1. Fetches the block to get the timestamp
2. Builds a dict with block number, timestamp, type, sender, receiver (if applicable), amount, symbol
3. Sorts all events by block number
4. Writes a copy to transaction_log.json (for external consumption)
5. Displays in a human-readable format with block number, timestamp, and action description
5c. test_contract.py — CLI Test Script
Runs through the full flow programmatically (no UI):
1. Connects and lists accounts
2. Alice deposits 1 ETH → checks balances
3. Alice pays Bob 0.5 ETH → checks both balances
4. Alice withdraws 0.3 ETH → checks contract + wallet balance
5. Owner transfers 100 STC to Alice → Alice sends 50 STC to Bob
6. Prints full transaction history from the contract
6. Configuration
hardhat.config.ts:
- Solidity version: 0.8.34
- Plugin: @nomicfoundation/hardhat-ignition
- Network: localhost (default, port 8545) via Hardhat's built-in EVM
- Sepolia testnet config reads SEPOLIA_RPC_URL and PRIVATE_KEY from .env
package.json:
- Dependencies: hardhat, @nomicfoundation/hardhat-ignition, dotenv
- No scripts defined — all commands run via npx
7. Data Flow — Complete Transaction Lifecycle
User clicks "Send ETH Payment" in Streamlit
        │
        ▼
app.py reads: sender address, receiver address, amount
        │
        ▼
to_wei(amount) converts ETH → wei (integer)
        │
        ▼
payment.functions.pay(receiver, wei_amount).transact({from: sender})
        │
        ▼
web3.py builds a transaction object:
  { to: payment_contract_address,
    from: sender,
    data: encoded_function_call,
    gas: auto-estimated,
    nonce: auto-fetched }
        │
        ▼
Transaction is signed (Hardhat auto-unlocks accounts, no private key needed)
        │
        ▼
HTTP POST to http://127.0.0.1:8545
  Method: eth_sendRawTransaction
        │
        ▼
Hardhat node receives the raw transaction
        │
        ▼
Node validates: nonce, signature, gas, balance
        │
        ▼
EVM executes: Payment.pay(receiver, amount)
  - Checks balances[sender] >= amount
  - Deducts from balances[sender]
  - Adds to balances[receiver]
  - Pushes sender to transactionHistory
  - Emits PaymentSent event
        │
        ▼
Transaction is mined into a new block
        │
        ▼
Receipt returned:
  { transactionHash, blockNumber, gasUsed, status: 1, logs: [...] }
        │
        ▼
w3.eth.wait_for_transaction_receipt(tx) returns to app.py
        │
        ▼
st.success() shows confirmation
        │
        ▼
st.rerun() re-fetches all balances and events
        │
        ▼
UI updates with new values
8. Event System — How History Works
The contracts emit Solidity events, which are stored in transaction logs (not in contract storage — they're cheaper). Python reads them via eth_getLogs:
deposit_events = payment.events.Deposit.get_logs(from_block=0)
Each event object contains:
- blockNumber — which block it was mined in
- args — decoded event parameters (e.g., sender, amount)
- transactionHash — the tx that triggered it
The app then fetches the block for each event to get the timestamp, and builds a chronological display. This is more gas-efficient than storing history in the contract itself (though the contract does store transactionHistory — a simplified version).
9. Known Limitations & Notes
Aspect	Detail
Network	Local only — no testnet/mainnet deployment
Security	No private key management — Hardhat auto-unlocks all 20 accounts
Access control	Payment.sol has no restrictions on who can deposit/withdraw
Gas	Hardhat auto-estimates; no manual gas configuration
Contract history	transactionHistory in Payment.sol only stores addresses, not amounts or timestamps — the event-based approach in Python is more complete
Token minting	Only accounts[0] (deployer) can mint — no UI for minting
Reentrancy	Payment.sol's withdraw follows checks-effects-interactions pattern (safe)
wei precision	All contract math is in wei (integers); Python divides by 10^18 for display
transaction_log.json	Overwritten on each page load with all historical events