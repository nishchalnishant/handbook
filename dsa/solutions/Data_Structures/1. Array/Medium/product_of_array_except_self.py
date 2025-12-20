from typing import List

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """
        Problem: Product of Array Except Self
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1) (excluding output array)
        """
        res = [1] * (len(nums))
        
        prefix = 1
        for i in range(len(nums)):
            res[i] = prefix
            prefix *= nums[i]
            
        postfix = 1
        for i in range(len(nums) - 1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
            
        return res

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.productExceptSelf([1,2,3,4])) # [24, 12, 8, 6]
