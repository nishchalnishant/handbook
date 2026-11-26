# Design Version Control System

> **Difficulty**: Hard  |  **Asked at**: Amazon, Google, Atlassian
> **Patterns the source uses**: Command (commit/checkout), Graph (DAG of commits), Composite (directory tree)

Design a Git-like version control system supporting repository initialization, file staging, committing with SHA-based content addressing, branching, checkout, and diff between two commits.

## In scope

1. `init()` — create a new repository
2. `stage(file_path, content)` — add file to staging area
3. `commit(message)` — snapshot staged files, return commit hash
4. `create_branch(name)` — create branch pointing to current commit
5. `checkout(branch_or_hash)` — switch HEAD
6. `diff(commit1_hash, commit2_hash)` — show added/removed/modified files
7. Content-addressed storage: SHA of content = object key
8. Branching: branch is a pointer to a commit hash

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/29-design-version-control.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **7 clarifying questions** in Phase 1 (the key asks 7)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
