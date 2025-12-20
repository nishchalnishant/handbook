from typing import List

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Problem: Move Zeroes
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        l = 0
        for r in range(len(nums)):
            if nums[r]:
                nums[l], nums[r] = nums[r], nums[l]
                l += 1
        return nums

# Test
if __name__ == "__main__":
    sol = Solution()
    arr = [0,1,0,3,12]
    sol.moveZeroes(arr)
    print(arr) # [1,3,12,0,0]
