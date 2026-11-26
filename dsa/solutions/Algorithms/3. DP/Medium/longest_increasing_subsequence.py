from typing import List

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Problem: Longest Increasing Subsequence
        Difficulty: Medium
        Time Complexity: O(n^2)
        Space Complexity: O(n)
        """
        LIS = [1] * len(nums)
        
        for i in range(len(nums) - 1, -1, -1):
            for j in range(i + 1, len(nums)):
                if nums[i] < nums[j]:
                    LIS[i] = max(LIS[i], 1 + LIS[j])
        return max(LIS)
