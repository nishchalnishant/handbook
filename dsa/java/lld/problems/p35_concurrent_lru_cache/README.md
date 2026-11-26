# Design Concurrent LRU Cache

> **Difficulty**: Hard  |  **Asked at**: Amazon, Google, Uber
> **Patterns the source uses**: LRU eviction (DoublyLinkedList + HashMap), Striped locking (segment-level), Thread safety

Design a thread-safe LRU cache with O(1) get/put. Support concurrent access from multiple threads without a single global lock (which would serialize all requests).

## In scope

1. `get(key)` → value or None; moves key to MRU position
2. `put(key, value)` → insert/update; evict LRU if at capacity
3. Thread-safe under concurrent access
4. O(1) get and put

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/35-design-concurrent-lru-cache.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
