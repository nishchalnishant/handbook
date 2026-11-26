def rod_cutting_unbounded(prices, n):
    """
    Problem: Maximize profit by cutting a rod of length 'n', given prices for each length 1..n. Pieces can be repeated.
    
    Approach: Unbounded Knapsack Pattern
    - dp[j] = max profit for length 'j'
    - transition: dp[j] = max(dp[j], price[len] + dp[j - len])
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    # prices[i] allows for length i+1
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1): # Lengths 1 to n
        for j in range(i, n + 1):
            dp[j] = max(dp[j], prices[i-1] + dp[j - i])
            
    return dp[n]

# Example Usage
if __name__ == "__main__":
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    n = 8
    print(f"Max profit for rod length {n}: {rod_cutting_unbounded(prices, n)}")
