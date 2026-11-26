# Special Algorithms — Amazon SDE-2 Reference

> Reference for the non-trivial algorithms tested at Amazon SDE-2.
> **SDE-2 bar:** BFS/DFS, Dijkstra, Topo Sort, 0-1 Knapsack, LIS, Edit Distance, Sliding Window, Two Pointers, Backtracking, Prefix Sum, Trie.
>
> Format per algorithm: **what it solves → when to use → key insight → gotchas → complexity**.

---

## What's Here

**SDE-2 core:** BFS, Dijkstra, Topo Sort, Merge Sort counting, Quick Select, 0-1 Knapsack, LIS, Edit Distance, Sliding Window, Two Pointers, Backtracking, Prefix Sum, Trie, Greedy Intervals, Sweep Line, Sieve.

---

## Table of Contents

- [Special Algorithms — Google Interview Reference (L3)](#special-algorithms--google-interview-reference-l3)
  - [What's Here](#whats-here)
  - [Table of Contents](#table-of-contents)
  - [Graph — Shortest Paths](#graph--shortest-paths)
    - [1. BFS (SSSP for unweighted graphs)](#1-bfs-sssp-for-unweighted-graphs)
    - [2. Dijkstra](#2-dijkstra)
  - [Graph — Spanning Trees \& Connectivity](#graph--spanning-trees--connectivity)
    - [3. DFS-based Connectivity \& Cycle Detection](#3-dfs-based-connectivity--cycle-detection)
    - [4. Prim's MST](#4-prims-mst)
    - [5. Topological Sort](#5-topological-sort)
  - [Sorting \& Selection](#sorting--selection)
    - [7. Merge Sort + Counting-in-Merge](#7-merge-sort--counting-in-merge)
    - [8. Quick Sort \& Quick Select](#8-quick-sort--quick-select)
    - [9. Top K Elements (Heap)](#9-top-k-elements-heap)
  - [Dynamic Programming Patterns](#dynamic-programming-patterns)
    - [10. 0/1 Knapsack](#10-01-knapsack)
    - [11. Longest Increasing Subsequence — O(n log n)](#11-longest-increasing-subsequence--on-log-n)
    - [12. Edit Distance (Levenshtein)](#12-edit-distance-levenshtein)
  - [Backtracking \& Recursion](#backtracking--recursion)
    - [17. Backtracking Template](#17-backtracking-template)
  - [Interval Techniques](#interval-techniques)
    - [20. Greedy Merge Intervals](#20-greedy-merge-intervals)
  - [Math](#math)
    - [22. Sieve of Eratosthenes](#22-sieve-of-eratosthenes)
  - [Complexity Quick-Reference](#complexity-quick-reference)
  - [Algorithm Selection Guide](#algorithm-selection-guide)
  - [Cross-references](#cross-references)

---

## Graph — Shortest Paths

> | Algorithm | Negative edges? | Time | Use when |
> |-----------|----------------|------|----------|
> | **BFS** | N/A (unweighted) | O(V+E) | Unweighted graph |
> | **Dijkstra** | ❌ | O((V+E) log V) | Non-negative weights, single source |

**Interview rule:** Default Dijkstra for weighted. BFS for unweighted.

---

### 1. BFS (SSSP for unweighted graphs)

**Why it matters:** Default for shortest path on unweighted graphs and the foundation for many problems (rotting oranges, word ladder, level-order).

**Template:**
```python
from collections import deque
q = deque([start])
dist = {start: 0}
while q:
    u = q.popleft()
    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
```

---

### 2. Dijkstra

**Files:** `algorithms/06_graph_algorithms.py` → `findCheapestPrice` (Bellman-Ford variant), `countPaths` (Dijkstra + count). LC 743 Network Delay Time and LC 778 Swim in Rising Water are in scope — add to `06_graph_algorithms.py` if not present.

**Key insight:** Min-heap of `(dist, node)`. Always pop the smallest. **Lazy deletion**: when you pop a `(d, u)` with `d > dist[u]`, skip — that's a stale entry from a previous relaxation.

**Skeleton:**
```python
import heapq

def dijkstra(n, adj, src):      # adj[u] = [(v, w), ...]
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]             # (dist, node)
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:         # stale entry
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

**Bottleneck variants** (common trap):
- `swimInWater`: cost to enter a cell is `max(current_cost, grid[r][c])`, NOT sum.
- `minimumEffortPath`: cost to traverse an edge is `max(current_cost, |height_diff|)`.

**Gotchas:**
- **Never use with negative edges.**
- Always skip stale heap entries: `if d > dist[u]: continue`.

**Complexity:** O((V+E) log V) time, O(V+E) space.

---

## Graph — Spanning Trees & Connectivity

---

### 3. DFS-based Connectivity & Cycle Detection

**Why not DSU?** DSU requires implementing a class with path compression and union-by-rank — that's 15+ lines of bookkeeping under interview pressure. DFS does the same job with code you already know.

**Connected components (LC 323):**
```python
from collections import defaultdict

def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v); graph[v].append(u)
    visited = set()

    def dfs(node):
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                dfs(nei)

    count = 0
    for i in range(n):
        if i not in visited:
            visited.add(i)
            dfs(i)
            count += 1
    return count
```

**Cycle detection in undirected graph — track parent (LC 684 Redundant Connection):**

Key insight: process edges one by one. The first edge where both endpoints are already reachable from each other creates the cycle.

```python
def findRedundantConnection(edges):
    graph = defaultdict(set)

    def connected(u, v):
        visited = set()
        stack = [u]
        while stack:
            node = stack.pop()
            if node == v: return True
            if node in visited: continue
            visited.add(node)
            stack.extend(graph[node])
        return False

    for u, v in edges:
        if connected(u, v):        # path already exists → this edge is redundant
            return [u, v]
        graph[u].add(v)
        graph[v].add(u)
    return []
```

**Complexity:** O(E · V) — DFS per edge. Slightly worse than DSU's O(E · α(V)) in theory, but for interview input sizes it's identical in practice and far simpler to write.

**When DSU is still worth it:** only if the problem involves millions of union/find operations or you need to process queries online. That's not L3.

---

### 4. Prim's MST

**File:** `algorithms/06_graph_algorithms.py` → LC 1584 Min Cost to Connect All Points

**Key insight:** Grow the tree from a seed node. Min-heap of `(weight, neighbor)`. Like Dijkstra but with the priority being edge weight, not path length.

**Skeleton:**
```python
def prim(n, adj):               # adj[u] = [(w, v), ...]
    visited = set()
    pq = [(0, 0)]               # (weight, node) — start at node 0
    mst_cost = 0
    while pq and len(visited) < n:
        w, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        mst_cost += w
        for edge_w, v in adj[u]:
            if v not in visited:
                heapq.heappush(pq, (edge_w, v))
    return mst_cost
```

**When to use:** **Dense/complete graphs** (E ≈ V²). Avoids materializing all O(V²) edges.

**Complexity:** O(E log V) time.

---

### 5. Topological Sort

**Files:** `algorithms/graph_algorithms.py` → `findOrder`, `minimumSemesters`

**Two methods:**

**Kahn's BFS (iterative, preferred):**
```python
from collections import deque

def topo_sort(n, edges):        # edges = [(u, v), ...]
    adj = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        indegree[v] += 1
    q = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                q.append(v)
    return order if len(order) == n else []  # empty = cycle
```

**DFS post-order:** Recurse, then append. Reverse at the end.

**Cycle detection:** `len(result) < n` in Kahn's; `WHITE → GRAY → BLACK` with back-edge detection in DFS.

**DP on DAG** (LC 2050 — parallel courses): after topo sort, `dp[v] = max(dp[u] + time[v])` for each predecessor `u` — gives the **critical path**.

**Complexity:** O(V+E) time, O(V+E) space.

---

## Sorting & Selection

> | Algorithm | Time | Space | Stable? | In-place? | Notes |
> |-----------|------|-------|---------|-----------|-------|
> | **Merge Sort** | O(n log n) | O(n) | ✅ | ❌ | Use for counting-in-merge (inversions) |
> | **Quick Sort** | O(n log n) avg | O(log n) | ❌ | ✅ | Fastest in practice; Quick Select for kth |
> | **Heap Sort** | O(n log n) | O(1) | ❌ | ✅ | Rarely coded, but heapify is essential |

**L3 rule:** You will not be asked to implement a sort. You WILL be asked to count inversions (merge sort pattern) or find kth-largest (quick select or heap).

---

### 7. Merge Sort + Counting-in-Merge

**Files:** `data_structures/array.py` → `mergeSort`, `countRangeSum`, `reversePairs`

**Skeleton:**
```python
def merge_sort_count(nums):
    count = 0
    def merge_sort(arr):
        nonlocal count
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort(arr[:mid])
        right = merge_sort(arr[mid:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                count += len(left) - i   # all remaining left form inversions with right[j]
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    merge_sort(nums)
    return count
```

**The trick — "counting during merge":** when you take an element from the **right** half during merge, **all remaining elements in the left half form a valid pair with it**. Increment the count then.

- **Inversions** (LC 493 reverse pairs): count pairs where `arr[i] > 2*arr[j]`.

**Complexity:** O(n log n) time, O(n) space.

---

### 8. Quick Sort & Quick Select

**File:** `data_structures/array.py` → `quickSort`, `findKthLargest`

**Quick Select — for "kth element":**
```python
def quickselect(nums, k):                # kth LARGEST
    def helper(l, r):
        pivot = nums[r]
        p = l
        for i in range(l, r):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        nums[p], nums[r] = nums[r], nums[p]
        # p is now pivot's final position; if p is (n-k), pivot IS the kth largest
        if p == len(nums) - k:  return nums[p]
        if p > len(nums) - k:   return helper(l, p-1)
        else:                   return helper(p+1, r)
    return helper(0, len(nums)-1)
```

**Random pivot** prevents worst case on sorted input. Average O(n), worst O(n²).

---

### 9. Top K Elements (Heap)

**File:** `data_structures/hashing.py` → `topKFrequent`

```python
def topKFrequent(nums: List[int], k: int) -> List[int]:
    count = Counter(nums)
    # O(N log K) using heap
    return heapq.nlargest(k, count.keys(), key=count.get)
```

**Key insight:** By passing `count.keys()` as the iterable and `count.get` as the key function, `heapq.nlargest` directly selects the unique numbers based on their frequency counts. Under the hood, it maintains a min-heap of size `k`, yielding O(n log k) time complexity.

---

## Dynamic Programming Patterns

> | Pattern | Trigger signal | Complexity |
> |---------|---------------|-----------|
> | **0/1 Knapsack** | "Capacity / budget / partition into equal subsets" | O(n·W) |
> | **LIS** | "Longest strictly increasing" | O(n log n) |
> | **Edit Distance** | "Min ops to convert / spell check" | O(n·m) |

---

### 10. 0/1 Knapsack

**File:** `algorithms/dynamic_programming.py` → `canPartition`, `lastStoneWeightII`

**Key insight:** 1D DP `dp[w]` = best value achievable with capacity `w`. Iterate `w` **backwards** so each item is used at most once.

```python
for item in items:
    for w in range(W, item.weight - 1, -1):     # backwards!
        dp[w] = max(dp[w], dp[w - item.weight] + item.value)
```

**"subset sum / partition" variant:** `dp[target]` is Boolean. `canPartition` = can you split the array into two equal-sum subsets? = `dp[total//2]`.

**Gotcha:** Forward iteration = **unbounded** knapsack (item reuse). Always backwards for 0/1.

---

### 11. Longest Increasing Subsequence — O(n log n)

**File:** `algorithms/dynamic_programming.py` → `lengthOfLIS`

**Skeleton:**
```python
from bisect import bisect_left

def lis_length(nums):
    tails = []
    for n in nums:
        pos = bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)
        else:
            tails[pos] = n
    return len(tails)
```

**Key insight:** Maintain `tails` where `tails[i]` = smallest possible tail element of any increasing subsequence of length `i+1`. For each new element, **binary search** for its position in `tails` (`bisect_left`):
- If it extends (position == len(tails)): append.
- Otherwise: replace at that position (smaller tail is always better).

**The length of `tails` is the LIS length.** `tails` is NOT the LIS itself — just a bookkeeping array.

**Gotcha:** "Strictly increasing" → use `bisect_left` (replace equal values). "Non-decreasing" → use `bisect_right`.

---

### 12. Edit Distance (Levenshtein)

**File:** `algorithms/dynamic_programming.py` → `minDistance`

**Skeleton:**
```python
def edit_distance(w1, w2):
    n, m = len(w1), len(w2)
    dp = list(range(m + 1))          # dp[j] = cost to reach w2[:j] from empty
    for i in range(1, n + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, m + 1):
            temp = dp[j]
            if w1[i-1] == w2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])  # replace, delete, insert
            prev = temp
    return dp[m]
```

**Key insight:** `dp[i][j]` = min cost to convert `word1[:i]` to `word2[:j]`. Three transitions from `dp[i-1][j-1]`, `dp[i-1][j]`, `dp[i][j-1]` (replace, delete, insert).

---

## Backtracking & Recursion

---

### 17. Backtracking Template

**File:** `algorithms/recursion_backtracking.py`

**The universal skeleton (memorize):**
```python
def backtrack(state, start, choices):
    if is_complete(state):
        result.append(state[:])     # ← snapshot, never append(state)!
        return
    for i in range(start, len(choices)):
        if not is_valid(choices[i], state, i): continue
        state.append(choices[i])    # choose
        backtrack(state, i + (1 if no_reuse else 0), choices)  # explore
        state.pop()                 # unchoose
```

**Variant cheat sheet:**
| Problem | Record when? | `start` after choosing | Skip duplicates |
|---------|-------------|------------------------|-----------------|
| Subsets | At every node | `i+1` | sort + `if i > start and nums[i]==nums[i-1]` |
| Permutations | At leaves | `0` (use `used[]` instead) | sort + same skip |
| Combination Sum (reuse) | At leaves | `i` (not `i+1`!) | sort + skip |
| N-Queens | At leaves | `0` | validity check before recurse |
| Word Search (2D) | At leaves | `0` | mark visited in-place, unmark after |

**Gotcha:** Forgetting `state[:]` (snapshot) — without it you collect references that all point to the same final list. **Most common backtracking bug.**

---

**2D — inclusion-exclusion:**
```python
P[r+1][c+1] = matrix[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]
rect_sum(r1,c1, r2,c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
```

**L3 rule:** Prefix sum = static arrays. Any updates? Use a sorted structure instead.

---


## Interval Techniques

---

### 20. Greedy Merge Intervals

**File:** `algorithms/greedy.py`

**Key insight:** Sort by **start**, then sweep: keep a running `end`; if next start ≤ current end, extend; else, save and start new.

```python
intervals.sort()                            # sort by start
merged = []
for s, e in intervals:
    if merged and s <= merged[-1][1]:
        merged[-1][1] = max(merged[-1][1], e)     # extend
    else:
        merged.append([s, e])                      # start new
```

**Extensions:**
- **Insert interval** — find first overlapping, merge in.
- **Non-overlapping intervals** (LC 435) — greedy by **end time** (NOT start), count removals.


## Math

---

### 22. Sieve of Eratosthenes

**File:** `algorithms/math_and_bit_manipulation.py`

**Key insight:** Start marking composites from `p²`, not `2p` — smaller multiples were already marked by smaller primes.

```python
def sieve(n):
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for m in range(p * p, n + 1, p):
                is_prime[m] = False
        p += 1
    return [i for i, v in enumerate(is_prime) if v]
```

**SPF variant:** also track smallest prime factor → factorise any number in O(log n).

**Complexity:** O(N log log N) time, O(N) space.

---

## Complexity Quick-Reference

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| BFS | O(V+E) | O(V) | Unweighted |
| Dijkstra | O((V+E) log V) | O(V+E) | Non-negative only |
| Prim | O(E log V) | O(V) | Use this for MST at L3 |
| DFS connectivity | O(V+E) | O(V) | Replaces DSU for L3 |
| Topological Sort | O(V+E) | O(V+E) | Cycle if `len < n` |
| Merge Sort | O(n log n) | O(n) | Stable |
| Quick Sort | O(n log n) avg | O(log n) | |
| Quick Select | O(n) avg | O(log n) | |
| 0/1 Knapsack | O(n·W) | O(W) | Backwards |
| LIS (binary search) | O(n log n) | O(n) | `bisect_left` |
| Edit Distance | O(n·m) | O(n·m) → O(m) | |
| Boyer-Moore | O(n) | O(1) | |
| Sliding Window | O(n) | O(k) | |
| Two Pointers | O(n) | O(1) | Sorted |
| Backtracking (subsets) | O(2ⁿ·n) | O(n) | |
| Backtracking (perms) | O(n!·n) | O(n) | |
| Prefix Sum 1D | O(n) build, O(1) query | O(n) | Static |
| Prefix Sum 2D | O(nm) build, O(1) query | O(nm) | |
| Trie | O(L) per op | O(N·L·Σ) | |
| Sweep Line | O(n log n) | O(n) | |
| Sieve | O(N log log N) | O(N) | |

---

## Algorithm Selection Guide

```
Shortest path?
├── Unweighted                    → BFS                    O(V+E)
└── Non-negative, single source   → DIJKSTRA               O((V+E) log V)

Connectivity / components?
├── Dynamic merges, cycle detect  → UNION-FIND             O(α(n))
├── Order in DAG                  → TOPO SORT (Kahn)       O(V+E)
└── 2-colorable?                  → BIPARTITE CHECK        O(V+E)

MST?
├── Sparse                        → KRUSKAL                O(E log E)
└── Dense / complete              → PRIM                   O(E log V)

DP?
├── Capacity / partition          → 0/1 KNAPSACK           O(n·W)
├── Longest increasing seq        → LIS                    O(n log n)
└── Transform one string to another→ EDIT DISTANCE          O(n·m)

Array / string tricks?
├── Majority / n/k                → BOYER-MOORE            O(n), O(1) space
├── Longest/shortest subarray     → SLIDING WINDOW         O(n)
├── Pair sum (sorted)             → TWO POINTERS           O(n)
└── 3-way partition               → DUTCH NATIONAL FLAG    O(n), O(1) space

Range queries on static array?
└── Prefix sum                    → PREFIX SUM             O(1) query
```

---

## Cross-references

- **`graph.md`**, **`tree.md`**, **`dp.md`** — deeper reference for those specific topics.
- **`/algorithms/` and `/data_structures/`** — code for every algorithm in this doc.
