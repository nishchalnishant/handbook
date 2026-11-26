from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        """
        Problem: Number of Islands
        Pattern: DFS (Flood Fill)
        """
        if not grid: return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0':
                return
            grid[r][c] = '0' # Mark as visited
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
            
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        """
        Problem: Max Area of Island
        Pattern: DFS
        """
        rows, cols = len(grid), len(grid[0])
        max_area = 0
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == 0:
                return 0
            grid[r][c] = 0
            return 1 + dfs(r+1, c) + dfs(r-1, c) + dfs(r, c+1) + dfs(r, c-1)
            
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    max_area = max(max_area, dfs(r, c))
        return max_area

    def solve(self, board: List[List[str]]) -> None:
        """
        Problem: Surrounded Regions
        Pattern: DFS (Reverse thinking: capture borders)
        """
        if not board: return
        rows, cols = len(board), len(board[0])
        
        def dfs(r, c):
            if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != 'O':
                return
            board[r][c] = 'temp'
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
            
        # Capture unsubmerged regions (connected to border)
        for r in range(rows):
            for c in range(cols):
                if (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and board[r][c] == 'O':
                    dfs(r, c)
        
        # Flip
        for r in range(rows):
            for c in range(cols):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
                elif board[r][c] == 'temp':
                    board[r][c] = 'O'
