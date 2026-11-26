---
tags: [coding, algorithms, two-pointers]
topic: Two Pointers
difficulty: mixed
---
# Two Pointers — Problem Set

## What this covers

> [!abstract] In this file
> **Covers:** Worked two-pointer problems: converging, fast/slow, partition, palindrome, two-sum variants, greedy two-pointer.
> **You'll be able to:** Solve the T1 two-pointer set cold with a stated invariant.
> **Prereqs:** Two-pointers lecture · **Pair with:** [Two-pointers lecture](../../03-algorithms/02-two-pointers.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Opposite Ends (Sorted Array)](#opposite-ends-sorted-array) · [Same Direction (Fast/Slow)](#same-direction-fastslow) · [Partition / Dutch National Flag](#partition--dutch-national-flag) · [Linked List Two Pointers](#linked-list-two-pointers) · [Palindrome Two Pointers](#palindrome-two-pointers) · [Hash Map Two-Sum Variant](#hash-map-two-sum-variant) · [Sorted Array / Two-Pointer Greedy](#sorted-array--two-pointer-greedy) · [Two-Pointer on Strings](#two-pointer-on-strings)

> [!tip] If you only have 20 minutes
> **Do these first:** [Two Sum II — Input Array is Sorted](#two-sum-ii--input-array-is-sorted-lc-167--t1) · [3Sum](#3sum-lc-15--t1) · [Container With Most Water](#container-with-most-water-lc-11--t1) · [Trapping Rain Water](#trapping-rain-water-lc-42--t1) · [Remove Duplicates from Sorted Array](#remove-duplicates-from-sorted-array-lc-26--t1) · [Move Zeroes](#move-zeroes-lc-283--t1) · [Sort Colors](#sort-colors-lc-75--t1) · [3Sum Closest](#3sum-closest-lc-16--t1)
> **Template:** Opposite ends on sorted input: `while l < r: s = a[l] + a[r]; if s == t: ... elif s < t: l += 1 else: r -= 1`.
> **Template:** Read/write pointers: `w = 0; for r in range(n): if keep(a[r]): a[w] = a[r]; w += 1`.
> **Gotchas:** 3Sum dedup: skip equal `a[i]` at the outer loop AND advance past equal `a[l]`/`a[r]` after a hit · Container: always move the shorter side · Sort Colors: don't advance `i` after swapping with `hi` · two pointers need sorted (or monotone) input.

---

## Opposite Ends (Sorted Array)

> [!info] Approach
> On a sorted array, `arr[lo] + arr[hi]` is controlled: too small → move `lo` right (increase); too large → move `hi` left (decrease). Every comparison eliminates an entire row or column of pairs, reducing O(n²) brute force to O(n).

---

### Two Sum II — Input Array is Sorted (LC 167) `⚡ T1`

> [!example] Problem
> Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be numbers[index1] and numbers[index2] where 1 <= index1 < index2 <= numbers.length.
> Return the indices of the two numbers, index1 and index2, added by one as an integer array [index1, index2] of length 2.
> The tests are generated such that there is exactly one solution. You may not use the same element twice.
> Your solution must use only constant extra space.
> 
> **Example 1:**
> ```
> Input: numbers = [2,7,11,15], target = 9
> Output: [1,2]
> Explanation: The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].
> ```
> 
> **Example 2:**
> ```
> Input: numbers = [2,3,4], target = 6
> Output: [1,3]
> Explanation: The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].
> ```
> 
> **Example 3:**
> ```
> Input: numbers = [-1,0], target = -1
> Output: [1,2]
> Explanation: The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].
> ```
> 
> **Constraints:**
> - 2 <= numbers.length <= 3 * 10^4
> - -1000 <= numbers[i] <= 1000
> - numbers is sorted in non-decreasing order.
> - -1000 <= target <= 1000
> - The tests are generated such that there is exactly one solution.

> [!tip] Recognize · Gotcha
> **Signal:** Complement from both ends · **Gotcha:** Input must be **sorted**; 1-indexed return in some problems.

> [!info] Approach
> Array is sorted — sum is monotonically controlled by which endpoints we choose. Brute force O(n²) is unnecessary. Converging pointers `lo = 0, hi = n-1`. Sum < target → `lo += 1`; sum > target → `hi -= 1`; sum == target → return. Each step either finds the answer or eliminates at least one impossible pair. Total: O(n) steps.

> [!note]- Python Solution
> ```python
> def two_sum_sorted(numbers, target):
>     lo, hi = 0, len(numbers) - 1
>     while lo < hi:
>         s = numbers[lo] + numbers[hi]
>         if s == target:
>             return [lo + 1, hi + 1]   # problem wants 1-based indices
>         elif s < target:
>             lo += 1
>         else:
>             hi -= 1
>     return []   # guaranteed to find
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> HashMap O(n) time + O(n) space — use when array is unsorted; sorted input makes two pointers strictly better.

---

### 3Sum (LC 15) `⚡ T1`

> [!example] Problem
> Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
> Notice that the solution set must not contain duplicate triplets.
> 
> **Example 1:**
> ```
> Input: nums = [-1,0,1,2,-1,-4]
> Output: [[-1,-1,2],[-1,0,1]]
> Explanation: 
> nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
> nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
> nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
> The distinct triplets are [-1,0,1] and [-1,-1,2].
> Notice that the order of the output and the order of the triplets does not matter.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,1]
> Output: []
> Explanation: The only possible triplet does not sum up to 0.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,0,0]
> Output: [[0,0,0]]
> Explanation: The only possible triplet sums up to 0.
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 3000
> - -10^5 <= nums[i] <= 10^5

