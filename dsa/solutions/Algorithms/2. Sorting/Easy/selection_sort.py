from typing import List

class Solution:
    def selectionSort(self, nums: List[int]) -> List[int]:
        """
        Problem: Selection Sort
        Difficulty: Easy
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        for i in range(len(nums)):
            min_idx = i
            for j in range(i + 1, len(nums)):
                if nums[j] < nums[min_idx]:
                    min_idx = j
            nums[i], nums[min_idx] = nums[min_idx], nums[i]
        return nums
