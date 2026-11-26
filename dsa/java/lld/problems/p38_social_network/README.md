# Design a Social Network (LinkedIn / Facebook)

> **Difficulty**: Hard  |  **Asked at**: Meta, LinkedIn, Google, Amazon
> **Patterns the source uses**: Observer (feed/notification fan-out), Strategy (feed ranking), State (connection lifecycle)

Design a simplified social network where users send and accept mutual connection requests (like Facebook friends, not one-way Twitter/Instagram follows), create posts, and view a news feed aggregating posts from their connections. The system must handle the connection request lifecycle correctly and generate feeds efficiently as the connection graph grows.

## In scope

1. Send, accept, and reject connection requests (mutual, state-machine driven)
2. Prevent duplicate/spam connection requests between the same pair of users
3. Create text/media posts with visibility scope (CONNECTIONS or PUBLIC)
4. Like and comment on posts
5. Generate a news feed for a user: posts from all accepted connections, chronologically ordered
6. Pluggable feed ranking strategy (chronological now, engagement-based later)
7. Thread-safe connection state transitions and feed reads under concurrent writes

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/38-design-social-network.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
