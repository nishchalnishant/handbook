class Solution:
    def myPow(self, x: float, n: int) -> float:
        """
        Problem: Pow(x, n)
        Difficulty: Medium
        Time Complexity: O(log n)
        Space Complexity: O(log n)
        """
        if n == 0: return 1
        if n < 0:
            return 1 / self.myPow(x, -n)
            
        half = self.myPow(x, n // 2)
        if n % 2 == 0:
            return half * half
        else:
            return x * half * half
