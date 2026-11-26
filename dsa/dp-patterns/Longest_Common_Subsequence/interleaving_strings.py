def is_interleave(s1, s2, s3):
    """
    Problem: Leetcode 97. Check if s3 is formed by interleaving s1 and s2.
    
    Approach: LCS / Grid DP
    - dp[i][j] = True if s3[0...i+j-1] is formed by s1[0...i-1] and s2[0...j-1].
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N)
    """
    if len(s1) + len(s2) != len(s3): return False
    
    m, n = len(s1), len(s2)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i > 0 and s1[i-1] == s3[i+j-1]:
                dp[i][j] |= dp[i-1][j]
            if j > 0 and s2[j-1] == s3[i+j-1]:
                dp[i][j] |= dp[i][j-1]
                
    return dp[m][n]

# Example Usage
if __name__ == "__main__":
    s1, s2, s3 = "aabcc", "dbbca", "aadbbcbcac"
    print(f"Is Interleave: {is_interleave(s1, s2, s3)}")
