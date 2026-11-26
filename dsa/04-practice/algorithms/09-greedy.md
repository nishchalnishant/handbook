---
tags: [coding, algorithms, greedy]
topic: Greedy Algorithms
difficulty: mixed
---
# Greedy Algorithms — Problem Compendium

## What this covers

> [!abstract] In this file
> **Covers:** Worked greedy problems: interval scheduling, jump/coverage, string/array greedy, sorting-based greedy, sweep line.
> **You'll be able to:** Justify each greedy choice in one sentence before coding.
> **Prereqs:** Greedy lecture · **Pair with:** [Greedy lecture](../../03-algorithms/09-greedy.md) · **Time:** 2–3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Interval Greedy](#interval-greedy) · [Simple Greedy](#simple-greedy) · [Jump / Coverage Greedy](#jump--coverage-greedy) · [String / Array Greedy](#string--array-greedy) · [Sorting-Based Greedy](#sorting-based-greedy)

> [!tip] If you only have 20 minutes
> **Do these first:** [Merge Intervals](#merge-intervals--t2) · [Non-overlapping Intervals (Minimum number to remove)](#non-overlapping-intervals-minimum-number-to-remove--t2) · [Meeting Rooms II](#interval-greedy) · [Minimum Number of Arrows to Burst Balloons](#interval-greedy) · [Jump Game (can reach?)](#jump-game-can-reach--t2) · [Jump Game II (minimum jumps)](#jump-game-ii-minimum-jumps--t2) · [Gas Station](#gas-station--t2) · [Partition Labels](#string--array-greedy) · [Reorganize String](#reorganize-string--t1)
> **Template:** Interval scheduling: sort by **end**, take an interval if `start >= last_end` (max non-overlapping = n − min removals).
> **Template:** Merge: sort by **start**, extend `cur_end = max(cur_end, e)` while overlapping.
> **Gotchas:** Greedy needs a one-line exchange argument — say it, or switch to DP · end-sort vs start-sort is the whole problem · touching endpoints (`<` vs `<=`) — ask · Gas Station: total < 0 ⇒ −1; else restart after any negative prefix.

---

Greedy works when a locally optimal choice at each step provably leads to a globally optimal solution (greedy-choice property + optimal substructure). Proof strategy: exchange argument — show any solution deviating from the greedy choice can be transformed into the greedy solution without worsening it. If no such argument holds, use DP.

---

## Interval Greedy

---

### Merge Intervals `🎯 T2`

> [!example] Problem
> Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
> Output: [[1,6],[8,10],[15,18]]
> Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,4],[4,5]]
> Output: [[1,5]]
> Explanation: Intervals [1,4] and [4,5] are considered overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^4
> - intervals[i].length == 2
> - 0 <= starti <= endi <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** "Overlapping ranges" · **Gotcha:** Update `end = max(end, next_end)`, not just `next_end`.

> [!info] Approach
> In arbitrary order, overlaps can't be detected without O(n²) pair checks. Sorting by start makes all overlapping intervals adjacent — one linear scan suffices. Sort by start; maintain a running merged interval; extend its end if current interval overlaps. `merged[-1][1] = max(merged[-1][1], end)` when `start ≤ merged[-1][1]`.

> [!note]- Python Solution
> ```python
> def merge(intervals):
>     intervals.sort(key=lambda x: x[0])
>     merged = []
>     for start, end in intervals:
>         if merged and start <= merged[-1][1]:
>             merged[-1][1] = max(merged[-1][1], end)
>         else:
>             merged.append([start, end])
>     return merged
> ```

> [!success] Complexity
> O(n log n) time, O(n) space.

> [!tip] Alternatives
> Sweep line with events (+1 at start, -1 at end) — O(n log n), harder to reconstruct intervals.

---

### Non-overlapping Intervals (Minimum number to remove) `🎯 T2`

> [!example] Problem
> Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping.
> Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
> 
> **Example 1:**
> ```
> Input: intervals = [[1,2],[2,3],[3,4],[1,3]]
> Output: 1
> Explanation: [1,3] can be removed and the rest of the intervals are non-overlapping.
> ```
> 
> **Example 2:**
> ```
> Input: intervals = [[1,2],[1,2],[1,2]]
> Output: 2
> Explanation: You need to remove two [1,2] to make the rest of the intervals non-overlapping.
> ```
> 
> **Example 3:**
> ```
> Input: intervals = [[1,2],[2,3]]
> Output: 0
> Explanation: You don't need to remove any of the intervals since they're already non-overlapping.
> ```
> 
> **Constraints:**
> - 1 <= intervals.length <= 10^5
> - intervals[i].length == 2
> - -5 * 10^4 <= starti < endi <= 5 * 10^4

