# Design a Library Management System

> **Difficulty**: Medium  |  **Asked at**: Amazon, TCS
> **Patterns the source uses**: State (book copy status), Strategy (fine calculation), Observer (reservation notifications)

Design a library management system where members can search for books, borrow and return physical copies, receive fines for late returns, and reserve books when all copies are checked out.

## In scope

1. Catalog: books with multiple physical copies per title
2. Members borrow copies; each copy tracks its own status (AVAILABLE, CHECKED_OUT, RESERVED, LOST)
3. Return triggers fine calculation for overdue copies
4. Reservation queue per book; first reserver notified on return
5. Membership tiers: standard (3 books) and premium (10 books)
6. Block borrowing if member has overdue books or unpaid fines

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/20-design-library-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
