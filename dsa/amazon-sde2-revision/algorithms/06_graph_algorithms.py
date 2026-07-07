"""
Graph Algorithms patterns and algorithms — Google L3/L4 interview prep.

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

class GraphAlgorithmSolutions:
    # -----------------------------------------------------------------------
    # 1. Number of Islands (LC 200) — T1
    # Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
    # Example: grid = [ → 1
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 300, grid[i][j] is '0' or '1'
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def numIslands(self, grid: List[List[str]]) -> int:
        # If the grid is empty, there are no islands.
        if not grid: return 0
        rows, cols = len(grid), len(grid[0])
        count = 0
        # Depth First Search to sink/flood-fill the connected land.
        def dfs(r, c):
            # Base case: if out of bounds or water ('0'), stop the traversal.
            """Depth-first-search helper for the enclosing solution."""
            if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
                return
            # Mark the current cell as water ('0') to prevent double-counting.
            grid[r][c] = '0'
            # Recursively traverse all four adjacent directions (down, up, right, left).
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)
        # Scan every cell in the grid.
        for r in range(rows):
            for c in range(cols):
                # When land ('1') is encountered, it indicates a new island.
                if grid[r][c] == '1':
                    count += 1
                    # Sink the entire island using DFS.
                    dfs(r, c)
        return count

    # -----------------------------------------------------------------------
    # 2. Clone Graph (LC 133) — T1
    # Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph. Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors. class Node { public int val; public List<Node> neighbors; } Test case format: For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list. An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph. The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.
    # Example: adjList = [[2,4],[1,3],[2,4],[1,3]] → [[2,4],[1,3],[2,4],[1,3]]
    # Constraints: The number of nodes in the graph is in the range [0, 100], 1 <= Node.val <= 100, Node.val is unique for each node, There are no repeated edges and no self-loops in the graph, The Graph is connected and all nodes can be visited starting from the given node
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def cloneGraph(self, node: 'GraphNode') -> 'GraphNode':
        # Base case: if the input node is None, return None.
        if not node: return node
        # Map to store mappings from original nodes to their cloned counterparts.
        oldToNew = {}
        # DFS function to traverse and clone the graph.
        def dfs(node):
            # If the node has already been cloned, return the existing copy to avoid cycles.
            """Depth-first-search helper for the enclosing solution."""
            if node in oldToNew:
                return oldToNew[node]
            # Create a clone of the current node with its value.
            copy = GraphNode(node.val)
            # Store the clone in the map before processing neighbors to handle cycle back-edges.
            oldToNew[node] = copy
            # Recursively clone all neighbors and append them to the cloned node's neighbors list.
            for nei in node.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy
        # Start the DFS cloning from the input node.
        return dfs(node)

    # -----------------------------------------------------------------------
    # 3. Pacific Atlantic Water Flow (LC 417) — T1
    # There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges. The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c). The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean. Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.
    # Example: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]] → [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
    # Constraints: m == heights.length, n == heights[r].length, 1 <= m, n <= 200, 0 <= heights[r][c] <= 10^5
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        ROWS, COLS = len(heights), len(heights[0])
        # Sets to store coordinate cells that can flow into the Pacific and Atlantic oceans.
        pac, atl = set(), set()
        
        # DFS to find all cells that can flow back from the ocean upward.
        def dfs(r, c, visit, prevHeight):
            # Stop if out of bounds, cell is already visited, or height is less than previous height (flow must go uphill).
            """Depth-first-search helper for the enclosing solution."""
            if ((r, c) in visit or r < 0 or c < 0 or r == ROWS or c == COLS or heights[r][c] < prevHeight):
                return
            # Mark the cell as visited for the current ocean.
            visit.add((r, c))
            # Recursively walk to neighbors in four directions.
            dfs(r + 1, c, visit, heights[r][c])
            dfs(r - 1, c, visit, heights[r][c])
            dfs(r, c + 1, visit, heights[r][c])
            dfs(r, c - 1, visit, heights[r][c])
            
        # Run DFS from the top row (Pacific) and bottom row (Atlantic).
        for c in range(COLS):
            dfs(0, c, pac, heights[0][c])
            dfs(ROWS - 1, c, atl, heights[ROWS - 1][c])
        # Run DFS from the left column (Pacific) and right column (Atlantic).
        for r in range(ROWS):
            dfs(r, 0, pac, heights[r][0])
            dfs(r, COLS - 1, atl, heights[r][COLS - 1])
            
        res = []
        # Find cells that are present in both Pacific and Atlantic reachable sets.
        for r in range(ROWS):
            for c in range(COLS):
                if (r, c) in pac and (r, c) in atl:
                    res.append([r, c])
        return res

    # -----------------------------------------------------------------------
    # 4. Course Schedule (LC 207) — T1
    # There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai. Return true if you can finish all courses. Otherwise, return false.
    # Example: numCourses = 2, prerequisites = [[1,0]] → true
    # Constraints: 1 <= numCourses <= 2000, 0 <= prerequisites.length <= 5000, prerequisites[i].length == 2, 0 <= ai, bi < numCourses, All the pairs prerequisites[i] are unique
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        # Build adjacency list mapping each course to its prerequisite courses.
        preMap = {i: [] for i in range(numCourses)}
        for crs, pre in prerequisites:
            preMap[crs].append(pre)
        # Set to track courses on the current recursion path to detect cycles.
        visitSet = set()
        # DFS helper to detect cycles.
        def dfs(crs):
            # If the course is already in the active DFS path, a cycle is detected.
            """Depth-first-search helper for the enclosing solution."""
            if crs in visitSet: return False
            # If the course has no prerequisites, it can be finished.
            if preMap[crs] == []: return True
            # Add course to current DFS path.
            visitSet.add(crs)
            # Recursively verify all prerequisites.
            for pre in preMap[crs]:
                if not dfs(pre): return False
            # Backtrack: remove course from the active path.
            visitSet.remove(crs)
            # Memoize by clearing prerequisites for this course since it's verified.
            preMap[crs] = []
            return True
        # Run DFS for every course in the graph to handle disconnected components.
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
        # Build adjacency list mapping each course to its prerequisites.
        preMap = {i: [] for i in range(numCourses)}
        for crs, pre in prerequisites:
            preMap[crs].append(pre)
        # visit tracks fully processed nodes; cycle tracks active path for cycle detection.
        visit, cycle = set(), set()
        output = []
        # Topological sort helper via DFS post-order traversal.
        def dfs(crs):
            # Cycle detected on the active path.
            """Depth-first-search helper for the enclosing solution."""
            if crs in cycle: return False
            # Memoized check: already processed and safe.
            if crs in visit: return True
            # Add node to active path.
            cycle.add(crs)
            # Process prerequisites first.
            for pre in preMap[crs]:
                if not dfs(pre): return False
            # Backtrack: remove from active path.
            cycle.remove(crs)
            # Mark node as fully processed.
            visit.add(crs)
            # Append to output after all prerequisites are processed (post-order).
            output.append(crs)
            return True
        # Traverse every course.
        for c in range(numCourses):
            if not dfs(c): return []
        return output

    # -----------------------------------------------------------------------
    # 6. Word Ladder (LC 127) — T1
    # A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that: Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
    # Example: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"] → 5
    # Constraints: 1 <= beginWord.length <= 10, endWord.length == beginWord.length, 1 <= wordList.length <= 5000, wordList[i].length == beginWord.length, beginWord, endWord, and wordList[i] consist of lowercase English letters, beginWord != endWord, All the words in wordList are unique
    # Time: O(N*L*26), Space: O(N)
    # -----------------------------------------------------------------------
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        # Convert wordList to set for O(1) lookups.
        wordSet = set(wordList)
        # If the target word is not in the dictionary, a valid sequence is impossible.
        if endWord not in wordSet: return 0
        # Initialize queue for BFS tracking (current_word, sequence_length).
        q = deque([(beginWord, 1)])
        while q:
            word, length = q.popleft()
            # If target word is reached, return the sequence length.
            if word == endWord: return length
            # Generate all possible single-character mutations of the current word.
            for i in range(len(word)):
                for c in 'abcdefghijklmnopqrstuvwxyz':
                    next_word = word[:i] + c + word[i+1:]
                    # If mutation exists in wordSet, it's a valid neighbor.
                    if next_word in wordSet:
                        # Remove from set to prevent visiting again and queue it up.
                        wordSet.remove(next_word)
                        q.append((next_word, length + 1))
        return 0

    # -----------------------------------------------------------------------
    # 7. All Paths From Source to Target — T1
    # Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order. The graph is given as follows: graph[i] is a list of all nodes you can visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).
    # Example: graph = [[1,2],[3],[3],[]] → [[0,1,3],[0,2,3]]
    # Constraints: n == graph.length, 2 <= n <= 15, 0 <= graph[i][j] < n, graph[i][j] != i (i.e., there will be no self-loops), All the elements of graph[i] are unique, The input graph is guaranteed to be a DAG
    # Time: O(2^V * V), Space: O(V)
    # -----------------------------------------------------------------------
    def allPathsSourceTarget(self, graph: List[List[int]]) -> List[List[int]]:
        res = []
        # DFS helper for path finding.
        def dfs(node, path):
            # Target node reached, store a copy of the path.
            """Depth-first-search helper for the enclosing solution."""
            if node == len(graph) - 1:
                res.append(path[:])
                return
            # Traverse neighbors and backtrack.
            for nei in graph[node]:
                path.append(nei)
                dfs(nei, path)
                path.pop()
        # Start path search from source node 0 with path initially containing [0].
        dfs(0, [0])
        return res

    # -----------------------------------------------------------------------
    # 8. Is Graph Bipartite — T1
    # There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to. More formally, for each v in graph[u], there is an undirected edge between node u and node v. The graph has the following properties: between them. A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B. Return true if and only if it is bipartite.
    # Example: graph = [[1,2,3],[0,2],[0,1,3],[0,2]] → false
    # Constraints: graph.length == n, 1 <= n <= 100, 0 <= graph[u].length < n, 0 <= graph[u][i] <= n - 1, graph[u] does not contain u, All the values of graph[u] are unique, If graph[u] contains v, then graph[v] contains u
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def isBipartite(self, graph: List[List[int]]) -> bool:
        colors = {}
        # Iterate through all nodes to handle disconnected graphs.
        for i in range(len(graph)):
            # If node is not colored, start a new coloring component.
            if i not in colors:
                colors[i] = 0
                q = deque([i])
                while q:
                    node = q.popleft()
                    # Assign opposite color (1-color) to all neighbors.
                    for nei in graph[node]:
                        if nei not in colors:
                            colors[nei] = 1 - colors[node]
                            q.append(nei)
                        # Conflict detected: neighbor has the same color.
                        elif colors[nei] == colors[node]:
                            return False
        return True

    # -----------------------------------------------------------------------
    # 9. Alien Dictionary (LC 269) — T1
    # There is a new alien language that uses the English alphabet. However, the order among the letters is unknown to you. You are given a list of strings words from the alien language's dictionary, where the strings in words are sorted lexicographically by the rules of this new language. Return a string of the unique letters in the new alien language sorted in lexicographically increasing order by the new language's rules.
    # Time: O(C), Space: O(U)
    # -----------------------------------------------------------------------
    def alienOrder(self, words: List[str]) -> str:
        # Initialize adjacency list for all unique characters present in the dictionary.
        adj = {c: set() for w in words for c in w}
        # Compare consecutive words to build directed ordering edges.
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            minLen = min(len(w1), len(w2))
            # Edge case: prefix check where a longer prefix comes before a shorter word.
            if len(w1) > len(w2) and w1[:minLen] == w2[:minLen]:
                return ""
            # Find the first differing character to build an order relationship.
            for j in range(minLen):
                if w1[j] != w2[j]:
                    adj[w1[j]].add(w2[j])
                    break
        # visit tracks states: True for in active path, False for fully visited.
        visit = {}
        res = []
        # Post-order DFS topological sort.
        def dfs(c):
            """Depth-first-search helper for the enclosing solution."""
            if c in visit: return visit[c]
            # Mark character as visiting in the active path.
            visit[c] = True
            for nei in adj[c]:
                # Recursively check neighbors for cycles.
                if dfs(nei): return True
            # Mark character as fully visited.
            visit[c] = False
            # Append to results in post-order.
            res.append(c)
            return False
        # Run topological sort DFS for each character.
        for c in adj:
            if dfs(c): return ""
        # Reverse post-order results to obtain the topological sort.
        res.reverse()
        return "".join(res)

    # -----------------------------------------------------------------------
    # 10. Longest Path in DAG — Topological Sort DP
    # Given a weighted directed acyclic graph with n nodes (0-indexed) and a list of directed weighted edges, find the length of the longest path (by total weight) in the DAG.
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def longestPathDAG(self, n: int, edges: List[List[int]]) -> int:
        """Longest Path in DAG: Build an adjacency list and compute in-degrees for all nodes."""
        # Build adjacency list representation of the directed weighted graph.
        adj = defaultdict(list)
        indegree = [0] * n
        for u, v, w in edges:
            adj[u].append((v, w))
            indegree[v] += 1
        # Queue to store nodes with 0 in-degree.
        q = deque()
        dist = [0] * n
        # Seed queue with all source nodes (zero in-degree).
        for i in range(n):
            if indegree[i] == 0:
                q.append(i)
        # Process nodes in topological order using Kahn's BFS.
        while q:
            u = q.popleft()
            # Relax outgoing edges from the current node.
            for v, w in adj[u]:
                if dist[u] + w > dist[v]:
                    dist[v] = dist[u] + w
                # Decrement in-degree for neighbors; enqueue when they become zero.
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)
        # Return the maximum distance computed in the DAG.
        return max(dist)

    # -----------------------------------------------------------------------
    # 11. Number of Ways to Reach Destination (LC 1976 variant)
    # Given n nodes, a list of weighted undirected edges, and source/destination, count the number of shortest paths from source to destination in the weighted graph.
    # Time: O((V+E) log V), Space: O(V+E)
    # -----------------------------------------------------------------------
    def countPaths(self, n: int, roads: List[List[int]], src: int, dst: int) -> int:
        import heapq
        MOD = 10**9 + 7
        # Build undirected graph adjacency list.
        adj = defaultdict(list)
        for u, v, w in roads:
            adj[u].append((v, w))
            adj[v].append((u, w))
        # dist tracks shortest distance; ways tracks count of shortest paths.
        dist = [float('inf')] * n
        ways = [0] * n
        dist[src] = 0
        ways[src] = 1
        # Min-heap stores pairs of (distance, node).
        heap = [(0, src)]
        while heap:
            d, u = heapq.heappop(heap)
            # Skip stale nodes popped from the heap.
            if d > dist[u]:
                continue
            # Relax neighbors of node u.
            for v, w in adj[u]:
                nd = d + w
                # Found a strictly shorter path to node v.
                if nd < dist[v]:
                    dist[v] = nd
                    ways[v] = ways[u]
                    heapq.heappush(heap, (nd, v))
                # Found an alternative path of the same shortest length.
                elif nd == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD
        # Return the number of shortest paths to the destination.
        return ways[dst]

    # -----------------------------------------------------------------------
    # 12. Cheapest Flights Within K Stops (LC 787)
    # Given n cities, a list of flights [from, to, price], find the cheapest price from src to dst with at most k stops. Return -1 if no such route exists.
    # Time: O(K * E), Space: O(V)
    # -----------------------------------------------------------------------
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        # dist tracks the minimum price to reach each node.
        dist = [float('inf')] * n
        dist[src] = 0
        # Relax edges up to k + 1 times (k stops + 1 transition edge).
        for _ in range(k + 1):
            # Create a snapshot copy of the previous round's prices.
            prices = dist[:]
            # Relax all flight edges.
            for u, v, w in flights:
                if prices[u] != float('inf') and prices[u] + w < dist[v]:
                    dist[v] = prices[u] + w
        # Return final price if reachable, else -1.
        return dist[dst] if dist[dst] != float('inf') else -1

    # -----------------------------------------------------------------------
    # 13. Parallel Courses (LC 1136)
    # Given n courses labeled 1..n and relations [prevCourse, nextCourse], return the minimum number of semesters to take all courses. Return -1 if impossible.
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def minimumSemesters(self, n: int, relations: List[List[int]]) -> int:
        # Build directed graph adjacency list and track in-degrees.
        adj = defaultdict(list)
        indegree = [0] * (n + 1)
        for prev, nxt in relations:
            adj[prev].append(nxt)
            indegree[nxt] += 1
        # Seed the queue with all courses that have no prerequisites.
        q = deque()
        for i in range(1, n + 1):
            if indegree[i] == 0:
                q.append(i)
        semesters = 0
        processed = 0
        # Process BFS level by level, where each level represents one semester.
        while q:
            semesters += 1
            # Process all courses available in the current semester.
            for _ in range(len(q)):
                node = q.popleft()
                processed += 1
                for nxt in adj[node]:
                    indegree[nxt] -= 1
                    # If all prerequisites are cleared, course is available next semester.
                    if indegree[nxt] == 0:
                        q.append(nxt)
        # Return semesters if all courses could be taken, otherwise -1 (cycle detected).
        return semesters if processed == n else -1

    # -----------------------------------------------------------------------
    # 14. Parallel Courses III (LC 2050)
    # Given n courses labeled 1..n, relations [prevCourse, nextCourse], and time[] where time[i] is weeks to complete course i+1, return the minimum number of weeks to complete all courses.
    # Time: O(V+E), Space: O(V+E)
    # -----------------------------------------------------------------------
    def minimumTime(self, n: int, relations: List[List[int]], time: List[int]) -> int:
        # Build adjacency list and in-degrees (1-indexed nodes).
        adj = defaultdict(list)
        indegree = [0] * (n + 1)
        for prev, nxt in relations:
            adj[prev].append(nxt)
            indegree[nxt] += 1
        # dp[i] will store the completion time of course i.
        dp = [0] * (n + 1)
        q = deque()
        # Initialise dp for source nodes and add them to the queue.
        for i in range(1, n + 1):
            if indegree[i] == 0:
                dp[i] = time[i - 1]
                q.append(i)
        # Kahn's BFS topological sort DP logic.
        while q:
            u = q.popleft()
            for v in adj[u]:
                # Relax completion time of dependent course v.
                dp[v] = max(dp[v], dp[u] + time[v - 1])
                indegree[v] -= 1
                if indegree[v] == 0:
                    q.append(v)
        # Return the maximum completion time across all courses.
        return max(dp[1:])

    # -----------------------------------------------------------------------
    # 15. Count Unreachable Pairs of Nodes (LC 2316)
    # Given n nodes (0-indexed) and a list of undirected edges, return the number of pairs of nodes (i, j) where i < j and there is no path between i and j.
    # Time: O(V+E), Space: O(V)
    # -----------------------------------------------------------------------
    def countPairs(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)
        visited = set()

        def dfs(node):
            size = 1
            for nei in graph[node]:
                if nei not in visited:
                    visited.add(nei)
                    size += dfs(nei)
            return size

        comp_sizes = []
        for i in range(n):
            if i not in visited:
                visited.add(i)
                comp_sizes.append(dfs(i))

        reachable = sum(s * (s - 1) // 2 for s in comp_sizes)
        total = n * (n - 1) // 2
        return total - reachable

    # -----------------------------------------------------------------------
    # 16. Reachable Nodes In Subdivided Graph (LC 882)
    # An undirected graph has n nodes. Each edge [u, v, cnt] has cnt new nodes inserted on it (subdividing it into cnt+1 edges). Starting from node 0 with maxMoves moves, return the number of reachable nodes (original + subdivided).
    # Time: O((V+E) log V), Space: O(V+E)
    # -----------------------------------------------------------------------
    def reachableNodes(self, edges: List[List[int]], maxMoves: int, n: int) -> int:
        import heapq
        # Build undirected graph adjacency list.
        adj = defaultdict(list)
        for u, v, cnt in edges:
            adj[u].append((v, cnt))
            adj[v].append((u, cnt))
        # Run Dijkstra from source node 0.
        dist = {0: 0}
        heap = [(0, 0)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist.get(u, float('inf')):
                continue
            for v, cnt in adj[u]:
                # Cost to traverse original edge is cnt + 1.
                nd = d + cnt + 1
                if nd < dist.get(v, float('inf')):
                    dist[v] = nd
                    heapq.heappush(heap, (nd, v))
        # Count all original nodes reached within maxMoves.
        result = sum(1 for i in range(n) if dist.get(i, float('inf')) <= maxMoves)
        # Process each edge to count how many subdivided nodes are reachable.
        for u, v, cnt in edges:
            from_u = max(0, maxMoves - dist.get(u, float('inf'))) if dist.get(u, float('inf')) <= maxMoves else 0
            from_v = max(0, maxMoves - dist.get(v, float('inf'))) if dist.get(v, float('inf')) <= maxMoves else 0
            # Sum of steps from both directions, capped by the total subdivided nodes count.
            result += min(from_u + from_v, cnt)
        return result

    # -----------------------------------------------------------------------
    # 17. Minimum Weighted Subgraph with Required Paths (LC 2203)
    # Given n nodes, weighted directed edges, src1, src2, dest, find the minimum weight of a subgraph that has paths from src1 to dest and src2 to dest. Return -1 if impossible.
    # Time: O((V+E) log V), Space: O(V+E)
    # -----------------------------------------------------------------------
    def minimumWeight(self, n: int, edges: List[List[int]], src1: int, src2: int, dest: int) -> int:
        import heapq
        # Build forward and reversed adjacency lists.
        adj = defaultdict(list)
        radj = defaultdict(list)
        for u, v, w in edges:
            adj[u].append((v, w))
            radj[v].append((u, w))
        # Dijkstra helper on a given graph from a source.
        def dijkstra(graph, src):
            # Distance array initialized to infinity
            dist = [float('inf')] * n
            dist[src] = 0
            # Min-heap with (distance, node)
            heap = [(0, src)]
            while heap:
                d, u = heapq.heappop(heap)
                # Skip if a shorter path is already found
                if d > dist[u]: continue
                # Relax neighbor edges
                for v, w in graph[u]:
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        heapq.heappush(heap, (dist[v], v))
            return dist
        # Run forward Dijkstra from src1 and src2, and reversed Dijkstra from dest.
        d1 = dijkstra(adj, src1)
        d2 = dijkstra(adj, src2)
        d3 = dijkstra(radj, dest)
        ans = float('inf')
        # Find the meeting point m that minimizes the sum of distances.
        for m in range(n):
            if d1[m] != float('inf') and d2[m] != float('inf') and d3[m] != float('inf'):
                ans = min(ans, d1[m] + d2[m] + d3[m])
        return ans if ans != float('inf') else -1

    # -----------------------------------------------------------------------
    # 18. Strange Printer II (LC 1591)
    # Given a target grid of colors (1-indexed), determine if it is possible to print the grid using a strange printer that prints solid rectangles of one color at a time, where later prints overwrite earlier ones.
    # Time: O(C^2 + R*C) where C=num colors, Space: O(C^2)
    # -----------------------------------------------------------------------
    def isPrintable(self, targetGrid: List[List[int]]) -> bool:
        rows, cols = len(targetGrid), len(targetGrid[0])
        # Find boundaries (min_row, min_col, max_row, max_col) for each color.
        bounds = {}
        for r in range(rows):
            for c in range(cols):
                color = targetGrid[r][c]
                if color not in bounds:
                    bounds[color] = [r, c, r, c]
                else:
                    bounds[color][0] = min(bounds[color][0], r)
                    bounds[color][1] = min(bounds[color][1], c)
                    bounds[color][2] = max(bounds[color][2], r)
                    bounds[color][3] = max(bounds[color][3], c)
        # Build dependency graph: color A must be printed before color B if B is inside A's bounds.
        adj = defaultdict(set)
        for color, (r1, c1, r2, c2) in bounds.items():
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    other = targetGrid[r][c]
                    if other != color:
                        adj[color].add(other)
        # visit tracks states: True for in active path, False for fully visited.
        visit = {}
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Return cached traversal/visiting state
            if node in visit:
                return visit[node]
            # Mark node on active path
            visit[node] = True
            for nei in adj[node]:
                if dfs(nei):
                    return True
            # Backtrack from active path
            visit[node] = False
            return False
        # Verify if the dependency graph contains any cycles.
        for color in bounds:
            if dfs(color):
                return False
        return True

if __name__ == "__main__":
    sol = GraphAlgorithmSolutions()

    # numIslands
    grid = [["1","1","1","1","0"],["1","1","0","1","0"],
            ["1","1","0","0","0"],["0","0","0","0","0"]]
    assert sol.numIslands([row[:] for row in grid]) == 1
    grid2 = [["1","1","0","0","0"],["1","1","0","0","0"],
             ["0","0","1","0","0"],["0","0","0","1","1"]]
    assert sol.numIslands([row[:] for row in grid2]) == 3

    # canFinish (cycle detection)
    assert sol.canFinish(2, [[1,0]]) == True
    assert sol.canFinish(2, [[1,0],[0,1]]) == False

    # findOrder (topological sort)
    res = sol.findOrder(4, [[1,0],[2,0],[3,1],[3,2]])
    assert len(res) == 4 and res[0] == 0  # 0 must come first

    # ladderLength (BFS)
    assert sol.ladderLength("hit", "cog", ["hot","dot","dog","lot","log","cog"]) == 5
    assert sol.ladderLength("hit", "cog", ["hot","dot","dog","lot","log"]) == 0

    # allPathsSourceTarget
    assert sorted(sol.allPathsSourceTarget([[1,2],[3],[3],[]])) == [[0,1,3],[0,2,3]]

    # isBipartite
    assert sol.isBipartite([[1,3],[0,2],[1,3],[0,2]]) == True
    assert sol.isBipartite([[1,2,3],[0,2],[0,1,3],[0,2]]) == False

    # alienOrder
    order = sol.alienOrder(["wrt","wrf","er","ett","rftt"])
    assert order != ""  # valid topological order exists
    assert sol.alienOrder(["z","x"]) in ["zx", ""]  # z before x
    assert sol.alienOrder(["z","x","z"]) == ""  # invalid

    # longestPathDAG
    # 0 --(3)--> 1 --(2)--> 2 : longest path = 5
    assert sol.longestPathDAG(3, [[0,1,3],[1,2,2]]) == 5
    assert sol.longestPathDAG(4, [[0,1,1],[0,2,4],[1,3,1],[2,3,1]]) == 5

    # countPaths (number of shortest paths)
    # 0 --1-- 1 --1-- 2  and  0 --2-- 2 : two shortest paths from 0 to 2
    paths = sol.countPaths(3, [[0,1,1],[1,2,1],[0,2,2]], 0, 2)
    assert paths == 2

    # findCheapestPrice (Bellman-Ford / K stops)
    assert sol.findCheapestPrice(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1) == 700
    assert sol.findCheapestPrice(3, [[0,1,100],[1,2,100],[0,2,500]], 0, 2, 0) == 500

    # minimumSemesters (Parallel Courses LC 1136)
    assert sol.minimumSemesters(3, [[1,3],[2,3]]) == 2
    assert sol.minimumSemesters(3, [[1,2],[2,3],[3,1]]) == -1

    # minimumTime (Parallel Courses III LC 2050)
    assert sol.minimumTime(3, [[1,3],[2,3]], [3,2,5]) == 8
    assert sol.minimumTime(5, [[1,5],[2,5],[3,5],[4,5]], [1,2,3,4,5]) == 9

    # countPairs (Count Unreachable Pairs LC 2316)
    assert sol.countPairs(7, [[0,2],[0,5],[2,4],[1,6],[5,4]]) == 14
    assert sol.countPairs(3, [[0,1],[0,2],[1,2]]) == 0

    # reachableNodes (LC 882)
    assert sol.reachableNodes([[0,1,10],[0,2,1],[1,2,2]], 6, 3) == 13
    assert sol.reachableNodes([[1,2,4],[1,4,5],[1,3,1],[2,3,4],[3,4,5]], 17, 5) == 1

    # minimumWeight (LC 2203)
    assert sol.minimumWeight(6, [[0,2,2],[0,5,6],[1,0,3],[1,4,5],[2,1,1],[2,3,3],[2,3,4],[3,4,2],[4,5,1]], 0, 1, 5) == 9
    assert sol.minimumWeight(3, [[0,1,1],[2,1,1]], 0, 1, 2) == -1

    # isPrintable (Strange Printer II LC 1591)
    assert sol.isPrintable([[1,1,1],[1,2,2],[1,2,2]]) == True
    assert sol.isPrintable([[1,2],[2,1]]) == False

    print("All graph algorithm tests passed.")
