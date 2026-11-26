def assign_tasks(tasks, time_limit):
    """
    Problem: Select maximum number of tasks that finish within time_limit.
    Essentially 0/1 Knapsack where value of each task is 1 and weight is duration.
    
    Approach: 0/1 Knapsack
    - dp[w] = max tasks with time w.
    
    Time Complexity: O(N * T)
    Space Complexity: O(T)
    """
    # Simply max items that fit? Sort by time shortest first (Greedy).
    # If tasks have values, then it's Knapsack.
    # Assuming standard knapsack where tasks have different importance/value.
    
    # Let's say: task = (duration, importance)
    # maximizes importance within time_limit.
    
    n = len(tasks)
    dp = [0] * (time_limit + 1)
    
    for duration, importance in tasks:
        for t in range(time_limit, duration - 1, -1):
            dp[t] = max(dp[t], dp[t - duration] + importance)
            
    return dp[time_limit]

# Example Usage
if __name__ == "__main__":
    tasks = [(10, 5), (20, 10), (30, 20)] # (duration, importance)
    limit = 40
    print(f"Max importance: {assign_tasks(tasks, limit)}")
