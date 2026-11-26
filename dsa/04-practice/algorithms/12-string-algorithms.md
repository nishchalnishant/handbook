---
tags: [coding, algorithms, string-algorithms]
topic: String Algorithms
difficulty: mixed
---
# String Algorithms

← [Concept deep-dive](../../03-algorithms/12-string-algorithms.md) · [Algorithms index](../../03-algorithms/README.md)

## What this covers

> [!abstract] In this file
> **Covers:** Worked pattern-matching problems: KMP, Rabin-Karp, Z-function, palindrome algorithms, suffix/trie-based, string windows.
> **You'll be able to:** Apply rolling hash / KMP when brute force is too slow.
> **Prereqs:** String algorithms lecture · **Pair with:** [String algorithms lecture](../../03-algorithms/12-string-algorithms.md) · **Time:** 2 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [KMP (Knuth-Morris-Pratt)](#kmp-knuth-morris-pratt) · [Rabin-Karp (Rolling Hash)](#rabin-karp-rolling-hash) · [Z-Function / Z-Algorithm](#z-function--z-algorithm) · [Palindrome Algorithms](#palindrome-algorithms) · [Suffix Array / Trie Based](#suffix-array--trie-based) · [Sliding Window on Strings](#sliding-window-on-strings)

> [!tip] If you only have 20 minutes
> **Do these first:** [Longest Palindromic Substring](#longest-palindromic-substring--t1) · [Palindromic Substrings — Count](#palindrome-algorithms) · [Permutation in String](#permutation-in-string--t1) · [Implement KMP — Failure Function + Search](#kmp-knuth-morris-pratt) · [Implement Rabin-Karp](#rabin-karp-rolling-hash) · [Longest Happy Prefix](#longest-happy-prefix--t2) · [Shortest Palindrome](#sliding-window-on-strings)
> **Template:** Expand around center: `2n-1` centers, `while l >= 0 and r < n and s[l] == s[r]: l -= 1; r += 1`.
> **Template:** KMP `lps`: on mismatch `length = lps[length-1]` (cascade), never reset to 0.
> **Gotchas:** Even-length centers (`i, i+1`) · Rabin-Karp: verify on hash hit; precompute `base^(m-1) mod p` · Shortest Palindrome needs the `#` separator · Manacher is `💤 T3` — mention only if asked.

---

## KMP (Knuth-Morris-Pratt)

**Also try:**

- **Implement KMP — Failure Function + Search** — Naive search rescans characters already matched; O(nm) is unacceptable for large text
- **Find All Occurrences of Pattern in Text** — Standard substring search is O(nm); we need every occurrence, not just the first
- **Add Minimum Characters to Make a String Palindrome** — Minimum insertions = `n - LPS(s)`, where LPS is the Longest Palindromic Subsequence

---

## Rabin-Karp (Rolling Hash)

---

### Longest Duplicate Substring `⚡ T1`

> [!example] Problem
> Given a string s, consider all duplicated substrings: (contiguous) substrings of s that occur 2 or more times. The occurrences may overlap.
> Return any duplicated substring that has the longest possible length. If s does not have a duplicated substring, the answer is "".
> 
> **Example 1:**
> ```
> Input: s = "banana"
> Output: "ana"
> ```
> 
> **Example 2:**
> ```
> Input: s = "abcd"
> Output: ""
> ```
> 
> **Constraints:**
> - 2 <= s.length <= 3 * 10^4
> - s consists of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** Monotone in length · **Gotcha:** Use a large mod / double hash; verify on hit

> [!info] Approach
> Checking all substrings for duplicates is O(n³). We need a smarter search space reduction. Binary search on length L. For each L, use rolling hash to collect all length-L substring hashes in a set; if any hash appears twice (and verification confirms no collision), a duplicate of length L exists. Binary search `[1, n-1]`. `check(L)`: slide window of size L, compute hash in O(1) per step, store in set. If duplicate found, record it; search larger L. If not, search smaller. Total: O(n log n).

> [!note]- Python Solution
> ```python
> def longest_dup_substring(s):
>     BASE, MOD = 131, (1 << 61) - 1
>     n = len(s)
>     nums = [ord(c) for c in s]
> 
>     def check(length):
>         power = pow(BASE, length, MOD)
>         h = 0
>         for c in nums[:length]:
>             h = (h * BASE + c) % MOD
>         seen = {h: [0]}
>         for i in range(1, n - length + 1):
>             h = (h * BASE - nums[i - 1] * power + nums[i + length - 1]) % MOD
>             if h in seen:
>                 for start in seen[h]:
>                     if s[start:start + length] == s[i:i + length]:
>                         return s[i:i + length]
>                 seen[h].append(i)
>             else:
>                 seen[h] = [i]
>         return ""
> 
>     lo, hi = 1, n - 1
>     result = ""
>     while lo <= hi:
>         mid = (lo + hi) // 2
>         candidate = check(mid)
>         if candidate:
>             result = candidate
>             lo = mid + 1
>         else:
>             hi = mid - 1
>     return result
> ```

> [!success] Complexity
> Time O(n log n) average | Space O(n).

> [!tip] Alternatives
> Suffix array + LCP array: O(n log n) build, then `max(LCP)` gives the answer in O(n). More complex to implement but same asymptotic and no collision risk.

**Also try:**

- **Implement Rabin-Karp** — Direct character-by-character comparison at each position is O(nm)
- **Count Distinct Doubled Substrings** — We need to find all substrings of even length where both halves are identical — checking naively is O(n³)

---

## Z-Function / Z-Algorithm

---

### Repeated String Match `🎯 T2`

> [!example] Problem
> LeetCode 686. Given strings `a` and `b`, return the minimum number of times you must repeat `a` such that `b` is a substring of the result. Return `-1` if this is impossible.
>
> **Example:**
> ```
> Input: a = "abcd", b = "cdabcdab"
> Output: 3   # "abcdabcdabcd" contains "cdabcdab"
>
> Input: a = "a", b = "aa"
> Output: 2
> ```

> [!info] Approach
> The minimum repeats needed is `ceil(len(b) / len(a))`. If `b` is a substring, it must appear within at most `ceil + 1` repetitions (one extra in case `b` spans a boundary). Build that string and check. Use Python's `in` operator (O(n·m) naive but accepted at interview); optionally use Rabin-Karp rolling hash for O(n+m).
>
> **Rolling hash approach:** hash `b`, then slide a window of `len(b)` over the repeated `a` string using the recurrence:
> `h = (h - ord(leaving) * base^(w-1)) * base + ord(entering)) % mod`

> [!note]- Python Solution
> ```python
> def repeated_string_match(a: str, b: str) -> int:
>     import math
>     reps = math.ceil(len(b) / len(a))
>     candidate = a * reps
>     if b in candidate:
>         return reps
>     candidate += a
>     if b in candidate:
>         return reps + 1
>     return -1
> ```

> [!note]- Python Solution (Rabin-Karp)
> ```python
> def repeated_string_match_rk(a: str, b: str) -> int:
>     import math
>     BASE, MOD = 31, (1 << 61) - 1
>     m = len(b)
>     # hash b
>     hb = 0
>     for c in b:
>         hb = (hb * BASE + ord(c)) % MOD
>     # build repeated a up to len(b) + len(a)
>     reps = math.ceil(len(b) / len(a)) + 1
>     s = a * reps
>     n = len(s)
>     if n < m:
>         return -1
>     # compute hash of first window
>     hs = 0
>     high = 1
>     for i in range(m):
>         hs = (hs * BASE + ord(s[i])) % MOD
>         if i < m - 1:
>             high = (high * BASE) % MOD
>     base_reps = math.ceil(len(b) / len(a))
>     for i in range(n - m + 1):
>         if hs == hb and s[i:i+m] == b:   # verify on hash match
>             needed = math.ceil((i + m) / len(a))
>             return needed
>         if i + m < n:
>             hs = (hs - ord(s[i]) * high) % MOD
>             hs = (hs * BASE + ord(s[i + m])) % MOD
>     return -1
> ```

> [!success] Complexity
> `in` operator: O(n·m) naive, O(n+m) with Python's optimized search. Rabin-Karp: O(n+m) expected. Space O(n+m) for the repeated string.

> [!tip] Edge cases / Alternatives
> - `len(a) > len(b)`: answer is either 1 (if `b in a`) or -1.
> - Characters in `b` not in `a`: immediately return -1 (can short-circuit with `set(b) <= set(a)`).
> - Double hashing (two independent mods) eliminates collision probability in adversarial inputs.

---

### Implement Z-Algorithm Search `🎯 T2`

> [!example] Problem
> Given pattern `P` and text `T`, return all start indices in `T` where `P` occurs as a substring.
>
> **Example:**
> ```
> Input: P = "aab", T = "aabaabaabaab"
> Output: [0, 3, 6, 9]
> ```

> [!info] Approach
> The Z-array of a string `s` stores at each index `i` the length of the longest substring starting at `i` that matches a prefix of `s`. Concatenate `P + '#' + T` (the `#` sentinel prevents Z-values from crossing the boundary). Any position `i` in the combined string where `Z[i] == len(P)` is a match start at offset `i - len(P) - 1` in `T`.
>
> **Z-array construction:** maintain a window `[l, r]` — the rightmost Z-box found so far. For each `i`:
> - If `i` is inside `[l, r]`, `Z[i] >= min(Z[i-l], r-i+1)` — use the mirror. Then try to extend.
> - Otherwise, extend from scratch.

> [!note]- Python Solution
> ```python
> def build_z(s):
>     n = len(s)
>     z = [0] * n
>     z[0] = n
>     l = r = 0
>     for i in range(1, n):
>         if i < r:
>             z[i] = min(r - i, z[i - l])
>         while i + z[i] < n and s[z[i]] == s[i + z[i]]:
>             z[i] += 1
>         if i + z[i] > r:
>             l, r = i, i + z[i]
>     return z
>
> def z_search(text, pattern):
>     if not pattern:
>         return list(range(len(text) + 1))
>     combined = pattern + '#' + text
>     z = build_z(combined)
>     m = len(pattern)
>     return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]
> ```

> [!success] Complexity
> Time O(n+m), Space O(n+m) — n = len(text), m = len(pattern).

> [!tip] Edge cases / Alternatives
> - Empty pattern: return all positions 0..n.
> - Pattern longer than text: return [].
> - vs KMP: identical complexity, different mental model. Z-array is often simpler to remember and implement under pressure.

---

### Longest Happy Prefix `🎯 T2`

> [!example] Problem
> LeetCode 1392. A string is "happy" if it has a longest prefix that is also a suffix (both proper and non-empty). Return that prefix, or `""` if none exists.
>
> **Example:**
> ```
> Input: s = "level"
> Output: "l"
>
> Input: s = "ababab"
> Output: "abab"
> ```

> [!info] Approach — KMP failure function
> The KMP LPS (longest proper prefix that is also suffix) array directly gives the answer. `lps[-1]` is the length of the longest proper prefix of the whole string that is also a suffix. Return `s[:lps[-1]]`.

> [!note]- Python Solution (KMP)
> ```python
> def longest_prefix(s: str) -> str:
>     n = len(s)
>     lps = [0] * n
>     length = 0
>     i = 1
>     while i < n:
>         if s[i] == s[length]:
>             length += 1
>             lps[i] = length
>             i += 1
>         elif length:
>             length = lps[length - 1]
>             # do NOT increment i
>         else:
>             lps[i] = 0
>             i += 1
>     return s[:lps[-1]]
> ```

> [!info] Approach — Z-algorithm
> Build the Z-array of `s`. Any `i` where `Z[i] + i == n` means the suffix starting at `i` matches a prefix of length `Z[i]`. The longest such prefix is `max(Z[i] for i in range(1, n) if Z[i] + i == n)`, defaulting to 0.

> [!note]- Python Solution (Z-array)
> ```python
> def longest_prefix_z(s: str) -> str:
>     z = build_z(s)   # from above
>     n = len(s)
>     best = 0
>     for i in range(1, n):
>         if z[i] + i == n:
>             best = max(best, z[i])
>     return s[:best]
> ```

> [!success] Complexity
> O(n) time, O(n) space — both approaches.

> [!tip] Edge cases / Alternatives
> - Single character: `lps[-1] == 0`, return `""`.
> - Whole string is periodic (e.g. `"aaaa"`): LPS answer is `n-1` = `"aaa"`.

**Also try:**

- **Pattern Matching Using Z-Array** — Same goal as KMP — O(n+m) pattern matching

---

## Palindrome Algorithms

### Longest Palindromic Substring `⚡ T1`

> [!example] Problem
> LeetCode 5. Given string `s`, return the longest substring that is a palindrome. If there are ties, return any.
>
> **Example:**
> ```
> Input: s = "babad"
> Output: "bab"  (or "aba")
>
> Input: s = "cbbd"
> Output: "bb"
> ```

> [!tip] Recognize · Gotcha
> **Signal:** "longest palindrome" · **Gotcha:** Must try even centers; track `(start, len)` not substrings

> [!info] Approach — O(n²) expand-around-center (default)
> For each center (n odd centers + n-1 even centers), expand while characters match. Track best. This is the expected L3 answer.

> [!note]- Python Solution (expand-around-center)
> ```python
> def longest_palindrome(s: str) -> str:
>     def expand(l, r):
>         while l >= 0 and r < len(s) and s[l] == s[r]:
>             l -= 1; r += 1
>         return s[l+1:r]
>     best = ""
>     for i in range(len(s)):
>         for sub in (expand(i, i), expand(i, i+1)):
>             if len(sub) > len(best):
>                 best = sub
>     return best
> ```

> [!info] Approach — O(n) Manacher's (when interviewer asks "can you do better than O(n²)?")
> **Transform:** insert `#` between every character and at boundaries: `"abc"` → `"#a#b#c#"`. Now every palindrome is odd-length.
>
> **p[i]:** palindrome radius at center `i` in the transformed string (not counting the center itself).
>
> **Mirror property:** maintain the rightmost palindrome `[l, r]` with center `c`. For new center `i`:
> - If `i < r`: `p[i] >= min(p[2*c - i], r - i)` — use mirror, then try to expand.
> - If `i >= r`: expand from scratch.
>
> Update `c, r` whenever expansion pushes past the current `r`.

> [!note]- Python Solution (Manacher)
> ```python
> def longest_palindrome_manacher(s: str) -> str:
>     # Transform: insert '#'
>     t = '#' + '#'.join(s) + '#'
>     n = len(t)
>     p = [0] * n
>     c = r = 0   # center and right boundary of rightmost palindrome
>     for i in range(n):
>         if i < r:
>             mirror = 2 * c - i
>             p[i] = min(r - i, p[mirror])
>         # try to expand
>         while i - p[i] - 1 >= 0 and i + p[i] + 1 < n and t[i - p[i] - 1] == t[i + p[i] + 1]:
>             p[i] += 1
>         # update rightmost palindrome
>         if i + p[i] > r:
>             c, r = i, i + p[i]
>     # find the max radius and map back to original string
>     best_center = p.index(max(p))
>     best_len = p[best_center]
>     # in transformed string, original index = (transformed_index - 1) // 2
>     start = (best_center - best_len) // 2
>     return s[start: start + best_len]
> ```

> [!success] Complexity
> Expand-around-center: O(n²) time, O(1) space. Manacher: O(n) time, O(n) space.

> [!tip] Edge cases / Alternatives
> - Empty string or single character: return `s` as-is.
> - All same characters (e.g. `"aaaa"`): answer is the whole string — both approaches handle this.
> - When to use Manacher: only if interviewer explicitly asks for O(n). The expand approach is cleaner and sufficient for L3.
> - The `#` sentinel makes all palindromes odd-length in the transformed string — this is the key insight that unifies odd/even cases.

---

### Manacher's Algorithm — O(n) All Palindromes `💤 T3`

> [!example] Problem
> Find the radius of the longest palindromic substring centered at every position in O(n). LeetCode 5 (O(n) solution).

> [!info] Approach
> Naive expand-around-center is O(n²) because each center expands independently. Manacher reuses overlap between palindromes. Transform `s` by inserting `#` between every character (`a#b#b#a` → `#a#b#b#a#`) to unify odd and even cases. Maintain the rightmost palindrome center `c` and its right boundary `r`. For each position i: mirror `i` across `c` to get `mirror = 2c - i`. Initialize `P[i] = min(r - i, P[mirror])` — reuse what's already known. Then try to extend beyond that. Update `c, r` when a new palindrome extends past `r`. Each character is "extended past" at most once (because r only increases), so total comparisons = O(n).

> [!note]- Python Solution
> ```python
> def manacher(s):
>     # Transform: "abc" -> "#a#b#c#"
>     t = '#' + '#'.join(s) + '#'
>     n = len(t)
>     P = [0] * n   # P[i] = palindrome radius at i in transformed string
>     c = r = 0     # center and right boundary of rightmost palindrome
> 
>     for i in range(n):
>         mirror = 2 * c - i
>         if i < r:
>             P[i] = min(r - i, P[mirror])
>         # Attempt to expand beyond known boundary
>         left, right = i - P[i] - 1, i + P[i] + 1
>         while left >= 0 and right < n and t[left] == t[right]:
>             P[i] += 1
>             left -= 1
>             right += 1
>         # Update rightmost palindrome
>         if i + P[i] > r:
>             c, r = i, i + P[i]
>     return P
> 
> def longest_palindrome_manacher(s):
>     P = manacher(s)
>     t = '#' + '#'.join(s) + '#'
>     center = P.index(max(P))
>     radius = P[center]
>     # Map back: original index = (center - radius) // 2
>     start = (center - radius) // 2
>     return s[start: start + radius]
> ```

> [!success] Complexity
> Time O(n) | Space O(n).

> [!tip] Alternatives
> Expand around center: O(n²) but simpler code; sufficient for most interview constraints (n ≤ 10⁵). Use Manacher when explicitly asked for O(n) or n > 10⁵.

**Also try:**

- **Palindromic Substrings — Count** — Each center expansion contributes one palindrome per step

---

## Suffix Array / Trie Based

**Also try:**

- **Number of Distinct Substrings** — Total substrings = n(n+1)/2
- **Longest Common Prefix of All Suffixes** — Brute-force LCP computation between all suffix pairs is O(n²)

---

## Sliding Window on Strings

---

### Permutation in String `⚡ T1`

> Full walkthrough: [Permutation in String (LC 567)](03-sliding-window.md#permutation-in-string-lc-567--t1).

---

### Distinct Subsequences (LC 115) `🎯 T2`

> Full walkthrough: [Distinct Subsequences](08-dynamic-programming.md#distinct-subsequences--t2).

**Also try:**

- **Longest Substring with K Distinct Characters** — We want the longest window satisfying a constraint on character diversity — a classic sliding window
- **Regular Expression Matching (LC 10)** — see [Regular Expression Matching](08-dynamic-programming.md#string-dp)
- **Wildcard Matching (LC 44)** — `'*'` can match any sequence — creates branching over all possible lengths
- **Shortest Palindrome** — We need the longest palindromic prefix

---

## See Also

[[string]] | [[trie]] | [[dynamic-programming]] | [[sliding-window]]
