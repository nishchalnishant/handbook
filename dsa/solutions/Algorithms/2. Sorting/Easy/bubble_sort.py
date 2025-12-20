from typing import List

class Solution:
    def bubbleSort(self, nums: List[int]) -> List[int]:
        """
        Problem: Bubble Sort
        Difficulty: Easy
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        n = len(nums)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                if nums[j] > nums[j + 1]:
                    nums[j], nums[j + 1] = nums[j + 1], nums[j]
                    swapped = True
            if not swapped:
                break
        return nums
