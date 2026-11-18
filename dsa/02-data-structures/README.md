# Data Structures — Google L3 Cheat Sheet

## What this covers

> [!abstract] In this file
> **Covers:** Study order for every data-structure file, the DS decision tree, last-minute pattern triggers and the must-solve list.
> **You'll be able to:** Know which file to open for any data-structure topic and which problems to solve first.
> **Prereqs:** None · **Pair with:** [Algorithms index](../03-algorithms/README.md) · [L3 roadmap](../00-start-here/01-roadmap.md) · **Time:** 10 min
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [L3 at a Glance](#l3-at-a-glance) · [Index](#index) · [DS Decision Tree](#ds-decision-tree) · [⚡ Quick Pattern Triggers — Last-Minute Review](#-quick-pattern-triggers--last-minute-review) · [L3 Must-Solve Problems (data structures)](#l3-must-solve-problems-data-structures)

---

## L3 at a Glance

Google L3 (SWE) loops are **4–5 coding rounds**, one problem each, **35–45 minutes**. Expect **medium** problems (occasionally medium-hard). You are graded on clarifying, communicating, choosing the right approach, clean code, dry-run, and stating complexity — not on memorizing obscure tricks.

| What L3 tests | What L3 does **not** test |
| :--- | :--- |
| BFS/DFS, heaps, sliding window, binary search on answer, tries, basic DP | System design, LLD, concurrency, SQL |
| Hash maps, two pointers, trees, union-find, topo sort | Segment trees, bitmask DP, Tarjan SCC |
| Googliness / behavioral (often 1 round) | ML theory (even on AI/ML loops — still DSA) |

**Companion files**

| Purpose | Link |
| :--- | :--- |
| Full L3 roadmap + 4-week schedule | [Roadmap](../00-start-here/01-roadmap.md) |
| 45-min pacing + constraint → Big-O heuristics | [Round cheatsheet](../00-start-here/02-round-cheatsheet.md) · [Complexity budget](../01-foundations/02-complexity-and-python.md) |
| Problem walkthroughs (code + approach) | [`04-practice/data-structures/`](../04-practice/data-structures/) |
| 30-min pattern revision | [Pattern sheet](../05-review/01-pattern-sheet.md) · [Ladders](../05-review/02-ladders.md) |
| Behavioral / Googliness | [Behavioral](../06-behavioral/BEHAVIORAL_GOOGLINESS.md) |

### L3 study order (data structures)

Study **T1 topics first**, in this order. Each block = read the deep-dive file, then solve 2–3 problems cold from the Questions table below.

| Week | Topics | Deep-dive files |
| :--- | :--- | :--- |
| 1 | Array, Hashing, Graphs (BFS/DFS), Matrix | `01-array.md`, `02-hashing.md`, `11-graphs.md`, `04-matrix.md` |
| 2 | Heap, Queue (BFS patterns), Trie | `10-heap.md`, `06-queue.md`, `09-trie.md` |
| 3 | Tree, Stack, Linked List | `08-tree.md`, `05-stack.md`, `07-linked-list.md` |
| 4 | String + integration mocks | `03-string.md` + timed mocks |

> Grid/matrix problems are graph problems — [`04-matrix.md`](04-matrix.md) pairs with week 1's BFS/DFS work.

> **Practice bar:** For each `⚡ T1` topic, you should be able to code the top 3 problems **without notes** in under 25 minutes and explain time/space complexity out loud.

### L3 readiness checklist

Before your onsite, you should be able to say **yes** to all of these:

- [ ] **Array/Hashing:** Two Sum, Subarray Sum Equals K, 3Sum — pattern and complexity without hesitation
- [ ] **Graphs:** Number of Islands, Rotting Oranges, Course Schedule — BFS vs DFS choice in one sentence
- [ ] **Graphs:** Word Ladder, Pacific Atlantic — multi-source BFS / reverse-from-border explained
- [ ] **Heap:** Kth Largest, Merge K Lists, Find Median from Data Stream — min-heap vs two-heap
- [ ] **Trie:** Implement Trie, Word Search II — insert/search and grid DFS + prune
- [ ] **Tree:** LCA, Validate BST, Level Order, Max Path Sum — postorder vs BFS
- [ ] **Linked List:** Reverse, Cycle (Floyd), LRU Cache — three-pointer and DLL+map
- [ ] **Stack/Queue:** Valid Parentheses, Daily Temperatures, Sliding Window Maximum — monotonic stack/deque
- [ ] **Edge cases:** empty input, single element, duplicates, disconnected graph, skewed tree — mention proactively in every round

### Skip for L3

**Segment trees and Fenwick trees (BIT) are not L3 material** — know the one-line idea; do not implement. Use prefix sum, monotonic deque, or heap instead.

→ [What to Skip at L3](../00-start-here/02-round-cheatsheet.md)

Also out of scope: consistent hashing, skip lists, Tarjan SCC, bitmask/digit DP. Ignore if you find old references elsewhere.

---

## Index

Study in this order — each file builds on the previous one.

| # | Topic | File | Tier |
| :-- | :---- | :--- | :--- |
| 1 | Array (prefix sum, Kadane, in-place tricks) | [Array](01-array.md) | `⚡ T1` |
| 2 | Hashing (frequency, complement, grouping) | [Hashing](02-hashing.md) | `⚡ T1` |
| 3 | String | [String](03-string.md) | `🎯 T2` |
| 4 | Matrix / Grid | [Matrix](04-matrix.md) | `⚡ T1` |
| 5 | Stack (monotonic stack) | [Stack](05-stack.md) | `🎯 T2` |
| 6 | Queue / Deque (BFS, monotonic deque) | [Queue](06-queue.md) | `🎯 T2` |
| 7 | Linked List | [Linked List](07-linked-list.md) | `🎯 T2` |
| 8 | Tree / BST | [Tree](08-tree.md) | `⚡ T1` |
| 9 | Trie | [Trie](09-trie.md) | `⚡ T1` |
| 10 | Heap / Priority Queue | [Heap](10-heap.md) | `⚡ T1` |
| 11 | Graphs (BFS/DFS, topo, shortest path, MST) | [Graphs](11-graphs.md) | `⚡ T1` |

Practice problems for each file: [04-practice/data-structures](../04-practice/README.md). Design problems (LRU, LFU, iterators): [12-design](../04-practice/data-structures/12-design.md).

---

## DS Decision Tree

```
Does the problem involve...

Arbitrary key lookup (string/obj keys)?
  → HashMap / HashSet

Prefix-based string queries (autocomplete)?
  → Trie

Hierarchical data or BST operations?
  → Tree (BST / AVL / RB)

Repeatedly extract current min or max?
  → Heap / Priority Queue

Arbitrary relationships / shortest path / cycle detection?
  → Graph (BFS / DFS / Kahn's / Dijkstra)

Sequential data with O(1) random access?
  → Array

Frequent mid-sequence insert/delete at known pointer?
  → Linked List

LIFO order / expression / DFS simulation?
  → Stack

FIFO order / BFS / level-order?
  → Queue
```

---

## ⚡ Quick Pattern Triggers — Last-Minute Review

> Read this the morning of your interview. Each line is one 30-second recognition drill.

| If you see... | Reach for... | Critical edge case |
| :--- | :--- | :--- |
| "Two numbers sum to target" | HashMap complement in one pass | Index 0 sentinel matters for prefix sum variant |
| "Maximum subarray" or "best profit" | Kadane's — reset when negative | Max product: also track `min_prod` for negatives |
| "All words/things starting with prefix" | Trie — O(L) independent of dict size | `is_end ≠ prefix reachable`; prune dead nodes in Word Search II |
| "Shortest path" (unweighted) | BFS — first reach = shortest | Mark visited **before enqueue** not after dequeue |
| "Shortest path" (weighted, no negatives) | Dijkstra + min-heap | Skip stale: `if d > dist[u]: continue` |
| "Dependency ordering" / "detect cycle in directed" | Kahn's Topo Sort | Edge direction: prereq→course; cycle iff `len(order) < n` |
| "All cells spread simultaneously" | Multi-source BFS — seed all at t=0 | Never run BFS per source — O(S×(V+E)) vs O(V+E) |
| "Max/Min in sliding window of size K" | Monotonic Deque — store indices | Store indices not values; pop front when `dq[0] <= i-k` |
| "Always extract current min/max from dynamic set" | Heap (min-heap; negate for max) | `heapq` Python = min-heap only; add `counter` for stability |
| "K-th largest / smallest" | Min-heap size K | QuickSelect is O(N) avg — mention as alternative |
| "Merge K sorted lists/arrays" | K-way merge heap: `(val, idx, elem)` | `idx` breaks ties when elements aren't directly comparable |
| "Find median from stream" | Two heaps: max-heap lower + min-heap upper | Rebalance so `len(lo) - len(hi) <= 1`; median = `lo[0]` or avg |
| "Cycle in linked list" | Floyd's fast/slow | `slow is fast` (identity); Phase 2: reset slow to head |
| "Reverse linked list" | Three-pointer: `prev, curr, nxt` | Save `nxt = curr.next` FIRST or you lose the tail |
| "Max path through a tree" | Tree DP — postorder | Cannot return cross-arm value to parent; use closure for global max |
| "Tree level order / level count" | BFS — snapshot `len(queue)` | Don't use `None` sentinel — use level-size snapshot |
| "Count connected components / flood fill" | DFS/BFS over all unvisited | Disconnected graph: outer loop over all nodes |
| "Sort / order tasks with prerequisites" | Topological sort (Kahn's) | — |
| "0/1 pick items, hit target weight" | 0/1 Knapsack — iterate W **backward** | Forward = unbounded; backward = each item used at most once |
| "Count/enumerate all subsets/permutations" | Backtracking — always `undo` after recurse | Copy path at goal: `results.append(path[:])` not `path` |
| "Minimum cost / steps — monotone feasibility" | Binary search on answer | Write `feasible(mid)` predicate; find min `mid` where feasible |
| "XOR of pairs" | XOR Trie — process MSB→LSB | Bit width: 31 for non-negative; 32 if negatives possible |
| "Exact match lookup, no ordering needed" | HashMap/HashSet O(1) avg | Mutable keys (list/dict) → use tuple; worst case O(N) |

---

## L3 Must-Solve Problems (data structures)

Solve these **cold** before your loop. Full walkthroughs live in [`04-practice/data-structures/`](../04-practice/data-structures/).

| # | Problem | Topic | Pattern |
| :- | :--- | :--- | :--- |
| 1 | Two Sum | Hashing | Complement map |
| 2 | Subarray Sum Equals K | Array / Hashing | Prefix sum + count map |
| 3 | 3Sum | Array | Sort + two pointers |
| 4 | Trapping Rain Water | Array | Two pointers or monotonic stack |
| 5 | Minimum Window Substring | String | Variable sliding window |
| 6 | Number of Islands | Graph | DFS/BFS flood fill |
| 7 | Rotting Oranges | Graph / Queue | Multi-source BFS |
| 8 | Course Schedule | Graph | Kahn's topo sort |
| 9 | Word Ladder | Graph / Queue | BFS on implicit graph |
| 10 | Pacific Atlantic Water Flow | Graph | Reverse BFS from borders |
| 11 | Clone Graph | Graph | DFS + old→clone map |
| 12 | Redundant Connection | Graph | Union-Find |
| 13 | Kth Largest Element | Heap | Min-heap size K |
| 14 | Merge K Sorted Lists | Heap / LL | K-way merge |
| 15 | Find Median from Data Stream | Heap | Two heaps |
| 16 | Implement Trie | Trie | children + is_end |
| 17 | Word Search II | Trie | Trie + grid DFS + prune |
| 18 | Binary Tree Level Order | Tree | BFS level snapshot |
| 19 | LCA of Binary Tree | Tree | Postorder DFS |
| 20 | Validate BST | Tree | DFS with (lo, hi) bounds |
| 21 | Binary Tree Max Path Sum | Tree | Tree DP + global max |
| 22 | Reverse Linked List | Linked List | Three-pointer reversal |
| 23 | Linked List Cycle | Linked List | Floyd fast/slow |
| 24 | LRU Cache | Linked List | DLL + HashMap |
| 25 | Valid Parentheses | Stack | Push opens, match closes |
| 26 | Daily Temperatures | Stack | Monotonic decreasing stack |
| 27 | Sliding Window Maximum | Queue | Monotonic deque |
| 28 | Insert Interval | Array / Intervals | Three-phase scan: copy left non-overlapping, merge overlapping, copy right |

> **Mock cadence:** Weeks 3–4, do **2 timed mocks per week** (35 min, one problem, talk out loud). Log misses in your own tracker; look problems up in [`04-practice/README.md`](../04-practice/README.md).

---

*Generated from source files in this repository. See individual `.md` files for full implementations, click moments, and flashcards.*
