from typing import List

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        """
        Problem: Permutations
        Difficulty: Medium
        Time Complexity: O(n!)
        Space Complexity: O(n!)
        """
        res = []
        
        def backtrack(path, choices):
            if not choices:
                res.append(path[:])
                return
            
            for i in range(len(choices)):
                path.append(choices[i])
                # Backtrack with remaining choices
                backtrack(path, choices[:i] + choices[i+1:])
                path.pop()
                
        backtrack([], nums)
        return res
