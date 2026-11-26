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

This folder now holds a **worked solution**. That makes the order matter:

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write your own code in this folder. `javac X.java && java X`.
3. **Only then** read `INTERVIEW.md` (the design spoken as a 45-minute answer)
   and `Chess.java` (a complete, self-asserting implementation):

   ```
   javac Chess.java && java Chess
   ```

4. The original source key, for a third opinion:

   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/07-design-chess.md`

Reading either before you attempt turns production practice back into
reading — which is the exact gap this repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