> [!tip] Recognize · Gotcha
> **Signal:** Fix i; two-pointer on rest · **Gotcha:** Sort first; skip **all** equal values at each level.

> [!failure] Tempting wrong approach
> Dedup with `set(tuple(sorted(t)))` over a hash-based pair search — O(n²) time but hides the real skip logic and costs extra memory. Sort, then skip equal neighbors for `i`, `lo`, and `hi`.

> [!info] Approach
> O(n³) brute force is too slow. Fix one element; remaining two-sum on sorted subarray reduces to O(n²) total. Sort array. For each anchor `i`, run converging two-pointer on `[i+1, n-1]`. Skip duplicate anchors (`nums[i] == nums[i-1]`). On finding a triplet, skip duplicate inner pointers before advancing.

> [!note]- Python Solution
> ```python
> def three_sum(nums):
>     nums.sort()
>     result = []
>     for i in range(len(nums) - 2):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue   # skip duplicate anchor
>         lo, hi = i + 1, len(nums) - 1
>         while lo < hi:
>             s = nums[i] + nums[lo] + nums[hi]
>             if s == 0:
>                 result.append([nums[i], nums[lo], nums[hi]])
>                 while lo < hi and nums[lo] == nums[lo + 1]: lo += 1
>                 while lo < hi and nums[hi] == nums[hi - 1]: hi -= 1
>                 lo += 1
>                 hi -= 1
>             elif s < 0:
>                 lo += 1
>             else:
>                 hi -= 1
>     return result
> ```

> [!success] Complexity
> O(n²) time, O(1) extra space (output excluded).

> [!tip] Alternatives
> HashSet for the inner search — same O(n²) but O(n) space; sorting + two-pointer is cache-friendlier.

---

### 4Sum (LC 18) `⚡ T1`

> [!example] Problem
> Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that:
> You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,0,-1,0,-2,2], target = 0
> Output: [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,2,2,2,2], target = 8
> Output: [[2,2,2,2]]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 200
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9

> [!info] Approach
> Fix two anchors, run two-pointer for the remaining pair. O(n³) total. Double outer loop (indices `i`, `j`), two-pointer inner loop `[j+1, n-1]`. Deduplicate both outer anchors separately. Same skip-duplicate pattern as 3Sum on inner pointers.

