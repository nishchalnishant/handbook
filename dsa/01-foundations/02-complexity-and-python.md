---
module: 01-foundations
topic: Complexity & Python Toolkit
tags: [complexity, big-o, python, foundations]
---
# Complexity & Python Toolkit

## What this covers

> [!abstract] In this file
> **Covers:** Reading the target complexity off the constraints, Big-O of every core structure and pattern, complexity traps, and the Python standard-library calls you will write in every round.
> **You'll be able to:** Pick the target complexity from n before choosing an approach, and state time/space correctly.
> **Prereqs:** None · **Pair with:** [How to think](01-how-to-think.md) · [Round cheatsheet](../00-start-here/02-round-cheatsheet.md) · **Time:** 30 min

**Sections:** [1. Constraint → complexity budget](#1-constraint--complexity-budget) · [2. Big-O reference](#2-big-o-reference) · [3. Complexity gotchas](#3-complexity-gotchas) · [4. Python whiteboarding essentials](#4-python-whiteboarding-essentials) · [See Also](#see-also)

---

## 1. Constraint → complexity budget
A budget of about 10⁸ simple operations per second is a safe rule.

| n up to | Budget | Typical techniques |
|---|---|---|
| ≤ 10–12 | O(n!) or O(nⁿ) | Permutations, brute-force backtracking |
| ≤ 20 | O(2ⁿ · n) | Subsets, bitmask DP |
| ≤ 40 | O(2^(n/2)) | Meet in the middle `💤 T3` |
| ≤ 100–500 | O(n³) | Floyd–Warshall, interval DP / MCM |
| ≤ 10³–5·10³ | O(n²) | 2D DP (LCS, edit distance), all pairs |
| ≤ 10⁵–10⁶ | O(n log n) | Sort, binary search, heap, Dijkstra |
| ≤ 10⁷–10⁸ | O(n) | Two pointers, sliding window, prefix sums, hashing, monotonic stack, sieve |
| ≥ 10⁹ (a value, not a length) | O(log n) or O(√n) | Binary search on the answer, binary exponentiation, √n divisor loop, maths |
| 10¹⁸ | O(log n) or digit count | Closed form, binary exponentiation; digit DP / matrix power `💤 T3` |

| Other constraint signal | Implication |
|---|---|
| "Answer modulo 10⁹+7" | Counting DP or combinatorics |
| Values ≤ 10⁵ but n large | Counting array or bucket instead of a hashmap; sieve |
| Sum of n over tests ≤ 2·10⁵ | Per-test cost must be linear in that test's n |
| Grid m·n ≤ 10⁵ | BFS/DFS over cells, O(mn) |
| Q queries ≥ 10⁵ | Precompute (prefix sums) or O(log n) per query via sort + binary search |

## 2. Big-O reference
### Data structures

| Structure | Insert | Search | Delete | Notes |
| :--- | :--- | :--- | :--- | :--- |
| Array | O(1) tail | O(n) | O(n) | Random access O(1) |
| Hash map | O(1)* | O(1)* | O(1)* | *amortized average |
| Stack / Queue | O(1) | — | O(1) | |
| Linked list | O(1) head | O(n) | O(n) | |
| Binary heap | O(log n) | O(1) peek | O(log n) | |
| BST (balanced) | O(log n) | O(log n) | O(log n) | |
| Trie | O(L) | O(L) | O(L) | L = key length |

### Algorithm patterns

| Pattern | Time | Space | When |
| :--- | :--- | :--- | :--- |
| Two pointers | O(n) | O(1) | Sorted array, opposite ends |
| Sliding window | O(n) | O(1)–O(k) | Contiguous subarray/substring |
| Binary search | O(log n) | O(1) | Sorted or monotonic feasibility |
| Sort + scan | O(n log n) | O(1)–O(n) | Intervals, greedy prep |
| BFS / DFS | O(V+E) | O(V) | Graphs, grids |
| Dijkstra | O((V+E) log V) | O(V) | Non-negative weights |
| Topological sort | O(V+E) | O(V) | DAG dependencies |
| Union-Find | O(α(n)) per op | O(n) | Dynamic connectivity |
| 1D DP | O(n) | O(n) → O(1) | Linear recurrence |
| 2D DP | O(n·m) | O(n·m) → O(m) | Grid, LCS, edit distance |
| Backtracking | O(k^n) worst | O(n) stack | Generate all valid configs |

### Common complexity mistakes

- Nested loop on n=10⁵ → O(n²) TLE
- BFS on weighted graph → wrong; use Dijkstra
- Greedy on coin change (arbitrary denominations) → wrong; use DP
- Forgetting `seen[0]=1` in prefix-sum counting
- Marking graph nodes visited **after** enqueue (BFS duplicates)

## 3. Complexity gotchas
- **Amortized O(1):** Hash map insertions, Python `list.append()`.
- **Space:** Recursion depth uses stack space! DFS on skewed tree is O(N) space.
- **String Concat:** `s += c` in a loop is O(N^2). Use `"".join(list)` for O(N).
- **Master Theorem:** Recognize when halving vs subtracting changes complexity.

## 4. Python whiteboarding essentials
- **Heaps:** `import heapq` (min-heap default). Multiply by -1 for max-heap. `heapify(arr)`, `heappush(arr, x)`, `heappop(arr)`.
- **Queues:** `from collections import deque`. `q.append()`, `q.appendleft()`, `q.popleft()`, `q.pop()`. (Never `list.pop(0)`!)
- **Maps/Sets:** `from collections import defaultdict, Counter`.
- **Sorting:** `arr.sort(key=lambda x: (x[1], x[0]))`.
- **Binary Search:** `import bisect`. `bisect_left(arr, x)`, `bisect_right(arr, x)`.

## See Also

- [How to think](01-how-to-think.md) — constraints as the answer key (§3)
- [Pattern sheet](../05-review/01-pattern-sheet.md) — keyword → pattern lookup
