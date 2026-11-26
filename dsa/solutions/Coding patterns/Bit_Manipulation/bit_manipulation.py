from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        """
        Problem: Single Number
        Pattern: XOR
        """
        res = 0
        for n in nums:
            res ^= n
        return res

    def hammingWeight(self, n: int) -> int:
        """
        Problem: Number of 1 Bits
        Pattern: Bit Manipulation (n & n-1)
        """
        res = 0
        while n:
            n &= (n - 1)
            res += 1
        return res

    def countBits(self, n: int) -> List[int]:
        """
        Problem: Counting Bits
        Pattern: DP + Bit Manipulation
        """
        dp = [0] * (n + 1)
        offset = 1
        for i in range(1, n + 1):
            if offset * 2 == i:
                offset = i
            dp[i] = 1 + dp[i - offset]
        return dp

    def missingNumber(self, nums: List[int]) -> int:
        """
        Problem: Missing Number
        Pattern: XOR (indices ^ nums)
        """
        res = len(nums)
        for i in range(len(nums)):
            res += (i - nums[i])
        return res
