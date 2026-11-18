---
tags: [coding, algorithms, dynamic-programming]
topic: Dynamic Programming
difficulty: mixed
---
# Dynamic Programming — Problem Reference by Pattern

## What this covers

> [!abstract] In this file
> **Covers:** Worked DP problems by pattern: linear, knapsack, LCS, grid, stock state machine, LIS, string DP, bitmask, interval, DP + binary search.
> **You'll be able to:** Derive state/transition for unseen DP problems and space-optimise.
> **Prereqs:** DP lecture · **Pair with:** [DP lecture](../../02-algorithms/15-dynamic-programming.md) · [Recursion → DP](../../02-algorithms/10-recursion-to-dp.md) · **Time:** 6–8 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/l3-google-roadmap.md#tier-legend))

**Sections:** [Linear DP (1-D)](#linear-dp-1-d) · [0/1 Knapsack](#01-knapsack) · [Unbounded Knapsack](#unbounded-knapsack) · [LCS Family](#lcs-family) · [Grid DP](#grid-dp) · [State Machine DP (Stock Problems)](#state-machine-dp-stock-problems) · [Longest Increasing Subsequence (LIS) Family](#longest-increasing-subsequence-lis-family) · [String DP](#string-dp) · [Bitmask DP](#bitmask-dp) · [DP on Sequences](#dp-on-sequences) · [Interval DP](#interval-dp) · [Game Theory (Minimax) DP](#game-theory-minimax-dp) · [Digit DP](#digit-dp)

> [!abstract]- Problem index (54)
> **Linear DP (1-D):** [Climbing Stairs](#climbing-stairs--t2) · [Min Cost Climbing Stairs](#min-cost-climbing-stairs--t2) · [House Robber](#house-robber--t2) · [House Robber II (Circular)](#house-robber-ii-circular--t2) · [Maximum Subarray (Kadane's — DP view)](#maximum-subarray-kadanes--dp-view--t2) · [Word Break](#word-break--t2) · [Decode Ways](#decode-ways--t2) · [Word Break II (LC 140)](#word-break-ii-lc-140--t2) · [Frog Jump (LC 403)](#frog-jump-lc-403--t2)  
> **0/1 Knapsack:** [Subset Sum Problem](#subset-sum-problem--t2) · [Partition Equal Subset Sum](#partition-equal-subset-sum--t2) · [Last Stone Weight II](#last-stone-weight-ii--t1)  
> **Unbounded Knapsack:** [Coin Change (Min Coins)](#coin-change-min-coins--t2) · [Coin Change II (Total Ways)](#coin-change-ii-total-ways--t2) · [Combination Sum IV (LC 377)](#combination-sum-iv-lc-377--t2) · [Perfect Squares](#perfect-squares--t2)  
> **LCS Family:** [Longest Common Subsequence](#longest-common-subsequence--t2) · [Edit Distance](#edit-distance--t2) · [Longest Palindromic Subsequence](#longest-palindromic-subsequence--t2) · [Minimum ASCII Delete Sum for Two Strings](#minimum-ascii-delete-sum-for-two-strings--t2) · [Minimum Window Subsequence (LC 727)](#minimum-window-subsequence-lc-727--t2)  
> **Grid DP:** [Unique Paths](#unique-paths--t1) · [Unique Paths II (With Obstacles)](#unique-paths-ii-with-obstacles--t2) · [Minimum Path Sum](#minimum-path-sum--t1) · [Maximal Square](#maximal-square--t2) · [Dungeon Game (LC 174)](#dungeon-game-lc-174--t2) · [Cherry Pickup (LC 741)](#cherry-pickup-lc-741--t3)  
> **State Machine DP (Stock Problems):** [Best Time to Buy and Sell Stock (All Variants)](#best-time-to-buy-and-sell-stock-all-variants--t2) · [Best Time to Buy and Sell Stock with Cooldown (LC 309)](#best-time-to-buy-and-sell-stock-with-cooldown-lc-309--t2) · [Stock with Transaction Fee](#stock-with-transaction-fee) · [Best Time to Buy and Sell Stock IV (LC 188)](#best-time-to-buy-and-sell-stock-iv-lc-188--t2)  
> **Longest Increasing Subsequence (LIS) Family:** [Longest Increasing Subsequence](#longest-increasing-subsequence--t1) · [Number of LIS](#number-of-lis)  
> **String DP:** [Distinct Subsequences](#distinct-subsequences--t2) · [Interleaving String](#interleaving-string--t2) · [Regular Expression Matching](#regular-expression-matching) · [Wildcard Matching (LC 44)](#wildcard-matching-lc-44--t2)  
> **Bitmask DP:** [Partition to K Equal Subset Sums](#partition-to-k-equal-subset-sums--t2) · [Smallest Sufficient Team (LC 1125)](#smallest-sufficient-team-lc-1125--t3)  
> **DP on Sequences:** [Jump Game II](#jump-game-ii--t2) · [Maximum Product Subarray](#maximum-product-subarray--t2) · [Longest Common Substring](#longest-common-substring) · [Russian Doll Envelopes (LC 354)](#russian-doll-envelopes-lc-354) · [Maximum Profit in Job Scheduling](#maximum-profit-in-job-scheduling--t2) · [Super Egg Drop (LC 887)](#super-egg-drop-lc-887--t3) · [Minimum Number of Refueling Stops (LC 871)](#minimum-number-of-refueling-stops-lc-871--t2)  
> **Interval DP:** [Matrix Chain Multiplication](#matrix-chain-multiplication) · [Burst Balloons (LC 312)](#burst-balloons-lc-312--t2) · [Minimum Cost to Cut a Stick (LC 1547)](#minimum-cost-to-cut-a-stick-lc-1547--t2) · [Strange Printer (LC 664)](#strange-printer-lc-664--t3)  
> **Game Theory (Minimax) DP:** [Predict the Winner / Stone Game (LC 486 / 877)](#predict-the-winner--stone-game-lc-486--877--t2) · [Stone Game II (LC 1140)](#stone-game-ii-lc-1140--t2)  
> **Digit DP:** [Numbers At Most N Given Digit Set (LC 902)](#numbers-at-most-n-given-digit-set-lc-902--t3) · [Count Numbers with Unique Digits (LC 357)](#count-numbers-with-unique-digits-lc-357--t2)  

> [!tip] If you only have 20 minutes
> **Do these first:** [Climbing Stairs](#climbing-stairs--t2) · [House Robber](#house-robber--t2) · [Coin Change (Min Coins)](#coin-change-min-coins--t2) · [Coin Change II (Total Ways)](#coin-change-ii-total-ways--t2) · [Partition Equal Subset Sum](#partition-equal-subset-sum--t2) · [Longest Increasing Subsequence](#longest-increasing-subsequence--t1) · [Longest Common Subsequence](#longest-common-subsequence--t2) · [Edit Distance](#edit-distance--t2) · [Unique Paths](#unique-paths--t1) · [Word Break](#word-break--t2)
> **Template:** Define `dp[i]` in one sentence → recurrence → base case → fill order → answer cell. Say all five before coding.
> **Template:** Knapsack 1-D: 0/1 iterates capacity **backwards**; unbounded iterates **forwards**. Coin Change II: coins outer = combinations; amount outer = permutations.
> **Gotchas:** Off-by-one in `dp` size (`n+1` for prefix-length states) · unreachable states must be `inf`, not `0` · LIS O(n log n) tails array is not the actual subsequence · start top-down memo if the recurrence isn't obvious, then convert.

---

> [!info] First Principles
> Use DP when the same subproblem shows up again and the best overall answer is built from best sub-answers. Write the recurrence first, set base cases, fill the table in an order where dependencies are ready, then shrink space if you only need the last row or two.

---

## Linear DP (1-D)

---

### Climbing Stairs `🎯 T2`

> [!example] Problem
> You are climbing a staircase. It takes n steps to reach the top.
> Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
> 
> **Example 1:**
> ```
> Input: n = 2
> Output: 2
> Explanation: There are two ways to climb to the top.
> 1. 1 step + 1 step
> 2. 2 steps
> ```
> 
> **Example 2:**
> ```
> Input: n = 3
> Output: 3
> Explanation: There are three ways to climb to the top.
> 1. 1 step + 1 step + 1 step
> 2. 1 step + 2 steps
> 3. 2 steps + 1 step
> ```
> 
> **Constraints:**
> - 1 <= n <= 45

> [!tip] Recognize · Gotcha
> **Signal:** "ways to reach step n" · **Gotcha:** Base `dp[1]=1, dp[2]=2`; roll two variables

> [!info] Approach
> reaching step `i` from step `i-1` or `i-2` creates overlapping recursive calls. `dp[i]` = number of ways to reach step `i`. `dp[i] = dp[i-1] + dp[i-2]`; base `dp[0]=1, dp[1]=1`. This is Fibonacci. Space collapses to two variables.

> [!note]- Python Solution
> ```python
> def climb_stairs(n):
>     if n <= 2:
>         return n
>     two_back, one_back = 1, 2
>     for _ in range(3, n + 1):
>         two_back, one_back = one_back, two_back + one_back
>     return one_back
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization; matrix exponentiation for O(log n).

---

### Min Cost Climbing Stairs `🎯 T2`

> [!example] Problem
> You are given an integer array cost where cost[i] is the cost of ith step on a staircase. Once you pay the cost, you can either climb one or two steps.
> You can either start from the step with index 0, or the step with index 1.
> Return the minimum cost to reach the top of the floor.
> 
> **Example 1:**
> ```
> Input: cost = [10,15,20]
> Output: 15
> Explanation: You will start at index 1.
> - Pay 15 and climb two steps to reach the top.
> The total cost is 15.
> ```
> 
> **Example 2:**
> ```
> Input: cost = [1,100,1,1,1,100,1,1,100,1]
> Output: 6
> Explanation: You will start at index 0.
> - Pay 1 and climb two steps to reach index 2.
> - Pay 1 and climb two steps to reach index 4.
> - Pay 1 and climb two steps to reach index 6.
> - Pay 1 and climb one step to reach index 7.
> - Pay 1 and climb two steps to reach index 9.
> - Pay 1 and climb one step to reach the top.
> The total cost is 6.
> ```
> 
> **Constraints:**
> - 2 <= cost.length <= 1000
> - 0 <= cost[i] <= 999

> [!info] Approach
> cost to reach step `i` depends on minimum of two prior steps. `dp[i]` = min cost to reach step `i`. `dp[i] = cost[i] + min(dp[i-1], dp[i-2])`; answer = `min(dp[n-1], dp[n-2])`.

> [!note]- Python Solution
> ```python
> def min_cost_climbing_stairs(cost):
>     n = len(cost)
>     two_back, one_back = cost[0], cost[1]
>     for i in range(2, n):
>         two_back, one_back = one_back, cost[i] + min(one_back, two_back)
>     return min(one_back, two_back)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down; extend `cost` with a zero at position `n` to unify the final min.

---

### House Robber `🎯 T2`

> [!example] Problem
> You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
> Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,3,1]
> Output: 4
> Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
> Total amount you can rob = 1 + 3 = 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [2,7,9,3,1]
> Output: 12
> Explanation: Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
> Total amount you can rob = 2 + 9 + 1 = 12.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 400

> [!tip] Recognize · Gotcha
> **Signal:** "no two adjacent" · **Gotcha:** Two-variable rolling

> [!info] Approach
> robbing house `i` forbids `i-1`; the optimal decision at each house depends on the optimal result two positions back. `dp[i]` = max money from houses `0..i`. `dp[i] = max(dp[i-1], dp[i-2] + nums[i])`; base `dp[0]=nums[0]`, `dp[1]=max(nums[0],nums[1])`.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     two_back, one_back = 0, 0
>     for n in nums:
>         two_back, one_back = one_back, max(one_back, two_back + n)
>     return one_back
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Greedy fails — skipping a high house today can be globally optimal.

---

### House Robber II (Circular) `🎯 T2`

> [!example] Problem
> You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.
> Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,2]
> Output: 3
> Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,1]
> Output: 4
> Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
> Total amount you can rob = 1 + 3 = 4.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,2,3]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 100
> - 0 <= nums[i] <= 1000

> [!tip] Recognize · Gotcha
> **Signal:** Circular street · **Gotcha:** `n == 1` → `nums[0]`

> [!info] Approach
> Circular constraint means house 0 and house n-1 can't both be robbed. Reduce to two linear subproblems that are mutually exclusive. `max(rob(0..n-2), rob(1..n-1))` — run linear House Robber twice.

> [!note]- Python Solution
> ```python
> def rob(nums):
>     def rob_linear(houses):
>         two_back, one_back = 0, 0
>         for h in houses:
>             two_back, one_back = one_back, max(one_back, two_back + h)
>         return one_back
> 
>     if len(nums) == 1:
>         return nums[0]
>     return max(rob_linear(nums[:-1]), rob_linear(nums[1:]))
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Single pass tracking whether house 0 was taken — equivalent but more complex to implement.

---

### Maximum Subarray (Kadane's — DP view) `🎯 T2`

> Full walkthrough: [Maximum Subarray](../data-structures/01-array.md#maximum-subarray--t2).

---

### Word Break `🎯 T2`

> [!example] Problem
> Given a string s and a dictionary of strings wordDict, return true if s can be segmented into a space-separated sequence of one or more dictionary words.
> Note that the same word in the dictionary may be reused multiple times in the segmentation.
> 
> **Example 1:**
> ```
> Input: s = "leetcode", wordDict = ["leet","code"]
> Output: true
> Explanation: Return true because "leetcode" can be segmented as "leet code".
> ```
> 
> **Example 2:**
> ```
> Input: s = "applepenapple", wordDict = ["apple","pen"]
> Output: true
> Explanation: Return true because "applepenapple" can be segmented as "apple pen apple".
> Note that you are allowed to reuse a dictionary word.
> ```
> 
> **Example 3:**
> ```
> Input: s = "catsandog", wordDict = ["cats","dog","sand","and","cat"]
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 300
> - 1 <= wordDict.length <= 1000
> - 1 <= wordDict[i].length <= 20
> - s and wordDict[i] consist of only lowercase English letters.
> - All the strings of wordDict are unique.

> [!tip] Recognize · Gotcha
> **Signal:** "can the string be segmented" · **Gotcha:** Use a set; cap `j` by max word length

> [!info] Approach
> `s[0..i]` is breakable if any split `s[0..j]` is breakable and `s[j+1..i]` is in the dictionary. Subproblems overlap at shared prefixes. `dp[i]` = True if `s[0..i-1]` is breakable. `dp[i] = any(dp[j] and s[j:i] in word_set)` for `j` in `[i-max_len, i)`. Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def word_break(s, wordDict):
>     word_set = set(wordDict)
>     max_len = max(len(w) for w in wordDict)
>     n = len(s)
>     dp = [False] * (n + 1)
>     dp[0] = True
>     for i in range(1, n + 1):
>         for j in range(max(0, i - max_len), i):
>             if dp[j] and s[j:i] in word_set:
>                 dp[i] = True
>                 break
>     return dp[n]
> ```

> [!success] Complexity
> Time O(n × max_word_len), Space O(n).

> [!tip] Alternatives
> BFS with memoization; Trie for faster dictionary lookup.

---

### Word Break II (LC 140) `🎯 T2`

> [!example] Problem
> Given string `s` and dictionary `wordDict`, return **all** sentences formed by inserting spaces so every word is in the dictionary. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Word Break, but "return all" instead of "can it" · **Gotcha:** Memoize on the start index — without it, inputs like `"aaaa…a"` with `["a","aa",…]` explode exponentially. Output size itself can be exponential, so the bound is output-sensitive.

> [!info] Approach
> `go(i)` = list of word-lists that segment `s[i:]`. Base: `go(len(s)) = [[]]` (one way: the empty sentence). For each end `j` with `s[i:j]` in the dictionary, prepend the word to every segmentation of `go(j)`. Cap `j` at `i + max_word_len` to avoid useless slices.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
>
> def word_break_ii(s, word_dict):
>     words = set(word_dict)
>     maxlen = max(map(len, words))
>
>     @lru_cache(None)
>     def go(i):
>         if i == len(s):
>             return [[]]
>         out = []
>         for j in range(i + 1, min(len(s), i + maxlen) + 1):
>             w = s[i:j]
>             if w in words:
>                 for rest in go(j):
>                     out.append([w] + rest)
>         return out
>
>     return [" ".join(p) for p in go(0)]
> ```

> [!success] Complexity
> Time O(n · L + output size), Space O(output size) where L = max word length.

> [!tip] Alternatives
> Run Word Break (boolean DP) first and return `[]` immediately if it fails — avoids building partial lists for unsegmentable inputs.

---

### Decode Ways `🎯 T2`

> [!example] Problem
> You have intercepted a secret message encoded as a string of numbers. The message is decoded via the following mapping:
> "1" -> 'A'
> "2" -> 'B'
> ...
> "25" -> 'Y'
> "26" -> 'Z'
> However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes ("2" and "5" vs "25").
> For example, "11106" can be decoded into:
> Note: there may be strings that are impossible to decode.
> 
> Given a string s containing only digits, return the number of ways to decode it. If the entire string cannot be decoded in any valid way, return 0.
> The test cases are generated so that the answer fits in a 32-bit integer.
> 
> **Example 1:**
> ```
> Input: s = "12"
> Output: 2
> Explanation:
> "12" could be decoded as "AB" (1 2) or "L" (12).
> ```
> 
> **Example 2:**
> ```
> Input: s = "226"
> Output: 3
> Explanation:
> "226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
> ```
> 
> **Example 3:**
> ```
> Input: s = "06"
> Output: 0
> Explanation:
> "06" cannot be mapped to "F" because of the leading zero ("6" is different from "06"). In this case, the string is not a valid encoding, so return 0.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 100
> - s contains only digits and may contain leading zero(s).

> [!tip] Recognize · Gotcha
> **Signal:** One- or two-digit branch · **Gotcha:** `'0'` alone is invalid; `"06"` is not 6

> [!info] Approach
> each position can be decoded as 1 or 2 digits; choices overlap across prefixes. `dp[i]` = number of decodings of `s[0..i-1]`. add `dp[i-1]` if `s[i-1] != '0'`; add `dp[i-2]` if `10 ≤ s[i-2:i] ≤ 26`. Base: `dp[0]=1`.

> [!note]- Python Solution
> ```python
> def num_decodings(s):
>     two_back, one_back = 1, 0 if s[0] == '0' else 1
>     for i in range(2, len(s) + 1):
>         curr = 0
>         if s[i-1] != '0':
>             curr += one_back
>         if 10 <= int(s[i-2:i]) <= 26:
>             curr += two_back
>         two_back, one_back = one_back, curr
>     return one_back
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Top-down memoization. Wildcard variant (LC 639) adds branching at `'*'` but same structure.

---

### Frog Jump (LC 403) `🎯 T2`

> [!example] Problem
> Stones at sorted positions `stones` (first is 0). A frog starts on stone 0 and its first jump is 1 unit. If its last jump was `k`, the next jump is `k-1`, `k`, or `k+1` (must be positive). Can it reach the last stone? [H]

> [!tip] Recognize · Gotcha
> **Signal:** Reachability where the allowed move depends on the previous move · **Gotcha:** State is `(stone, last_jump)`, not just the stone. Jump sizes never exceed `n`, so the state space is O(n²).

> [!info] Approach
> `reach[pos]` = set of jump sizes that can land on `pos`. Seed `reach[0] = {0}` so the first jump is 1. Process stones in order; for each `k` in `reach[pos]` and each `step` in `k-1, k, k+1` with `step > 0` and `pos + step` a stone, add `step` to that stone's set. Answer is whether the last stone's set is non-empty.

> [!note]- Python Solution
> ```python
> def can_cross(stones):
>     pos = {s: set() for s in stones}
>     pos[stones[0]].add(0)
>     for s in stones:
>         for k in pos[s]:
>             for step in (k - 1, k, k + 1):
>                 if step > 0 and s + step in pos:
>                     pos[s + step].add(step)
>     return bool(pos[stones[-1]])
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> Top-down `f(stone_index, k)` with memo; same state space. Quick early exit: if `stones[1] != 1`, return False.

---

## 0/1 Knapsack

---

### Subset Sum Problem `🎯 T2`

> [!example] Problem
> Given integers and target `T`, can any subset sum to `T`?

> [!info] Approach
> each item has two choices (include/exclude); overlap arises because the same remaining capacity is reachable via multiple item sequences. `dp[j]` = True if sum `j` is achievable using a subset of items seen so far. iterate items; for each item `x`, sweep `j` from `T` down to `x`: `dp[j] |= dp[j - x]`. Reverse sweep prevents reuse of same item (0/1 knapsack). Base: `dp[0]=True`.

> [!note]- Python Solution
> ```python
> def can_partition(nums, target):
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for x in nums:
>         for j in range(target, x - 1, -1):
>             dp[j] = dp[j] or dp[j - x]
>     return dp[target]
> ```

> [!success] Complexity
> Time O(n × T), Space O(T).

> [!tip] Alternatives
> Meet-in-the-middle O(2^(n/2)) for very large `n` with small target; bitset optimization.

---

### Partition Equal Subset Sum `🎯 T2`

> [!example] Problem
> Given an integer array nums, return true if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or false otherwise.
> 
> **Example 1:**
> ```
> Input: nums = [1,5,11,5]
> Output: true
> Explanation: The array can be partitioned as [1, 5, 5] and [11].
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,5]
> Output: false
> Explanation: The array cannot be partitioned into equal sum subsets.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 200
> - 1 <= nums[i] <= 100

> [!tip] Recognize · Gotcha
> **Signal:** "split into two equal halves" · **Gotcha:** Odd total → False immediately

> [!info] Approach
> Equal partition iff one subset sums to `total/2`. Reduces to subset-sum with `T = total // 2`. Same as Subset Sum with `target = sum(nums) // 2`. Odd total → return False immediately. Then run 0/1 knapsack DP.

> [!note]- Python Solution
> ```python
> def can_partition(nums):
>     total = sum(nums)
>     if total % 2:
>         return False
>     target = total // 2
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for x in nums:
>         for j in range(target, x - 1, -1):
>             dp[j] = dp[j] or dp[j - x]
>     return dp[target]
> ```

> [!success] Complexity
> Time O(n × sum), Space O(sum).

> [!tip] Alternatives
> Early exit if any single element > target. Bitset trick for constant-factor speedup.

---

### Last Stone Weight II `⚡ T1`

> [!example] Problem
> You are given an array of integers stones where stones[i] is the weight of the ith stone.
> We are playing a game with the stones. On each turn, we choose any two stones and smash them together. Suppose the stones have weights x and y with x <= y. The result of this smash is:
> At the end of the game, there is at most one stone left.
> Return the smallest possible weight of the left stone. If there are no stones left, return 0.
> 
> **Example 1:**
> ```
> Input: stones = [2,7,4,1,8,1]
> Output: 1
> Explanation:
> We can combine 2 and 4 to get 2, so the array converts to [2,7,1,8,1] then,
> we can combine 7 and 8 to get 1, so the array converts to [2,1,1,1] then,
> we can combine 2 and 1 to get 1, so the array converts to [1,1,1] then,
> we can combine 1 and 1 to get 0, so the array converts to [1], then that's the optimal value.
> ```
> 
> **Example 2:**
> ```
> Input: stones = [31,26,33,21,40]
> Output: 5
> ```
> 
> **Constraints:**
> - 1 <= stones.length <= 30
> - 1 <= stones[i] <= 100

> [!info] Approach
> Each stone ultimately gets a sign `+1` or `-1`; minimize `|P - N| = |total - 2N|`. Maximize `N ≤ total/2`. Same as subset sum to target. `dp[j]` = True if subset sum `j` is reachable, for `j ≤ total // 2`. Standard 0/1 knapsack boolean DP; answer = `total - 2 × max_j_where_dp[j]`.

> [!note]- Python Solution
> ```python
> def last_stone_weight_ii(stones):
>     total = sum(stones)
>     target = total // 2
>     dp = [False] * (target + 1)
>     dp[0] = True
>     for s in stones:
>         for j in range(target, s - 1, -1):
>             dp[j] = dp[j] or dp[j - s]
>     best = next(j for j in range(target, -1, -1) if dp[j])
>     return total - 2 * best
> ```

> [!success] Complexity
> Time O(n × total), Space O(total).

> [!tip] Alternatives
> Integer DP counting ways; the boolean version suffices here.

---

## Unbounded Knapsack

---

### Coin Change (Min Coins) `🎯 T2`

> [!example] Problem
> You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
> Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.
> You may assume that you have an infinite number of each kind of coin.
> 
> **Example 1:**
> ```
> Input: coins = [1,2,5], amount = 11
> Output: 3
> Explanation: 11 = 5 + 5 + 1
> ```
> 
> **Example 2:**
> ```
> Input: coins = [2], amount = 3
> Output: -1
> ```
> 
> **Example 3:**
> ```
> Input: coins = [1], amount = 0
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= coins.length <= 12
> - 1 <= coins[i] <= 2^{31} - 1
> - 0 <= amount <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** "fewest coins" · **Gotcha:** Init `inf`, `dp[0] = 0`; return `-1` if still `inf`

> [!failure] Tempting wrong approach
> Greedy largest-coin-first — coins `[1,3,4]`, amount 6 gives 4+1+1 (3 coins), optimal is 3+3 (2).

> [!info] Approach
> Coins are reusable → unbounded knapsack. Overlapping subproblems: the optimal solution for amount `i` reuses optimal solutions for `i - coin`. `dp[i]` = min coins to make amount `i`. `dp[i] = min(dp[i-c] + 1)` for each coin `c ≤ i`; forward sweep (reuse allowed). Base: `dp[0]=0`, rest `inf`.

> [!note]- Python Solution
> ```python
> def coin_change(coins, amount):
>     dp = [float('inf')] * (amount + 1)
>     dp[0] = 0
>     for i in range(1, amount + 1):
>         for c in coins:
>             if c <= i:
>                 dp[i] = min(dp[i], dp[i - c] + 1)
>     return dp[amount] if dp[amount] != float('inf') else -1
> ```

> [!success] Complexity
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> BFS level-by-level (level = coin count) — same complexity but queue overhead. Top-down memo.

---

### Coin Change II (Total Ways) `🎯 T2`

> [!example] Problem
> You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
> Return the number of combinations that make up that amount. If that amount of money cannot be made up by any combination of the coins, return 0.
> You may assume that you have an infinite number of each kind of coin.
> The answer is guaranteed to fit into a signed 32-bit integer.
> 
> **Example 1:**
> ```
> Input: amount = 5, coins = [1,2,5]
> Output: 4
> Explanation: there are four ways to make up the amount:
> 5=5
> 5=2+2+1
> 5=2+1+1+1
> 5=1+1+1+1+1
> ```
> 
> **Example 2:**
> ```
> Input: amount = 3, coins = [2]
> Output: 0
> Explanation: the amount of 3 cannot be made up just with coins of 2.
> ```
> 
> **Example 3:**
> ```
> Input: amount = 10, coins = [10]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= coins.length <= 300
> - 1 <= coins[i] <= 5000
> - All the values of coins are unique.
> - 0 <= amount <= 5000

> [!tip] Recognize · Gotcha
> **Signal:** "number of combinations" · **Gotcha:** Amount outer counts permutations (LC 377)

> [!info] Approach
> Combinations require each denomination to be processed once, not per position. Loop coins outer, amounts inner. `dp[i]` = number of combination ways to make amount `i`. Outer loop over coins; inner forward sweep: `dp[i] += dp[i-c]`. This ensures [1,2] and [2,1] are the same combination.

> [!note]- Python Solution
> ```python
> def change(amount, coins):
>     dp = [0] * (amount + 1)
>     dp[0] = 1
>     for c in coins:
>         for i in range(c, amount + 1):
>             dp[i] += dp[i - c]
>     return dp[amount]
> ```

> [!success] Complexity
> Time O(amount × |coins|), Space O(amount).

> [!tip] Alternatives
> Swapping loop order counts permutations (ordered sequences) — different problem. 2D DP clarifies the derivation.

---

### Combination Sum IV (LC 377) `🎯 T2`

> [!example] Problem
> Distinct positive `nums`, a `target`. Count the **ordered** sequences (repetition allowed) that sum to `target`. **Medium.**
>
> ```
> Input: nums = [1,2,3], target = 4  →  7
> (1,1,1,1) (1,1,2) (1,2,1) (2,1,1) (2,2) (1,3) (3,1)
> ```

> [!tip] Recognize · Gotcha
> **Signal:** "count", and different orderings count separately · **Gotcha:** it's DP, not backtracking — enumerating the 7 sequences generalizes to exponential output and TLEs.

> [!info] Approach
> **Key insight:** order matters → put the **amount in the outer loop**. `dp[t]` = number of sequences summing to `t`; the last number picked is any `x ≤ t`, so `dp[t] = Σ dp[t − x]`. Swapping the loops (coins outer) gives Coin Change II's unordered count — the single most-asked contrast.

> [!note]- Python Solution
> ```python
> def combination_sum4(nums, target):
>     dp = [1] + [0] * target          # one way to make 0: pick nothing
>     for t in range(1, target + 1):   # amount OUTER → ordered
>         for x in nums:
>             if x <= t:
>                 dp[t] += dp[t - x]
>     return dp[target]
> ```

> [!success] Complexity
> **TC**: O(target · |nums|) | **SC**: O(target).

> [!tip] Alternatives
> Top-down `@cache def f(t): return t == 0 or sum(f(t-x) for x in nums if x <= t)`. **Follow-up (negatives allowed):** unbounded cycles → infinite answers; must cap sequence length.

---


### Perfect Squares `🎯 T2`

> [!example] Problem
> Given an integer n, return the least number of perfect square numbers that sum to n.
> A perfect square is an integer that is the square of an integer; in other words, it is the product of some integer with itself. For example, 1, 4, 9, and 16 are perfect squares while 3 and 11 are not.
> 
> **Example 1:**
> ```
> Input: n = 12
> Output: 3
> Explanation: 12 = 4 + 4 + 4.
> ```
> 
> **Example 2:**
> ```
> Input: n = 13
> Output: 2
> Explanation: 13 = 4 + 9.
> ```
> 
> **Constraints:**
> - 1 <= n <= 10^4

> [!info] Approach
> Perfect squares are unlimited "coins"; this is unbounded knapsack / coin change with coins = {1,4,9,16,...}. `dp[i]` = min squares summing to `i`. `dp[i] = min(dp[i - k²] + 1)` for all `k² ≤ i`. Base: `dp[0]=0`.

> [!note]- Python Solution
> ```python
> def num_squares(n):
>     squares = [k*k for k in range(1, int(n**0.5) + 1)]
>     dp = [float('inf')] * (n + 1)
>     dp[0] = 0
>     for i in range(1, n + 1):
>         for sq in squares:
>             if sq > i:
>                 break
>             dp[i] = min(dp[i], dp[i - sq] + 1)
>     return dp[n]
> ```

> [!success] Complexity
> Time O(n√n), Space O(n).

> [!tip] Alternatives
> BFS (level = number of squares used). Lagrange's four-square theorem: answer ≤ 4; check 1, 2, 3, 4 mathematically in O(√n) — but DP is the expected interview answer.

---

## LCS Family

---

### Longest Common Subsequence `🎯 T2`

> [!example] Problem
> Given two strings text1 and text2, return the length of their longest common subsequence. If there is no common subsequence, return 0.
> A subsequence of a string is a new string generated from the original string with some characters (can be none) deleted without changing the relative order of the remaining characters.
> A common subsequence of two strings is a subsequence that is common to both strings.
> 
> **Example 1:**
> ```
> Input: text1 = "abcde", text2 = "ace" 
> Output: 3  
> Explanation: The longest common subsequence is "ace" and its length is 3.
> ```
> 
> **Example 2:**
> ```
> Input: text1 = "abc", text2 = "abc"
> Output: 3
> Explanation: The longest common subsequence is "abc" and its length is 3.
> ```
> 
> **Example 3:**
> ```
> Input: text1 = "abc", text2 = "def"
> Output: 0
> Explanation: There is no such common subsequence, so the result is 0.
> ```
> 
> **Constraints:**
> - 1 <= text1.length, text2.length <= 1000
> - text1 and text2 consist of only lowercase English characters.

> [!tip] Recognize · Gotcha
> **Signal:** 2D DP · **Gotcha:** **Space** O(min(m,n)) possible; **empty** string base.

> [!info] Approach
> Matching characters at positions `i,j` yields a subproblem on the remaining suffixes; these sub-results are reused. `dp[i][j]` = LCS length of `s1[0..i-1]` and `s2[0..j-1]`. If `s1[i-1]==s2[j-1]`: `dp[i][j] = dp[i-1][j-1]+1`; else `max(dp[i-1][j], dp[i][j-1])`. Space: roll to one row.

> [!note]- Python Solution
> ```python
> def longest_common_subsequence(text1, text2):
>     if len(text1) < len(text2):
>         text1, text2 = text2, text1
>     prev = [0] * (len(text2) + 1)
>     for ch1 in text1:
>         curr = [0] * (len(text2) + 1)
>         for j, ch2 in enumerate(text2, 1):
>             curr[j] = prev[j-1] + 1 if ch1 == ch2 else max(prev[j], curr[j-1])
>         prev = curr
>     return prev[len(text2)]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D table for path reconstruction. Hunt-Szymanski for sparse matches.

---

### Edit Distance `🎯 T2`

> [!example] Problem
> Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.
> You have the following three operations permitted on a word
> 
> **Example 1:**
> ```
> Input: word1 = "horse", word2 = "ros"
> Output: 3
> Explanation: 
> horse -> rorse (replace 'h' with 'r')
> rorse -> rose (remove 'r')
> rose -> ros (remove 'e')
> ```
> 
> **Example 2:**
> ```
> Input: word1 = "intention", word2 = "execution"
> Output: 5
> Explanation: 
> intention -> inention (remove 't')
> inention -> enention (replace 'i' with 'e')
> enention -> exention (replace 'n' with 'x')
> exention -> exection (replace 'n' with 'c')
> exection -> execution (insert 'u')
> ```
> 
> **Constraints:**
> - 0 <= word1.length, word2.length <= 500
> - word1 and word2 consist of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** "min ops to convert" · **Gotcha:** Base row/col = `i` / `j`, not 0

> [!info] Approach
> Three operations at each mismatch create overlapping subproblems on shorter string pairs. `dp[i][j]` = edit distance between `word1[0..i-1]` and `word2[0..j-1]`. If chars match: `dp[i-1][j-1]`; else `1 + min(replace=dp[i-1][j-1], delete=dp[i-1][j], insert=dp[i][j-1])`. Base: `dp[i][0]=i`, `dp[0][j]=j`.

> [!note]- Python Solution
> ```python
> def min_distance(word1, word2):
>     m, n = len(word1), len(word2)
>     prev = list(range(n + 1))
>     for i in range(1, m + 1):
>         curr = [i] + [0] * n
>         for j in range(1, n + 1):
>             if word1[i-1] == word2[j-1]:
>                 curr[j] = prev[j-1]
>             else:
>                 curr[j] = 1 + min(prev[j-1], prev[j], curr[j-1])
>         prev = curr
>     return prev[n]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Full 2D for operation reconstruction. Ukkonen's O(k×min(m,n)) when distance `k` is small.

---

### Longest Palindromic Subsequence `🎯 T2`

> [!example] Problem
> Given a string s, find the longest palindromic subsequence's length in s.
> A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.
> 
> **Example 1:**
> ```
> Input: s = "bbbab"
> Output: 4
> Explanation: One possible longest palindromic subsequence is "bbbb".
> ```
> 
> **Example 2:**
> ```
> Input: s = "cbbd"
> Output: 2
> Explanation: One possible longest palindromic subsequence is "bb".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 1000
> - s consists only of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** `LCS(s, rev(s))` shortcut · **Gotcha:** Single chars: `dp[i][i] = 1` base case

> [!info] Approach
> A palindrome is its own reverse; LPS(s) = LCS(s, reverse(s)). Both overlapping subproblems. `dp[i][j]` = LPS length in `s[i..j]`. If `s[i]==s[j]`: `dp[i][j] = dp[i+1][j-1]+2`; else `max(dp[i+1][j], dp[i][j-1])`. Fill diagonals outward (length 1→2→…→n).

> [!note]- Python Solution
> ```python
> def longest_palindrome_subseq(s):
>     n = len(s)
>     dp = [[0] * n for _ in range(n)]
>     for i in range(n):
>         dp[i][i] = 1
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             if s[i] == s[j]:
>                 dp[i][j] = (dp[i+1][j-1] if length > 2 else 0) + 2
>             else:
>                 dp[i][j] = max(dp[i+1][j], dp[i][j-1])
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n²), Space O(n²).

> [!tip] Alternatives
> LCS(s, s[::-1]) — simpler to implement, same complexity. Space-optimize with two 1D arrays.

---

### Minimum ASCII Delete Sum for Two Strings `🎯 T2`

> [!example] Problem
> Given two strings s1 and s2, return the lowest ASCII sum of deleted characters to make two strings equal.
> 
> **Example 1:**
> ```
> Input: s1 = "sea", s2 = "eat"
> Output: 231
> Explanation: Deleting "s" from "sea" adds the ASCII value of "s" (115) to the sum.
> Deleting "t" from "eat" adds 116 to the sum.
> At the end, both strings are equal, and 115 + 116 = 231 is the minimum sum possible to achieve this.
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "delete", s2 = "leet"
> Output: 403
> Explanation: Deleting "dee" from "delete" to turn the string into "let",
> adds 100[d] + 101[e] + 101[e] to the sum.
> Deleting "e" from "leet" adds 101[e] to the sum.
> At the end, both strings are equal to "let", and the answer is 100+101+101+101 = 403.
> If instead we turned both strings into "lee" or "eet", we would get answers of 433 or 417, which are higher.
> ```
> 
> **Constraints:**
> - 1 <= s1.length, s2.length <= 1000
> - s1 and s2 consist of lowercase English letters.

> [!info] Approach
> Deleting characters to equalize is equivalent to keeping the maximum-weight common subsequence (measured in ASCII values). Overlapping on pairs of string prefixes. `dp[i][j]` = min ASCII delete cost to equalize `s1[0..i-1]` and `s2[0..j-1]`. If `s1[i-1]==s2[j-1]`: `dp[i][j]=dp[i-1][j-1]`; else `min(dp[i-1][j]+ord(s1[i-1]), dp[i][j-1]+ord(s2[j-1]))`. Base: prefix ASCII sums.

> [!note]- Python Solution
> ```python
> def minimum_delete_sum(s1, s2):
>     m, n = len(s1), len(s2)
>     prev = [sum(ord(c) for c in s2[:j]) for j in range(n + 1)]
>     for i in range(1, m + 1):
>         curr = [prev[0] + ord(s1[i-1])] + [0] * n
>         for j in range(1, n + 1):
>             if s1[i-1] == s2[j-1]:
>                 curr[j] = prev[j-1]
>             else:
>                 curr[j] = min(prev[j] + ord(s1[i-1]), curr[j-1] + ord(s2[j-1]))
>         prev = curr
>     return prev[n]
> ```

> [!success] Complexity
> Time O(m×n), Space O(min(m,n)).

> [!tip] Alternatives
> Compute LCS weighted by ASCII; answer = `total_ascii(s1) + total_ascii(s2) - 2 × weighted_LCS`.

---

### Minimum Window Subsequence (LC 727) `🎯 T2`

> [!example] Problem
> Given strings `s1` and `s2`, return *the minimum contiguous substring part of *`s1`*, so that *`s2`* is a subsequence of the part*.
> 
> If there is no such window in `s1` that covers all characters in `s2`, return the empty string `""`. If there are multiple such minimum-length windows, return the one with the **left-most starting index**.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** s1 = "abcdebdde", s2 = "bde"
> **Output:** "bcde"
> **Explanation:** 
> "bcde" is the answer because it occurs before "bdde" which has the same length.
> "deb" is not a smaller window because the elements of s2 in the window must occur in order.
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** s1 = "jmeqksfrsdcmsiwvaovztaqenprpvnbstl", s2 = "u"
> **Output:** ""
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= s1.length <= 2 * 10^4`
> 	
> - `1 <= s2.length <= 100`
> 	
> - `s1` and `s2` consist of lowercase English letters.

> [!info] Approach
> Brute force tries all substrings O(n²*m). DP achieves O(n*m): track, for each position in s, the earliest start index in s such that t[0..j] has been matched as a subsequence ending at that position. 2D DP — dp[i][j] = starting index in s such that s[dp[i][j]..i] contains t[0..j] as a subsequence. dp[i][j] = dp[i-1][j-1] if s[i]==t[j] else dp[i-1][j]. Base: dp[i][0] = i when s[i]==t[0]. When dp[i][len(t)-1] is valid, compute window length = i - dp[i][len(t)-1] + 1 and track minimum.

> [!note]- Python Solution
> ```python
> def min_window(s, t):
>     m, n = len(s), len(t)
>     # dp[j] = start index in s for matching t[0..j] ending at current s position
>     INF = float('inf')
>     dp = [INF] * n
>     best_start, best_len = 0, INF
> 
>     for i in range(m):
>         # iterate j in reverse to avoid using s[i] twice in same row
>         new_dp = [INF] * n
>         for j in range(n):
>             if s[i] == t[j]:
>                 if j == 0:
>                     new_dp[j] = i  # fresh match starting at i
>                 elif dp[j-1] != INF:
>                     new_dp[j] = dp[j-1]  # extend previous match
>             else:
>                 new_dp[j] = dp[j]  # carry forward
>         dp = new_dp
>         if dp[n-1] != INF:
>             window_len = i - dp[n-1] + 1
>             if window_len < best_len:
>                 best_len = window_len
>                 best_start = dp[n-1]
> 
>     return s[best_start:best_start + best_len] if best_len != INF else ""
> ```

> [!success] Complexity
> O(n*m) time, O(m) space (rolling 1D dp array, optimized from O(n*m)).

> [!tip] Alternatives
> Two-pointer O(n*m): forward pass to find end of window (extend right until t matched), backward pass to minimize start (contract left). Simpler to implement — for each valid end, walk backwards through s matching t in reverse to find tightest start.

---

## Grid DP

---

### Unique Paths `⚡ T1`

> [!example] Problem
> There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
> Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.
> The test cases are generated so that the answer will be less than or equal to 2 * 109.
> 
> **Example 1:**
> ```
> Input: m = 3, n = 7
> Output: 28
> ```
> 
> **Example 2:**
> ```
> Input: m = 3, n = 2
> Output: 3
> Explanation: From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
> 1. Right -> Down -> Down
> 2. Down -> Down -> Right
> 3. Down -> Right -> Down
> ```
> 
> **Constraints:**
> - 1 <= m, n <= 100

> [!tip] Recognize · Gotcha
> **Signal:** `dp[r][c] = dp[r-1][c] + dp[r][c-1]` · **Gotcha:** Base row/col = all 1s

> [!info] Approach
> Each cell is reachable from exactly above or left; paths to any cell = sum of paths to two neighbors — overlapping. `dp[j]` = paths to column `j` of current row (rolling 1D array). `dp[j] += dp[j-1]` for each row. Base: all 1s initially (single path along edges).

> [!note]- Python Solution
> ```python
> def unique_paths(m, n):
>     dp = [1] * n
>     for _ in range(1, m):
>         for j in range(1, n):
>             dp[j] += dp[j-1]
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Combinatorics: `math.comb(m+n-2, m-1)` — O(min(m,n)) time, O(1) space.

---

### Unique Paths II (With Obstacles) `🎯 T2`

> [!example] Problem
> You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
> An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.
> Return the number of possible unique paths that the robot can take to reach the bottom-right corner.
> The testcases are generated so that the answer will be less than or equal to 2 * 109.
> 
> **Example 1:**
> ```
> Input: obstacleGrid = [[0,0,0],[0,1,0],[0,0,0]]
> Output: 2
> Explanation: There is one obstacle in the middle of the 3x3 grid above.
> There are two ways to reach the bottom-right corner:
> 1. Right -> Right -> Down -> Down
> 2. Down -> Down -> Right -> Right
> ```
> 
> **Example 2:**
> ```
> Input: obstacleGrid = [[0,1],[0,0]]
> Output: 1
> ```
> 
> **Constraints:**
> - m == obstacleGrid.length
> - n == obstacleGrid[i].length
> - 1 <= m, n <= 100
> - obstacleGrid[i][j] is 0 or 1.

> [!tip] Recognize · Gotcha
> **Signal:** Set `dp[r][c] = 0` when obstacle · **Gotcha:** Re-check first row/col early

> [!info] Approach
> Same grid DP but obstacle cells have zero paths and block propagation downstream. `dp[j]` = paths to `(i,j)` treating blocked cells as 0. Same recurrence; set `dp[j]=0` when `obstacleGrid[i][j]==1`. Careful with first row/col initialization.

> [!note]- Python Solution
> ```python
> def unique_paths_with_obstacles(obstacleGrid):
>     m, n = len(obstacleGrid), len(obstacleGrid[0])
>     dp = [0] * n
>     dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
>     for i in range(m):
>         for j in range(n):
>             if obstacleGrid[i][j] == 1:
>                 dp[j] = 0
>             elif j > 0:
>                 dp[j] += dp[j-1]
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Full 2D table is simpler to reason about. No combinatorial shortcut with obstacles.

---

### Minimum Path Sum `⚡ T1`

> [!example] Problem
> Given a m x n grid filled with non-negative numbers, find a path from top left to bottom right, which minimizes the sum of all numbers along its path.
> Note: You can only move either down or right at any point in time.
> 
> **Example 1:**
> ```
> Input: grid = [[1,3,1],[1,5,1],[4,2,1]]
> Output: 7
> Explanation: Because the path 1 → 3 → 1 → 1 → 1 minimizes the sum.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,2,3],[4,5,6]]
> Output: 12
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 200
> - 0 <= grid[i][j] <= 200

> [!tip] Recognize · Gotcha
> **Signal:** "min cost, right/down" · **Gotcha:** Init first row/col as prefix sums

> [!info] Approach
> Min-cost path to `(i,j)` = grid value + min of cost from above or left — overlapping. `dp[j]` = min cost to reach column `j` of current row. `dp[j] = grid[i][j] + min(dp[j], dp[j-1])`. Initialize first row as prefix sums.

> [!note]- Python Solution
> ```python
> def min_path_sum(grid):
>     m, n = len(grid), len(grid[0])
>     dp = grid[0][:]
>     for j in range(1, n):
>         dp[j] += dp[j-1]
>     for i in range(1, m):
>         dp[0] += grid[i][0]
>         for j in range(1, n):
>             dp[j] = grid[i][j] + min(dp[j], dp[j-1])
>     return dp[n-1]
> ```

> [!success] Complexity
> Time O(m×n), Space O(n).

> [!tip] Alternatives
> Dijkstra if negative weights possible. In-place modification gives O(1) extra space.

---

### Maximal Square `🎯 T2`

> [!example] Problem
> Given an m x n binary matrix filled with 0's and 1's, find the largest square containing only 1's and return its area.
> 
> **Example 1:**
> ```
> Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [["0","1"],["1","0"]]
> Output: 1
> ```
> 
> **Example 3:**
> ```
> Input: matrix = [["0"]]
> Output: 0
> ```
> 
> **Constraints:**
> - m == matrix.length
> - n == matrix[i].length
> - 1 <= m, n <= 300
> - matrix[i][j] is '0' or '1'.

> [!tip] Recognize · Gotcha
> **Signal:** Extend bottom-right corner · **Gotcha:** `matrix` is `str`, cast to int

> [!info] Approach
> A square of side `k` at `(i,j)` requires squares of side `k-1` at three adjacent neighbors — optimal substructure with overlapping sub-rectangles. `dp[i][j]` = side of largest all-1s square with bottom-right at `(i,j)`. If `matrix[i][j]=='1'`: `dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1`. Roll to two rows or 1D.

> [!note]- Python Solution
> ```python
> def maximal_square(matrix):
>     m, n = len(matrix), len(matrix[0])
>     dp = [[0] * (n + 1) for _ in range(m + 1)]
>     side = 0
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if matrix[i-1][j-1] == '1':
>                 dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
>                 side = max(side, dp[i][j])
>     return side * side
> ```

> [!success] Complexity
> Time O(m×n), Space O(m×n) → reducible to O(n).

> [!tip] Alternatives
> Histogram approach (largest rectangle in histogram per row) — O(m×n) but harder to implement.

---

### Dungeon Game (LC 174) `🎯 T2`

> [!example] Problem
> A knight starts at the top-left of an `m×n` grid and must reach the bottom-right (moving only right or down). Each cell adds or subtracts health. Health must stay ≥ 1 at all times. Return the minimum initial health. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Path where a running prefix must never dip below a threshold · **Gotcha:** Forward DP (min-sum or max-sum) fails — the best prefix and the future requirement interact. Go **backwards** from the princess: `dp[i][j]` = min health needed *entering* cell `(i,j)`.

> [!info] Approach
> At the goal you need `max(1, 1 - d)`. For any cell: health on entry must satisfy `entry + d[i][j] >= need_next` where `need_next = min(dp[i+1][j], dp[i][j+1])`, so `dp[i][j] = max(1, need_next - d[i][j])`. The `max(1, …)` clamp is the "never below 1" rule: a big heal cannot lower the requirement below 1. Rolling 1-D array, with `inf` sentinels beyond the edges.

> [!note]- Python Solution
> ```python
> def calculate_minimum_hp(d):
>     m, n = len(d), len(d[0])
>     dp = [float('inf')] * (n + 1)
>     dp[n - 1] = 1
>     for i in range(m - 1, -1, -1):
>         for j in range(n - 1, -1, -1):
>             need = min(dp[j], dp[j + 1]) - d[i][j]
>             dp[j] = max(1, need)
>         dp[n] = float('inf')
>     return dp[0]
> ```

> [!success] Complexity
> Time O(m · n), Space O(n).

> [!tip] Alternatives
> Binary search on initial health + forward feasibility DP (maximize health with clamps) — O(mn log answer), more code.

---

### Cherry Pickup (LC 741) `💤 T3`

> [!example] Problem
> `n×n` grid: `0` empty, `1` cherry, `-1` thorn. Walk (0,0) → (n-1,n-1) moving right/down, then back to (0,0) moving left/up, picking cherries (a picked cell becomes 0). Return max cherries; `0` if no valid path. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Round trip on a grid · **Gotcha:** "Best path, remove cherries, best path again" is greedy and wrong. Model two simultaneous down-right walkers; count a shared cell once.

> [!info] Approach
> Reverse the return trip: both walkers go down-right from (0,0). After `t` steps both are on diagonal `r + c = t`, so state is `dp[r1][r2]` with `c = t - r`. Each walker came from up or left, so four predecessors. Skip thorns and unreachable (`-inf`) states. By symmetry only `r1 <= r2` is needed. Answer `max(0, dp[n-1][n-1])` after `2n-2` steps.

> [!note]- Python Solution
> ```python
> def cherry_pickup(grid):
>     n = len(grid)
>     NEG = float('-inf')
>     dp = [[NEG] * n for _ in range(n)]
>     dp[0][0] = grid[0][0]
>     for t in range(1, 2 * n - 1):
>         new = [[NEG] * n for _ in range(n)]
>         for r1 in range(max(0, t - n + 1), min(n - 1, t) + 1):
>             for r2 in range(r1, min(n - 1, t) + 1):
>                 c1, c2 = t - r1, t - r2
>                 if grid[r1][c1] == -1 or grid[r2][c2] == -1:
>                     continue
>                 best = max(dp[r1][r2],
>                            dp[r1 - 1][r2] if r1 else NEG,
>                            dp[r1][r2 - 1] if r2 else NEG,
>                            dp[r1 - 1][r2 - 1] if r1 and r2 else NEG)
>                 if best == NEG:
>                     continue
>                 gain = grid[r1][c1] + (grid[r2][c2] if r1 != r2 else 0)
>                 new[r1][r2] = best + gain
>         dp = new
>     return max(0, dp[n - 1][n - 1])
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> Memoized `f(r1, c1, r2)` top-down (`c2 = r1 + c1 - r2`). See the lecture's *Two-Walker Grid DP* section.

---

## State Machine DP (Stock Problems)

---

### Best Time to Buy and Sell Stock (All Variants) `🎯 T2`

> [!example] Problem
> You are given an array prices where prices[i] is the price of a given stock on the ith day.
> You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
> Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
> 
> **Example 1:**
> ```
> Input: prices = [7,1,5,3,6,4]
> Output: 5
> Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
> Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.
> ```
> 
> **Example 2:**
> ```
> Input: prices = [7,6,4,3,1]
> Output: 0
> Explanation: In this case, no transactions are done and the max profit = 0.
> ```
> 
> **Constraints:**
> - 1 <= prices.length <= 10^5
> - 0 <= prices[i] <= 10^4

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     min_price, max_profit = float('inf'), 0
>     for p in prices:
>         min_price = min(min_price, p)
>         max_profit = max(max_profit, p - min_price)
>     return max_profit
> ```

> [!example] Problem II — Unlimited transactions

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     return sum(max(0, prices[i] - prices[i-1]) for i in range(1, len(prices)))
> ```

> [!example] Problem III — At most 2 transactions

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     b1 = b2 = float('-inf')
>     s1 = s2 = 0
>     for p in prices:
>         b1 = max(b1, -p)
>         s1 = max(s1, b1 + p)
>         b2 = max(b2, s1 - p)
>         s2 = max(s2, b2 + p)
>     return s2
> ```

> [!example] Problem IV — At most k transactions

> [!note]- Python Solution
> ```python
> def max_profit(k, prices):
>     n = len(prices)
>     if not prices or k == 0:
>         return 0
>     if k >= n // 2:
>         return sum(max(0, prices[i] - prices[i-1]) for i in range(1, n))
>     dp = [0] * n
>     for _ in range(k):
>         new_dp, best = [0] * n, -prices[0]
>         for i in range(1, n):
>             new_dp[i] = max(new_dp[i-1], prices[i] + best)
>             best = max(best, dp[i] - prices[i])
>         dp = new_dp
>     return dp[-1]
> ```

> [!success] Complexity
> Time O(n) for I/II/III; O(kn) for IV. Space O(1) for I/II/III; O(n) for IV.

---

### Best Time to Buy and Sell Stock with Cooldown (LC 309) `🎯 T2`

> [!example] Problem
> Unlimited transactions; after selling you must rest 1 day before buying again. **Medium.**
>
> ```
> Input: [1,2,3,0,2]  →  3   (buy, sell, cooldown, buy, sell)
> ```

> [!tip] Recognize · Gotcha
> **Signal:** "cooldown" / "must wait after selling" → state machine · **Gotcha:** update all three states from the **previous** day's values (tuple assignment) — sequential updates leak today's sale into today's buy.

> [!info] Approach
> Three states model the constraint: holding, just sold (cooldown), resting. Transitions connect states across days. `held` = best profit when holding; `sold` = best on day of sell; `rest` = best when not holding and not in cooldown. `held = max(held, rest - price)`, `sold = held + price`, `rest = max(rest, sold)`.

> [!note]- Python Solution
> ```python
> def max_profit(prices):
>     held, sold, rest = float('-inf'), 0, 0
>     for p in prices:
>         held, sold, rest = max(held, rest - p), held + p, max(rest, sold)
>     return max(sold, rest)
> ```

> [!success] Complexity
> Time O(n), Space O(1).

---

### Stock with Transaction Fee

> [!example] Problem
> Unlimited transactions; fixed `fee` per sell.

> [!info] Approach
> Two states: `hold` (best profit holding), `cash` (best profit not holding). `hold = max(hold, cash - price)`, `cash = max(cash, hold + price - fee)`.

> [!note]- Python Solution
> ```python
> def max_profit(prices, fee):
>     hold, cash = float('-inf'), 0
>     for p in prices:
>         hold, cash = max(hold, cash - p), max(cash, hold + p - fee)
>     return cash
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Apply fee on buy side: `cash - p - fee` when buying. Equivalent result.

---

### Best Time to Buy and Sell Stock IV (LC 188) `🎯 T2`

> [!example] Problem
> Given `prices` and integer `k`, return the max profit with at most `k` transactions (buy then sell, no overlapping). [H]

> [!tip] Recognize · Gotcha
> **Signal:** Stock with a transaction cap · **Gotcha:** If `k >= n // 2` the cap never binds — fall back to the unlimited-transactions sum of positive differences (also avoids allocating huge `k`-sized arrays).

> [!info] Approach
> Two states per transaction count `t`: `hold[t]` = best cash while holding a stock, having used `t` buys; `sold[t]` = best cash with `t` completed transactions. Per price `p`: `hold[t] = max(hold[t], sold[t-1] - p)`, `sold[t] = max(sold[t], hold[t] + p)`. Because `hold[t]` is updated first and reads only `sold[t-1]` (from a lower `t`, already updated for this day), a same-day buy-and-sell just adds `0` and is harmless.

> [!note]- Python Solution
> ```python
> def max_profit_k(k, prices):
>     n = len(prices)
>     if n < 2 or k == 0:
>         return 0
>     if k >= n // 2:
>         return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, n))
>     hold = [float('-inf')] * (k + 1)
>     sold = [0] * (k + 1)
>     for p in prices:
>         for t in range(1, k + 1):
>             hold[t] = max(hold[t], sold[t - 1] - p)
>             sold[t] = max(sold[t], hold[t] + p)
>     return sold[k]
> ```

> [!success] Complexity
> Time O(n · k), Space O(k).

> [!tip] Alternatives
> `dp[t][i]` 2D form with a running `max(dp[t-1][j] - prices[j])`. Generalizes LC 121 (`k=1`), LC 123 (`k=2`), LC 122 (`k=∞`).

---

## Longest Increasing Subsequence (LIS) Family

---

### Longest Increasing Subsequence `⚡ T1`

> [!example] Problem
> Given an integer array nums, return the length of the longest strictly increasing subsequence.
> 
> **Example 1:**
> ```
> Input: nums = [10,9,2,5,3,7,101,18]
> Output: 4
> Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,1,0,3,2,3]
> Output: 4
> ```
> 
> **Example 3:**
> ```
> Input: nums = [7,7,7,7,7,7,7]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2500
> - -10^4 <= nums[i] <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** LIS O(n log n) · **Gotcha:** **Strictly** increasing vs **non-decreasing** changes binary search.

> [!failure] Tempting wrong approach
> Greedy "extend if larger than the last taken" — `[3,4,1,2,3]` gives 2, true LIS is 3. Use O(n²) DP or patience sorting (O(n log n)).

> [!info] Approach
> Naïve O(n²) DP checks all prior elements; patience sort uses a maintained tails array to binary-search the right position, achieving O(n log n). `tails[i]` = smallest tail element of all increasing subsequences of length `i+1` seen so far. For each `x` in `nums`, binary search `tails` for the first element `>= x`. If found, replace it with `x`; otherwise append `x`. Answer = `len(tails)`.

> [!note]- Python Solution
> ```python
> import bisect
> def length_of_lis(nums):
>     tails = []
>     for x in nums:
>         pos = bisect.bisect_left(tails, x)
>         if pos == len(tails):
>             tails.append(x)
>         else:
>             tails[pos] = x
>     return len(tails)
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> O(n²) DP: `dp[i] = max(dp[j]+1 for j<i if nums[j]<nums[i])`. To reconstruct the actual subsequence, maintain a `parent` array alongside the patience sort.

---

### Number of LIS

> [!example] Problem
> Given `nums`, return the number of longest increasing subsequences (LC 673).

> [!info] Approach
> Length alone isn't enough; need to count paths. Two parallel arrays track both. `length[i]` = LIS length ending at index `i`. `count[i]` = number of such subsequences. For each `i`, scan `j < i`. If `nums[j] < nums[i]`: if `length[j]+1 > length[i]`, update both; if equal, add `count[j]` to `count[i]`. Answer = sum of `count[i]` where `length[i] == max_length`.

> [!note]- Python Solution
> ```python
> def find_number_of_lis(nums):
>     n = len(nums)
>     length = [1] * n
>     count = [1] * n
>     for i in range(n):
>         for j in range(i):
>             if nums[j] < nums[i]:
>                 if length[j] + 1 > length[i]:
>                     length[i] = length[j] + 1
>                     count[i] = count[j]
>                 elif length[j] + 1 == length[i]:
>                     count[i] += count[j]
>     max_len = max(length)
>     return sum(c for l, c in zip(length, count) if l == max_len)
> ```

> [!success] Complexity
> Time O(n²), Space O(n).

> [!tip] Alternatives
> O(n log n) with a BIT/segment tree storing (max_length, count) pairs per compressed value.

---

## String DP

---

### Distinct Subsequences `🎯 T2`

> [!example] Problem
> Given two strings s and t, return the number of distinct subsequences of s which equals t.
> The test cases are generated so that the answer fits on a 32-bit signed integer.
> 
> **Example 1:**
> ```
> Input: s = "rabbbit", t = "rabbit"
> Output: 3
> Explanation:
> As shown below, there are 3 ways you can generate "rabbit" from s.
> rabbbit
> rabbbit
> rabbbit
> ```
> 
> **Example 2:**
> ```
> Input: s = "babgbag", t = "bag"
> Output: 5
> Explanation:
> As shown below, there are 5 ways you can generate "bag" from s.
> babgbag
> babgbag
> babgbag
> babgbag
> babgbag
> ```
> 
> **Constraints:**
> - 1 <= s.length, t.length <= 1000
> - s and t consist of English letters.

> [!tip] Recognize · Gotcha
> **Signal:** Add ways when chars match · **Gotcha:** `dp[i][0] = 1` (empty t always subseq)

> [!info] Approach
> At each position we either use `s[i]` to match `t[j]` or we skip it; both branches must be counted. `dp[i][j]` = number of ways to form `t[:j]` from `s[:i]`. If `s[i-1] == t[j-1]`: `dp[i][j] = dp[i-1][j-1] + dp[i-1][j]` (use or skip). Else: `dp[i][j] = dp[i-1][j]`. Base: `dp[i][0] = 1` for all `i`.

> [!note]- Python Solution
> ```python
> def num_distinct(s, t):
>     m, n = len(s), len(t)
>     dp = [0] * (n + 1)
>     dp[0] = 1
>     for ch in s:
>         for j in range(n, 0, -1):
>             if ch == t[j - 1]:
>                 dp[j] += dp[j - 1]
>     return dp[n]
> ```

> [!success] Complexity
> Time O(mn), Space O(n) with 1-D rolling array.

> [!tip] Alternatives
> Full 2-D table is clearer for derivation; rolling array suffices for space optimization.

---

### Interleaving String `🎯 T2`

> [!example] Problem
> Given strings s1, s2, and s3, find whether s3 is formed by an interleaving of s1 and s2.
> An interleaving of two strings s and t is a configuration where s and t are divided into n and m substrings respectively, such that:
> Note: a + b is the concatenation of strings a and b.
> 
> **Example 1:**
> ```
> Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
> Output: true
> Explanation: One way to obtain s3 is:
> Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
> Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
> Since s3 can be obtained by interleaving s1 and s2, we return true.
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
> Output: false
> Explanation: Notice how it is impossible to interleave s2 with any other string to obtain s3.
> ```
> 
> **Example 3:**
> ```
> Input: s1 = "", s2 = "", s3 = ""
> Output: true
> ```
> 
> **Constraints:**
> - 0 <= s1.length, s2.length <= 100
> - 0 <= s3.length <= 200
> - s1, s2, and s3 consist of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** Two sources for each `s3` char · **Gotcha:** Check `m+n == len(s3)` first

> [!info] Approach
> At each position in `s3` we choose whether the next character comes from `s1` or `s2`; overlapping subproblems arise. `dp[i][j]` = true if `s3[:i+j]` can be formed from `s1[:i]` and `s2[:j]`. `dp[i][j] = (dp[i-1][j] and s1[i-1]==s3[i+j-1]) or (dp[i][j-1] and s2[j-1]==s3[i+j-1])`. Base: `dp[0][0] = True`.

> [!note]- Python Solution
> ```python
> def is_interleave(s1, s2, s3):
>     m, n = len(s1), len(s2)
>     if m + n != len(s3):
>         return False
>     dp = [False] * (n + 1)
>     dp[0] = True
>     for j in range(1, n + 1):
>         dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
>     for i in range(1, m + 1):
>         dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
>         for j in range(1, n + 1):
>             dp[j] = (dp[j] and s1[i-1] == s3[i+j-1]) or \
>                     (dp[j-1] and s2[j-1] == s3[i+j-1])
>     return dp[n]
> ```

> [!success] Complexity
> Time O(mn), Space O(n).

> [!tip] Alternatives
> BFS/DFS with memoization on `(i, j)` state is equivalent and sometimes clearer.

---

### Regular Expression Matching

> [!example] Problem
> Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where:
> The matching should cover the entire input string (not partial).
> 
> **Example 1:**
> ```
> Input: s = "aa", p = "a"
> Output: false
> Explanation: "a" does not match the entire string "aa".
> ```
> 
> **Example 2:**
> ```
> Input: s = "aa", p = "a*"
> Output: true
> Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".
> ```
> 
> **Example 3:**
> ```
> Input: s = "ab", p = ".*"
> Output: true
> Explanation: ".*" means "zero or more (*) of any character (.)".
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 20
> - 1 <= p.length <= 20
> - s contains only lowercase English letters.
> - p contains only lowercase English letters, '.', and '*'.
> - It is guaranteed for each appearance of the character '*', there will be a previous valid character to match.

> [!tip] Recognize · Gotcha
> **Signal:** `*` = zero-or-more of PRECEDING char · **Gotcha:** Base case: leading `a*b*` matches `""`

> [!info] Approach
> `*` introduces branching — match zero occurrences (skip pattern pair) or one-or-more — creating overlapping sub-problems. `dp[i][j]` = true if `s[:i]` matches `p[:j]`. If `p[j-1] == '*'`: `dp[i][j] = dp[i][j-2]` (zero uses) or `(dp[i-1][j] and (p[j-2]=='.' or p[j-2]==s[i-1]))` (one+ uses). Else: `dp[i][j] = dp[i-1][j-1] and (p[j-1]=='.' or p[j-1]==s[i-1])`.

> [!note]- Python Solution
> ```python
> def is_match(s, p):
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(2, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 2]
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] == '*':
>                 dp[i][j] = dp[i][j - 2] or \
>                     (dp[i - 1][j] and p[j - 2] in {'.', s[i - 1]})
>             else:
>                 dp[i][j] = dp[i - 1][j - 1] and p[j - 1] in {'.', s[i - 1]}
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(mn), Space O(mn); reducible to O(n) with two rows.

> [!tip] Alternatives
> LC 44 (Wildcard Matching) replaces `*` semantics — similar structure but `*` matches any sequence directly.

---

### Wildcard Matching (LC 44) `🎯 T2`

> [!example] Problem
> Implement matching of `s` against pattern `p` with `?` (any single char) and `*` (any sequence, including empty). The match must cover the entire string. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Pattern match with free-standing `*` · **Gotcha:** Unlike regex (LC 10), `*` here is not tied to the preceding character. Initialize `dp[0][j] = dp[0][j-1]` when `p[j-1] == '*'` so leading stars match the empty string.

> [!info] Approach
> `dp[i][j]` = `s[:i]` matches `p[:j]`. If `p[j-1] == '*'`: either the star matches empty (`dp[i][j-1]`) or consumes `s[i-1]` and stays available (`dp[i-1][j]`). If `p[j-1]` is `?` or equals `s[i-1]`: `dp[i][j] = dp[i-1][j-1]`. Otherwise false.

> [!note]- Python Solution
> ```python
> def is_match_wild(s, p):
>     m, n = len(s), len(p)
>     dp = [[False] * (n + 1) for _ in range(m + 1)]
>     dp[0][0] = True
>     for j in range(1, n + 1):
>         if p[j - 1] == '*':
>             dp[0][j] = dp[0][j - 1]
>     for i in range(1, m + 1):
>         for j in range(1, n + 1):
>             if p[j - 1] == '*':
>                 dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
>             elif p[j - 1] == '?' or p[j - 1] == s[i - 1]:
>                 dp[i][j] = dp[i - 1][j - 1]
>     return dp[m][n]
> ```

> [!success] Complexity
> Time O(m · n), Space O(m · n) (rollable to O(n)).

> [!tip] Alternatives
> Two-pointer greedy with backtracking to the last `*` is O(m · n) worst case but O(1) space — often what interviewers want as a follow-up.

---

## Bitmask DP

---

### Partition to K Equal Subset Sums `🎯 T2`

> [!example] Problem
> Given `nums` and integer `k`, return true if the array can be partitioned into `k` subsets each with equal sum (LC 698).

> [!tip] Recognize · Gotcha
> **Signal:** "Can array be split into K equal-sum subsets?" · **Gotcha:** Sort descending first — places large elements first and prunes faster. Skip identical-value buckets at same depth.

> [!info] Approach
> Subset assignment is NP-hard in general but `n ≤ 16` makes 2^n bitmask DP feasible. `dp[mask]` = true if the elements indicated by `mask` can be perfectly distributed into some number of full buckets. `target = total / k`. Iterate all masks in order. For each set mask, compute `current_sum = sum of selected elements % target`. Try adding each unselected element; if it fits, `dp[mask | (1<<i)] = True`. Answer = `dp[(1<<n)-1]`.

> [!note]- Python Solution
> ```python
> def can_partition_k_subsets(nums, k):
>     total = sum(nums)
>     if total % k:
>         return False
>     target = total // k
>     nums.sort(reverse=True)
>     if nums[0] > target:
>         return False
>     n = len(nums)
>     dp = [False] * (1 << n)
>     dp[0] = True
>     current_sum = [0] * (1 << n)
>     for mask in range(1 << n):
>         if not dp[mask]:
>             continue
>         for i in range(n):
>             if mask & (1 << i):
>                 continue
>             next_mask = mask | (1 << i)
>             if current_sum[mask] + nums[i] <= target:
>                 current_sum[next_mask] = (current_sum[mask] + nums[i]) % target
>                 dp[next_mask] = True
>     return dp[(1 << n) - 1]
> ```

> [!success] Complexity
> Time O(2^n · n), Space O(2^n).

> [!tip] Alternatives
> Backtracking with pruning often faster in practice. Bitmask DP guarantees polynomial in 2^n so preferred when n ≤ 20.

---

### Smallest Sufficient Team (LC 1125) `💤 T3`

> [!example] Problem
> Given `req_skills` (≤ 16) and `people` (each a list of skills), return indices of the smallest team that covers all required skills. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Set cover with a small universe · **Gotcha:** Bitmask the *skills*, not the people (people can be 60). Skip people with zero required skills.

> [!info] Approach
> `dp[mask]` = smallest list of people whose combined skills equal `mask`. Start `dp = {0: []}`. For each person with skill mask `pm`, for each existing `(mask, team)`: `dp[mask | pm]` becomes `team + [p]` if absent or strictly shorter. Iterate over a snapshot (`list(dp.items())`) so the same person is not used twice in a pass. Answer `dp[full]`.

> [!note]- Python Solution
> ```python
> def smallest_sufficient_team(req_skills, people):
>     idx = {s: i for i, s in enumerate(req_skills)}
>     full = (1 << len(req_skills)) - 1
>     dp = {0: []}
>     for p, skills in enumerate(people):
>         pm = 0
>         for s in skills:
>             pm |= 1 << idx[s]
>         if pm == 0:
>             continue
>         for mask, team in list(dp.items()):
>             nm = mask | pm
>             if nm not in dp or len(dp[nm]) > len(team) + 1:
>                 dp[nm] = team + [p]
>     return dp[full]
> ```

> [!success] Complexity
> Time O(P · 2^S), Space O(2^S · S) where S = skills, P = people.

> [!tip] Alternatives
> Backtracking over uncovered skills with pruning; or min-sessions style `dp[mask]` array of ints with parent pointers to save memory.

---

## DP on Sequences

---

### Jump Game II `🎯 T2`

> Full walkthrough: [Jump Game II (minimum jumps)](16-greedy.md#jump-game-ii-minimum-jumps--t2).

---

### Maximum Product Subarray `🎯 T2`

> [!example] Problem
> Given an integer array nums, find a subarray that has the largest product, and return the product.
> The test cases are generated so that the answer will fit in a 32-bit integer.
> 
> **Example 1:**
> ```
> Input: nums = [2,3,-2,4]
> Output: 6
> Explanation: [2,3] has the largest product 6.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [-2,0,-1]
> Output: 0
> Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - -10 <= nums[i] <= 10
> - The product of any subarray of nums is guaranteed to fit in a 32-bit integer.

> [!info] Approach
> A negative number flips max↔min, so both must be tracked at each position. `max_prod` and `min_prod` ending at index `i`. At each element `x`: `max_prod, min_prod = max(x, max_prod*x, min_prod*x), min(x, max_prod*x, min_prod*x)`. Update global answer with `max_prod`.

> [!note]- Python Solution
> ```python
> def max_product(nums):
>     max_p = min_p = result = nums[0]
>     for x in nums[1:]:
>         candidates = (x, max_p * x, min_p * x)
>         max_p, min_p = max(candidates), min(candidates)
>         result = max(result, max_p)
>     return result
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Prefix product with reset at zeros; or observe the answer is always a prefix or suffix product between zeros.

---

### Longest Common Substring

> [!example] Problem
> Find the length of the longest common contiguous substring shared by two strings.

> [!info] Approach
> Unlike LCS, contiguity matters. A mismatch breaks the chain, so the DP state must reset to zero on mismatch. `dp[i][j]` is the length of the longest common substring ending at `s1[i-1]` and `s2[j-1]`. If characters match, extend the diagonal: `dp[i][j] = dp[i-1][j-1] + 1`; else `dp[i][j] = 0`. Track the global maximum.

> [!note]- Python Solution
> ```python
> def longest_common_substring(s1, s2):
>     m, n = len(s1), len(s2)
>     prev = [0] * (n + 1)
>     best = 0
>     for i in range(1, m + 1):
>         cur = [0] * (n + 1)
>         for j in range(1, n + 1):
>             if s1[i - 1] == s2[j - 1]:
>                 cur[j] = prev[j - 1] + 1
>                 best = max(best, cur[j])
>         prev = cur
>     return best
> ```

> [!success] Complexity
> O(mn) time, O(n) space with row compression.

> [!tip] Alternatives
> Suffix automaton or suffix array can solve richer substring problems faster, but DP is the clean interview answer.

---

### Russian Doll Envelopes (LC 354)

> [!example] Problem
> You are given a 2D array of integers envelopes where envelopes[i] = [wi, hi] represents the width and the height of an envelope.
> One envelope can fit into another if and only if both the width and height of one envelope are greater than the other envelope's width and height.
> Return the maximum number of envelopes you can Russian doll (i.e., put one inside the other).
> Note: You cannot rotate an envelope.
> 
> **Example 1:**
> ```
> Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
> Output: 3
> Explanation: The maximum number of envelopes you can Russian doll is 3 ([2,3] => [5,4] => [6,7]).
> ```
> 
> **Example 2:**
> ```
> Input: envelopes = [[1,1],[1,1],[1,1]]
> Output: 1
> ```
> 
> **Constraints:**
> - 1 <= envelopes.length <= 10^5
> - envelopes[i].length == 2
> - 1 <= wi, hi <= 10^5

> [!tip] Recognize · Gotcha
> **Signal:** 2D nesting · **Gotcha:** Descending `h` blocks equal widths nesting

> [!info] Approach
> If we sort by width, this becomes LIS on heights. But with equal widths, we can't include two envelopes (a wider envelope can't fit inside one of the same width). Fix: sort by `(width asc, height desc)` — the descending height ensures equal-width envelopes can never form an increasing subsequence. Sort by `(w asc, h desc)`. Extract heights. Run patience sort (O(n log n) LIS) on heights. `bisect_left` on the `tails` array — same as LC 300 LIS.

> [!note]- Python Solution
> ```python
> import bisect
> >
> def max_envelopes(envelopes):
>     envelopes.sort(key=lambda x: (x[0], -x[1]))
>     tails = []
>     for _, h in envelopes:
>         pos = bisect.bisect_left(tails, h)
>         if pos == len(tails):
>             tails.append(h)
>         else:
>             tails[pos] = h
>     return len(tails)
> ```

> [!success] Complexity
> Time O(n log n), Space O(n).

> [!tip] Alternatives
> - O(n²) DP: for each envelope, check all previous ones and extend. Too slow for large inputs (n up to 10^5).
> - Key trick: the `(w asc, h desc)` sort is the entire insight — without it, equal-width envelopes would incorrectly contribute to the LIS.

---

### Maximum Profit in Job Scheduling `🎯 T2`

> [!example] Problem
> Given jobs as `(startTime, endTime, profit)`, pick non-overlapping jobs maximizing total profit. Jobs ending at t and starting at t don't overlap.

> [!info] Approach
> Weighted interval scheduling — greedy fails because profits are arbitrary, so it's DP. Sort jobs by **end time**; let `dp[i]` = best profit using the first i jobs. For job i: skip it (`dp[i-1]`) or take it (`profit + dp[j]` where j = count of jobs ending `≤ start_i`, found with `bisect_right` on the sorted ends). The DP + binary-search composition is exactly the "combine two T1 patterns" move Google L4 rounds test.

> [!note]- Python Solution
> ```python
> import bisect
> >
> def jobScheduling(startTime, endTime, profit):
>     jobs = sorted(zip(endTime, startTime, profit))
>     ends = [e for e, _, _ in jobs]
>     dp = [0] * (len(jobs) + 1)
>     for i, (e, s, p) in enumerate(jobs):
>         j = bisect.bisect_right(ends, s, 0, i)
>         dp[i + 1] = max(dp[i], dp[j] + p)
>     return dp[-1]
> ```

> [!success] Complexity
> Time O(n log n); Space O(n).

> [!warning] Gotcha
> `bisect_right` (not `bisect_left`) because a job ending exactly at `s` is compatible. Limit the search to `[0, i)` — searching the whole array can "find" the current job. State the greedy counter-example (one long high-profit job vs many short ones) before writing the DP.

---

### Super Egg Drop (LC 887) `💤 T3`

> [!example] Problem
> With `k` eggs and a building of `n` floors, find the minimum number of moves (egg drops) that guarantees finding the critical floor in the worst case. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Min-max over a split point; `n` up to 10⁴ kills the O(k·n²) DP · **Gotcha:** Flip the question: with `m` moves and `e` eggs, how many floors can you resolve? Then the answer is the smallest `m` reaching `n`.

> [!info] Approach
> `f(m, e) = f(m-1, e-1) + f(m-1, e) + 1`: drop from some floor; if the egg breaks, `f(m-1, e-1)` floors below are resolvable; if not, `f(m-1, e)` above; plus the tested floor. Keep a 1-D array over `e` updated in place from high `e` to low (so `dp[e-1]` is still the previous move's value). Increase `moves` until `dp[k] >= n`.

> [!note]- Python Solution
> ```python
> def super_egg_drop(k, n):
>     dp = [0] * (k + 1)
>     moves = 0
>     while dp[k] < n:
>         moves += 1
>         for e in range(k, 0, -1):
>             dp[e] = dp[e] + dp[e - 1] + 1
>     return moves
> ```

> [!success] Complexity
> Time O(k · moves) where moves ≤ n (≈ log n for large k), Space O(k).

> [!tip] Alternatives
> `dp[e][n]` with binary search on the drop floor (the break and survive terms are monotone): O(k · n log n). State the O(k·n²) version first, then optimize.

---

### Minimum Number of Refueling Stops (LC 871) `🎯 T2`

> [!example] Problem
> Car starts with `startFuel`, 1 fuel per mile. `stations[i] = [position, fuel]`. Return the fewest stops to reach `target`, or `-1`. [H]

> [!tip] Recognize · Gotcha
> **Signal:** "Fewest refuels" with reachable-range growth · **Gotcha:** Don't decide at a station whether to stop; decide **retroactively** — when you run out, fill from the largest station you already passed.

> [!info] Approach
> **Greedy/heap view:** drive through stations, pushing each station's fuel into a max-heap. When fuel goes negative, pop the largest fuel seen so far (as if you stopped there) and count a stop; if the heap empties while still negative, return `-1`. Append `[target, 0]` as a final station.
> **DP view:** `dp[k]` = farthest distance reachable with exactly `k` stops. For each station (in order), for `k` from high to low: if `dp[k] >= pos`, `dp[k+1] = max(dp[k+1], dp[k] + fuel)`. Answer is the smallest `k` with `dp[k] >= target`.

> [!note]- Python Solution
> ```python
> import heapq
>
> def min_refuel_stops(target, start_fuel, stations):
>     heap = []
>     fuel, stops, prev = start_fuel, 0, 0
>     for pos, cap in stations + [[target, 0]]:
>         fuel -= pos - prev
>         while fuel < 0 and heap:
>             fuel += -heapq.heappop(heap)
>             stops += 1
>         if fuel < 0:
>             return -1
>         heapq.heappush(heap, -cap)
>         prev = pos
>     return stops
> ```

> [!success] Complexity
> Heap: Time O(n log n), Space O(n). DP: Time O(n²), Space O(n).

> [!tip] Alternatives
> In interviews, present the O(n²) DP first (shows the state), then the heap as the optimization — both are accepted.

---

## Interval DP

---

### Matrix Chain Multiplication

> [!example] Problem
> Given a sequence of matrices with dimensions `dims[i-1] × dims[i]`, find the minimum number of scalar multiplications to compute their product.

> [!info] Approach
> The order of multiplication matters. Interval DP: `dp[i][j]` = minimum cost to multiply matrices `i` through `j`. Split at every `k` from `i` to `j-1`. `dp[i][j] = min over k in [i, j-1] of dp[i][k] + dp[k+1][j] + dims[i-1] * dims[k] * dims[j]`. Fill by increasing interval length (length 1 has cost 0). Outer loop: `length` from 2 to n. Inner loops: `i`, then `k`.

> [!note]- Python Solution
> ```python
> def matrix_chain_order(dims):
>     n = len(dims) - 1
>     dp = [[0] * n for _ in range(n)]
>     for length in range(2, n + 1):
>         for i in range(n - length + 1):
>             j = i + length - 1
>             dp[i][j] = float('inf')
>             for k in range(i, j):
>                 cost = dp[i][k] + dp[k+1][j] + dims[i] * dims[k+1] * dims[j+1]
>                 dp[i][j] = min(dp[i][j], cost)
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> - Top-down with a memo dict on `(i, j)` — same asymptotic, easy to explain in an interview.
> - Pattern: this is the canonical "interval DP" template. Also appears in: burst balloons, remove boxes, strange printer.

---

### Burst Balloons (LC 312) `🎯 T2`

> [!example] Problem
> Given `n` balloons with values `nums[i]`, bursting balloon `i` earns `nums[left] * nums[i] * nums[right]` coins (adjacent *remaining* balloons). Maximize total coins after bursting all balloons. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Interval DP · **Gotcha:** **Multiply** `nums[i]*nums[k]*nums[j]` — **add** boundary 1s as sentinels.

> [!info] Approach
> Thinking forward ("which balloon do I burst first?") fails because bursting changes adjacency unpredictably. Think **backward**: fix which balloon `k` is burst **last** in the open interval `(i, j)`. When `k` is last, its neighbors are the fixed boundaries `i` and `j`, so it earns `nums[i] * nums[k] * nums[j]`. Pad the array with 1s on both ends. `dp[i][j]` = max coins from bursting everything strictly between `i` and `j`: `dp[i][j] = max over k in (i, j) of dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j]`. Fill by increasing interval length.

> [!note]- Python Solution
> ```python
> def max_coins(nums):
>     nums = [1] + nums + [1]
>     n = len(nums)
>     dp = [[0] * n for _ in range(n)]
>     for length in range(2, n):          # gap between i and j
>         for i in range(n - length):
>             j = i + length
>             for k in range(i + 1, j):   # k burst last in (i, j)
>                 dp[i][j] = max(dp[i][j],
>                                dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
>     return dp[0][n-1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> - Key insight to state in interview: "last burst" makes subproblems independent — "first burst" does not.
> - Same last-action-in-interval trick: Remove Boxes (LC 546), Strange Printer (LC 664), Minimum Cost to Merge Stones — all `💤 T3` at L3.

---

### Minimum Cost to Cut a Stick (LC 1547) `🎯 T2`

> [!example] Problem
> A stick of length `n` must be cut at the positions in `cuts`. Each cut costs the current length of the piece being cut. Return the minimum total cost over all orderings. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Order of operations matters and each op splits a range into independent halves · **Gotcha:** Sort `cuts` and add `0` and `n` as sentinels; `dp[i][j]` is over indices in this list, with cost `c[j] - c[i]` for the piece between them.

> [!info] Approach
> Think about the **first** cut in segment `(i, j)`: it costs `c[j] - c[i]` and leaves independent segments `(i, k)` and `(k, j)`. `dp[i][j] = (c[j] - c[i]) + min over k in (i, j) of dp[i][k] + dp[k][j]`, with `dp[i][i+1] = 0`. Fill by increasing gap. Same shape as Burst Balloons (with "first" instead of "last" because costs depend on the segment's ends, which are fixed).

> [!note]- Python Solution
> ```python
> def min_cost_cut(n, cuts):
>     c = [0] + sorted(cuts) + [n]
>     m = len(c)
>     dp = [[0] * m for _ in range(m)]
>     for length in range(2, m):
>         for i in range(m - length):
>             j = i + length
>             dp[i][j] = (c[j] - c[i]) + min(dp[i][k] + dp[k][j]
>                                           for k in range(i + 1, j))
>     return dp[0][m - 1]
> ```

> [!success] Complexity
> Time O(m³), Space O(m²) where m = len(cuts) + 2.

> [!tip] Alternatives
> Same structure as Matrix Chain Multiplication and Minimum Cost to Merge Stones (LC 1000, `💤 T3`).

---

### Strange Printer (LC 664) `💤 T3`

> [!example] Problem
> A printer prints one repeated character in a contiguous range per turn, overwriting what is there. Return the min turns to print string `s`. [H]

> [!tip] Recognize · Gotcha
> **Signal:** Range overwrites; minimizing operations on a string · **Gotcha:** Compress consecutive duplicates first. For `s[j]`, either print it alone (`dp[i][j-1] + 1`) or extend the print that produced an earlier equal character `s[k]`.

> [!info] Approach
> `dp[i][j]` = min turns for `s[i..j]`. Default: `dp[i][j-1] + 1`. For each `k` in `[i, j)` with `s[k] == s[j]`, the stroke that prints `s[k]` can also cover `s[j]` for free, so `dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j-1])` (second term is 0 when empty). Fill `i` downward, `j` upward.

> [!note]- Python Solution
> ```python
> def strange_printer(s):
>     s = "".join(ch for i, ch in enumerate(s) if i == 0 or s[i - 1] != ch)
>     n = len(s)
>     if n == 0:
>         return 0
>     dp = [[0] * n for _ in range(n)]
>     for i in range(n - 1, -1, -1):
>         dp[i][i] = 1
>         for j in range(i + 1, n):
>             dp[i][j] = dp[i][j - 1] + 1
>             for k in range(i, j):
>                 if s[k] == s[j]:
>                     dp[i][j] = min(dp[i][j],
>                                    dp[i][k] + (dp[k + 1][j - 1] if k + 1 <= j - 1 else 0))
>     return dp[0][n - 1]
> ```

> [!success] Complexity
> Time O(n³), Space O(n²).

> [!tip] Alternatives
> Remove Boxes (LC 546, `💤 T3`) uses the same "merge equal characters across a gap" idea with an extra state for the count of attached boxes.

---

## Game Theory (Minimax) DP

### Predict the Winner / Stone Game (LC 486 / 877) `🎯 T2`

> [!example] Problem
> Players alternately take a number from either end of `nums`. Player 1 starts. Return true if Player 1 can win (a tie counts as a win) with optimal play. (LC 877 Stone Game is the even-length special case where Alice always wins.) [M]

> [!tip] Recognize · Gotcha
> **Signal:** "Both players play optimally" over a shrinking range · **Gotcha:** Store the score **difference** for the player to move; `nums[i] - dp[i+1][j]` — subtract, don't add, because the opponent moves next.

> [!info] Approach
> `dp[i][j]` = best (mine − theirs) on `nums[i..j]` for the mover. Take left: `nums[i] - dp[i+1][j]`; take right: `nums[j] - dp[i][j-1]`. Player 1 wins iff `dp[0][n-1] >= 0`. Rolling over `i` descending lets one 1-D array hold row `i`: `dp[j]` before update is `dp[i+1][j]`, `dp[j-1]` is already `dp[i][j-1]`.

> [!note]- Python Solution
> ```python
> def predict_the_winner(nums):
>     n = len(nums)
>     dp = nums[:]
>     for i in range(n - 2, -1, -1):
>         for j in range(i + 1, n):
>             dp[j] = max(nums[i] - dp[j], nums[j] - dp[j - 1])
>     return dp[n - 1] >= 0
> ```

> [!success] Complexity
> Time O(n²), Space O(n).

> [!tip] Alternatives
> LC 877: `return True` (even length ⇒ first player can force taking all odd- or all even-indexed piles). Mention it, then show the DP.

---

### Stone Game II (LC 1140) `🎯 T2`

> [!example] Problem
> Piles in a row. Alice then Bob alternately take the first `X` piles where `1 <= X <= 2M`, then `M = max(M, X)`. Start `M = 1`. Return the max stones Alice can get. [M]

> [!tip] Recognize · Gotcha
> **Signal:** Take-from-front game where the allowed move size grows · **Gotcha:** State needs `M`. Use suffix sums: `best(i, M)` = most stones the mover collects from `piles[i:]`; the opponent then gets `best(i+x, max(M,x))` of the remainder.

> [!info] Approach
> `best(i, m) = suf[i]` when `i + 2m >= n` (take everything). Otherwise `max over x in 1..2m of suf[i] - best(i + x, max(m, x))` — everything remaining minus what the opponent will collect. Memoize on `(i, m)`; `m` is at most `n`.

> [!note]- Python Solution
> ```python
> from functools import lru_cache
>
> def stone_game_ii(piles):
>     n = len(piles)
>     suf = [0] * (n + 1)
>     for i in range(n - 1, -1, -1):
>         suf[i] = suf[i + 1] + piles[i]
>
>     @lru_cache(None)
>     def best(i, m):
>         if i + 2 * m >= n:
>             return suf[i]
>         return max(suf[i] - best(i + x, max(m, x)) for x in range(1, 2 * m + 1))
>
>     return best(0, 1)
> ```

> [!success] Complexity
> Time O(n³) (n·n states × O(n) moves), Space O(n²).

> [!tip] Alternatives
> Bottom-up over `i` descending with a `dp[i][m]` table. Stone Game III (LC 1406) is the same idea with moves 1–3.

---

## Digit DP

### Numbers At Most N Given Digit Set (LC 902) `💤 T3`

> [!example] Problem
> Given a sorted list `digits` of characters `'1'..'9'` and an integer `n`, return how many positive integers `<= n` can be written using only digits from the set (digits reusable). [H]

> [!tip] Recognize · Gotcha
> **Signal:** "Count numbers ≤ N with allowed digits" · **Gotcha:** Two parts: all **shorter** lengths are free (`d^1 + … + d^(L-1)`), then walk N's digits while staying tight. If a digit of N isn't in the set, you can't stay tight — stop. If you survive every digit, add 1 for N itself.

> [!info] Approach
> For each position `i` of N's string `s`: numbers whose first `i` digits match `s` and whose digit `i` is strictly smaller than `s[i]` can fill the remaining `L-i-1` positions freely: `smaller * d^(L-i-1)`. Then require `s[i]` in the set to keep matching; otherwise return the running total. After the loop add 1.

> [!note]- Python Solution
> ```python
> def at_most_n_given_digit_set(digits, n):
>     s, L, d = str(n), len(str(n)), len(digits)
>     total = sum(d ** k for k in range(1, L))
>     for i, ch in enumerate(s):
>         smaller = sum(1 for x in digits if x < ch)
>         total += smaller * d ** (L - i - 1)
>         if ch not in digits:
>             return total
>     return total + 1
> ```

> [!success] Complexity
> Time O(L · d), Space O(1).

> [!tip] Alternatives
> General digit DP `go(pos, tight, started)` — see the lecture's *Digit DP* pattern. Prefer it if the interviewer tweaks the property.

---

### Count Numbers with Unique Digits (LC 357) `🎯 T2`

> [!example] Problem
> Given `n`, count numbers `x` with `0 <= x < 10^n` whose digits are all distinct. [M]

> [!tip] Recognize · Gotcha
> **Signal:** Count with "no repeated digit" · **Gotcha:** First digit has 9 choices (no leading zero), later digits have 9, 8, 7, … because zero becomes available but used digits are removed. `n = 0` returns 1; lengths beyond 10 add nothing (multiplier hits 0).

> [!info] Approach
> Count by length. Length 1: 10 (including 0). Length `L >= 2`: `9 * 9 * 8 * … ` (the last factor is `10 - (L-1)`). Running sum over lengths `1..n`. The multiplicative product is the DP: `cur_L = cur_{L-1} * avail`.

> [!note]- Python Solution
> ```python
> def count_numbers_unique_digits(n):
>     if n == 0:
>         return 1
>     total, cur, avail = 10, 9, 9
>     for _ in range(2, n + 1):
>         cur *= avail
>         avail -= 1
>         total += cur
>     return total
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> Digit-DP with a used-digit bitmask answers "unique digits in `[0, N]`" for arbitrary `N` (LC 1012, `💤 T3`) — see the lecture's `count_no_repeat`.

---
## See Also

[[recursion]] | [[sorting]] | [[binary-search]] | [[graph-algorithms]]
