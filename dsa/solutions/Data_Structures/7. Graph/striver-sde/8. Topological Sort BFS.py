from collections import defaultdict, deque

def topological_sort_bfs(vertices, edges):
    """
    Perform topological sort on a directed acyclic graph (DAG) using BFS (Kahn's Algorithm).

    :param vertices: Number of vertices in the graph
    :param edges: List of edges in the graph (directed)
    :return: List representing the topological order of the graph
    """
    # Step 1: Create an adjacency list and calculate in-degrees of all vertices
    adj_list = defaultdict(list)
    in_degree = [0] * vertices

    for u, v in edges:
        adj_list[u].append(v)
        in_degree[v] += 1

    # Step 2: Initialize a queue with all vertices having in-degree 0
    queue = deque([i for i in range(vertices) if in_degree[i] == 0])

    # Step 3: Perform BFS and generate the topological order
    topo_order = []
    while queue:
        node = queue.popleft()
        topo_order.append(node)

        # Reduce the in-degree of neighbors and add them to the queue if in-degree becomes 0
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # If the topological order contains all vertices, return it
    if len(topo_order) == vertices:
        return topo_order
    else:
        # Graph has a cycle, topological sort is not possible
        return []

# Example usage
if __name__ == "__main__":
    vertices = 6
    edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    result = topological_sort_bfs(vertices, edges)
    if result:
        print("Topological Sort:", result)
    else:
        print("The graph has a cycle, topological sort is not possible.")