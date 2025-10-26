def detect_cycle_dfs(node, adj, visited, dfs_visited):
    visited[node] = True
    dfs_visited[node] = True

    for neighbor in adj[node]:
        if not visited[neighbor]:
            if detect_cycle_dfs(neighbor, adj, visited, dfs_visited):
                return True
        elif dfs_visited[neighbor]:
            return True

    dfs_visited[node] = False
    return False

def is_cyclic(n, edges):
    # Create adjacency list
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    visited = [False] * n
    dfs_visited = [False] * n

    for i in range(n):
        if not visited[i]:
            if detect_cycle_dfs(i, adj, visited, dfs_visited):
                return True

    return False

# Example usage
if __name__ == "__main__":
    n = 4
    edges = [(0, 1), (1, 2), (2, 3), (3, 1)]  # Example graph with a cycle
    if is_cyclic(n, edges):
        print("Cycle detected in the graph.")
    else:
        print("No cycle detected in the graph.")