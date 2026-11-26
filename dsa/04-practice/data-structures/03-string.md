---
tags: [coding, data-structures, string]
topic: String
difficulty: mixed
---
# String Problems — Deep Dive

## What this covers

> [!abstract] In this file
> **Covers:** Worked string problems: anagrams, palindromes, sliding window, encoding, parsing/simulation, pattern matching.
> **You'll be able to:** Solve string window and parsing problems without index bugs.
> **Prereqs:** String lecture · **Pair with:** [String lecture](../../02-data-structures/03-string.md) · **Time:** 4 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Frequency Map / Anagram](#frequency-map--anagram) · [Two Pointers — Palindrome](#two-pointers--palindrome) · [Sliding Window](#sliding-window) · [Prefix Sum on Characters](#prefix-sum-on-characters) · [Encoding / Hashing](#encoding--hashing) · [Parsing / Simulation](#parsing--simulation) · [Two Pointers — Reverse / Subsequence](#two-pointers--reverse--subsequence) · [Pattern Matching](#pattern-matching) · [String Manipulation](#string-manipulation)

> [!tip] If you only have 20 minutes
> **Do these first:** [Valid Anagram](#valid-anagram--t2) · [Group Anagrams](#group-anagrams--t1) · [Valid Palindrome](#valid-palindrome--t2) · [Longest Substring Without Repeating Characters](#longest-substring-without-repeating-characters--t1) · [Longest Palindromic Substring](#longest-palindromic-substring--t1) · [Minimum Window Substring](#minimum-window-substring--t1) · [Encode and Decode Strings](#encode-and-decode-strings--t2) · [Decode String](#parsing--simulation)
> **Template:** Frequency key: `tuple(count[26])` or `''.join(sorted(s))` for grouping.
> **Template:** Expand around center over `2n-1` centers: `expand(i, i)` and `expand(i, i+1)`.
> **Gotchas:** Python strings are immutable — build with a list + `''.join` · Unicode/case/non-alnum rules — ask first · Encode/Decode: length-prefix (`len#str`), not a delimiter · most "string" problems are really hashing or sliding window.

---

Pattern tags: frequency map, two pointers, sliding window, hashing, parsing.

---

## Frequency Map / Anagram

---

### Valid Anagram `🎯 T2`

> [!example] Problem
> Given two strings s and t, return true if t is an anagram of s, and false otherwise.
> 
> **Example 1:**
> ```
> Input: s = "anagram", t = "nagaram"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "rat", t = "car"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length, t.length <= 5 * 10^4
> - s and t consist of lowercase English letters.

> [!info] Approach
> Two strings are anagrams iff they are identical after sorting. Sorting is O(n log n). We can do O(n) by comparing character frequency vectors. A 26-bucket frequency array (fixed alphabet) or a `Counter`. Two strings are anagrams iff their frequency maps are equal. Build `Counter(s)` and `Counter(t)`. Return `Counter(s) == Counter(t)`. For pure lowercase ASCII, use `[0]*26` and compare arrays — same asymptotic cost, better constant.

> [!note]- Python Solution
> ```python
> from collections import Counter
> 
> def is_anagram(s, t):
>     if len(s) != len(t):
>         return False
>     return Counter(s) == Counter(t)
> 
> # O(1) space variant for lowercase a-z only
> def is_anagram_array(s, t):
>     if len(s) != len(t):
>         return False
>     freq = [0] * 26
>     for c in s:
>         freq[ord(c) - ord('a')] += 1
>     for c in t:
>         freq[ord(c) - ord('a')] -= 1
>     for f in freq:
>         if not (f == 0):
>             return False
>     return True
> ```

> [!success] Complexity
> Time O(n). Space O(1) for fixed alphabet (26 buckets), O(n) for general `Counter`.

> [!tip] Alternatives
> - Sorting: `sorted(s) == sorted(t)` — O(n log n), simpler to write, correct for Unicode.
> - XOR trick: works only if each character appears an even number of times — too restrictive for general anagram check.

---

### Group Anagrams `⚡ T1`

> [!example] Problem
> Given an array of strings strs, group the anagrams together. You can return the answer in any order.
> 
> **Example 1:**
> ```
> Input: strs = ["eat","tea","tan","ate","nat","bat"]
> Output: [["bat"],["nat","tan"],["ate","eat","tea"]]
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: strs = [""]
> Output: [[""]]
> ```
> 
> **Example 3:**
> ```
> Input: strs = ["a"]
> Output: [["a"]]
> ```
> 
> **Constraints:**
> - 1 <= strs.length <= 10^4
> - 0 <= strs[i].length <= 100
> - strs[i] consists of lowercase English letters.

> [!tip] Recognize · Gotcha
> **Signal:** "Same letters, group together" · **Gotcha:** 26-array fails for Unicode; `sorted` is O(K log K) vs O(K) count.

> [!info] Approach
> All anagrams share the same canonical form — their sorted version. Use that as a hash map key. HashMap from canonical key → list of anagrams. For pure lowercase ASCII, use a tuple of 26 frequency counts as key (avoids O(L log L) sort per word). For each word, compute `key = tuple(freq_array)` or `key = "".join(sorted(word))`. Append word to `groups[key]`. Return `list(groups.values())`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def group_anagrams(strs):
>     groups = defaultdict(list)
>     for word in strs:
>         freq = [0] * 26
>         for c in word:
>             freq[ord(c) - ord('a')] += 1
>         groups[tuple(freq)].append(word)
>     return list(groups.values())
> ```

> [!success] Complexity
> Time O(N × L) where N = number of words, L = max word length. Space O(N × L).

> [!tip] Alternatives
> - Sort-based key `sorted(word)`: O(N × L log L) — simpler but slower due to the sort.
> - Prime product key: assign each letter a prime, key = product of primes for each char. O(N × L) but product overflows for long words — not safe.

---

### Find All Anagrams in a String `⚡ T1`

> Full walkthrough: [Find All Anagrams in a String (LC 438)](../algorithms/03-sliding-window.md#find-all-anagrams-in-a-string-lc-438--t1).

---

## Two Pointers — Palindrome

---

### Valid Palindrome `🎯 T2`

> [!example] Problem
> A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
> Given a string s, return true if it is a palindrome, or false otherwise.
> 
> **Example 1:**
> ```
> Input: s = "A man, a plan, a canal: Panama"
> Output: true
> Explanation: "amanaplanacanalpanama" is a palindrome.
> ```
> 
> **Example 2:**
> ```
> Input: s = "race a car"
> Output: false
> Explanation: "raceacar" is not a palindrome.
> ```
> 
> **Example 3:**
> ```
> Input: s = " "
> Output: true
> Explanation: s is an empty string "" after removing non-alphanumeric characters.
> Since an empty string reads the same forward and backward, it is a palindrome.
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 2 * 10^5
> - s consists only of printable ASCII characters.

> [!info] Approach
> After filtering to alphanumeric + lowercase, a palindrome reads the same forwards and backwards. Two pointers moving inward compare characters without allocating a filtered string. Left pointer starts at 0, right pointer starts at end. Skip non-alphanumeric characters. Compare lowercase versions. While `l < r`: skip `l` while not alphanumeric, skip `r` while not alphanumeric. If `s[l].lower() != s[r].lower()`, return False. Advance both pointers inward.

> [!note]- Python Solution
> ```python
> def is_palindrome(s):
>     l, r = 0, len(s) - 1
>     while l < r:
>         while l < r and not s[l].isalnum():
>             l += 1
>         while l < r and not s[r].isalnum():
>             r -= 1
>         if s[l].lower() != s[r].lower():
>             return False
>         l += 1
>         r -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n). Space O(1).

> [!tip] Alternatives
> - Filter then compare: `clean = [c.lower() for c in s if c.isalnum()]; return clean == clean[::-1]` — O(n) time, O(n) space, less elegant.
> - Regex filter: `re.sub(r'[^a-z0-9]', '', s.lower())` then compare to its reverse — same complexity, cleaner for production code.

---

### Longest Palindromic Substring `⚡ T1`

> Full walkthrough: [Longest Palindromic Substring](../algorithms/12-string-algorithms.md#longest-palindromic-substring--t1).

**Also try:**

- **Palindromic Substrings (Count All Palindromic Substrings)** — see [Palindromic Substrings — Count](../algorithms/12-string-algorithms.md#palindrome-algorithms)

---

## Sliding Window

---

### Longest Substring Without Repeating Characters `⚡ T1`

> Full walkthrough: [Longest Substring Without Repeating Characters (LC 3)](../algorithms/03-sliding-window.md#longest-substring-without-repeating-characters-lc-3--t1).

---

### Minimum Window Substring `⚡ T1`

> Full walkthrough: [Minimum Window Substring (LC 76)](../algorithms/03-sliding-window.md#minimum-window-substring-lc-76--t1).

---

### Longest Repeating Character Replacement `⚡ T1`

> Full walkthrough: [Longest Repeating Character Replacement (LC 424)](../algorithms/03-sliding-window.md#longest-repeating-character-replacement-lc-424--t1).

---

## Prefix Sum on Characters

---

### Subarray Sum Equals K (character version) `⚡ T1`

> Full walkthrough: [Subarray Sum Equals K](02-hashing.md#subarray-sum-equals-k--t1).

**Also try:**

- **Prefix Sum on Characters Pattern**
- **Number of Substrings Containing All Three Characters** — For any right endpoint `r`, the valid left endpoints form a contiguous suffix — as soon as all three chars appear, every further-left start …
- **Count Vowel Substrings of a Word** — see [Count Vowel Substrings of a Word (LC 2062)](../algorithms/03-sliding-window.md#variable-window--exactly-k)
- **Binary Subarrays With Sum** — see [Binary Subarrays with Sum (LC 930)](../algorithms/03-sliding-window.md#variable-window--max-length-flip--delete)

---

## Encoding / Hashing

---

### Encode and Decode Strings `🎯 T2`

> [!example] Problem
> Design an algorithm to encode **a list of strings** to **a string**. The encoded string is then sent over the network and is decoded back to the original list of strings.
> 
> Machine 1 (sender) has the function:
> 
> ```
> 
> string encode(vector<string> strs) {
>   // ... your code
>   return encoded_string;
> }
> ```
> 
> Machine 2 (receiver) has the function:
> 
> ```
> 
> vector<string> decode(string s) {
>   //... your code
>   return strs;
> }
> 
> ```
> 
> So Machine 1 does:
> 
> ```
> 
> string encoded_string = encode(strs);
> 
> ```
> 
> and Machine 2 does:
> 
> ```
> 
> vector<string> strs2 = decode(encoded_string);
> 
> ```
> 
> `strs2` in Machine 2 should be the same as `strs` in Machine 1.
> 
> Implement the `encode` and `decode` methods.
> 
> You are not allowed to solve the problem using any serialize methods (such as `eval`).
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** dummy_input = ["Hello","World"]
> **Output:** ["Hello","World"]
> **Explanation:**
> Machine 1:
> Codec encoder = new Codec();
> String msg = encoder.encode(strs);
> Machine 1 ---msg---> Machine 2
> 
> Machine 2:
> Codec decoder = new Codec();
> String[] strs = decoder.decode(msg);
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** dummy_input = [""]
> **Output:** [""]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= strs.length <= 200`
> 	
> - `0 <= strs[i].length <= 200`
> 	
> - `strs[i]` contains any possible characters out of `256` valid ASCII characters.
> 
>  
> 
> **Follow up: **Could you write a generalized algorithm to work on any possible set of characters?

> [!info] Approach
> Simple delimiters (`,`, `#`) fail if the strings contain those characters. A length-prefix scheme is delimiter-free and unambiguous. Encode each string as `{length}#{string}`. The `#` here marks the end of the length field, not a content separator — the length tells us exactly how many bytes to read. Encode: for each string, emit `str(len(s)) + '#' + s`. Decode: read digits up to `#` to get length L; read exactly L characters as the next string; advance pointer past them; repeat.

> [!note]- Python Solution
> ```python
> def encode(strs):
>     return "".join(f"{len(s)}#{s}" for s in strs)
> 
> def decode(s):
>     result = []
>     i = 0
>     while i < len(s):
>         j = s.index('#', i)
>         length = int(s[i:j])
>         result.append(s[j + 1: j + 1 + length])
>         i = j + 1 + length
>     return result
> ```

> [!success] Complexity
> Time O(total characters) for both encode and decode. Space O(total characters).

> [!tip] Alternatives
> - Escape-character scheme: prefix special chars with `\` — O(n) but encoding complexity grows with character set.
> - Fixed-width length field (e.g., always 4 bytes big-endian): avoids the `#` separator entirely — used in binary protocols like protobuf.

**Also try:**

- **String Hashing (Duplicate Substring Detection)** — Comparing every pair of substrings of length L is O(n × L) per comparison and O(n²L) total

---

## Parsing / Simulation

---

### Text Justification `⚡ T1`

> [!example] Problem
> Given words and maxWidth, format the text fully justified: each line packed greedily with as many words as fit, extra spaces distributed as evenly as possible with left gaps getting more. The last line (and any single-word line) is left-justified, padded right.

> [!info] Approach
> Zero algorithms, pure care — that's why Google asks it at L4. Two phases per line: greedy packing (a word fits if `current_length + len(line) + len(word) <= maxWidth`, where `len(line)` counts the mandatory single spaces), then space distribution: with `gaps = len(line) - 1`, hand out `maxWidth - length` spaces round-robin so the leftmost gaps get the extras. Handle the two left-justified cases (last line, single word) with `' '.join(...).ljust(maxWidth)`.

> [!note]- Python Solution
> ```python
> def fullJustify(words, maxWidth):
>     res, line, length = [], [], 0
>     for w in words:
>         if length + len(line) + len(w) > maxWidth:
>             gaps = len(line) - 1 or 1
>             for i in range(maxWidth - length):
>                 line[i % gaps] += ' '
>             res.append(''.join(line))
>             line, length = [], 0
>         line.append(w)
>         length += len(w)
>     res.append(' '.join(line).ljust(maxWidth))
>     return res
> ```

> [!success] Complexity
> Time O(total characters); Space O(maxWidth) working.

> [!warning] Gotcha
> The `or 1` makes a single-word line reuse the round-robin path (all spaces onto `line[0]`) — one branch instead of three. Dry-run the last line and a one-word line before declaring done; that's where everyone fails.

---

### Valid Number `🎯 T2`

> [!example] Problem
> Return whether a string is a valid number: optional sign, digits, at most one dot, at most one exponent (`e`/`E`) which must be preceded by a number and followed by an integer.

> [!info] Approach
> A hand-rolled state machine via three flags: `seen_digit`, `seen_dot`, `seen_exp`. Walk once; each character class checks its legality against the flags. The key rule: after `e`, **reset `seen_digit`** — the exponent needs its own digits. Enumerate the grammar out loud before coding; the interviewer is grading the enumeration.

> [!note]- Python Solution
> ```python
> def isNumber(s):
>     seen_digit = seen_dot = seen_exp = False
>     for i, c in enumerate(s):
>         if c.isdigit():
>             seen_digit = True
>         elif c in '+-':
>             if i > 0 and s[i-1] not in 'eE':
>                 return False
>         elif c == '.':
>             if seen_dot or seen_exp:
>                 return False
>             seen_dot = True
>         elif c in 'eE':
>             if seen_exp or not seen_digit:
>                 return False
>             seen_exp, seen_digit = True, False
>         else:
>             return False
>     return seen_digit
> ```

> [!success] Complexity
> Time O(n); Space O(1).

> [!warning] Gotcha
> A sign is only legal at index 0 or right after `e` — that single condition covers `"+-6"`, `"6+1"`, `"1e+5"` at once. Test set: `".1"` ✓, `"3."` ✓, `"e3"` ✗, `"1e"` ✗, `"."` ✗.

**Also try:**

- **String to Integer (atoi)** — This is a state-machine / parsing problem
- **Longest Common Prefix** — The longest common prefix is bounded by the shortest string
- **Decode String** — Nested brackets suggest a stack
- **Compare Version Numbers** — Split on `.` gives revision tokens
- **Integer to English Words** — Numbers follow a recursive pattern: every 3-digit group is described the same way, then suffixed with Billion/Million/Thousand

---

## Two Pointers — Reverse / Subsequence

**Also try:**

- **Reverse String** — see [Reverse String (LC 344)](../algorithms/02-two-pointers.md#two-pointer-on-strings)
- **Is Subsequence** — Greedy two-pointer: advance through `t` trying to match characters of `s` in order

---

## Pattern Matching

**Also try:**

- **Implement strStr (KMP)** — Naive search is O(n×m) in the worst case (e.g., `haystack = "aaa…a"`, `needle = "aaa…ab"`)
- **Repeated Substring Pattern** — If `s` is a repetition of some pattern `p`, then `s + s` contains `s` starting at a position other than 0 or `len(s)`
- **Longest Happy Prefix** — see [Longest Happy Prefix](../algorithms/12-string-algorithms.md#longest-happy-prefix--t2)

---

## String Manipulation

---

### Valid Palindrome II (LC 680) `🎯 T2`

> [!example] Problem
> Given a string s, return true if the s can be palindrome after deleting at most one character from it.
> 
> **Example 1:**
> ```
> Input: s = "aba"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "abca"
> Output: true
> Explanation: You could delete the character 'c'.
> ```
> 
> **Example 3:**
> ```
> Input: s = "abc"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^5
> - s consists of lowercase English letters.

> [!info] Approach
> A standard two-pointer palindrome check stops at the first mismatch. At that point, removing either the left or right character might fix things — we just need to check both possibilities. Two pointers `left` and `right`. If characters match, move both inward. On mismatch, try removing `left` or removing `right` and check if the remainder is a palindrome. Helper `is_palindrome(l, r)` checks `s[l..r]`. Main: walk until mismatch, then return `is_palindrome(left+1, right) or is_palindrome(left, right-1)`.

> [!note]- Python Solution
> ```python
> def valid_palindrome(s):
>     def is_palindrome(left, right):
>         while left < right:
>             if s[left] != s[right]:
>                 return False
>             left += 1
>             right -= 1
>         return True
> >
>     left = 0
>     right = len(s) - 1
>     while left < right:
>         if s[left] != s[right]:
>             return is_palindrome(left + 1, right) or is_palindrome(left, right - 1)
>         left += 1
>         right -= 1
>     return True
> ```

> [!success] Complexity
> Time O(n), Space O(1).

> [!tip] Alternatives
> - Check all single-character deletions: O(n²) — correct but too slow.
> - Key insight: once we find a mismatch, we only try removing one of the two mismatching characters — no need to try every position.

**Also try:**

- **String Compression** — We need to write compressed output back into the same array, so one pointer reads runs and another pointer writes results
- **Zigzag Conversion (LC 6)** — Rather than simulating the 2D grid (wastes space), we can directly assign each character to its row number by tracking which row we're curre…
- **Reverse Words in a String (LC 151)** — Python's `split()` without arguments handles multiple spaces and strips leading/trailing whitespace

---

## See Also

[[two-pointers]] | [[sliding-window]] | [[hashing]] | [[string-algorithms]]
