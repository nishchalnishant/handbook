from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Problem: Container With Most Water
        Pattern: Two Pointers - Converging
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        left, right = 0, len(height) - 1
        max_water = 0
        
        while left < right:
            # Calculate current area
            width = right - left
            h = min(height[left], height[right])
            max_water = max(max_water, width * h)
            
            # Move the shorter line inwards to potentially find a taller line
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
                
        return max_water

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxArea([1,8,6,2,5,4,8,3,7])) # Expected: 49
