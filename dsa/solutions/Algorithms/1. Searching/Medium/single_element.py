from typing import List

class Solution:
    def singleNonDuplicate(self, nums: List[int]) -> int:
        """
        Problem: Single Element in a Sorted Array
        Difficulty: Medium
        Time Complexity: O(log n)
        Space Complexity: O(1)
        """
        l, r = 0, len(nums) - 1
        
        while l <= r:
            m = l + ((r - l) // 2)
            if ((m - 1 < 0 or nums[m - 1] != nums[m]) and 
                (m + 1 == len(nums) or nums[m] != nums[m + 1])):
                return nums[m]
            
            leftSize = m - 1 if nums[m-1] == nums[m] else m
            if leftSize % 2:
                r = m - 1
            else:
                l = m + 1
