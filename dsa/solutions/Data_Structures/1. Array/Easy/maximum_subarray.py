from typing import List

class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """
        Problem: Maximum Subarray (Kadane's Algorithm)
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        maxSub = nums[0]
        curSum = 0
        
        for n in nums:
            if curSum < 0:
                curSum = 0
            curSum += n
            maxSub = max(maxSub, curSum)
        return maxSub

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSubArray([-2,1,-3,4,-1,2,1,-5,4])) # 6
