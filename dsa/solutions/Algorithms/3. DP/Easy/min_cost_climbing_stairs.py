from typing import List

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        """
        Problem: Min Cost Climbing Stairs
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        cost.append(0)
        
        for i in range(len(cost) - 3, -1, -1):
            cost[i] += min(cost[i + 1], cost[i + 2])
            
        return min(cost[0], cost[1])
