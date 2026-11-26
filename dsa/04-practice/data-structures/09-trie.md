---
tags: [coding, data-structures, trie]
topic: Trie
difficulty: mixed
---
# Trie Problems

## What this covers

> [!abstract] In this file
> **Covers:** Worked trie problems: implementation, autocomplete, Trie + backtracking, XOR trie.
> **You'll be able to:** Implement and apply a trie in an interview setting.
> **Prereqs:** Trie lecture · **Pair with:** [Trie lecture](../../02-data-structures/09-trie.md) · **Time:** 2 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Core Trie Implementation](#core-trie-implementation) · [Autocomplete / Prefix Search](#autocomplete--prefix-search) · [Trie + Backtracking](#trie--backtracking) · [XOR Trie](#xor-trie) · [Bitwise Trie / Other](#bitwise-trie--other) · [Trie Applications](#trie-applications)

> [!tip] If you only have 20 minutes
> **Do these first:** [Implement Trie (Prefix Tree)](#implement-trie-prefix-tree--t1) · [Add and Search Word](#add-and-search-word--t1) · [Word Search II](#word-search-ii--t1) · [Search Suggestions System](#search-suggestions-system--t1) · [Replace Words](#replace-words-lc-648--t1) · [Maximum XOR of Two Numbers in an Array](#maximum-xor-of-two-numbers-in-an-array--t1)
> **Template:** Node = `{children: dict, end: bool}` (or `word: str` to avoid rebuilding paths). Insert/search are the same loop; only the final check differs.
> **Template:** Bitwise trie for XOR: insert 31→0 bits; greedily take the opposite bit at each level.
> **Gotchas:** `search` vs `startsWith` differ only on the `end` check · Word Search II: prune the trie (delete finished leaves) and clear `node.word` to avoid duplicates · `.` wildcard → DFS over all children.

---

Pattern tags: trie insert/search, prefix search, backtracking, XOR trie, suffix trie.

---

## Core Trie Implementation

---

### Implement Trie (Prefix Tree) `⚡ T1`

> [!example] Problem
> A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker.
> Implement the Trie class
> 
> **Example 1:**
> ```
> Input
> ["Trie", "insert", "search", "search", "startsWith", "insert", "search"]
> [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]]
> Output
> [null, null, true, false, true, null, true]
> 
> Explanation
> Trie trie = new Trie();
> trie.insert("apple");
> trie.search("apple");   // return True
> trie.search("app");     // return False
> trie.startsWith("app"); // return True
> trie.insert("app");
> trie.search("app");     // return True
> ```
> 
> **Constraints:**
> - 1 <= word.length, prefix.length <= 2000
> - word and prefix consist only of lowercase English letters.
> - At most 3 * 10^4 calls in total will be made to insert, search, and startsWith.

> [!tip] Recognize · Gotcha
> **Gotcha:** Don't forget `is_end = True` after inserting last char

> [!info] Approach
> A hash set gives O(L) exact match but cannot answer "does any word start with prefix X?" without scanning all keys — O(N × L). A Trie shares common prefixes as tree paths, enabling O(L) prefix queries regardless of dictionary size N. N-ary tree where each edge carries one character. Each node holds a `children` dict and an `is_end` flag. The path from root to any node marked `is_end = True` spells a complete word.

>   - `insert`: walk the tree character by character, creating nodes as needed, set `is_end = True` at the last character.
>   - `search`: walk the tree; return False if any character is missing; return `node.is_end` at the end — this distinguishes "apple" (exact) from "app" (only prefix).
>   - `startsWith`: same walk as search but return True after the walk completes regardless of `is_end`.
> - **EDGE CASES:** The empty string is valid only if you explicitly mark the root as terminal; duplicate inserts are idempotent with a boolean trie; deletes must prune only dead branches so shared prefixes stay intact.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children: dict[str, TrieNode] = {}
>         self.is_end: bool = False
> 
> class Trie:
>     def __init__(self):
>         self.root = TrieNode()
> 
>     def insert(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = TrieNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def search(self, word):
>         node = self._walk(word)
>         return node is not None and node.is_end
> 
>     def starts_with(self, prefix):
>         return self._walk(prefix) is not None
> 
>     def _walk(self, s):
>         node = self.root
>         for c in s:
>             if c not in node.children:
>                 return None
>             node = node.children[c]
>         return node
> 
>     def delete(self, word):
>         """Remove word; prune dead branches. Returns True if word existed."""
>         def _del(node, depth):
>             if depth == len(word):
>                 if not node.is_end:
>                     return False, False
>                 node.is_end = False
>                 return True, len(node.children) == 0   # safe to prune if leaf
>             c = word[depth]
>             if c not in node.children:
>                 return False, False
>             existed, should_prune_child = _del(node.children[c], depth + 1)
>             if should_prune_child:
>                 del node.children[c]
>             return existed, not node.is_end and len(node.children) == 0
>         existed, _ = _del(self.root, 0)
>         return existed
> ```

> [!success] Complexity
> Time O(L) per operation where L = word/prefix length. Space O(total stored characters) with `dict` children, or O(nodes × Σ) with a fixed child array. If the alphabet is sparse or unknown, `dict` is usually the right tradeoff.

> [!tip] Alternatives
> - Hash set: O(L) exact search, O(N × L) prefix scan — no true prefix query support.
> - Sorted list + binary search: O(log N) prefix range, O(N) insert — no O(L) guarantee.
> - Fixed `children[26]` array instead of dict: faster constant (array index vs hash), but 26× memory waste for sparse alphabets.

---

### Add and Search Word `⚡ T1`

> [!example] Problem
> Design a data structure with `addWord(word)` and `search(word)`. `search` supports the wildcard character `.` which matches any single letter. Return true if the word (with wildcards) matches any previously added word.

> [!info] Approach
> Exact-match trie search is O(L). The `.` wildcard requires branching — at each `.` we must try all children. A standard trie provides the tree structure needed for this DFS with branching. Standard trie insert. Search becomes a recursive DFS: literal characters follow the exact child; `.` recursively searches all children at the current node. `addWord`: standard trie insert. `search(word, node, i)`: if `i == len(word)` return `node.is_end`. If `word[i] == '.'`, recurse into every child and return True if any succeeds. Otherwise follow the exact child as usual.

> [!note]- Python Solution
> ```python
> class WCNode:
>     def __init__(self):
>         self.children: dict[str, WCNode] = {}
>         self.is_end: bool = False
> 
> class WordDictionary:
>     def __init__(self):
>         self.root = WCNode()
> 
>     def add_word(self, word):
>         node = self.root
>         for c in word:
>             if c not in node.children:
>                 node.children[c] = WCNode()
>             node = node.children[c]
>         node.is_end = True
> 
>     def search(self, word):
>         return self._dfs(self.root, word, 0)
> 
>     def _dfs(self, node, word, i):
>         if i == len(word):
>             return node.is_end
>         c = word[i]
>         if c == '.':
>             for child in node.children.values():
>                 if self._dfs(child, word, i + 1):
>                     return True
>             return False
>         if c not in node.children:
>             return False
>         return self._dfs(node.children[c], word, i + 1)
> ```

> [!success] Complexity
> Time O(L) average; O(26^L) worst case for an all-`.` pattern against a full dictionary of L-length words. Space O(N × L) for the trie.

> [!tip] Alternatives
> - Regex: `re.fullmatch` on every stored word — O(N × L) per query. Simple but doesn't scale.
> - Hash map per word length: group words by length; for `.` patterns, scan the right bucket — still O(N × L) per query in the worst case.

---

### Implement Trie II (Count Prefixes and Equal Words) `⚡ T1`

> [!example] Problem
> Extend a trie so you can count how many words equal a string and how many words have a given prefix.

> [!info] Approach
> Standard trie nodes need counters, not just child pointers, when queries ask for multiplicity. Each node stores `pass` (words passing through) and `end` (words ending here). Increment `pass` while descending during insertion and increment `end` at the final node. Decrement counters on erase.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children = {}
>         self.pass_count = 0
>         self.end_count = 0
> 
> class Trie:
>     def __init__(self):
>         self.root = TrieNode()
> ```

> [!success] Complexity
> O(L) per insert/search/erase, where `L` is the word length.

> [!tip] Alternatives
> A hash map can count whole words, but prefix counts require a trie or another prefix-aware structure.

---

## Autocomplete / Prefix Search

---

### Search Suggestions System `⚡ T1`

> [!example] Problem
> You are given an array of strings products and a string searchWord.
> Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.
> Return a list of lists of the suggested products after each character of searchWord is typed.
> 
> **Example 1:**
> ```
> Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
> Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
> Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
> After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
> After typing mou, mous and mouse the system suggests ["mouse","mousepad"].
> ```
> 
> **Example 2:**
> ```
> Input: products = ["havana"], searchWord = "havana"
> Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
> Explanation: The only word "havana" will be always suggested while typing the search word.
> ```
> 
> **Constraints:**
> - 1 <= products.length <= 1000
> - 1 <= products[i].length <= 3000
> - 1 <= sum(products[i].length) <= 2 * 10^4
> - All the strings of products are unique.
> - products[i] consists of lowercase English letters.
> - 1 <= searchWord.length <= 1000
> - searchWord consists of lowercase English letters.

> [!info] Approach
> After inserting and sorting, a trie lets us walk to the prefix node once and collect the first 3 words in lexicographic order via a bounded DFS — O(prefix_length + output) per query. Insert all products (sorted) into the trie. At each node store up to 3 of the lexicographically smallest words that pass through it (filled at insert time since we sort first). Sort `products`. Insert each: at every node on the path, append the word to `node.suggestions` if `len < 3`. Query: walk the search word prefix character by character; at each step return `node.suggestions` (or `[]` if the branch doesn't exist, and stay dead for subsequent characters).

> [!note]- Python Solution
> ```python
> class SSNode:
>     def __init__(self):
>         self.children: dict[str, SSNode] = {}
>         self.suggestions: list[str] = []
> 
> class Solution:
>     def suggested_products(self, products, searchWord):
>         root = SSNode()
>         for product in sorted(products):
>             node = root
>             for c in product:
>                 if c not in node.children:
>                     node.children[c] = SSNode()
>                 node = node.children[c]
>                 if len(node.suggestions) < 3:
>                     node.suggestions.append(product)
> 
>         result = []
>         node: SSNode | None = root
>         for c in searchWord:
>             if node and c in node.children:
>                 node = node.children[c]
>             else:
>                 node = None
>             result.append(node.suggestions if node else [])
>         return result
> ```

> [!success] Complexity
> Time O(N × L log(N × L)) to sort and insert + O(|searchWord|) to query. Space O(N × L).

> [!tip] Alternatives
> - Binary search on sorted list: for each prefix, binary-search the start and collect next 3 — O(N log N) sort + O(L × log N) query. Simpler, nearly as fast in practice.
> - Two-pointer on sorted array: same idea but with `bisect_left` — O(log N) per prefix.

**Also try:**

- **Map Sum Pairs** — A trie propagates prefix sums naturally — each node on the insertion path of a key can accumulate that key's value
- **Longest Word in Dictionary** — "Each prefix must also be in the dictionary" maps exactly to "each ancestor in the trie must have `is_end = True`"
- **Count Words With Given Prefix** — A trie answers prefix-count queries in O(L) after O(N × L) build — count of words in the subtree rooted at the prefix node
- **Implement Magic Dictionary** — We need "exactly one substitution" match, not exact or prefix match

---

## Trie + Backtracking

---

### Word Search II `⚡ T1`

> [!example] Problem
> Given an m x n board of characters and a list of strings words, return all words on the board.
> Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
> 
> **Example 1:**
> ```
> Input: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = ["oath","pea","eat","rain"]
> Output: ["eat","oath"]
> ```
> 
> **Example 2:**
> ```
> Input: board = [["a","b"],["c","d"]], words = ["abcb"]
> Output: []
> ```
> 
> **Constraints:**
> - m == board.length
> - n == board[i].length
> - 1 <= m, n <= 12
> - board[i][j] is a lowercase English letter.
> - 1 <= words.length <= 3 * 10^4
> - 1 <= words[i].length <= 10
> - words[i] consists of lowercase English letters.
> - All the strings of words are unique.

> [!tip] Recognize · Gotcha
> **Gotcha:** Mark visited with `#`; prune dead trie nodes after finding to cut later DFS

> [!info] Approach
> Searching the board independently for each word is O(W × M × 4 × 3^(L-1)) where W = words, M = board cells, L = max word length. The trie prunes entire word subtrees: if the current board path matches no trie prefix, stop immediately — shared prefixes across words are explored only once. Trie of all target words. DFS from every board cell; at each step check if the current character exists in the current trie node's children. Build trie, storing the actual word string at `is_end` nodes. DFS: if `ch` not in `node.children`, return immediately. If `node.word` is set, record and clear it (deduplication). Mark cell as `'#'` during DFS; restore on backtrack. After DFS, prune dead trie nodes (`del node.children[ch]` when subtree is empty) to avoid re-exploring exhausted branches.

> [!note]- Python Solution
> ```python
> class WSNode:
>     def __init__(self):
>         self.children: dict[str, WSNode] = {}
>         self.word: str | None = None   # stores the full word at the end node
> 
> def find_words(board, words):
>     root = WSNode()
>     for w in words:
>         node = root
>         for c in w:
>             node = node.children.setdefault(c, WSNode())
>         node.word = w
> 
>     rows, cols = len(board), len(board[0])
>     result = []
> 
>     def dfs(node, r, c):
>         ch = board[r][c]
>         if ch not in node.children:
>             return
>         next_node = node.children[ch]
>         if next_node.word:
>             result.append(next_node.word)
>             next_node.word = None   # deduplicate: clear so same word isn't found again
>         board[r][c] = '#'   # mark visited
>         for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
>             nr, nc = r + dr, c + dc
>             if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] != '#':
>                 dfs(next_node, nr, nc)
>         board[r][c] = ch   # restore
>         # prune empty subtree — critical for performance
>         if not next_node.children and not next_node.word:
>             del node.children[ch]
> 
>     for r in range(rows):
>         for c in range(cols):
>             dfs(root, r, c)
>     return result
> ```

> [!success] Complexity
> Time O(M × 4 × 3^(L-1)) where M = board cells, L = max word length — 3 because after the first step, the cell we came from is marked visited (not 4). Trie pruning makes this much faster in practice. Space O(W × L) for trie.

> [!tip] Alternatives
> - DFS per word: O(W × M × 3^L) — no shared prefix benefit.
> - BFS per word: BFS doesn't naturally handle the "no cell reuse per word" constraint — DFS + backtracking is the fit.

---

## XOR Trie

---

### Maximum XOR of Two Numbers in an Array `⚡ T1`

> [!example] Problem
> Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.
> 
> **Example 1:**
> ```
> Input: nums = [3,10,5,25,2,8]
> Output: 28
> Explanation: The maximum result is 5 XOR 25 = 28.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [14,70,53,83,49,91,36,80,92,51,66,70]
> Output: 127
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 2 * 10^5
> - 0 <= nums[i] <= 2^{31} - 1

> [!tip] Recognize · Gotcha
> **Gotcha:** Process bits from MSB (bit 31) to LSB; handle negative numbers with sign bit

> [!info] Approach
> Brute force is O(n²). XOR is maximized bit by bit from the MSB. A binary trie lets us greedily pick the opposite bit at each level, constructing the maximum XOR in O(32) per element after O(32n) build. Binary trie where each number is inserted bit by bit from bit 31 (MSB) to bit 0. For each number, greedily navigate the trie choosing the opposite bit to maximize XOR contribution at each level. `insert(num)`: for bits 31 → 0, compute `b = (num >> bit) & 1`, follow or create the `b` branch. `max_xor(num)`: for each bit, try to go to `1 - b` (opposite = XOR bit = 1); if that branch exists, take it and add `1 << bit` to the XOR; otherwise take the `b` branch. Build the trie with all numbers, then query each number for its best XOR pair.

> [!note]- Python Solution
> ```python
> class XORNode:
>     def __init__(self):
>         self.children: dict[int, XORNode] = {}
> 
> class XORTrie:
>     def __init__(self):
>         self.root = XORNode()
> 
>     def insert(self, num):
>         node = self.root
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             if b not in node.children:
>                 node.children[b] = XORNode()
>             node = node.children[b]
> 
>     def max_xor(self, num):
>         node = self.root
>         xor = 0
>         for bit in range(31, -1, -1):
>             b = (num >> bit) & 1
>             want = 1 - b   # opposite bit maximizes XOR at this position
>             if want in node.children:
>                 xor |= (1 << bit)
>                 node = node.children[want]
>             else:
>                 node = node.children[b]
>         return xor
> 
> def find_maximum_xor(nums):
>     trie = XORTrie()
>     for n in nums:
>         trie.insert(n)
>     return max(trie.max_xor(n) for n in nums)
> ```

> [!success] Complexity
> Time O(32n) = O(n). Space O(32n) = O(n).

> [!tip] Alternatives
> - Brute force O(n²): try all pairs — correct, too slow for large inputs.
> - Prefix XOR + hash set: for each bit from MSB, assume that bit can be 1 in the answer, check if the required pair exists using a prefix hash set — O(32n), same complexity, no trie, harder to reason about.

**Also try:**

- **Maximum XOR With an Element From Array** — If we could insert all `nums` freely, a standard XOR trie answers each query in O(32)

---

## Bitwise Trie / Other

---

### Palindrome Pairs `⚡ T1`

> [!example] Problem
> You are given a 0-indexed array of unique strings words.
> A palindrome pair is a pair of integers (i, j) such that:
> Return an array of all the palindrome pairs of words.
> You must write an algorithm with O(sum of words[i].length) runtime complexity.
> 
> **Example 1:**
> ```
> Input: words = ["abcd","dcba","lls","s","sssll"]
> Output: [[0,1],[1,0],[3,2],[2,4]]
> Explanation: The palindromes are ["abcddcba","dcbaabcd","slls","llssssll"]
> ```
> 
> **Example 2:**
> ```
> Input: words = ["bat","tab","cat"]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["battab","tabbat"]
> ```
> 
> **Example 3:**
> ```
> Input: words = ["a",""]
> Output: [[0,1],[1,0]]
> Explanation: The palindromes are ["a","a"]
> ```
> 
> **Constraints:**
> - 1 <= words.length <= 5000
> - 0 <= words[i].length <= 300
> - words[i] consists of lowercase English letters.

> [!info] Approach
> Brute force O(N² × L). A trie of reversed words reduces the search: for each word `w`, we look for reversed words that can pair with it to form a palindrome. Insert all reversed words into a trie, tagging each end node with the word's index. For each word `w`, walk the trie with `w`'s characters; if we reach a word end before exhausting `w`, check if the remaining suffix of `w` is a palindrome (then `w + rev_word` is a palindrome). If we exhaust `w` first, collect all words in the trie subtree whose corresponding remaining suffix is a palindrome. At each trie node, store a list of word indices whose reversed word ends here but the trie path continues — these are "prefix palindrome" candidates. Walk trie with `w`; if `node.word_idx != -1` and the remaining `w[i:]` is a palindrome, record `(word_idx, i_word)`. After exhausting `w`, collect from `node.palindrome_suffixes` (stored during build).

> [!note]- Python Solution
> ```python
> def palindrome_pairs(words):
>     def is_palindrome(s):
>         return s == s[::-1]
> 
>     word_map = {w: i for i, w in enumerate(words)}
>     result = []
> 
>     for i, word in enumerate(words):
>         n = len(word)
>         for j in range(n + 1):
>             # Case 1: word[:j] is palindrome → rev(word[j:]) + word is palindrome
>             prefix, suffix = word[:j], word[j:]
>             if is_palindrome(prefix):
>                 rev_suf = suffix[::-1]
>                 if rev_suf in word_map and word_map[rev_suf] != i:
>                     result.append([word_map[rev_suf], i])
>             # Case 2: word[j:] is palindrome → word + rev(word[:j]) is palindrome
>             if j < n and is_palindrome(suffix):
>                 rev_pre = prefix[::-1]
>                 if rev_pre in word_map and word_map[rev_pre] != i:
>                     result.append([i, word_map[rev_pre]])
>         # Avoid duplicates when j == 0 in both cases (empty prefix/suffix overlap)
>     return result
> ```

> [!success] Complexity
> Time O(N × L²) — N words, each generates O(L) splits, palindrome check O(L) each. Space O(N × L) for hash map.

> [!tip] Alternatives
> - Trie of reversed words (true trie approach): walk each word through the reversed-word trie; at each step check partial palindromes — same O(N × L²) complexity, more complex code with similar performance in Python.
> - Brute force with hash map: check `word + rev(other_word)` — O(N² × L).

---

### Design Search Autocomplete System (Trie + DFS Variant) `⚡ T1`

> [!example] Problem
> Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character `'#'`).
> 
> You are given a string array `sentences` and an integer array `times` both of length `n` where `sentences[i]` is a previously typed sentence and `times[i]` is the corresponding number of times the sentence was typed. For each input character except `'#'`, return the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed.
> 
> Here are the specific rules:
> 
> 	
> - The hot degree for a sentence is defined as the number of times a user typed the exactly same sentence before.
> 	
> - The returned top `3` hot sentences should be sorted by hot degree (The first is the hottest one). If several sentences have the same hot degree, use ASCII-code order (smaller one appears first).
> 	
> - If less than `3` hot sentences exist, return as many as you can.
> 	
> - When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.
> 
> Implement the `AutocompleteSystem` class:
> 
> 	
> - `AutocompleteSystem(String[] sentences, int[] times)` Initializes the object with the `sentences` and `times` arrays.
> 	`List<String> input(char c)` This indicates that the user typed the character `c`.
> 	
> 		
> - Returns an empty array `[]` if `c == '#'` and stores the inputted sentence in the system.
> 		
> - Returns the top `3` historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than `3` matches, return them all.
> 	
> 	
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input**
> ["AutocompleteSystem", "input", "input", "input", "input"]
> [[["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]], ["i"], [" "], ["a"], ["#"]]
> **Output**
> [null, ["i love you", "island", "i love leetcode"], ["i love you", "i love leetcode"], [], []]
> 
> **Explanation**
> AutocompleteSystem obj = new AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]);
> obj.input("i"); // return ["i love you", "island", "i love leetcode"]. There are four sentences that have prefix "i". Among them, "ironman" and "i love leetcode" have same hot degree. Since ' ' has ASCII code 32 and 'r' has ASCII code 114, "i love leetcode" should be in front of "ironman". Also we only need to output top 3 hot sentences, so "ironman" will be ignored.
> obj.input(" "); // return ["i love you", "i love leetcode"]. There are only two sentences that have prefix "i ".
> obj.input("a"); // return []. There are no sentences that have prefix "i a".
> obj.input("#"); // return []. The user finished the input, the sentence "i a" should be saved as a historical sentence in system. And the following input will be counted as a new search.
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `n == sentences.length`
> 	
> - `n == times.length`
> 	
> - `1 <= n <= 100`
> 	
> - `1 <= sentences[i].length <= 100`
> 	
> - `1 <= times[i] <= 50`
> 	
> - `c` is a lowercase English letter, a hash `'#'`, or space `' '`.
> 	
> - Each tested sentence will be a sequence of characters `c` that end with the character `'#'`.
> 	
> - Each tested sentence will have a length in the range `[1, 200]`.
> 	
> - The words in each input sentence are separated by single spaces.
> 	
> - At most `5000` calls will be made to `input`.

> [!tip] Recognize · Gotcha
> **Gotcha:** Store top-3 at each node (lazy — update on insert) to avoid DFS on every query

> [!info] Approach
> The main LC 642 solution stores all sentences at every ancestor node — O(S × L) extra space. This variant stores only frequency at terminal nodes; DFS is O(output) per query but saves memory. Trie with `freq` at terminal nodes only. Query: walk to prefix node, run DFS to collect all `(freq, sentence)` pairs, return top 3 by `(-freq, sentence)`. `insert(sentence, freq)`: standard trie, set `node.freq = freq` at terminal. `query(prefix)`: walk to prefix node. DFS collecting `(freq, built_string)` for all `is_end` nodes. Sort and return top 3.

> [!note]- Python Solution
> ```python
> class ACNode2:
>     def __init__(self):
>         self.children: dict[str, ACNode2] = {}
>         self.freq: int = 0
> 
> class AutocompleteSystemV2:
>     def __init__(self, sentences, times):
>         self.root = ACNode2()
>         self.curr_prefix: list[str] = []
>         self.curr_node: ACNode2 | None = self.root
>         for s, t in zip(sentences, times):
>             self._insert(s, t)
> 
>     def _insert(self, sentence, freq):
>         node = self.root
>         for c in sentence:
>             if c not in node.children:
>                 node.children[c] = ACNode2()
>             node = node.children[c]
>         node.freq += freq
> 
>     def _dfs(self, node, path, results, str]]):
>         if node.freq > 0:
>             results.append((node.freq, ''.join(path)))
>         for ch, child in node.children.items():
>             path.append(ch)
>             self._dfs(child, path, results)
>             path.pop()
> 
>     def input(self, c):
>         if c == '#':
>             sentence = ''.join(self.curr_prefix)
>             self._insert(sentence, 1)
>             self.curr_prefix = []
>             self.curr_node = self.root
>             return []
>         self.curr_prefix.append(c)
>         if self.curr_node and c in self.curr_node.children:
>             self.curr_node = self.curr_node.children[c]
>         else:
>             self.curr_node = None
>         if not self.curr_node:
>             return []
>         results = []
>         self._dfs(self.curr_node, self.curr_prefix[:], results)
>         results.sort(key=lambda x: (-x[0], x[1]))
>         return [s for _, s in results[:3]]
> ```

> [!success] Complexity
> Time O(p + output × L) per input character where p = prefix length, output = matching sentences. Space O(N × L) — no per-node sentence lists.

> [!tip] Alternatives
> - Per-node cached lists (LC 642 main solution): O(1) query time after O(S × L) build space — trades memory for speed.

**Also try:**

- **Design File System** — A trie over path components (split by `/`) models the hierarchical file system naturally
- **Stream of Characters** — Checking all words against the current stream suffix by suffix is O(W × L) per query

---

## Trie Applications

---

### Replace Words (LC 648) `⚡ T1`

> [!example] Problem
> In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful".
> Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length.
> Return the sentence after the replacement.
> 
> **Example 1:**
> ```
> Input: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery"
> Output: "the cat was rat by the bat"
> ```
> 
> **Example 2:**
> ```
> Input: dictionary = ["a","b","c"], sentence = "aadsfasf absbs bbab cadsfafs"
> Output: "a a b c"
> ```
> 
> **Constraints:**
> - 1 <= dictionary.length <= 1000
> - 1 <= dictionary[i].length <= 100
> - dictionary[i] consists of only lower-case letters.
> - 1 <= sentence.length <= 10^6
> - sentence consists of only lower-case letters and spaces.
> - The number of words in sentence is in the range [1, 1000]
> - The length of each word in sentence is in the range [1, 1000]
> - Every two consecutive words in sentence will be separated by exactly one space.
> - sentence does not have leading or trailing spaces.

> [!tip] Recognize · Gotcha
> **Gotcha:** Return shortest root prefix, not full word

> [!info] Approach
> For each word in the sentence we need to find if any dictionary root is a prefix of it, and we want the shortest such root. A trie makes prefix lookup O(L) and naturally returns the shortest match first. Build a trie from the dictionary roots. For each word in the sentence, walk down the trie character by character. The moment you hit a terminal node (end of a root), that is the shortest matching root. Insert all roots. For each sentence word, traverse the trie; if a node has `is_end = True`, return the prefix built so far. If traversal ends without a match, keep the original word.

> [!note]- Python Solution
> ```python
> class TrieNode:
>     def __init__(self):
>         self.children = {}
>         self.is_end = False
> >
> def replace_words(dictionary, sentence):
>     root = TrieNode()
>     for word in dictionary:
>         node = root
>         for ch in word:
>             if ch not in node.children:
>                 node.children[ch] = TrieNode()
>             node = node.children[ch]
>         node.is_end = True
> >
>     def replace(word):
>         node = root
>         prefix = []
>         for ch in word:
>             if ch not in node.children:
>                 break
>             node = node.children[ch]
>             prefix.append(ch)
>             if node.is_end:
>                 return ''.join(prefix)
>         return word
> >
>     return ' '.join(replace(word) for word in sentence.split())
> ```

> [!success] Complexity
> Time O(D + S) where D = total characters in dictionary, S = total characters in sentence. Space O(D).

> [!tip] Alternatives
> - Sort dictionary by word length, check each word for prefix match: O(D * S) — too slow.
> - Key insight: stopping at the first `is_end` node guarantees the *shortest* root is returned, since shorter roots are encountered before longer ones when traversing from the root.

**Also try:**

- **Word Squares (LC 425)** — When building the square row by row, the prefix of each new row is already determined by the column values filled in so far

---

## See Also

[[string-algorithms]] | [[backtracking]] | [[hashing]]
[[string-algorithms]] | [[backtracking]] | [[hashing]] | [[dynamic-programming]]