> [!tip] Recognize · Gotcha
> **Signal:** Min removals · **Gotcha:** **Sort by end** not start — **counterexample** if start sort.

> [!info] Approach
> Equivalent to maximizing the number of non-overlapping intervals kept (classic Activity Selection). Exchange argument: among all intervals overlapping with the current boundary, keeping the one with the earliest end leaves maximum room — any other choice can only tighten the constraint. Sort by end time. Greedily keep intervals that don't overlap with the last kept interval. Count removals. Track `last_end`; if `start >= last_end`, keep (update last_end = end); else remove (increment count).

> [!note]- Python Solution
> ```python
> def erase_overlap_intervals(intervals):
>     intervals.sort(key=lambda x: x[1])
>     last_end = float('-inf')
>     remove = 0
>     for start, end in intervals:
>         if start >= last_end:
>             last_end = end
>         else:
>             remove += 1
>     return remove
> ```

> [!success] Complexity
> O(n log n) time, O(1) space.

> [!tip] Alternatives
> DP longest non-overlapping chain: O(n²) without binary search, O(n log n) with — same asymptotic but more complex. Answer = n - (max non-overlapping count).

---

### Interval List Intersections `⚡ T1`

**Problem**: Two lists of sorted, disjoint intervals. Return their intersections.

**Key Insight**: Two pointers. Candidate intersection = `[max(starts), min(ends)]`, real iff `start <= end`. Advance whichever interval **ends first** — it can't intersect anything else.

```python
def intervalIntersection(A, B):
    res, i, j = [], 0, 0
    while i < len(A) and j < len(B):
        s = max(A[i][0], B[j][0])
        e = min(A[i][1], B[j][1])
        if s <= e:
            res.append([s, e])
        if A[i][1] < B[j][1]:
            i += 1
        else:
            j += 1
    return res
```

**TC**: O(m + n) | **SC**: O(1) extra | Same "advance the smaller end" move as merge sort's merge step.

---

### My Calendar I `⚡ T1`

**Problem**: `book(start, end)` succeeds only if the event doesn't double-book with any prior booking. Bookings arrive online.

**Key Insight**: The *online* version of interval overlap. Keep a sorted list of bookings; conflict iff the symmetric overlap test fires against a neighbor. With `SortedList`, bisect to find the insertion point and check only the two neighbors — O(log n). A plain list with a linear scan is acceptable if you state it's O(n).

```python
from sortedcontainers import SortedList

class MyCalendar:
    def __init__(self):
        self.cal = SortedList()

    def book(self, start, end):
        i = self.cal.bisect_right((start, end))
        if i > 0 and self.cal[i-1][1] > start:
            return False
        if i < len(self.cal) and self.cal[i][0] < end:
            return False
        self.cal.add((start, end))
        return True
```

**TC**: O(log n) per booking | **SC**: O(n)

---

### My Calendar II `🎯 T2`

**Problem**: Same, but allow double-booking; reject only **triple** bookings.

**Key Insight**: Keep two lists: `bookings` and `overlaps` (regions already booked twice). A new event causes a triple booking iff it intersects anything in `overlaps`. Otherwise, add its intersections with `bookings` to `overlaps`, then add it to `bookings`. Generalization to "at most k" = sweep line with a diff map (My Calendar III).

```python
class MyCalendarTwo:
    def __init__(self):
        self.bookings = []
        self.overlaps = []

    def book(self, start, end):
        for s, e in self.overlaps:
            if start < e and s < end:
                return False
        for s, e in self.bookings:
            if start < e and s < end:
                self.overlaps.append((max(start, s), min(end, e)))
        self.bookings.append((start, end))
        return True
```

**TC**: O(n) per booking | **SC**: O(n)

---

### Car Pooling `🎯 T2`

