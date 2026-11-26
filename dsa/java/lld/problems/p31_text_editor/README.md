# Design Text Editor

> **Difficulty**: Hard  |  **Asked at**: Amazon, Microsoft, Dropbox
> **Patterns the source uses**: Command Pattern (undo/redo), Gap Buffer (efficient insert/delete at cursor)

Design the backend of a text editor supporting efficient insert, delete, cursor movement, undo/redo, and text search.

## In scope

1. Insert character / string at cursor
2. Delete character (backspace at cursor)
3. Move cursor (left, right)
4. Undo / redo (up to 100 levels)
5. Get current content as string
6. Cursor position tracking

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/31-design-text-editor.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
