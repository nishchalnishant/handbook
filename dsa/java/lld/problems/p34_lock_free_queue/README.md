# Design Lock-Free Queue

> **Difficulty**: Hard  |  **Asked at**: Amazon, Jane Street, Two Sigma
> **Patterns the source uses**: Compare-and-Swap (CAS), ABA problem, Michael-Scott queue algorithm

Design a lock-free FIFO queue that supports concurrent enqueue and dequeue operations without using mutexes or locks, using Java's real hardware-backed CAS primitive (`AtomicStampedReference`) — the JVM equivalent of C++'s `std::atomic`.

## In scope

1. Thread-safe enqueue (tail insert)
2. Thread-safe dequeue (head remove)
3. Non-blocking — return None if empty, no busy-wait beyond CAS retries
4. Explain Michael-Scott queue algorithm
5. Explain and handle the ABA problem

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/34-design-lock-free-queue.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
