import math

class Solution:
    def gcd(self, a: int, b: int) -> int:
        """
        Problem: Greatest Common Divisor
        Difficulty: Easy
        Time Complexity: O(log(min(a, b)))
        """
        while b:
            a, b = b, a % b
        return a

    def lcm(self, a: int, b: int) -> int:
        """
        Problem: Least Common Multiple
        """
        if a == 0 or b == 0: return 0
        return abs(a * b) // self.gcd(a, b)
