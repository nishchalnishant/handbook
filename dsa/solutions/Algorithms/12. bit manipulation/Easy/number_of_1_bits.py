class Solution:
    def hammingWeight(self, n: int) -> int:
        """
        Problem: Number of 1 Bits
        Difficulty: Easy
        Time Complexity: O(1) (32 bits)
        """
        res = 0
        while n:
            n &= (n - 1)
            res += 1
        return res
