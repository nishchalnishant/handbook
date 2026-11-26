# Design Inventory Management System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Walmart, Shopify
> **Patterns the source uses**: Observer (stock alerts), Strategy (reservation), Optimistic locking (concurrent updates)

Design an inventory management system that tracks stock levels for products across multiple warehouses, handles reservations (soft holds during checkout), and fires low-stock alerts.

## In scope

1. Track stock per product per warehouse
2. Reserve stock (soft hold, time-bounded); release if not confirmed
3. Deduct stock permanently on order confirmation
4. Restock (add inventory)
5. Low-stock alerts via Observer when quantity falls below threshold
6. Stock movement history

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/24-design-inventory-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
