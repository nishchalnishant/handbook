from typing import List

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Problem: Rotate Array
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        k = k % len(nums)
        
        def reverse(l, r):
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l, r = l + 1, r - 1
                
        # Reverse all
        reverse(0, len(nums) - 1)
        # Reverse first k
        reverse(0, k - 1)
        # Reverse last n-k
        reverse(k, len(nums) - 1)
