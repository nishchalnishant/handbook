# Design a Car Rental System

> **Difficulty**: Medium  |  **Asked at**: Uber, Enterprise, Turo, Amazon
> **Patterns the source uses**: Strategy (pricing), Factory (vehicle creation), interval-overlap scheduling

Design a car rental system operating across multiple branches. Customers search for available vehicles by branch, category, and date range; reserve a vehicle in advance; pick it up (starting a rental agreement); and return it (which computes any late or damage fees). The system must never double-book the same physical vehicle for overlapping date ranges.

## In scope

1. Search available vehicles by branch, category, and date range
2. Create a reservation with an atomic availability check (no double-booking)
3. Pick up a vehicle — convert a reservation into an active `RentalAgreement`
4. Return a vehicle — compute base cost, late fee, and damage fee; close the agreement
5. Cancel a reservation before pickup
6. Pluggable pricing strategy per vehicle category
7. Thread-safe reservation creation across concurrent requests

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/41-design-car-rental.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
