from typing import List

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        """
        Problem: Search a 2D Matrix II
        Difficulty: Medium
        Time Complexity: O(n + m)
        Space Complexity: O(1)
        """
        ROWS, COLS = len(matrix), len(matrix[0])
        
        r, c = 0, COLS - 1
        
        while r < ROWS and c >= 0:
            if matrix[r][c] > target:
                c -= 1
            elif matrix[r][c] < target:
                r += 1
            else:
                return True
        return False
