---
tags: [coding, algorithms, range-queries, fenwick, segment-tree]
topic: Range Queries
difficulty: mixed
---
# Range Queries — Problem Deep Dives

> 💤 T3 at L3 — promoted to 🎯 T2 for L4/SDE-2+ and hard-round companies. At L3 prefer prefix sums / sorting + binary search / heap.

## What this covers

> [!abstract] In this file
> **Covers:** Prefix sums, Fenwick tree, segment tree, merge-sort counting, sorted-list interval problems, heap sweeps.
> **You'll be able to:** Pick the lightest structure for the update/query mix and write a Fenwick or iterative segment tree from memory.
> **Prereqs:** Range Queries lecture · **Pair with:** [Range Queries lecture](../../02-algorithms/19-range-queries.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Prefix Sums](#prefix-sums) · [Fenwick Tree & Segment Tree](#fenwick-tree--segment-tree) · [Counting Pairs: Compression & Merge Sort](#counting-pairs-compression--merge-sort) · [Sweep Line & Intervals](#sweep-line--intervals) · [Heaps & Windows](#heaps--windows) · [Order Statistics with Fenwick](#order-statistics-with-fenwick)

> [!tip] If you only have 20 minutes
> **Do these first:** [Range Sum Query - Immutable](#range-sum-query---immutable--t1) · [Range Sum Query 2D - Immutable](#range-sum-query-2d---immutable--t1) · [Range Sum Query - Mutable](#range-sum-query---mutable--t2) · [Count of Smaller Numbers After Self](#count-of-smaller-numbers-after-self--t2) · [The Skyline Problem](#the-skyline-problem--t2) · [My Calendar I](#my-calendar-i--t1)
> **Template:** Fenwick: `while i <= n: t[i] += d; i += i & -i` · prefix: `while i: s += t[i]; i -= i & -i` (1-indexed).
> **Imports assumed in every snippet:** `from bisect import bisect_left, bisect_right, insort` · `import heapq` · `from collections import defaultdict`.
> **Gotchas:** Update by delta · strictly smaller = query `rank-1` · half-open calendar intervals · compress before indexing a BIT.

---

## Prefix Sums

---

### Range Sum Query - Immutable `⚡ T1`

> [!example] Problem
> **[E]** Design `NumArray(nums)` with `sumRange(left, right)` returning the inclusive sum, called many times. Example: `nums=[-2,0,3,-5,2,-1]`, `sumRange(0,2)=1`, `sumRange(2,5)=-1`.

> [!info] Approach
> No updates, so precompute `p[i+1] = p[i] + nums[i]`. Answer is `p[right+1] - p[left]`. The leading 0 removes the `left == 0` special case.

> [!note]- Python Solution
> ```python
> class NumArray:                       # LC 303
>     def __init__(self, nums):
>         self.p = [0]
>         for x in nums:
>             self.p.append(self.p[-1] + x)
>     def sumRange(self, left, right):
>         return self.p[right + 1] - self.p[left]
> ```

> [!success] Complexity
> Build O(n), query O(1), space O(n).

> [!tip] Alternatives
> Baseline for the whole file: if the problem has no updates, stop here.

---

### Range Sum Query 2D - Immutable `⚡ T1`

> [!example] Problem
> **[M]** Design `NumMatrix(matrix)` with `sumRegion(r1, c1, r2, c2)` returning the sum of the inclusive rectangle, called many times.

> [!info] Approach
> 2D prefix `p[i+1][j+1] = a[i][j] + p[i][j+1] + p[i+1][j] - p[i][j]` (inclusion-exclusion). Region sum = `p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]`.

> [!note]- Python Solution
> ```python
> class NumMatrix:                      # LC 304
>     def __init__(self, matrix):
>         m, n = len(matrix), len(matrix[0])
>         self.p = [[0] * (n + 1) for _ in range(m + 1)]
>         for i in range(m):
>             for j in range(n):
>                 self.p[i+1][j+1] = matrix[i][j] + self.p[i][j+1] + self.p[i+1][j] - self.p[i][j]
>     def sumRegion(self, r1, c1, r2, c2):
>         p = self.p
>         return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
> ```

> [!success] Complexity
> Build O(mn), query O(1), space O(mn).

---

## Fenwick Tree & Segment Tree

---

### Range Sum Query - Mutable `🎯 T2`

> [!example] Problem
> **[M]** Design `NumArray(nums)` supporting `update(index, val)` (assign) and `sumRange(left, right)` (inclusive sum).

> [!info] Approach
> Point update + range sum is the textbook Fenwick case: store the **delta** `val - old`, climb with `i += i & -i`; prefix query descends with `i -= i & -i`. Build in O(n) by pushing each node into its parent. The iterative segment tree (leaves at `[n, 2n)`) is the generalisation if the interview changes sum to min/max.

> [!note]- Fenwick Solution
> ```python
> class NumArrayBIT:                    # LC 307 Fenwick
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.nums = nums[:]
>         self.t = [0] * (self.n + 1)
>         for i, x in enumerate(nums, 1):          # O(n) build
>             self.t[i] += x
>             j = i + (i & -i)
>             if j <= self.n:
>                 self.t[j] += self.t[i]
>     def update(self, index, val):
>         d, self.nums[index] = val - self.nums[index], val
>         i = index + 1
>         while i <= self.n:
>             self.t[i] += d
>             i += i & -i
>     def _pre(self, i):
>         s = 0
>         while i:
>             s += self.t[i]
>             i -= i & -i
>         return s
>     def sumRange(self, left, right):
>         return self._pre(right + 1) - self._pre(left)
> ```

> [!note]- Segment Tree Solution
> ```python
> class NumArraySeg:                    # LC 307 iterative segment tree
>     def __init__(self, nums):
>         self.n = len(nums)
>         self.t = [0] * self.n + nums
>         for i in range(self.n - 1, 0, -1):
>             self.t[i] = self.t[2*i] + self.t[2*i+1]
>     def update(self, index, val):
>         i = index + self.n
>         self.t[i] = val
>         while i > 1:
>             i >>= 1
>             self.t[i] = self.t[2*i] + self.t[2*i+1]
>     def sumRange(self, left, right):
>         l, r, s = left + self.n, right + self.n + 1, 0
>         while l < r:
>             if l & 1: s += self.t[l]; l += 1
>             if r & 1: r -= 1; s += self.t[r]
>             l >>= 1; r >>= 1
>         return s
> ```

> [!success] Complexity
> Build O(n), update O(log n), query O(log n), space O(n).

> [!tip] Alternatives
> Sqrt decomposition is O(sqrt n) per op with less code; mention it, don't code it.

---

## Counting Pairs: Compression & Merge Sort

---

### Count of Smaller Numbers After Self `🎯 T2`

> [!example] Problem
> **[H]** Given `nums`, return `counts` where `counts[i]` is the number of `j > i` with `nums[j] < nums[i]`. Example: `[5,2,6,1]` -> `[2,1,1,0]`.

> [!info] Approach
> **Fenwick + compression**: map values to dense ranks, scan right-to-left; `prefix(rank-1)` is the count of strictly smaller elements already seen, then add `rank`. **Merge sort**: sort indices by value; while merging, for each left element count right elements strictly smaller already emitted (pointer `j - mid`). State both; the merge-sort one needs no compression.

> [!note]- Fenwick + Compression
> ```python
> def countSmallerBIT(nums):            # LC 315
>     rank = {v: i for i, v in enumerate(sorted(set(nums)), 1)}
>     t = [0] * (len(rank) + 1)
>     res = []
>     for x in reversed(nums):
>         i = rank[x] - 1                      # strictly smaller ranks
>         c = 0
>         while i:
>             c += t[i]; i -= i & -i
>         res.append(c)
>         i = rank[x]
>         while i <= len(rank):
>             t[i] += 1; i += i & -i
>     return res[::-1]
> ```

> [!note]- Merge Sort (indices)
> ```python
> def count_smaller(nums):
>     n = len(nums)
>     res = [0] * n
>     idx = list(range(n))
>     def sort(lo, hi):              # sorts idx[lo:hi] by nums value
>         if hi - lo <= 1: return
>         mid = (lo + hi) // 2
>         sort(lo, mid); sort(mid, hi)
>         merged, j = [], mid
>         for i in range(lo, mid):
>             while j < hi and nums[idx[j]] < nums[idx[i]]:
>                 merged.append(idx[j]); j += 1
>             res[idx[i]] += j - mid
>             merged.append(idx[i])
>         merged.extend(idx[j:hi])
>         idx[lo:hi] = merged
>     sort(0, n)
>     return res
> ```

> [!success] Complexity
> Both O(n log n) time, O(n) space.

> [!tip] Alternatives
> `SortedList`: scan right-to-left, `res = sl.bisect_left(x)`, `sl.add(x)`. With the `insort` fallback inserts are O(n) worst case.

---

### Reverse Pairs `🎯 T2`

> [!example] Problem
> **[H]** Count pairs `(i, j)` with `i < j` and `nums[i] > 2 * nums[j]`. Example: `[1,3,2,3,1]` -> `2`.

> [!info] Approach
> Merge sort: after sorting both halves, count cross pairs with a monotone pointer `j` (valid because both halves are sorted: as `x` grows `j` only advances), **then** merge. Counting must be a separate pass from merging because the condition (`2*y`) differs from the sort order. Fenwick alternative: compress `nums` and `2*nums`, query count of earlier values `> 2*x`.

> [!note]- Merge Sort Solution
> ```python
> def reversePairs(nums):               # LC 493
>     def sort(a):
>         if len(a) <= 1: return a, 0
>         mid = len(a) // 2
>         L, cl = sort(a[:mid]); R, cr = sort(a[mid:])
>         cnt, j = cl + cr, 0
>         for x in L:                          # L, R sorted; pointer j only moves right
>             while j < len(R) and x > 2 * R[j]:
>                 j += 1
>             cnt += j
>         return sorted(L + R), cnt            # Timsort merges two runs in O(n)
>     return sort(nums)[1]
> ```

> [!success] Complexity
> O(n log n) time, O(n) space. The `sorted(L + R)` merge is O(n) for two runs (Timsort); write a manual merge if the interviewer objects.

---

### Count of Range Sum `💤 T3`

> [!example] Problem
> **[H]** Count subarrays `nums[i..j]` whose sum lies in `[lower, upper]`. Example: `nums=[-2,5,-1]`, `lower=-2`, `upper=2` -> `3`.

> [!info] Approach
> With prefix sums `s`, a subarray ending at `j` is good iff an earlier prefix `p` has `s_j - upper <= p <= s_j - lower`. Compress all prefix sums (include `0`), Fenwick-count earlier prefixes, using `bisect` to convert the bounds to rank range. Merge-sort version: count with two pointers across halves of the prefix array.

> [!note]- Fenwick Solution
> ```python
> def countRangeSum(nums, lower, upper):  # LC 327, Fenwick over compressed prefix sums
>     pre = [0]
>     for x in nums: pre.append(pre[-1] + x)
>     vals = sorted(set(pre))
>     t = [0] * (len(vals) + 1)
>     def add(i):
>         while i <= len(vals): t[i] += 1; i += i & -i
>     def q(i):
>         s = 0
>         while i > 0: s += t[i]; i -= i & -i
>         return s
>     ans = 0
>     for s in pre:
>         lo = bisect_left(vals, s - upper)        # count prior prefixes p with s-upper <= p <= s-lower
>         hi = bisect_right(vals, s - lower)
>         ans += q(hi) - q(lo)
>         add(bisect_left(vals, s) + 1)
>     return ans
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

---

## Sweep Line & Intervals

---

### The Skyline Problem `🎯 T2`

> [!example] Problem
> **[H]** Buildings `[left, right, height]`; return the key points `[x, height]` of the skyline (height changes), ending with `[last_x, 0]`.

> [!info] Approach
> Sweep over sorted distinct x. Push every building with `left <= x` into a max-heap `(-h, right)`; lazily pop tops with `right <= x`; current height = top or 0. Append only when it differs from the last emitted height. Handling all events at one x before reading the max resolves same-x start/end ties. Segment-tree alternative: compress x, range-chmax heights over each building's span, then read leaves left to right.

> [!note]- Heap Sweep Solution
> ```python
> def getSkyline(buildings):            # LC 218
>     xs = sorted({x for l, r, h in buildings for x in (l, r)})
>     buildings = sorted(buildings)
>     heap, i, res = [], 0, []
>     for x in xs:
>         while i < len(buildings) and buildings[i][0] <= x:
>             heapq.heappush(heap, (-buildings[i][2], buildings[i][1])); i += 1
>         while heap and heap[0][1] <= x:
>             heapq.heappop(heap)
>         h = -heap[0][0] if heap else 0
>         if not res or res[-1][1] != h:
>             res.append([x, h])
>     return res
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

---

### My Calendar I `⚡ T1`

> [!example] Problem
> **[M]** `book(start, end)` for half-open `[start, end)`; return `True` and store it only if it overlaps no existing booking.

> [!info] Approach
> Keep disjoint bookings sorted by start in parallel lists. `i = bisect_right(starts, start)`; only the predecessor (`ends[i-1] > start`) and successor (`starts[i] < end`) can conflict.

> [!note]- Sorted-List Solution
> ```python
> class MyCalendar:                     # LC 729
>     def __init__(self): self.s, self.e = [], []      # parallel, sorted, disjoint
>     def book(self, start, end):
>         i = bisect_right(self.s, start)
>         if i > 0 and self.e[i-1] > start: return False
>         if i < len(self.s) and self.s[i] < end: return False
>         self.s.insert(i, start); self.e.insert(i, end)
>         return True
> ```

> [!success] Complexity
> O(log n) search + O(n) list insert (memmove), O(n) space.

> [!tip] Alternatives
> Brute-force O(n) scan per booking passes on LeetCode; the bisect version is the one to present.

---

### My Calendar II `🎯 T2`

> [!example] Problem
> **[M]** Same API, but reject a booking that would create a **triple** booking (three overlapping).

> [!info] Approach
> Track `booked` intervals and `over` (double-booked regions). A new interval is rejected if it overlaps any `over` region; otherwise add its intersections with `booked` to `over`, then append it to `booked`. Check before mutating.

> [!note]- Overlap-List Solution
> ```python
> class MyCalendarTwo:                  # LC 731
>     def __init__(self): self.booked, self.over = [], []
>     def book(self, start, end):
>         for s, e in self.over:
>             if start < e and s < end: return False
>         for s, e in self.booked:
>             if start < e and s < end:
>                 self.over.append((max(s, start), min(e, end)))
>         self.booked.append((start, end))
>         return True
> ```

> [!success] Complexity
> O(n) per booking, O(n) space.

> [!tip] Alternatives
> Sweep line over boundary deltas (as in Calendar III) with a `> 2` check also works.

---

### My Calendar III `🎯 T2`

> [!example] Problem
> **[H]** After each `book(start, end)`, return the maximum number of simultaneous bookings so far (k-booking).

> [!info] Approach
> Boundary deltas: `+1` at start, `-1` at end in a dict plus a sorted key list (`insort`). Sweep keys accumulating the running sum; the maximum is the answer. n <= 400 so O(n) per call is fine. For large n use a dynamic segment tree with lazy range-add / range-max over coordinates up to 1e9, or compress offline.

> [!note]- Sweep Solution
> ```python
> class MyCalendarThree:                # LC 732, sweep over sorted boundaries
>     def __init__(self): self.d = defaultdict(int); self.keys = []
>     def book(self, startTime, endTime):
>         for x, v in ((startTime, 1), (endTime, -1)):
>             if x not in self.d: insort(self.keys, x)
>             self.d[x] += v
>         cur = best = 0
>         for k in self.keys:
>             cur += self.d[k]; best = max(best, cur)
>         return best
> ```

> [!success] Complexity
> O(n) per booking (sweep over keys; insort shift is also O(n)); a dynamic segment tree gives O(log C).

---

### Range Module `💤 T3`

> [!example] Problem
> **[H]** Track half-open ranges: `addRange(l, r)`, `queryRange(l, r)` (is `[l, r)` fully tracked), `removeRange(l, r)`.

> [!info] Approach
> Maintain disjoint, merged intervals in parallel sorted lists `L`, `R`. Add: find the block of intervals touching `[l, r]` via two bisects, replace them with one merged interval. Remove: find intervals overlapping `[l, r)`, keep the left and right leftovers. Query: the interval with the greatest `L <= l` must have `R >= r`.

> [!note]- Interval-List Solution
> ```python
> class RangeModule:                    # LC 715
>     def __init__(self): self.L, self.R = [], []      # disjoint, non-touching, sorted
>     def addRange(self, left, right):
>         i, j = bisect_left(self.R, left), bisect_right(self.L, right)
>         if i < j:
>             left, right = min(left, self.L[i]), max(right, self.R[j-1])
>         self.L[i:j] = [left]; self.R[i:j] = [right]
>     def queryRange(self, left, right):
>         i = bisect_right(self.L, left) - 1
>         return i >= 0 and self.R[i] >= right
>     def removeRange(self, left, right):
>         i, j = bisect_right(self.R, left), bisect_left(self.L, right)
>         nl, nr = [], []
>         if i < j:
>             if self.L[i] < left: nl.append(self.L[i]); nr.append(left)
>             if self.R[j-1] > right: nl.append(right); nr.append(self.R[j-1])
>         self.L[i:j] = nl; self.R[i:j] = nr
> ```

> [!success] Complexity
> O(log n) search + O(n) slice replacement per op.

> [!tip] Alternatives
> A dynamic segment tree with assign-lazy handles 1e9 coordinate range in O(log C).

---

### Falling Squares `💤 T3`

> [!example] Problem
> **[H]** Squares drop one by one as `[left, sideLength]`, landing on the highest square beneath; after each, report the current maximum stack height.

> [!info] Approach
> Each square's base is the max top among earlier squares whose x-range overlaps (open overlap: `l < x+s and x < r`). With n <= 1000, O(n^2) over a list of placed squares is fine. Faster: compress coordinates and use a segment tree with range-assign + range-max lazy.

> [!note]- O(n^2) Solution
> ```python
> def fallingSquares(positions):        # LC 699, O(n^2)
>     iv, res, best = [], [], 0          # iv: (left, right, top)
>     for x, s in positions:
>         base = 0
>         for l, r, top in iv:
>             if l < x + s and x < r: base = max(base, top)
>         iv.append((x, x + s, base + s))
>         best = max(best, base + s); res.append(best)
>     return res
> ```

> [!success] Complexity
> O(n^2) time (segment tree: O(n log n)), O(n) space.

---

## Heaps & Windows

---

### Sliding Window Median `🎯 T2`

> [!example] Problem
> **[H]** Return the median of every window of size `k` over `nums` (float for even `k`). Example: `[1,3,-1,-3,5,3,6,7]`, `k=3` -> `[1,-1,-1,3,5,6]`.

> [!info] Approach
> **Two heaps with lazy deletion**: max-heap `small` (negated) holds the lower half (size `ceil(k/2)`), min-heap `large` the upper. Sliding: mark the outgoing value in `dead`, insert the incoming value to the proper side, track a balance of live-size difference, move one top across if unbalanced, then prune dead tops. **Simpler**: keep a sorted window list, `del w[bisect_left(...)]` + `insort` (O(k) memmove per step, fine for k up to ~1e4-1e5); or `SortedList` and index `k//2`.

> [!note]- Two-Heap Solution
> ```python
> def medianSlidingWindow(nums, k):     # LC 480, two heaps + lazy deletion
>     small, large = [], []              # small: max-heap via negation
>     dead = defaultdict(int)
>     def prune(h, sign):
>         while h and dead[sign * h[0]]:
>             dead[sign * h[0]] -= 1; heapq.heappop(h)
>     for x in nums[:k]:
>         heapq.heappush(small, -x)
>     for _ in range(k // 2):
>         heapq.heappush(large, -heapq.heappop(small))
>     res = []
>     for i in range(k, len(nums) + 1):
>         res.append(float(-small[0]) if k & 1 else (-small[0] + large[0]) / 2)
>         if i == len(nums): break
>         out, inn = nums[i - k], nums[i]
>         bal = -1 if out <= -small[0] else 1     # which side loses a live element
>         dead[out] += 1
>         if inn <= -small[0]:
>             heapq.heappush(small, -inn); bal += 1
>         else:
>             heapq.heappush(large, inn); bal -= 1
>         if bal > 0:                              # small has one too many live
>             heapq.heappush(large, -heapq.heappop(small))
>         elif bal < 0:
>             heapq.heappush(small, -heapq.heappop(large))
>         prune(small, -1); prune(large, 1)
>     return res
> ```

> [!note]- Sorted-Window Fallback
> ```python
> def medianSlidingWindowBisect(nums, k):   # simple O(n*k) memmove fallback
>     w = sorted(nums[:k]); res = []
>     for i in range(k, len(nums) + 1):
>         res.append(float(w[k//2]) if k & 1 else (w[k//2 - 1] + w[k//2]) / 2)
>         if i == len(nums): break
>         del w[bisect_left(w, nums[i - k])]
>         insort(w, nums[i])
>     return res
> ```

> [!success] Complexity
> Heaps: O(n log k) time, O(n) worst-case space for dead entries. Sorted window: O(n·k) with tiny constant.

> [!tip] Alternatives
> Float-valued medians: use `(a + b) / 2`, never `//`.

---

## Order Statistics with Fenwick

---

### Create Sorted Array through Instructions `💤 T3`

> [!example] Problem
> **[H]** Insert `instructions[i]` one by one into an initially empty array; cost of each insert is `min(# strictly smaller, # strictly larger)` among existing elements. Return the total cost mod 1e9+7.

> [!info] Approach
> Fenwick over values (max value <= 1e5, so no compression). Before inserting `x` as the n-th element (`n` already present): `less = prefix(x-1)`, `leq = prefix(x)`, `greater = n - leq`. Add `min(less, greater)`, then `add(x, 1)`.

> [!note]- Fenwick Solution
> ```python
> def createSortedArray(instructions):  # LC 1649
>     MOD = 10**9 + 7
>     M = max(instructions)
>     t = [0] * (M + 1)
>     cost = 0
>     for n, x in enumerate(instructions):
>         i, less = x - 1, 0
>         while i: less += t[i]; i -= i & -i
>         i, le = x, 0
>         while i: le += t[i]; i -= i & -i
>         cost += min(less, n - le)
>         i = x
>         while i <= M: t[i] += 1; i += i & -i
>     return cost % MOD
> ```

> [!success] Complexity
> O(n log M) time, O(M) space.

> [!tip] Alternatives
> If values are large, compress first (sorted unique ranks).

---
