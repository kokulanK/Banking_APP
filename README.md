# 🏦 Mini Banking System
 
A console-based banking application built in Python that simulates real-world banking operations. Account data is persisted across sessions using **flat-file storage** (`bank_data.txt`), with separate workflows for **Customers** and a **Manager** — all driven by a simple terminal menu.
 
> Built as the first project for Unicom Tic — demonstrating Python fundamentals: file I/O, dictionaries, functions, loops, and input validation.
 
---
 
## 📋 Table of Contents
 
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [Role-Based Entry](#role-based-entry)
  - [Manager Section](#manager-section)
  - [Customer Section](#customer-section)
  - [Authentication System](#authentication-system)
  - [File Persistence](#file-persistence)
- [Getting Started](#getting-started)
- [Data File Format](#data-file-format)
- [Sample Walkthrough](#sample-walkthrough)
- [Known Limitations](#known-limitations)
- [License](#license)
---
 
## Overview
 
This project implements a **Mini Banking System** entirely in Python — no external libraries, no database. All account records are read from and written to `bank_data.txt` on every operation, so data survives between runs.
 
The system is split into two roles:
 
- **Customer** — can deposit, withdraw, check balance, view transaction history, and recover a forgotten password.
- **Manager** — protected by a PIN, can create accounts and apply interest across all accounts.
---
 
## Features
 
| Feature | Role | Description |
|---|---|---|
| Create Account | Manager | Register a new customer with name, password, PIN, and opening balance |
| Deposit Money | Customer | Add funds to any account by account number |
| Withdraw Money | Customer | Deduct funds after password authentication; checks for sufficient balance |
| Check Balance | Customer | View current balance after authentication |
| Transaction History | Customer | Full log of all deposits, withdrawals, interest credits, and password changes |
| Forget Password | Customer | Reset password via 4-digit security PIN (3 attempts allowed) |
| Calculate Interest | Manager | Apply 5% interest to all account balances in one operation |
| File Persistence | System | All data auto-saved to `bank_data.txt` after every operation |
| Input Validation | System | Handles invalid types, negative amounts, and wrong account numbers gracefully |
 
---
 
## Project Structure
 
```
Banking_APP/
├── FileHandlingwithbank.py   # Main application — all logic lives here
├── bank_data.txt             # Auto-generated data file; persists all account records
└── README.md
```
 
This is an intentionally single-file project — every function (account creation, auth, deposit, withdrawal, file I/O) is defined in `FileHandlingwithbank.py`.
 
---
 
## How It Works
 
### Role-Based Entry
 
On launch, the program loads `bank_data.txt` and presents a role selector:
 
```
=============================================
      Welcome To Mini Banking System
=============================================
Please select your role:
 [1] Customer
 [2] Manager
 [3] Exit
```
 
### Manager Section
 
The Manager section is protected by a hardcoded PIN (`123456`). Once authenticated, the manager can:
 
- **Create Account** — prompts for name, password, 4-digit security PIN, and initial deposit. Assigns an auto-incremented account number starting from `1000`.
- **Calculate Interest** — applies a flat **5% interest rate** to every account's current balance and logs the transaction.
### Customer Section
 
The Customer section presents a menu of 5 operations. Most require **password authentication** before proceeding:
 
```
======================================================
      Welcome To Mini Banking Customer Section
======================================================
1. Deposit Money
2. Withdraw Money
3. Check Balance
4. Transaction History
5. Forget the password
6. Exit
```
 
### Authentication System
 
Protected operations (withdraw, check balance, transaction history) call `authenticate()`, which:
 
1. Asks for the account number.
2. Greets the user by name.
3. Allows **3 password attempts** before locking out access.
Password recovery (`forget_password`) works similarly — it asks for the account number and then allows **3 PIN attempts** before denying access. On success, the user sets and confirms a new password. Each password change is counted and logged to the transaction history.
 
### File Persistence
 
Every write operation calls `save_data()`, which rewrites `bank_data.txt` from scratch with all current account states. On startup, `load_data()` parses the file back into the in-memory `accounts` dictionary.
 
The file stores one account block per record, separated by blank lines:
 
```
AccountCounter: 1002
 
Account Number: 1000
Created time is 2025-05-13 18:16:00
Name: Kokulan
Password: securePass
PIN: 1234
Balance: 15000.0
Password Changes: 1
Transactions:
 - Account created with initial balance: 10000.0
 - Deposited: 5000.0
 - Interest added: 750.0
 - Password changed count: 1
```
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.x (no third-party libraries required)
### Run
 
```bash
# Clone the repository
git clone https://github.com/kokulanK/Banking_APP.git
cd Banking_APP
 
# Run the application
python FileHandlingwithbank.py
```
 
`bank_data.txt` is created automatically on the first run if it doesn't exist.
 
---
 
## Data File Format
 
| Field | Type | Description |
|---|---|---|
| `AccountCounter` | int | Next account number to be assigned |
| `Account Number` | int | Unique ID, auto-incremented from 1000 |
| `Name` | str | Account holder's full name |
| `Password` | str | Plain-text password (see Known Limitations) |
| `PIN` | int | 4-digit security PIN for password recovery |
| `Balance` | float | Current account balance |
| `Password Changes` | int | Count of how many times the password was reset |
| `Transactions` | list | Chronological log of all account activity |
 
---
 
## Sample Walkthrough
 
```
# Step 1 — Manager creates an account
Role: [2] Manager
PIN: 123456
Choice: 1. Create Account
Name: Kokulan
Password: myPass123
Security PIN: 4567
Initial balance: 10000
 
→ Account created! Your account number is 1000
 
# Step 2 — Customer deposits money
Role: [1] Customer
Choice: 1. Deposit Money
Account number: 1000
Name confirmed → Choice: 1
Amount: 5000
 
→ Deposited 5000 successfully!
 
# Step 3 — Customer withdraws money
Choice: 2. Withdraw Money
Account number: 1000 | Password: myPass123
Amount: 2000
 
→ Withdrew 2000 successfully! Final balance: 13000.0
 
# Step 4 — Manager applies interest
Role: [2] Manager → 2. Calculate Interest
→ Interest added to all accounts (5%)
→ Account 1000 balance: 13650.0
```
 
---
 
## Known Limitations
 
These are acknowledged trade-offs of a first project, relevant to understand scope:
 
- **Plain-text passwords** — passwords are stored as-is in `bank_data.txt`. A production system would hash them with `bcrypt` or `hashlib`.
- **No concurrency control** — the flat-file model would break under simultaneous access; a real system uses a database with transactions.
- **Manager PIN is hardcoded** — `'123456'` is set directly in the source. This should come from a config or be hashed.
- **No account deletion** — accounts can be created but not removed.
- **Deposit doesn't require authentication** — the deposit function verifies the account name visually but doesn't require a password, unlike withdraw.
---
 
## License
 
This project is open-source and available under the [MIT License](LICENSE).
 
---

*Built by - Kokulan Kugathasan 
https://github.com/kokulanK 
+94 76 752 20033
kokulankugathasan2003@gmail.com
BSc (Hons) Information Technology, SLIIT Sri Lanka.*
