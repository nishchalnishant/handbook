# Design Snake and Ladder

> **Difficulty**: Easy  |  **Asked at**: Amazon, Intuit
> **Patterns the source uses**: Strategy (dice), Observer (position events), Factory (board setup)

Design a Snake and Ladder board game for 2 or more players, with a configurable board of snakes and ladders, dice rolling, and win detection.

## In scope

1. 2–4 players take turns rolling a dice and moving
2. Landing on a snake head moves the player to the snake's tail (lower cell)
3. Landing on a ladder base moves the player to the ladder's top (higher cell)
4. Exact roll required to land on cell 100 to win
5. Invalid config (snake head == ladder base at same cell) is rejected at setup

## How to use this folder

This folder now holds a **worked solution**. That makes the order matter:

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write your own code in this folder. `javac X.java && java X`.
3. **Only then** read `INTERVIEW.md` (the design spoken as a 45-minute answer)
   and `SnakeAndLadder.java` (a complete, self-asserting implementation):

   ```
   javac SnakeAndLadder.java && java SnakeAndLadder
   ```

4. The original source key, for a third opinion:

   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/08-design-snake-and-ladder.md`

Reading either before you attempt turns production practice back into
reading — which is the exact gap this repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
