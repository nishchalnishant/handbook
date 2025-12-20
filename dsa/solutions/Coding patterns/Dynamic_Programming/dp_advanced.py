from typing import List

class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """
        Problem: Best Time to Buy and Sell Stock with Cooldown
        Pattern: State Machine DP
        """
        # State: held, sold, reset
        held, sold, reset = -float('inf'), -float('inf'), 0
        
        for price in prices:
            prev_sold = sold
            sold = held + price
            held = max(held, reset - price)
            reset = max(reset, prev_sold)
            
        return max(sold, reset)

    def maxProfitIII(self, prices: List[int]) -> int:
        """
        Problem: Best Time to Buy and Sell Stock III
        Pattern: State Machine DP (At most 2 transactions)
        """
        t1_cost, t2_cost = float('inf'), float('inf')
        t1_profit, t2_profit = 0, 0
        
        for price in prices:
            t1_cost = min(t1_cost, price)
            t1_profit = max(t1_profit, price - t1_cost)
            t2_cost = min(t2_cost, price - t1_profit)
            t2_profit = max(t2_profit, price - t2_cost)
            
        return t2_profit
