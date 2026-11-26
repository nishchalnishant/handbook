from collections import deque

def is_bipartite(graph):
    """
    Function to check if a graph is bipartite using BFS.
    
    :param graph: Adjacency list representation of the graph
    :return: True if the graph is bipartite, False otherwise
    """
    n = len(graph)
    color = [-1] * n  # -1 indicates uncolored nodes

    for start in range(n):
        if color[start] == -1:  # If the node is not yet colored
            queue = deque([start])
            color[start] = 0  # Start coloring with 0

            while queue:
                node = queue.popleft()

                for neighbor in graph[node]:
                    if color[neighbor] == -1:  # If the neighbor is not colored
                        color[neighbor] = 1 - color[node]  # Assign alternate color
                        queue.append(neighbor)
                    elif color[neighbor] == color[node]:  # If the neighbor has the same color
                        return False

    return True

# Example usage
if __name__ == "__main__":
    graph = [
        [1, 3],
        [0, 2],
        [1, 3],
        [0, 2]
    ]
    print("Graph is Bipartite" if is_bipartite(graph) else "Graph is not Bipartite")