from typing import List

class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        """
        Problem: Unique Paths
        Pattern: Grid DP
        """
        row = [1] * n
        
        # Go bottom up
        for i in range(m - 1):
            newRow = [1] * n
            for j in range(n - 2, -1, -1):
                newRow[j] = newRow[j+1] + row[j]
            row = newRow
        return row[0]

    def minPathSum(self, grid: List[List[int]]) -> int:
        """
        Problem: Minimum Path Sum
        Pattern: Grid DP
        """
        rows, cols = len(grid), len(grid[0])
        
        res = [[float('inf')] * (cols + 1) for _ in range(rows + 1)]
        res[rows - 1][cols] = 0 # Base case
        
        for r in range(rows - 1, -1, -1):
            for c in range(cols - 1, -1, -1):
                res[r][c] = grid[r][c] + min(res[r+1][c], res[r][c+1])
                
        return res[0][0]
