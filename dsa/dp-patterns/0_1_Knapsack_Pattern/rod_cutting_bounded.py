def rod_cutting_bounded(lengths, prices, max_len):
    """
    Problem: Rod cutting where each specific piece length is distinct/unique (bounded).
    Given lengths and prices of piece types, and we have exactly ONE of each type.
    Maximize profit.
    
    Approach: 0/1 Knapsack Pattern
    - Weights = lengths
    - Values = prices
    - Capacity = max_len
    
    Time Complexity: O(N * max_len)
    Space Complexity: O(max_len)
    """
    n = len(lengths)
    dp = [0] * (max_len + 1)
    
    for i in range(n):
        length = lengths[i]
        price = prices[i]
        # Iterate backwards
        for j in range(max_len, length - 1, -1):
            dp[j] = max(dp[j], dp[j - length] + price)
            
    return dp[max_len]

# Example Usage
if __name__ == "__main__":
    lengths = [1, 2, 3, 4, 5, 6, 7, 8]
    prices = [1, 5, 8, 9, 10, 17, 17, 20]
    max_len = 4
    # treating as 0/1 knapsack (only 1 of each length available in this variant)
    print(f"Max profit (Bounded/0-1): {rod_cutting_bounded(lengths, prices, max_len)}")
