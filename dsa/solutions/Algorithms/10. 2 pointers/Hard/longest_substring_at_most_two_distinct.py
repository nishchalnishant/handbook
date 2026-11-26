class Solution:
    def lengthOfLongestSubstringTwoDistinct(self, s: str) -> int:
        """
        Problem: Longest Substring with At Most Two Distinct Characters
        Difficulty: Medium/Hard
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        n = len(s)
        if n < 3: return n
        
        l, r = 0, 0
        hashmap = {} # char -> last index
        max_len = 2
        
        while r < n:
            if len(hashmap) < 3:
                hashmap[s[r]] = r
                r += 1
                
            if len(hashmap) == 3:
                del_idx = min(hashmap.values())
                del hashmap[s[del_idx]]
                l = del_idx + 1
                
            max_len = max(max_len, r - l)
        return max_len