> [!note]- Python Solution
> ```python
> def four_sum(nums, target):
>     nums.sort()
>     n = len(nums)
>     result = []
>     for i in range(n - 3):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         for j in range(i + 1, n - 2):
>             if j > i + 1 and nums[j] == nums[j - 1]:
>                 continue
>             lo, hi = j + 1, n - 1
>             while lo < hi:
>                 s = nums[i] + nums[j] + nums[lo] + nums[hi]
>                 if s == target:
>                     result.append([nums[i], nums[j], nums[lo], nums[hi]])
>                     while lo < hi and nums[lo] == nums[lo + 1]: lo += 1
>                     while lo < hi and nums[hi] == nums[hi - 1]: hi -= 1
>                     lo += 1
>                     hi -= 1
>                 elif s < target:
>                     lo += 1
>                 else:
>                     hi -= 1
>     return result
> ```

> [!success] Complexity
> O(n³) time, O(1) extra space.

> [!tip] Alternatives
> HashMap approach — same asymptotic; k-sum generalizes recursively to O(n^(k-1)).

---

### Container With Most Water (LC 11) `⚡ T1`

> [!example] Problem
> You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
> Find two lines that together with the x-axis form a container, such that the container contains the most water.
> Return the maximum amount of water a container can store.
> Notice that you may not slant the container.
> 
> **Example 1:**
> ```
> Input: height = [1,8,6,2,5,4,8,3,7]
> Output: 49
> Explanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.
> ```
> 
> **Example 2:**
> ```
> Input: height = [1,1]
> Output: 1
> ```
> 
> **Constraints:**
> - n == height.length
> - 2 <= n <= 10^5
> - 0 <= height[i] <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** Move shorter side · **Gotcha:** Moving taller side never increases min height.

> [!failure] Tempting wrong approach
> Moving the taller pointer "to explore." Area is capped by the shorter side, so moving the taller one can never increase it — always move the shorter.

> [!info] Approach
> Volume = `min(height[lo], height[hi]) * (hi - lo)`. Moving the taller bar inward can only decrease or keep width the same while min height can only stay equal or decrease — it can never improve the result. So always move the shorter bar. Start with widest container `lo=0, hi=n-1`. Move the shorter side inward. `if height[lo] <= height[hi]: lo += 1` else `hi -= 1`. Record max at each step.

> [!note]- Python Solution
> ```python
> def max_area(height):
>     lo, hi = 0, len(height) - 1
>     best = 0
>     while lo < hi:
>         area = min(height[lo], height[hi]) * (hi - lo)
>         best = max(best, area)
>         if height[lo] <= height[hi]:
>             lo += 1   # move shorter bar
>             taller side moving can't improve
>         else:
>             hi -= 1
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> O(n²) brute force — check all pairs. No better than O(n) is known.

---

### Trapping Rain Water (LC 42) `⚡ T1`

> [!example] Problem
> Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
> 
> **Example 1:**
> ```
> Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
> Output: 6
> Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.
> ```
> 
> **Example 2:**
> ```
> Input: height = [4,2,0,3,2,5]
> Output: 9
> ```
> 
> **Constraints:**
> - n == height.length
> - 1 <= n <= 2 * 10^4
> - 0 <= height[i] <= 10^5

> [!tip] Recognize · Gotcha
> **Signal:** Advance smaller `l_max`/`r_max` side · **Gotcha:** Two-pointer O(n) O(1); differs from stack solution.

> [!failure] Tempting wrong approach
> Water per bar from adjacent neighbors (`min(h[i-1], h[i+1])`). Depth depends on the max to the left and right across the whole array, not the neighbors.

> [!info] Approach
> Water at position `i` = `min(max_left, max_right) - height[i]`. Two pointers maintain running left/right maxima without two passes. Converging pointers. Whichever side has the smaller max — that side's water is determined by its own max (the other side can only be higher). Process that side. `if left_max <= right_max: water += left_max - height[lo]; lo += 1` else process right side.

> [!note]- Python Solution
> ```python
> def trap(height):
>     lo, hi = 0, len(height) - 1
>     left_max = right_max = 0
>     water = 0
>     while lo < hi:
>         if height[lo] <= height[hi]:
>             left_max = max(left_max, height[lo])
>             water += left_max - height[lo]
>             lo += 1
>         else:
>             right_max = max(right_max, height[hi])
>             water += right_max - height[hi]
>             hi -= 1
>     return water
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Precompute prefix/suffix max arrays O(n) time + O(n) space; monotonic stack O(n) time + O(n) space — both more complex than two-pointer.

