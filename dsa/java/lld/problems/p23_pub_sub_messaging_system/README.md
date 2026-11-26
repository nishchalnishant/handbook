# Design a Pub-Sub Messaging System

> **Difficulty**: Hard  |  **Asked at**: Amazon, Google, Meta
> **Patterns the source uses**: Observer, Strategy (delivery guarantee), Command (message processing)

Design a publish-subscribe messaging system where publishers send messages to named topics, subscribers consume messages, and the system provides configurable delivery guarantees and consumer group semantics.

## In scope

1. Publishers publish messages to named topics
2. Subscribers subscribe to topics; pull messages from their subscription
3. Consumer groups: each group sees every message; only one member in the group processes it
4. At-least-once delivery: unacknowledged messages redelivered after timeout
5. Dead letter queue after `max_retries` failed deliveries
6. Message ordering preserved per topic

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/23-design-pub-sub.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
