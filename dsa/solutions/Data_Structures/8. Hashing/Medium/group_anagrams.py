from typing import List
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """
        Problem: Group Anagrams
        Difficulty: Medium
        Time Complexity: O(m * n)
        Space Complexity: O(m * n)
        """
        ans = defaultdict(list)
        
        for s in strs:
            count = [0] * 26
            for c in s:
                count[ord(c) - ord("a")] += 1
            ans[tuple(count)].append(s)
            
        return list(ans.values())
