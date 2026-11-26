class Solution:
    def factorial(self, n: int) -> int:
        """
        Problem: Factorial
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(n) (recursion stack)
        """
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)
