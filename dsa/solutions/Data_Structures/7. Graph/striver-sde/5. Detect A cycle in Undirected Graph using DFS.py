from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def is_cycle_util(self, v, visited, parent):
        visited[v] = True

        for neighbor in self.graph[v]:
            if not visited[neighbor]:
                if self.is_cycle_util(neighbor, visited, v):
                    return True
            elif parent != neighbor:
                return True

        return False

    def is_cycle(self):
        visited = [False] * self.V

        for i in range(self.V):
            if not visited[i]:
                if self.is_cycle_util(i, visited, -1):
                    return True

        return False

# Example usage
if __name__ == "__main__":
    g = Graph(5)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 1)

    if g.is_cycle():
        print("Graph contains cycle")
    else:
        print("Graph does not contain cycle")