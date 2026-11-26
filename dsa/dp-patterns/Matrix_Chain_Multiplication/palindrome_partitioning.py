def min_cut(s):
    """
    Problem: Minimum cuts to partition string s such that everyone substring is a palindrome.
    
    Approach: MCM / Partition DP
    - Optimized approach uses O(N^2) palindrome check + O(N^2) DP.
    - dp[i] = min cuts for s[0...i-1].
    - dp[i] = min(dp[j] + 1) for all j < i if s[j...i-1] is palindrome.
    (This is slightly more efficient than full simple MCM O(N^3))
    
    Time Complexity: O(N^2)
    Space Complexity: O(N^2) (for palindrome table)
    """
    n = len(s)
    # is_pal[i][j] is True if s[i:j+1] is palindrome
    is_pal = [[False] * n for _ in range(n)]
    
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length <= 2 or is_pal[i+1][j-1]:
                    is_pal[i][j] = True
                    
    # dp[i] = min cuts for prefix of length i
    dp = [float('inf')] * (n + 1)
    dp[0] = -1 # Base case adjustment so first cut counts correctly
    
    for i in range(1, n + 1):
        for j in range(i):
            if is_pal[j][i-1]:
                dp[i] = min(dp[i], dp[j] + 1)
                
    return dp[n]

# Example Usage
if __name__ == "__main__":
    s = "aab"
    print(f"Min cuts: {min_cut(s)}")
