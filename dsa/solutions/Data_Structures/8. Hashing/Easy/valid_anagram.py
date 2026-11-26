from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """
        Problem: Valid Anagram
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1) (26 chars)
        """
        return Counter(s) == Counter(t)
