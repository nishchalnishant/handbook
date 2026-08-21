# Design an ATM System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Goldman Sachs
> **Patterns the source uses**: State (ATM states), Strategy (cash dispensing), Template Method (transaction flow)

Design an ATM system where a user can insert a card, authenticate with a PIN, check their balance, withdraw cash (selecting denominations), and deposit funds. The system transitions through well-defined states and interacts with a bank backend for account validation and fund management.

## In scope

1. Insert card → authenticate with PIN (up to 3 attempts)
2. Select transaction: withdraw, deposit, check balance
3. Withdrawal with denomination selection (greedy algorithm)
4. Deposit funds
5. Balance check
6. Eject card / end session
7. State machine enforcing valid operation sequences

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/12-design-atm.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
