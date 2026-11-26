from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        """
        Problem: Jump Game
        Pattern: Greedy (Move goal post)
        """
        goal = len(nums) - 1
        
        for i in range(len(nums) - 2, -1, -1):
            if i + nums[i] >= goal:
                goal = i
                
        return goal == 0

    def jump(self, nums: List[int]) -> int:
        """
        Problem: Jump Game II
        Pattern: Greedy (BFS like levels)
        """
        res = 0
        l = r = 0
        
        while r < len(nums) - 1:
            farthest = 0
            for i in range(l, r + 1):
                farthest = max(farthest, i + nums[i])
            l = r + 1
            r = farthest
            res += 1
        return res
