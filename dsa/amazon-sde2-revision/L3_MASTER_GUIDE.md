# Amazon SDE-2 Master Prep Guide

# Amazon SDE-2 Interview Prep

> **SDE-2 = Mid-level / ~3-5 YOE bar.**
> Loop structure: 2 coding rounds + 1 system design round + 1–2 LP (behavioral) rounds.
>
> The coding bar is: solve a medium problem cleanly in ~35-45 min, handle one
> follow-up (usually space/time optimization or a variation), state complexity
> correctly, test edge cases aloud. Hard problems appear occasionally as a
> differentiator, not as the norm.
>
> This file lists every topic + the exact problems to grind. Mark each ✅ when
> you can solve it cold in ≤ 35 min with no hints.


---

## Section 1 — Arrays & Hashing (Round 1 staple)

> Highest frequency category at L3. Expect at least one problem from here.

### Must-Know Patterns
- Prefix sum (1D): subarray sum queries in O(1) after O(n) build
- Hash map for frequency / complement lookup
- Two-pass hash (e.g., first pass count, second pass answer)
- Sliding window (variable + fixed)

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Two Sum | 1 | Easy | |
| 2 | Contains Duplicate | 217 | Easy | |
| 3 | Product of Array Except Self | 238 | Medium | |
| 4 | Subarray Sum Equals K | 560 | Medium | |
| 5 | Longest Consecutive Sequence | 128 | Medium | |
| 6 | Group Anagrams | 49 | Medium | |
| 7 | Top K Frequent Elements | 347 | Medium | |
| 8 | Minimum Window Substring | 76 | Hard | |
| 9 | Trapping Rain Water | 42 | Hard | |
| 10 | 4Sum | 18 | Medium | |

---

## Section 2 — Two Pointers & Sliding Window

> Appears in almost every loop. Often combined with sorting.

### Must-Know Patterns
- Opposite-end pointers on sorted array (pair sum, pair difference)
- Fast/slow pointers (cycle detection, middle of list)
- Variable window: expand right, shrink left when invalid
- Fixed window: maintain a deque or frequency map

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Valid Palindrome | 125 | Easy | |
| 2 | 3Sum | 15 | Medium | |
| 3 | Container With Most Water | 11 | Medium | |
| 4 | Longest Substring Without Repeating Characters | 3 | Medium | |
| 5 | Longest Repeating Character Replacement | 424 | Medium | |
| 6 | Permutation in String | 567 | Medium | |
| 7 | Fruit Into Baskets | 904 | Medium | |

---

## Section 3 — Binary Search

> Google loves disguised binary search — "search on answer" is the main L3 trap.

### Must-Know Patterns
- Classic: sorted array, rotated array, matrix
- Search on answer: binary search on the result space, not the array
- Template: `lo, hi = ...; while lo < hi: mid = (lo+hi)//2; if feasible(mid): hi=mid else: lo=mid+1`

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Binary Search | 704 | Easy | |
| 2 | Search in Rotated Sorted Array | 33 | Medium | |
| 3 | Find Minimum in Rotated Sorted Array | 153 | Medium | |
| 4 | Search a 2D Matrix | 74 | Medium | |
| 5 | Koko Eating Bananas | 875 | Medium | |
| 6 | Minimum in Rotated Array II (with duplicates) | 154 | Hard | |
| 7 | Capacity to Ship Packages Within D Days | 1011 | Medium | |
| 8 | Find Peak Element | 162 | Medium | |

---

## Section 4 — Linked List

> L3 rounds often open or close with a linked list warm-up.

### Must-Know Patterns
- Dummy node to simplify head-manipulation
- Fast/slow pointer (cycle, middle, kth from end)
- Reverse in-place (iterative, not recursive under pressure)
- Merge two sorted lists

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Reverse Linked List | 206 | Easy | |
| 2 | Merge Two Sorted Lists | 21 | Easy | |
| 3 | Linked List Cycle | 141 | Easy | |
| 4 | Remove Nth Node From End | 19 | Medium | |
| 5 | Reorder List | 143 | Medium | |
| 6 | LRU Cache | 146 | Medium | |
| 7 | Merge K Sorted Lists | 23 | Hard | |
| 8 | Copy List with Random Pointer | 138 | Medium | |

---

## Section 5 — Trees & BST

> Trees are the most common L3 topic. Expect DFS/BFS on trees in every loop.

### Must-Know Patterns
- DFS: pre/in/post-order; return value pattern `(left_result, right_result) → node_result`
- BFS: level-order with a deque, track level by queue size snapshot
- BST: in-order = sorted; validate with min/max bounds
- LCA: bubble up and check

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Invert Binary Tree | 226 | Easy | |
| 2 | Maximum Depth of Binary Tree | 104 | Easy | |
| 3 | Balanced Binary Tree | 110 | Easy | |
| 4 | Diameter of Binary Tree | 543 | Easy | |
| 5 | Same Tree | 100 | Easy | |
| 6 | Binary Tree Level Order Traversal | 102 | Medium | |
| 7 | Binary Tree Right Side View | 199 | Medium | |
| 8 | Count Good Nodes in Binary Tree | 1448 | Medium | |
| 9 | Lowest Common Ancestor of BST | 235 | Medium | |
| 10 | Lowest Common Ancestor of Binary Tree | 236 | Medium | |
| 11 | Binary Tree Maximum Path Sum | 124 | Hard | |
| 12 | Serialize and Deserialize Binary Tree | 297 | Hard | |
| 13 | Validate BST | 98 | Medium | |
| 14 | Kth Smallest Element in BST | 230 | Medium | |

---

## Section 6 — Graphs

> Expect one graph problem in the loop. BFS/DFS matrix problems are most common.
> type
>   directed
>   undirected
>   cyclic graph
>   acyclic graph
>   degree of a graph -- no of edges that are attache to it
> componenet
>   node/vertes
>   edges
> terms in graph
>   cycles in a graph -if we start from a node and reach at that node

