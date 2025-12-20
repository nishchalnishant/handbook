def tsp(dist):
    """
    Problem: Find shortest route visiting all cities and returning to start (0).
    
    Approach: Bitmask DP
    - dp[mask][i] = min cost to visit nodes in 'mask' ending at node 'i'.
    - Transition: dp[mask | (1<<j)][j] = min(dp[mask | (1<<j)][j], dp[mask][i] + dist[i][j])
    - Final Answer: min(dp[(1<<n)-1][i] + dist[i][0]) for all i.
    
    Time Complexity: O(2^N * N^2)
    Space Complexity: O(2^N * N)
    """
    n = len(dist)
    # 1 << n states, n ending nodes
    dp = [[float('inf')] * n for _ in range(1 << n)]
    
    # Base case: cost to reach node i from 0 visiting only i is dist[0][i]
    # Assuming we start at 0. 'mask' for visiting only i is 1<<i.
    # Note: Usually we assume mask includes 0 and i, so base mask for just 0 is 1.
    # Actually, simpler: dp[1<<i][i] = dist[0][i] if we consider 0->i as first step?
    # Standard: Start at 0, mask 1 (0th bit set).
    dp[1][0] = 0
    
    for mask in range(1, 1 << n):
        for u in range(n):
            if (mask >> u) & 1: # If u is in mask
                if dp[mask][u] == float('inf'): continue
                
                # Try to go to next node v
                for v in range(n):
                    if not ((mask >> v) & 1): # If v not in mask
                        next_mask = mask | (1 << v)
                        dp[next_mask][v] = min(dp[next_mask][v], dp[mask][u] + dist[u][v])
                        
    # Close the tour: Go back to 0 from any node i covering all nodes
    full_mask = (1 << n) - 1
    ans = float('inf')
    for i in range(1, n):
        ans = min(ans, dp[full_mask][i] + dist[i][0])
        
    return ans

# Example Usage
if __name__ == "__main__":
    # Distance matrix
    dist = [[0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]]
    print(f"Min TSP Cost: {tsp(dist)}")
