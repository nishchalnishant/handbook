def max_profit(prices):
    """
    Problem: Maximize profit by buying and selling once.
    
    Approach: Kadane's Variant / Greedy
    - Maintain `min_price` seen so far.
    - Profit at current step = price - min_price.
    - Update global max_profit.
    - Essentially finding max subarray sum of differences array.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not prices: return 0
    
    min_price = float('inf')
    max_p = 0
    
    for p in prices:
        if p < min_price:
            min_price = p
        elif p - min_price > max_p:
            max_p = p - min_price
            
    return max_p

# Example Usage
if __name__ == "__main__":
    prices = [7, 1, 5, 3, 6, 4]
    print(f"Max profit: {max_profit(prices)}")
