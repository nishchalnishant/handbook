"""
Advanced graph algorithms — Google L4 interview prep.

Covers the three classic algorithms not yet present elsewhere in this repo:
Bellman-Ford (negative edges / edge-relaxation), Floyd-Warshall (all-pairs
shortest path), and Prim's (heap-based MST, contrast with Kruskal in
07_union_find.py).

Dijkstra (positive-weight single-source) and Kruskal's MST (via union-find)
already live in 06_graph_algorithms.py and 07_union_find.py.
"""

from typing import List
import heapq
from collections import defaultdict


class AdvancedGraphSolutions:

    # -----------------------------------------------------------------------
    # 1. Cheapest Flights Within K Stops (LC 787) — Bellman-Ford (bounded)
    #
    # Problem Description:
    # There are n cities connected by flights, flights[i] = [from, to, price].
    # Find the cheapest price from src to dst with at most k stops. Return -1
    # if no such route exists.
    #
    # Approach: Bellman-Ford relaxation, but capped at k+1 rounds (k stops =
    # k+1 edges). Standard Bellman-Ford relaxes V-1 times; capping the round
    # count is exactly what "at most k stops" needs — Dijkstra can't express
    # this constraint because it greedily commits to the lowest-cost node,
    # not the fewest edges.
    # Key Insight: must snapshot `dist` before each round, otherwise an edge
    # relaxed earlier in the same round would be reused, silently allowing
    # more than k stops.
    # Gotchas: use a *copy* of dist per round, not a fresh array (must carry
    # forward best-known distances from prior rounds).
    # Time: O(k * E), Space: O(n)
    # -----------------------------------------------------------------------
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        dist = [float('inf')] * n
        dist[src] = 0
        for _ in range(k + 1):
            new_dist = dist[:]
            for u, v, w in flights:
                if dist[u] != float('inf') and dist[u] + w < new_dist[v]:
                    new_dist[v] = dist[u] + w
            dist = new_dist
        return dist[dst] if dist[dst] != float('inf') else -1

    # -----------------------------------------------------------------------
    # 2. Detect Negative Cycle — classic Bellman-Ford
    #
    # Problem Description:
    # Given n nodes and weighted directed edges (u, v, w), detect whether the
    # graph contains a negative-weight cycle reachable from src.
    # Approach: relax all edges n-1 times (guarantees shortest paths if no
    # negative cycle exists, since a shortest simple path has at most n-1
    # edges). Run one extra relaxation pass — if any edge still relaxes,
    # a negative cycle exists.
    # Key Insight: this is the textbook algorithm Dijkstra cannot replace,
    # since Dijkstra assumes non-negative weights and greedily finalizes
    # distances.
    # Time: O(V*E), Space: O(V)
    # -----------------------------------------------------------------------
    def hasNegativeCycle(self, n: int, edges: List[List[int]], src: int) -> bool:
        dist = [float('inf')] * n
        dist[src] = 0
        for i in range(n - 1):
            updated = False
            for u, v, w in edges:
                if dist[u] != float('inf') and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break
        # One more pass: any further relaxation implies a negative cycle.
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                return True
        return False

    # -----------------------------------------------------------------------
    # 3. Find the City With the Smallest Number of Neighbors at a Threshold
    #    Distance (LC 1334) — Floyd-Warshall
    #
    # Problem Description:
    # n cities connected by weighted edges. For each city, count neighbors
    # reachable within distanceThreshold. Return the city with the fewest
    # such neighbors (largest index if tied).
    # Approach: Floyd-Warshall computes all-pairs shortest paths in
    # O(n^3) — the natural choice whenever every pair's shortest distance is
    # needed (n is small, typically <= 100..250) rather than running
    # Dijkstra from every node.
    # Key Insight: the triple loop order matters — k (intermediate node) must
    # be the outermost loop so dist[i][j] only ever uses paths already
    # confirmed optimal through nodes 0..k-1.
    # Gotchas: initialize dist[i][i] = 0 and all others to infinity before
    # filling in edges (graph may not be complete).
    # Time: O(n^3), Space: O(n^2)
    # -----------------------------------------------------------------------
    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        dist = [[float('inf')] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)

        for k in range(n):
            for i in range(n):
                if dist[i][k] == float('inf'):
                    continue
                for j in range(n):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]

        best_city, best_count = -1, float('inf')
        for i in range(n):
            count = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if count <= best_count:
                best_count = count
                best_city = i
        return best_city

    # -----------------------------------------------------------------------
    # 4. Min Cost to Connect All Points (LC 1584) — Prim's algorithm
    #
    # Problem Description:
    # Given points on a 2D plane, connect all points with the minimum total
    # Manhattan-distance edges (a spanning tree).
    # Approach: Prim's grows a single MST from an arbitrary root, greedily
    # adding the cheapest edge that connects a visited node to an unvisited
    # one — contrast with Kruskal (07_union_find.py minimumSpanningTree),
    # which sorts *all* edges globally and uses union-find to avoid cycles.
    # Prim's is preferable here because edges are implicit (dense graph,
    # O(n^2) pairs) — generating and sorting all of them for Kruskal costs
    # the same, but Prim's heap naturally handles dense graphs without
    # ever materializing the edge list up front.
    # Key Insight: push (cost, node) lazily; skip nodes already visited when
    # popped, rather than trying to decrease-key in the heap.
    # Time: O(n^2 log n), Space: O(n^2)
    # -----------------------------------------------------------------------
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        visited = [False] * n
        min_heap = [(0, 0)]  # (cost, node)
        total = 0
        edges_used = 0

        while edges_used < n:
            cost, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            total += cost
            edges_used += 1
            for v in range(n):
                if not visited[v]:
                    dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    heapq.heappush(min_heap, (dist, v))

        return total

    # -----------------------------------------------------------------------
    # 5. Prim's on an explicit adjacency list (generic form)
    #
    # Problem Description: given n nodes and weighted undirected edges
    # (u, v, w), return the total weight of a minimum spanning tree, or -1
    # if the graph is disconnected.
    # Key Insight: same greedy-frontier idea as above but for sparse graphs
    # expressed as adjacency lists rather than an implicit dense metric —
    # this is the form most often asked as "implement Prim's" directly.
    # Time: O(E log V), Space: O(V + E)
    # -----------------------------------------------------------------------
    def primMST(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((w, v))
            graph[v].append((w, u))

        visited = [False] * n
        min_heap = [(0, 0)]  # (weight, node)
        total = 0
        nodes_used = 0

        while min_heap and nodes_used < n:
            w, u = heapq.heappop(min_heap)
            if visited[u]:
                continue
            visited[u] = True
            total += w
            nodes_used += 1
            for weight, v in graph[u]:
                if not visited[v]:
                    heapq.heappush(min_heap, (weight, v))

        return total if nodes_used == n else -1


if __name__ == "__main__":
    sol = AdvancedGraphSolutions()

    # Bellman-Ford (bounded) — LC 787
    assert sol.findCheapestPrice(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1) == 700
    assert sol.findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 1) == 200

    # Negative cycle detection
    assert sol.hasNegativeCycle(3, [[0,1,1],[1,2,-3],[2,0,1]], 0) is True
    assert sol.hasNegativeCycle(3, [[0,1,1],[1,2,2]], 0) is False

    # Floyd-Warshall — LC 1334
    assert sol.findTheCity(4, [[0,1,3],[1,2,1],[1,3,4],[2,3,1]], 4) == 3

    # Prim's — LC 1584
    assert sol.minCostConnectPoints([[0,0],[2,2],[3,10],[5,2],[7,0]]) == 20

    # Generic Prim's
    assert sol.primMST(4, [[0,1,1],[1,2,2],[0,2,4],[2,3,3]]) == 6  # edges (0,1)+(1,2)+(2,3)=1+2+3
    assert sol.primMST(3, [[0,1,1]]) == -1  # disconnected

    print("All advanced graph tests passed.")
