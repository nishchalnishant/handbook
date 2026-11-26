def min_path_sum(grid):
    """
    Problem: Find path from top-left to bottom-right min sum of numbers along path.
    
    Approach: Grid DP
    - dp[i][j] = grid[i][j] + min(dp[i-1][j], dp[i][j-1])
    - Can modify grid in-place to save space.
    
    Time Complexity: O(M*N)
    Space Complexity: O(1) (In-place)
    """
    m, n = len(grid), len(grid[0])
    
    for i in range(m):
        for j in range(n):
            if i == 0 and j == 0:
                continue
            elif i == 0:
                grid[i][j] += grid[i][j-1]
            elif j == 0:
                grid[i][j] += grid[i-1][j]
            else:
                grid[i][j] += min(grid[i-1][j], grid[i][j-1])
                
    return grid[m-1][n-1]

# Example Usage
if __name__ == "__main__":
    grid = [[1,3,1],[1,5,1],[4,2,1]]
    print(f"Min Path Sum: {min_path_sum(grid)}")
