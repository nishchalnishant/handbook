# Design Notification System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Uber, LinkedIn
> **Patterns the source uses**: Observer, Strategy (channel), Chain of Responsibility (retry/fallback)

Design a notification system that can send alerts to users via multiple channels (Email, SMS, Push), with preference-based routing and retry on failure.

## In scope

1. Send notifications via Email, SMS, Push
2. Route by user's channel preferences and opt-outs
3. Retry up to 3 times on failure; fall back to next channel
4. Simple template engine for notification content
5. Pluggable new channels without modifying existing code

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/16-design-notification-system.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
