# Design Chess

> **Difficulty**: Hard  |  **Asked at**: Amazon, Google, Jane Street
> **Patterns the source uses**: Polymorphism (piece hierarchy), State enum, Template Method

Design a two-player chess game with all piece types, legal move validation (including check), and end-game detection (checkmate and stalemate).

## In scope

1. Two players alternate turns, White moves first
2. Each piece type enforces its own legal moves
3. A move is rejected if it leaves the moving side's king in check
4. Detect check, checkmate (game over — opponent wins), stalemate (draw)
5. Invalid moves are rejected clearly

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/07-design-chess.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
