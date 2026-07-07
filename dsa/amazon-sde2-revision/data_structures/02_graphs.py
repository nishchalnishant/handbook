"""
Graphs patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Infinite loops! Always use a `visited` set to track seen nodes.\n- Disconnected components: assuming the graph is fully connected (may need an outer loop over all nodes).\n- Confusing graph representations (Adjacency List vs Adjacency Matrix vs Edge List).

Common Variants:
- BFS/DFS on Adjacency List\n- Matrix / Grid traversals (Number of Islands)\n- Topological Sort (Course Schedule)\n- Shortest Path (Dijkstra)

General Tips & Best Practices:
- Adjacency list `adj = collections.defaultdict(list)` is the most versatile representation.\n- For grids, use a directions array: `dirs = [(0,1), (1,0), (0,-1), (-1,0)]`.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
from collections import deque, defaultdict

class GraphNode:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class GraphSolutions:
    # -----------------------------------------------------------------------
    # 1. Number of Islands (LC 200) — T1
    # Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
    # Example: grid = [ → 1
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 300, grid[i][j] is '0' or '1'
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def numIslands(self, grid: List[List[str]]) -> int:
        # Guard check: empty grid check
        if not grid: 
            return 0
        # Initialize grid dimensions
        rows, cols = len(grid), len(grid[0])
        # Island counter
        count = 0

        def dfs(r, c):
            """Depth-first-search helper for the enclosing solution."""
            # Base cases: boundary check and water check
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
                return
            # Sink current land cell in-place to avoid revisited checks
            grid[r][c] = '0'
            # Recursively explore all four cardinal neighbors
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)

        # Loop through every cell in the grid
        for r in range(rows):
            for c in range(cols):
                # When land is encountered, trigger sink DFS
                if grid[r][c] == '1':
                    count += 1
                    dfs(r, c)
        return count

    # -----------------------------------------------------------------------
    # 2. Max Area of Island (LC 695) — T1
    # You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water. The area of an island is the number of cells with a value 1 in the island. Return the maximum area of an island in grid. If there is no island, return 0.
    # Example: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[ → 6
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 50, grid[i][j] is either 0 or 1
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        # Initialize grid dimensions
        rows, cols = len(grid), len(grid[0])
        # Maximum area tracked across all islands
        max_area = 0

        def dfs(r, c):
            """Depth-first-search helper for the enclosing solution."""
            # Out of bounds or water cell checks
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 0:
                return 0
            # Zero out visited land cell to prevent infinite loop
            grid[r][c] = 0
            # Accumulate current cell and areas of all neighbors
            return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)

        # Search every cell in grid
        for r in range(rows):
            for c in range(cols):
                # Trigger DFS for land cells to compute area
                if grid[r][c] == 1:
                    max_area = max(max_area, dfs(r, c))
        return max_area

    # -----------------------------------------------------------------------
    # 3. Clone Graph (LC 133) — T1
    # Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph. Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors. class Node { public int val; public List<Node> neighbors; } Test case format: For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list. An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph. The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.
    # Example: adjList = [[2,4],[1,3],[2,4],[1,3]] → [[2,4],[1,3],[2,4],[1,3]]
    # Constraints: The number of nodes in the graph is in the range [0, 100], 1 <= Node.val <= 100, Node.val is unique for each node, There are no repeated edges and no self-loops in the graph, The Graph is connected and all nodes can be visited starting from the given node
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def cloneGraph(self, node: 'GraphNode') -> 'GraphNode':
        """Clone Graph (LC 133): Use a hash map (oldToNew) that maps each original node to its clone."""
        # Guard: return empty/None node if graph is empty
        if not node: return node
        # Mapping from original node to cloned node
        oldToNew = {}

        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: return cloned node if already cloned
            if node in oldToNew:
                return oldToNew[node]
            # Instantiate new node copy
            copy = GraphNode(node.val)
            # Map original node to its copy immediately to avoid cyclic loops
            oldToNew[node] = copy
            # Recursively clone all neighbor nodes
            for neighbor in node.neighbors:
                copy.neighbors.append(dfs(neighbor))
            return copy
        # Start graph traversal from entry node
        return dfs(node)

    # -----------------------------------------------------------------------
    # 4. Course Schedule (LC 207) — T1
    # There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses. Otherwise, return false.
    # Example: numCourses = 2, prerequisites = [[1,0]] → true
    # Constraints: 1 <= numCourses <= 2000, 0 <= prerequisites.length <= 5000, prerequisites[i].length == 2, 0 <= ai, bi < numCourses, All the pairs prerequisites[i] are unique
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Map course to its direct prerequisites
        preMap = {i: [] for i in range(numCourses)}
        for crs, pre in prerequisites:
            preMap[crs].append(pre)

        # Track active traversal path to detect cycles
        visitSet = set()
        def dfs(crs):
            """Depth-first-search helper for the enclosing solution."""
            # Cycle detected on the active path
            if crs in visitSet: return False
            # Course has no remaining prerequisites / already validated
            if preMap[crs] == []: return True

            # Mark course on active path
            visitSet.add(crs)
            # Recursively validate all prerequisites
            for pre in preMap[crs]:
                if not dfs(pre): return False
            # Backtrack active path marker
            visitSet.remove(crs)
            # Clear prereqs list to memoize course as fully safe
            preMap[crs] = []
            return True

        # Run DFS check for all courses to support disconnected graphs
        for crs in range(numCourses):
            if not dfs(crs): return False
        return True

    # -----------------------------------------------------------------------
    # 5. Course Schedule II (LC 210) — T1
    # There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
    # Example: numCourses = 2, prerequisites = [[1,0]] → [0,1]
    # Constraints: 1 <= numCourses <= 2000, 0 <= prerequisites.length <= numCourses * (numCourses - 1), prerequisites[i].length == 2, 0 <= ai, bi < numCourses, ai != bi, All the pairs [ai, bi] are distinct
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        # Map course to its list of prerequisites
        preMap = {i: [] for i in range(numCourses)}
        for crs, pre in prerequisites:
            preMap[crs].append(pre)

        # visit: globally safe nodes, cycle: active traversal path
        visit, cycle = set(), set()
        # Holds the post-order topological sort
        output = []

        def dfs(crs):
            """Depth-first-search helper for the enclosing solution."""
            # Cycle detected on path
            if crs in cycle: return False
            # Node already processed, no need to re-verify
            if crs in visit: return True

            # Add course to active cycle set
            cycle.add(crs)
            # Check prerequisites recursively
            for pre in preMap[crs]:
                if not dfs(pre): return False
            # Backtrack from active path
            cycle.remove(crs)
            # Add to globally completed course set
            visit.add(crs)
            # Append to output topological order
            output.append(crs)
            return True

        # Process all courses
        for c in range(numCourses):
            if not dfs(c): return []
        return output

    # -----------------------------------------------------------------------
    # 6. Alien Dictionary (LC 269) — T1
    # There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you. You are given a list of strings words from the alien language's dictionary, where the strings in words are sorted lexicographically by the rules of this new language. Return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules. If there is no solution, return "". If there are multiple solutions, return any of them.
    # Example: words = ["wrt","wrf","er","ett","rftt"] → "wertf"
    # Constraints: 1 <= words.length <= 100, 1 <= words[i].length <= 100
    # Time: O(C), Space: O(U) where C = total characters in all words, U = unique characters
    # -----------------------------------------------------------------------
    def alienOrder(self, words: List[str]) -> str:
        # Initialize empty adjacency lists for every unique character
        adj = {c: set() for w in words for c in w}

        # Compare consecutive words to find character ordering constraints
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            minLen = min(len(w1), len(w2))
            # Invalid order: shorter prefix word comes after longer word
            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
                return ""
            # Find the first mismatch to establish directed edge
            for j in range(minLen):
                if w1[j] != w2[j]:
                    adj[w1[j]].add(w2[j])
                    break

        # State tracking: True (in active path), False (safely visited)
        visit = {}
        # Stores reverse topological order
        res = []

        def dfs(c):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: return state of node if already visited
            if c in visit: return visit[c]
            # Mark node as in active path
            visit[c] = True
            # Recurse through neighbors
            for nei in adj[c]:
                if dfs(nei): return True
            # Mark node as safe and backtrack active path
            visit[c] = False
            res.append(c)
            return False

        # Run topological sort on all character nodes
        for c in adj:
            if dfs(c): return ""
        # Reverse to get the correct lexicographical order
        res.reverse()
        return "".join(res)

class GraphSolutionsT2:
    # -----------------------------------------------------------------------
    # 7. Flood Fill (LC 733) — T1
    # An image is represented by an m x n integer grid image where image[i][j] represents the pixel value of the image. You are also given three integers sr, sc, and color. You should perform a flood fill on the image starting from the pixel image[sr][sc].
    # Example: image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2 → [[2,2,2],[2,2,0],[2,0,1]]
    # Constraints: m == image.length, n == image[i].length, 1 <= m, n <= 50
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        # Capture the original color of the starting pixel
        oldColor = image[sr][sc]
        # Guard: return early if target color is same as old color
        if oldColor == color: return image
        # Initialize image dimensions
        rows, cols = len(image), len(image[0])

        def dfs(r, c):
            """Depth-first-search helper for the enclosing solution."""
            # Boundary checks and matching color check
            if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != oldColor:
                return
            # Recolor current cell
            image[r][c] = color
            # Recurse on all adjacent neighbors
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)

        # Trigger flood fill
        dfs(sr, sc)
        return image

    # -----------------------------------------------------------------------
    # 8. Pacific Atlantic Water Flow (LC 417) — T1
    # There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges. Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.
    # Example: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]] → [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    # Constraints: m == heights.length, n == heights[r].length, 1 <= m, n <= 200
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        # Initialize grid dimensions
        ROWS, COLS = len(heights), len(heights[0])
        # Track cells reachable from Pacific and Atlantic oceans
        pac, atl = set(), set()

        def dfs(r, c, visit, prevHeight):
            """Depth-first-search helper for the enclosing solution."""
            # Base check: already visited, out-of-bounds, or cannot flow uphill
            if ((r, c) in visit or r < 0 or c < 0 or r == ROWS or c == COLS or heights[r][c] < prevHeight):
                return
            # Add to reachable set
            visit.add((r, c))
            # Flood uphill in all four directions
            dfs(r + 1, c, visit, heights[r][c])
            dfs(r - 1, c, visit, heights[r][c])
            dfs(r, c + 1, visit, heights[r][c])
            dfs(r, c - 1, visit, heights[r][c])

        # Seed DFS from top (Pacific) and bottom (Atlantic) edges
        for c in range(COLS):
            dfs(0, c, pac, heights[0][c])
            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])

        # Seed DFS from left (Pacific) and right (Atlantic) edges
        for r in range(ROWS):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, COLS - 1, atl, heights[r][COLS - 1])

        # Find cells that are present in both ocean reachable sets
        res = []
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) in pac and (r, c) in atl:
                    res.append([r, c])
        return res

    # -----------------------------------------------------------------------
    # 9. Surrounded Regions (LC 130) — T1
    # Given an m x n matrix board containing 'X' and 'O', capture all regions that are 4-directionally surrounded by 'X'. A region is captured by flipping all 'O's into 'X's in that surrounded region.
    # Example: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]] → [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
    # Constraints: m == board.length, n == board[i].length, 1 <= m, n <= 200
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def solve(self, board: List[List[str]]) -> None:
        """Surrounded Regions (LC 130): Any 'O' connected to the border cannot be captured."""
        # Guard check: empty board check
        if not board: return
        # Initialize board dimensions
        ROWS, COLS = len(board), len(board[0])

        def dfs(r, c):
            """Depth-first-search helper for the enclosing solution."""
            # Out of bounds or not an 'O' cell check
            if r < 0 or r == ROWS or c < 0 or c == COLS or board[r][c] != "O":
                return
            # Mark cell temporarily as safe (sentinel 'S')
            board[r][c] = "S"
            # Traverse neighboring cells
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

        # DFS from all border 'O's to mark them as safe
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O" and (r in [0, ROWS - 1] or c in [0, COLS - 1]):
                    dfs(r, c)

        # Capture surrounded 'O's and restore safe 'S' cells back to 'O'
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O":
                    board[r][c] = "X"
                elif board[r][c] == "S":
                    board[r][c] = "O"

    # -----------------------------------------------------------------------
    # 10. Is Graph Bipartite? (LC 785) — T1
    # There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to. Return true if and only if it is bipartite.
    # Example: graph = [[1,2,3],[0,2],[0,1,3],[0,2]] → false
    # Constraints: graph.length == n, 1 <= n <= 100
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def isBipartite(self, graph: List[List[int]]) -> bool:
        # Map node to color (0 or 1)
        colors = {}
        # Iterate over all nodes to support disconnected components
        for i in range(len(graph)):
            if i not in colors:
                # Color the seed node 0
                colors[i] = 0
                # Initialize BFS queue
                q = deque([i])
                while q:
                    node = q.popleft()
                    # Process neighbors
                    for nei in graph[node]:
                        # Assign alternate color if unvisited
                        if nei not in colors:
                            colors[nei] = 1 - colors[node]
                            q.append(nei)
                        # Conflict found: adjacent nodes have matching color
                        elif colors[nei] == colors[node]:
                            return False
        return True

    # -----------------------------------------------------------------------
    # 11. Find Eventual Safe States (LC 802) — T1
    # There is a directed graph of n nodes with each node labeled from 0 to n - 1. A node is a terminal node if there are no outgoing edges. A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node). Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.
    # Example: graph = [[1,2],[2,3],[5],[0],[5],[],[]] → [2,4,5,6]
    # Constraints: n == graph.length, 1 <= n <= 10^4
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def eventualSafeNodes(self, graph: List[List[int]]) -> List[int]:
        n = len(graph)
        color = [0] * n # 0: unvisited, 1: safe, 2: unsafe

        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Check if node is already visited or processed
            if color[node] != 0:
                return color[node] == 1

            # Mark node as visiting (unsafe/cycle path)
            color[node] = 2
            # Recursively check neighbors
            for nei in graph[node]:
                if not dfs(nei):
                    return False

            # Upgrade node to safe once all neighbors are verified safe
            color[node] = 1
            return True

        res = []
        # Check all nodes
        for i in range(n):
            if dfs(i): res.append(i)
        return res

    # -----------------------------------------------------------------------
    # 12. Redundant Connection (LC 684) — T1
    # In this problem, a tree is an undirected graph that is connected and has no cycles. You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. Return an edge that can be removed so that the resulting graph is a tree of n nodes.
    # Example: edges = [[1,2],[1,3],[2,3]] → [2,3]
    # Constraints: n == edges.length, 3 <= n <= 1000
    # Time: O(n * alpha(n)), Space: O(n)
    # -----------------------------------------------------------------------
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # Initial parents array: each node is its own parent
        par = [i for i in range(len(edges) + 1)]
        # Track ranks to keep the Union-Find tree flat
        rank = [1] * (len(edges) + 1)

        def find(n):
            """Finds the representative/root value used by the enclosing data structure."""
            p = par[n]
            # Find the root representative
            while p != par[p]:
                # Path compression (pointing parent to grandparent)
                par[p] = par[par[p]]
                p = par[p]
            return p

        def union(n1, n2):
            """Merges two components when they are not already connected."""
            p1, p2 = find(n1), find(n2)
            # Both nodes already belong to the same component
            if p1 == p2:
                return False
            # Merge smaller rank component under the larger rank
            if rank[p1] > rank[p2]:
                par[p2] = p1
                rank[p1] += rank[p2]
            else:
                par[p1] = p2
                rank[p2] += rank[p1]
            return True

        # Process each edge to check if it creates a cycle
        for n1, n2 in edges:
            # If union fails, we found the redundant edge
            if not union(n1, n2):
                return [n1, n2]

    # -----------------------------------------------------------------------
    # 13. All Paths from Source to Target (LC 797) — T1
    # Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order.
    # Example: graph = [[1,2],[3],[3],[]] → [[0,1,3],[0,2,3]]
    # Constraints: n == graph.length, 2 <= n <= 15
    # Time: O(2^V * V), Space: O(V)
    # -----------------------------------------------------------------------
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        # Holds all valid source-to-target paths
        res = []
        def dfs(node, path):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: reached target node
            if node == len(graph) - 1:
                # Store a snapshot copy of the current path
                res.append(path[:])
                return
            # Recurse on all neighbor nodes
            for nei in graph[node]:
                # Choose: append neighbor
                path.append(nei)
                # Recurse DFS
                dfs(nei, path)
                # Backtrack: pop neighbor
                path.pop()

        # Start search from node 0
        dfs(0, [0])
        return res

    # -----------------------------------------------------------------------
    # 14. Minimum Vertices to Reach All Nodes (LC 1557) — T1
    # Given a directed acyclic graph, with n vertices numbered from 0 to n-1, and an array edges where edges[i] = [fromi, toi] represents a directed edge from node fromi to node toi. Find the smallest set of vertices from which all nodes in the graph are reachable.
    # Example: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]] → [0,3]
    # Constraints: 2 <= n <= 10^5, 1 <= edges.length <= min(10^5, n * (n - 1) / 2)
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def findSmallestSetOfVertices(self, n: int, edges: List[List[int]]) -> List[int]:
        # Array to store incoming edges count for each node
        indegree = [0] * n
        # Increment in-degree for the destination node
        for u, v in edges:
            indegree[v] += 1
        # Nodes with in-degree 0 are unreachable by any other node
        return [i for i in range(n) if indegree[i] == 0]

    # -----------------------------------------------------------------------
    # 15. Number of Connected Components (LC 323) — T2
    # You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] indicates that there is an edge between ai and bi in the graph. Return the number of connected components in the graph.
    # Example: n = 5, edges = [[0,1],[1,2],[3,4]] → 2
    # Constraints: 1 <= n <= 2000, 1 <= edges.length <= 5000
    # Time: O(n * alpha(n)), Space: O(n)
    # -----------------------------------------------------------------------
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        # Track parent representative for disjoint sets
        par = [i for i in range(n)]
        # Track heights for union by rank
        rank = [1] * n

        def find(n1):
            """Finds the representative/root value used by the enclosing data structure."""
            res = n1
            # Loop until reaching root representative
            while res != par[res]:
                # Amortize: path compression step
                par[res] = par[par[res]]
                res = par[res]
            return res

        def union(n1, n2):
            """Merges two components when they are not already connected."""
            p1, p2 = find(n1), find(n2)
            # Already connected
            if p1 == p2:
                return 0
            # Merge smaller component under larger
            if rank[p2] > rank[p1]:
                par[p1] = p2
                rank[p2] += rank[p1]
            else:
                par[p2] = p1
                rank[p1] += rank[p2]
            return 1

        # Start with n disjoint components
        res = n
        # Process each edge to merge components
        for n1, n2 in edges:
            res -= union(n1, n2)
        return res

    # -----------------------------------------------------------------------
    # 16. Graph Valid Tree (LC 261) — T2
    # You have a graph of n nodes labeled from 0 to n - 1. You are given an integer n and a list of edges where edges[i] = [ai, bi] indicates that there is an undirected edge between nodes ai and bi in the graph. Return true if the edges of the given graph make up a valid tree, and false otherwise.
    # Example: n = 5, edges = [[0,1],[0,2],[0,3],[1,4]] → true
    # Constraints: 1 <= n <= 2000, 0 <= edges.length <= 5000
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        # Empty tree is valid
        if not n: return True
        # Build adjacency representation
        adj = {i: [] for i in range(n)}
        for n1, n2 in edges:
            adj[n1].append(n2)
            adj[n2].append(n1)

        # Track visited nodes to verify connectivity and cycle detection
        visit = set()
        def dfs(i, prev):
            """Depth-first-search helper for the enclosing solution."""
            # Back-edge detected: cycle exists
            if i in visit: return False
            visit.add(i)
            # Explore neighbors
            for j in adj[i]:
                # Skip edge going back to direct parent
                if j == prev: continue
                # Recurse and return False if cycle detected
                if not dfs(j, i): return False
            return True

        # Check for cycles starting from node 0 and verify all nodes are visited
        return dfs(0, -1) and n == len(visit)

    # -----------------------------------------------------------------------
    # 17. Minimum Spanning Tree — Kruskal's (LC 1584) — T1
    # Find the Minimum Spanning Tree (MST) of a weighted undirected graph using Kruskal's algorithm. Given n nodes and a list of edges with weights, return the sum of weights of the edges in the MST.
    # Example: n = 4, edges = [[0,1,1],[1,2,2],[2,3,3],[0,3,4]] → 6
    # Constraints: 1 <= n <= 10^4
    # Time: O(E log E), Space: O(V)
    # -----------------------------------------------------------------------
    def minimumSpanningTree(self, n: int, edges: List[List[int]]) -> int:
        # Initialize union find parents
        par = list(range(n))
        # Keep track of component sizes
        rank = [0] * n

        def find(x):
            """Finds the representative/root value used by the enclosing data structure."""
            # Traverse up to the root parent
            while par[x] != x:
                # Path compression
                par[x] = par[par[x]]
                x = par[x]
            return x

        def union(x, y):
            """Merges two components when they are not already connected."""
            px, py = find(x), find(y)
            # Vertices are already connected
            if px == py: return False
            # Swap to attach smaller rank tree to larger
            if rank[px] < rank[py]: px, py = py, px
            par[py] = px
            # Upgrade rank if trees have same depth
            if rank[px] == rank[py]: rank[px] += 1
            return True

        # Sort edges in ascending order of weights
        edges.sort(key=lambda e: e[2])
        # Accumulate weight and count of edges in MST
        total, count = 0, 0
        # Iterate and greedily add edges
        for u, v, w in edges:
            if union(u, v):
                total += w
                count += 1
                # MST contains exactly n-1 edges
                if count == n - 1: break
        return total if count == n - 1 else -1

    # -----------------------------------------------------------------------
    # 18. Network Delay Time — Dijkstra (LC 743) — T2
    # You are given a network of n nodes, labeled from 1 to n. You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target. We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. If it is impossible for all the n nodes to receive the signal, return -1.
    # Example: times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2 → 2
    # Constraints: 1 <= k <= n <= 100
    # Time: O((V+E) log V), Space: O(V+E)
    # -----------------------------------------------------------------------
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        import heapq
        # Build adjacency graph representing (neighbor, weight)
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))
        # Shortest distance tracking dictionary
        dist = {k: 0}
        # Min-heap initialized with (distance, node)
        minH = [(0, k)]
        while minH:
            # Get node with the minimum current distance
            d, node = heapq.heappop(minH)
            # Skip processing if we found a shorter path in the meantime
            if d > dist.get(node, float("inf")): continue
            # Check adjacent neighbor nodes
            for nei, w in graph[node]:
                nd = d + w
                # Relax edge: update distance if new path is shorter
                if nd < dist.get(nei, float("inf")):
                    dist[nei] = nd
                    heapq.heappush(minH, (nd, nei))
        # Return max time to reach all nodes, or -1 if unreachable
        return max(dist.values()) if len(dist) == n else -1

    # -----------------------------------------------------------------------
    # 19. Swim in Rising Water — Dijkstra min-of-max (LC 778) — T2
    # You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j). The rain starts to fall. At time t, the depth of the water everywhere is t. You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. Return the least time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).
    # Example: grid = [[0,2],[1,3]] → 3
    # Constraints: n == grid.length, n == grid[i].length
    # Time: O(n^2 log n), Space: O(n^2)
    # -----------------------------------------------------------------------
    def swimInWater(self, grid: List[List[int]]) -> int:
        import heapq
        # Dimensions of square grid
        N = len(grid)
        # Visited tracking set
        visit = {(0, 0)}
        # Min-heap initialized with (time/elevation, r, c)
        minH = [(grid[0][0], 0, 0)]
        # Four cardinal directions
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        while minH:
            # Extract cell with lowest reachable elevation
            t, r, c = heapq.heappop(minH)
            # Reached target bottom-right cell
            if r == N - 1 and c == N - 1: return t
            # Check neighbors
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # Check bounds and visited status
                if 0 <= nr < N and 0 <= nc < N and (nr, nc) not in visit:
                    # Mark neighbor as visited immediately
                    visit.add((nr, nc))
                    # Push to heap with updated peak path elevation
                    heapq.heappush(minH, (max(t, grid[nr][nc]), nr, nc))

    # -----------------------------------------------------------------------
    # 20. Shortest Path with Obstacle Elimination — BFS + state (r,c,k) (LC 1293) — T2
    # You are given an m x n integer matrix grid where each cell is either 0 (empty) or 1 (obstacle). You can move up, down, left, or right from and to an empty cell in one step. Return the minimum number of steps to walk from the upper left corner (0, 0) to the lower right corner (m - 1, n - 1) given that you can eliminate at most k obstacles. If it is not possible to find such walk return -1.
    # Example: grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], k = 1 → 6
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 40
    # Time: O(m*n*k), Space: O(m*n*k)
    # -----------------------------------------------------------------------
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        if ROWS == 1 and COLS == 1: return 0
        q = deque([(0, 0, k, 0)])  # r, c, remaining eliminations, steps
        visited = {(0, 0, k)}
        dirs = [(0,1),(0,-1),(1,0),(-1,0)]
        while q:
            r, c, elim, steps = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    new_elim = elim - grid[nr][nc]
                    if new_elim >= 0 and (nr, nc, new_elim) not in visited:
                        if nr == ROWS - 1 and nc == COLS - 1:
                            return steps + 1
                        visited.add((nr, nc, new_elim))
                        q.append((nr, nc, new_elim, steps + 1))
        return -1

    # -----------------------------------------------------------------------
    # 21. Sequence Reconstruction (LC 444) — T1
    # You are given an integer array nums of length n where nums is a permutation of the integers in the range [1, n]. You are also given a 2D integer array sequences where sequences[i] is a subsequence of nums. Check if nums is the shortest possible and the only supersequence.
    # Example: nums = [1,2,3], sequences = [[1,2],[1,3]] → false
    # Constraints: n == nums.length, 1 <= n <= 10^4
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def sequenceReconstruction(self, nums: List[int], sequences: List[List[int]]) -> bool:
        # Check if the unique topological sort of sequences is exactly nums
        adj = defaultdict(list)
        indegree = defaultdict(int)

        # Build graph
        nodes = set()
        for seq in sequences:
            for i in range(len(seq)):
                nodes.add(seq[i])
                if i < len(seq) - 1:
                    u, v = seq[i], seq[i+1]
                    adj[u].append(v)
                    indegree[v] += 1

        # Check if nodes in sequences match elements in nums
        if len(nodes) != len(nums) or set(nums) != nodes:
            return False

        # Topo sort
        q = deque([node for node in nodes if indegree[node] == 0])
        res = []

        while q:
            # For a unique reconstruction, there must be exactly one choice at each step
            if len(q) > 1:
                return False

            node = q.popleft()
            res.append(node)

            for nei in adj[node]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return res == nums

    # -----------------------------------------------------------------------
    # 13. Regions Cut By Slashes (LC 959) — T3
    # An n x n grid is composed of 1 x 1 squares where each 1 x 1 square consists of a '/', '\', or blank space ' '. These characters divide the square into contiguous regions. Given the grid grid represented as a string array, return the number of regions. Note that backslash characters are escaped, so a '\' is represented as '\\'.
    # Example: grid = [" /","/ "] → 2
    # Constraints: n == grid.length == grid[i].length, 1 <= n <= 30, grid[i][j] is either '/', '\', or ' '
    # Time: O(n^2 * alpha(n^2)), Space: O(n^2)
    # -----------------------------------------------------------------------
    def regionsBySlashes(self, grid: List[str]) -> int:
        # Grid dimensions (n x n)
        n = len(grid)
        # parent array tracking disjoint sets of size 4*n*n
        parent = list(range(4 * n * n))

        def find(i):
            """Finds the representative/root value used by the enclosing data structure."""
            # If not root node
            if parent[i] != i:
                # Path compression
                parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            """Merges two components when they are not already connected."""
            # Find representatives of both sets
            root_i = find(i)
            root_j = find(j)
            # Union the components if they are in different sets
            if root_i != root_j:
                parent[root_i] = root_j

        # Loop through each cell in grid
        for r in range(n):
            for c in range(n):
                # Compute base index for the 4 triangles of current cell
                root = 4 * (r * n + c)
                val = grid[r][c]

                # Internal edges: Union triangles inside the cell
                if val == '/':
                    union(root + 0, root + 3)
                    union(root + 1, root + 2)
                elif val == '\\':
                    union(root + 0, root + 1)
                    union(root + 2, root + 3)
                else:
                    union(root + 0, root + 1)
                    union(root + 1, root + 2)
                    union(root + 2, root + 3)

                # Down edge: Connect bottom triangle to neighbor top triangle
                if r + 1 < n:
                    union(root + 2, 4 * ((r + 1) * n + c) + 0)
                # Right edge: Connect right triangle to neighbor left triangle
                if c + 1 < n:
                    union(root + 1, 4 * (r * n + c + 1) + 3)

        # Count total number of unique roots
        return sum(find(i) == i for i in range(4 * n * n))

    # -----------------------------------------------------------------------
    # 14. Minimum Cost to Make at Least One Valid Path in a Grid (LC 1368) — T3
    # Given an m x n grid. Each cell of the grid has a sign pointing to the next cell you should visit if you are currently in this cell. The sign of grid[i][j] can be: Notice that there could be some signs on the cells of the grid that point outside the grid. You will initially start at the upper left cell (0, 0). A valid path in the grid is a path that starts from the upper left cell (0, 0) and ends at the bottom-right cell (m - 1, n - 1) following the signs on the grid. The valid path does not have to be the shortest. You can modify the sign on a cell with cost = 1. You can modify the sign on a cell one time only. Return the minimum cost to make the grid have at least one valid path.
    # Example: grid = [[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]] → 3
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 100, 1 <= grid[i][j] <= 4
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def minCost(self, grid: List[List[int]]) -> int:
        from collections import deque
        # Retrieve grid dimensions
        m, n = len(grid), len(grid[0])
        # Right, Left, Down, Up (matching index + 1 value in grid)
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        # Min cost array to reach each cell, initialized to infinity
        dist = [[float('inf')] * n for _ in range(m)]
        # Cost to reach start cell is zero
        dist[0][0] = 0

        # Deque for 0-1 BFS
        q = deque([(0, 0)])

        while q:
            r, c = q.popleft()

            # Process all 4 neighbor directions
            for i, (dr, dc) in enumerate(dirs):
                nr, nc = r + dr, c + dc
                # Check grid boundary bounds
                if 0 <= nr < m and 0 <= nc < n:
                    # cost is 0 if move matches arrow direction, else 1
                    cost = 0 if grid[r][c] == i + 1 else 1
                    # Relax cost if a cheaper path is found
                    if dist[r][c] + cost < dist[nr][nc]:
                        dist[nr][nc] = dist[r][c] + cost
                        # If cost-0, prioritize at front of queue; if cost-1, append to back
                        if cost == 0:
                            q.appendleft((nr, nc))
                        else:
                            q.append((nr, nc))

        # Return cost to reach destination
        return dist[m - 1][n - 1]

    # -----------------------------------------------------------------------
    # 15. Transitive Closure (Graph classic) — T2
    # Given a directed graph, find the transitive closure of the graph. The transitive closure is a boolean matrix representing whether there is a path from each node to every other node.
    # Example: n = 4, edges = [[0,1], [1,2], [2,3]] → [[1,1,1,1],[0,1,1,1],[0,0,1,1],[0,0,0,1]]
    # Constraints: 1 <= n <= 100
    # Time: O(n^3), Space: O(n^2)
    # -----------------------------------------------------------------------
    def transitiveClosure(self, n: int, graph: List[List[int]]) -> List[List[int]]:
        # Initialize transitive closure matrix
        closure = [[0] * n for _ in range(n)]

        # Copy direct edges adjacency matrix into closure matrix
        for i in range(n):
            for j in range(n):
                closure[i][j] = graph[i][j]

        # Floyd-Warshall reachability DP matrix updates
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    # Check if i can reach j via intermediate node k
                    closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

        return closure

if __name__ == "__main__":
    sol1 = GraphSolutions()
    sol2 = GraphSolutionsT2()

    # numIslands
    assert sol1.numIslands([["1","1","0"],["0","1","0"],["0","0","1"]]) == 2
    assert sol1.numIslands([["1","1","1"],["0","1","0"],["1","1","1"]]) == 1

    # maxAreaOfIsland
    assert sol1.maxAreaOfIsland([[0,0,1,0],[0,1,1,0],[0,1,0,0],[0,0,0,1]]) == 4
    assert sol1.maxAreaOfIsland([[0,0,0,0]]) == 0

    # cloneGraph (basic: 4-node cycle 1-2-3-4-1)
    n1 = GraphNode(1); n2 = GraphNode(2); n3 = GraphNode(3); n4 = GraphNode(4)
    n1.neighbors = [n2, n4]; n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]; n4.neighbors = [n1, n3]
    cloned = sol1.cloneGraph(n1)
    assert cloned is not n1
    assert cloned.val == 1
    assert len(cloned.neighbors) == 2

    # canFinish (cycle detection)
    assert sol1.canFinish(2, [[1, 0]]) == True
    assert sol1.canFinish(2, [[1, 0], [0, 1]]) == False

    # findOrder (topological sort)
    assert sol1.findOrder(4, [[1,0],[2,0],[3,1],[3,2]]) == [0, 1, 2, 3] or \
           sol1.findOrder(4, [[1,0],[2,0],[3,1],[3,2]]) in [[0,2,1,3], [0,1,2,3]]
    assert sol1.findOrder(1, []) == [0]

    # alienOrder
    result = sol1.alienOrder(["wrt","wrf","er","ett","rftt"])
    assert result in ["wertf", "wrtef"] or len(result) == 5  # valid topo order

    # floodFill
    img = [[1,1,1],[1,1,0],[1,0,1]]
    assert sol2.floodFill(img, 1, 1, 2) == [[2,2,2],[2,2,0],[2,0,1]]

    # pacificAtlantic
    heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
    result = sol2.pacificAtlantic(heights)
    assert [0,4] in result and [1,3] in result and [4,0] in result

    # solve (surrounded regions)
    board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
    sol2.solve(board)
    assert board[1][1] == "X" and board[3][1] == "O"  # border-connected O preserved

    # isBipartite
    assert sol2.isBipartite([[1,3],[0,2],[1,3],[0,2]]) == True
    assert sol2.isBipartite([[1,2,3],[0,2],[0,1,3],[0,2]]) == False

    # eventualSafeNodes
    assert sol2.eventualSafeNodes([[1,2],[2,3],[5],[0],[5],[],[]]) == [2,4,5,6]

    # findRedundantConnection
    assert sol2.findRedundantConnection([[1,2],[1,3],[2,3]]) == [2,3]

    # allPathsSourceTarget
    paths = sol2.allPathsSourceTarget([[1,2],[3],[3],[]])
    assert sorted(paths) == sorted([[0,1,3],[0,2,3]])

    # findSmallestSetOfVertices
    assert sorted(sol2.findSmallestSetOfVertices(6, [[0,1],[0,2],[2,5],[3,4],[4,2]])) == [0,3]

    # countComponents
    assert sol2.countComponents(5, [[0,1],[1,2],[3,4]]) == 2
    assert sol2.countComponents(4, [[0,1],[2,3],[1,2]]) == 1

    # validTree
    assert sol2.validTree(5, [[0,1],[0,2],[0,3],[1,4]]) == True
    assert sol2.validTree(5, [[0,1],[1,2],[2,3],[1,3],[1,4]]) == False

    # minimumSpanningTree (Kruskal/Prim)
    assert sol2.minimumSpanningTree(4, [[0,1,1],[0,2,4],[1,2,2],[1,3,5],[2,3,1]]) == 4

    # networkDelayTime (Dijkstra)
    assert sol2.networkDelayTime([[2,1,1],[2,3,1],[3,4,1]], 4, 2) == 2
    assert sol2.networkDelayTime([[1,2,1]], 2, 2) == -1  # unreachable

    # swimInWater
    assert sol2.swimInWater([[0,2],[1,3]]) == 3
    assert sol2.swimInWater([[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]) == 16

    # shortestPath (BFS with at most k obstacles)
    assert sol2.shortestPath([[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]], 1) == 6
    assert sol2.shortestPath([[0,1,1],[1,1,1],[1,0,0]], 1) == -1

    # sequenceReconstruction
    assert sol2.sequenceReconstruction([1,2,3], [[1,2],[1,3],[2,3]]) == True
    assert sol2.sequenceReconstruction([1,2,3], [[1,2],[2,3],[1,3],[3,2]]) == False

    # regionsBySlashes
    assert sol2.regionsBySlashes([" /","/ "]) == 2
    assert sol2.regionsBySlashes(["/\\"]) == 2  # LC example

    # minCost (0-1 BFS)
    assert sol2.minCost([[1,1,1,1],[2,2,2,2],[1,1,1,1],[2,2,2,2]]) == 3

    # transitiveClosure
    g = [[1,1,0,1],[0,1,1,0],[0,0,1,1],[0,0,0,1]]
    tc = sol2.transitiveClosure(4, g)
    assert tc[0][3] == 1  # 0 can reach 3 directly
    assert tc[1][3] == 1  # 1->2->3

    print("All graph tests passed.")
