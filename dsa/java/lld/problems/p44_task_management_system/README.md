# Design a Task Management System

> **Difficulty**: Medium  |  **Asked at**: Atlassian, Asana, Meta, Microsoft
> **Patterns the source uses**: Observer (activity log/notifications), Command (undo/redo task moves), State (status transitions)

Design a task management system like Jira/Trello/Asana: users create boards, boards contain columns (lists) representing workflow stages, and tasks live in columns and move between them. Tasks can be assigned to users, have due dates and priority, support comments, and every change is recorded in an activity log. The system must handle concurrent edits from multiple users safely.

## In scope

1. Create boards with a fixed set of columns (TODO, IN_PROGRESS, IN_REVIEW, DONE)
2. Create tasks within a column; set title, description, due date, priority
3. Move a task between columns, enforcing valid status transitions
4. Assign a task to a single user
5. Add comments to a task
6. Maintain an activity log per task (status changes, assignment changes, comments)
7. Notify interested parties (assignee) on task changes via Observer
8. Thread-safe concurrent task updates using optimistic locking (version field)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/06-additional-problems/44-design-task-management.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **3 follow-ups** absorbed in Phase 6 (the key covers 3)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
