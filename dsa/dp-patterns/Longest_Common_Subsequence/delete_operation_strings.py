def min_distance(word1, word2):
    """
    Problem: Leetcode 583. Min steps to make word1 and word2 same by deleting characters.
    
    Approach: LCS
    - Find Longest Common Subsequence length.
    - Result = len(word1) - LCS + len(word2) - LCS.
    
    Time Complexity: O(M*N)
    Space Complexity: O(M*N)
    """
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i-1] == word2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                
    lcs = dp[m][n]
    return m + n - 2 * lcs

# Example Usage
if __name__ == "__main__":
    w1, w2 = "sea", "eat"
    print(f"Min deletions: {min_distance(w1, w2)}")
