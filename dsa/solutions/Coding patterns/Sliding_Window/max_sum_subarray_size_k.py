from typing import List

class Solution:
    def maxSumSubarray(self, nums: List[int], k: int) -> int:
        """
        Problem: Max Sum Subarray of Size K
        Pattern: Sliding Window - Fixed Size
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        if not nums or k <= 0: return 0
        
        current_sum = 0
        max_sum = float('-inf')
        
        for i in range(len(nums)):
            current_sum += nums[i]
            
            # Once we hit window size k
            if i >= k - 1:
                max_sum = max(max_sum, current_sum)
                # Slide window: subtract the element leaving the window
                current_sum -= nums[i - (k - 1)]
                
        return max_sum

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSumSubarray([2, 1, 5, 1, 3, 2], 3)) # Expected: 9 (5+1+3)
