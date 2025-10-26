from collections import defaultdict, deque

def detect_cycle_in_directed_graph_bfs(V, edges):
    # Create adjacency list
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)
    
    # Calculate in-degrees
    in_degree = [0] * V
    for u in range(V):
        for v in adj[u]:
            in_degree[v] += 1
    
    # Initialize queue with nodes having in-degree 0
    queue = deque([i for i in range(V) if in_degree[i] == 0])
    count = 0  # To count visited nodes
    
    while queue:
        node = queue.popleft()
        count += 1
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # If count of visited nodes is not equal to total nodes, there is a cycle
    return count != V

# Example usage
if __name__ == "__main__":
    V = 4
    edges = [(0, 1), (1, 2), (2, 3), (3, 1)]  # Example graph with a cycle
    if detect_cycle_in_directed_graph_bfs(V, edges):
        print("Cycle detected in the graph.")
    else:
        print("No cycle detected in the graph.")