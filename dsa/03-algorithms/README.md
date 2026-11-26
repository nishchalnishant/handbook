# Algorithms — Google L3 Cheat Sheet

## What this covers

> [!abstract] In this file
> **Covers:** Study order for every algorithm file, quick pattern triggers, and the must-solve list.
> **You'll be able to:** Know which file to open for any algorithm topic and which problems to solve first.
> **Prereqs:** None · **Pair with:** [DS index](../02-data-structures/README.md) · [L3 roadmap](../00-start-here/01-roadmap.md) · **Time:** 10 min
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Index](#index) · [⚡ Quick Pattern Triggers — Algorithms](#-quick-pattern-triggers--algorithms) · [L3 Must-Solve Problems (algorithms)](#l3-must-solve-problems-algorithms)

---

## Index

Study in this order — each file builds on the previous one.

| # | Topic | File | Tier |
| :-- | :---- | :--- | :--- |
| 1 | Sorting, QuickSelect | [Sorting](01-sorting.md) | `🎯 T2` |
| 2 | Two Pointers | [Two Pointers](02-two-pointers.md) | `⚡ T1` |
| 3 | Sliding Window | [Sliding Window](03-sliding-window.md) | `⚡ T1` |
| 4 | Binary Search (incl. on answer) | [Binary Search](04-binary-search.md) | `⚡ T1` |
| 5 | Recursion | [Recursion](05-recursion.md) | `⚡ T1` |
| 6 | Backtracking | [Backtracking](06-backtracking.md) | `⚡ T1` |
| 7 | Recursion → Memo → Tabulation | [Recursion to DP](07-recursion-to-dp.md) | `⚡ T1` |
| 8 | Dynamic Programming | [DP](08-dynamic-programming.md) | `⚡ T1` |
| 9 | Greedy, Intervals, Sweep Line | [Greedy](09-greedy.md) | `🎯 T2` |
| 10 | Union-Find (DSU) | [Union-Find](10-union-find.md) | `🎯 T2` |
| 11 | Graph algorithms (Dijkstra, Bellman-Ford, MST, Eulerian) | [Graphs §3](../02-data-structures/11-graphs.md#3-weighted--advanced-algorithms) | `⚡ T1` / `🎯 T2` |
| 12 | String algorithms (KMP, Z, rolling hash) | [String Algorithms](12-string-algorithms.md) | `🎯 T2` |
| 13 | Bit manipulation | [Bits](13-bit-manipulation.md) | `🎯 T2` |
| 14 | Math & number theory | [Math](14-math-and-number-theory.md) | `🎯 T2` |
| 15 | Range queries (Fenwick / segment tree) | [Range Queries](15-range-queries.md) | `💤 T3` (prefix sums `⚡ T1`) |

Practice problems for each file: [04-practice/algorithms](../04-practice/README.md).

---

## ⚡ Quick Pattern Triggers — Algorithms

> Read this the morning of your interview. One-line recognition drills.

| If you see... | Algorithm | Critical detail |
| :--- | :--- | :--- |
| "Shortest path" in unweighted graph | BFS | Mark visited before enqueue |
| "Shortest path" weighted, no negatives | Dijkstra | Skip stale: `if d > dist[u]: continue` |
| "Negative edge weights" | Bellman-Ford K+1 rounds | Use copy of dist array each round |
| "Order tasks / prerequisites" | Kahn's Topo Sort | Cycle ⇔ `len(order) < n` |
| "Maximize/minimize with feasibility" | Binary search on answer | Write `feasible(mid)`; min: `hi=mid` on feasible |
| "Partition + pick items once" | 0/1 Knapsack | Inner loop W **backward** |
| "Partition + reuse items" | Unbounded Knapsack | Inner loop W **forward** |
| "Two sequences — align & match" | LCS DP | `dp[i][j] = dp[i-1][j-1] + 1` on match |
| "All valid configurations / subsets" | Backtracking | `undo` after recurse; copy path at goal |
| "Locally optimal = globally optimal" | Greedy | Prove with exchange argument |
| "Sorted array, find target" | Binary Search `lo <= hi` | `mid = lo + (hi-lo)//2` prevents overflow |
| "Connected components / cycle in undirected" | Union-Find | `union()` returns False on first cycle |
| "XOR pair / single number" | XOR + bit trick | `a^a=0`; `a^0=a`; XOR all → singles survive |
| "Touching interval boundary" | Greedy — sort by end | `>` vs `>=` — verify with one example |
| "Count inversions / merge" | Merge Sort D&C | Count during merge step, not split |
| "All paths" in a DAG | DFS backtrack, no visited set | DAG → no cycles → no infinite loops |
| "State machine (hold / sell / cooldown)" | DP with states | Track all states at each step simultaneously |

---

## L3 Must-Solve Problems (algorithms)

Solve these **cold** before your loop.

| # | Problem | Topic | Pattern |
| :- | :--- | :--- | :--- |
| 1 | Two Sum II (Sorted) | Two Pointers | Converging |
| 2 | 3Sum | Two Pointers | Sort + converging + dedup |
| 3 | Container With Most Water | Two Pointers | Move shorter side |
| 4 | Trapping Rain Water | Two Pointers / Stack | Two-pointer or monotonic stack |
| 5 | Minimum Window Substring | Sliding Window | Variable window + freq map |
| 6 | Sliding Window Maximum | Sliding Window | Monotonic deque |
| 7 | Binary Search (exact) | Binary Search | `lo <= hi` template |
| 8 | Search in Rotated Array | Binary Search | Determine sorted half first |
| 9 | Koko Eating Bananas | Binary Search | BS on answer + `feasible()` |
| 10 | Climbing Stairs | DP | Linear / Fibonacci |
| 11 | Coin Change I | DP | Unbounded Knapsack — minimize |
| 12 | Word Break | DP | Linear DP + HashSet |
| 13 | Longest Common Subsequence | DP | LCS 2D table |
| 14 | Maximal Square | DP | Grid DP — `min(up, left, diag) + 1` |
| 15 | Subsets | Backtracking | Include/exclude + `start` index |
| 16 | Combination Sum | Backtracking | Reuse allowed — pass `i` |
| 17 | Word Search | Backtracking | Grid DFS + in-place mark |
| 18 | Generate Parentheses | Backtracking | Count `open`/`close`; prune |
| 19 | N-Queens | Backtracking | Constraint sets `cols, diag1, diag2` |
| 20 | Course Schedule | Graph | Kahn's topo sort |
| 21 | Word Ladder | Graph | BFS on implicit graph |
| 22 | Pacific Atlantic Water Flow | Graph | Reverse BFS from borders |
| 23 | Redundant Connection | Union-Find | First cycle-creating edge |
| 24 | Cheapest Flights K Stops | Advanced Graph | Bellman-Ford K+1 rounds |
| 25 | Merge Intervals | Greedy | Sort + sweep |
| 26 | Insert Interval | Greedy | Three-phase scan |
| 27 | Task Scheduler | Greedy | Freq formula |
| 28 | Maximum Subarray | D&C / Kadane | Reset on negative |

> **Mock cadence:** Weeks 3-4, do **2 timed mocks per week** (35 min, one problem, talk out loud).

---

*See individual topic sections above for full patterns, gotchas, and complexity analysis.*
