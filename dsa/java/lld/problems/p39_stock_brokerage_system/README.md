# Design a Stock Brokerage System

> **Difficulty**: Hard  |  **Asked at**: Robinhood, Bloomberg, Goldman Sachs, Morgan Stanley
> **Patterns the source uses**: Strategy (order execution), Observer (price-triggered limit orders), Command (order lifecycle)

Design an online stock brokerage system where users hold a cash account, place market and limit orders to buy/sell stocks, and see their portfolio update as orders execute. The system must guarantee an account never spends more cash than it has available, execute market orders immediately against a live quote, and hold limit orders until the market price crosses the specified threshold.

## In scope

1. Place market orders (buy/sell) — execute immediately against the current quote
2. Place limit orders (buy/sell) — hold as PENDING until price crosses limit, then execute
3. Validate and lock buying power at order placement time; release on cancel, debit on execution
4. Cancel a pending limit order
5. Track portfolio holdings per account: quantity and running average cost per stock
6. React to quote/price updates and trigger eligible limit orders (Observer)
7. Thread-safe fund locking and order execution under concurrent access

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/39-design-stock-brokerage.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
