# Design Download Manager

> **Difficulty**: Hard  |  **Asked at**: Amazon, BitTorrent, Mozilla
> **Patterns the source uses**: Thread pool (parallel chunks), State Machine (download lifecycle), Strategy (retry)

Design a download manager that downloads large files in parallel chunks using HTTP Range requests, tracks progress, supports pause/resume, and merges chunks into a final file.

## In scope

1. Download a file in N parallel chunks using HTTP Range requests
2. Track download progress per chunk and overall
3. Pause / resume downloads
4. Retry failed chunks (up to 3 times with backoff)
5. Merge chunks in order after all complete

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/32-design-download-manager.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
