# Design Minesweeper

> **Difficulty**: Medium  |  **Asked at**: Amazon, Google, Meta
> **Patterns the source uses**: Flood Fill (BFS/DFS), State Machine (cell state), Factory (board setup)

Design the classic Minesweeper game. The player reveals cells on a grid; unrevealed mines explode and end the game; blank cells auto-expand via flood fill; revealed mine counts guide the player.

## In scope

1. Configurable grid: rows × cols with num_mines
2. Reveal a cell: mine → GAME_OVER; blank → BFS flood fill; numbered → show count
3. First click guaranteed safe (re-place mine if needed)
4. Flag/unflag cells
5. Win detection: all non-mine cells revealed

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/25-design-minesweeper.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
