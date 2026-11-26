class Solution:
    def fib(self, n: int) -> int:
        """
        Problem: Fibonacci Number
        Difficulty: Easy
        Time Complexity: O(2^n) (without memoization) -> O(n) (with memoization)
        Space Complexity: O(n)
        """
        # Memoization
        cache = {}
        
        def helper(n):
            if n in cache:
                return cache[n]
            if n <= 1:
                return n
            
            res = helper(n - 1) + helper(n - 2)
            cache[n] = res
            return res
            
        return helper(n)
