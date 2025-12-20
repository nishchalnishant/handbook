class Solution:
    def shortestPalindrome(self, s: str) -> str:
        """
        Problem: Shortest Palindrome
        Difficulty: Hard
        Time Complexity: O(n) using KMP
        """
        rev_s = s[::-1]
        new_s = s + "#" + rev_s
        n = len(new_s)
        
        # KMP table
        lps = [0] * n
        for i in range(1, n):
            j = lps[i - 1]
            while j > 0 and new_s[i] != new_s[j]:
                j = lps[j - 1]
            if new_s[i] == new_s[j]:
                j += 1
            lps[i] = j
            
        pal_len = lps[-1]
        return rev_s[:len(s) - pal_len] + s
