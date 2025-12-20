from typing import List
from collections import deque

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        """
        Problem: Sliding Window Maximum
        Pattern: Sliding Window - Monotonic Queue
        Time Complexity: O(n)
        Space Complexity: O(k)
        """
        output = []
        q = deque()  # stores indices
        left = 0
        
        for right in range(len(nums)):
            # Remove indices that are out of the window
            while q and q[0] < right - k + 1:
                q.popleft()
            
            # Remove elements smaller than current element from the right
            # Maintain decreasing order in the deque
            while q and nums[q[-1]] < nums[right]:
                q.pop()
                
            q.append(right)
            
            # Add to output once window is fully formed
            if right >= k - 1:
                output.append(nums[q[0]])
                
        return output

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3)) # [3,3,5,5,6,7]
