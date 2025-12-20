def shortest_path_all_nodes(graph):
    """
    Problem: Shortest path visiting all nodes in an undirected graph. Can revisit nodes/edges.
    
    Approach: BFS + Bitmask State
    - State: (u, mask) where u is current node, mask is set of visited nodes.
    - BFS guarantees shortest path because edge weights are 1.
    - Start BFS from ALL nodes simultaneously with initial mask (1<<i).
    - Visited set stores (u, mask) to avoid cycles/redundant states.
    
    Time Complexity: O(2^N * N^2)
    Space Complexity: O(2^N * N)
    """
    import collections
    n = len(graph)
    queue = collections.deque()
    visited = set()
    
    for i in range(n):
        mask = 1 << i
        queue.append((i, mask, 0)) # node, mask, dist
        visited.add((i, mask))
        
    full_mask = (1 << n) - 1
    
    while queue:
        u, mask, dist = queue.popleft()
        
        if mask == full_mask:
            return dist
            
        for v in graph[u]:
            new_mask = mask | (1 << v)
            if (v, new_mask) not in visited:
                visited.add((v, new_mask))
                queue.append((v, new_mask, dist + 1))
                
    return 0

# Example Usage
if __name__ == "__main__":
    graph = [[1,2,3],[0],[0],[0]]
    print(f"Shortest path length: {shortest_path_all_nodes(graph)}")
