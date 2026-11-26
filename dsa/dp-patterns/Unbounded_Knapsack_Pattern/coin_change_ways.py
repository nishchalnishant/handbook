def coin_change_ways(coins, amount):
    """
    Problem: Count the number of combinations to make up the amount using given coins (unlimited supply).
    
    Approach: Unbounded Knapsack Pattern
    - dp[j] = number of ways to make amount 'j'
    - transition: dp[j] += dp[j - coin]
    
    Time Complexity: O(N * Amount)
    Space Complexity: O(Amount)
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for j in range(coin, amount + 1):
            dp[j] += dp[j - coin]
            
    return dp[amount]

# Example Usage
if __name__ == "__main__":
    coins = [1, 2, 5]
    amount = 5
    print(f"Ways to make change for {amount}: {coin_change_ways(coins, amount)}")
