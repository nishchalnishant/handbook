def min_cost_climbing_stairs(cost):
    """
    Problem: Leetcode 746. Min Cost Climbing Stairs.
    Pay cost[i] to climb 1 or 2 steps. Start at 0 or 1.
    
    Approach: Simple DP
    - dp[i] = cost to reach step i.
    - dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])
    - Optimized: Keep track of just two previous costs.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    n = len(cost)
    prev2 = 0 # Step -2 (virtual)
    prev1 = 0 # Step -1 (virtual)
    # Reaching step 0 or 1 is free initially, but we pay to leave?
    # Standard def: Cost to reach TOP of floor.
    # cost[i] is cost to jump FROM index i.
    
    for i in range(2, n + 1):
        curr = min(prev1 + cost[i-1], prev2 + cost[i-2])
        prev2 = prev1
        prev1 = curr
        
    return prev1

# Example Usage
if __name__ == "__main__":
    cost = [10, 15, 20]
    print(f"Min cost: {min_cost_climbing_stairs(cost)}")