> Full walkthrough: [Car Pooling](../data-structures/01-array.md#car-pooling--t2) — difference array, not greedy; listed here because it is often confused with Meeting Rooms II.

---

### Employee Free Time `🎯 T2`

**Problem**: Each employee has a sorted list of working intervals. Return the finite intervals where **everyone** is free.

**Key Insight**: Individual ownership doesn't matter — flatten all intervals, sort by start, merge; the **gaps between merged blocks** are the common free time. K-way heap merge saves the sort if lists are long (say it as the follow-up).

```python
def employeeFreeTime(schedule):
    ivals = sorted((iv.start, iv.end) for emp in schedule for iv in emp)
    res, end = [], ivals[0][1]
    for s, e in ivals[1:]:
        if s > end:
            res.append((end, s))
        end = max(end, e)
    return res
```

**TC**: O(n log n) | **SC**: O(n) | Related: Merge Intervals (this is its "invert the output" twin)

**Also try:**

- **Meeting Rooms II** — Each new meeting either reuses an ended room or opens a new one
- **Minimum Number of Arrows to Burst Balloons** — Same as activity selection but we want to maximize simultaneous coverage (one arrow covers all overlapping intervals at a point)
- **Minimum Taps to Open to Water a Garden** — Same as Video Stitching — interval covering problem
- **Minimum Number of Groups for Non-Overlapping Intervals** — This is exactly Meeting Rooms II — minimum rooms = minimum groups

---

## Simple Greedy

---

### Best Time to Buy and Sell Stock II (LC 122) `⚡ T1`

> [!example] Problem
> `prices[i]` is the price on day `i`. Unlimited transactions, at most one share held at a time; you may buy and sell on the same day. Return max profit. **Medium.**
>
> ```
> Input: [7,1,5,3,6,4]  →  7   (buy 1 sell 5, buy 3 sell 6)
> Input: [1,2,3,4,5]    →  4   (one long hold == four one-day gains)
> Input: [7,6,4,3,1]    →  0
> ```

> [!tip] Recognize · Gotcha
> **Signal:** "as many transactions as you like" · **Gotcha:** don't hunt for valley/peak pairs explicitly — summing every positive `p[i] − p[i−1]` is the same number and has no off-by-one risk.

> [!info] Approach
> **Key insight:** any profitable hold from day `a` to day `b` equals the sum of the day-to-day deltas between them, so collecting every positive delta is optimal and never worse than any schedule. **Exchange argument:** a schedule that skips a positive delta can add that one-day trade without conflicting with anything.

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
> ```

> [!success] Complexity
> **TC**: O(n) | **SC**: O(1).

> [!tip] Alternatives
> State-machine DP `hold = max(hold, cash − p)`, `cash = max(cash, hold + p)` — same answer, and it is the form that extends to cooldown / fee / k transactions ([all variants](08-dynamic-programming.md#best-time-to-buy-and-sell-stock-all-variants--t2)).

**Also try:**

- **Assign Cookies (LC 455)** — Sort both
- **Largest Perimeter Triangle (LC 976)** — Triangle inequality: a+b > c where a≤b≤c

---

## Jump / Coverage Greedy

---

### Jump Game (can reach?) `🎯 T2`

> [!example] Problem
> You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position.
> Return true if you can reach the last index, or false otherwise.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: true
> Explanation: Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,1,0,4]
> Output: false
> Explanation: You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 10^5

> [!tip] Recognize · Gotcha
> **Signal:** "Can you reach the end?" · **Gotcha:** O(N) — not DP. Greedy works because reaching farther never hurts.

> [!info] Approach
> At any reachable index i, all indices up to `i + nums[i]` are also reachable — the reachable set is always a contiguous prefix `[0, max_reach]`. Track the frontier; if current index exceeds it, the last index is unreachable. Track `max_reach = max(i + nums[i])` for all reachable i. If `i > max_reach` at any point, return False. Single pass; early exit the moment current index exceeds max_reach.

> [!note]- Python Solution
> ```python
> def can_jump(nums):
>     max_reach = 0
>     for i, jump in enumerate(nums):
>         if i > max_reach:
>             return False
>         max_reach = max(max_reach, i + jump)
>     return True
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> DP O(n²) — `dp[i] = any(dp[j] and j+nums[j]>=i for j<i)`. Backward scan: track `goal = n-1`, update if `i + nums[i] >= goal`. Greedy subsumes both.

---

### Jump Game II (minimum jumps) `🎯 T2`

> [!example] Problem
> You are given a 0-indexed array of integers nums of length n. You are initially positioned at nums[0].
> Each element nums[i] represents the maximum length of a forward jump from index i. In other words, if you are at nums[i], you can jump to any nums[i + j] where:
> Return the minimum number of jumps to reach nums[n - 1]. The test cases are generated such that you can reach nums[n - 1].
> 
> **Example 1:**
> ```
> Input: nums = [2,3,1,1,4]
> Output: 2
> Explanation: The minimum number of jumps to reach the last index is 2. Jump 1 step from index 0 to 1, then 3 steps to the last index.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,3,0,1,4]
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - 0 <= nums[i] <= 1000
> - It's guaranteed that you can reach nums[n - 1].

> [!tip] Recognize · Gotcha
> **Signal:** Min jumps · **Gotcha:** **O(n)** single pass; **Jump Game I** is only reachability (different).

> [!info] Approach
> At each "jump boundary," we must take a new jump. Exchange argument: among all positions reachable in the current jump, choosing the one that extends furthest is always optimal — picking any shorter reach can only worsen future options. Maintain `cur_end` (end of current jump range) and `farthest` (max reach seen so far). When `i == cur_end`, take a jump: increment count, advance `cur_end = farthest`. Loop only to `n-2` (last index doesn't need a jump from it).

> [!note]- Python Solution
> ```python
> def jump(nums):
>     jumps = cur_end = farthest = 0
>     for i in range(len(nums) - 1):
>         farthest = max(farthest, i + nums[i])
>         if i == cur_end:
>             jumps += 1
>             cur_end = farthest
>     return jumps
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> BFS level-by-level — conceptually identical, O(n), more code. DP O(n²).

---

### Jump Game VI (DP + Deque) `🎯 T2`

> Full walkthrough: [Jump Game VI (LC 1696)](03-sliding-window.md#jump-game-vi-lc-1696--t2).

---

### Candy (LC 135) `🎯 T2`

> [!example] Problem
> There are n children standing in a line. Each child is assigned a rating value given in the integer array ratings.
> You are giving candies to these children subjected to the following requirements:
> Return the minimum number of candies you need to have to distribute the candies to the children.
> 
> **Example 1:**
> ```
> Input: ratings = [1,0,2]
> Output: 5
> Explanation: You can allocate to the first, second and third child with 2, 1, 2 candies respectively.
> ```
> 
> **Example 2:**
> ```
> Input: ratings = [1,2,2]
> Output: 4
> Explanation: You can allocate to the first, second and third child with 1, 2, 1 candies respectively.
> The third child gets 1 candy because it satisfies the above two conditions.
> ```
> 
> **Constraints:**
> - n == ratings.length
> - 1 <= n <= 2 * 10^4
> - 0 <= ratings[i] <= 2 * 10^4

> [!info] Approach
> Two constraints (left and right neighbors) conflict if solved simultaneously. Solve each independently and take max. Two passes — left-to-right enforces left constraint, right-to-left enforces right constraint.

>   1. Init candies = [1]*n.
>   2. Left pass: if ratings[i] > ratings[i-1]: candies[i] = candies[i-1]+1.
>   3. Right pass: if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1]+1).
>   4. Return sum(candies).

