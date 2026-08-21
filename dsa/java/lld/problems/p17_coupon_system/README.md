# Design Coupon System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Shopify, DoorDash
> **Patterns the source uses**: Composite (coupon stacking), Chain of Responsibility (validation), Strategy (discount type)

Design a coupon and discount system for an e-commerce platform that supports percentage, fixed-amount, and free-shipping discounts, with validation rules and stacking limits.

## In scope

1. Coupon types: PERCENTAGE, FIXED_AMOUNT, FREE_SHIPPING
2. Validation: expiry date, minimum order value, per-user usage limit
3. Scope: order-wide, per-category, per-product
4. At most one product coupon + one shipping coupon per order
5. Apply discounts to the order total; return itemized breakdown

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/17-design-coupon-system.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
