# Amazon SDE-2 Interview Preparation Guide

This repository is a revision-first collection of core data structures and
algorithmic patterns for Amazon SDE-2-style interviews.

The files are organized so you can study in three passes:

1. **Pattern recognition:** Start with `L3_MASTER_GUIDE.md` and learn when each
   technique applies.
2. **Implementation recall:** Re-code the T1/T2 problems from memory until the
   template feels automatic.
3. **SDE-2 depth:** For the T2/L4-tagged problems, practice explaining the invariant,
   proof idea, edge cases, and complexity before writing code.

Amazon SDE-2 loop: **2 coding rounds + 1 system design round + 1–2 behavioral (LP) rounds**.
Coding rounds are ~45 min each; expect 1–2 medium problems per round, occasionally one hard.

For scope control, the advanced L4 sections (Bitmask DP, Digit DP, Advanced
Strings, Game Theory DP, Max Flow) are kept as reference but are **out of
Amazon SDE-2 scope** — do not prioritize them before your interview. This
branch (`leetcode-medium-only`) has additionally been pruned to keep only
**LeetCode Medium-difficulty** problems for focused interview revision; Easy
and Hard problems are intentionally removed here (they remain available on
`main`).

Segment Tree, Fenwick Tree (`data_structures/11_segment_tree_fenwick.py`), and
Bellman-Ford / Floyd-Warshall / Prim's (`algorithms/15_advanced_graph.py`) are
**Google-specific additions** — out of Amazon SDE-2 scope, but worth knowing
cold for Google loops, which go deeper on graphs and design-a-data-structure
questions.

## Repository Reading Contract

Each solved problem should be readable as interview revision material, not just
as accepted code. Use this structure when reviewing or adding solutions:

- **Problem header:** LeetCode number/name, difficulty tag (`T1`, `T2`, `L4`),
  short problem statement, example, constraints, time, and space.
- **Docstring:** `Approach`, `Key Insight`, `Gotchas`, and `Tricks`.
- **Code comments:** Comment invariants, boundary decisions, pruning rules, and
  non-obvious data-structure updates. Avoid comments that merely restate a line
  of code.
- **Tests:** Keep small executable examples in the file's `__main__` section so
  a topic can be revised and verified independently.

Good interview explanations should answer these questions:

- What is the brute-force solution and why is it too slow?
- What pattern unlocks the better solution?
- What invariant makes the algorithm correct?
- Which edge cases commonly break this solution?
- What are the exact time and space complexities?

## Local Verification

Run all topic checks from the repository root:

```bash
PYTHONPYCACHEPREFIX=/private/tmp/codex_pycache python3 - <<'PY'
import pathlib, subprocess, sys

for path in sorted(pathlib.Path('.').glob('**/*.py')):
    result = subprocess.run([sys.executable, str(path)], text=True)
    if result.returncode:
        raise SystemExit(f"Failed: {path}")

print("All revision examples passed.")
PY
```

## How to Approach a Coding Interview (Amazon SDE-2)

Amazon interviewers score on **correctness, code quality, communication, and LP signal**. Silent perfect code still fails if you don't communicate.

### 1. Clarify & Understand (2-3 minutes)
**Never start coding immediately.**
- Repeat the problem back in your own words.
- Ask about edge cases: *"Can the array be empty?"*, *"Are there negative numbers?"*, *"Does this need to handle duplicates?"*
- Confirm the expected output on a small example.

### 2. State the Brute Force (1-2 minutes)
- Quickly state the naive approach and its complexity: *"The brute-force is O(N²) with nested loops — we can do better."*
- This proves you can solve it and sets a baseline.

### 3. Plan the Optimal Solution (5-8 minutes)
- Think aloud: *"Since we're looking for subarrays, a sliding window or prefix-sum hash map gives O(N)."*
- State time and space complexity before coding.
- **Ask for permission:** *"I'll solve this with a hash map in O(N) time and O(N) space — does that work?"*

### 4. Implement (15-20 minutes)
- Talk while you type. Explain your logic, not every line.
- Use descriptive variable names (`max_profit`, not `m`).
- Write helper stubs (`def helper(): pass`) to maintain momentum.

### 5. Dry Run and Test (3-5 minutes)
- Walk through a small example line-by-line after coding.
- Catch your own bugs before the interviewer does — it's a strong signal.

### Amazon-Specific Tips
- Amazon values **working code** over partial elegant code. A clean O(N log N) solution that runs beats a broken O(N) attempt.
- Interviewers are often checking LP traits (Ownership, Dive Deep, Deliver Results) even in coding rounds — mention trade-offs and decisions explicitly.
- After solving, proactively discuss: *"One edge case I should handle is an empty input... Another follow-up could be to optimize space to O(1) by..."*

### The Golden Rule
Treat it as a **collaborative pair-programming session**. If stuck: *"I'm deciding between a heap and sorting first — heap gives O(N log K) but sorting simplifies the logic. I'll go with the heap."* Amazon interviewers will nudge you if needed.
