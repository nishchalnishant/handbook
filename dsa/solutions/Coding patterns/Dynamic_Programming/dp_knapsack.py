from typing import List

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        """
        Problem: Partition Equal Subset Sum
        Pattern: 0/1 Knapsack
        """
        if sum(nums) % 2:
            return False
        
        dp = set()
        dp.add(0)
        target = sum(nums) // 2
        
        for i in range(len(nums) - 1, -1, -1):
            nextDP = set()
            for t in dp:
                if (t + nums[i]) == target:
                    return True
                nextDP.add(t + nums[i])
                nextDP.add(t)
            dp = nextDP
        return True if target in dp else False

    def coinChange(self, coins: List[int], amount: int) -> int:
        """
        Problem: Coin Change
        Pattern: Unbounded Knapsack
        """
        dp = [amount + 1] * (amount + 1)
        dp[0] = 0
        
        for a in range(1, amount + 1):
            for c in coins:
                if a - c >= 0:
                    dp[a] = min(dp[a], 1 + dp[a - c])
                    
        return dp[amount] if dp[amount] != amount + 1 else -1

    def change(self, amount: int, coins: List[int]) -> int:
        """
        Problem: Coin Change 2
        Pattern: Unbounded Knapsack (Count ways)
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        
        for c in coins:
            for a in range(c, amount + 1):
                dp[a] += dp[a - c]
        return dp[amount]
