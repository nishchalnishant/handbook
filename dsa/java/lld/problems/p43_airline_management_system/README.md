# Design an Airline Management System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Google, Uber, Expedia
> **Patterns the source uses**: State (Seat lifecycle), Strategy (fare pricing), Factory (seat map construction), Observer (waitlist notification)

Design the core booking engine of an airline management system: search flights, hold a seat temporarily while the passenger enters payment details, confirm the booking once payment succeeds, and release the hold if payment doesn't complete in time. The system must guarantee that no two passengers are ever confirmed onto the same seat, even under heavy concurrent demand (e.g., a popular route going on sale).

## In scope

1. Search flights by origin, destination, and date
2. View seat map for a flight with availability per seat class
3. Hold a seat temporarily (TTL-based lock) while the passenger completes payment
4. Confirm a booking — convert a valid hold into a confirmed booking backed by a successful payment
5. Automatically expire and release holds that aren't confirmed within the TTL window
6. Cancel a confirmed booking — refund payment, free the seat
7. Support ECONOMY and BUSINESS seat classes with independent pricing
8. Thread-safe seat hold/confirm/release under concurrent access

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/43-design-airline-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
