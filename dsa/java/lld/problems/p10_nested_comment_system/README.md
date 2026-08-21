# Design a Nested Comment System

> **Difficulty**: Medium  |  **Asked at**: Amazon, Meta, Twitter
> **Patterns the source uses**: Composite (tree of comments), Strategy (sort), Observer (notifications)

Design a nested comment system like Reddit or YouTube where users can post comments on content, reply to existing comments forming a thread tree, like comments, and retrieve comments sorted by time or popularity.

## In scope

1. Add a top-level comment to a post
2. Reply to an existing comment (nested, unlimited depth)
3. Like / unlike a comment (unique per user, toggleable)
4. Delete a comment (soft delete — content replaced, replies preserved)
5. Retrieve all comments for a post sorted by time or likes
6. Preserve nested structure in retrieval

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/02-frequent-problems/10-design-comment-system.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
