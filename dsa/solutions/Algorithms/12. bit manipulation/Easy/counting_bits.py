from typing import List

class Solution:
    def countBits(self, n: int) -> List[int]:
        """
        Problem: Counting Bits
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        dp = [0] * (n + 1)
        offset = 1
        
        for i in range(1, n + 1):
            if offset * 2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]
            
        return dp
