def min_distance(word1, word2):
    """
    Problem: Minimum operations (insert, delete, replace) to convert word1 to word2.
    
    Approach: LCS Pattern
    - dp[i][j] = min ops for word1[:i] -> word2[:j]
    - If chars match: dp[i][j] = dp[i-1][j-1]
    - If chars mismatch: 1 + min(insert, delete, replace)
        - insert: dp[i][j-1]
        - delete: dp[i-1][j]
        - replace: dp[i-1][j-1]
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    # Base cases
    for i in range(n + 1): dp[i][0] = i
    for j in range(m + 1): dp[0][j] = j
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j],    # Delete
                                   dp[i][j-1],    # Insert
                                   dp[i-1][j-1])  # Replace
                                   
    return dp[n][m]

# Example Usage
if __name__ == "__main__":
    word1 = "horse"
    word2 = "ros"
    print(f"Edit Distance: {min_distance(word1, word2)}")
