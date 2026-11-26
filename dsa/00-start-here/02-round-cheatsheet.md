---
module: 00-start-here
topic: Round Cheatsheet
tags: [cheatsheet, round-execution, revision]
---
# Round Cheatsheet — Execution & Revision

## What this covers

> [!abstract] In this file
> **Covers:** The 45-minute plan, universal edge cases, what to skip at L3, what Google scores, how to talk, and 7-day / 48-hour / night-before revision plans.
> **You'll be able to:** Run every round on the same clock and plan the final week.
> **Prereqs:** None · **Pair with:** [Complexity & Python](../01-foundations/02-complexity-and-python.md) · [Pattern sheet](../05-review/01-pattern-sheet.md) · [Roadmap](01-roadmap.md) · **Time:** 20 min (reread before every mock)

**Sections:** [1. 45-Minute Execution Plan](#1-45-minute-execution-plan) · [2. Choosing the pattern](#2-choosing-the-pattern) · [3. Universal edge cases](#3-universal-edge-cases) · [4. What to skip at L3](#4-what-to-skip-at-l3) · [Round cheatsheet (one page)](#round-cheatsheet-one-page) · [Communication (how to sound clear at Google)](#communication-how-to-sound-clear-at-google) · [Revision schedules](#revision-schedules) · [After the interview](#after-the-interview)

---

## 1. 45-Minute Execution Plan
- **Min 0-5 (Clarify & De-risk):** Listen, repeat, clarify edge cases (empty, negative, cycles, memory), write a custom tricky example.
- **Min 5-15 (Design):** State brute force, reverse-engineer constraints, pitch optimal solution (draw it out). Get green light before coding.
- **Min 15-35 (Code):** Write clean, modular, bug-free code. Stop talking to focus. Use helper functions.
- **Min 35-45 (Dry Run & Big-O):** Trace code line-by-line with custom example. State Time/Space complexity. Fix bugs gracefully.

## 2. Choosing the pattern

Keywords → technique: [Pattern sheet — quick decision trees](../05-review/01-pattern-sheet.md#quick-decision-trees). Constraint → target complexity: [Complexity budget](../01-foundations/02-complexity-and-python.md#1-constraint--complexity-budget).

## 3. Universal edge cases
- **General:** Empty input, single element, all identical, negative values, integer max bounds.
- **Array:** Already sorted, reverse sorted, duplicates.
- **String:** Case sensitivity, whitespace, special chars.
- **Linked List:** `None` head, single node, cycles, even/odd lengths.
- **Trees:** Skewed tree (O(n) height), `None` root, disconnected graphs, graph with cycles.
- **Binary Search:** Off-by-one bounds (`lo <= hi`), infinite loops (`mid = (lo+hi)//2`).

## 4. What to skip at L3
- **Do NOT study:** Segment Trees, Fenwick Trees (BIT), Tarjan/Kosaraju SCC, Floyd-Warshall, Bitmask/Digit DP, System Design. (They live in the repo as `💤 T3` — [Range Queries](../03-algorithms/15-range-queries.md), [DP practice](../04-practice/algorithms/08-dynamic-programming.md) — for L4+ or hard-round companies.) (Focus heavily on BFS/DFS, Heaps, Two Pointers, Binary Search instead).

---
## Round cheatsheet (one page)

### What Google looks for (coding round)

- **Problem-solving**: Clarify → brute force → optimize → code → test → complexity.
- **Communication**: Think out loud; state assumptions; ask about constraints (empty input, duplicates, size limits).
- **Code quality**: Clear names, handle edge cases, correct complexity analysis.

### Topic priority (typical frequency)

| Priority | Topics | Patterns to nail |
|----------|--------|------------------|
| **1** | Arrays, Strings, Hashing | Two pointers, sliding window, prefix sum + map, frequency map |
| **2** | Trees, Graphs | BFS/DFS, LCA, topo sort, shortest path (BFS / Dijkstra) |
| **3** | DP | 1D recurrence, 2D (LCS/grid), interval DP basics |
| **4** | Heap, Binary Search | Top-K, merge K lists, BS on answer, rotated array |
| **5** | Stack/Queue | Monotonic stack, monotonic deque |

### Complexity you must state correctly

Sound bites — say them exactly like this:

- “We visit each node/edge at most once → **O(V + E)**” (BFS/DFS); Dijkstra: **O((V + E) log V)** with min-heap.
- “Sorting dominates → **O(N log N)**.”
- “Hash map gives O(1) average lookup, so overall **O(N)**.”
- “Binary search on answer: O(N) check per mid × O(log range) mids → **O(N log range)**.”
- Sliding window: usually **O(N)** time.

### Open with / Close with

**Open:** repeat the problem in your words; ask — size limits? duplicates? can we modify input?
**Close:** state time and space; run two test cases (normal + edge); name a follow-up (stream, huge n).

---

## Communication (how to sound clear at Google)

1. **Start:** “Let me restate the problem and confirm constraints: can the array be empty? Are numbers non-negative?”
2. **Brute force:** “A naive approach would be O(…) because …”
3. **Optimize:** “We can improve by … which brings it to O(…) because …”
4. **While coding:** Narrate non-obvious indices and invariants (“`left` is always the start of the valid window”).
5. **End:** “Time is O(…), space is O(…). Edge cases: empty input, single element, …”

If stuck: “I’m considering BFS vs DFS — for shortest path in an unweighted graph I’ll use BFS because…”

---

## Revision schedules

### If you have 7 days

| Day | Focus | Action |
|-----|--------|--------|
| 1 | Arrays + hashing | Review [array](../02-data-structures/01-array.md) + [hashing](../02-data-structures/02-hashing.md); 4 problems |
| 2 | Strings + two pointers | [string](../02-data-structures/03-string.md) + sliding window pattern; 4 problems |
| 3 | Trees + BST | [tree](../02-data-structures/08-tree.md); 3 problems |
| 4 | Graphs | [graph](../02-data-structures/11-graphs.md); BFS/DFS/topo; 4 problems |
| 5 | DP | [DP](../03-algorithms/08-dynamic-programming.md) + [recursion → DP](../03-algorithms/07-recursion-to-dp.md); 4 problems |
| 6 | Heap + binary search + stack | [heap](../02-data-structures/10-heap.md), [binary search](../03-algorithms/04-binary-search.md), [stack](../02-data-structures/05-stack.md); 4 problems |
| 7 | Mixed mock | 2 timed problems (45 min each) + review mistakes |

### If you have 48 hours

- **Hour 0–4:** [this cheatsheet](#1-45-minute-execution-plan) + redo 2 Medium problems you failed recently.
- **Hour 4–12:** Skim Quick Revision in: array, tree, graph, DP, heap, binary search.
- **Hour 12–24:** One full mock (2 problems); note gaps only.
- **Hour 24–36:** Only gaps + Union-Find + topo sort if weak.
- **Hour 36–48:** Sleep, light review of the round cheatsheet, no new problems.

### Night before

- Skim the **round cheatsheet** (edge cases, Big-O).
- Do **not** cram new topics; review **one** problem per weak area only.
- Prepare 2–3 questions for your interviewers (team, code review, on-call).

---

## After the interview

- Jot down problems you saw (titles only) while memory is fresh — helps if you have future rounds.
- Regardless of outcome, note **one** pattern to drill next time.

---
