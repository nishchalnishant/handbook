def num_squares(n):
    """
    Problem: Leetcode 279. Least number of perfect squares that sum to n.
    
    Approach: Unbounded Knapsack / BFS
    - Items: squares [1, 4, 9, 16...]
    - Capacity: n
    - Value: -1 (minimize count) or Cost 1.
    - dp[i] = min squares to sum to i.
    - dp[i] = min(dp[i - square]) + 1
    
    Time Complexity: O(N * sqrt(N))
    Space Complexity: O(N)
    """
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    
    squares = []
    i = 1
    while i*i <= n:
        squares.append(i*i)
        i += 1
        
    for s in squares:
        for i in range(s, n + 1):
            dp[i] = min(dp[i], dp[i-s] + 1)
            
    return dp[n]

# Example Usage
if __name__ == "__main__":
    n = 12
    print(f"Min perfect squares for {n}: {num_squares(n)}")
