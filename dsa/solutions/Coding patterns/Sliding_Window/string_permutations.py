from typing import List
from collections import Counter

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """
        Problem: Permutation in String
        Pattern: Sliding Window - Fixed Size (Frequency Map)
        """
        if len(s1) > len(s2): return False
        
        s1_count = Counter(s1)
        window_count = Counter()
        
        left = 0
        for right in range(len(s2)):
            window_count[s2[right]] += 1
            
            # If window size exceeds s1 length, shrink from left
            if right - left + 1 > len(s1):
                if window_count[s2[left]] == 1:
                    del window_count[s2[left]]
                else:
                    window_count[s2[left]] -= 1
                left += 1
                
            if window_count == s1_count:
                return True
                
        return False

    def findAnagrams(self, s: str, p: str) -> List[int]:
        """
        Problem: Find All Anagrams in a String
        Pattern: Sliding Window - Fixed Size
        """
        if len(p) > len(s): return []
        
        p_count = Counter(p)
        window_count = Counter()
        res = []
        
        left = 0
        for right in range(len(s)):
            window_count[s[right]] += 1
            
            if right - left + 1 > len(p):
                if window_count[s[left]] == 1:
                    del window_count[s[left]]
                else:
                    window_count[s[left]] -= 1
                left += 1
            
            if window_count == p_count:
                res.append(left)
                
        return res

# Test
if __name__ == "__main__":
    sol = Solution()
    print(f"Permutation: {sol.checkInclusion('ab', 'eidbaooo')}") # True
    print(f"Anagrams: {sol.findAnagrams('cbaebabacd', 'abc')}") # [0, 6]
