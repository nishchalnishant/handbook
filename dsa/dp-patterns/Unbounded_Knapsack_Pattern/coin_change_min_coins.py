def coin_change_min(coins, amount):
    """
    Problem: Find minimum number of coins needed to make up the amount.
    
    Approach: Unbounded Knapsack Pattern
    - dp[j] = min coins to make amount 'j'
    - transition: dp[j] = min(dp[j], dp[j - coin] + 1)
    
    Time Complexity: O(N * Amount)
    Space Complexity: O(Amount)
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for coin in coins:
        for j in range(coin, amount + 1):
            if dp[j - coin] != float('inf'):
                dp[j] = min(dp[j], dp[j - coin] + 1)
            
    return dp[amount] if dp[amount] != float('inf') else -1

# Example Usage
if __name__ == "__main__":
    coins = [1, 2, 5]
    amount = 11
    print(f"Min coins for {amount}: {coin_change_min(coins, amount)}")
