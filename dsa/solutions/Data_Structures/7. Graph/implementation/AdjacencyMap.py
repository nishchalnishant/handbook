class Graph:
    def __init__(self, directed=False):
        self.graph = {}  # Adjacency map to store vertices and their neighbors
        self.directed = directed

    def add_vertex(self, vertex):
        """Add a new vertex to the graph."""
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def add_edge(self, u, v, weight=1):
        """Add an edge from vertex u to vertex v with an optional weight."""
        # Ensure both vertices exist in the graph
        if u not in self.graph:
            self.add_vertex(u)
        if v not in self.graph:
            self.add_vertex(v)

        # Add the edge from u to v
        self.graph[u][v] = weight

        # If undirected, add the reverse edge from v to u
        if not self.directed:
            self.graph[v][u] = weight

    def remove_edge(self, u, v):
        """Remove an edge between vertices u and v."""
        if u in self.graph and v in self.graph[u]:
            del self.graph[u][v]
        if not self.directed and v in self.graph and u in self.graph[v]:
            del self.graph[v][u]

    def remove_vertex(self, vertex):
        """Remove a vertex and all associated edges."""
        if vertex in self.graph:
            # Remove all edges from other vertices to this vertex
            for neighbor in list(self.graph[vertex]):
                self.remove_edge(vertex, neighbor)
            # Remove the vertex from the graph
            del self.graph[vertex]

        # Remove edges pointing to this vertex from all other vertices
        for v in self.graph:
            if vertex in self.graph[v]:
                del self.graph[v][vertex]

    def get_neighbors(self, vertex):
        """Return a dictionary of neighbors and weights for a given vertex."""
        return self.graph.get(vertex, {})

    def display(self):
        """Print the adjacency map representation of the graph."""
        for vertex, neighbors in self.graph.items():
            print(f"{vertex} -> {neighbors}")

# Usage Example
g = Graph(directed=False)
g.add_vertex("A")
g.add_vertex("B")
g.add_edge("A", "B", weight=5)
g.add_edge("A", "C", weight=3)
g.add_edge("B", "C", weight=2)

print("Graph adjacency map:")
g.display()

# Display neighbors of a specific vertex
print("\nNeighbors of A:", g.get_neighbors("A"))

# Remove an edge and display the graph
g.remove_edge("A", "B")
print("\nGraph after removing edge A-B:")
g.display()

# Remove a vertex and display the graph
g.remove_vertex("C")
print("\nGraph after removing vertex C:")
g.display()