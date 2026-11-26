class Solution:
    def longestPalindrome(self, s: str) -> str:
        """
        Problem: Longest Palindromic Substring
        Pattern: Two Pointers - Expanding From Center
        """
        res = ""
        for i in range(len(s)):
            # Odd length
            tmp = self.helper(s, i, i)
            if len(tmp) > len(res):
                res = tmp
            # Even length
            tmp = self.helper(s, i, i + 1)
            if len(tmp) > len(res):
                res = tmp
        return res
    
    def helper(self, s: str, l: int, r: int) -> str:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l+1:r]

    def validPalindrome(self, s: str) -> bool:
        """
        Problem: Valid Palindrome II
        Pattern: Two Pointers - Converging
        """
        l, r = 0, len(s) - 1
        while l < r:
            if s[l] != s[r]:
                return self.is_palindrome_range(s, l+1, r) or self.is_palindrome_range(s, l, r-1)
            l += 1
            r -= 1
        return True
    
    def is_palindrome_range(self, s: str, i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

# Test
if __name__ == "__main__":
    sol = Solution()
    print(f"Longest Palindrome: {sol.longestPalindrome('babad')}") # 'bab' or 'aba'
    print(f"Valid Palindrome II: {sol.validPalindrome('abca')}") # True
