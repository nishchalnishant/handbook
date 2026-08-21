# Design Tic-Tac-Toe

> **Difficulty**: Easy  |  **Asked at**: Amazon, Apple, Airbnb
> **Patterns the source uses**: Strategy (win checker), State enum, counter-based O(1) win detection

Design a two-player Tic-Tac-Toe game on an NxN board where players alternate placing marks, and the system detects wins (row, column, diagonal) and draws after each move.

## In scope

1. NxN board, configurable at construction
2. Two players alternate turns (X goes first)
3. `make_move(player, row, col)` — validates and applies a move
4. Win detection after each move (row, column, two diagonals)
5. Draw detection when board is full with no winner
6. Game state tracking: IN_PROGRESS, X_WINS, O_WINS, DRAW

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/01-core-problems/03-design-tic-tac-toe.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
