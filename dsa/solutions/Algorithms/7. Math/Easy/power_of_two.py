class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        """
        Problem: Power of Two
        Difficulty: Easy
        Time Complexity: O(1)
        """
        return n > 0 and (n & (n - 1)) == 0
