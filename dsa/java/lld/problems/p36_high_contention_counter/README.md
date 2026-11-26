# Design High-Contention Counter

> **Difficulty**: Hard  |  **Asked at**: Amazon, Cloudflare, Stripe
> **Patterns the source uses**: Striped counters (LongAdder pattern), CAS loops, Eventual consistency

Design a counter that supports high-throughput concurrent increment operations without becoming a bottleneck. A naive shared integer with a lock is a sequential bottleneck at high concurrency.

## In scope

1. `increment(delta=1)` — high-throughput, concurrent-safe
2. `decrement(delta=1)` — high-throughput, concurrent-safe
3. `get()` — returns approximate current value (may be slightly stale)
4. `reset()` — reset counter to 0

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/36-design-high-contention-counter.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
