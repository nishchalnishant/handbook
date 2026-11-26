# Design a Ride Sharing System

> **Difficulty**: Hard  |  **Asked at**: Amazon, Uber, Lyft
> **Patterns the source uses**: State (ride status), Strategy (matching/fare), Observer (driver location updates)

Design a ride-sharing platform where riders request rides, the system matches them to a nearby available driver, tracks the ride through pickup and drop-off, calculates the fare, and allows both parties to rate each other.

## In scope

1. Rider requests a ride with pickup and dropoff location
2. System matches nearest available driver
3. Driver accepts or rejects; if rejected, try next closest
4. Ride lifecycle: REQUESTED → MATCHED → IN_PROGRESS → COMPLETED / CANCELLED
5. Fare calculated on completion (base + distance + time)
6. Mutual rating (rider rates driver, driver rates rider)
7. Driver state machine: OFFLINE → AVAILABLE → ON_RIDE

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/22-design-ride-sharing.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
