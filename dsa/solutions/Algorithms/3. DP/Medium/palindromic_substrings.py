class Solution:
    def countSubstrings(self, s: str) -> int:
        """
        Problem: Palindromic Substrings
        Difficulty: Medium
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        res = 0
        
        for i in range(len(s)):
            # odd length
            l, r = i, i
            while l >= 0 and r < len(s) and s[l] == s[r]:
                res += 1
                l -= 1
                r += 1
            
            # even length
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                res += 1
                l -= 1
                r += 1
        return res
