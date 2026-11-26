def maximal_square(matrix):
    """
    Problem: Find largest square containing only 1s and return its area.
    
    Approach: Grid DP
    - dp[i][j] = side length of largest square ending at (i, j).
    - If matrix[i][j] == '1':
        dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N)
    """
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_side = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if matrix[i-1][j-1] == '1':
                dp[i][j] = min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1]) + 1
                max_side = max(max_side, dp[i][j])
                
    return max_side * max_side

# Example Usage
if __name__ == "__main__":
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    print(f"Maximal Square Area: {maximal_square(matrix)}")
