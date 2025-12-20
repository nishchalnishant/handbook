def num_distinct(s, t):
    """
    Problem: Count distinct subsequences of s which equals t.
    
    Approach: LCS Pattern
    - dp[i][j] = num ways to form t[:j] from s[:i]
    - If s[i-1] == t[j-1]:
        - We can use s[i-1] to match t[j-1]: dp[i-1][j-1]
        - We can skip s[i-1]: dp[i-1][j]
        - dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
    - Else: s[i-1] cannot help match t[j-1], must skip: dp[i-1][j]
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(s), len(t)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        dp[i][0] = 1 # Empty t is subsequence of any s
        
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s[i-1] == t[j-1]:
                dp[i][j] = dp[i-1][j-1] + dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j]
                
    return dp[n][m]

# Example Usage
if __name__ == "__main__":
    s = "rabbbit"
    t = "rabbit"
    print(f"Distinct subsequences: {num_distinct(s, t)}")
