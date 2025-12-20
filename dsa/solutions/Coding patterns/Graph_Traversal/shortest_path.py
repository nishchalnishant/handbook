from typing import List
import heapq

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        """
        Problem: Network Delay Time
        Pattern: Dijkstra's Algorithm
        """
        adj = {i: [] for i in range(1, n + 1)}
        for u, v, w in times:
            adj[u].append((v, w))
            
        min_heap = [(0, k)] # (dist, node)
        visit = set()
        t = 0
        
        while min_heap:
            w1, n1 = heapq.heappop(min_heap)
            if n1 in visit: continue
            visit.add(n1)
            t = max(t, w1)
            
            for n2, w2 in adj[n1]:
                if n2 not in visit:
                    heapq.heappush(min_heap, (w1 + w2, n2))
                    
        return t if len(visit) == n else -1

    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        """
        Problem: Cheapest Flights Within K Stops
        Pattern: Bellman-Ford (or modified Dijkstra)
        """
        # Bellman-Ford approach
        prices = [float("inf")] * n
        prices[src] = 0
        
        for i in range(k + 1):
            tmp_prices = prices.copy()
            for s, d, p in flights: # s=source, d=dest, p=price
                if prices[s] == float("inf"):
                    continue
                if prices[s] + p < tmp_prices[d]:
                    tmp_prices[d] = prices[s] + p
            prices = tmp_prices
            
        return -1 if prices[dst] == float("inf") else prices[dst]
