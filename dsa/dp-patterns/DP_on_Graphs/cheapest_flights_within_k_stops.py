def find_cheapest_price(n, flights, src, dst, k):
    """
    Problem: Min cost from src to dst with at most k stops.
    
    Approach: Bellman-Ford / DP
    - dp[k][u] = min cost to u with at most k edges (k-1 stops).
    - We need k+1 edges allowed (k stops).
    - Relax edges k+1 times.
    
    Time Complexity: O(K * E)
    Space Complexity: O(N)
    """
    prices = [float('inf')] * n
    prices[src] = 0
    
    for i in range(k + 1):
        tmp_prices = prices[:]
        for s, d, p in flights:
            if prices[s] == float('inf'):
                continue
            if prices[s] + p < tmp_prices[d]:
                tmp_prices[d] = prices[s] + p
        prices = tmp_prices
        
    return prices[dst] if prices[dst] != float('inf') else -1

# Example Usage
if __name__ == "__main__":
    n = 4
    flights = [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]]
    src, dst, k = 0, 3, 1
    print(f"Cheapest price: {find_cheapest_price(n, flights, src, dst, k)}")
