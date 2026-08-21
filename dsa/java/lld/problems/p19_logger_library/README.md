# Design a Logger Library

> **Difficulty**: Medium  |  **Asked at**: Amazon, Google
> **Patterns the source uses**: Chain of Responsibility (log level filtering), Strategy (sink/appender), Singleton (logger instance)

Design a logging library that allows applications to emit log messages at different severity levels (DEBUG, INFO, WARN, ERROR) and route them to multiple configurable output sinks such as console, file, and remote endpoints.

## In scope

1. Log messages at four severity levels: DEBUG, INFO, WARN, ERROR
2. Global minimum log level threshold on the Logger
3. Multiple handlers (Console, File, Remote) each with their own level filter
4. Pluggable Formatter per handler (text, JSON)
5. Thread-safe logging
6. Log rotation for FileHandler (size-based)

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/03-domain-specific/19-design-logger-library.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **6 clarifying questions** in Phase 1 (the key asks 6)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
