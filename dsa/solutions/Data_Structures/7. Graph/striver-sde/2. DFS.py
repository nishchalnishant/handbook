# Depth First Search (DFS) implementation in Python

# Depth First Search is a graph traversal algorithm that starts at a source node
# and explores as far as possible along each branch before backtracking.

# Function to perform DFS
def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()  # To keep track of visited nodes

    # Mark the current node as visited
    visited.add(start)
    print(start, end=" ")  # Print the node (or process it as needed)

    # Recur for all the vertices adjacent to this vertex
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Example usage
if __name__ == "__main__":
    # Representing the graph as an adjacency list
    graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }

    print("Depth First Search starting from node 'A':")
    dfs(graph, 'A')