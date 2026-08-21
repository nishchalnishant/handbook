# Design Stack Overflow

> **Difficulty**: Medium  |  **Asked at**: Google, Meta, Amazon, Atlassian
> **Patterns the source uses**: Strategy (ranking), Observer (answer/comment notifications), State-ish (vote transitions), Composite (Question → Answer → Comment)

Design a Q&A platform where users post questions, other users post answers and comments, the community votes on questions and answers, question owners can accept a best answer, and content is tagged and searchable. The system must track reputation as a derived, vote-driven quantity and rank questions by relevance under a pluggable strategy.

## In scope

1. Post a question with title, body, and 1-5 tags
2. Post an answer to a question; post comments on questions and answers
3. Upvote/downvote questions and answers — one vote per user per post, changeable, not duplicable
4. Reputation system driven by vote and accept-answer events
5. Question owner accepts exactly one answer; acceptance is exclusive and revocable (accepting a different one un-accepts the old)
6. Tag-based filtering and simple keyword search over title/body
7. Pluggable ranking strategy (hot / top / newest) for listing questions
8. Notify question owner when a new answer is posted (and, extensibly, watchers)
9. Thread-safe voting under concurrent access

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/37-design-stack-overflow.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
