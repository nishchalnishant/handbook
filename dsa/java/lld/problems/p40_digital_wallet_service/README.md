# Design a Digital Wallet Service

> **Difficulty**: Hard  |  **Asked at**: PayPal, Stripe, Square, PhonePe, Google Pay
> **Patterns the source uses**: Double-Entry Ledger, Idempotency Key + Dedupe Table, Lock Ordering (deadlock avoidance), Command (TransferRequest)

Design a digital wallet service (like PayPal/Venmo/PayTM) that lets a user hold a balance, transfer money to another user's wallet, and top up their wallet from a linked bank account. The system must guarantee money is never created or destroyed (conservation), never double-process a retried transfer (idempotency), and never deadlock when two wallets transfer to each other concurrently in opposite directions.

## In scope

1. Create a wallet for a user with a zero starting balance
2. Transfer money from one wallet to another, atomically, with an idempotency key
3. Top up a wallet from a linked bank account (external gateway call, then credit on confirmation)
4. Maintain a full double-entry transaction ledger — every money movement is two immutable rows (debit + credit) that net to zero
5. Retrieve transaction history for a wallet
6. Reject transfers that would take a wallet negative
7. Thread-safe, deadlock-free concurrent transfers, including two wallets transferring to each other simultaneously in opposite directions
8. Exactly-once processing of a transfer under client retries (same idempotency key)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/40-design-digital-wallet.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
