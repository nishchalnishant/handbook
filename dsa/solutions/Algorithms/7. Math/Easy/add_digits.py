class Solution:
    def addDigits(self, num: int) -> int:
        """
        Problem: Add Digits
        Difficulty: Easy
        Time Complexity: O(1)
        """
        if num == 0: return 0
        if num % 9 == 0: return 9
        return num % 9
