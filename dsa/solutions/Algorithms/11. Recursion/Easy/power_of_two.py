class Solution:
    def isPowerOfTwo(self, n: int) -> bool:
        """
        Problem: Power of Two (Recursive)
        Difficulty: Easy
        Time Complexity: O(log n)
        Space Complexity: O(log n)
        """
        if n <= 0: return False
        if n == 1: return True
        return n % 2 == 0 and self.isPowerOfTwo(n // 2)
