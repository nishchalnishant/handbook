def min_cost_tickets(days, costs):
    """
    Problem: Leetcode 983. Minimum Cost For Tickets.
    You have days you want to travel. Costs for 1-day, 7-day, 30-day passes.
    
    Approach: Unbounded Knapsack / DP on constraints
    - dp[i] = min cost to cover travel up to day 'i'
    - If 'i' is not a travel day, dp[i] = dp[i-1]
    - Else, dp[i] = min(dp[i-1]+cost[0], dp[i-7]+cost[1], dp[i-30]+cost[2])
    
    Time Complexity: O(MaxDay)
    Space Complexity: O(MaxDay)
    """
    max_day = days[-1]
    travel_days = set(days)
    dp = [0] * (max_day + 1)
    
    for i in range(1, max_day + 1):
        if i not in travel_days:
            dp[i] = dp[i-1]
        else:
            cost1 = dp[i-1] + costs[0]
            cost7 = dp[max(0, i-7)] + costs[1]
            cost30 = dp[max(0, i-30)] + costs[2]
            dp[i] = min(cost1, cost7, cost30)
            
    return dp[max_day]

# Example Usage
if __name__ == "__main__":
    days = [1, 4, 6, 7, 8, 20]
    costs = [2, 7, 15]
    print(f"Min cost for tickets: {min_cost_tickets(days, costs)}")
