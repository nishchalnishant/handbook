from typing import List

class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        """
        Problem: Combination Sum
        Difficulty: Medium
        Time Complexity: O(2^t) where t is target
        Space Complexity: O(t)
        """
        res = []
        
        def backtrack(i, cur, total):
            if total == target:
                res.append(cur[:])
                return
            
            if i >= len(candidates) or total > target:
                return
            
            # Choice 1: Include candidates[i]
            cur.append(candidates[i])
            backtrack(i, cur, total + candidates[i])
            
            # Choice 2: Don't include candidates[i]
            cur.pop()
            backtrack(i + 1, cur, total)
            
        backtrack(0, [], 0)
        return res
