def count_paths(grid):
    """
    Problem: Leetcode 2328. Number of Increasing Paths in a Grid.
    From cell, move up/down/left/right if next cell value > current cell.
    
    Approach: Grid DP with Memoization (DFS)
    - dp[i][j] = 1 + sum(dp[neighbors]) where neighbor > current
    - Sort cells by value to process in order? Or just Memoized DFS.
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N)
    """
    m, n = len(grid), len(grid[0])
    MOD = 10**9 + 7
    memo = [[0] * n for _ in range(m)]
    
    def dfs(i, j):
        if memo[i][j]: return memo[i][j]
        
        c = 1
        for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > grid[i][j]:
                c = (c + dfs(ni, nj)) % MOD
                
        memo[i][j] = c
        return c
        
    ans = 0
    for i in range(m):
        for j in range(n):
            ans = (ans + dfs(i, j)) % MOD
            
    return ans

# Example Usage
if __name__ == "__main__":
    grid = [[1, 1], [3, 4]]
    print(f"Number of Increasing Paths: {count_paths(grid)}")
