def max_profit_iii(prices):
    """
    Problem: At most 2 transactions.
    
    Approach: DP / State Machine
    - States:
        - t1_cost: Min cost to buy 1st stock
        - t1_profit: Max profit after selling 1st stock
        - t2_cost: Min effective cost to buy 2nd stock (price - t1_profit)
        - t2_profit: Max profit after selling 2nd stock
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    t1_cost, t2_cost = float('inf'), float('inf')
    t1_profit, t2_profit = 0, 0
    
    for p in prices:
        # Transaction 1
        t1_cost = min(t1_cost, p)
        t1_profit = max(t1_profit, p - t1_cost)
        
        # Transaction 2 (Reinvest t1_profit)
        t2_cost = min(t2_cost, p - t1_profit)
        t2_profit = max(t2_profit, p - t2_cost)
        
    return t2_profit

# Example Usage
if __name__ == "__main__":
    prices = [3, 3, 5, 0, 0, 3, 1, 4]
    print(f"Max profit (2 transactions): {max_profit_iii(prices)}")
