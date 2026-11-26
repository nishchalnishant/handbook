class Solution:
    def rangeBitwiseAnd(self, left: int, right: int) -> int:
        """
        Problem: Bitwise AND of Numbers Range
        Difficulty: Medium
        Time Complexity: O(1)
        """
        shift = 0
        while left < right:
            left >>= 1
            right >>= 1
            shift += 1
        return left << shift
