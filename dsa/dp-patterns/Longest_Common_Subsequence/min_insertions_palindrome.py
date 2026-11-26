def min_insertions(s):
    """
    Problem: Min insertions to make string palindrome.
    
    Approach: LCS
    - Find Longest Palindromic Subsequence (LPS).
    - Result = len(s) - LPS.
    - LPS of s is LCS(s, reverse(s)).
    
    Time Complexity: O(N^2)
    Space Complexity: O(N^2)
    """
    # Helper for LCS
    def lcs(text1, text2):
        m, n = len(text1), len(text2)
        dp = [0] * (n + 1)
        for c1 in text1:
            prev = 0
            for j, c2 in enumerate(text2):
                temp = dp[j+1]
                if c1 == c2:
                    dp[j+1] = prev + 1
                else:
                    dp[j+1] = max(dp[j+1], dp[j])
                prev = temp
        return dp[n]
        
    lps_len = lcs(s, s[::-1])
    return len(s) - lps_len

# Example Usage
if __name__ == "__main__":
    s = "zzazz"
    print(f"Min insertions: {min_insertions(s)}")
