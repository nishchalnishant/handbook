from collections import deque

def is_cycle_bfs(V, adj):
    visited = [False] * V

    def bfs(node):
        queue = deque([(node, -1)])  # (current_node, parent_node)
        visited[node] = True

        while queue:
            current, parent = queue.popleft()

            for neighbor in adj[current]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append((neighbor, current))
                elif neighbor != parent:
                    return True
        return False

    for i in range(V):
        if not visited[i]:
            if bfs(i):
                return True
    return False

# Example usage:
if __name__ == "__main__":
    V = 5
    adj = [
        [1, 2],  # Edges for vertex 0
        [0, 3],  # Edges for vertex 1
        [0, 3],  # Edges for vertex 2
        [1, 2, 4],  # Edges for vertex 3
        [3]       # Edges for vertex 4
    ]

    if is_cycle_bfs(V, adj):
        print("Cycle detected in the graph.")
    else:
        print("No cycle detected in the graph.")