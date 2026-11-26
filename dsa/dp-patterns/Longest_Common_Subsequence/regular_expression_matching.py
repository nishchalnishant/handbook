def is_match_regex(s, p):
    """
    Problem: Regex matching with '.' (any char) and '*' (zero or more of preceding element).
    
    Approach: LCS Pattern
    - dp[i][j] = match between s[:i] and p[:j]
    - If p[j-1] == '.' or p[j-1] == s[i-1]: dp[i][j] = dp[i-1][j-1]
    - If p[j-1] == '*':
        - Zero occurences of preceeding char (p[j-2]): dp[i][j-2]
        - One+ occurences (if s[i-1] matches p[j-2]): dp[i-1][j]
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(s), len(p)
    dp = [[False] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*b*c* matching empty
    for j in range(1, m + 1):
        if p[j-1] == '*':
            dp[0][j] = dp[0][j-2]
            
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if p[j-1] == '.' or p[j-1] == s[i-1]:
                dp[i][j] = dp[i-1][j-1]
            elif p[j-1] == '*':
                dp[i][j] = dp[i][j-2] # Zero occurrences
                if p[j-2] == '.' or p[j-2] == s[i-1]:
                    dp[i][j] = dp[i][j] or dp[i-1][j] # One or more
                    
    return dp[n][m]

# Example Usage
if __name__ == "__main__":
    s = "aab"
    p = "c*a*b"
    print(f"Regex match: {is_match_regex(s, p)}")
