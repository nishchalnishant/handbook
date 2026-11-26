def max_profit_ii(prices):
    """
    Problem: Buy and sell multiple times.
    
    Approach: Greedy / Accumulate positive differences.
    - If prices[i] > prices[i-1], we buy at i-1 and sell at i.
    - Total profit = sum(max(0, prices[i] - prices[i-1]))
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    profit = 0
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            profit += prices[i] - prices[i-1]
            
    return profit

# Example Usage
if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print(f"Max profit (multiple transactions): {max_profit_ii(prices)}")
