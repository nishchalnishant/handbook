# Design a Food Delivery System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Uber, DoorDash
> **Patterns the source uses**: State (order lifecycle), Observer (tracking), Strategy (delivery assignment)

Design a food delivery platform like Swiggy or DoorDash where users can browse restaurant menus, add items to a cart, place orders, and track them through preparation and delivery. The system assigns a delivery agent to each order and updates order status in real time.

## In scope

1. Browse restaurant menus; add items to cart
2. Place order from cart
3. Order moves through status lifecycle: PLACED → CONFIRMED → PREPARING → PICKED_UP → DELIVERED
4. Delivery agent automatically assigned when order is confirmed
5. Update order status (by restaurant or agent)
6. Cancel order (only before PREPARING)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/14-design-food-delivery.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
