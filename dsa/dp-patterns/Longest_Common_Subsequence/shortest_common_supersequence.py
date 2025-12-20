def shortest_common_supersequence(str1, str2):
    """
    Problem: Find the shortest string that has both str1 and str2 as subsequences.
    
    Approach: LCS Pattern
    - Length of SCS = len(str1) + len(str2) - len(LCS(str1, str2))
    - To reconstruct the string, backtrack the LCS table:
        - If characters match, include once.
        - If mismatch, include the character from the side that gave max, and move.
    
    Time Complexity: O(N*M)
    Space Complexity: O(N*M)
    """
    n, m = len(str1), len(str2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                
    # Backtrack
    i, j = n, m
    res = []
    while i > 0 and j > 0:
        if str1[i-1] == str2[j-1]:
            res.append(str1[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            res.append(str1[i-1])
            i -= 1
        else:
            res.append(str2[j-1])
            j -= 1
            
    while i > 0:
        res.append(str1[i-1])
        i -= 1
    while j > 0:
        res.append(str2[j-1])
        j -= 1
        
    return "".join(res[::-1])

# Example Usage
if __name__ == "__main__":
    str1 = "abac"
    str2 = "cab"
    print(f"Shortest Common Supersequence: {shortest_common_supersequence(str1, str2)}")
