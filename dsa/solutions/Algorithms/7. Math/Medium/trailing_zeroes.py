class Solution:
    def trailingZeroes(self, n: int) -> int:
        """
        Problem: Factorial Trailing Zeroes
        Difficulty: Medium
        Time Complexity: O(log n)
        """
        count = 0
        while n > 0:
            n //= 5
            count += n
        return count
