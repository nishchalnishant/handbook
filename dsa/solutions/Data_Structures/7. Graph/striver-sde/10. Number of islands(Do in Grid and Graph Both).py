from collections import defaultdict

# Number of Islands in a Grid (DFS Approach)
def numIslandsGrid(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] == '0' or visited[r][c]:
            return
        visited[r][c] = True
        # Explore all 4 directions
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    island_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and not visited[r][c]:
                dfs(r, c)
                island_count += 1

    return island_count


# Number of Islands in a Graph (Using Adjacency List)

def numIslandsGraph(edges, n):
    # Create adjacency list
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n

    def dfs(node):
        visited[node] = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                dfs(neighbor)

    island_count = 0
    for node in range(n):
        if not visited[node]:
            dfs(node)
            island_count += 1

    return island_count


# Example Usage
# Grid Example
grid = [
    ["1", "1", "0", "0", "0"],
    ["1", "1", "0", "0", "0"],
    ["0", "0", "1", "0", "0"],
    ["0", "0", "0", "1", "1"]
]
print("Number of islands in grid:", numIslandsGrid(grid))

# Graph Example
edges = [(0, 1), (1, 2), (3, 4)]  # Graph edges
n = 5  # Number of nodes
print("Number of islands in graph:", numIslandsGraph(edges, n))