> [!note]- Python Solution
> ```python
> def candy(ratings):
>     n = len(ratings)
>     candies = [1] * n
>     for i in range(1, n):
>         if ratings[i] > ratings[i - 1]:
>             candies[i] = candies[i - 1] + 1
>     for i in range(n - 2, -1, -1):
>         if ratings[i] > ratings[i + 1]:
>             candies[i] = max(candies[i], candies[i + 1] + 1)
>     return sum(candies)
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> One-pass O(n) with slope tracking — track ascending/descending runs and handle peak reassignment; complex but O(1) space.

---

### Reorganize String `⚡ T1`

> Full walkthrough: [Reorganize String (LC 767)](../data-structures/10-heap.md#reorganize-string-lc-767--t1).

**Also try:**

- **Rearrange String k Distance Apart (Rearrange Barcodes)** — Generalization of Reorganize String with cooldown k instead of 1
- **Video Stitching (LC 1024)** — This is the classic "minimum jumps to cover a range" greedy problem
- **Minimum Taps to Water a Garden (LC 1326)** — This reduces directly to the Jump Game II / interval cover problem

---

## String / Array Greedy

---

### Gas Station `🎯 T2`

> [!example] Problem
> There are n gas stations along a circular route, where the amount of gas at the ith station is gas[i].
> You have a car with an unlimited gas tank and it costs cost[i] of gas to travel from the ith station to its next (i + 1)th station. You begin the journey with an empty tank at one of the gas stations.
> Given two integer arrays gas and cost, return the starting gas station's index if you can travel around the circuit once in the clockwise direction, otherwise return -1. If there exists a solution, it is guaranteed to be unique.
> 
> **Example 1:**
> ```
> Input: gas = [1,2,3,4,5], cost = [3,4,5,1,2]
> Output: 3
> Explanation:
> Start at station 3 (index 3) and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 4. Your tank = 4 - 1 + 5 = 8
> Travel to station 0. Your tank = 8 - 2 + 1 = 7
> Travel to station 1. Your tank = 7 - 3 + 2 = 6
> Travel to station 2. Your tank = 6 - 4 + 3 = 5
> Travel to station 3. The cost is 5. Your gas is just enough to travel back to station 3.
> Therefore, return 3 as the starting index.
> ```
> 
> **Example 2:**
> ```
> Input: gas = [2,3,4], cost = [3,4,3]
> Output: -1
> Explanation:
> You can't start at station 0 or 1, as there is not enough gas to travel to the next station.
> Let's start at station 2 and fill up with 4 unit of gas. Your tank = 0 + 4 = 4
> Travel to station 0. Your tank = 4 - 3 + 2 = 3
> Travel to station 1. Your tank = 3 - 3 + 3 = 3
> You cannot travel back to station 2, as it requires 4 unit of gas but you only have 3.
> Therefore, you can't travel around the circuit once no matter where you start.
> ```
> 
> **Constraints:**
> - n == gas.length == cost.length
> - 1 <= n <= 10^5
> - 0 <= gas[i], cost[i] <= 10^4
> - The input is generated such that the answer is unique.

> [!tip] Recognize · Gotcha
> **Signal:** Circular greedy · **Gotcha:** **Proof** — if sum ≥ 0 solution exists; **O(n)** single pass.

> [!info] Approach
> Two insights: (1) If total gas < total cost, no solution. (2) If solution exists, the starting point is the index after the last point where cumulative tank went negative. Proof: any station between `start` and the negative-tank point would inherit a deficit. Track running tank. When tank < 0, reset to 0 and update start = i+1. Single pass. Feasibility check built into the same pass via total sum.

> [!note]- Python Solution
> ```python
> def can_complete_circuit(gas, cost):
>     if sum(gas) < sum(cost):
>         return -1
>     tank = start = 0
>     for i in range(len(gas)):
>         tank += gas[i] - cost[i]
>         if tank < 0:
>             tank = 0
>             start = i + 1
>     return start
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Brute force O(n²): try each start. Prefix sum: find index after global minimum of `diff` prefix sums — equivalent.

