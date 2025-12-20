from typing import List

class Solution:
    def search(self, nums: List[int], target: int) -> int:
        """
        Problem: Binary Search
        Pattern: Standard Binary Search
        """
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            if nums[m] == target:
                return m
            elif nums[m] < target:
                l = m + 1
            else:
                r = m - 1
        return -1

    def searchRange(self, nums: List[int], target: int) -> List[int]:
        """
        Problem: Find First and Last Position of Element in Sorted Array
        Pattern: Binary Search (Modified to find bounds)
        """
        left = self.binSearch(nums, target, True)
        right = self.binSearch(nums, target, False)
        return [left, right]
    
    def binSearch(self, nums, target, leftBias):
        l, r = 0, len(nums) - 1
        i = -1
        while l <= r:
            m = (l + r) // 2
            if nums[m] < target:
                l = m + 1
            elif nums[m] > target:
                r = m - 1
            else:
                i = m
                if leftBias:
                    r = m - 1
                else:
                    l = m + 1
        return i

    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        Problem: Search a 2D Matrix
        Pattern: Binary Search (Treat as 1D array)
        """
        rows, cols = len(matrix), len(matrix[0])
        l, r = 0, rows * cols - 1
        
        while l <= r:
            m = (l + r) // 2
            if matrix[m // cols][m % cols] == target:
                return True
            elif matrix[m // cols][m % cols] < target:
                l = m + 1
            else:
                r = m - 1
        return False
