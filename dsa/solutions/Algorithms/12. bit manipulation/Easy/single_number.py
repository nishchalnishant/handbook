from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Problem: Single Number
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        res = 0
        for n in nums:
            res ^= n
        return res
