def unique_paths(m, n):
    """
    Problem: Count unique paths from top-left to bottom-right in m x n grid. Move only down or right.
    
    Approach: Grid DP
    - dp[i][j] = ways to reach cell (i, j)
    - dp[i][j] = dp[i-1][j] (from top) + dp[i][j-1] (from left)
    - Base case: dp[0][0] = 1, or initialize first row and col to 1.
    
    Time Complexity: O(M*N)
    Space Complexity: O(N) (Optimized from O(M*N))
    """
    row = [1] * n
    
    for i in range(1, m):
        new_row = [1] * n
        for j in range(1, n):
            new_row[j] = new_row[j-1] + row[j]
        row = new_row
        
    return row[-1]

# Example Usage
if __name__ == "__main__":
    m, n = 3, 7
    print(f"Unique Paths: {unique_paths(m, n)}")
