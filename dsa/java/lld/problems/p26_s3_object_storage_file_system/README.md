# Design S3 Object Storage / File System

> **Difficulty**: Hard  |  **Asked at**: Amazon, Dropbox, Google
> **Patterns the source uses**: Composite (folder hierarchy), Metadata separation, Strategy (permissions)

Design a simplified S3-like object storage or hierarchical file system supporting bucket/folder/object operations, metadata management, and access control.

## In scope

1. Bucket create/delete
2. Object put (with metadata), get, delete
3. List objects in a bucket with optional prefix filter
4. Per-object and per-bucket ACL (READ, WRITE, DELETE permissions)
5. Metadata: content-type, size, checksum, tags

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/26-design-s3-object-storage.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **4 follow-ups** absorbed in Phase 6 (the key covers 4)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
