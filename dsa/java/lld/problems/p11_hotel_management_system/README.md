# Design a Hotel Management System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Booking.com
> **Patterns the source uses**: Factory (room types), State (room/reservation status), Strategy (pricing)

Design a hotel booking system where guests can search for available rooms by type and date range, make reservations, check in and check out, and receive a bill based on their stay duration and room pricing.

## In scope

1. Search available rooms by type and date range
2. Create a reservation for a guest
3. Check in (marks room OCCUPIED)
4. Check out (marks room AVAILABLE, generates bill)
5. Cancel a reservation
6. Prevent double-booking (date range overlap detection)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/11-design-hotel-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
