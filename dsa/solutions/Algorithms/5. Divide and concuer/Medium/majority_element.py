from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        Problem: Majority Element (Divide and Conquer)
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(log n)
        """
        def helper(l, r):
            if l == r:
                return nums[l]
            
            mid = (l + r) // 2
            left = helper(l, mid)
            right = helper(mid + 1, r)
            
            if left == right:
                return left
            
            leftCount = sum(1 for i in range(l, r + 1) if nums[i] == left)
            rightCount = sum(1 for i in range(l, r + 1) if nums[i] == right)
            
            return left if leftCount > rightCount else right
            
        return helper(0, len(nums) - 1)
