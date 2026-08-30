# Project Details - Payment POC

> This file is a live learning log. Every time we learn something new about the project,
> its tools, or its concepts, we add it here.

## Current State

- Hardhat 3 project (minimal setup, no plugins)
- TypeScript + Solidity
- Single contract: `contracts/payment.sol`

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

Example from this project:
```ts
import { defineConfig } from "hardhat/config";

export default defineConfig({
  solidity: {
    version: "0.8.34",
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
| `hardhat.config.ts` | Compiler version + project settings |
| `contracts/payment.sol` | The only smart contract (payment system placeholder) |
| `artifacts/` | Compiler output (ABI + bytecode) |
| `cache/` | Hardhat's recompile cache |
| `package.json` | Node project metadata + deps |
| `tsconfig.json` | TypeScript compiler settings |
| `README.md` | Project readme |

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