---
tags: [coding, algorithms, sorting]
topic: Sorting
difficulty: mixed
---
# Sorting — Problem Compendium

## What this covers

> [!abstract] In this file
> **Covers:** Worked sorting problems: merge-sort variants (inversions), quickselect, bucket sort, intervals/sweep line, custom ordering, topological sort, K-way merge.
> **You'll be able to:** Use sort as the first step and know when quickselect/bucket sort beats it.
> **Prereqs:** Sorting lecture · **Pair with:** [Sorting lecture](../../03-algorithms/01-sorting.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [QuickSort / QuickSelect](#quicksort--quickselect) · [Bucket Sort](#bucket-sort) · [Interview Classics](#interview-classics) · [Classic Merge Variants](#classic-merge-variants) · [Interval / Sweep Line](#interval--sweep-line) · [Offline Sorting Tricks](#offline-sorting-tricks) · [Topological Sort](#topological-sort) · [External Sort / K-way Merge](#external-sort--k-way-merge) · [Sorting Applications](#sorting-applications)

---

> [!info] Approach
> Identify what property sorting exposes (adjacency, rank, monotone structure), then apply the right sort variant. Non-comparison sorts (counting/radix/bucket) bypass O(n log n) when keys are bounded integers. QuickSelect gets rank-k in O(n) avg. Merge sort naturally counts cross-half inversions.

---

## QuickSort / QuickSelect

**Also try:**

- **Maximum Gap (Bucket Sort)** — Comparison sort O(n log n) is too slow

---

## Bucket Sort

**Also try:**

- **Pancake Sorting** — Standard swaps aren't available; only prefix reversals
- **Custom Sort String** — Standard sort knows nothing about the custom ordering
- **Largest Number (custom comparator)** — Numeric sort fails (e.g., 9 vs 91: "991" > "919" so 9 should precede 91)
- **Wiggle Sort II (LC 324)** — Find median, then place larger-than-median elements at odd indices and smaller-than-median elements at even indices, both in reverse order t…

---

## Interview Classics

---

### H-Index (LC 274) `⚡ T1`

> [!example] Problem
> Given an array of integers citations where citations[i] is the number of citations a researcher received for their ith paper, return the researcher's h-index.
> According to the definition of h-index on Wikipedia: The h-index is defined as the maximum value of h such that the given researcher has published at least h papers that have each been cited at least h times.
> 
> **Example 1:**
> ```
> Input: citations = [3,0,6,1,5]
> Output: 3
> Explanation: [3,0,6,1,5] means the researcher has 5 papers in total and each of them had received 3, 0, 6, 1, 5 citations respectively.
> Since the researcher has 3 papers with at least 3 citations each and the remaining two with no more than 3 citations each, their h-index is 3.
> ```
> 
> **Example 2:**
> ```
> Input: citations = [1,3,1]
> Output: 1
> ```
> 
> **Constraints:**
> - n == citations.length
> - 1 <= n <= 5000
> - 0 <= citations[i] <= 1000

> [!info] Approach
> After sorting descending, at position i (0-indexed), if citations[i] >= i+1 then at least i+1 papers have >= i+1 citations. Track the largest such i+1. Sort descending; scan linearly to find max h. For each i, if citations[i] >= i+1, update h = i+1. Return max h found.

> [!note]- Python Solution
> ```python
> def h_index(citations):
>     citations.sort(reverse=True)
>     h = 0
>     for i, c in enumerate(citations):
>         if c >= i + 1:
>             h = i + 1
>         else:
>             break
>     return h
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> Counting sort O(n): bucket[min(c, n)] += 1; scan from n down accumulating count — stop when cumulative count >= bucket index. Binary search on sorted array O(n log n) same asymptotic.

**Also try:**

- **Meeting Rooms II (LC 253)** — see [Meeting Rooms II](09-greedy.md#interval-greedy)

---

## Classic Merge Variants

---

### Majority Element (Boyer-Moore) `🎯 T2`

> Full walkthrough: [Majority Element](../data-structures/01-array.md#majority-element--t2).

**Also try:**

- **Sort an Array (Counting Sort Variant)** — Comparison-based sorts bottom out at O(n log n); counting sort exploits a bounded integer domain to achieve O(n + k)
- **Radix Sort Implementation** — Achieves O(d · (n + b)) where d = number of digits, b = base (10)
- **Maximum Number After Digit Swaps (LC 2231)** — Digits at even positions can only be rearranged among themselves; same for odd positions

---

## Interval / Sweep Line

**Also try:**

- **Minimum Number of Arrows to Burst Balloons (LC 452)** — see [Minimum Number of Arrows to Burst Balloons](09-greedy.md#interval-greedy)

---

## Offline Sorting Tricks

**Also try:**

- **Sort Array by Parity (LC 905)** — Classic two-pointer Dutch-flag-style partition
- **Advantages Shuffle (LC 870)** — Greedy: for each element of `nums2` (sorted descending), try to "beat" it with the smallest element of `nums1` that is still larger

---

## Topological Sort

---

### Course Schedule II (LC 210) `⚡ T1`

> Full walkthrough: [Course Schedule II](../data-structures/11-graph.md#course-schedule-ii--t1).

---

### Alien Dictionary (LC 269) `⚡ T1`

> Full walkthrough: [Alien Dictionary](../data-structures/06-queue.md#alien-dictionary--t1).

---

## External Sort / K-way Merge

---

### Find K Pairs with Smallest Sums (LC 373) `⚡ T1`

> Full walkthrough: [Find K Pairs with Smallest Sums](../data-structures/10-heap.md#find-k-pairs-with-smallest-sums--t1).

---

### Kth Largest Element in a Stream (LC 703) `⚡ T1`

> Full walkthrough: [Kth Largest Element in a Stream](../data-structures/10-heap.md#kth-largest-element-in-a-stream--t1).

---

### Find Median from Data Stream (LC 295) `⚡ T1`

> Full walkthrough: [Find Median from Data Stream](../data-structures/06-queue.md#find-median-from-data-stream--t1).

---

## Sorting Applications

**Also try:**

- **Relative Sort Array (LC 1122)** — Standard sorting can't directly encode a custom ordering defined by another array

---

## See Also

[[array]] | [[binary-search]] | [[greedy]] | [[two-pointers]]
