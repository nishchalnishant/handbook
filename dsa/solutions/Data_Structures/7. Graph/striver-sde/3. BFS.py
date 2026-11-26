from collections import deque

def bfs(graph, start):
    """
    Perform Breadth-First Search (BFS) on a graph.

    :param graph: Dictionary representing the adjacency list of the graph.
    :param start: Starting node for BFS.
    :return: List of nodes in the order they are visited.
    """
    visited = set()  # To keep track of visited nodes
    queue = deque([start])  # Queue for BFS
    bfs_order = []  # List to store the BFS traversal order

    while queue:
        # Dequeue a node from the front of the queue
        node = queue.popleft()

        # If the node has not been visited
        if node not in visited:
            visited.add(node)  # Mark the node as visited
            bfs_order.append(node)  # Add it to the BFS order

            # Enqueue all unvisited neighbors
            for neighbor in graph[node]:
                if neighbor not in visited:
                    queue.append(neighbor)

    return bfs_order


# Example usage
if __name__ == "__main__":
    # Graph represented as an adjacency list
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1],
        5: [2]
    }

    start_node = 0
    print("BFS Traversal:", bfs(graph, start_node))