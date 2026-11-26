---
module: 02-algorithms
topic: Range Queries
tags: [algorithms, fenwick, segment-tree, prefix-sum, range-queries]
---
# Range Queries — Prefix Sums, Fenwick, Segment Trees

← [Algorithms index](README.md) · [Patterns master](../05-review/01-pattern-sheet.md)

> 💤 T3 at L3 — promoted to 🎯 T2 for L4/SDE-2+ and hard-round companies. At L3 prefer prefix sums / sorting + binary search / heap.

## What this covers

> [!abstract] In this file
> **Covers:** Choosing a range-query structure; prefix sums (1D/2D); coordinate compression; Fenwick tree (point update, range-update/point-query, k-th); iterative and lazy segment trees; sparse table; merge-sort counting; `SortedList` and its `bisect.insort` fallback.
> **You'll be able to:** Pick the lightest structure that fits the update/query mix, code a Fenwick in 8 lines, and offer a merge-sort or sorted-list alternative when a segment tree is overkill.
> **Prereqs:** Arrays, binary search, heaps, merge sort · **Pair with:** [Range Queries problems](../04-practice/algorithms/15-range-queries.md) · **Time:** 2 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Core Idea](#core-idea) · [Decision Table](#decision-table) · [Theory & Mental Models](#theory--mental-models) · [1. Prefix Sums & Coordinate Compression](#1-prefix-sums--coordinate-compression) · [2. Fenwick Tree (BIT)](#2-fenwick-tree-bit) · [3. Segment Trees](#3-segment-trees) · [4. Sparse Table](#4-sparse-table) · [5. L3-Friendly Alternatives](#5-l3-friendly-alternatives) · [Interview Questions — Logic & Trickiness](#interview-questions--logic--trickiness) · [Quick Revision Triggers](#quick-revision-triggers) · [Flashcards](#flashcards)

---

## Core Idea
- **Root problem**: Answer many "aggregate over `[l, r]`" queries while the array changes. Recomputing is O(n) per query; a static prefix array is O(1) but dies on the first update.
- **Core insight**: Store aggregates over *power-of-two-aligned blocks*. Any range decomposes into O(log n) blocks, and any point belongs to O(log n) blocks, so both query and update touch O(log n) nodes.
- **Invariant**: Every node stores the aggregate of exactly the interval it owns (Fenwick: `(i - lowbit(i), i]`; segment tree: a dyadic interval). Update must refresh all owners of the changed point.
- **Where it breaks**: Fenwick needs an invertible operation (sum, xor) for range queries — min/max need a segment tree. Lazy propagation requires that the update composes (add, assign) and can be applied to a node's aggregate in O(1).

### First-Principles Map

```
[RANGE QUERIES — MINDMAP]
├── WHY IT EXISTS
│   └── Problem class: interleaved updates and range aggregates; n, q up to 1e5 forbids O(n) per op
├── WHAT IT IS
│   ├── Prefix sum: P[i] = a[0]+..+a[i-1]; sum(l..r) = P[r+1] - P[l]
│   ├── Fenwick: tree[i] covers (i - lowbit(i), i]; i += i & -i climbs, i -= i & -i descends
│   └── Segment tree: binary tree, node = merge(left, right); leaves = elements
├── HOW IT WORKS
│   ├── Query: decompose [l, r] into O(log n) canonical blocks and merge them
│   ├── Update: touch every block containing the point (log n)
│   └── Lazy: park a pending range-update tag on a node, push it down only when a query/update must go deeper
├── COMPLEXITY
│   └── Build O(n) · point/range op O(log n) · space n (Fenwick, iterative seg) or 4n (recursive seg)
├── WHEN TO USE
│   ├── "Range sum, point updates" -> Fenwick
│   ├── "Range min/max/gcd, point updates" -> iterative segment tree
│   ├── "Range add + range sum" -> lazy segment tree (or two Fenwicks)
│   └── "Count elements smaller/larger after/before me" -> Fenwick over compressed values, or merge sort
└── COMMON MISTAKES
    ├── Fenwick index 0 -> infinite loop (`0 & -0 == 0`); always 1-index
    ├── Half-open vs inclusive bounds mixed between build and query
    └── Forgetting to compress values/coordinates before indexing a BIT
```

---

## Decision Table

| Situation | Reach for | Cost |
| :--- | :--- | :--- |
| Static array, range sum | Prefix sum (`⚡ T1`) | O(n) build, O(1) query |
| Static array, range min/max/gcd | Sparse table | O(n log n) build, O(1) query |
| Static 2D, rectangle sum | 2D prefix sum (`⚡ T1`) | O(mn) build, O(1) query |
| Point update + range sum | Fenwick | O(log n) each |
| Range add + point query | Fenwick over difference array | O(log n) each |
| Range add + range sum | Lazy segment tree (or two Fenwicks) | O(log n) each |
| Range min/max/custom merge + updates | Segment tree | O(log n) each |
| Count smaller/larger elements (order statistics) | Fenwick over compressed ranks; `SortedList` + `bisect`; merge sort | O(n log n) total |
| Intervals / calendar / skyline | Sorted list + bisect, sweep line + heap; segment tree if heavy | O(n log n) |

Rule of thumb: pick the **leftmost** row that fits. If queries are offline, sorting + Fenwick or merge sort almost always replaces a segment tree.

---

## Theory & Mental Models

**Fenwick = binary-representation ladder.** `i & -i` isolates the lowest set bit. `tree[i]` owns the last `lowbit(i)` elements ending at `i`. A prefix query clears one set bit per step (at most log n); an update adds the lowbit per step, climbing to every owner.

**Segment tree = tournament bracket.** Each internal node is the merge of its children. Iterative layout (size `2n`): leaves at `[n, 2n)`, node `i` has children `2i, 2i+1`, root at 1. Works for any `n` (not only powers of two) and for non-commutative merges if left/right accumulators are kept separate.

**Lazy propagation = deferred paperwork.** A node fully covered by an update records the tag and fixes only its own aggregate (`sum += v * length`). Children are updated only when a later operation must descend through the node (`push`).

**Offline beats online.** If all queries are known upfront, sort/compress and sweep: counting "pairs (i<j) with relation" is merge sort or Fenwick, no tree-of-intervals needed.

| Structure | Build | Update | Query | Space | Supports |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Prefix sum | O(n) | O(n) | O(1) | n | invertible ops, static |
| Sparse table | O(n log n) | rebuild | O(1) | n log n | idempotent ops (min, max, gcd), static |
| Fenwick | O(n) | O(log n) | O(log n) | n | invertible ops (sum, xor) |
| Segment tree | O(n) | O(log n) | O(log n) | 2n / 4n | any associative merge |
| Lazy segment tree | O(n) | O(log n) range | O(log n) | 4n | range updates that compose |

---

## 1. Prefix Sums & Coordinate Compression

```python
def build_prefix(a):
    p = [0] * (len(a) + 1)
    for i, x in enumerate(a):
        p[i + 1] = p[i] + x
    return p

def build_prefix_2d(g):
    m, n = len(g), len(g[0])
    p = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            p[i+1][j+1] = g[i][j] + p[i][j+1] + p[i+1][j] - p[i][j]
    return p

def rect(p, r1, c1, r2, c2):       # inclusive corners
    return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
```

**Coordinate compression**: map values to dense ranks so a BIT of size `#distinct` can index them. Use 1-based ranks.

```python
def compress(vals):
    s = sorted(set(vals))
    return {v: i + 1 for i, v in enumerate(s)}, s
```

#### Common Variants & Twists
- Subarray sum equals k: prefix sums + hash map of seen prefixes (no tree needed).
- Difference array: `diff[l] += v; diff[r+1] -= v`, then prefix-sum once — offline range add in O(n + q).
- XOR prefix works the same (invertible).

---

## 2. Fenwick Tree (BIT)

Point update, prefix/range sum, and `kth` (find the k-th smallest in a multiset of counts) by binary lifting. All indices 1-based.

```python
class BIT:
    def __init__(self, n):
        self.n = n
        self.t = [0] * (n + 1)

    def add(self, i, d):           # 1-indexed point add
        while i <= self.n:
            self.t[i] += d
            i += i & -i

    def prefix(self, i):           # sum of [1..i]
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def range(self, l, r):         # sum of [l..r]
        return self.prefix(r) - self.prefix(l - 1)

    def kth(self, k):              # smallest i with prefix(i) >= k; all values >= 0, 1 <= k <= total
        pos = 0
        pw = 1 << self.n.bit_length()
        while pw:
            nxt = pos + pw
            if nxt <= self.n and self.t[nxt] < k:
                pos = nxt
                k -= self.t[nxt]
            pw >>= 1
        return pos + 1
```

**Range add + point query**: store the difference array in a BIT; point value = prefix sum of the diffs.

```python
class RangeAddPointQuery:          # BIT over the difference array
    def __init__(self, n):
        self.b = BIT(n + 1)
    def add(self, l, r, v):        # add v to [l..r], 1-indexed
        self.b.add(l, v)
        self.b.add(r + 1, -v)
    def get(self, i):
        return self.b.prefix(i)
```

**Range add + range sum** with Fenwick: maintain two BITs `B1, B2` over the difference array; `prefix(i) = B1.prefix(i) * i - B2.prefix(i)` where each range add `v` on `[l, r]` does `B1.add(l, v); B1.add(r+1, -v); B2.add(l, v*(l-1)); B2.add(r+1, -v*r)`. Say it, don't code it, unless asked; use a lazy segment tree otherwise.

**Order statistics**: counts in a BIT over compressed values; `kth(k)` returns the compressed rank of the k-th smallest; map back through the sorted list.

#### Common Variants & Twists
- Inversion count / count smaller after self: iterate, `prefix(rank-1)` then `add(rank, 1)`.
- Fenwick of max (prefix max, values only increase) works; arbitrary updates and arbitrary ranges do not.
- 2D Fenwick: nested loops over both indices; O(log m log n) per op.

---

## 3. Segment Trees

### Iterative (bottom-up), size 2n

Generic over `(op, identity)`. Query is **half-open** `[l, r)`; update is a point assignment.

```python
class SegTree:
    def __init__(self, data, op, e):
        self.n, self.op, self.e = len(data), op, e
        self.t = [e] * self.n + list(data)
        for i in range(self.n - 1, 0, -1):
            self.t[i] = op(self.t[2*i], self.t[2*i+1])

    def update(self, i, v):        # 0-indexed point assign
        i += self.n
        self.t[i] = v
        while i > 1:
            i >>= 1
            self.t[i] = self.op(self.t[2*i], self.t[2*i+1])

    def query(self, l, r):         # half-open [l, r)
        resl = resr = self.e
        l += self.n; r += self.n
        while l < r:
            if l & 1:
                resl = self.op(resl, self.t[l]); l += 1
            if r & 1:
                r -= 1; resr = self.op(self.t[r], resr)
            l >>= 1; r >>= 1
        return self.op(resl, resr)
```

```python
st = SegTree(nums, lambda a, b: a + b, 0)        # range sum
mn = SegTree(nums, min, float("inf"))            # range min
```

### Recursive with lazy propagation (range add, range sum)

Inclusive bounds `[l, r]`; arrays sized `4n`.

```python
class LazySeg:
    def __init__(self, a):
        self.n = len(a)
        self.s = [0] * (4 * self.n)
        self.z = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, a)

    def _build(self, o, lo, hi, a):
        if lo == hi:
            self.s[o] = a[lo]; return
        mid = (lo + hi) // 2
        self._build(2*o, lo, mid, a); self._build(2*o+1, mid+1, hi, a)
        self.s[o] = self.s[2*o] + self.s[2*o+1]

    def _apply(self, o, lo, hi, v):
        self.s[o] += v * (hi - lo + 1)
        self.z[o] += v

    def _push(self, o, lo, hi):
        if self.z[o]:
            mid = (lo + hi) // 2
            self._apply(2*o, lo, mid, self.z[o])
            self._apply(2*o+1, mid+1, hi, self.z[o])
            self.z[o] = 0

    def add(self, l, r, v, o=1, lo=0, hi=None):    # inclusive [l, r]
        if hi is None: hi = self.n - 1
        if r < lo or hi < l: return
        if l <= lo and hi <= r:
            self._apply(o, lo, hi, v); return
        self._push(o, lo, hi)
        mid = (lo + hi) // 2
        self.add(l, r, v, 2*o, lo, mid); self.add(l, r, v, 2*o+1, mid+1, hi)
        self.s[o] = self.s[2*o] + self.s[2*o+1]

    def sum(self, l, r, o=1, lo=0, hi=None):
        if hi is None: hi = self.n - 1
        if r < lo or hi < l: return 0
        if l <= lo and hi <= r: return self.s[o]
        self._push(o, lo, hi)
        mid = (lo + hi) // 2
        return self.sum(l, r, 2*o, lo, mid) + self.sum(l, r, 2*o+1, mid+1, hi)
```

For range **assign** the tag needs a sentinel (`None`) because "assign 0" differs from "no tag"; for range add + range max, `apply` does `mx += v` (no length factor).

#### Common Variants & Twists
- Dynamic (sparse) segment tree: create children on demand over a huge coordinate range (My Calendar III, Falling Squares).
- Segment tree storing `(sum, prefix_max, ...)` tuples for custom merges (max subarray sum in a range).
- Merge-sort tree / persistent tree: name them, don't code them.

---

## 4. Sparse Table

Static range minimum in O(1) by overlapping two power-of-two blocks. Only valid for idempotent operations (min, max, gcd); not sum.

```python
class SparseMin:
    def __init__(self, a):
        self.st = [list(a)]
        j = 1
        while (1 << j) <= len(a):
            prev, h = self.st[-1], 1 << (j - 1)
            self.st.append([min(prev[i], prev[i + h]) for i in range(len(a) - (1 << j) + 1)])
            j += 1

    def query(self, l, r):         # inclusive
        j = (r - l + 1).bit_length() - 1
        return min(self.st[j][l], self.st[j][r - (1 << j) + 1])
```

---

## 5. L3-Friendly Alternatives

### Merge sort counting

Count, for each element, how many elements to its right are smaller — the same split-and-count idea solves inversions, Reverse Pairs and Count of Range Sum in O(n log n) with no tree.

```python
def count_smaller(nums):
    n = len(nums)
    res = [0] * n
    idx = list(range(n))
    def sort(lo, hi):              # sorts idx[lo:hi] by nums value
        if hi - lo <= 1: return
        mid = (lo + hi) // 2
        sort(lo, mid); sort(mid, hi)
        merged, j = [], mid
        for i in range(lo, mid):
            while j < hi and nums[idx[j]] < nums[idx[i]]:
                merged.append(idx[j]); j += 1
            res[idx[i]] += j - mid
            merged.append(idx[i])
        merged.extend(idx[j:hi])
        idx[lo:hi] = merged
    sort(0, n)
    return res
```

### SortedList and the `bisect.insort` fallback

`sortedcontainers.SortedList` gives O(log n)-ish `add`, `remove`, `bisect_left`, indexing. It is on LeetCode but **not guaranteed in an interview**; ask, otherwise use the fallback below. Its `insert`/`del` are O(n) element shifts (a fast `memmove`), fine to roughly 1e5 elements, but state the O(n) worst case aloud and offer Fenwick-over-compressed-values if n is larger.

```python
try:
    from sortedcontainers import SortedList
except ImportError:
    class SortedList:
        def __init__(self, it=()): self.a = sorted(it)
        def add(self, x): insort(self.a, x)                     # O(n) shift, tiny constant
        def remove(self, x):
            i = bisect_left(self.a, x)
            if i == len(self.a) or self.a[i] != x: raise ValueError(x)
            del self.a[i]
        def bisect_left(self, x): return bisect_left(self.a, x)
        def bisect_right(self, x): return bisect_right(self.a, x)
        def __getitem__(self, i): return self.a[i]
        def __len__(self): return len(self.a)
```

---

## Interview Questions — Logic & Trickiness

| Question | Pattern | Click Moment | Core Logic | Trickiness / Gotchas |
| :--- | :--- | :--- | :--- | :--- |
| **Range Sum Query - Immutable `⚡ T1`** | Prefix sum | "No updates" | `P[r+1] - P[l]` | Off-by-one: prefix length is `n+1`. |
| **Range Sum Query - Mutable `🎯 T2`** | Fenwick / seg tree | "Point update + range sum" | BIT delta update, `prefix(r) - prefix(l-1)` | Update by **delta**, not by value; keep a copy of `nums`. |
| **Count of Smaller Numbers After Self `🎯 T2`** | Fenwick + compression / merge sort | "Count of smaller to my right" | Scan right-to-left; query `rank-1`; add `rank` | Strictly smaller means query `rank-1`, not `rank`. Duplicates share a rank. |
| **Reverse Pairs `🎯 T2`** | Merge sort | "i<j and a[i] > 2·a[j]" | Count across halves *before* merging | Use `x > 2*y` in ints; do not count during the merge itself. |
| **Count of Range Sum `💤 T3`** | Prefix sums + Fenwick / merge sort | "Subarray sum in [lo, hi]" | For each prefix `s`, count earlier prefixes in `[s-hi, s-lo]` | Include the empty prefix `0`; compress prefix sums, not nums. |
| **The Skyline Problem `🎯 T2`** | Sweep + max-heap | "Max height changes at x" | Heap `(-h, end)`; lazy pop expired | Emit only when height changes; ties at same x handled by processing all events at x before reading the max. |
| **My Calendar I `⚡ T1` / II / III** | Sorted list / sweep | "Overlap counting" | Neighbour check with bisect; boundary deltas | Intervals are half-open `[s, e)`; touching is not overlapping. |
| **Sliding Window Median `🎯 T2`** | Two heaps (lazy) / SortedList | "Median of moving window" | Rebalance after each slide | Duplicate values: lazy-delete by value, track live sizes. Even `k` returns float. |

---

## Quick Revision Triggers

- "Static array, many range-sum queries" → prefix sum; `P[r+1] - P[l]`.
- "Point update + range sum" → Fenwick, update by delta.
- "Range min/max with updates" → iterative segment tree with `(op, identity)`.
- "Range add + range sum" → lazy segment tree; tag stores pending add.
- "Count smaller/larger elements before/after" → Fenwick over compressed ranks, or merge sort.
- "Pairs (i<j) with a relation on values" → merge sort counting across halves.
- "Intervals overlap/booking" → sorted list + `bisect`; sweep line with deltas.
- "Library not guaranteed" → `bisect.insort` fallback; mention O(n) insert.
- "Fenwick loops forever" → you used index 0.

---

## See also

- [Union-Find](10-union-find.md) — the other "log-ish" structure on this tier
- [Sorting](01-sorting.md) — merge sort as the counting engine
- [Binary Search](04-binary-search.md) — `bisect` semantics
- [Heaps](../02-data-structures/10-heap.md) — skyline and sliding-window median
- [Patterns Master](../05-review/01-pattern-sheet.md)

## Flashcards

**Static array, many range-sum queries — what technique?** #flashcard
Prefix sum: build `P` of length n+1; answer `P[r+1] - P[l]` in O(1).

**Point update + range sum — what technique, and what does an update pass in?** #flashcard
Fenwick tree; pass the **delta** (`new - old`), not the new value.

**What does `i & -i` return and why does Fenwick use it?** #flashcard
The lowest set bit of `i`; `tree[i]` owns that many elements ending at `i`, and adding/subtracting it climbs/descends the ladder in O(log n).

**Why must Fenwick be 1-indexed?** #flashcard
`0 & -0 == 0`, so index 0 never advances and loops forever.

**Fenwick vs segment tree — when is Fenwick not enough?** #flashcard
Fenwick needs an invertible op (sum, xor). Min/max, gcd, custom merges and most lazy range updates need a segment tree.

**Range add + point query — how with Fenwick?** #flashcard
BIT over the difference array: `add(l, v); add(r+1, -v)`; point value = `prefix(i)`.

**How does `kth` on a Fenwick work?** #flashcard
Binary lifting from the highest power of two: step to `pos + pw` while `tree[pos+pw] < k`, subtracting; answer is `pos + 1`. Requires non-negative counts.

**Why is lazy propagation needed, and when is the tag pushed?** #flashcard
Range updates would touch O(n) leaves; store a tag on fully covered nodes and push it to children only when an operation must descend.

**Sparse table: which operations and what query cost?** #flashcard
Idempotent ops only (min, max, gcd), O(1) query via two overlapping power-of-two blocks, O(n log n) build, static array.

**Count of Smaller Numbers After Self — two O(n log n) approaches?** #flashcard
Fenwick over compressed ranks (scan right-to-left, query `rank-1`, add `rank`), or merge sort tracking original indices.

**`SortedList` unavailable — fallback and its caveat?** #flashcard
`bisect.insort` on a list; O(n) shift per insert/delete (fast memmove, fine to ~1e5), so state the worst case.

**Why prefer merge sort over a segment tree for "count pairs i<j with relation"?** #flashcard
Offline split-and-count is O(n log n), no coordinate compression or tree code, and generalises to Reverse Pairs and Count of Range Sum.
