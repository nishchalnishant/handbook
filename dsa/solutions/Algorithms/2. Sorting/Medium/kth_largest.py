from typing import List
import random

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Problem: Kth Largest Element (Quick Select)
        Difficulty: Medium
        Time Complexity: O(n) average, O(n^2) worst
        Space Complexity: O(1) (iterative)
        """
        k = len(nums) - k # Convert to index of kth smallest
        
        l, r = 0, len(nums) - 1
        return self.quickSelect(nums, l, r, k)
        
    def quickSelect(self, nums, l, r, k):
        pivot, p = nums[r], l
        for i in range(l, r):
            if nums[i] <= pivot:
                nums[p], nums[i] = nums[i], nums[p]
                p += 1
        nums[p], nums[r] = nums[r], nums[p]
        
        if p > k: return self.quickSelect(nums, l, p - 1, k)
        elif p < k: return self.quickSelect(nums, p + 1, r, k)
        else: return nums[p]
