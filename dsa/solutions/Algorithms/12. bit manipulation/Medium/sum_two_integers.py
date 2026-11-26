class Solution:
    def getSum(self, a: int, b: int) -> int:
        """
        Problem: Sum of Two Integers
        Difficulty: Medium
        Time Complexity: O(1)
        """
        # Python handles large integers automatically, so we need to mask for 32-bit
        mask = 0xffffffff
        
        while (b & mask) > 0:
            carry = (a & b) << 1
            a = (a ^ b)
            b = carry
            
        # Handle negative result
        return (a & mask) if b > 0 else a
