"""
Strings patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- String concatenation in a loop `s += c` is O(N^2) in many languages (Python optimizes it sometimes, but `"".join(list)` is safer).\n- Off-by-one errors in substring slicing `s[start:end]`.\n- ASCII vs Unicode: assuming characters are only 'a'-'z' (use `ord(c) - ord('a')` carefully).

Common Variants:
- Palindromes (Expand from center, or two pointers)\n- Anagrams (Character frequency counts)\n- Sliding window on strings\n- Trie operations

General Tips & Best Practices:
- Strings are immutable in Python; convert to list if you need to modify characters heavily.\n- Use `collections.Counter` for quick anagram/frequency checks.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from collections import Counter
from typing import List

class StringSolutions:
    # -----------------------------------------------------------------------
    # 1. Minimum Window Substring — T1
    # Given two strings s and t of lengths m and n respectively, return the minimum window substring of s such that every character in t (including duplicates) is included in the window. If there is no such substring, return the empty string "". The testcases will be generated such that the answer is unique.
    # Example: s = "ADOBECODEBANC", t = "ABC" → "BANC"
    # Constraints: m == s.length, n == t.length, 1 <= m, n <= 10^5, s and t consist of uppercase and lowercase English letters, Follow up: Could you find an algorithm that runs in O(m + n) time?
    # Time: O(m + n), Space: O(m + n)
    # -----------------------------------------------------------------------
    def minWindow(self, s: str, t: str) -> str:
        # Guard case: if either target or search string is empty, return empty string.
        if not t or not s: return ""
        # Count frequency of each character in the target string t.
        dict_t = Counter(t)
        # Total unique characters in t that must be present in the window.
        required = len(dict_t)
        # Left and right pointers for the sliding window.
        l, r = 0, 0
        # Track how many unique characters have met their required frequency.
        formed = 0
        # Keep track of characters and their counts in the current window.
        window_counts = {}
        # Result tuple: (window length, left index, right index).
        ans = float("inf"), None, None

        # Iterate through the string s with the right pointer.
        while r < len(s):
            character = s[r]
            # Add character at right pointer to the window counts.
            window_counts[character] = window_counts.get(character, 0) + 1
            # If the current character is in target and meets its count requirement:
            if character in dict_t and window_counts[character] == dict_t[character]:
                formed += 1

            # Contract the window from the left as long as it contains all target characters.
            while l <= r and formed == required:
                character = s[l]
                # Update the minimum window if the current window is smaller.
                if r - l + 1 < ans[0]:
                    ans = (r - l + 1, l, r)
                # Remove the character at the left pointer from the window.
                window_counts[character] -= 1
                # If removing it drops its frequency below target requirement:
                if character in dict_t and window_counts[character] < dict_t[character]:
                    formed -= 1
                # Slide the left pointer to the right.
                l += 1
            # Expand the window by moving the right pointer.
            r += 1

        # Return the minimum window or empty string if no valid window was found.
        return "" if ans[0] == float("inf") else s[ans[1]: ans[2] + 1]

    # -----------------------------------------------------------------------
    # 2. Longest Substring Without Repeating Characters — T1
    # Given a string s, find the length of the longest substring without duplicate characters.
    # Example: s = "abcabcbb" → 3
    # Constraints: 0 <= s.length <= 5 * 10^4, s consists of English letters, digits, symbols and spaces
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def lengthOfLongestSubstring(self, s: str) -> int:
        # Map to store the last seen index of each character.
        seen = {}
        # Left pointer of the sliding window.
        l = 0
        # Variable to keep track of the maximum length found.
        res = 0
        # Iterate through the string with the right pointer.
        for r in range(len(s)):
            # If the character is already in the map, jump the left pointer.
            if s[r] in seen:
                # Move l to index after the duplicate, but never move it backward.
                l = max(l, seen[s[r]] + 1)
            # Record or update the index of the current character.
            seen[s[r]] = r
            # Update the max length with the current window size.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 3. Find All Anagrams in a String — T1
    # Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
    # Example: s = "cbaebabacd", p = "abc" → [0,6]
    # Constraints: 1 <= s.length, p.length <= 3 * 10^4, s and p consist of lowercase English letters
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findAnagrams(self, s: str, p: str) -> list[int]:
        # If the target anagram is longer than the search string, no match can exist.
        if len(p) > len(s): return []
        # Compute frequencies of the target string p.
        p_count = Counter(p)
        # Pre-populate counts for the first len(p)-1 characters of s.
        s_count = Counter(s[:len(p)-1])
        res = []
        # Left boundary of the sliding window.
        l = 0
        # Slide the window from the end of the pre-populated prefix to the end of s.
        for r in range(len(p)-1, len(s)):
            # Include the new character on the right.
            s_count[s[r]] += 1
            # Check if the current window frequencies match target frequencies.
            if s_count == p_count:
                res.append(l)
            # Remove the outgoing character on the left.
            s_count[s[l]] -= 1
            # Clean up the key from Counter if its frequency drops to zero.
            if s_count[s[l]] == 0:
                del s_count[s[l]]
            # Slide left pointer forward.
            l += 1
        return res

    # -----------------------------------------------------------------------
    # 4. Permutation in String — T1
    # Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise. In other words, return true if one of s1's permutations is the substring of s2.
    # Example: s1 = "ab", s2 = "eidbaooo" → true
    # Constraints: 1 <= s1.length, s2.length <= 10^4, s1 and s2 consist of lowercase English letters
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def checkInclusion(self, s1: str, s2: str) -> bool:
        # If target string s1 is longer than s2, a permutation cannot be a substring.
        if len(s1) > len(s2): 
            return False
        # Calculate character counts for s1 and initial part of s2.
        s1_count, s2_count = Counter(s1), Counter(s2[:len(s1)-1])
        l = 0
        # Iterate over characters of s2 starting from the end of the initial window.
        for r in range(len(s1)-1, len(s2)):
            # Add the current rightmost character to the window count.
            s2_count[s2[r]] += 1
            # If the frequency maps match, a permutation is found.
            if s1_count == s2_count:
                return True
            # Decrement the count of the character leaving the window.
            s2_count[s2[l]] -= 1
            # Remove character key if count is zero to ensure correct equality check.
            if s2_count[s2[l]] == 0:
                del s2_count[s2[l]]
            # Increment left pointer to slide the window.
            l += 1
        return False

    # -----------------------------------------------------------------------
    # 6. Longest Repeating Character Replacement — T1
    # You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times. Return the length of the longest substring containing the same letter you can get after performing the above operations.
    # Example: s = "ABAB", k = 2 → 4
    # Constraints: 1 <= s.length <= 10^5, s consists of only uppercase English letters, 0 <= k <= s.length
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def characterReplacement(self, s: str, k: int) -> int:
        # Map to store frequency of characters in the current window.
        count = {}
        # Max length of substring satisfying the condition.
        res = 0
        # Left pointer of the window.
        l = 0
        # Maintain the maximum frequency of any character seen in the window.
        max_f = 0
        # Move the right pointer across the string.
        for r in range(len(s)):
            # Increment count of the current character.
            count[s[r]] = 1 + count.get(s[r], 0)
            # Update the maximum character frequency.
            max_f = max(max_f, count[s[r]])
            # If the remaining characters to be replaced exceed our budget k:
            while (r - l + 1) - max_f > k:
                # Reduce count of the leftmost character.
                count[s[l]] -= 1
                # Contract the window from the left.
                l += 1
            # Track the maximum size of a valid window.
            res = max(res, r - l + 1)
        return res

class Codec:
    # -----------------------------------------------------------------------
    # 1. Encode and Decode Strings (LC 271) — T2
    # Design an algorithm to encode a list of strings to a string. The encoded string is then sent over the network and is decoded back to the original list of strings.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def encode(self, strs: List[str]) -> str:
        # Initialize an empty result string.
        res = ""
        # Process each word in the list.
        for s in strs:
            # Prepend the length and the '#' separator before the original string.
            res += str(len(s)) + "#" + s
        return res

    # Time: O(n), Space: O(n)
    def decode(self, s: str) -> List[str]:
        """Process each word in the list."""
        # List to hold the decoded strings and cursor pointer.
        res, i = [], 0
        # Process the entire encoded string.
        while i < len(s):
            j = i
            # Find the position of the next '#' separator.
            while s[j] != "#":
                j += 1
            # Parse the length of the next string segment.
            length = int(s[i:j])
            # Slice and extract the original string of the parsed length.
            res.append(s[j + 1 : j + 1 + length])
            # Advance index to the start of the next encoded block.
            i = j + 1 + length
        return res

class StringSolutionsT2:
    # -----------------------------------------------------------------------
    # 3. Longest Palindromic Substring (LC 5) — T2
    # Given a string s, return the longest palindromic substring in s.
    # Example: s = "babad" → "bab"
    # Constraints: 1 <= s.length <= 1000, s consist of only digits and English letters
    # Time: O(n^2), Space: O(1)
    # -----------------------------------------------------------------------
    def longestPalindrome(self, s: str) -> str:
        res = ""
        resLen = 0

        for i in range(len(s)):
            # odd length
            l, r = i, i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > resLen:
                    res = s[l:r+1]
                    resLen = r - l + 1
                l -= 1
                r += 1

            # even length
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if (r - l + 1) > resLen:
                    res = s[l:r+1]
                    resLen = r - l + 1
                l -= 1
                r += 1
        return res

    # -----------------------------------------------------------------------
    # 4. Palindromic Substrings (LC 647) — T2
    # Given a string s, return the number of palindromic substrings in it. A string is a palindrome when it reads the same backward as forward. A substring is a contiguous sequence of characters within the string.
    # Example: s = "abc" → 3
    # Constraints: 1 <= s.length <= 1000, s consists of lowercase English letters
    # Time: O(n^2), Space: O(1)
    # -----------------------------------------------------------------------
    def countSubstrings(self, s: str) -> int:
        res = 0
        # Try each index as the center of a palindrome.
        for i in range(len(s)):
            # Expand for odd-length palindromes (single-character center).
            l = r = i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                res += 1
                l -= 1
                r += 1

            # Expand for even-length palindromes (center in between i and i+1).
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                res += 1
                l -= 1
                r += 1
        return res

    # -----------------------------------------------------------------------
    # 5. Reverse Words in a String (LC 151) — T2
    # Given an input string s, reverse the order of the words. A word is defined as a sequence of non-space characters. The words in s will be separated by at least one space. Return a string of the words in reverse order concatenated by a single space. Note that s may contain leading or trailing spaces or multiple spaces between two words. The returned string should only have a single space separating the words. Do not include any extra spaces.
    # Example: s = "the sky is blue" → "blue is sky the"
    # Constraints: 1 <= s.length <= 10^4, s contains English letters (upper-case and lower-case), digits, and spaces ' ', There is at least one word in s, Follow-up: If the string data type is mutable in your language, can you solve it in-place with O(1), extra space?
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def reverseWords(self, s: str) -> str:
        return " ".join(s.split()[::-1])

    # -----------------------------------------------------------------------
    # 6. Group Anagrams (T1) — listed under both Hashing and String sections
    # Given an array of strings, group the anagrams together.
    # Time: O(n * k log k), Space: O(n * k)
    # -----------------------------------------------------------------------
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """Given an array of strings, group the anagrams together."""
        from collections import defaultdict
        # Map key (sorted characters tuple) to list of anagrams.
        groups = defaultdict(list)
        for s in strs:
            # Sorting the string creates a canonical key for all its anagrams.
            key = tuple(sorted(s))
            # Append the original string to its anagram group.
            groups[key].append(s)
        # Return all anagram groups as a list of lists.
        return list(groups.values())

    # -----------------------------------------------------------------------
    # 7. Valid Parenthesis String (LC 678) — T2
    # Given a string s containing only three types of characters: '(', ')' and '*', return true if s is valid. The following rules define a valid string: empty string "".
    # Example: s = "()" → true
    # Constraints: 1 <= s.length <= 100, s[i] is '(', ')' or '*'
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def checkValidString(self, s: str) -> bool:
        # Maintain the minimum and maximum possible count of open parentheses.
        leftMin, leftMax = 0, 0
        for c in s:
            if c == "(":
                # Open parenthesis increases both minimum and maximum limits.
                leftMin, leftMax = leftMin + 1, leftMax + 1
            elif c == ")":
                # Close parenthesis decreases both minimum and maximum limits.
                leftMin, leftMax = leftMin - 1, leftMax - 1
            else:
                # Wildcard: can be ')' (decreases leftMin) or '(' (increases leftMax).
                leftMin, leftMax = leftMin - 1, leftMax + 1

            # If max count of open parentheses goes negative, invalid string.
            if leftMax < 0:
                return False
            # Open parentheses count cannot be negative; clamp minimum to 0.
            if leftMin < 0:
                leftMin = 0

        # String is valid if it is possible to end up with 0 open parentheses.
        return leftMin == 0

    # -----------------------------------------------------------------------
    # 8. Integer to Roman (LC 12) — T2
    # Seven different symbols represent Roman numerals with the following values: Symbol Value I 1 V 5 X 10 L 50 C 100 D 500 M 1000 Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting a decimal place value into a Roman numeral has the following rules: subtracted from the input, append that symbol to the result, subtract its value, and convert the remainder to a Roman numeral. the following symbol, for example, 4 is 1 (I) less than 5 (V): IV and 9 is 1 (I) less than 10 (X): IX. Only the following subtractive forms are used: 4 (IV), 9 (IX), 40 (XL), 90 (XC), 400 (CD) and 900 (CM). multiples of 10. You cannot append 5 (V), 50 (L), or 500 (D) multiple times. If you need to append a symbol 4 times use the subtractive form. Given an integer, convert it to a Roman numeral.
    # Example: num = 3749 → "MMMDCCXLIX"
    # Constraints: 1 <= num <= 3999
    # Time: O(1), Space: O(1)
    # -----------------------------------------------------------------------
    def intToRoman(self, num: int) -> str:
        # Parallel arrays containing standard values and subtractive pairs.
        val = [
            1000, 900, 500, 400,
            100, 90, 50, 40,
            10, 9, 5, 4,
            1
        ]
        # Roman numeral symbols corresponding to each value in 'val'.
        syb = [
            "M", "CM", "D", "CD",
            "C", "XC", "L", "XL",
            "X", "IX", "V", "IV",
            "I"
        ]

        roman_num = ""
        i = 0
        # Iterate greedily from the largest value to the smallest.
        while num > 0:
            # Append symbol as many times as its value divides into num.
            for _ in range(num // val[i]):
                roman_num += syb[i]
                # Reduce num by the consumed value.
                num -= val[i]
            # Advance to the next smaller Roman numeral value.
            i += 1
        return roman_num

    # -----------------------------------------------------------------------
    # 10. Shortest Palindrome — T3
    # You are given a string s. You can convert s to a palindrome by adding characters in front of it. Return the shortest palindrome you can find by performing this transformation.
    # Example: s = "aacecaaa" → "aaacecaaa"
    # Constraints: 0 <= s.length <= 5 * 10^4, s consists of lowercase English letters only
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def shortestPalindrome(self, s: str) -> str:
        # If the input string is empty, it is already a palindrome.
        if not s: return s
        # Reverse the original string.
        rev_s = s[::-1]
        # Concatenate original string, a separator, and reversed string.
        l = s + "#" + rev_s
        # Initialize LPS array for KMP prefix matching.
        p = [0] * len(l)
        # Populate the LPS array.
        for i in range(1, len(l)):
            j = p[i - 1]
            # Fall back through LPS array on mismatch.
            while j > 0 and l[i] != l[j]:
                j = p[j - 1]
            # Match found, increment prefix length.
            if l[i] == l[j]:
                p[i] = j + 1
        # Prepend the non-palindromic suffix of rev_s to the original string.
        return rev_s[:len(s) - p[-1]] + s

    # -----------------------------------------------------------------------
    # 13. Longest Happy Prefix — T3
    # A string is called a happy prefix if is a non-empty prefix which is also a suffix (excluding itself). Given a string s, return the longest happy prefix of s. Return an empty string "" if no such prefix exists.
    # Example: s = "level" → "l"
    # Constraints: 1 <= s.length <= 10^5, s contains only lowercase English letters
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def longestPrefix(self, s: str) -> str:
        # Longest Prefix Suffix (LPS) array for KMP-like lookup.
        p = [0] * len(s)
        # Populate LPS array starting from index 1.
        for i in range(1, len(s)):
            j = p[i - 1]
            # Fall back to previous matches while characters mismatch.
            while j > 0 and s[i] != s[j]:
                j = p[j - 1]
            # If a match is found, extend the matching prefix length.
            if s[i] == s[j]:
                p[i] = j + 1
        # The last value in the LPS array corresponds to the longest happy prefix length.
        return s[:p[-1]]

if __name__ == "__main__":
    sol = StringSolutions()
    sol2 = StringSolutionsT2()

    # minWindow
    assert sol.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert sol.minWindow("a", "a") == "a"
    assert sol.minWindow("a", "aa") == ""

    # lengthOfLongestSubstring
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("") == 0

    # findAnagrams
    assert sol.findAnagrams("cbaebabacd", "abc") == [0, 6]

    # checkInclusion
    assert sol.checkInclusion("ab", "eidbaooo") == True
    assert sol.checkInclusion("ab", "eidboaoo") == False

    # characterReplacement
    assert sol.characterReplacement("AABABBA", 1) == 4

    # Codec encode/decode round trip
    codec = Codec()
    words = ["Hello", "World"]
    assert codec.decode(codec.encode(words)) == words
    assert codec.decode(codec.encode(["", "abc", "def"])) == ["", "abc", "def"]

    # longestPalindrome
    assert sol2.longestPalindrome("babad") in ["bab", "aba"]
    assert sol2.longestPalindrome("cbbd") == "bb"

    # countSubstrings
    assert sol2.countSubstrings("abc") == 3
    assert sol2.countSubstrings("aaa") == 6

    # reverseWords
    assert sol2.reverseWords("the sky is blue") == "blue is sky the"
    assert sol2.reverseWords("  hello world  ") == "world hello"

    # groupAnagrams
    res = sol2.groupAnagrams(["eat","tea","tan","ate","nat","bat"])
    assert sorted([sorted(g) for g in res]) == [["ate","eat","tea"],["bat"],["nat","tan"]]

    # checkValidString
    assert sol2.checkValidString("(*))") == True
    assert sol2.checkValidString("(*)") == True
    assert sol2.checkValidString("((*)") == True

    # shortestPalindrome
    assert sol2.shortestPalindrome("aacecaaa") == "aaacecaaa"
    assert sol2.shortestPalindrome("abcd") == "dcbabcd"

    # longestPrefix (KMP happy prefix)
    assert sol2.longestPrefix("level") == "l"
    assert sol2.longestPrefix("ababab") == "abab"

    print("All string tests passed.")
