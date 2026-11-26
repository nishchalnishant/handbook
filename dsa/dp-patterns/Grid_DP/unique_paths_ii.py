def unique_paths_with_obstacles(obstacleGrid):
    """
    Problem: Unique paths with obstacles (1 denotes obstacle).
    
    Approach: Grid DP
    - If cell is obstacle, dp[i][j] = 0.
    - Else, dp[i][j] = dp[i-1][j] + dp[i][j-1].
    
    Time Complexity: O(M*N)
    Space Complexity: O(N)
    """
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [0] * n
    dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
    
    for i in range(m):
        for j in range(n):
            if obstacleGrid[i][j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j-1]
                
    return dp[n-1]

# Example Usage
if __name__ == "__main__":
    grid = [[0,0,0],[0,1,0],[0,0,0]]
    print(f"Unique Paths with Obstacles: {unique_paths_with_obstacles(grid)}")
