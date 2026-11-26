from collections import defaultdict, deque

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def dfs(self, v, visited):
        visited[v] = True
        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited)

    def get_transpose(self):
        transpose = Graph(self.V)
        for u in self.graph:
            for v in self.graph[u]:
                transpose.add_edge(v, u)
        return transpose

    def is_strongly_connected(self):
        visited = [False] * self.V

        # Step 1: Perform DFS from the first vertex
        self.dfs(0, visited)
        if not all(visited):
            return False

        # Step 2: Get the transpose of the graph
        transpose = self.get_transpose()

        # Step 3: Perform DFS on the transpose graph
        visited = [False] * self.V
        transpose.dfs(0, visited)
        if not all(visited):
            return False

        return True


# Example usage
if __name__ == "__main__":
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 0)
    g.add_edge(2, 4)
    g.add_edge(4, 2)

    if g.is_strongly_connected():
        print("The graph is strongly connected.")
    else:
        print("The graph is not strongly connected.")