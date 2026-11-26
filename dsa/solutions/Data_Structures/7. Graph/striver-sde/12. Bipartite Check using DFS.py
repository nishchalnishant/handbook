def is_bipartite_dfs(node, graph, color):
    for neighbor in graph[node]:
        if color[neighbor] == -1:  # If the neighbor is not colored
            color[neighbor] = 1 - color[node]  # Assign the opposite color
            if not is_bipartite_dfs(neighbor, graph, color):
                return False
        elif color[neighbor] == color[node]:  # If the neighbor has the same color
            return False
    return True

def check_bipartite(graph):
    n = len(graph)
    color = [-1] * n  # -1 indicates uncolored nodes

    for i in range(n):
        if color[i] == -1:  # If the node is not yet visited
            color[i] = 0  # Start coloring with 0
            if not is_bipartite_dfs(i, graph, color):
                return False
    return True

# Example usage
if __name__ == "__main__":
    graph = {
        0: [1, 3],
        1: [0, 2],
        2: [1, 3],
        3: [0, 2]
    }
    print("Graph is Bipartite" if check_bipartite(graph) else "Graph is not Bipartite")