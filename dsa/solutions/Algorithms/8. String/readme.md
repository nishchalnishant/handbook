# String Algorithms Overview 🧵

String manipulation is a core part of programming interviews.

## Concepts
- **Two Pointers**: Used in palindromes, reversals.
- **Sliding Window**: Longest substring problems.
- **KMP / Rabin-Karp**: Efficient Pattern Matching.

---

## Problems & Solutions

### Easy
1. **[Reverse String](Easy/reverse_string.py)**
   - In-place reversal.
2. **[Valid Palindrome](Easy/valid_palindrome.py)**
   - Check if string is palindrome (ignoring casing/non-alphanumeric).
3. **[Longest Common Prefix](Easy/longest_common_prefix.py)**
   - Common prefix among array of strings.
4. **[Valid Anagram](../8.%20Hashing/Easy/valid_anagram.py)**
   - Check if strings are anagrams.

### Medium
1. **[Longest Palindromic Substring](Medium/longest_palindromic_substring.py)**
   - Expand around center.
2. **[String Compression](Medium/string_compression.py)**
   - Run-length encoding.
3. **[Zigzag Conversion](Medium/zigzag_conversion.py)**
   - Zigzag pattern printing.
4. **[Group Anagrams](../8.%20Hashing/Medium/group_anagrams.py)**
   - Grouping.

### Hard
1. **[Minimum Window Substring](Hard/min_window_substring.py)**
   - Minimum window containing all chars of T.
2. **[KMP Algorithm](Hard/kmp_algorithm.py)**
   - Knuth-Morris-Pratt Pattern Matching.

---

## Tips for Interviews
- **Immutability**: Python strings are immutable. operations like `s += "c"` create new strings. Use list `[]` and `"".join()` for efficiency.
- **Edge Cases**: Empty strings, single characters.
