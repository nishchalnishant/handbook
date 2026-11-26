from typing import List

class Solution:
    def minPatches(self, nums: List[int], n: int) -> int:
        """
        Problem: Patching Array
        Difficulty: Hard
        Time Complexity: O(m + log n)
        Space Complexity: O(1)
        """
        res = 0
        i = 0
        missing = 1
        
        while missing <= n:
            if i < len(nums) and nums[i] <= missing:
                missing += nums[i]
                i += 1
            else:
                res += 1
                missing += missing
        return res
