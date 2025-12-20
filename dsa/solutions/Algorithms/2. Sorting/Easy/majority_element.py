from typing import List

class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        """
        Problem: Majority Element
        Difficulty: Easy
        Time Complexity: O(n log n) (Sorting approach)
        """
        nums.sort()
        return nums[len(nums) // 2]
    
    # Note: Moore's Voting Algorithm is O(n)
