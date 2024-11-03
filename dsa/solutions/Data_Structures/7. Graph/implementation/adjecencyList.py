from collections import defaultdict, deque

class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed

    def add_vertex(self, vertex):
        """Add a vertex to the graph."""
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        """Add an edge between two vertices."""
        self.graph[vertex1].append(vertex2)
        if not self.directed:
            self.graph[vertex2].append(vertex1)

    def bfs(self, start_vertex):
        """Perform Breadth-First Search (BFS) from a start vertex."""
        visited = set()
        queue = deque([start_vertex])
        visited.add(start_vertex)
        bfs_order = []
        
        while queue:
            vertex = queue.popleft()
            bfs_order.append(vertex)
            
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)
        
        return bfs_order

    def dfs(self, start_vertex):
        """Perform Depth-First Search (DFS) from a start vertex."""
        visited = set()
        dfs_order = []
        self._dfs_recursive(start_vertex, visited, dfs_order)
        return dfs_order

    def _dfs_recursive(self, vertex, visited, dfs_order):
        """Helper function for DFS traversal using recursion."""
        visited.add(vertex)
        dfs_order.append(vertex)
        
        for neighbor in self.graph[vertex]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, dfs_order)

    def display(self):
        """Display the adjacency list of the graph."""
        for vertex in self.graph:
            print(f"{vertex} -> {self.graph[vertex]}")

# Usage Example
g = Graph(directed=False)
g.add_vertex(1)
g.add_vertex(2)
g.add_vertex(3)
g.add_vertex(4)
g.add_edge(1, 2)
g.add_edge(1, 3)
g.add_edge(2, 4)
g.add_edge(3, 4)

print("Graph adjacency list:")
g.display()

# Perform BFS and DFS
print("\nBFS from vertex 1:", g.bfs(1))  # Output may vary depending on structure
print("DFS from vertex 1:", g.dfs(1))  # Output may vary depending on structure