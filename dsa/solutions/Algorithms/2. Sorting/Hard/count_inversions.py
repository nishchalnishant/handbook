from typing import List

class Solution:
    def countInversions(self, nums: List[int]) -> int:
        """
        Problem: Count Inversions
        Difficulty: Hard
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        return self.mergeSort(nums, 0, len(nums) - 1)
    
    def mergeSort(self, nums, l, r):
        res = 0
        if l < r:
            m = (l + r) // 2
            res += self.mergeSort(nums, l, m)
            res += self.mergeSort(nums, m + 1, r)
            res += self.merge(nums, l, m, r)
        return res
        
    def merge(self, nums, l, m, r):
        left = nums[l : m + 1]
        right = nums[m + 1 : r + 1]
        
        i, j, k = 0, 0, l
        inv_count = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                nums[k] = left[i]
                i += 1
            else:
                nums[k] = right[j]
                j += 1
                inv_count += (len(left) - i) # All remaining left elements are greater
            k += 1
            
        while i < len(left):
            nums[k] = left[i]
            i += 1
            k += 1
        while j < len(right):
            nums[k] = right[j]
            j += 1
            k += 1
            
        return inv_count
