from typing import List

class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        """
        Problem: Find Peak Element
        Difficulty: Medium
        Time Complexity: O(log n)
        Space Complexity: O(1)
        """
        l, r = 0, len(nums) - 1
        
        while l <= r:
            m = l + ((r - l) // 2)
            # Left neighbor greater
            if m > 0 and nums[m] < nums[m - 1]:
                r = m - 1
            # Right neighbor greater
            elif m < len(nums) - 1 and nums[m] < nums[m + 1]:
                l = m + 1
            else:
                return m
