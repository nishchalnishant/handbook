from typing import List

class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        """
        Problem: 3Sum Closest
        Pattern: Two Pointers - Converging (after sort)
        Time Complexity: O(n^2)
        Space Complexity: O(1)
        """
        nums.sort()
        res = nums[0] + nums[1] + nums[2]
        
        for i in range(len(nums) - 2):
            left, right = i + 1, len(nums) - 1
            while left < right:
                current_sum = nums[i] + nums[left] + nums[right]
                if abs(target - current_sum) < abs(target - res):
                    res = current_sum
                
                if current_sum < target:
                    left += 1
                elif current_sum > target:
                    right -= 1
                else:
                    return current_sum # Found exact match
        
        return res

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.threeSumClosest([-1,2,1,-4], 1)) # Expected: 2
