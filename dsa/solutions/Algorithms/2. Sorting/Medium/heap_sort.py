from typing import List

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        """
        Problem: Heap Sort
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(1)
        """
        n = len(nums)
        
        # Build Max Heap
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(nums, n, i)
            
        # Extract elements one by one
        for i in range(n - 1, 0, -1):
            nums[i], nums[0] = nums[0], nums[i] # Swap root (max) to end
            self.heapify(nums, i, 0) # Heapify root
            
        return nums
    
    def heapify(self, nums, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and nums[left] > nums[largest]:
            largest = left
        
        if right < n and nums[right] > nums[largest]:
            largest = right
            
        if largest != i:
            nums[i], nums[largest] = nums[largest], nums[i]
            self.heapify(nums, n, largest)
