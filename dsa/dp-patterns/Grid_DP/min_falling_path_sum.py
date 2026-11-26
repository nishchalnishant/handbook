def min_falling_path_sum(matrix):
    """
    Problem: Start at any element in first row, move to (row+1, col-1), (row+1, col), or (row+1, col+1). Find min sum.
    
    Approach: Grid DP
    - dp[i][j] = matrix[i][j] + min(dp[i-1][j-1], dp[i-1][j], dp[i-1][j+1])
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N) (Can be O(1) in-place)
    """
    n = len(matrix)
    dp = [row[:] for row in matrix]
    
    for i in range(1, n):
        for j in range(n):
            top = dp[i-1][j]
            top_left = dp[i-1][j-1] if j > 0 else float('inf')
            top_right = dp[i-1][j+1] if j < n - 1 else float('inf')
            
            dp[i][j] += min(top, top_left, top_right)
            
    return min(dp[n-1])

# Example Usage
if __name__ == "__main__":
    matrix = [[2,1,3],[6,5,4],[7,8,9]]
    print(f"Min Falling Path Sum: {min_falling_path_sum(matrix)}")
