# Design a Vending Machine

> **Difficulty**: Medium  |  **Asked at**: Amazon, Google, Microsoft
> **Patterns the source uses**: State pattern (machine states), Strategy (payment), Command (dispense)

Design a vending machine that accepts item selection and coin/card payments, dispenses items and change, manages inventory, and handles the full transaction lifecycle through distinct states.

## In scope

1. Item selection with inventory check
2. Coin insertion and accumulation within a transaction
3. Purchase completion — dispense item + return change
4. Transaction cancellation — return all inserted coins
5. State machine: IDLE → ITEM_SELECTED → PAYMENT → DISPENSING → IDLE
6. Inventory management (decrement on successful purchase)
7. Change calculation using coin denominations

## How to use this folder

This folder now holds a **worked solution**. That makes the order matter:

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write your own code in this folder. `javac X.java && java X`.
3. **Only then** read `INTERVIEW.md` (the design spoken as a 45-minute answer)
   and `VendingMachine.java` (a complete, self-asserting implementation):

   ```
   javac VendingMachine.java && java VendingMachine
   ```

4. The original source key, for a third opinion:

   `../../../../SystemDesign/06-lld/06-problems/01-core-problems/04-design-vending-machine.md`

Reading either before you attempt turns production practice back into
reading — which is the exact gap this repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