---

## Same Direction (Fast/Slow)

> [!info] Approach
> A `read` pointer scans every element; a `write` pointer only advances when the current element should be kept. The gap between them encodes how many elements have been removed. Both move left-to-right, giving O(n) total.

---

### Remove Duplicates from Sorted Array (LC 26) `⚡ T1`

> [!example] Problem
> Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same. Then return the number of unique elements in nums.
> Consider the number of unique elements of nums to be k, to get accepted, you need to do the following things:
> Custom Judge:
> The judge will test your solution with the following code:
> If all assertions pass, then your solution will be accepted.
> 
> **Example 1:**
> ```
> int[] nums = [...]; // Input array
> int[] expectedNums = [...]; // The expected answer with correct length
> 
> int k = removeDuplicates(nums); // Calls your implementation
> 
> assert k == expectedNums.length;
> for (int i = 0; i < k; i++) {
>     assert nums[i] == expectedNums[i];
> }
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,1,2]
> Output: 2, nums = [1,2,_]
> Explanation: Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,0,1,1,1,2,2,3,3,4]
> Output: 5, nums = [0,1,2,3,4,_,_,_,_,_]
> Explanation: Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
> It does not matter what you leave beyond the returned k (hence they are underscores).
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -100 <= nums[i] <= 100
> - nums is sorted in non-decreasing order.

> [!tip] Recognize · Gotcha
> **Signal:** `write` only on new value · **Gotcha:** Return `write+1` as new length.

> [!info] Approach
> Array is sorted — duplicates are contiguous. A write pointer marks the last accepted position. `write = 1` (index 0 always kept). For each `read >= 1`, copy to `write` only if `nums[read] != nums[read-1]`. Each non-duplicate advances `write`. Duplicates are simply skipped.

> [!note]- Python Solution
> ```python
> def remove_duplicates(nums):
>     if not nums:
>         return 0
>     write = 1
>     for read in range(1, len(nums)):
>         if nums[read] != nums[read - 1]:
>             nums[write] = nums[read]
>             write += 1
>     return write
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Python `list(dict.fromkeys(nums))` — not in-place; interviewer expects in-place two-pointer.

---

### Move Zeroes (LC 283) `⚡ T1`

> [!example] Problem
> Given an integer array nums, move all 0's to the end of it while maintaining the relative order of the non-zero elements.
> Note that you must do this in-place without making a copy of the array.
> 
> **Example 1:**
> ```
> Input: nums = [0,1,0,3,12]
> Output: [1,3,12,0,0]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0]
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -2^{31} <= nums[i] <= 2^{31} - 1

> [!info] Approach
> Two-step: compact non-zeros forward (remove-element pattern), then fill tail with zeros. `write` pointer collects non-zeros. After loop, fill `nums[write:]` with zeros. Avoids unnecessary writes for zeros — write pointer skips over zero positions and fills at the end.

> [!note]- Python Solution
> ```python
> def move_zeroes(nums):
>     write = 0
>     for read in range(len(nums)):
>         if nums[read] != 0:
>             nums[write] = nums[read]
>             write += 1
>     for i in range(write, len(nums)):
>         nums[i] = 0
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Swap `nums[write]` and `nums[read]` when `nums[read] != 0` — single pass but does redundant swaps of 0s.

---

### Minimum Operations to Reduce X to Zero (LC 1658) `⚡ T1`

> [!example] Problem
> You are given an integer array nums and an integer x. In one operation, you can either remove the leftmost or the rightmost element from the array nums and subtract its value from x. Note that this modifies the array for future operations.
> Return the minimum number of operations to reduce x to exactly 0 if it is possible, otherwise, return -1.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,4,2,3], x = 5
> Output: 2
> Explanation: The optimal solution is to remove the last two elements to reduce x to zero.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5,6,7,8,9], x = 4
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,2,20,1,1,3], x = 10
> Output: 5
> Explanation: The optimal solution is to remove the last three elements and the first two elements (5 operations in total) to reduce x to zero.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - 1 <= nums[i] <= 10^4
> - 1 <= x <= 10^9

