from typing import List

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Problem: Sort Colors (Dutch National Flag)
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        l, r = 0, len(nums) - 1
        i = 0
        
        def swap(i, j):
            nums[i], nums[j] = nums[j], nums[i]
            
        while i <= r:
            if nums[i] == 0:
                swap(l, i)
                l += 1
                i += 1 # We know what we switched from left is 0 or 1
            elif nums[i] == 2:
                swap(i, r)
                r -= 1
                # Don't increment i, need to check what we swapped from right
            else:
                i += 1
