from typing import List

class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        """
        Problem: Assign Cookies
        Difficulty: Easy
        Time Complexity: O(n log n + m log m)
        Space Complexity: O(1)
        """
        g.sort()
        s.sort()
        
        i, j = 0, 0
        while i < len(g) and j < len(s):
            if s[j] >= g[i]:
                i += 1
            j += 1
        return i
