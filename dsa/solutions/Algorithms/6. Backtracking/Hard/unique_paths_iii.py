from typing import List

class Solution:
    def uniquePathsIII(self, grid: List[List[int]]) -> int:
        """
        Problem: Unique Paths III
        Difficulty: Hard
        """
        ROWS, COLS = len(grid), len(grid[0])
        start, end = None, None
        empty = 0
        
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:
                    start = (r, c)
                elif grid[r][c] == 2:
                    end = (r, c)
                
                if grid[r][c] != -1:
                    empty += 1
                    
        res = 0
        def dfs(r, c, visited):
            nonlocal res
            if (r < 0 or r == ROWS or c < 0 or c == COLS or
                grid[r][c] == -1):
                return
            
            if (r, c) == end:
                if visited == empty:
                    res += 1
                return
                
            grid[r][c] = -1 # mark visited
            dfs(r + 1, c, visited + 1)
            dfs(r - 1, c, visited + 1)
            dfs(r, c + 1, visited + 1)
            dfs(r, c - 1, visited + 1)
            grid[r][c] = 0 # backtrack
            
        dfs(start[0], start[1], 1)
        return res
