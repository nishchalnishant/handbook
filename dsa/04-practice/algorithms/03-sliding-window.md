---
tags: [coding, algorithms, sliding-window]
topic: Sliding Window
difficulty: mixed
---
# Sliding Window — Problem Set

## What this covers

> [!abstract] In this file
> **Covers:** Worked sliding-window problems: fixed, at-most-K, exactly-K, minimum length, monotonic deque.
> **You'll be able to:** Write the window template cold and pick the shrink condition correctly.
> **Prereqs:** Sliding-window lecture · **Pair with:** [Sliding-window lecture](../../03-algorithms/03-sliding-window.md) · **Time:** 3–4 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Fixed-Size Window](#fixed-size-window) · [Variable Window — At Most K](#variable-window--at-most-k) · [Variable Window — Exactly K](#variable-window--exactly-k) · [Variable Window — Minimum Length](#variable-window--minimum-length) · [Sliding Window + Monotonic Deque](#sliding-window--monotonic-deque) · [Variable Window — Max Length (Flip / Delete)](#variable-window--max-length-flip--delete) · [More Variable Window Problems](#more-variable-window-problems)

> [!tip] If you only have 20 minutes
> **Do these first:** [Longest Substring Without Repeating Characters](#longest-substring-without-repeating-characters-lc-3--t1) · [Longest Repeating Character Replacement](#longest-repeating-character-replacement-lc-424--t1) · [Minimum Window Substring](#minimum-window-substring-lc-76--t1) · [Permutation in String](#permutation-in-string-lc-567--t1) · [Find All Anagrams in a String](#find-all-anagrams-in-a-string-lc-438--t1) · [Max Consecutive Ones III](#max-consecutive-ones-iii-lc-1004--t1) · [Subarrays with K Different Integers](#subarrays-with-k-different-integers-lc-992--t1) · [Sliding Window Maximum](#sliding-window-maximum-lc-239--t1)
> **Template:** Variable: `for r in range(n): add(a[r]); while invalid(): remove(a[l]); l += 1; best = max(best, r - l + 1)`.
> **Template:** Exactly K = atMost(K) − atMost(K−1). Fixed size: add `a[r]`, drop `a[r-k]` once `r >= k`.
> **Gotchas:** Window only works when shrinking monotonically fixes validity (negatives break sum windows → prefix sums) · Min Window: track `formed` count, not dict equality · Char Replacement: `maxf` never needs decrementing.

---

## Fixed-Size Window

> [!info] Approach
> For a window of exactly size `k`, every slide adds one element on the right and removes one on the left. Maintain state incrementally in O(1) per step rather than recomputing from scratch — reduces O(nk) to O(n).

---

### Find All Anagrams in a String (LC 438) `⚡ T1`

> [!example] Problem
> Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
> 
> **Example 1:**
> ```
> Input: s = "cbaebabacd", p = "abc"
> Output: [0,6]
> Explanation:
> The substring with start index = 0 is "cba", which is an anagram of "abc".
> The substring with start index = 6 is "bac", which is an anagram of "abc".
> ```
> 
> **Example 2:**
> ```
> Input: s = "abab", p = "ab"
> Output: [0,1,2]
> Explanation:
> The substring with start index = 0 is "ab", which is an anagram of "ab".
> The substring with start index = 1 is "ba", which is an anagram of "ab".
> The substring with start index = 2 is "ab", which is an anagram of "ab".
> ```
> 
> **Constraints:**
> - 1 <= s.length, p.length <= 3 * 10^4
> - s and p consist of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** Window size = len(p) · **Gotcha:** Fixed window — slide by one char at a time.

> [!info] Approach
> An anagram is a permutation — same character frequencies, different order. Fixed window of size `len(p)`. Maintain a frequency diff between window and `need`. Track how many characters are "satisfied" with a `matches` counter — avoids O(26) dict comparison each step. On adding `s[right]`: if freq reaches exactly `need[c]` → `matches += 1`. On removing `s[left]`: if freq drops below `need[c]` → `matches -= 1`. When `matches == len(need)` → anagram found.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def find_anagrams(s, p):
>     need = Counter(p)
>     window = {}
>     matches = 0
>     required = len(need)
>     result = []
>     k = len(p)
> 
>     for right in range(len(s)):
>         c = s[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:   # window overflows — remove leftmost
>             lc = s[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             result.append(right - k + 1)
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Compare `Counter` dicts directly each step — O(26) per slide vs O(1) with match counter; both O(n) overall but match counter is cleaner.

---

### Permutation in String (LC 567) `⚡ T1`

> [!example] Problem
> Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.
> In other words, return true if one of s1's permutations is the substring of s2.
> 
> **Example 1:**
> ```
> Input: s1 = "ab", s2 = "eidbaooo"
> Output: true
> Explanation: s2 contains one permutation of s1 ("ba").
> ```
> 
> **Example 2:**
> ```
> Input: s1 = "ab", s2 = "eidboaoo"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s1.length, s2.length <= 10^4
> - s1 and s2 consist of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Gotcha:** Same as anagram; use match-count trick to avoid full comparison

> [!failure] Tempting wrong approach
> Sorting every window (O(n·m log m)), or KMP. It's the same multiset in any order, so use a fixed window with count matching.

> [!info] Approach
> A permutation has the same character frequencies. Fixed window of size `len(s1)` with frequency matching. Same match-counter technique as Find All Anagrams — identical logic, just return True/False. When `matches == required` at any valid window position → return True.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def check_inclusion(s1, s2):
>     if len(s1) > len(s2):
>         return False
>     need = Counter(s1)
>     window = {}
>     matches = 0
>     required = len(need)
>     k = len(s1)
> 
>     for right in range(len(s2)):
>         c = s2[right]
>         window[c] = window.get(c, 0) + 1
>         if c in need and window[c] == need[c]:
>             matches += 1
> 
>         if right >= k:
>             lc = s2[right - k]
>             if lc in need and window[lc] == need[lc]:
>                 matches -= 1
>             window[lc] -= 1
>             if window[lc] == 0:
>                 del window[lc]
> 
>         if right >= k - 1 and matches == required:
>             return True
> 
>     return False
> ```

> [!success] Complexity
> O(n) time where n = len(s2), O(|alphabet|) space.

> [!tip] Alternatives
> Sort both strings per window O(nk log k) — too slow; direct Counter comparison O(n · 26) — correct but slower constant.

---

### Grumpy Bookstore Owner (LC 1052) `⚡ T1`

> [!example] Problem
> There is a bookstore owner that has a store open for n minutes. You are given an integer array customers of length n where customers[i] is the number of the customers that enter the store at the start of the ith minute and all those customers leave after the end of that minute.
> During certain minutes, the bookstore owner is grumpy. You are given a binary array grumpy where grumpy[i] is 1 if the bookstore owner is grumpy during the ith minute, and is 0 otherwise.
> When the bookstore owner is grumpy, the customers entering during that minute are not satisfied. Otherwise, they are satisfied.
> The bookstore owner knows a secret technique to remain not grumpy for minutes consecutive minutes, but this technique can only be used once.
> Return the maximum number of customers that can be satisfied throughout the day.
> 
> **Example 1:**
> ```
> Input: customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3
> Output: 16
> Explanation:
> The bookstore owner keeps themselves not grumpy for the last 3 minutes.
> The maximum number of customers that can be satisfied = 1 + 1 + 1 + 1 + 7 + 5 = 16.
> ```
> 
> **Example 2:**
> ```
> Input: customers = [1], grumpy = [0], minutes = 1
> Output: 1
> ```
> 
> **Constraints:**
> - n == customers.length == grumpy.length
> - 1 <= minutes <= n <= 2 * 10^4
> - 0 <= customers[i] <= 1000
> - grumpy[i] is either 0 or 1.

> [!info] Approach
> Customers at non-grumpy minutes are always satisfied. Customers at grumpy minutes are only satisfied during the technique window. We want to choose the `minutes`-long window that maximises the extra customers gained. Base count = sum of `customers[i]` where `grumpy[i] == 0`. Extra count for a window = sum of `customers[i]` where `grumpy[i] == 1` within the window. Slide a fixed window of size `minutes` to find the maximum extra. Compute base. Slide window: at each step, add `customers[right] * grumpy[right]` and subtract `customers[right - minutes] * grumpy[right - minutes]`. Track max window extra.

> [!note]- Python Solution
> ```python
> def max_satisfied(customers, grumpy, minutes):
>     n = len(customers)
>     base = sum(customers[i] for i in range(n) if grumpy[i] == 0)
>     window_extra = sum(customers[i] * grumpy[i] for i in range(minutes))
>     max_extra = window_extra
>     for i in range(minutes, n):
>         window_extra += customers[i] * grumpy[i]
>         window_extra -= customers[i - minutes] * grumpy[i - minutes]
>         max_extra = max(max_extra, window_extra)
>     return base + max_extra
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Brute force O(n * minutes): slide and recompute the window sum from scratch each step.
> - Key insight: separate "always satisfied" from "sometimes satisfied" — only the grumpy minutes within the window contribute to the extra gain.

**Also try:**

- **Maximum Average Subarray I (LC 643)** — Maximizing average is equivalent to maximizing sum (k is fixed)
- **Number of Sub-arrays of Size K and Average ≥ Threshold (LC 1343)** — Fixed window of size `k`; average ≥ threshold ↔ sum ≥ k * threshold
- **Maximum Sum of Almost Unique Subarray (LC 2841)** — Fixed window of size `k`; track distinct count in the window alongside the running sum
- **Sliding Window Average from Data Stream (LC 346)** — see [Moving Average from Data Stream](../data-structures/06-queue.md#design)
- **Maximum Number of Vowels in a Substring of Given Length** — The window size is fixed, so every move only removes one character and adds one character
- **Minimum Number of Flips to Make Binary String Alternating (LC 1888)** — There are only two valid alternating patterns: "0101..." and "1010..."
- **Diet Plan Performance (LC 1176)** — Straightforward fixed window of size `k`

---

## Variable Window — At Most K

> [!info] Approach
> Expand `right` greedily; when the constraint is violated, shrink `left` until it's satisfied again. Each element enters and exits the window exactly once → O(n) amortized. Window length `right - left + 1` at any valid state is a candidate for the maximum.

---

### Longest Substring Without Repeating Characters (LC 3) `⚡ T1`

> [!example] Problem
> Given a string s, find the length of the longest substring without duplicate characters.
> 
> **Example 1:**
> ```
> Input: s = "abcabcbb"
> Output: 3
> Explanation: The answer is "abc", with the length of 3.
> ```
> 
> **Example 2:**
> ```
> Input: s = "bbbbb"
> Output: 1
> Explanation: The answer is "b", with the length of 1.
> ```
> 
> **Example 3:**
> ```
> Input: s = "pwwkew"
> Output: 3
> Explanation: The answer is "wke", with the length of 3.
> Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
> ```
> 
> **Constraints:**
> - 0 <= s.length <= 5 * 10^4
> - s consists of English letters, digits, symbols and spaces.

> [!tip] Recognize · Gotcha
> **Signal:** Jump `left` past last index of char · **Gotcha:** Only jump if char is **inside** window.

> [!failure] Tempting wrong approach
> On a repeat, `left = last[c] + 1` without `max(left, …)`. If the old occurrence is already outside the window, `left` jumps backward.

> [!info] Approach
> At most 0 duplicate characters per window. Expanding right adds a character; if it duplicates, shrink left past the previous occurrence. Track last-seen index of each character. On duplicate: `left = last_seen[c] + 1` (jump, not step-by-step). Only jump `left` if `last_seen[c] >= left` (character might be outside current window — stale).

> [!note]- Python Solution
> ```python
> def length_of_longest_substring(s):
>     last_seen = {}
>     left = 0
>     best = 0
>     for right, c in enumerate(s):
>         if c in last_seen and last_seen[c] >= left:
>             left = last_seen[c] + 1   # jump past previous occurrence
>         last_seen[c] = right
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(|alphabet|) space.

> [!tip] Alternatives
> Frequency map + step-by-step shrink — also O(n) but more steps; jump optimization is constant-factor faster.

---

### Longest Repeating Character Replacement (LC 424) `⚡ T1`

> [!example] Problem
> You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.
> Return the length of the longest substring containing the same letter you can get after performing the above operations.
> 
> **Example 1:**
> ```
> Input: s = "ABAB", k = 2
> Output: 4
> Explanation: Replace the two 'A's with two 'B's or vice versa.
> ```
> 
> **Example 2:**
> ```
> Input: s = "AABABBA", k = 1
> Output: 4
> Explanation: Replace the one 'A' in the middle with 'B' and form "AABBBBA".
> The substring "BBBB" has the longest repeating letters, which is 4.
> There may exists other ways to achieve this answer too.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of only uppercase English letters.
> - 0 <= k <= s.length

> [!failure] Tempting wrong approach
> Recomputing `maxf` on every shrink in the belief it must drop. A stale `maxf` never yields a wrong answer — the best length only grows when a truly larger `maxf` appears.

> [!info] Approach
> In a window of length `L`, we need `L - max_count <= k` (replace all non-max-frequency characters). Expand while valid; shrink otherwise. Track `max_count` — the frequency of the most common character in the window. When `(window_size - max_count) > k` → shrink. Key insight: `max_count` never needs to decrease (we only care about the *best* window seen so far). When we shrink, `max_count` stays the same, and the window stays the same size or shrinks — we're looking for a *longer* window.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def character_replacement(s, k):
>     freq = defaultdict(int)
>     max_count = 0
>     left = 0
>     best = 0
> 
>     for right, c in enumerate(s):
>         freq[c] += 1
>         max_count = max(max_count, freq[c])
>         # Window invalid: replacements needed exceed k
>         if (right - left + 1) - max_count > k:
>             freq[s[left]] -= 1
>             left += 1   # shrink by 1
>             don't update max_count (intentional)
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(26) = O(1) space.

> [!tip] Alternatives
> Binary search on answer + sliding window validation — O(n log n); direct sliding window is O(n).

---

### Fruits Into Baskets (At Most 2 Distinct) (LC 904) `⚡ T1`

> [!example] Problem
> You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array fruits where fruits[i] is the type of fruit the ith tree produces.
> You want to collect as much fruit as possible. However, the owner has some strict rules that you must follow:
> Given the integer array fruits, return the maximum number of fruits you can pick.
> 
> **Example 1:**
> ```
> Input: fruits = [1,2,1]
> Output: 3
> Explanation: We can pick from all 3 trees.
> ```
> 
> **Example 2:**
> ```
> Input: fruits = [0,1,2,2]
> Output: 3
> Explanation: We can pick from trees [1,2,2].
> If we had started at the first tree, we would only pick from trees [0,1].
> ```
> 
> **Example 3:**
> ```
> Input: fruits = [1,2,3,2,2]
> Output: 4
> Explanation: We can pick from trees [2,3,2,2].
> If we had started at the first tree, we would only pick from trees [1,2].
> ```
> 
> **Constraints:**
> - 1 <= fruits.length <= 10^5
> - 0 <= fruits[i] < fruits.length

> [!info] Approach
> Longest subarray with at most 2 distinct values. Direct application of at-most-K window. Frequency map. While `len(freq) > 2` → shrink left: decrement `freq[s[left]]`; delete key if 0. Window length `right - left + 1` after shrinking is the candidate answer.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def total_fruit(fruits):
>     freq = defaultdict(int)
>     left = 0
>     best = 0
> 
>     for right, f in enumerate(fruits):
>         freq[f] += 1
>         while len(freq) > 2:
>             freq[fruits[left]] -= 1
>             if freq[fruits[left]] == 0:
>                 del freq[fruits[left]]
>             left += 1
>         best = max(best, right - left + 1)
> 
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space (at most 3 keys ever in freq map).

> [!tip] Alternatives
> Identical to "Longest Substring with At Most K Distinct" with k=2.

**Also try:**

- **Longest Substring with At Most K Distinct Characters (LC 340)** — General form of the "at most K distinct" pattern
- **Subarray Product Less Than K (LC 713)** — All elements are positive → product is monotonically non-decreasing as window expands
- **Longest Subarray with Sum ≤ K (Nonnegative)** — Non-negative elements ensure monotone sum — expanding can only increase sum, so shrink-when-violated is valid

---

## Variable Window — Exactly K

> [!info] Approach
> "Exactly K" windows are hard to count directly because shrinking can overshoot. The trick: `exactly(k) = at_most(k) - at_most(k-1)`. Both `at_most` calls are O(n), giving O(n) total.

---

### Subarrays with K Different Integers (LC 992) `⚡ T1`

> [!example] Problem
> Given an integer array nums and an integer k, return the number of good subarrays of nums.
> A good array is an array where the number of different integers in that array is exactly k.
> A subarray is a contiguous part of an array.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1,2,3], k = 2
> Output: 7
> Explanation: Subarrays formed with exactly 2 different integers: [1,2], [2,1], [1,2], [2,3], [1,2,1], [2,1,2], [1,2,1,2]
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,1,3,4], k = 3
> Output: 3
> Explanation: Subarrays formed with exactly 3 different integers: [1,2,1,3], [2,1,3], [1,3,4].
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^4
> - 1 <= nums[i], k <= nums.length

> [!tip] Recognize · Gotcha
> **Signal:** `exactly(K) = atMost(K) - atMost(K-1)` · **Gotcha:** "Exactly K" is not monotonic — never use one sliding window for exactly.

> [!failure] Tempting wrong approach
> A single window counting "exactly K". Several valid `left`s exist for one `right`, so no single shrink rule works. Use `atMost(K) - atMost(K-1)`.

> [!info] Approach
> The "exactly k" constraint is not monotone for a window — adding elements can go over or under. Reframe as difference of two at-most problems. `at_most(k)` counts subarrays with ≤ k distinct values. Use a window where every valid `[left, right]` contributes `right - left + 1` subarrays (all subarrays ending at `right`). `count(exactly k) = at_most(k) - at_most(k-1)`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def subarrays_with_k_distinct(nums, k):
>     def at_most(k):
>         freq = defaultdict(int)
>         left = count = 0
>         for right, n in enumerate(nums):
>             freq[n] += 1
>             while len(freq) > k:
>                 freq[nums[left]] -= 1
>                 if freq[nums[left]] == 0:
>                     del freq[nums[left]]
>                 left += 1
>             count += right - left + 1   # all subarrays [left..right], [left+1..right], ...
>         return count
> 
>     return at_most(k) - at_most(k - 1)
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Prefix sums + hashing O(n) — more complex; sliding window `exactly` without the trick requires two separate left pointers.

**Also try:**

- **Count Number of Nice Subarrays (LC 1248)** — Remap: odd → 1, even → 0
- **Count Vowel Substrings of a Word (LC 2062)** — Exactly-5-distinct-vowels, all characters must be vowels

---

## Variable Window — Minimum Length

> [!info] Approach
> Expand `right` until the window satisfies the constraint (becomes valid). Then shrink `left` as long as the window remains valid, recording the minimum length. Swap the "update answer" location from the expansion step to the shrink step.

---

### Minimum Window Substring (LC 76) `⚡ T1`

> [!example] Problem
> Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "".
> The testcases will be generated such that the answer is unique.
> 
> **Example 1:**
> ```
> Input: s = "ADOBECODEBANC", t = "ABC"
> Output: "BANC"
> Explanation: The minimum window substring "BANC" includes 'A', 'B', and 'C' from string t.
> ```
> 
> **Example 2:**
> ```
> Input: s = "a", t = "a"
> Output: "a"
> Explanation: The entire string s is the minimum window.
> ```
> 
> **Example 3:**
> ```
> Input: s = "a", t = "aa"
> Output: ""
> Explanation: Both 'a's from t must be included in the window.
> Since the largest window of s only has one 'a', return empty string.
> ```
> 
> **Constraints:**
> - m == s.length
> - n == t.length
> - 1 <= m, n <= 10^5
> - s and t consist of uppercase and lowercase English letters.

> [!tip] Recognize · Gotcha
> **Gotcha:** Shrink until `s[left]` is a required char, then record

> [!failure] Tempting wrong approach
> Comparing full Counters each step, or shrinking only once per `right`. Track a `formed` count of satisfied characters and shrink in a `while` loop.

> [!info] Approach
> Need to cover all characters of `t`. Use a `missing` counter — total characters still needed. Once 0 → window is valid → shrink. Expand right: if `need[c] > 0` before decrement, `missing -= 1`. Shrink while `missing == 0`: advance left past non-required characters (those with `need[s[left]] < 0`), record window, then remove `s[left]` from window. `need` can go negative (excess characters) — only decrement `missing` when `need[c]` was positive (character was still required).

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def min_window(s, t):
>     need = Counter(t)
>     missing = len(t)    # total characters still needed
>     best_start = best_len = 0
>     found = False
>     left = 0
> 
>     for right, c in enumerate(s):
>         if need[c] > 0:
>             missing -= 1
>         need[c] -= 1
> 
>         if missing == 0:                    # valid window found
>             while need[s[left]] < 0:       # shrink: skip excess characters
>                 need[s[left]] += 1
>                 left += 1
>             # s[left] is now required — record this tightest window
>             if not found or right - left + 1 < best_len:
>                 best_start = left
>                 best_len = right - left + 1
>                 found = True
>             # Slide: invalidate window to search for next candidate
>             need[s[left]] += 1
>             missing += 1
>             left += 1
> 
>     return s[best_start:best_start + best_len] if found else ""
> ```

> [!success] Complexity
> O(|s| + |t|) time, O(|alphabet|) space.

> [!tip] Alternatives
> Two-pointer with explicit char counts O(n) — equivalent; the `missing` trick avoids full dict comparison.

**Also try:**

- **Minimum Size Subarray Sum (LC 209)** — Positive integers mean adding elements always increases sum, removing always decreases
- **Minimum Window with All Characters Including Duplicates** — This IS LC 76 — the standard minimum window already handles duplicates via `missing` counter
- **Smallest Subarray with Distinct Element Count K** — Minimum-length window with an exact distinct count

---

## Sliding Window + Monotonic Deque

> [!info] Approach
> A monotonic deque stores indices in order of decreasing value (for max) or increasing value (for min). The front always holds the extreme element for the current window. Amortized O(1) per element: each index is pushed and popped at most once.

---

### Sliding Window Maximum (LC 239) `⚡ T1`

> [!example] Problem
> You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position.
> Return the max sliding window.
> 
> **Example 1:**
> ```
> Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
> Output: [3,3,5,5,6,7]
> Explanation: 
> Window position                Max
> ---------------               -----
> [1  3  -1] -3  5  3  6  7       3
>  1 [3  -1  -3] 5  3  6  7       3
>  1  3 [-1  -3  5] 3  6  7       5
>  1  3  -1 [-3  5  3] 6  7       5
>  1  3  -1  -3 [5  3  6] 7       6
>  1  3  -1  -3  5 [3  6  7]      7
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
> - 1 <= k <= nums.length

> [!tip] Recognize · Gotcha
> **Signal:** Front = max; pop expired indices · **Gotcha:** Store **indices** in deque, not values.

> [!failure] Tempting wrong approach
> A max-heap without evicting out-of-window indices returns stale maxima. With lazy eviction it's O(n log n). The monotonic deque is O(n).

> [!info] Approach
> Recomputing max per window is O(nk). A deque maintaining a decreasing sequence of indices gives O(1) max lookup. Deque stores indices in decreasing order of their values. Front = index of max for current window. Before adding `i`: (1) pop front if it's outside window `[i-k+1, i]`; (2) pop back while `nums[deque[-1]] <= nums[i]` (smaller elements can never be max while `i` is in window). Append `i`. Record `nums[deque[0]]` once `i >= k-1`.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_sliding_window(nums, k):
>     dq: deque[int] = deque()  # stores indices
>     front = max of current window
>     result = []
> 
>     for i, val in enumerate(nums):
>         # Remove indices outside current window
>         if dq and dq[0] < i - k + 1:
>             dq.popleft()
>         # Maintain decreasing order: evict smaller elements from back
>         while dq and nums[dq[-1]] < val:
>             dq.pop()
>         dq.append(i)
>         if i >= k - 1:
>             result.append(nums[dq[0]])
> 
>     return result
> ```

> [!success] Complexity
> O(n) time, O(k) space.

> [!tip] Alternatives
> Segment tree or sparse table — O(n log n) build + O(1) query; overkill. Max-heap O(n log k) — correct but slower. Deque is optimal for this specific problem.

---

### Jump Game VI (LC 1696) `🎯 T2`

> [!example] Problem
> You are given a 0-indexed integer array nums and an integer k.
> You are initially standing at index 0. In one move, you can jump at most k steps forward without going outside the boundaries of the array. That is, you can jump from index i to any index in the range [i + 1, min(n - 1, i + k)] inclusive.
> You want to reach the last index of the array (index n - 1). Your score is the sum of all nums[j] for each index j you visited in the array.
> Return the maximum score you can get.
> 
> **Example 1:**
> ```
> Input: nums = [1,-1,-2,4,-7,3], k = 2
> Output: 7
> Explanation: You can choose your jumps forming the subsequence [1,-1,4,3] (underlined above). The sum is 7.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [10,-5,-2,4,0,3], k = 3
> Output: 17
> Explanation: You can choose your jumps forming the subsequence [10,4,3] (underlined above). The sum is 17.
> ```
> 
> **Example 3:**
> ```
> Input: nums = [1,-5,-20,4,-1,3,-6,-3], k = 2
> Output: 0
> ```
> 
> **Constraints:**
> - 1 <= nums.length, k <= 10^5
> - -10^4 <= nums[i] <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** `dp[i] = nums[i] + max(window)` · **Gotcha:** Pop front when out of window

> [!info] Approach
> DP recurrence: `dp[i] = nums[i] + max(dp[i-k], ..., dp[i-1])`. Naive O(nk). Optimize with a decreasing deque of the last `k` dp values — front = max in range. `dp[i] = nums[i] + dp[deque_front]`. Maintain deque in decreasing dp-value order. Evict front when it's outside the `k`-window. Before computing `dp[i]`: evict stale front (`dq[0] < i - k`). After computing `dp[i]`: evict back while `dp[dq[-1]] <= dp[i]`; append `i`. Space-optimise by storing dp in original array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def max_result(nums, k):
>     n = len(nums)
>     dp = [0] * n
>     dp[0] = nums[0]
>     dq: deque[int] = deque()
>     dq.append(0)
> 
>     for i in range(1, n):
>         # Evict indices outside the k-window
>         while dq and dq[0] < i - k:
>             dq.popleft()
>         dp[i] = nums[i] + dp[dq[0]]
>         # Maintain decreasing deque by dp value
>         while dq and dp[dq[-1]] <= dp[i]:
>             dq.pop()
>         dq.append(i)
> 
>     return dp[n - 1]
> ```

> [!success] Complexity
> O(n) time, O(n) space (dp array + deque).

> [!tip] Alternatives
> Priority heap O(n log k) — correct but slower; sparse table for range max O(n log n) build + O(1) query, O(n log n) overall — more complex. Deque DP is the idiomatic O(n) solution.

**Also try:**

- **Sliding Window Minimum (LC variant)** — Symmetric to sliding window maximum
- **Longest Continuous Subarray with Absolute Diff ≤ Limit (LC 1438)** — `max(window) - min(window) <= limit`

---

## Variable Window — Max Length (Flip / Delete)

> [!info] Approach
> A class of problems where you can "spend" a budget (flip zeros, delete elements) to extend a valid window. The window tracks how much budget has been used; shrink when budget is exceeded. Equivalent to "at most K bad elements".

---

### Max Consecutive Ones III (LC 1004) `⚡ T1`

> [!example] Problem
> Given a binary array nums and an integer k, return the maximum number of consecutive 1's in the array if you can flip at most k 0's.
> 
> **Example 1:**
> ```
> Input: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2
> Output: 6
> Explanation: [1,1,1,0,0,1,1,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], k = 3
> Output: 10
> Explanation: [0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1]
> Bolded numbers were flipped from 0 to 1. The longest subarray is underlined.
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^5
> - nums[i] is either 0 or 1.
> - 0 <= k <= nums.length

> [!info] Approach
> Window contains at most `k` zeros. Expanding right adds ones (free) or zeros (costs 1 from budget). When zeros in window exceed `k`, shrink left. Track `zeros` count in the window. While `zeros > k` → if `nums[left] == 0`, decrement zeros; advance left. Answer is `right - left + 1` after each valid step — window never shrinks below the best size seen (LC 424 trick not needed here since we do want exact max).

> [!note]- Python Solution
> ```python
> def longest_ones(nums, k):
>     left = zeros = best = 0
>     for right in range(len(nums)):
>         if nums[right] == 0:
>             zeros += 1
>         while zeros > k:
>             if nums[left] == 0:
>                 zeros -= 1
>             left += 1
>         best = max(best, right - left + 1)
>     return best
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Same as "Longest Repeating Character Replacement" restricted to binary input. For k=0 this degenerates to counting max run of ones.

**Also try:**

- **Longest Subarray of 1s After Deleting One Element (LC 1493)** — Deleting one element = flipping one 0 to nothing, or dropping one 1
- **Binary Subarrays with Sum (LC 930)** — Exactly-k trick: binary values make at_most well-defined

---

## More Variable Window Problems

---

## See Also

[[two-pointers]] | [[hashing]] | [[string]] | [[queue]]
[[two-pointers]] | [[array]] | [[hashing]] | [[string-algorithms]]
