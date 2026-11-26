def longest_common_substring(s1, s2):
    """
    Problem: Find the length of the longest substring common to both strings (contiguous).
    
    Approach: LCS Pattern
    - dp[i][j] = length of common substring ending at s1[i-1] and s2[j-1].
    - If s1[i-1] == s2[j-1]: dp[i][j] = 1 + dp[i-1][j-1]
    - Else: dp[i][j] = 0 (reset because substring must be contiguous)
    - Keep track of max value in dp table.
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
                max_len = max(max_len, dp[i][j])
            else:
                dp[i][j] = 0
                
    return max_len

# Example Usage
if __name__ == "__main__":
    s1 = "ABCDGH"
    s2 = "ACDGHR"
    print(f"LCS substring length: {longest_common_substring(s1, s2)}")
