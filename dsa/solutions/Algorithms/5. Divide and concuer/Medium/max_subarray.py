from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Problem: Maximum Subarray (Divide and Conquer)
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(log n)
        """
        return self.helper(nums, 0, len(nums) - 1)
        
    def helper(self, nums, l, r):
        if l == r:
            return nums[l]
        
        mid = (l + r) // 2
        leftMax = self.helper(nums, l, mid)
        rightMax = self.helper(nums, mid + 1, r)
        crossMax = self.crossSum(nums, l, mid, r)
        
        return max(leftMax, rightMax, crossMax)
    
    def crossSum(self, nums, l, mid, r):
        leftSum = float('-inf')
        curr = 0
        for i in range(mid, l - 1, -1):
            curr += nums[i]
            leftSum = max(leftSum, curr)
            
        rightSum = float('-inf')
        curr = 0
        for i in range(mid + 1, r + 1):
            curr += nums[i]
            rightSum = max(rightSum, curr)
            
        return leftSum + rightSum
