---
tags: [coding, data-structures, hashing]
topic: hashing
difficulty: mixed
---
# Hashing Problems

## What this covers

> [!abstract] In this file
> **Covers:** Worked hashing problems: complement map, frequency map, set operations, design, rolling hash.
> **You'll be able to:** Reach for a map/set reflexively and pick the right key.
> **Prereqs:** Hashing lecture · **Pair with:** [Hashing lecture](../../02-data-structures/02-hashing.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Complement Map](#complement-map) · [Prefix Sum + Map](#prefix-sum--map) · [Frequency Map](#frequency-map) · [Design](#design) · [Set Operations](#set-operations) · [Rolling Hash / Dedup](#rolling-hash--dedup)

> [!tip] If you only have 20 minutes
> **Do these first:** [Two Sum](#two-sum--t1) · [Subarray Sum Equals K](#subarray-sum-equals-k--t1) · [Contiguous Array](#contiguous-array-lc-525--t1) · [Subarray Sums Divisible by K](#subarray-sums-divisible-by-k--t1) · [Top K Frequent Elements](#top-k-frequent-elements--t1) · [Longest Consecutive Sequence](#longest-consecutive-sequence--t1) · [Insert Delete GetRandom O(1)](#insert-delete-getrandom-o1--t1)
> **Template:** Prefix-sum count: `cnt = {0: 1}; for x in a: s += x; ans += cnt.get(s - k, 0); cnt[s] = cnt.get(s, 0) + 1`.
> **Template:** Check-then-insert (Two Sum) to avoid pairing an element with itself.
> **Gotchas:** Seed `{0: 1}` (or `{0: -1}` for longest length) · Python `%` is non-negative; other languages need `((s % k) + k) % k` · Longest Consecutive: only start counting from `x` where `x-1` not in set · Top K: bucket sort beats heap.

---

## Complement Map

---

### Two Sum `⚡ T1`

> [!example] Problem
> Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
> You may assume that each input would have exactly one solution, and you may not use the same element twice.
> You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [2,7,11,15], target = 9
> Output: [0,1]
> Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [3,2,4], target = 6
> Output: [1,2]
> ```
> 
> **Example 3:**
> ```
> Input: nums = [3,3], target = 6
> Output: [0,1]
> ```
> 
> **Constraints:**
> - 2 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9
> - -10^9 <= target <= 10^9
> - Only one valid answer exists.

> [!tip] Recognize · Gotcha
> **Signal:** "Pair summing to target" · **Gotcha:** Return **indices** vs values — clarify with interviewer.

> [!failure] Tempting wrong approach
> Sort + two pointers — loses the original indices. Store `value → index` and check the complement *before* inserting (handles `[3,3]`).

> [!info] Approach
> Brute force checks every pair — O(n²). We need to answer "have I seen the complement of this number?" in O(1). A hash map from value to index. For each `x`, check if `target - x` is already stored. Single pass. Before storing `x`, look up `target - x`. If found, return `[seen[complement], i]`. Store `x → i` after checking to avoid using the same index twice.

> [!note]- Python Solution
> ```python
> def two_sum(nums, target):
>     seen = {}
>     for i, x in enumerate(nums):
>         complement = target - x
>         if complement in seen:
>             return [seen[complement], i]
>         seen[x] = i
>     return []
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Sort + two pointers — O(n log n) and destroys original indices. Only valid if indices don't matter.

---

### 3Sum (hash-based) `⚡ T1`

> [!example] Problem
> Same problem as [3Sum (LC 15)](../algorithms/02-two-pointers.md#3sum-lc-15--t1) — this section covers the alternative approach only.

> [!info] Approach
> Reduce to two-sum: fix element `a`, find pair `(b, c)` with `b + c = -a` in the remaining array. Sort first to handle duplicates. For each index `i`, use a set to find complements in `nums[i+1:]`. Sort. Skip duplicate values of `a`. For the inner scan, use a seen set: if `target - b` in seen, record triplet; else add `b` to seen.

> [!note]- Python Solution
> ```python
> def three_sum(nums):
>     nums.sort()
>     result = []
>     seen_triplets = set()
>     for i in range(len(nums) - 2):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         target = -nums[i]
>         seen = set()
>         j = i + 1
>         while j < len(nums):
>             complement = target - nums[j]
>             if complement in seen:
>                 triplet = (nums[i], complement, nums[j])
>                 if triplet not in seen_triplets:
>                     seen_triplets.add(triplet)
>                     result.append(list(triplet))
>                 while j + 1 < len(nums) and nums[j] == nums[j + 1]:
>                     j += 1
>             seen.add(nums[j])
>             j += 1
>     return result
> ```

> [!success] Complexity
> Time O(n²); Space O(n) for the seen set.

> [!tip] Alternatives
> Two-pointer after sort — same O(n²) time, O(1) extra space. Cleaner and preferred in interviews.

---

### 4Sum (hash-based) `⚡ T1`

> [!example] Problem
> Same problem as [4Sum (LC 18)](../algorithms/02-two-pointers.md#4sum-lc-18--t1) — this section covers the alternative approach only.

> [!info] Approach
> Reduce to 3Sum by fixing one element. Reduce 3Sum to 2Sum by fixing another. Sort + two outer loops (skip duplicates) + hash set inner two-sum. Fix `nums[i]` and `nums[j]`. Inner target is `target - nums[i] - nums[j]`. Use seen set for two-sum on remaining elements.

> [!note]- Python Solution
> ```python
> def four_sum(nums, target):
>     nums.sort()
>     result = []
>     seen_quads = set()
>     n = len(nums)
>     for i in range(n - 3):
>         if i > 0 and nums[i] == nums[i - 1]:
>             continue
>         for j in range(i + 1, n - 2):
>             if j > i + 1 and nums[j] == nums[j - 1]:
>                 continue
>             need = target - nums[i] - nums[j]
>             seen = set()
>             k = j + 1
>             while k < n:
>                 if need - nums[k] in seen:
>                     quad = (nums[i], nums[j], need - nums[k], nums[k])
>                     if quad not in seen_quads:
>                         seen_quads.add(quad)
>                         result.append(list(quad))
>                     while k + 1 < n and nums[k] == nums[k + 1]:
>                         k += 1
>                 seen.add(nums[k])
>                 k += 1
>     return result
> ```

> [!success] Complexity
> Time O(n³); Space O(n).

> [!tip] Alternatives
> Four-pointer two-pointer approach O(n³) O(1) space. For exactly 4 arrays (4Sum II), hash all A+B sums then count complementary C+D — O(n²) time and space.

---

### 4Sum II `⚡ T1`

> [!example] Problem
> Given four integer arrays nums1, nums2, nums3, and nums4 all of length n, return the number of tuples (i, j, k, l) such that
> 
> **Example 1:**
> ```
> Input: nums1 = [1,2], nums2 = [-2,-1], nums3 = [-1,2], nums4 = [0,2]
> Output: 2
> Explanation:
> The two tuples are:
> 1. (0, 0, 0, 1) -> nums1[0] + nums2[0] + nums3[0] + nums4[1] = 1 + (-2) + (-1) + 2 = 0
> 2. (1, 1, 0, 0) -> nums1[1] + nums2[1] + nums3[0] + nums4[0] = 2 + (-1) + (-1) + 0 = 0
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [0], nums2 = [0], nums3 = [0], nums4 = [0]
> Output: 1
> ```
> 
> **Constraints:**
> - n == nums1.length
> - n == nums2.length
> - n == nums3.length
> - n == nums4.length
> - 1 <= n <= 200
> - -228 <= nums1[i], nums2[i], nums3[i], nums4[i] <= 228

> [!info] Approach
> Brute force O(n⁴). Split into two pairs: count all `A[i] + B[j]` sums, then for each `C[k] + D[l]` check if its negation was seen. Hash map `ab_sum → count`. Then iterate all C, D pairs and look up `-(C[k] + D[l])`. Two nested loops for AB → Counter. Two nested loops for CD → look up complement. Sum all matching counts.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def four_sum_count(nums1: list[int], nums2: list[int],
>                    nums3: list[int], nums4: list[int]) -> int:
>     ab = defaultdict(int)
>     for a in nums1:
>         for b in nums2:
>             ab[a + b] += 1
>     count = 0
>     for c in nums3:
>         for d in nums4:
>             count += ab[-(c + d)]
>     return count
> ```

> [!success] Complexity
> Time O(n²); Space O(n²).

> [!tip] Alternatives
> Meet-in-the-middle generalizes: split k arrays into two halves of k/2, hash one half's sums, probe with the other. Always yields O(n^(k/2)) for k-sum variants.

**Also try:**

- **Max Number of K-Sum Pairs** — see [Max Number of K-Sum Pairs (LC 1679)](../algorithms/02-two-pointers.md#sorted-array--two-pointer-greedy)

---

## Prefix Sum + Map

---

### Contiguous Array (LC 525) `⚡ T1`

> [!example] Problem
> Given a binary array nums, return the maximum length of a contiguous subarray with an equal number of 0 and 1.
> 
> **Example 1:**
> ```
> Input: nums = [0,1]
> Output: 2
> Explanation: [0, 1] is the longest contiguous subarray with an equal number of 0 and 1.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0]
> Output: 2
> Explanation: [0, 1] (or [1, 0]) is a longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [0,1,1,1,1,1,0,0,0]
> Output: 6
> Explanation: [1,1,1,0,0,0] is the longest contiguous subarray with equal number of 0 and 1.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.

> [!failure] Tempting wrong approach
> Sliding window on 0/1 counts — there's no monotone shrink condition. Map 0 → −1 and find the longest zero-sum subarray via first-seen prefix index.

> [!info] Approach
> Map 0 → -1. Now "equal 0s and 1s" means "subarray sum = 0". A subarray `[i+1..j]` sums to zero iff `prefix[j] == prefix[i]`. We want the maximum `j - i` among equal prefix sums. Hash map of `prefix_sum -> first_index`. When a prefix sum repeats, the distance gives a candidate max length. Initialize `{0: -1}`. For each index `i`, update `prefix`. If `prefix` is in the map, update `max_len = max(max_len, i - first_seen[prefix])`. Otherwise record `first_seen[prefix] = i`.

> [!note]- Python Solution
> ```python
> def find_max_length(nums):
>     first_seen = {0: -1}
>     prefix = 0
>     max_len = 0
>     for i, num in enumerate(nums):
>         prefix += 1 if num == 1 else -1
>         if prefix in first_seen:
>             max_len = max(max_len, i - first_seen[prefix])
>         else:
>             first_seen[prefix] = i
>     return max_len
> ```

> [!success] Complexity
> Time O(n), Space O(n).

> [!tip] Alternatives
> - Brute force O(n²): enumerate all subarrays, count 0s and 1s.
> - Key insight: store only the *first* occurrence of each prefix sum to maximise the gap.

---

### Subarray Sum Equals K `⚡ T1`

> [!example] Problem
> Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k.
> A subarray is a contiguous non-empty sequence of elements within an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1], k = 2
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3], k = 3
> Output: 2
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - -1000 <= nums[i] <= 1000
> - -10^7 <= k <= 10^7

> [!tip] Recognize · Gotcha
> **Signal:** Prefix sum + frequency · **Gotcha:** **Prefix 0** means subarray from start. **Negative numbers** → prefix sum still works; no sliding window for “exactly K” with negatives.

> [!failure] Tempting wrong approach
> Sliding window — invalid with negatives because the sum isn't monotone in window size. Use prefix sums + a count map seeded with `{0: 1}`.

> [!info] Approach
> Sliding window fails with negatives (sum can decrease when adding elements). Need a different invariant. prefix[j] - prefix[i] = k implies prefix[i] = prefix[j] - k. Count how many times each prefix sum has appeared. Maintain running prefix sum. Before updating the map, check `seen[prefix - k]`. Initialize `seen = {0: 1}` to handle subarrays starting at index 0.

> [!note]- Python Solution
> ```python
> def subarray_sum(nums, k):
>     count = 0
>     prefix = 0
>     seen = {0: 1}
>     for x in nums:
>         prefix += x
>         count += seen.get(prefix - k, 0)
>         seen[prefix] = seen.get(prefix, 0) + 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> O(n²) prefix sum array with nested loop — correct but slow. Sliding window — only works for positive numbers.

---

### Subarray Sums Divisible by K `⚡ T1`

> [!example] Problem
> Given an integer array nums and an integer k, return the number of non-empty subarrays that have a sum divisible by k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [4,5,0,-2,-3,1], k = 5
> Output: 7
> Explanation: There are 7 subarrays with a sum divisible by k = 5:
> [4, 5, 0, -2, -3, 1], [5], [5, 0], [5, 0, -2, -3], [0], [0, -2, -3], [-2, -3]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [5], k = 9
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 3 * 10^4
> - -10^4 <= nums[i] <= 10^4
> - 2 <= k <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** "Count subarrays whose sum is divisible by K" · **Gotcha:** Python modulo is always positive; Java/C++ can be negative. Normalize: `(pref % k + k) % k`. `seen[0]=1` for subarray from index 0.

> [!info] Approach
> `(prefix[j] - prefix[i]) % K == 0` iff `prefix[j] % K == prefix[i] % K`. Count pairs of equal remainders. Frequency map of prefix sums mod K. Each pair of indices with equal remainder contributes one valid subarray. `seen = {0: 1}`. For each element, compute `prefix % K` (handle negatives: `% K` in Python already returns non-negative). Add `seen[(prefix % K)]` to count. Increment map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> >
> def subarrays_div_by_k(nums, k):
>     count = 0
>     prefix = 0
>     seen = defaultdict(int)
>     seen[0] = 1
>     for x in nums:
>         prefix = (prefix + x) % k
>         count += seen[prefix]
>         seen[prefix] += 1
>     return count
> ```

> [!success] Complexity
> Time O(n); Space O(k) — at most k distinct remainders.

> [!tip] Alternatives
> Prefix array + O(n²) nested loop — correct, slow. This is optimal.

**Also try:**

- **Longest Subarray with Sum K** — Sliding window fails with negatives
- **Count Number of Nice Subarrays** — see [Count Number of Nice Subarrays (LC 1248)](../algorithms/03-sliding-window.md#variable-window--exactly-k)
- **Make the Array Sum Divisible by P** — We want `(total - subarray_sum) % P == 0`, i.e., `subarray_sum % P == total % P`

---

## Frequency Map

---

### Top K Frequent Elements `⚡ T1`

> [!example] Problem
> Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,2,2,3], k = 2
> Output: [1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1], k = 1
> Output: [1]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - -10^4 <= nums[i] <= 10^4
> - k is in the range [1, the number of unique elements in the array].
> - It is guaranteed that the answer is unique.

> [!tip] Recognize · Gotcha
> **Signal:** Bucket vs heap · **Gotcha:** **Heap** is O(n log k); **bucket sort** can be O(n) if frequencies bounded.

> [!failure] Tempting wrong approach
> Sorting by frequency — O(n log n). Use a size-k min-heap (O(n log k)) or bucket sort by count (O(n)).

> [!info] Approach
> Sorting by frequency is O(n log n). Bucket sort on frequency gives O(n). Count frequencies, then place each number into a bucket indexed by its frequency. Collect from the highest-frequency buckets downward. `Counter` → buckets list of size `n+1` where `buckets[f]` holds all numbers with frequency `f`. Iterate from index `n` down and collect until we have `k` elements.

> [!note]- Python Solution
> ```python
> from collections import Counter
> >
> def top_k_frequent(nums, k):
>     freq = Counter(nums)
>     buckets = [[] for _ in range(len(nums) + 1)]
>     for num, count in freq.items():
>         buckets[count].append(num)
>     result = []
>     for i in range(len(buckets) - 1, 0, -1):
>         for num in buckets[i]:
>             result.append(num)
>             if len(result) == k:
>                 return result
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> `heapq.nlargest(k, freq, key=freq.get)` — O(n log k), clean one-liner but not O(n). QuickSelect on frequencies — O(n) average, O(n²) worst.

**Also try:**

- **First Unique Character in a String** — Need both frequency (to identify unique) and order (to find the first)
- **Ransom Note** — This is a frequency matching problem; each character in the note must be available at least as many times as needed
- **Subdomain Visit Count** — Each domain contributes its count to itself and all suffix domains
- **Sort Characters by Frequency** — Need characters ordered by count descending
- **Substring with Concatenation of All Words** — Words are fixed length
- **Max Points on a Line** — For each pair of points, their line is defined by slope

---

## Design

---

### Insert Delete GetRandom O(1) `⚡ T1`

> Full walkthrough: [Insert Delete GetRandom O(1)](12-design.md#insert-delete-getrandom-o1--t1).

---

### Design HashMap `⚡ T1`

> [!example] Problem
> Design a HashMap without using any built-in hash table libraries.
> Implement the MyHashMap class
> 
> **Example 1:**
> ```
> Input
> ["MyHashMap", "put", "put", "get", "get", "put", "get", "remove", "get"]
> [[], [1, 1], [2, 2], [1], [3], [2, 1], [2], [2], [2]]
> Output
> [null, null, null, 1, -1, null, 1, null, -1]
> 
> Explanation
> MyHashMap myHashMap = new MyHashMap();
> myHashMap.put(1, 1); // The map is now [[1,1]]
> myHashMap.put(2, 2); // The map is now [[1,1], [2,2]]
> myHashMap.get(1);    // return 1, The map is now [[1,1], [2,2]]
> myHashMap.get(3);    // return -1 (i.e., not found), The map is now [[1,1], [2,2]]
> myHashMap.put(2, 1); // The map is now [[1,1], [2,1]] (i.e., update the existing value)
> myHashMap.get(2);    // return 1, The map is now [[1,1], [2,1]]
> myHashMap.remove(2); // remove the mapping for 2, The map is now [[1,1]]
> myHashMap.get(2);    // return -1 (i.e., not found), The map is now [[1,1]]
> ```
> 
> **Constraints:**
> - 0 <= key, value <= 10^6
> - At most 10^4 calls will be made to put, get, and remove.

> [!info] Approach
> Understand collision resolution. Chaining: each bucket holds a list of `(key, value)` pairs. Array of `capacity` buckets. Hash function: `key % capacity` with prime capacity to reduce clustering. `put` scans bucket for existing key (update) or appends. `get` scans for key, returns -1 if absent. `remove` filters out the key.

> [!note]- Python Solution
> ```python
> class MyHashMap:
>     def __init__(self, capacity=1009):  # prime capacity
>         self._cap = capacity
>         self._buckets: list[list[tuple[int, int]]] = [[] for _ in range(capacity)]
> >
>     def _idx(self, key):
>         return key % self._cap
> >
>     def put(self, key, value):
>         bucket = self._buckets[self._idx(key)]
>         for i, (k, _) in enumerate(bucket):
>             if k == key:
>                 bucket[i] = (key, value)
>                 return
>         bucket.append((key, value))
> >
>     def get(self, key):
>         for k, v in self._buckets[self._idx(key)]:
>             if k == key:
>                 return v
>         return -1
> >
>     def remove(self, key):
>         idx = self._idx(key)
>         self._buckets[idx] = [(k, v) for k, v in self._buckets[idx] if k != key]
> ```

> [!success] Complexity
> Time O(1) average, O(n) worst (all keys collide); Space O(n + capacity).

> [!tip] Alternatives
> Open addressing (linear probing) — better cache locality, needs tombstones for delete. Robin Hood hashing — minimizes max probe length.

---

## Set Operations

---

### Two Sum Less Than K `⚡ T1`

> [!example] Problem
> Given an array `nums` of integers and integer `k`, return the maximum `sum` such that there exists `i < j` with `nums[i] + nums[j] = sum` and `sum < k`. If no `i`, `j` exist satisfying this equation, return `-1`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** nums = [34,23,1,24,75,33,54,8], k = 60
> **Output:** 58
> **Explanation: **We can use 34 and 24 to sum 58 which is less than 60.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** nums = [10,20,30], k = 15
> **Output:** -1
> **Explanation: **In this case it is not possible to get a pair sum less that 15.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= nums.length <= 100`
> 	
> - `1 <= nums[i] <= 1000`
> 	
> - `1 <= k <= 2000`

> [!info] Approach
> We want the largest valid pair sum — greedy with two pointers after sorting is cleanest. Hash set alternative: for each `x`, check if any value in `[k - x - (n-1)..k - x - 1]` is present. Sort. Use two pointers. If `nums[l] + nums[r] < k`, record sum and advance `l`. Else shrink `r`. After sort, `l = 0`, `r = n - 1`. Converge inward. Track `best = max(best, sum)` when `sum < k`.

> [!note]- Python Solution
> ```python
> def two_sum_less_than_k(nums, k):
>     nums.sort()
>     l, r = 0, len(nums) - 1
>     best = -1
>     while l < r:
>         s = nums[l] + nums[r]
>         if s < k:
>             best = max(best, s)
>             l += 1
>         else:
>             r -= 1
>     return best
> ```

> [!success] Complexity
> Time O(n log n); Space O(1).

> [!tip] Alternatives
> Hash set per element: O(n * k) worst case — avoid. Counting sort if values are bounded (e.g., 1–1000): O(max_val) space.

---

### Longest Consecutive Sequence `⚡ T1`

> [!example] Problem
> Given an unsorted array of integers nums, return the length of the longest consecutive elements sequence.
> You must write an algorithm that runs in O(n) time.
> 
> **Example 1:**
> ```
> Input: nums = [100,4,200,1,3,2]
> Output: 4
> Explanation: The longest consecutive elements sequence is [1, 2, 3, 4]. Therefore its length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,3,7,2,5,8,4,6,0,1]
> Output: 9
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,0,1,2]
> Output: 3
> ```
> 
> **Constraints:**
> - 0 <= nums.length <= 10^5
> - -10^9 <= nums[i] <= 10^9

> [!tip] Recognize · Gotcha
> **Signal:** O(n) expected, not sort · **Gotcha:** **O(n)** only if you don’t sort; **inner while** looks O(n²) but each number visited once across all sequences.

> [!failure] Tempting wrong approach
> Sorting (O(n log n) breaks the O(n) ask), or walking from every element (O(n²)). Only start a walk where `x - 1` is absent.

> [!info] Approach
> Sorting is O(n log n). We need O(n). Hash set enables O(1) membership checks. Only start counting a sequence from `x` if `x - 1` is NOT in the set. This prevents redundant work — each element is visited at most twice total. Build set. For each `x`, if `x - 1 not in set`, extend the chain `x, x+1, x+2, ...` while each successor is in the set.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums):
>     num_set = set(nums)
>     best = 0
>     for x in num_set:
>         if x - 1 not in num_set:  # only start from sequence heads
>             length = 1
>             while x + length in num_set:
>                 length += 1
>             best = max(best, length)
>     return best
> ```

> [!success] Complexity
> Time O(n) — each element processed at most twice; Space O(n).

> [!tip] Alternatives
> Sort + scan — O(n log n), simpler but doesn't meet the O(n) constraint. Union-Find — O(n α(n)), correct but overkill.

---

### Valid Sudoku (LC 36) `🎯 T2`

> [!example] Problem
> Determine whether a partially filled 9x9 Sudoku board is valid: each row, each column and each of the nine 3x3 boxes must contain the digits 1-9 at most once. Empty cells are `'.'`. Only the filled cells are checked; the board need not be solvable.
>
> **Example 1:** the standard sample board (first row `53..7....`) returns `true`.
>
> **Example 2:** the same board with the first cell changed from `5` to `8` returns `false` (two 8s in the top-left box).

> [!tip] Recognize · Gotcha
> **Signal:** "no duplicates in rows / columns / blocks" · **Gotcha:** box index is `(r // 3) * 3 + c // 3`; do not compare against solvability, and skip `'.'`.

> [!info] Approach
> One pass with 27 sets: 9 rows, 9 columns, 9 boxes. For each filled cell, if its digit is already in its row, column or box set, return false; otherwise add it to all three. Trade-off: sets cost more memory than 9-bit bitmasks (`mask & bit`), which is the micro-optimization if asked, but sets are clearer.

> [!note]- Python Solution
> ```python
> def is_valid_sudoku(board):
>     rows = [set() for _ in range(9)]
>     cols = [set() for _ in range(9)]
>     boxes = [set() for _ in range(9)]
>     for r in range(9):
>         for c in range(9):
>             ch = board[r][c]
>             if ch == '.':
>                 continue
>             b = (r // 3) * 3 + c // 3
>             if ch in rows[r] or ch in cols[c] or ch in boxes[b]:
>                 return False
>             rows[r].add(ch); cols[c].add(ch); boxes[b].add(ch)
>     return True
> ```

> [!success] Complexity
> Time O(81) = O(1) (O(n^2) for an n x n board); Space O(1).

> [!tip] Follow-up
> Use a single set of strings like `"5 in row 0"`, `"5 in col 1"`, `"5 in box 0"` for a compact one-set variant. Sudoku Solver (backtracking) reuses these exact structures to prune.

**Also try:**

- **Contains Duplicate** — Membership check in O(1) is exactly what a hash set provides
- **Intersection of Two Arrays** — Set intersection directly models the problem

---

## Rolling Hash / Dedup

---

### Longest Duplicate Substring (Rabin-Karp) `⚡ T1`

> Full walkthrough: [Longest Duplicate Substring](../algorithms/12-string-algorithms.md#longest-duplicate-substring--t1).

**Also try:**

- **Find Duplicate File in System** — Files with the same content are duplicates

---

## See Also

[[array]] | [[sliding-window]] | [[string]] | [[two-pointers]]
[[array]] | [[two-pointers]] | [[sliding-window]] | [[sorting]]
