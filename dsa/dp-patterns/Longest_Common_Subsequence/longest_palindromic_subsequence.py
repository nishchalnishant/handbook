def longest_palindrome_subseq(s):
    """
    Problem: Find length of longest subsequence of s that is a palindrome.
    
    Approach: LCS Pattern
    - The LPS of 's' is the LCS of 's' and 'reverse(s)'.
    - Alternatively, can solve directly on one string range constraints:
      - dp[i][j] = LPS of s[i...j]
      - if s[i] == s[j]: 2 + dp[i+1][j-1]
      - else: max(dp[i+1][j], dp[i][j-1])
    
    Time Complexity: O(N^2)
    Space Complexity: O(N^2)
    """
    n = len(s)
    s_rev = s[::-1]
    
    # LCS of s and s_rev
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if s[i-1] == s_rev[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                
    return dp[n][n]

# Example Usage
if __name__ == "__main__":
    s = "bbbab"
    print(f"Longest Palindromic Subsequence: {longest_palindrome_subseq(s)}")
