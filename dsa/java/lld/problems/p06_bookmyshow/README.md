# Design BookMyShow

> **Difficulty**: Hard  |  **Asked at**: Amazon, Flipkart, Paytm
> **Patterns the source uses**: State (booking status), Strategy (payment), TTL-based seat locking, Template Method (booking flow)

Design a movie ticket booking system where users can browse shows, select and temporarily lock seats, pay to confirm their booking, and cancel if needed — with the system preventing double-booking under concurrent load.

## In scope

1. Browse shows for a movie
2. Lock seats for a TTL window (10 minutes) before payment
3. Confirm booking — process payment, finalize booking
4. Cancel booking with refund per cancellation policy
5. Release expired seat locks (lazy or scheduled)
6. BookingStatus state machine: PENDING → CONFIRMED → CANCELLED
7. Prevent double-booking under concurrent access

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/06-design-bookmyshow.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
