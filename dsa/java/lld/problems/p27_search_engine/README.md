# Design Search Engine (Inverted Index)

> **Difficulty**: Hard  |  **Asked at**: Amazon, Google, LinkedIn
> **Patterns the source uses**: Inverted Index, TF-IDF ranking, Strategy (tokenizer), Iterator (result pagination)

Design a simple search engine that indexes text documents, processes queries, and returns ranked results using TF-IDF scoring.

## In scope

1. Add / update / delete documents
2. Index documents using inverted index (term → postings list)
3. Search by keyword(s); return ranked results by TF-IDF score
4. Basic tokenization: lowercase, remove punctuation, split on whitespace

## How to use this folder

1. Open `ATTEMPT.md` and fill it in. Six phases, 45 minutes, out loud.
   Procedure: `../../../notes/THE_SCRIPT.md`.
2. Write the code in this folder. `javac X.java && java X`.
3. **Only then** open the answer key:
   `../../../../SystemDesign/06-lld/06-problems/04-advanced-niche/27-design-search-engine.md`

The key is a full worked solution with Java. Opening it before you attempt
turns production practice back into reading — which is the exact gap this
repo exists to close.

## Calibration

Before you look, you are aiming for roughly:

- **5 clarifying questions** in Phase 1 (the key asks 5)
- **5 follow-ups** absorbed in Phase 6 (the key covers 5)

If you asked 1 question and handled 0 follow-ups, that is the gap — not the code.
