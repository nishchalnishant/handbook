from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Problem: Container With Most Water
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        l, r = 0, len(height) - 1
        res = 0
        
        while l < r:
            area = (r - l) * min(height[l], height[r])
            res = max(res, area)
            
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return res
