# Design a Restaurant Management System

> **Difficulty**: Medium  |  **Asked at**: OpenTable, Toast, Swiggy, DoorDash
> **Patterns the source uses**: State (order-item lifecycle), Observer (kitchen display notifications), Strategy (bill splitting)

Design a restaurant management system that handles dine-in table assignment/reservation, order taking against a categorized menu, routing order items to the kitchen as tickets, tracking each item through preparation to served, and generating a bill at the end of the meal — including splitting the bill across multiple guests.

## In scope

1. Assign a walk-in table or reserve a table for a future time window; prevent overlapping reservations for the same table
2. Browse a categorized menu with per-item availability
3. Place an order for a table — creates order items, each independently tracked
4. Kitchen ticket routing: new orders notify a Kitchen Display System via Observer
5. Order-item status lifecycle enforced as a state machine: `PLACED → IN_KITCHEN → READY → SERVED → PAID`
6. Generate a bill with tax; support even split across guests and itemized split by guest assignment
7. Mark menu items unavailable and handle in-flight orders for items that go out of stock
8. Thread-safe table reservation and order-item status transitions

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/42-design-restaurant-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
