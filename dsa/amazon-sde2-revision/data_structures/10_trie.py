"""
Trie (Prefix Tree) patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Forgetting to mark the `is_word` or `is_end` flag when inserting.\n- Assuming every node has a value (nodes usually represent paths/edges, not the characters themselves).\n- Memory usage: Tries can take a lot of memory compared to Hash Sets.

Common Variants:
- Word Dictionary (Add / Search with wildcards)\n- Word Search II (DFS on grid + Trie)\n- Autocomplete Systems

General Tips & Best Practices:
- Use a dictionary for children: `self.children = {}` instead of an array of size 26 for cleaner code.\n- Tries are perfect for 'prefix matching' problems.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
from collections import defaultdict

class TrieNode:
    """Node definition used by trie-based interview problems."""
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    # -----------------------------------------------------------------------
    # 1. Implement Trie (Prefix Tree) (LC 208) — T1
    # A trie (pronounced as "try") or prefix tree is a tree data structure used to efficiently store and retrieve keys in a dataset of strings. There are various applications of this data structure, such as autocomplete and spellchecker. Implement the Trie class: before), and false otherwise. has the prefix prefix, and false otherwise.
    # Constraints: 1 <= word.length, prefix.length <= 2000, word and prefix consist only of lowercase English letters, At most 3 * 10^4 calls in total will be made to insert, search, and startsWith
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.root = TrieNode()

    # Time: O(n), Space: O(n)
    def insert(self, word: str) -> None:
        """LC 208: Each character in the word becomes a level in the Trie tree."""
        # Start traversal from the root node
        curr = self.root
        # Process each character in the word
        for c in word:
            # If the character does not exist, create a new node
            if c not in curr.children:
                curr.children[c] = TrieNode()
            # Move to the child node
            curr = curr.children[c]
        # Mark the final node as a word ending
        curr.is_end = True

    # Time: O(n), Space: O(1)
    def search(self, word: str) -> bool:
        # Start traversal from the root node
        curr = self.root
        # Process each character in the word
        for c in word:
            # If character not found, word does not exist
            if c not in curr.children:
                return False
            # Move to the child node
            curr = curr.children[c]
        # Return True if it's marked as a complete word
        return curr.is_end

    # Time: O(n), Space: O(1)
    def startsWith(self, prefix: str) -> bool:
        # Start traversal from the root node
        curr = self.root
        # Process each character in the prefix
        for c in prefix:
            # If any character is missing, prefix does not exist
            if c not in curr.children:
                return False
            # Move to the child node
            curr = curr.children[c]
        # All characters in the prefix were found
        return True

class WordSearchIITrieNode:
    def __init__(self):
        self.children = {}
        self.word = None

class TrieSolutions:
    # -----------------------------------------------------------------------
    # 2. Word Search II (LC 212) — T1
    # Given an m x n board of characters and a list of strings words, return all words on the board. Each word must be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.
    # Example: board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]], words = → ["eat","oath"]
    # Constraints: m == board.length, n == board[i].length, 1 <= m, n <= 12, board[i][j] is a lowercase English letter, 1 <= words.length <= 3 * 10^4, 1 <= words[i].length <= 10, words[i] consists of lowercase English letters, All the strings of words are unique
    # Time: O(m*n*4^L + W*L), Space: O(W*L)
    # -----------------------------------------------------------------------
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = WordSearchIITrieNode()
        for w in words:
            curr = root
            for c in w:
                if c not in curr.children:
                    curr.children[c] = WordSearchIITrieNode()
                curr = curr.children[c]
            curr.word = w

        rows, cols = len(board), len(board[0])
        res = []

        def dfs(r, c, node):
            """Depth-first-search helper for the enclosing solution."""
            if node.word:
                res.append(node.word)
                node.word = None

            if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] not in node.children:
                return

            char = board[r][c]
            board[r][c] = "#"

            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                dfs(r + dr, c + dc, node.children[char])

            board[r][c] = char
            if not node.children[char].children:
                del node.children[char]

        for r in range(rows):
            for c in range(cols):
                if board[r][c] in root.children:
                    dfs(r, c, root)
        return res

    # -----------------------------------------------------------------------
    # 3. Maximum XOR of Two Numbers (LC 421) — T1
    # Given an integer array nums, return the maximum result of nums[i] XOR nums[j], where 0 <= i <= j < n.
    # Time: O(n*32), Space: O(n*32)
    # -----------------------------------------------------------------------
    def findMaximumXOR(self, nums: List[int]) -> int:
        # Initialize binary trie root
        root = {}
        # Insert each number bit-by-bit from MSB to LSB
        for num in nums:
            node = root
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                if bit not in node:
                    node[bit] = {}
                node = node[bit]

        max_xor = 0
        # For each number, query the trie greedily to maximize XOR
        for num in nums:
            node = root
            curr_xor = 0
            for i in range(31, -1, -1):
                bit = (num >> i) & 1
                toggled = 1 - bit
                # Prefer the opposite bit branch to maximize XOR
                if toggled in node:
                    curr_xor |= (1 << i)
                    node = node[toggled]
                else:
                    node = node[bit]
            max_xor = max(max_xor, curr_xor)
        return max_xor

    # -----------------------------------------------------------------------
    # 4. Replace Words (LC 648) — T1
    # In English, we have a concept called root, which can be followed by some other word to form another longer word - let's call this word derivative. For example, when the root "help" is followed by the word "ful", we can form a derivative "helpful". Given a dictionary consisting of many roots and a sentence consisting of words separated by spaces, replace all the derivatives in the sentence with the root forming it. If a derivative can be replaced by more than one root, replace it with the root that has the shortest length. Return the sentence after the replacement.
    # Example: dictionary = ["cat","bat","rat"], sentence = "the cattle was rattled by the battery" → "the cat was rat by the bat"
    # Constraints: 1 <= dictionary.length <= 1000, 1 <= dictionary[i].length <= 100, dictionary[i] consists of only lower-case letters, 1 <= sentence.length <= 10^6, sentence consists of only lower-case letters and spaces, The number of words in sentence is in the range [1, 1000], The length of each word in sentence is in the range [1, 1000], Every two consecutive words in sentence will be separated by exactly one space, sentence does not have leading or trailing spaces
    # Time: O(D*R + S*W), Space: O(D*R)
    # -----------------------------------------------------------------------
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        """Replace Words (LC 648): Insert every root from the dictionary into a Trie."""
        # Initialize Trie with all roots
        root = TrieNode()
        for word in dictionary:
            curr = root
            for c in word:
                if c not in curr.children:
                    curr.children[c] = TrieNode()
                curr = curr.children[c]
            curr.is_end = True

        res = []
        # Process each word in the sentence
        for word in sentence.split():
            curr = root
            prefix = ""
            for c in word:
                # Stop if char not in Trie or we hit the end of a root
                if c not in curr.children or curr.is_end:
                    break
                curr = curr.children[c]
                prefix += c
            # Replace word with prefix if a valid root is found
            if curr.is_end:
                res.append(prefix)
            else:
                res.append(word)
        return " ".join(res)

class WordDictionary:
    # -----------------------------------------------------------------------
    # 5. Design Add and Search Words Data Structure (LC 211) — T2
    # Design a data structure that supports adding new words and finding if a string matches any previously added string. Implement the WordDictionary class: false otherwise. word may contain dots '.' where dots can be matched with any letter.
    # Constraints: 1 <= word.length <= 25, word in addWord consists of lowercase English letters, word in search consist of '.' or lowercase English letters, There will be at most 2 dots in word for search queries, At most 10^4 calls will be made to addWord and search
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.root = TrieNode()

    # Time: O(n), Space: O(n)
    def addWord(self, word: str) -> None:
        # Start from the root of WordDictionary
        curr = self.root
        # Process each character of the word
        for c in word:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        # Mark word ending
        curr.is_end = True

    # Time: O(n*26^d) where d is number of dots, Space: O(n)
    def search(self, word: str) -> bool:
        def dfs(j, root):
            """Depth-first-search helper for the enclosing solution."""
            curr = root
            # Iterate through the word from index j
            for i in range(j, len(word)):
                c = word[i]
                # Wildcard case: branch to all children
                if c == '.':
                    for child in curr.children.values():
                        if dfs(i + 1, child):
                            return True
                    return False
                # Standard character matching
                else:
                    if c not in curr.children:
                        return False
                    curr = curr.children[c]
            # Verify if path ends on a valid word
            return curr.is_end
        # Launch DFS starting at index 0 from root
        return dfs(0, self.root)

class TrieSolutionsT2:
    # -----------------------------------------------------------------------
    # 6. Longest Word in Dictionary (LC 720) — T2
    # Given an array of strings words representing an English Dictionary, return the longest word in words that can be built one character at a time by other words in words. If there is more than one possible answer, return the longest word with the smallest lexicographical order. If there is no answer, return the empty string. Note that the word should be built from left to right with each additional character being added to the end of a previous word.
    # Example: words = ["w","wo","wor","worl","world"] → "world"
    # Constraints: 1 <= words.length <= 1000, 1 <= words[i].length <= 30, words[i] consists of lowercase English letters
    # Time: O(W*L*log W), Space: O(W*L)
    # -----------------------------------------------------------------------
    def longestWord(self, words: List[str]) -> str:
        # Sort words lexicographically
        words.sort()
        # Initialize word set with empty prefix base case
        word_set = set([""])
        res = ""
        # Check if the prefix of each word exists in the set
        for w in words:
            if w[:-1] in word_set:
                word_set.add(w)
                # Track the longest word found
                if len(w) > len(res):
                    res = w
        return res

class MapSum:
    # -----------------------------------------------------------------------
    # 7. Map Sum Pairs (LC 677) — T2
    # Design a map that allows you to do the following: Implement the MapSum class: existed, the original key-value pair will be overridden to the new one.
    # Constraints: 1 <= key.length, prefix.length <= 50, key and prefix consist of only lowercase English letters, 1 <= val <= 1000, At most 50 calls will be made to insert and sum
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.root = TrieNode()
        self.map = {}

    # Time: O(n), Space: O(n)
    def insert(self, key: str, val: int) -> None:
        """Map Sum Pairs (LC 677): Insert the key character by character into a Trie."""
        # Calculate delta diff for key update/insertion
        diff = val - self.map.get(key, 0)
        self.map[key] = val
        curr = self.root
        # Insert key and propagate diff score to all node prefix paths
        for c in key:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
            if not hasattr(curr, 'score'): curr.score = 0
            curr.score += diff

    # Time: O(n), Space: O(1)
    def sum(self, prefix: str) -> int:
        curr = self.root
        # Walk prefix in Trie
        for c in prefix:
            if c not in curr.children:
                return 0
            curr = curr.children[c]
        # Return aggregated score at the prefix node
        return getattr(curr, 'score', 0)

class AutocompleteNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class AutocompleteSystem:
    # -----------------------------------------------------------------------
    # 8. Design Search Autocomplete System (LC 642) — T1
    # Design a search autocomplete system for a search engine. Stores top-3 hot sentences at each node to avoid DFS on every keystroke
    # Time: O(S*L), Space: O(S*L)
    # -----------------------------------------------------------------------
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = AutocompleteNode()
        self.freq = {}
        self.cur_input = ""
        for s, t in zip(sentences, times):
            self.freq[s] = self.freq.get(s, 0) + t
            self._add(s)

    # Time: O(n), Space: O(n)
    def _add(self, sentence: str) -> None:
        """Adds a value to the underlying data structure."""
        node = self.root
        # Traverse and insert sentence into Trie
        for c in sentence:
            if c not in node.children:
                node.children[c] = AutocompleteNode()
            node = node.children[c]
        # Mark sentence ending node
        node.is_end = True

    # Time: O(P + K*log K), Space: O(K)
    def input(self, c: str) -> List[str]:
        if c == '#':
            # Commit current sentence and reset state
            self.freq[self.cur_input] = self.freq.get(self.cur_input, 0) + 1
            self._add(self.cur_input)
            self.cur_input = ""
            return []
        self.cur_input += c
        # Walk to current prefix node
        node = self.root
        for ch in self.cur_input:
            if ch not in node.children:
                return []
            node = node.children[ch]
        # DFS to gather all completions
        res = []
        def dfs(n, path):
            """Depth-first-search helper for the enclosing solution."""
            # Collect frequencies of valid sentences found
            if n.is_end:
                res.append((self.freq.get(path, 0), path))
            # Recurse through all children branches
            for ch, child in n.children.items():
                dfs(child, path + ch)
        # Gather matching results
        dfs(node, self.cur_input)
        # Return top 3: sort by (-freq, sentence)
        res.sort(key=lambda x: (-x[0], x[1]))
        return [s for _, s in res[:3]]

class StreamChecker:
    # -----------------------------------------------------------------------
    # 9. Stream of Characters (T2) — Reverse trie of suffixes
    # Design a stream of characters that checks if the characters appended so far spell any word in the dictionary.
    # Time: O(W*L), Space: O(W*L)
    # -----------------------------------------------------------------------
    def __init__(self, words: List[str]):
        self.root = {}
        for w in words:
            node = self.root
            for ch in reversed(w):
                node = node.setdefault(ch, {})
            node['$'] = True
        self.stream = []

    # Time: O(L), Space: O(1)
    def query(self, letter: str) -> bool:
        # Append incoming letter to history
        self.stream.append(letter)
        node = self.root
        # Traverse suffix of the stream in reverse order
        for ch in reversed(self.stream):
            if ch not in node:
                return False
            node = node[ch]
            # Match found if suffix matches any dictionary word
            if node.get('$'):
                return True
        return False

# -----------------------------------------------------------------------
# 12. Implement Magic Dictionary (LC 676) — T2
# Design a data structure that is initialized with a list of different words. Provided a string, you should determine if you can change exactly one character in this string to match any word in the data structure. Implement the MagicDictionary class: dictionary. to match any string in the data structure, otherwise returns false.
# Constraints: 1 <= dictionary.length <= 100, 1 <= dictionary[i].length <= 100, dictionary[i] consists of only lower-case English letters, All the strings in dictionary are distinct, 1 <= searchWord.length <= 100, searchWord consists of only lower-case English letters, buildDict will be called only once before search, At most 100 calls will be made to search
# -----------------------------------------------------------------------
class MagicDictionary:
    # Time: O(1), Space: O(1)
    def __init__(self):
        self.words = set()
        self.count = {}

    # Time: O(L), Space: O(L)
    def _get_neighbors(self, word):
        for i in range(len(word)):
            yield word[:i] + '*' + word[i+1:]

    # Time: O(W*L), Space: O(W*L)
    def buildDict(self, dictionary: List[str]) -> None:
        # Add dictionary words to the lookup set and build wildcard count map
        for word in dictionary:
            self.words.add(word)
            for neighbor in self._get_neighbors(word):
                self.count[neighbor] = self.count.get(neighbor, 0) + 1

    # Time: O(L), Space: O(1)
    def search(self, searchWord: str) -> bool:
        # Search for neighbor pattern that matches exactly one different word
        for neighbor in self._get_neighbors(searchWord):
            c = self.count.get(neighbor, 0)
            # True if multiple matches or single match not identical to searchWord
            if c > 1 or (c == 1 and searchWord not in self.words):
                return True
        return False

class TrieSolutionsAdditional:
    # -----------------------------------------------------------------------
    # 13. Boggle Game (T3) — T3
    # Given a 2D board of characters and a list of words, find the maximum number of non-overlapping words you can find on the board.
    # Time: O(W*L + m*n*4^L + 2^P) where P is number of found paths, Space: O(W*L + P)
    # -----------------------------------------------------------------------

    # -----------------------------------------------------------------------
    # 14. Concatenated Words (LC 472) — T2
    # Given an array of strings words (without duplicates), return all the concatenated words in the given list of words. A concatenated word is defined as a string that is comprised entirely of at least two shorter words (not necessarily distinct) in the given array.
    # Example: words = ["cat","cats","catsdogcats","dog","dogcatsdog","hippopotamuses","rat","ratcatdogcat"] → ["catsdogcats","dogcatsdog","ratcatdogcat"]
    # Constraints: 1 <= words.length <= 10^4, 1 <= words[i].length <= 30, words[i] consists of only lowercase English letters, All the strings of words are unique, 1 <= sum(words[i].length) <= 10^5
    # Time: O(W*L^2), Space: O(W*L)
    # -----------------------------------------------------------------------
    def findAllConcatenatedWordsInADict(self, words: List[str]) -> List[str]:
        """Concatenated Words (LC 472): Store all words in a hash set for O(L) average-case lookup."""
        # Convert dictionary list to hash set for O(1) searches
        word_set = set(words)
        memo = {}

        def dfs(word):
            """Depth-first-search helper for the enclosing solution."""
            if word in memo:
                return memo[word]

            # Try prefix splits at indices 1 to len-1
            for i in range(1, len(word)):
                prefix = word[:i]
                suffix = word[i:]

                # Check if prefix is dictionary word and suffix is valid or concatenatable
                if prefix in word_set and (suffix in word_set or dfs(suffix)):
                    memo[word] = True
                    return True

            memo[word] = False
            return False

        # Return all words that are valid concatenations
        return [w for w in words if dfs(w)]

class TrieGoogleL4:
    # ------------------------------------------------------------------ #
    # LC 336 — Palindrome Pairs (trie-based palindrome detection)
    # Details: Given a list of unique words, return all pairs (i, j) such
    # that words[i] + words[j] is a palindrome.
    # Example:
    #   Input:  words = ["abcd","dcba","lls","s","sssll"]
    #   Output: [[0,1],[1,0],[3,2],[2,4]]
    # Constraints:
    #   - 1 <= words.length <= 5000
    #   - 0 <= words[i].length <= 300
    #   - words[i] consists of lower-case English letters
    # Time: O(W * L^2), Space: O(W * L)
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    # LC 1065 — Index Pairs of a String (trie multi-pattern match)
    # Details: Given a string text and a list of words, return all [i,j]
    # pairs such that text[i..j] (inclusive) is in words, sorted.
    # Example:
    #   Input:  text = "thestoryofleetcodeandme",
    #           words = ["story","fleet","leetcode"]
    #   Output: [[3,7],[9,13],[10,17]]
    # Constraints:
    #   - 1 <= text.length <= 100
    #   - 1 <= words.length <= 20
    #   - 1 <= words[i].length <= 50
    #   - words[i] and text consist of lower-case English letters
    # Time: O(W*L + T^2), Space: O(W*L)
    # ------------------------------------------------------------------ #
    def indexPairs(self, text: str, words: List[str]) -> List[List[int]]:
        # Build Trie with all words
        root = TrieNode()
        for word in words:
            node = root
            for c in word:
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
            node.is_end = True

        res = []
        n = len(text)
        # Search every starting position on text
        for i in range(n):
            node = root
            for j in range(i, n):
                c = text[j]
                if c not in node.children:
                    break
                node = node.children[c]
                # Collect index range if a word ends at index j
                if node.is_end:
                    res.append([i, j])
        return res

    # ------------------------------------------------------------------ #
    # LC 1268 — Search Suggestions System (trie + sorted suffixes)
    # Details: Given an array of products and a searchWord, after each
    # character typed, return up to 3 lexicographically smallest products
    # that share the current prefix.
    # Example:
    #   Input:  products = ["mobile","mouse","moneypot","monitor","mousepad"],
    #           searchWord = "mouse"
    #   Output: [["mobile","moneypot","monitor"],
    #            ["mobile","moneypot","monitor"],
    #            ["mouse","mousepad"],
    #            ["mouse","mousepad"],
    #            ["mouse","mousepad"]]
    # Constraints:
    #   - 1 <= products.length <= 1000
    #   - 1 <= products[i].length <= 3000
    #   - 1 <= searchWord.length <= 1000
    #   - All products are distinct lowercase English strings
    # Time: O(P*L*log P + S*L), Space: O(P*L)
    # ------------------------------------------------------------------ #
    def suggestedProducts(self, products: List[str], searchWord: str) -> List[List[str]]:
        class SNode:
            __slots__ = ('children', 'suggestions')
            def __init__(self):
                self.children = {}
                self.suggestions = []

        root = SNode()
        # Sort products to ensure suggestions are lexicographically sorted
        products.sort()

        # Insert products and store up to 3 suggestions at each prefix node
        for product in products:
            node = root
            for c in product:
                if c not in node.children:
                    node.children[c] = SNode()
                node = node.children[c]
                if len(node.suggestions) < 3:
                    node.suggestions.append(product)

        res = []
        node = root
        dead = False
        # Retrieve suggestions for each typed prefix character
        for c in searchWord:
            if dead or c not in node.children:
                dead = True
                res.append([])
            else:
                node = node.children[c]
                res.append(node.suggestions)
        return res



    # ------------------------------------------------------------------ #
    # LC 1707 — Maximum XOR With an Element From Array (offline + trie XOR)
    # Details: Given an integer array nums and queries[i] = [xi, mi], for
    # each query find the maximum XOR of xi with any element of nums that
    # is <= mi. If no such element exists return -1.
    # Example:
    #   Input:  nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
    #   Output: [3,3,7]
    # Constraints:
    #   - 1 <= nums.length, queries.length <= 10^5
    #   - 0 <= nums[i], xi <= 10^8
    #   - 1 <= mi <= 10^8
    # Time: O((N + Q) * log(MAX)), Space: O(N * log(MAX))
    # ------------------------------------------------------------------ #
    def maximizeXor(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        nums.sort()
        indexed_queries = sorted(enumerate(queries), key=lambda x: x[1][1])

        # Trie as list: trie[node] = [left_child, right_child]
        trie = [[-1, -1]]

        def insert(num):
            """Maximum XOR With an Element From Array (offline + trie XOR) (LC 1707). O((N + Q) * log(MAX))."""
            node = 0
            # Walk from 30th bit down to 0
            for bit in range(30, -1, -1):
                b = (num >> bit) & 1
                # If child node doesn't exist, create and link it
                if trie[node][b] == -1:
                    trie.append([-1, -1])
                    trie[node][b] = len(trie) - 1
                node = trie[node][b]

        def query_max_xor(num):
            node = 0
            xor = 0
            # Walk the Trie to maximize XOR by preferring the opposite bit
            for bit in range(30, -1, -1):
                b = (num >> bit) & 1
                want = 1 - b
                if trie[node][want] != -1:
                    xor |= (1 << bit)
                    node = trie[node][want]
                elif trie[node][b] != -1:
                    node = trie[node][b]
                else:
                    return -1
            return xor

        res = [-1] * len(queries)
        ptr = 0
        for orig_idx, (xi, mi) in indexed_queries:
            while ptr < len(nums) and nums[ptr] <= mi:
                insert(nums[ptr])
                ptr += 1
            if ptr == 0:
                res[orig_idx] = -1
            else:
                res[orig_idx] = query_max_xor(xi)
        return res


if __name__ == "__main__":
    # Trie basic
    t = Trie()
    t.insert("apple")
    assert t.search("apple") == True
    assert t.search("app") == False
    assert t.startsWith("app") == True
    t.insert("app")
    assert t.search("app") == True

    # WordDictionary (wildcard search)
    wd = WordDictionary()
    wd.addWord("bad"); wd.addWord("dad"); wd.addWord("mad")
    assert wd.search("pad") == False
    assert wd.search("bad") == True
    assert wd.search(".ad") == True
    assert wd.search("b..") == True

    # TrieSolutions
    ts = TrieSolutions()

    # findWords (Word Search II)
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    res = sorted(ts.findWords(board, ["oath","pea","eat","rain"]))
    assert res == ["eat", "oath"]

    # findMaximumXOR (Trie-based)
    assert ts.findMaximumXOR([3, 10, 5, 25, 2, 8]) == 28

    # replaceWords
    assert ts.replaceWords(["cat","bat","rat"], "the cattle was rattled by the battery") == \
           "the cat was rat by the bat"

    # TrieSolutionsT2.longestWord
    ts2 = TrieSolutionsT2()
    assert ts2.longestWord(["w","wo","wor","worl","world"]) == "world"
    assert ts2.longestWord(["a","banana","app","appl","ap","apply","apple"]) == "apple"

    # MapSum
    ms = MapSum()
    ms.insert("apple", 3)
    assert ms.sum("ap") == 3
    ms.insert("app", 2)
    assert ms.sum("ap") == 5

    # TrieGoogleL4 tests
    gl4 = TrieGoogleL4()

    # LC 1065 — Index Pairs of a String
    ip = gl4.indexPairs("thestoryofleetcodeandme", ["story","fleet","leetcode"])
    assert [3,7] in ip
    assert [9,13] in ip
    assert [10,17] in ip
    ip2 = gl4.indexPairs("ababa", ["aba","ab"])
    assert [0,1] in ip2 and [0,2] in ip2 and [2,3] in ip2 and [2,4] in ip2

    # LC 1268 — Search Suggestions System
    sugg = gl4.suggestedProducts(["mobile","mouse","moneypot","monitor","mousepad"], "mouse")
    assert sugg[0] == ["mobile","moneypot","monitor"]
    assert sugg[2] == ["mouse","mousepad"]
    assert sugg[4] == ["mouse","mousepad"]

    # LC 1707 — Maximum XOR With an Element From Array
    xor_res = gl4.maximizeXor([0,1,2,3,4], [[3,1],[1,3],[5,6]])
    assert xor_res == [3,3,7], xor_res
    xor_res2 = gl4.maximizeXor([5,2,4,6,6,3], [[12,4],[8,1],[6,3]])
    assert xor_res2 == [15,-1,5], xor_res2

    print("All trie tests passed.")



