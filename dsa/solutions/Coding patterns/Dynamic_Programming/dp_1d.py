from typing import List

class Solution:
    def climbStairs(self, n: int) -> int:
        """
        Problem: Climbing Stairs
        Pattern: 1D DP (Fibonacci)
        """
        one, two = 1, 1
        for i in range(n - 1):
            temp = one
            one = one + two
            two = temp
        return one

    def rob(self, nums: List[int]) -> int:
        """
        Problem: House Robber
        Pattern: 1D DP
        """
        rob1, rob2 = 0, 0
        
        for n in nums:
            temp = max(n + rob1, rob2)
            rob1 = rob2
            rob2 = temp
        return rob2

    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        """
        Problem: Word Break
        Pattern: 1D DP
        """
        dp = [False] * (len(s) + 1)
        dp[len(s)] = True
        
        for i in range(len(s) - 1, -1, -1):
            for w in wordDict:
                if (i + len(w)) <= len(s) and s[i : i + len(w)] == w:
                    dp[i] = dp[i + len(w)]
                if dp[i]:
                    break
        return dp[0]

    def maxProduct(self, nums: List[int]) -> int:
        """
        Problem: Maximum Product Subarray
        Pattern: 1D DP (Track max and min)
        """
        res = max(nums)
        curMin, curMax = 1, 1
        
        for n in nums:
            if n == 0:
                curMin, curMax = 1, 1
                continue
            tmp = curMax * n
            curMax = max(n * curMax, n * curMin, n)
            curMin = min(tmp, n * curMin, n)
            res = max(res, curMax)
        return res
