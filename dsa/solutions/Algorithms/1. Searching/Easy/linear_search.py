from typing import List

class Solution:
    def linearSearch(self, nums: List[int], target: int) -> int:
        """
        Problem: Linear Search
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        for i, n in enumerate(nums):
            if n == target:
                return i
        return -1
