# Design Unlock Pattern

> **Difficulty**: Medium  |  **Asked at**: Amazon, Google, LeetCode (Android Unlock Pattern)
> **Patterns the source uses**: DFS / Backtracking, Adjacency constraint validation, Graph traversal

Design the Android unlock pattern system. A 3×3 grid of dots (numbered 1–9). The user draws a pattern by connecting dots. Count (or validate) all valid patterns of a given length, subject to skip constraints.

## In scope

1. Count all valid unlock patterns of length m to n (1 ≤ m ≤ n ≤ 9)
2. Validate whether a given sequence of dot indices is a valid unlock pattern
3. Precompute the "skip" map: if going from A to B skips through C, C must be visited

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/33-design-unlock-pattern.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
