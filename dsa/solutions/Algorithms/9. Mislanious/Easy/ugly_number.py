class Solution:
    def isUgly(self, n: int) -> bool:
        """
        Problem: Ugly Number
        Difficulty: Easy
        Time Complexity: O(log n)
        """
        if n <= 0: return False
        
        for p in [2, 3, 5]:
            while n % p == 0:
                n //= p
        return n == 1
