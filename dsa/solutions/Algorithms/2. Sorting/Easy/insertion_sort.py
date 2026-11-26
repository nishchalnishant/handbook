from typing import List

class Solution:
    def insertionSort(self, nums: List[int]) -> List[int]:
        """
        Problem: Insertion Sort
        Difficulty: Easy
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        for i in range(1, len(nums)):
            key = nums[i]
            j = i - 1
            while j >= 0 and key < nums[j]:
                nums[j + 1] = nums[j]
                j -= 1
            nums[j + 1] = key
        return nums
