# Design an Order Management System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Flipkart
> **Patterns the source uses**: State (order status), Saga (multi-step order flow), Observer (status notifications)

Design an order management system that handles placing orders, moving them through a lifecycle (placed → confirmed → shipped → delivered), deducting inventory, and supporting cancellations.

## In scope

1. Place orders with multiple items; reserve inventory at placement
2. Confirm order (deduct inventory, charge payment)
3. Ship order with a tracking number
4. Mark order delivered
5. Cancel order only if not yet shipped; release reserved inventory
6. Idempotency for order placement via client-supplied key
7. Status change notifications via Observer

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/21-design-order-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