---

### Trapping Rain Water (greedy view) `⚡ T1`

> Full walkthrough: [Trapping Rain Water (LC 42)](02-two-pointers.md#trapping-rain-water-lc-42--t1).

**Also try:**

- **GCD of Strings** — A GCD string must divide both strings
- **Connect Sticks (Huffman / Min Cost)** — Each stick's length contributes to the total cost once per merge it participates in
- **Minimum Difference After Operations** — After removing k elements, we keep n-k elements
- **Partition Labels (LC 763)** — Each character must stay in one partition — it determines the right boundary of the partition containing its first occurrence

---

## Sorting-Based Greedy

---

### IPO (Maximize Capital, LC 502) `⚡ T1`

> Full walkthrough: [IPO (Maximize Capital)](../data-structures/10-heap.md#ipo-maximize-capital--t1).

---

### Hand of Straights `🎯 T2`

**Problem**: Given a hand of cards and a groupSize, check if you can rearrange them into groups of `groupSize` consecutive cards.

**Key Insight**: Use an ordered map (sorted Counter). Always start from the smallest card — if you can't form a group starting from smallest, it's impossible.

```python
from collections import Counter
def isNStraightHand(hand, groupSize):
    if len(hand) % groupSize: return False
    count = Counter(hand)
    for card in sorted(count):
        if count[card]:
            freq = count[card]
            for i in range(groupSize):
                count[card + i] -= freq
                if count[card + i] < 0: return False
    return True
```

**TC**: O(n log n) | **SC**: O(n) | Related: Task Scheduler (same greedy idea)

**Also try:**

- **Queue Reconstruction by Height (LC 406)** — Taller people are invisible to shorter ones for the k-count
- **Activity Selection (Maximum Non-Overlapping Intervals)** — Greedy by earliest finishing time leaves the most room for future intervals

---

## See Also

[[dynamic-programming]] | [[sorting]] | [[heap]] | [[binary-search]]
[[dynamic-programming]] | [[sorting]] | [[heap]] | [[binary-search]] | [[sliding-window]]
