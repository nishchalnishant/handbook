from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """
        Problem: Jump Game
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        goal = len(nums) - 1
        
        for i in range(len(nums) - 1, -1, -1):
            if i + nums[i] >= goal:
                goal = i
                
        return goal == 0
