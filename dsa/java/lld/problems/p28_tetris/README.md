# Design Tetris

> **Difficulty**: Hard  |  **Asked at**: Amazon, Intuit
> **Patterns the source uses**: Factory (tetromino types), Strategy (rotation), Command (move/rotate/drop)

Design the core game engine for Tetris: spawning falling tetromino pieces, detecting collisions with the board and existing blocks, clearing completed lines, tracking score, and managing the game loop until the board fills up.

## In scope

1. Spawn all 7 tetromino types using a factory
2. Move pieces left, right, down; rotate 90 degrees clockwise/counter-clockwise
3. Collision detection with board edges and locked pieces
4. Lock piece when it can no longer fall
5. Clear completed lines and shift rows down
6. Score based on lines cleared (1/2/3/4 -> 100/300/500/800 x level)
7. Level progression increases gravity speed
8. Next piece preview queue
9. Hard drop and soft drop
10. Game over detection when spawn position is blocked

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/28-design-tetris.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