> [!info] Approach
> Removing from both ends to sum to `x` is equivalent to finding the longest subarray in the middle with sum = `total - x`. This is a sliding window on the middle subarray. Find the maximum-length subarray with sum = `total - x`. The answer is `n - max_length`. Two-pointer (sliding window): expand right to grow the window, shrink left when the window sum exceeds `target`. Track the maximum window length where sum equals `target`.

> [!note]- Python Solution
> ```python
> def min_operations(nums, x):
>     target = sum(nums) - x
>     if target < 0:
>         return -1
>     if target == 0:
>         return len(nums)
>     n = len(nums)
>     left = 0
>     current_sum = 0
>     max_len = -1
>     for right in range(n):
>         current_sum += nums[right]
>         while current_sum > target and left <= right:
>             current_sum -= nums[left]
>             left += 1
>         if current_sum == target:
>             max_len = max(max_len, right - left + 1)
>     if max_len == -1:
>         return -1
>     return n - max_len
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Prefix sum + hash map: store prefix sums, search for `prefix[i] == total - x - suffix_sum`. O(n) time but O(n) space.
> - Key insight: the "remove from both ends" framing is a classic redirect — always ask if the complement (middle subarray) is easier.

**Also try:**

- **Remove Element (LC 27)** — Need to compact array without extra space
- **Squares of a Sorted Array (LC 977)** — Squares of negatives can be large

---

## Partition / Dutch National Flag

---

### Sort Colors (LC 75) `⚡ T1`

> [!example] Problem
> Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.
> We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.
> You must solve this problem without using the library's sort function.
> 
> **Example 1:**
> ```
> Input: nums = [2,0,2,1,1,0]
> Output: [0,0,1,1,2,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,0,1]
> Output: [0,1,2]
> ```
> 
> **Constraints:**
> - n == nums.length
> - 1 <= n <= 300
> - nums[i] is either 0, 1, or 2.

> [!tip] Recognize · Gotcha
> **Signal:** Three pointers lo/mid/hi · **Gotcha:** Swap mid with hi then mid++ only if not 2.

> [!failure] Tempting wrong approach
> Advancing `i` after swapping with `hi`. The value swapped in from the right is unexamined — advance `i` only on the `lo` swap or on a 1.

> [!info] Approach
> Standard sort is O(n log n). Three distinct values allow O(n) single-pass partitioning. Three pointers: `lo` (next 0 position), `mid` (current element), `hi` (next 2 position from right). Process `nums[mid]`: if 0 → swap with `lo`, advance both `lo` and `mid`; if 1 → advance `mid` only; if 2 → swap with `hi`, decrement `hi` but do NOT advance `mid` (swapped element is unseen).

> [!note]- Python Solution
> ```python
> def sort_colors(nums):
>     lo, mid, hi = 0, 0, len(nums) - 1
>     while mid <= hi:
>         if nums[mid] == 0:
>             nums[lo], nums[mid] = nums[mid], nums[lo]
>             lo += 1
>             mid += 1
>         elif nums[mid] == 1:
>             mid += 1
>         else:  # nums[mid] == 2
>             nums[mid], nums[hi] = nums[hi], nums[mid]
>             hi -= 1
>             # do NOT increment mid: swapped element from hi is unseen
> ```

> [!success] Complexity
> O(n) time, O(1) space. Single pass.

> [!tip] Alternatives
> Count occurrences then overwrite — two passes, also O(n); DNF is strictly single-pass. Standard sort O(n log n) — overkill.

---

## Linked List Two Pointers

> [!info] Approach
> Linked lists lack random access. Two pointers with different speeds (fast/slow) or different start offsets simulate the "looking ahead" that indices would provide in arrays.

---

### Linked List Cycle (LC 141) `🎯 T2`

> Full walkthrough: [Linked List Cycle](../data-structures/07-linked-list.md#linked-list-cycle--t2).

---

### Remove Nth Node From End of List (LC 19) `🎯 T2`

> Full walkthrough: [Remove Nth Node From End of List](../data-structures/07-linked-list.md#remove-nth-node-from-end-of-list--t2).

**Also try:**

- **Find Duplicate Number — Floyd's (LC 287)** — see [Find the Duplicate Number](../data-structures/01-array.md#find-the-duplicate-number--t2)
- **Middle of the Linked List (LC 876)** — see [Middle of the Linked List](../data-structures/07-linked-list.md#fast--slow-pointers)

---

## Palindrome Two Pointers

---

### 3Sum Closest (LC 16) `⚡ T1`

> [!example] Problem
> Given an integer array nums of length n and an integer target, find three integers in nums such that the sum is closest to target.
> Return the sum of the three integers.
> You may assume that each input would have exactly one solution.
> 
> **Example 1:**
> ```
> Input: nums = [-1,2,1,-4], target = 1
> Output: 2
> Explanation: The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,0], target = 1
> Output: 0
> Explanation: The sum that is closest to the target is 0. (0 + 0 + 0 = 0).
> ```
> 
> **Constraints:**
> - 3 <= nums.length <= 500
> - -1000 <= nums[i] <= 1000
> - -10^4 <= target <= 10^4

> [!info] Approach
> Same scaffold as 3Sum — fix anchor, converging two-pointer on remainder. Track closest sum instead of exact match. Sort array. For each anchor `i`, run `lo = i+1, hi = n-1`. Update best if `|s - target| < |best - target|`. Move pointer based on whether sum is too small or too large. If `s < target` → `lo += 1` (need larger sum); if `s > target` → `hi -= 1`; if equal → return immediately.

> [!note]- Python Solution
> ```python
> def three_sum_closest(nums, target):
>     nums.sort()
>     best = float('inf')
>     for i in range(len(nums) - 2):
>         lo, hi = i + 1, len(nums) - 1
>         while lo < hi:
>             s = nums[i] + nums[lo] + nums[hi]
>             if abs(s - target) < abs(best - target):
>                 best = s
>             if s < target:
>                 lo += 1
>             elif s > target:
>                 hi -= 1
>             else:
>                 return s   # exact match
>     return best
> ```

> [!success] Complexity
> O(n²) time, O(1) extra space.

> [!tip] Alternatives
> Brute force O(n³) — no benefit; three nested loops. Sorting + two-pointer is optimal.

---

## Hash Map Two-Sum Variant

**Also try:**

- **Partition Array According to Given Pivot (LC 2161)** — Relative order must be preserved, so an in-place swap (DNF-style) would break ordering
- **Minimum Difference Between Highest and Lowest of K Scores (LC 1984)** — After sorting, the k elements with minimum spread must be contiguous (any non-contiguous selection can be improved by replacing the outlier …

---

## Sorted Array / Two-Pointer Greedy

**Also try:**

- **Number of Subsequences That Satisfy the Given Sum Condition (LC 1498)** — After sorting, for a fixed minimum at index `lo`, find the furthest `hi` where `nums[lo] + nums[hi] <= target`
- **Max Number of K-Sum Pairs (LC 1679)** — Each operation removes a pair summing to k
- **Bag of Tokens (LC 948)** — To maximize points, spend power on the cheapest token (face-up) and spend points on the most expensive token to regain power (face-down)
- **Boats to Save People (LC 881)** — Greedy: pair the heaviest person with the lightest person if their combined weight fits

---

## Two-Pointer on Strings

**Also try:**

- **Reverse String (LC 344)** — Swapping from both ends converges in n/2 steps — the simplest two-pointer pattern
- **Long Pressed Name (LC 925)** — Both strings share a subsequence structure — `name` characters must appear in `typed` in order, with possible repetitions in `typed`
- **Reverse Vowels of a String** — The vowels to swap form a sparse subset, so moving two pointers inward and skipping non-vowels is optimal

---

## See Also

[[binary-search]] | [[sliding-window]] | [[array]] | [[linked-list]]
[[binary-search]] | [[sorting]] | [[sliding-window]] | [[array]]
