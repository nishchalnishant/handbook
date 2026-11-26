# Design Mentorship Platform

> **Difficulty**: Medium  |  **Asked at**: Amazon, Coursera, LinkedIn
> **Patterns the source uses**: Strategy (matching), Observer (booking events), Conflict detection (interval overlap)

Design a mentorship platform where mentors set their availability, mentees book 1:1 sessions, and the system prevents double-booking.

## In scope

1. Mentors define weekly availability windows and specific date overrides
2. Mentees search available slots for a given mentor in a date range
3. Book a slot — prevents double-booking via conflict detection
4. Cancel a booking if more than 24 hours before session
5. All times stored in UTC

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/18-design-mentorship-platform.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
