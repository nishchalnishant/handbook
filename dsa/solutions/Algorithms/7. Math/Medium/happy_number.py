class Solution:
    def isHappy(self, n: int) -> bool:
        """
        Problem: Happy Number
        Difficulty: Medium
        Time Complexity: O(log n)
        """
        visit = set()
        
        while n not in visit:
            visit.add(n)
            n = self.sumOfSquares(n)
            
            if n == 1:
                return True
        return False
    
    def sumOfSquares(self, n: int) -> int:
        output = 0
        while n:
            digit = n % 10
            output += digit ** 2
            n //= 10
        return output
