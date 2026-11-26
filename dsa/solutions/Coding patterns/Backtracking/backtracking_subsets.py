from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Problem: Subsets
        Pattern: Backtracking
        """
        res = []
        subset = []
        
        def dfs(i):
            if i >= len(nums):
                res.append(subset[:])
                return
            
            # Include nums[i]
            subset.append(nums[i])
            dfs(i + 1)
            
            # Exclude nums[i]
            subset.pop()
            dfs(i + 1)
            
        dfs(0)
        return res

    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Problem: Combination Sum
        Pattern: Backtracking
        """
        res = []
        
        def dfs(i, curr, total):
            if total == target:
                res.append(curr[:])
                return
            if i >= len(candidates) or total > target:
                return
            
            # Include
            curr.append(candidates[i])
            dfs(i, curr, total + candidates[i])
            
            # Exclude (move to next candidate)
            curr.pop()
            dfs(i + 1, curr, total)
            
        dfs(0, [], 0)
        return res

    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Problem: Permutations
        Pattern: Backtracking
        """
        res = []
        
        if len(nums) == 1:
            return [nums[:]]
            
        for i in range(len(nums)):
            n = nums.pop(0)
            perms = self.permute(nums)
            
            for p in perms:
                p.append(n)
            res.extend(perms)
            
            nums.append(n)
        return res
