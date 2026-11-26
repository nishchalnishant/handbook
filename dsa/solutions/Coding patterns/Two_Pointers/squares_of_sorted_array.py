from typing import List

class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        """
        Problem: Squares of a Sorted Array
        Pattern: Two Pointers - Converging
        Time Complexity: O(n)
        Space Complexity: O(n) for result
        """
        n = len(nums)
        res = [0] * n
        left, right = 0, n - 1
        
        for i in range(n - 1, -1, -1):
            if abs(nums[left]) > abs(nums[right]):
                res[i] = nums[left] ** 2
                left += 1
            else:
                res[i] = nums[right] ** 2
                right -= 1
                
        return res

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.sortedSquares([-4,-1,0,3,10])) # Expected: [0,1,9,16,100]
