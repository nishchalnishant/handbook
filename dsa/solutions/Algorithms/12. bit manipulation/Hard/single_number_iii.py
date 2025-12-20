from typing import List

class Solution:
    def singleNumber(self, nums: List[int]) -> List[int]:
        """
        Problem: Single Number III
        Difficulty: Hard
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        xor = 0
        for n in nums:
            xor ^= n
            
        # Find lowest set bit
        mask = 1
        while not (xor & mask):
            mask <<= 1
            
        a, b = 0, 0
        for n in nums:
            if n & mask:
                a ^= n
            else:
                b ^= n
        return [a, b]
