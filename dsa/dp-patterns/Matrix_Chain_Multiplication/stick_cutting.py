def min_cost_cut_stick(n, cuts):
    """
    Problem: Leetcode 1547. Minimum cost to cut a stick of length n. Cost = length of stick segment being cut.
    
    Approach: MCM Pattern
    - Sort cuts and add 0 and n.
    - dp[i][j] = min cost to cut segment between cuts[i] and cuts[j].
    - dp[i][j] = length(cuts[j]-cuts[i]) + min(dp[i][k] + dp[k][j]) for k in cuts between i, j.
    
    Time Complexity: O(M^3) where M is number of cuts.
    Space Complexity: O(M^2)
    """
    cuts = sorted(cuts)
    cuts = [0] + cuts + [n]
    m = len(cuts)
    dp = [[0] * m for _ in range(m)]
    
    for length in range(2, m):
        for i in range(m - length):
            j = i + length
            cost = cuts[j] - cuts[i]
            dp[i][j] = float('inf')
            for k in range(i + 1, j):
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k][j] + cost)
                
    return dp[0][m-1]

# Example Usage
if __name__ == "__main__":
    n = 7
    cuts = [1, 3, 4, 5]
    print(f"Min cost to cut stick: {min_cost_cut_stick(n, cuts)}")
