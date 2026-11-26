def shortest_path_dag(n, edges, start):
    """
    Problem: Find shortest path from start node to all other nodes in a DAG (Weighted).
    
    Approach: DP on Graphs / Topological Sort
    - Since it's a DAG, we can process nodes in topological order.
    - Relax edges: dist[v] = min(dist[v], dist[u] + weight).
    - Or Memoized DFS: dp[u] = min(weight + dp[v]).
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        
    # Topological Sort approach is standard for iterative DP
    visited = [False] * n
    stack = []
    
    def topo_sort(u):
        visited[u] = True
        for v, _ in adj[u]:
            if not visited[v]:
                topo_sort(v)
        stack.append(u)
        
    for i in range(n):
        if not visited[i]:
            topo_sort(i)
            
    # Process in topo order
    dist = [float('inf')] * n
    dist[start] = 0
    
    while stack:
        u = stack.pop()
        if dist[u] != float('inf'):
            for v, w in adj[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    
    return dist

# Example Usage
if __name__ == "__main__":
    n = 6
    # u, v, w
    edges = [[0,1,2], [0,4,1], [4,5,4], [4,2,2], [1,2,3], [2,3,6], [5,3,1]]
    start = 0
    dists = shortest_path_dag(n, edges, start)
    print(f"Shortest paths from {start}: {dists}")