### Must-Know Patterns
- BFS for shortest path (unweighted)
- DFS for connected components, cycle detection, flood fill
- Topological sort (Kahn's BFS): course schedule
- Union-Find: dynamic connectivity, redundant edges
- Dijkstra: only if the problem has weighted edges

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Number of Islands | 200 | Medium | |
| 2 | Clone Graph | 133 | Medium | |
| 3 | Max Area of Island | 695 | Medium | |
| 4 | Pacific Atlantic Water Flow | 417 | Medium | |
| 5 | Rotting Oranges | 994 | Medium | |
| 6 | Course Schedule | 207 | Medium | |
| 7 | Course Schedule II | 210 | Medium | |
| 8 | Number of Connected Components in Undirected Graph | 323 | Medium | |
| 9 | Redundant Connection | 684 | Medium | |
| 10 | Word Ladder | 127 | Hard | |
| 11 | Network Delay Time (Dijkstra) | 743 | Medium | |
| 12 | Walls and Gates | 286 | Medium | |

### Google-specific additions (beyond Amazon SDE-2 scope)

> Google loops go deeper on graphs than Amazon. Bellman-Ford, Floyd-Warshall,
> and Prim's are all in `algorithms/15_advanced_graph.py`.

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 13 | Cheapest Flights Within K Stops (Bellman-Ford) | 787 | Medium | |
| 14 | Find the City With the Smallest Number of Neighbors (Floyd-Warshall) | 1334 | Medium | |
| 15 | Min Cost to Connect All Points (Prim's) | 1584 | Medium | |
| 16 | Detect Negative Cycle (Bellman-Ford) | — | — | |

---

## Section 7 — Heap / Priority Queue

> Two-heap pattern and top-K are high-frequency at L3.

### Must-Know Patterns
- Min-heap for kth largest (size-K min-heap)
- Max-heap for kth smallest (negate values)
- Two heaps: median of stream (max-heap lower half, min-heap upper half)
- Merge K sorted: heap of `(value, list_index, element_index)`

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Kth Largest Element in Array | 215 | Medium | |
| 2 | K Closest Points to Origin | 973 | Medium | |
| 3 | Find Median from Data Stream | 295 | Hard | |
| 4 | Task Scheduler | 621 | Medium | |
| 5 | Design Twitter | 355 | Medium | |
| 6 | Merge K Sorted Lists | 23 | Hard | |
| 7 | Reorganize String | 767 | Medium | |

---

## Section 8 — Dynamic Programming

> DP is tested at L3 but usually only 1D/2D patterns. Bitmask/digit DP are rare.

### Must-Know Patterns
- 1D DP: climbing stairs, house robber, coin change
- 2D DP: grid paths, edit distance
- Subsequence DP: LCS, LIS
- Knapsack: subset sum, partition equal subset

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Climbing Stairs | 70 | Easy | |
| 2 | House Robber | 198 | Medium | |
| 3 | House Robber II | 213 | Medium | |
| 4 | Coin Change | 322 | Medium | |
| 5 | Longest Increasing Subsequence | 300 | Medium | |
| 6 | Longest Common Subsequence | 1143 | Medium | |
| 7 | Word Break | 139 | Medium | |
| 8 | Unique Paths | 62 | Medium | |
| 9 | Jump Game | 55 | Medium | |
| 10 | Jump Game II | 45 | Medium | |
| 11 | Partition Equal Subset Sum | 416 | Medium | |
| 12 | Edit Distance | 72 | Hard | |
| 13 | Decode Ways | 91 | Medium | |
| 14 | Palindromic Substrings | 647 | Medium | |

---

## Section 9 — Stack & Monotonic Stack

> Stack problems come up as "warm-ups" that interviewers use to gauge fluency.

### Must-Know Patterns
- Valid parentheses / matching brackets
- Monotonic stack: maintain increasing or decreasing invariant
- "Next greater element" pattern
- Stack for min/max tracking

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Valid Parentheses | 20 | Easy | |
| 2 | Min Stack | 155 | Medium | |
| 3 | Daily Temperatures | 739 | Medium | |
| 4 | Largest Rectangle in Histogram | 84 | Hard | |
| 5 | Car Fleet | 853 | Medium | |
| 6 | Evaluate Reverse Polish Notation | 150 | Medium | |
| 7 | Generate Parentheses | 22 | Medium | |

---

## Section 10 — Backtracking

> Always asked at L3. The template is fixed — practice until you write it without thinking.

### Must-Know Patterns
- Subsets, permutations, combinations — know the exact `start` and skip-duplicate rule for each
- Prune before recursing, not after
- Snapshot: always `result.append(path[:])` not `result.append(path)`

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Subsets | 78 | Medium | |
| 2 | Subsets II (with duplicates) | 90 | Medium | |
| 3 | Permutations | 46 | Medium | |
| 4 | Permutations II (with duplicates) | 47 | Medium | |
| 5 | Combination Sum | 39 | Medium | |
| 6 | Combination Sum II | 40 | Medium | |
| 7 | Word Search | 79 | Medium | |
| 8 | N-Queens | 51 | Hard | |
| 9 | Palindrome Partitioning | 131 | Medium | |

---

## Section 11 — Greedy & Intervals

> Intervals are a favorite Google pattern. Greedy choice must be justified.

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Meeting Rooms | 252 | Easy | |
| 2 | Meeting Rooms II | 253 | Medium | |
| 3 | Merge Intervals | 56 | Medium | |
| 4 | Insert Interval | 57 | Medium | |
| 5 | Non-overlapping Intervals | 435 | Medium | |
| 6 | Jump Game | 55 | Medium | |
| 7 | Gas Station | 134 | Medium | |
| 8 | Hand of Straights | 846 | Medium | |
| 9 | Task Scheduler | 621 | Medium | |

---

## Section 12 — Trie

> Word Search II, prefix-matching, and autocomplete are the recurring patterns.

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Implement Trie (Prefix Tree) | 208 | Medium | |
| 2 | Design Add and Search Words Data Structure | 211 | Medium | |
| 3 | Word Search II | 212 | Hard | |
| 4 | Replace Words | 648 | Medium | |

---

## Section 12b — Segment Tree & Fenwick Tree (Google-specific)

> Not typical at Amazon SDE-2, but Google frequently asks "design a data
> structure supporting range query + update" — a step beyond static
> prefix sums. Implementations in `data_structures/11_segment_tree_fenwick.py`.

### Must-Know Patterns
- Segment tree: O(log n) point update + range query, any associative op (sum/min/max)
- Fenwick tree (BIT): O(log n) prefix sum + point update, simpler/faster, sum/xor only
- Use Fenwick when the op is invertible (sum); use segment tree for min/max/gcd

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Range Sum Query - Mutable | 307 | Medium | |
| 2 | Range Sum Query 2D - Mutable | 308 | Hard | |
| 3 | Count of Smaller Numbers After Self | 315 | Hard | |
| 4 | The Skyline Problem | 218 | Hard | |

---

## Section 13 — Math & Bit Manipulation

> One math/bit problem per loop is common as a quick opener or closer.

### Problems

| # | Problem | LC | Difficulty | ✅ |
|---|---------|-----|-----------|---|
| 1 | Number of 1 Bits | 191 | Easy | |
| 2 | Counting Bits | 338 | Easy | |
| 3 | Reverse Bits | 190 | Easy | |
| 4 | Single Number | 136 | Easy | |
| 5 | Missing Number | 268 | Easy | |
| 6 | Sum of Two Integers (no + operator) | 371 | Medium | |
| 7 | Pow(x, n) | 50 | Medium | |
| 8 | Happy Number | 202 | Easy | |

---

## Amazon Leadership Principles (LP) Round — What to Prepare

Amazon's behavioral rounds use the **STAR format** (Situation, Task, Action, Result).
Prepare 2-3 stories per LP that can flex across multiple questions. At SDE-2, expect
deeper "tell me more" follow-ups — have 2 layers of detail ready per story.

### The 16 Leadership Principles (SDE-2 most-tested)

| LP | Most Common Question Form |
|----|--------------------------|
| **Customer Obsession** | Tell me about a time you went beyond what was asked to improve the customer experience |
| **Ownership** | Tell me about a time you took initiative on something outside your direct responsibilities |
| **Invent and Simplify** | Describe a time you simplified a complex process or built something novel |
| **Are Right, A Lot** | Tell me about a time you had to make a decision with incomplete information |
| **Learn and Be Curious** | Tell me about a time you learned a new skill or domain quickly to solve a problem |
| **Hire and Develop the Best** | Tell me about a time you mentored someone or raised the bar on your team |
| **Insist on the Highest Standards** | Tell me about a time you caught a quality issue others missed |
| **Think Big** | Tell me about a time you proposed or delivered something with outsized impact |
| **Bias for Action** | Tell me about a time you had to move fast with imperfect data |
| **Frugality** | Tell me about a time you accomplished more with fewer resources |
| **Earn Trust** | Tell me about a time you disagreed with a colleague — how did you handle it? |
| **Dive Deep** | Tell me about a time you uncovered a root cause that wasn't obvious |
| **Have Backbone; Disagree and Commit** | Tell me about a time you pushed back on a decision — and what happened |
| **Deliver Results** | Tell me about the most impactful project you've shipped |
| **Strive to be Earth's Best Employer** | Tell me about a time you supported a teammate's growth or wellbeing |
| **Success and Scale Bring Broad Responsibility** | Tell me about a decision you made with long-term or societal considerations |

### Tips
- Lead with **measurable impact** ("reduced P95 latency by 40%", "shipped to 2M users") — Amazon values data
- Each story should be ~2 min; interviewers will probe deeper ("why did you choose that approach?", "what would you do differently?")
- For "why Amazon": tie it to a specific LP or product challenge — *"I want to work at scale on systems where Ownership is non-negotiable"* beats generic answers
- At SDE-2, expect **2+ follow-up questions per story** — prepare depth, not just breadth
- Stories should demonstrate SDE-2 scope: multi-team impact, technical judgment calls, mentorship, or architectural decisions — not just individual contributor execution

### LP Round Strategy
- Map your 5-6 best engineering stories to multiple LPs
- The most versatile stories involve: disagreement + resolution, ambiguous requirements + decision under uncertainty, technical trade-offs with business impact
- Never invent stories; interviewers are trained to probe inconsistencies

---

## Week-Before Checklist

### Coding
- [ ] Can you write DSU from scratch in < 3 min?
- [ ] Can you write BFS/DFS on a grid from scratch in < 2 min?
- [ ] Can you write the backtracking template from scratch in < 2 min?
- [ ] Have you done at least 3 timed mock sessions (45 min, no hints)?
- [ ] Have you practiced thinking aloud while coding (not just silent grinding)?
- [ ] Do you know the complexity of every algorithm in `misllanious.md` cold?
- [ ] Can you implement LRU Cache (doubly-linked list + hash map) from scratch?
- [ ] Can you implement Trie insert/search from scratch?

### System Design
- [ ] Do you have a design template? (Clarify → Capacity → API → Data Model → Core Components → Scale)
- [ ] Can you design: URL Shortener, Twitter Feed, Rate Limiter, Distributed Cache?
- [ ] Do you know the trade-offs: SQL vs NoSQL, sync vs async, CDN vs no CDN?
- [ ] Can you estimate QPS, storage, and bandwidth for a medium-scale system?

### Behavioral (LP)
- [ ] Do you have 5-6 STAR stories mapped to multiple LPs?
- [ ] Can you go 2 levels deep on each story (follow-up probes)?
- [ ] Have you practiced out loud (not just in your head)?
- [ ] Do you have a "why Amazon" answer tied to a specific LP or product?

---

## What Amazon SDE-2 Coding Rounds Do NOT Require

- Bitmask DP, Digit DP, Game Theory DP — out of scope for coding rounds
- Max Flow / Bipartite Matching, Tarjan SCC — not asked at SDE-2
- Segment Tree with lazy propagation, Fenwick Tree — not expected
- KMP, Z-Algorithm, Aho-Corasick — string problems at SDE-2 use sliding window / hashing
- Bellman-Ford (with K-stops is asked occasionally — worth knowing), Floyd-Warshall — rare
- XOR basis, Submask enumeration — out of scope
- These are in your repo as L4 references — ignore them for this interview

## What Amazon SDE-2 DOES Require (vs L3)

These topics appear more frequently or at harder depth at SDE-2 compared to a new-grad bar:

- **Design problems in coding rounds**: LRU Cache (LC 146), LFU Cache (LC 460), Design Twitter (LC 355), Insert Delete GetRandom O(1) (LC 380) — Amazon loves these
- **Harder DP**: Burst Balloons, Word Break II, Minimum Cost to Cut a Stick, Regular Expression Matching
- **Graph variants**: Dijkstra (Network Delay Time, Cheapest Flights Within K Stops), Reconstruct Itinerary, Accounts Merge
- **Heap problems**: Sliding Window Median, Find Median from Data Stream, IPO, Single-Threaded CPU
- **Trie**: Word Search II, Design Search Autocomplete System — know these cold
- **System design round**: ~45 min, medium-scale distributed system (see checklist above)

---

## Complexity Cheat-Sheet (Know These Cold)

| Pattern | Time | Space |
|---------|------|-------|
| Binary search | O(log n) | O(1) |
| BFS / DFS on graph | O(V+E) | O(V) |
| BFS / DFS on grid (n×m) | O(n·m) | O(n·m) |
| Merge sort / any comparison sort | O(n log n) | O(n) |
| Quick select (kth element) | O(n) avg | O(1) |
| Heap push/pop | O(log n) | — |
| Build heap from array | O(n) | — |
| DP 1D | O(n) | O(n) → O(1) rolling |
| DP 2D | O(n·m) | O(n·m) → O(m) rolling |
| Backtracking subsets | O(2ⁿ · n) | O(n) stack |
| Backtracking permutations | O(n! · n) | O(n) stack |
| Union-Find per op | O(α(n)) ≈ O(1) | O(n) |
| Trie insert/search | O(L) | O(N·L·Σ) total |
| Sliding window | O(n) | O(k) window |
| Two pointers | O(n) | O(1) |


---

# Amazon SDE-2 Interview — Algorithmic Patterns Glossary

> This document is the **complete revision glossary** for Amazon SDE-2 prep.
> Each section covers a pattern with:
> - **What it is** and when to recognize it
> - **Key insight / mental model**
> - **Common sub-patterns and variants**
> - **All problems in this repo** that use the pattern
> - **SDE-2 priority** (P0 = must know cold, P1 = know well, P2 = skip until P0/P1 solid)
>
> **SDE-2 scope:** Sections 1–16, 18–21, 24 are in-scope. Sections 13, 17, 22, 23, 25
> are advanced (L4+) — they are kept for reference but **do not study them before
> your Amazon SDE-2 interview**. They are marked **[OUT OF SDE-2 SCOPE]** below.

---

## Table of Contents

1. [Arrays & Prefix Sums](#1-arrays--prefix-sums)
2. [Hashing](#2-hashing)
3. [Two Pointers](#3-two-pointers)
4. [Sliding Window](#4-sliding-window)
5. [Binary Search](#5-binary-search)
6. [Sorting](#6-sorting)
7. [Stack & Monotonic Stack](#7-stack--monotonic-stack)
8. [Linked List](#8-linked-list)
9. [Trees (DFS / BFS)](#9-trees-dfs--bfs)
10. [Heap / Priority Queue](#10-heap--priority-queue)
11. [Trie (Prefix Tree)](#11-trie-prefix-tree)
12. [Graphs (BFS / DFS)](#12-graphs-bfs--dfs)
13. [Advanced Graphs](#13-advanced-graphs) *(L4+ — skip for L3)*
14. [Union-Find (Disjoint Set)](#14-union-find-disjoint-set)
15. [Backtracking](#15-backtracking)
16. [Dynamic Programming (1D / 2D)](#16-dynamic-programming-1d--2d)
17. [Advanced DP (Bitmask, Digit, Interval, Game Theory)](#17-advanced-dp-bitmask-digit-interval-game-theory) *(L4+ — skip for L3)*
18. [Greedy](#18-greedy)
19. [Intervals](#19-intervals)
20. [Bit Manipulation](#20-bit-manipulation)
21. [Math & Number Theory](#21-math--number-theory)
22. [Advanced Strings (KMP, Z, Rabin-Karp, Aho-Corasick)](#22-advanced-strings-kmp-z-rabin-karp-aho-corasick) *(L4+ — skip for L3)*
23. [Advanced Trees (Segment Tree, BIT, Sparse Table, Binary Lifting)](#23-advanced-trees-segment-tree-bit-sparse-table-binary-lifting) *(L4+ — skip for L3)*
24. [Divide & Conquer](#24-divide--conquer)
25. [Monotonic Queue (Deque)](#25-monotonic-queue-deque) *(L4+ — skip for L3)*

---

## 1. Arrays & Prefix Sums

**What it is:** The prefix sum `pre[i] = nums[0] + ... + nums[i-1]` lets you compute any subarray sum in O(1) after O(n) preprocessing. The core identity is `sum(l, r) = pre[r+1] - pre[l]`.

**When to recognize it:** The problem asks for subarray sums, range queries, or "number of subarrays where sum equals / is divisible by K".

**Key insight:** Combine with a **hash map** to turn O(n²) brute-force into O(n) by asking "have I seen `pre[i] - k` before?"

### Sub-patterns
| Sub-pattern | Trigger | Trick |
|---|---|---|
| Range sum query | "Sum of elements between index i and j" | Build pre[] once, answer in O(1) |
| Subarray sum = K | "Count subarrays summing to K" | HashMap of counts: `count[pre[i]-k]` |
| Subarray sum divisible by K | "Divisible by K" | `pre[i] % k` — two equal remainders → valid subarray |
| Contiguous array | Equal 0s and 1s | Map 0→-1, then find subarray sum = 0 |
| 2D prefix sum | Grid range queries | `pre[r][c] = sum of rectangle from (0,0) to (r,c)` |
| Kadane's algorithm | Max subarray sum | Running max of `current + nums[i]` vs `nums[i]` |

### Problems in This Repo
- `array.py` — **Two Sum**, **Maximum Subarray** (Kadane's), **Product of Array Except Self**, **Subarray Sum Equals K**, **Trapping Rain Water**, **Range Sum Query**, **Range Sum Query 2D**, **Maximum Product Subarray**, **Find Minimum in Rotated Sorted Array**, **Jump Game**, **Next Permutation**, **Set Matrix Zeroes**, **Spiral Matrix**
- `hashing.py` — **Subarray Sum Equals K**, **Subarray Sums Divisible by K**, **Continuous Subarray Sum**, **Contiguous Array**, **Make Sum Divisible by P**

---

## 2. Hashing

**What it is:** O(1) average-case lookup/insert using a hash map (dict) or hash set. The single most important data structure for "do I know about X?" style questions.

**When to recognize it:** "Find", "detect duplicate", "group", "count frequency", "O(1) lookup required".

**Key insight:** The hash map often stores **index**, **count**, or **prefix state**, not just the element itself.

### Sub-patterns
| Sub-pattern | Trigger | Example |
|---|---|---|
| Frequency map | Count occurrences | Top K Frequent, Group Anagrams |
| Prefix sum + hash map | Subarray sum queries | Subarray Sum = K |
| State as key | BFS visited states | Word Ladder, Open the Lock |
| Two-sum complement | "Find pair summing to target" | `target - x in seen` |
| LRU / LFU Cache | O(1) get + put + eviction | OrderedDict / doubly-linked list + hash map |

### Problems in This Repo
- `hashing.py` — **Two Sum**, **Group Anagrams**, **Top K Frequent Elements**, **Valid Anagram**, **Longest Consecutive Sequence**, **Subarray Sum Equals K**, **LRU Cache**, **Ransom Note**, **4Sum II**, **Insert Delete GetRandom O(1)**, **Subarrays with K Different Integers**, **Subarray Sums Divisible by K**, **Continuous Subarray Sum**, **Max Number of K-Sum Pairs**, **Contiguous Array**, **Make Sum Divisible by P**
- `linked_list.py` — **LRU Cache**, **LFU Cache**

---

## 3. Two Pointers

**What it is:** Two indices (`l`, `r` or `slow`, `fast`) moving through the array/string/list with a specific invariant. Enables O(n) solutions for problems that would otherwise be O(n²).

**When to recognize it:** Sorted arrays, pairs/triplets summing to target, cycle detection, palindromes, in-place partitioning.

**Key insight:** The sorted order provides a **monotonic property** — moving left increases the sum, moving right decreases it.

### Sub-patterns
| Sub-pattern | Trigger | Technique |
|---|---|---|
| Collision (opposite ends) | Find pair in sorted array | `l=0, r=n-1`; shrink toward center |
| Fast & slow (Floyd's) | Cycle detection, find middle | Slow moves 1, fast moves 2 |
| Dutch National Flag | 3-way partition (0s, 1s, 2s) | `l`, `i`, `r` pointers; single pass |
| Read/Write pointer | Remove duplicates in-place | Write pointer trails behind read |
| K-Sum | Generalized N-Sum | Fix n-2 elements, use 2-ptr for last 2 |

### Problems in This Repo
- `two_pointers.py` — **Two Sum II**, **3Sum**, **Container With Most Water**, **Trapping Rain Water**, **Sort Colors**, **Longest Substring Without Repeating Chars**, **Minimum Window Substring**, **Find All Anagrams in a String**, **Valid Palindrome II**, **Linked List Cycle**, **Subarrays with K Distinct**, **Find the Duplicate Number**, **4Sum**, **Max Consecutive Ones III**, **Minimum Operations to Reduce X to Zero**, **Count Number of Nice Subarrays**, **Frequency of the Most Frequent Element**, **Longest Subarray of 1s After Deleting One Element**
- `array.py` — **3Sum**, **Container With Most Water**, **Trapping Rain Water**
- `linked_list.py` — **Linked List Cycle**, **Linked List Cycle II**, **Palindrome Linked List**, **Remove Nth From End**

---

## 4. Sliding Window

**What it is:** A window `[l, r]` that slides over the array/string. Expand `r` to grow the window; shrink `l` when a constraint is violated. Maintains the window invariant at all times.

**When to recognize it:** "Longest/shortest subarray/substring satisfying condition X", "find all subarrays of size K".

**Key insight:**
- **Fixed-size window:** move `l` and `r` together, `r - l == k - 1` always
- **Variable window:** expand `r` freely, shrink `l` when window becomes invalid
- The key insight for "exactly K" problems: `exactly(K) = atMost(K) - atMost(K-1)`

### Sub-patterns
| Sub-pattern | Key Pattern | Example |
|---|---|---|
| Fixed size | Max sum of k elements | Max Sum Subarray of Size K |
| Shrink on violation | Longest with at most k distinct | Longest Substring Without Repeating |
| Minimum valid window | Smallest satisfying window | Minimum Window Substring |
| Anagram / permutation check | Fixed-size with frequency match | Find All Anagrams, Permutation in String |
| Exactly K distinct | `atMost(k) - atMost(k-1)` | Subarrays with K Distinct |

### Problems in This Repo
- `sliding_window.py` — **Minimum Window Substring**, **Longest Substring Without Repeating Characters**, **Longest Repeating Character Replacement**, **Permutation in String**, **Find All Anagrams in a String**, **Maximum Consecutive Ones III**, **Fruit Into Baskets**, **Subarrays with K Different Integers**, **Sliding Window Median**
- `two_pointers.py` — **Sliding Window Maximum**, **Minimum Window Substring**, **Longest Repeating Character Replacement**, **Subarrays with K Distinct**
- `string.py` — **Minimum Window Substring**, **Find All Anagrams**, **Permutation in String**, **Longest Repeating Character Replacement**

---

## 5. Binary Search

**What it is:** Divide the search space in half each iteration. Applies to sorted arrays AND to any **monotonic answer space** — where "can we do it in X?" has a yes/no threshold.

**When to recognize it:** "Find in sorted", "find minimum X that satisfies condition", "search on value not index".

**Key insight:** Always define the invariant clearly: `lo` is always valid, `hi` is always invalid (or vice versa). The template changes, but the invariant doesn't.

### Sub-patterns
| Sub-pattern | Trigger | Example |
|---|---|---|
| Classic search | Sorted array lookup | Binary Search |
| Rotated array | Array was rotated | Search in Rotated Sorted Array |
| Search on answer space | Min/max feasibility | Koko Eating Bananas, Ship Packages |
| 2D matrix search | Sorted rows/columns | Search a 2D Matrix |
| Find boundary | First/last occurrence | `lo = mid + 1` vs `hi = mid` |
| Peak element | Mountain-like array | Find peak where `arr[i] > arr[i+1]` |

### Problems in This Repo
- `binary_search.py` — **Binary Search**, **Search in Rotated Sorted Array**, **Find Minimum in Rotated Sorted Array**, **Koko Eating Bananas**, **Search a 2D Matrix**, **Capacity to Ship Packages Within D Days**, **Find Minimum in Rotated Sorted Array II**, **Search in Rotated Sorted Array II**, **Time Based Key-Value Store**, **Sqrt**

---

## 6. Sorting

**What it is:** Rearranging elements to unlock O(n log n) or O(n) solutions for problems that would otherwise be quadratic.

**When to recognize it:** "Find pairs/triples", "merge overlapping intervals", "K-th largest/smallest", "reconstruct by ordering".

**Key insight:** Sorting changes the **search strategy** — a sorted array allows two pointers, binary search, and greedy decisions that are impossible on unsorted data.

### Sub-patterns
| Sub-pattern | Algorithm | Example |
|---|---|---|
| Comparison-based | Merge Sort (stable, O(n log n)) | Count of Range Sum, Reverse Pairs |
| In-place partition | Quick Sort / QuickSelect | Kth Largest Element |
| Counting sort | Limited value range | Sort Colors (Dutch Flag) |
| Custom comparator | Non-standard ordering | Largest Number, Queue Reconstruction |
| Bucket sort | Frequency-indexed buckets | Top K Frequent Elements (O(n)) |
| Interval sort | Sort by start/end time | Merge Intervals, Meeting Rooms |

### Problems in This Repo
- `sorting.py` — **Sort Colors**, **Kth Largest Element**, **Largest Number**, **Russian Doll Envelopes**, **Maximum Gap**, **H-Index**, **3Sum Closest**, **Merge Sort**, **Quick Sort**, **Count of Range Sum**, **Reverse Pairs**, **Pancake Sorting**, **Sort Transformed Array**, **Sort Characters By Frequency**, **Queue Reconstruction by Height**
- `hashing.py` — **Top K Frequent Elements** (bucket sort variant)

---

## 7. Stack & Monotonic Stack

**What it is:** A stack that maintains elements in **strictly increasing or decreasing order**. When a new element violates the order, pop until it doesn't — the popped elements have found their "next greater/smaller" element.

**When to recognize it:** "Next greater element", "largest rectangle", "stock span", "remove digits to minimize", "balanced parentheses".

**Key insight:** The monotonic stack does in O(n) what brute-force does in O(n²): for each element, it knows the answer to "what's the nearest element that's larger/smaller than me?"

### Sub-patterns
| Sub-pattern | Stack Type | Example |
|---|---|---|
| Next greater element | Monotone decreasing | Daily Temperatures, Next Greater Element |
| Next smaller element | Monotone increasing | Largest Rectangle in Histogram |
| Running max/min span | Pop & record span | Online Stock Span |
| Parentheses matching | Paired push/pop | Valid Parentheses, Basic Calculator |
| Expression evaluation | Operator stack | Evaluate RPN, Basic Calculator II |
| Decode nested | Push context on open | Decode String |
| Monotone + area | Pop when height drops | Largest Rectangle, Maximal Rectangle |

### Problems in This Repo
- `stack.py` — **Valid Parentheses**, **Trapping Rain Water**, **Daily Temperatures**, **Largest Rectangle in Histogram**, **Min Stack**, **Implement Queue using Stacks**, **Next Greater Element I & II**, **Evaluate RPN**, **Decode String**, **Maximal Rectangle**, **Asteroid Collision**, **Remove K Digits**, **Basic Calculator I & II**, **Online Stock Span**
- `monotonic.py` — **Daily Temperatures**, **Next Greater Element I/II/III**, **Largest Rectangle in Histogram**, **Sum of Subarray Minimums**, **Sum of Subarray Ranges**, **Stock Spanner**, **Maximum Width Ramp**, **Sliding Window Maximum**, **Remove Duplicate Letters**, **Remove K Digits**, **132 Pattern**, **Trapping Rain Water**, **Maximal Rectangle**

---

## 8. Linked List

**What it is:** A chain of nodes where each node holds a value and a pointer to the next node. Problems require careful pointer manipulation without extra space.

**When to recognize it:** "Reverse", "detect cycle", "merge", "find middle", "K-group reversal".

**Key insight:** Use a **dummy/sentinel node** to avoid edge cases with head changes. Use **fast & slow pointers** for cycle detection and middle-finding.

### Sub-patterns
| Sub-pattern | Technique | Example |
|---|---|---|
| Reversal | Iterative 3-pointer (`prev, cur, nxt`) | Reverse Linked List, Reverse K-Group |
| Cycle detection | Floyd's tortoise & hare | Linked List Cycle, Cycle II |
| Find middle | Fast (2x) + Slow (1x) | Sort List, Palindrome Linked List |
| Merge | Two-pointer merge | Merge Two Sorted Lists, Merge K Sorted Lists |
| In-place reorder | Find middle → reverse second half → merge | Reorder List |
| Random pointer copy | Hash map old→new nodes | Copy List with Random Pointer |
| LRU Cache | Doubly-linked list + hash map | LRU Cache, LFU Cache |

### Problems in This Repo
- `linked_list.py` — **Reverse Linked List**, **Linked List Cycle**, **Merge Two Sorted Lists**, **Merge K Sorted Lists**, **Reorder List**, **Remove Nth From End**, **Linked List Cycle II**, **Palindrome Linked List**, **Copy List with Random Pointer**, **Reverse K-Group**, **Sort List**, **Intersection of Two Lists**, **Add Two Numbers**, **Flatten Multilevel Doubly Linked List**, **LRU Cache**, **LFU Cache**, **Delete the Middle Node**, **Swap Nodes in Pairs**

---

## 9. Trees (DFS / BFS)

**What it is:** Trees are hierarchical graphs with no cycles. DFS (recursion / explicit stack) processes depth-first; BFS (queue) processes level-by-level.

**When to recognize it:** Any problem with a tree structure. DFS for path sums, LCA, construction. BFS for level-order, shortest path, right-side view.

**Key insight:** Most tree problems are **post-order DFS** — you need information from both subtrees before you can answer at the current node. The recursive return value carries the answer up the tree.

### Sub-patterns
| Sub-pattern | Traversal | Example |
|---|---|---|
| Level-order | BFS + queue | Binary Tree Level Order Traversal, Right Side View |
| Path sums | DFS, accumulate path | Path Sum III, Binary Tree Max Path Sum |
| LCA | DFS returning found flags | LCA of Binary Tree, LCA of BST |
| Serialize / Deserialize | Pre-order DFS with null markers | Serialize/Deserialize Binary Tree |
| Construct from traversals | Pre+In or Post+In | Build Tree from Pre+Inorder |
| BST operations | Leverage BST property: left < root < right | Validate BST, Kth Smallest, LCA of BST |
| Tree DP | Post-order; each node returns aggregated value | House Robber III, Binary Tree Cameras |
| Morris Traversal | O(1) space inorder without stack | Morris Inorder Traversal |

### Problems in This Repo
- `tree.py` — **Binary Tree Level Order Traversal**, **Validate BST**, **LCA of Binary Tree**, **Binary Tree Max Path Sum**, **Serialize/Deserialize Binary Tree**, **Diameter of Binary Tree**, **Construct Tree from Pre+Inorder**, **Construct Tree from Inorder+Postorder**, **Maximum Depth**, **Invert Binary Tree**, **Symmetric Tree**, **LCA of BST**, **Kth Smallest in BST**, **House Robber III**, **Binary Tree Cameras**, **Recover BST**, **Vertical Order Traversal**, **Flatten Binary Tree to LL**, **Path Sum III**, **Count Good Nodes**, **All Nodes Distance K**, **Populating Next Right Pointers**, **Binary Tree Right Side View**, **LCA of Deepest Leaves**

---

## 10. Heap / Priority Queue

**What it is:** A complete binary tree maintaining the heap property (min-heap: parent ≤ children). Python's `heapq` is a **min-heap**; negate values for max-heap behavior.

**When to recognize it:** "Top K", "K-th largest/smallest", "running median", "merge K sorted", "always process the cheapest/largest item".

**Key insight:** A heap of size K finds the K largest elements in O(n log K) — much better than sorting O(n log n) for large n with small K.

### Sub-patterns
| Sub-pattern | Heap Type | Example |
|---|---|---|
| Top K largest | Min-heap of size K | Kth Largest, K Closest Points |
| Top K frequent | Min-heap keyed by frequency | Top K Frequent Elements |
| K-way merge | Min-heap of (val, list_idx) | Merge K Sorted Lists, Find K Pairs |
| Running median | Max-heap (lower half) + min-heap (upper half) | Find Median from Stream |
| Greedy scheduling | Max-heap for selection | Task Scheduler, IPO, Course Schedule III |
| Monotone greedy swap | Keep best seen via heap | Furthest Building, Minimum Refueling Stops |
| Sliding window median | Two heaps with lazy deletion | Sliding Window Median |

### Problems in This Repo
- `heap.py` — **Kth Largest Element**, **K Closest Points to Origin**, **Top K Frequent Elements**, **Find Median from Stream**, **Task Scheduler**, **Reorganize String**, **Kth Largest in Stream**, **IPO**, **Find K Pairs with Smallest Sums**, **Furthest Building**, **Minimum Refueling Stops**, **Kth Smallest in Sorted Matrix**, **Ugly Number II**, **Meeting Rooms I & II**, **Single-Threaded CPU**, **Last Stone Weight**, **Trapping Rain Water II**, **Minimize Deviation in Array**, **Design Twitter**, **Sliding Window Median**

---

## 11. Trie (Prefix Tree)

**What it is:** A tree where each node represents a character. Paths from root to marked nodes spell out stored words. Enables O(L) lookup/insert for strings of length L, independent of dictionary size.

**When to recognize it:** "Autocomplete", "word search in a grid", "find words with a given prefix", "maximum XOR of two numbers".

**Key insight:** Tries excel when you need to **share prefixes** across many strings. For XOR maximization, treat each bit as a character (binary trie).

### Sub-patterns
| Sub-pattern | Variation | Example |
|---|---|---|
| Standard prefix trie | Insert + search + startsWith | Implement Trie |
| Wildcard search | DFS at '.' nodes | Design Add and Search Words |
| Word search in grid | Trie + DFS pruning | Word Search II, Boggle |
| Binary trie (XOR) | Bits as characters, greedy XOR | Maximum XOR of Two Numbers |
| Map sum | Aggregate values at prefix | Map Sum Pairs |
| Autocomplete | Return all words under a prefix node | Design Search Autocomplete System |
| Aho-Corasick *(L4+)* | Failure links across patterns | Stream of Characters (multi-pattern match) |

### Problems in This Repo
- `trie.py` — **Implement Trie**, **Word Search II**, **Maximum XOR of Two Numbers**, **Replace Words**, **Design Add and Search Words**, **Longest Word in Dictionary**, **Map Sum Pairs**, **Design Search Autocomplete System**, **Stream of Characters**, **Implement Magic Dictionary**, **Boggle Game**, **Concatenated Words**

---

## 12. Graphs (BFS / DFS)

**What it is:** A collection of nodes connected by edges. DFS uses a stack (or recursion); BFS uses a queue and guarantees shortest path in **unweighted** graphs.

**When to recognize it:** "Connected components", "shortest path in unweighted graph", "topological order", "detect cycle", "island problems".

**Key insight:**
- **DFS** → reach, cycle detection, topological sort, connected components
- **BFS** → shortest path (unweighted), level-by-level processing, multi-source propagation

### Sub-patterns
| Sub-pattern | Algorithm | Example |
|---|---|---|
| Island / connected component | DFS/BFS flood fill | Number of Islands, Max Area of Island |
| Multi-source BFS | Start BFS from all sources simultaneously | Rotten Oranges, Walls and Gates, 01 Matrix |
| Topological sort (Kahn's) | In-degree array + queue | Course Schedule, Alien Dictionary |
| Topological sort (DFS) | Post-order DFS | Course Schedule II |
| Cycle detection (directed) | Color: white/gray/black (0/1/2) | Find Eventual Safe States |
| Bipartite check | 2-coloring via BFS/DFS | Is Graph Bipartite |
| BFS with state | Encode extra info in node | Shortest Path with Obstacle Elimination |

### Problems in This Repo
- `graphs.py` — **Number of Islands**, **Max Area of Island**, **Clone Graph**, **Course Schedule**, **Course Schedule II**, **Alien Dictionary**, **Flood Fill**, **Pacific Atlantic Water Flow**, **Surrounded Regions**, **Is Graph Bipartite**, **Find Eventual Safe States**, **Redundant Connection**, **All Paths from Source to Target**, **Minimum Vertices to Reach All Nodes**, **Number of Connected Components**, **Graph Valid Tree**, **Shortest Path with Obstacle Elimination**, **Sequence Reconstruction**, **Regions Cut by Slashes**, **Transitive Closure**
- `queue.py` — **Rotten Oranges**, **01 Matrix**, **Walls and Gates**, **Shortest Path in Binary Matrix**, **Word Ladder**, **Open the Lock**, **As Far from Land as Possible**
- `graph_algorithms.py` — **Word Ladder**, **All Paths from Source to Target**, **Is Graph Bipartite**, **Alien Dictionary**, **Cheapest Flights**, **Reconstruct Itinerary**, **Evaluate Division**, **Network Delay Time**, **Critical Connections**, **Tarjan's SCC**

---

## 13. Advanced Graphs

> **[OUT OF SDE-2 SCOPE]** — Dijkstra IS in-scope (Network Delay Time, Cheapest Flights are asked at SDE-2).
> Skip Bellman-Ford (except K-stops variant — borderline), Floyd-Warshall, Tarjan SCC, Max Flow, and Bidirectional BFS for your Amazon SDE-2 interview.
> Come back to this section after the interview for deeper graph prep.

**What it is:** Weighted graph algorithms for shortest paths, MST, bridges, SCCs, Eulerian paths, and flow. These are the L4/L5 graph topics.

**When to recognize it:** Edge weights, "minimum cost path", "critical connections", "find path visiting all nodes", "maximum flow / bipartite matching".

### Sub-patterns

#### Shortest Path Algorithms
| Algorithm | Use Case | Complexity |
|---|---|---|
| **Dijkstra** | Non-negative edge weights, SSSP | O((V+E) log V) |
| **Bellman-Ford** | Negative weights, K-hop constraint | O(K × E) |
| **Floyd-Warshall** | All-pairs shortest path | O(V³) |

- **Dijkstra:** `advanced_graphs.py` — **Network Delay Time**, **Swim in Rising Water**, **Path With Minimum Effort**, **Minimum Cost to Connect All Points** (Prim's)
- **Bellman-Ford (K-round):** `advanced_graphs.py` — **Cheapest Flights Within K Stops**
- **Floyd-Warshall:** `advanced_graphs.py` — **Find City With Smallest Neighbors at Threshold**

#### MST (Minimum Spanning Tree)
| Algorithm | Strategy |
|---|---|
| **Kruskal's** | Sort edges by weight, union-find to skip cycles |
| **Prim's** | Greedy min-heap expansion from any node |

- `union_find.py` — **Kruskal's MST**
- `advanced_graphs.py` — **Minimum Cost to Connect All Points** (Prim's)
- `graphs.py` — **Minimum Spanning Tree (Kruskal's)**

#### Bridge Finding & SCC
- **Tarjan's Bridges:** `advanced_graphs.py` — **Critical Connections in a Network**
- **Tarjan's SCC:** `advanced_graphs.py` — **Strongly Connected Components**

#### Eulerian Path
- **Hierholzer's Algorithm:** `advanced_graphs.py` — **Reconstruct Itinerary**

#### BFS with Complex State
- `advanced_graphs.py` — **Bidirectional BFS Word Ladder**, **Open the Lock**, **Minimum Genetic Mutation**, **Bus Routes**, **Snakes and Ladders**

#### Weighted BFS / Graph DP
- `advanced_graphs.py` — **Evaluate Division** (weighted BFS), **Number of Ways to Arrive at Destination** (Dijkstra + count), **Course Schedule III** (greedy + max-heap), **DP on DAGs**

#### Max Flow / Bipartite Matching
- `advanced_graphs.py` — **Max Flow / Bipartite Matching** (Ford-Fulkerson / Edmonds-Karp)

---

## 14. Union-Find (Disjoint Set)

**What it is:** A data structure that efficiently answers "are X and Y in the same group?" and merges groups. Uses **path compression** and **union by rank** for near-O(1) operations (inverse Ackermann α(n)).

**When to recognize it:** "Number of connected components", "detect cycle in undirected graph", "merge groups by condition", "MST".

**Key insight:** Path compression makes `find()` flatten the tree to near O(1). Union by rank keeps the tree shallow. Together they give O(α(n)) ≈ O(1) amortized.

### Sub-patterns
| Sub-pattern | Use Case | Example |
|---|---|---|
| Count components | Connected regions | Number of Connected Components |
| Cycle detection | Undirected graph cycles | Redundant Connection, Graph Valid Tree |
| Merge by condition | Merge accounts, pixels | Accounts Merge |
| MST (Kruskal) | Sort edges, union non-same-component | Kruskal's MST |
| Dynamic connectivity | Edges added online | Number of Islands II |
| Rollback / offline | Undo operations | DSU with Rollback (advanced_trees.py) |

### Problems in This Repo
- `union_find.py` — **Number of Connected Components**, **Redundant Connection**, **Graph Valid Tree**, **Accounts Merge**, **Kruskal's MST**, **Number of Provinces**, **Number of Islands II**, **Smallest String with Swaps**, **Satisfiability of Equality Equations**, **Evaluate Division**, **Most Stones Removed**, **Number of Operations to Make Network Connected**, **Swim in Rising Water**, **Remove Max Number of Edges to Keep Graph Fully Traversable**

---

## 15. Backtracking

**What it is:** Systematic enumeration of all possible solutions by building candidates incrementally and **abandoning (pruning)** candidates that cannot lead to a valid solution.

**When to recognize it:** "Generate all", "find all combinations/permutations/subsets", "constraint satisfaction" (Sudoku, N-Queens).

**Key insight:** The backtracking tree has O(k^n) nodes in the worst case. **Pruning** (early termination) is what makes it practical. Always think: "What condition lets me skip this branch entirely?"

### Template
```python
def backtrack(start, current_state):
    if is_complete(current_state):
        result.append(current_state[:])
        return
    for choice in get_choices(start):
        if is_valid(choice):
            make_choice(choice)
            backtrack(next_start, current_state)
            undo_choice(choice)   # restore state
```

### Sub-patterns
| Sub-pattern | Key Constraint | Example |
|---|---|---|
| Subsets | Use index to avoid reuse | Subsets, Subsets II |
| Combinations | Use index, choose k of n | Combinations, Combination Sum |
| Permutations | Use `visited[]` array | Permutations, Permutations II |
| Constraint satisfaction | Check full board validity | N-Queens, Sudoku Solver |
| Partition | Try all split points | Palindrome Partitioning |
| Grid DFS | Mark visited, unmark on return | Word Search, Unique Paths III |

### Problems in This Repo
- `recursion_backtracking.py` — **Word Search**, **Generate Parentheses**, **Subsets**, **Subsets II**, **Permutations**, **Permutations II**, **Combination Sum**, **Combination Sum II**, **N-Queens**, **Palindrome Partitioning**, **Letter Combinations of a Phone Number**, **Combinations**, **Target Sum**, **Word Break II**, **Unique Paths III**, **Combination Sum III**, **Letter Case Permutation**, **Sudoku Solver**, **Beautiful Arrangement**, **Restore IP Addresses**, **Gray Code**, **Matchsticks to Square**, **Remove Invalid Parentheses**

---

## 16. Dynamic Programming (1D / 2D)

**What it is:** Decomposing a problem into overlapping subproblems and storing results to avoid recomputation. Every DP problem has: **state definition**, **recurrence relation**, **base case**, and **evaluation order**.

**When to recognize it:** Optimization (min/max), counting, or feasibility where the answer depends on previously computed answers. Overlapping subproblems + optimal substructure = DP.

**Key insight:** The hardest part of DP is **state definition**. Ask: "What is the minimum information I need to know at position i to compute the answer?"

### Sub-patterns

#### Linear DP (1D)
| Problem Type | State | Recurrence |
|---|---|---|
| Staircase / ways to reach | `dp[i]` = ways to reach i | `dp[i] = dp[i-1] + dp[i-2]` |
| House Robber | `dp[i]` = max without adjacent | `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` |
| Jump game | `dp[i]` = can reach i | `dp[i] = any dp[j] where j+nums[j] >= i` |
| LIS | `dp[i]` = LIS ending at i | `dp[i] = max(dp[j]+1) for j < i where nums[j] < nums[i]` |
| Coin change | `dp[i]` = min coins for amount i | `dp[i] = min(dp[i-coin]+1) for coin in coins` |

#### 2D Grid DP
| Problem Type | State | Example |
|---|---|---|
| Unique paths | `dp[r][c]` = ways to reach (r,c) | Unique Paths, Unique Paths II |
| Min/max path cost | `dp[r][c]` = cost to reach | Minimum Path Sum |
| Word match | `dp[i][j]` = match s[i] with p[j] | Edit Distance, Regular Expression Matching |
| LCS / LPS | `dp[i][j]` = LCS of first i, j chars | Longest Common Subsequence |

#### State Machine DP
- Model each state explicitly: `dp[i][state]` where state encodes discrete conditions
- Transition graph: draw all states and label edges with actions
- Classic family: **Best Time to Buy and Sell Stock** variants
  - State 0: `holding` — max profit while holding a stock
  - State 1: `sold` — max profit day after selling (cooldown if applicable)
  - State 2: `cooldown` — must wait one day (Stock with Cooldown)
- Generalizes to: at most k transactions (Stock III/IV), unlimited, exactly one
- **Problems:** **Best Time to Buy and Sell Stock I/II/III/IV**, **Stock with Cooldown**, **Stock with Transaction Fee**

#### Knapsack Family
| Variant | Constraint | Example |
|---|---|---|
| 0/1 Knapsack | Each item used at most once | Partition Equal Subset Sum, Target Sum |
| Unbounded Knapsack | Items reusable | Coin Change I, Combination Sum IV |
| Bounded | Limited counts | Coin Change II |

### Problems in This Repo
- `dynamic_programming.py` — **Word Break**, **Maximal Square**, **Climbing Stairs**, **House Robber I/II/III**, **Decode Ways**, **Partition Equal Subset Sum**, **Target Sum**, **Coin Change I/II**, **Longest Increasing Subsequence**, **Edit Distance**, **Unique Paths I/II**, **Interleaving String**, **Palindrome Partitioning II**, **Best Time to Buy/Sell Stock (all variants)**, **Min Cost Climbing Stairs**, **Last Stone Weight II**, **Longest Common Subsequence**, **Longest Palindromic Subsequence**, **Burst Balloons**, **Regular Expression Matching**, **Combination Sum IV**, **Distinct Subsequences**, **Jump Game VI**, **Maximum Product Subarray**

---

## 17. Advanced DP (Bitmask, Digit, Interval, Game Theory)

> **[OUT OF SDE-2 SCOPE]** — Bitmask DP, Digit DP, and Game Theory DP are out of scope for Amazon SDE-2.
> Interval DP is a **stretch goal**: Burst Balloons and Palindrome Partitioning II occasionally appear as Hard differentiators.
> Master §16 (1D/2D DP) fully before touching Interval DP. Skip Bitmask/Digit/Game Theory DP entirely.

**What it is:** Extensions of DP using non-standard state representations for harder combinatorial problems.

**When to recognize it:** Small n (≤20) with subset enumeration → Bitmask DP. "Count numbers up to N satisfying X" → Digit DP. "Optimal play between two players" → Game Theory DP. "Merge intervals optimally" → Interval DP.

### Sub-patterns

#### Bitmask DP
- State: `dp[mask]` where bit i is set if element i is included
- Transition: try adding each unset bit
- Complexity: O(2^n × n)
- **Problems:** **Shortest Path Visiting All Nodes** (TSP on graph), **Partition to K Equal Sum Subsets**, **Stickers to Spell Word**, **Shortest Superstring**

#### Digit DP
- State: `dp[pos][tight][...extra]`
- `tight` flag: whether we're still bounded by N's digits
- Used for: "Count integers in [0, N] satisfying property P"
- **Problems:** **Count Digit One**, **Numbers At Most N Given Digit Set**, **Count Numbers with Unique Digits**

#### Interval DP
- State: `dp[l][r]` = optimal cost/value for interval [l, r]
- Transition: try all split points k: `dp[l][r] = opt(dp[l][k] + dp[k+1][r] + cost)`
- Order: increasing length
- **Problems:** **Burst Balloons**, **Palindrome Partitioning II**, **Minimum Cost to Cut a Stick**, **Strange Printer II**

#### Game Theory DP (Minimax)
- State: who's turn, current configuration
- Transition: current player picks optimally (max own score – opponent's optimal)
- **Problems:** **Predict the Winner**, **Stone Game I/II**, **Nim Game**, **Flip Game II**, **Cat and Mouse**

#### Meet in the Middle
- Split input into two halves, enumerate all 2^(n/2) subsets of each half
- Store first-half results in a hash map; query it for each second-half result
- Reduces O(2^n) brute-force to O(2^(n/2)) — critical when n ≈ 40
- **Problems:** **Partition to K Equal Sum Subsets** (extended), **Target Sum** (with large nums)
- **Recognition trigger:** n ≈ 30-40, "find subset satisfying constraint"

### Problems in This Repo
- `dynamic_programming.py` — **Bitmask DP (Shortest Path Visiting All Nodes)**, **Digit DP (Count Digit One)**, **Predict the Winner**, **Stone Game**, **Stone Game II**, **Nim Game**, **Flip Game II**, **Cat and Mouse**, **Shortest Superstring**, **Stickers to Spell Word**, **Numbers At Most N Given Digit Set**, **Count Numbers with Unique Digits**, **Job Scheduling (Convex Hull Trick)**, **Minimum Cost to Cut a Stick**, **Best Time to Buy/Sell Stock III/IV** (State Machine DP)
- `game_theory.py` — Game theory patterns and Sprague-Grundy theorem

---

## 18. Greedy

**What it is:** At each step, make the locally optimal choice, trusting that these local optima compose into a global optimum. Greedy works when the problem has the **greedy choice property** and **optimal substructure**.

**When to recognize it:** Interval scheduling, jump/reach maximization, "always pick the best available resource", activity selection.

**Key insight:** Unlike DP (which explores all choices), greedy commits. Proving greedy correctness usually requires an **exchange argument**: swapping the greedy choice with any other can only make things worse.

### Sub-patterns
| Sub-pattern | Strategy | Example |
|---|---|---|
| Interval scheduling | Sort by end time, greedily select | Non-overlapping Intervals |
| Jump game | Track max reachable index | Jump Game I & II |
| Two-pass greedy | Left-to-right then right-to-left | Candy |
| Greedy + max-heap | Track best discarded option | Furthest Building, Course Schedule III |
| Huffman encoding | Always merge two smallest | Minimum Cost to Connect Sticks |
| Sweep line | Process events in order | The Skyline Problem |

### Problems in This Repo
- `greedy.py` — **Task Scheduler**, **Merge Intervals**, **Jump Game I/II**, **Gas Station**, **Partition Labels**, **3Sum Closest**, **Candy**, **IPO**, **The Skyline Problem**, **Video Stitching**, **Minimum Number of Taps to Water Garden**, **Distant Barcodes**, **Minimum Cost to Connect Sticks**

---

## 19. Intervals

**What it is:** Problems involving ranges `[start, end]`. The key operations are: sort, merge, insert, count overlaps, find gaps.

**When to recognize it:** Meeting rooms, schedule conflicts, range merge/insert, covering problems.

**Key insight:**
- Sort by **start time** for merging
- Sort by **end time** for greedy selection (activity selection)
- **Sweep line**: convert each interval to two events (+1 at start, -1 at end), sort events, scan

### Sub-patterns
| Sub-pattern | Key Step | Example |
|---|---|---|
| Merge intervals | Sort by start; merge if overlap | Merge Intervals |
| Insert interval | Binary search + merge | Insert Interval |
| Min meeting rooms | Sweep line or min-heap of end times | Meeting Rooms II |
| Non-overlapping | Sort by end, greedy skip | Non-overlapping Intervals |
| Minimum arrows | Sort by end, shoot at end | Minimum Arrows to Burst Balloons |
| Interval intersection | Two pointers on sorted lists | Interval List Intersections |
| Segment overlap count | Segment tree or sorted events | My Calendar II/III |

### Problems in This Repo
- `intervals.py` — **Merge Intervals**, **Insert Interval**, **Non-overlapping Intervals**, **Meeting Rooms I/II**, **Minimum Arrows to Burst Balloons**, **Interval List Intersections**, **Employee Free Time**, **My Calendar I/II/III**, **Data Stream as Disjoint Intervals**, **Minimum Interval to Include Each Query**, **Remove Covered Intervals**, **Divide Intervals Into Minimum Number of Groups**

---

## 20. Bit Manipulation

**What it is:** Directly operating on binary representations of integers for O(1) set operations, XOR tricks, and subset enumeration.

**When to recognize it:** "Find the single non-duplicate", "count set bits", "XOR-based uniqueness", "enumerate all subsets", "2^n state space with n ≤ 20".

**Key insight:**
- `x ^ x = 0`, `x ^ 0 = x` → XOR cancels duplicates
- `x & (x-1)` clears the lowest set bit
- `x & (-x)` isolates the lowest set bit
- Negating all elements: `x ^ (1 << 31 - 1)` → bit complement

### Sub-patterns
| Sub-pattern | Bit Trick | Example |
|---|---|---|
| Single non-duplicate | XOR all elements | Single Number I |
| Appear once out of 3 | Bit counting mod 3 | Single Number II |
| Subset enumeration | `for sub = mask; sub > 0; sub = (sub-1) & mask` | Submask Enumeration |
| Power of 2 check | `n & (n-1) == 0` | Power of Two |
| Count set bits | Brian Kernighan's algorithm | Number of 1 Bits, Counting Bits |
| XOR max | Binary trie or linear basis | Maximum XOR of Two Numbers |
| Bitmask DP state | `dp[mask]` for subsets | TSP, Partition to K Equal Subsets |

### Problems in This Repo
- `bit_manipulation.py` — **Single Number I/II/III**, **Number of 1 Bits**, **Counting Bits**, **Reverse Bits**, **Missing Number**, **Sum of Two Integers**, **Maximum XOR of Two Numbers**, **Subsets via Bitmask**, **Reservoir Sampling**, **Random Pick with Weight**, **Maximum XOR With Element From Array**, **Submask Enumeration**, **Count OR Subsets**, **Partition to K Equal Sum Subsets**
- `math_and_bit_manipulation.py` — **Bitwise AND of Numbers Range**, **Power of Two**, and all math problems with bit tricks

---

## 21. Math & Number Theory

**What it is:** Number theory foundations: prime sieve, GCD/LCM, modular arithmetic, digit manipulation, geometric series.

**When to recognize it:** "Count primes", "trailing zeros", "GCD of strings", "palindrome number", "reverse integer".

### Sub-patterns
| Sub-pattern | Algorithm | Example |
|---|---|---|
| Prime sieve | Sieve of Eratosthenes | Count Primes |
| Trailing zeros | Count factors of 5 | Factorial Trailing Zeroes |
| GCD | Euclidean algorithm | Greatest Common Divisor of Strings |
| Fast exponentiation | Binary exponentiation | Pow(x, n), Super Pow |
| Digit extraction | `n % 10` and `n // 10` | Palindrome Number, Reverse Integer |
| Modular arithmetic | `(a * b) % m` | Count of Range Sum |
| Math DP | Digit DP, Pascal's triangle | Count Numbers with Unique Digits |

### Problems in This Repo
- `math_and_bit_manipulation.py` — **Count Primes**, **Factorial Trailing Zeroes**, **Bitwise AND of Numbers Range**, **Excel Sheet Column Number**, **Greatest Common Divisor of Strings**, **Nth Digit**, **Palindrome Number**, **Power of Two**, **Integer to English Words**, **Fraction to Recurring Decimal**, **Perfect Squares**, **Largest Number**, **Ugly Number I/II**, **Josephus Problem**, **Sieve of Eratosthenes**, **Pascal's Triangle I/II**
- `divide_conquer_math.py` — **Maximum Subarray**, **Pow(x, n)**, **Merge K Sorted Lists**, **Happy Number**, **Reverse Integer**, **Majority Element I/II**, **Convert Sorted Array to BST**

---

## 22. Advanced Strings (KMP, Z, Rabin-Karp, Aho-Corasick)

> **[OUT OF SDE-2 SCOPE]** — None of KMP, Z-algorithm, Rabin-Karp, Manacher's, or Aho-Corasick are
> required at Amazon SDE-2. String problems are covered by sliding window and hashing (§2, §4).
> The only exception: if the problem explicitly says "pattern matching" and your interviewer
> expects better than O(n²), mention KMP exists — but you will not be asked to implement it.

**What it is:** Sophisticated string matching algorithms that avoid quadratic backtracking by preprocessing the pattern.

**When to recognize it:** "Find all occurrences of pattern in text", "repeated substring", "longest prefix that is also a suffix", "multi-pattern search in a stream".

### Sub-patterns
| Algorithm | What it computes | Complexity | Example |
|---|---|---|---|
| **KMP** | `lps[]` — longest proper prefix = suffix | O(n + m) | Shortest Palindrome, Repeated Substring Pattern, Longest Happy Prefix |
| **Z-Algorithm** | `z[i]` — length of longest substring starting at i matching prefix | O(n) | Pattern matching |
| **Rabin-Karp** | Rolling hash for substring search | O(n) avg | Longest Duplicate Substring |
| **Manacher's** | Longest palindrome centered at each position | O(n) | Longest Palindromic Substring |
| **Aho-Corasick** | Multi-pattern search with failure links | O(n + total pattern len) | Stream of Characters |

### Problems in This Repo
- `advanced_strings.py` — **Manacher's Algorithm**, **Rabin-Karp Substring Search**, **Longest Duplicate Substring**, **Aho-Corasick Algorithm**, **KMP Pattern Matching**, **Z-Algorithm**, **Palindrome decomposition**, **Anagram detection**
- `string.py` — **Shortest Palindrome**, **Repeated Substring Pattern**, **Distinct Echo Substrings**, **Longest Happy Prefix**, **Longest Palindromic Substring** (Manacher's or expand-around-center)

---

## 23. Advanced Trees (Segment Tree, BIT, Sparse Table, Binary Lifting)

> **[OUT OF SDE-2 SCOPE]** — Segment Tree, BIT/Fenwick Tree, Sparse Table, and Binary Lifting LCA
> are all L4+ topics. At SDE-2, tree problems are covered by §9 (DFS/BFS on trees).
> Count of Smaller Numbers After Self occasionally appears as a Hard problem — use merge sort, no BIT needed.

**What it is:** Specialized tree structures for range queries and updates in O(log n), and preprocessing techniques for O(1) static range queries and LCA.

**When to recognize it:** "Range sum/min/max with updates", "count inversions", "K-th ancestor of a node", "LCA in O(log n)".

### Sub-patterns

#### Segment Tree
- Range query + point/range update in O(log n)
- Lazy propagation for range updates
- **Problems:** Range Sum Query with Update, Count of Smaller Numbers After Self (coordinate compression + BIT)

#### Binary Indexed Tree (Fenwick Tree)
- Prefix sum queries + point updates in O(log n)
- Simpler than segment tree for prefix-type queries
- **Problems:** Count of Smaller Numbers After Self, Count of Range Sum

#### Sparse Table
- Static array: O(n log n) build, O(1) range min/max query (no updates)
- **Problems:** SparseTable (advanced_trees.py), range minimum queries

#### Binary Lifting (Euler tour + LCA)
- Preprocess ancestors at powers of 2: `up[v][k]` = 2^k-th ancestor of v
- LCA in O(log n) after O(n log n) preprocessing
- **Problems:** LCA (Binary Lifting), Kth Ancestor of a Tree Node

#### Monotonic Stack + Trees
- Combine with segment tree for range-based stack problems
- **Problems:** **Sum of Subarray Minimums**, **Maximum Width Ramp**, **Largest Rectangle in Histogram**, **Trapping Rain Water** (in advanced_trees.py)

### Problems in This Repo
- `advanced_trees.py` — **Segment Tree (Range Sum Query with Update)**, **Lazy Segment Tree (Range Update)**, **Binary Indexed Tree**, **Count of Smaller Numbers After Self**, **Sparse Table**, **LCA with Binary Lifting**, **Kth Ancestor of a Tree Node**, **DSU with Rollback**, **Sum of Subarray Minimums**, **Maximum Width Ramp**, **Largest Rectangle in Histogram**, **Trapping Rain Water**

---

## 24. Divide & Conquer

**What it is:** Recursively split the problem into smaller subproblems, solve each independently, and combine results. The paradigm behind Merge Sort, Binary Search, and many counting problems.

**When to recognize it:** "Count inversions", "find median of two sorted arrays", "closest pair of points", "Karatsuba multiplication".

**Key insight:** Divide & Conquer often achieves O(n log n) by doing O(n) work at each of O(log n) levels. The **merge step** is where the real work (and cleverness) lives.

### Sub-patterns
| Sub-pattern | Merge Step | Example |
|---|---|---|
| Merge sort variant | Count while merging | Count Inversions, Reverse Pairs, Count of Range Sum |
| Closest pair | Merge across midpoint | Closest Pair of Points |
| Expression parsing | Recurse on operators | Different Ways to Add Parentheses |
| Fast exponentiation | Halve the exponent | Pow(x, n) |
| Max subarray (D&C) | Cross-midpoint subarray | Maximum Subarray |

### Problems in This Repo
- `divide_conquer_math.py` — **Maximum Subarray** (D&C), **Pow(x, n)** (fast exponentiation), **Merge K Sorted Lists**, **Majority Element** (Boyer-Moore + D&C)
- `sorting.py` — **Merge Sort** (with inversion count), **Count of Range Sum**, **Reverse Pairs**

---

## 25. Monotonic Queue (Deque)

> **[OUT OF SDE-2 SCOPE]** — The monotonic deque (sliding window max/min, constrained DP) is an
> L4 pattern. At SDE-2, Sliding Window Maximum (LC 239) occasionally appears as a Hard problem —
> if it comes up, the O(nk) naive solution is acceptable and the deque solution is a bonus.
> Do not prioritize this over §7 (monotonic stack) which IS required at SDE-2.

**What it is:** A double-ended queue that maintains elements in **monotone order**. Elements are added to the back and removed from the front, but also pruned from the back when the monotone invariant is violated.

**When to recognize it:** "Sliding window maximum/minimum", "constrained subsequence sum", "jump game with bounded look-back".

**Key insight:** The monotonic deque is the O(n) solution to sliding window max/min — the naive approach is O(nk). It gives O(1) amortized access to the window's maximum/minimum by keeping only "useful" elements.

### Sub-patterns
| Sub-pattern | Deque Type | Example |
|---|---|---|
| Sliding window max | Decreasing deque (indices) | Sliding Window Maximum |
| Sliding window min | Increasing deque (indices) | Shortest Subarray with Sum ≥ K |
| Constrained DP | Deque optimizes dp transition | Constrained Subsequence Sum, Jump Game VI |
| Monotone + BFS | Deque as BFS queue | 0-1 BFS (edge weight 0 or 1) |

### Problems in This Repo
- `queue.py` — **Sliding Window Maximum**, **Shortest Subarray with Sum at Least K**, **Constrained Subsequence Sum**, **Jump Game III**
- `monotonic.py` — **Sliding Window Maximum**, **Constrained Subsequence Sum**, **Jump Game VI**, **Shortest Subarray with Sum ≥ K**
- `two_pointers.py` — **Sliding Window Maximum**
- `advanced_trees.py` — **Largest Rectangle in Histogram** (monotonic stack variant)

---

## Amazon SDE-2 Interview Quick Reference

### How to Use Each Solution File
Every topic file is meant to be studied in this order:

1. Read the problem header and classify the pattern before opening the code.
2. Read the method docstring and say the approach out loud in your own words.
3. Trace one example manually and name the loop invariant or recursion state.
4. Re-code the solution without looking, then compare against the checked-in
   implementation.
5. Run that file directly to verify the embedded examples.

### Standard Solution Docstring
Use this shape when adding or revising problems:

```python
"""
Approach: The high-level algorithm in plain English.

Key Insight: The invariant, monotonic property, recurrence, or graph property
that makes the optimized solution possible.

Gotchas:
- Edge cases and off-by-one risks.
- State updates that must happen in a specific order.

Tricks:
- Interview shortcuts, reusable templates, or implementation details worth
  remembering.
"""
```

### Priority Levels for Amazon SDE-2

| Tag | Meaning | How to prepare |
|---|---|---|
| **P0** | Must solve cold in ≤ 20 min — appears in almost every Amazon loop | Code from memory until automatic |
| **P1** | Should solve in ≤ 35 min — high frequency, clear SDE-2 bar | Trace manually, code without hints |
| **P2** | Hard/rare — differentiator; also includes design-in-code problems | Study only after P0/P1 are solid |
| **L4+** | Out of Amazon SDE-2 scope — keep as reference, skip before the interview | Ignore until after the interview |

P0 sections: §1 Arrays, §3 Two Pointers, §4 Sliding Window, §5 Binary Search, §9 Trees, §12 Graphs, §15 Backtracking, §16 DP 1D/2D  
P1 sections: §2 Hashing, §6 Sorting, §7 Stack/Monotonic Stack, §8 Linked List, §10 Heap, §11 Trie, §14 Union-Find, §18 Greedy, §19 Intervals  
P2 sections: §20 Bit Manipulation, §21 Math, §24 Divide & Conquer, design-in-code (LRU/LFU/Twitter)  
L4+ (skip): §13 Advanced Graphs (except Dijkstra), §17 Advanced DP (Bitmask/Digit/Game Theory), §22 Advanced Strings, §23 Advanced Trees, §25 Monotonic Queue

**Amazon-specific note:** Trie is promoted from P2 → P1 vs Google L3. Design-in-code problems (LRU Cache, LFU Cache, Design Twitter) are P2 and appear more at Amazon than at other companies.

### Pattern Recognition Decision Tree (Amazon SDE-2)
```
Is the input sorted (or can you sort it)?
  → Two Pointers / Binary Search / Greedy

Is it a graph / matrix problem?
  → Unweighted + shortest path → BFS
  → Weighted shortest path → Dijkstra  [SDE-2 in-scope; Bellman-Ford K-stops borderline]
  → Connected components / cycles → DFS / Union-Find
  → Ordering dependencies → Topological Sort (Kahn's BFS)

Optimize over a window?
  → Fixed size → Sliding Window (fixed)
  → Variable size → Sliding Window (variable)
  → Monotonic Stack needed → §7 Stack & Monotonic Stack

Need "best first" or "K-th"?
  → Heap / Priority Queue

Need prefix lookups or wildcard matching?
  → Trie

Does "try all possibilities" sound right?
  → Backtracking (with pruning)

Overlapping subproblems + optimal substructure?
  → DP 1D / 2D (§16)  ← this is the SDE-2 DP bar
  → [L4+] n ≤ 20 and subsets → Bitmask DP
  → [L4+] Count integers up to N → Digit DP
  → [L4+] Ranges → Interval DP
  → [L4+] Two players → Game Theory DP

Range queries with updates?
  → [L4+] Segment Tree or BIT (Fenwick Tree)
  → At L3: use merge sort for inversion count

String pattern matching?
  → At L3: sliding window + hash map covers it
  → [L4+] KMP / Z-Algorithm / Rabin-Karp
```

### High-Frequency Amazon SDE-2 Pattern Combos
| Combo | Classic Problem | Amazon Frequency |
|---|---|---|
| Prefix Sum + Hash Map | Subarray Sum = K, Contiguous Array | Very High |
| BFS Level-order | Binary Tree Right Side View, Rotten Oranges | Very High |
| DFS + Post-order Return | Binary Tree Max Path Sum, LCA | Very High |
| Sliding Window | Minimum Window Substring, Longest Repeating Char Replacement | Very High |
| Heap + Greedy | Task Scheduler, K Closest Points, Find Median from Stream | High |
| Two Pointers + Sort | 3Sum, Container With Most Water | High |
| DP + Knapsack | Partition Equal Subset Sum, Coin Change | High |
| Doubly-LL + Hash Map | LRU Cache, LFU Cache | High (Amazon favorite) |
| Union-Find + Sorting | Accounts Merge, Redundant Connection | High |
| Trie + DFS | Word Search II, Design Autocomplete | High |
| BFS + State Encoding | Shortest Path with Obstacle Elimination, Word Ladder | Medium |
| Binary Search + Greedy | Koko Eating Bananas, Capacity to Ship Packages | Medium |
| Monotonic Stack | Largest Rectangle in Histogram, Daily Temperatures | Medium |
| Dijkstra | Network Delay Time, Cheapest Flights Within K Stops | Medium |

---

*Last updated: June 2026 — Calibrated for Amazon SDE-2 prep. Sections 13, 17, 22, 23, 25 are kept for reference but are out of Amazon SDE-2 scope. Focus on Sections 1–16, 18–21, 24 for coding rounds, plus system design and LP prep.*
