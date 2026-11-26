def max_gold(grid):
    """
    Problem: Miner starts at any row in col 0. Can move right, right-up, or right-down. Maximize gold collected.
    
    Approach: Grid DP
    - Similar to Min Path Sum but moves are different.
    - Traverse col by col from right to left (or left to right depending on definition, but usually "next step" dependencies).
    - If moving Right->Left is easier to conceptualize dependencies (value at col j depends on col j+1).
    Or standard: dp[i][j] is max gold reaching (i, j).
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N)
    """
    n, m = len(grid), len(grid[0])
    dp = [[0] * m for _ in range(n)]
    
    # Initialize last column
    for i in range(n):
        dp[i][m-1] = grid[i][m-1]
        
    for j in range(m - 2, -1, -1):
        for i in range(n):
            right = dp[i][j+1]
            right_up = dp[i-1][j+1] if i > 0 else 0
            right_down = dp[i+1][j+1] if i < n - 1 else 0
            
            dp[i][j] = grid[i][j] + max(right, right_up, right_down)
            
    return max(dp[i][0] for i in range(n))

# Example Usage
if __name__ == "__main__":
    grid = [[1, 3, 3],
            [2, 1, 4],
            [0, 6, 4]]
    print(f"Max Gold: {max_gold(grid)}")
