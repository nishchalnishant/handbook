from typing import List

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """
        Problem: Subsets
        Difficulty: Medium
        Time Complexity: O(2^n)
        Space Complexity: O(2^n)
        """
        res = []
        
        def backtrack(index, path):
            res.append(path[:])
            
            for i in range(index, len(nums)):
                path.append(nums[i])
                backtrack(i + 1, path)
                path.pop()
                
        backtrack(0, [])
        return res
