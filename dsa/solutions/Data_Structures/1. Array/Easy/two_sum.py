from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """
        Problem: Two Sum
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        prevMap = {} # val : index
        for i, n in enumerate(nums):
            diff = target - n
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[n] = i
        return []

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.twoSum([2,7,11,15], 9)) # [0, 1]
