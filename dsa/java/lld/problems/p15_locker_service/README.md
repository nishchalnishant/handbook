# Design Locker Service

> **Difficulty**: Medium  |  **Asked at**: Amazon, DoorDash, Shopify
> **Patterns the source uses**: Strategy (size matching), Inheritance (locker sizes), Factory

Design a package locker service (like Amazon Locker) where customers can pick up deliveries. Couriers drop packages into available lockers, customers get a code to retrieve them.

## In scope

1. Assign an available locker of the right size (or larger) to a package
2. Generate a unique PIN for the customer
3. Customer enters PIN to retrieve package; locker frees
4. Locker expiry after 3 days frees the locker
5. Handle no available locker gracefully

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/15-design-locker-service.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
