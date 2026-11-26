def is_match_wildcard(s, p):
    """
    Problem: Implement wildcard matching with '?' (any char) and '*' (sequence of length 0+).
    
    Approach: LCS Pattern
    - dp[i][j] = match between s[:i] and p[:j]
    - If p[j-1] == '?' or s[i-1] == p[j-1]: dp[i][j] = dp[i-1][j-1]
    - If p[j-1] == '*':
        - '*' matches empty: dp[i][j-1]
        - '*' matches s[i-1] (and maybe more): dp[i-1][j]
        - dp[i][j] = dp[i][j-1] or dp[i-1][j]
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    # Handle patterns starting with *
    for j in range(1, m + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-1]
            
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j-1] == '?' or s[i-1] == p[j-1]:
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-1] or dp[i-1][j]
                
    return dp[n][m]

# Example Usage
if __name__ == "__main__":
    s = "adceb"
    p = "*a*b"
    print(f"Wildcard match: {is_match_wildcard(s, p)}")
