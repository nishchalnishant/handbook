---
tags: [coding, data-structures, graph]
topic: graph
difficulty: mixed
---
# Graph Problems — Deep Dive

## What this covers

> [!abstract] In this file
> **Covers:** Worked graph problems: BFS/DFS, topological sort, weighted shortest path, bipartite, implicit-graph BFS.
> **You'll be able to:** Model the problem as a graph and pick the traversal in under 2 min.
> **Prereqs:** Graph lecture · **Pair with:** [Graph lecture](../../02-data-structures/11-graphs.md) · [Graph algorithm problems](../algorithms/11-graph-algorithms.md) · **Time:** 4–5 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [BFS on Graphs](#bfs-on-graphs) · [DFS on Graphs](#dfs-on-graphs) · [Topological Sort](#topological-sort) · [Shortest Path / Weighted](#shortest-path--weighted) · [Bipartite / Coloring](#bipartite--coloring) · [Advanced](#advanced)

> [!tip] If you only have 20 minutes
> **Do these first:** [Number of Islands (BFS)](#number-of-islands-bfs--t1) · [Rotting Oranges](#rotting-oranges--t1) · [Clone Graph](#clone-graph--t1) · [Course Schedule II](#course-schedule-ii--t1) · [Pacific Atlantic Water Flow](#pacific-atlantic-water-flow--t1) · [Word Ladder](#word-ladder--t1) · [Is Graph Bipartite?](#is-graph-bipartite--t1) · [Network Delay Time (Dijkstra's)](#shortest-path--weighted) · [Redundant Connection](#redundant-connection--t1)
> **Template:** Grid DFS/BFS: mark visited **when enqueuing**, 4-dir `for dr, dc in ((1,0),(-1,0),(0,1),(0,-1))`.
> **Template:** Multi-source BFS: push all sources at distance 0, then expand level by level. Kahn's: queue indegree-0 nodes; `len(order) < n` ⇒ cycle.
> **Gotchas:** Marking on pop instead of push → duplicates/TLE · directed cycle needs 3 colors, undirected needs `parent` · Dijkstra: skip stale heap entries (`if d > dist[u]: continue`) · reverse thinking (border-in, target-out) for Surrounded/Pacific.

---

**Pattern map**: Graph problems collapse into five patterns — BFS (shortest path, multi-source spread), DFS (connectivity, flood fill, cycle detection), Topological Sort (dependency ordering on DAGs), Shortest Path / Weighted (Dijkstra, modified BFS), Bipartite coloring, and Advanced (Union-Find / MST / DAG DP). Pick BFS when you need minimum steps; DFS when you need reachability or ordering; Union-Find when you need dynamic connectivity with no full traversal needed.

**Interview checklist**: First classify the graph — directed or undirected, weighted or unweighted, connected or disconnected, and whether you need a path, ordering, component count, or just a yes/no query. Then look for the standard lever: multi-source BFS for simultaneous spread, DFS for flood-fill and cycle detection, Kahn's for DAG ordering, Dijkstra for non-negative weights, Bellman-Ford for hop-limited or negative-weight cases, Union-Find for connectivity, and two-coloring for bipartite checks.

**Edge cases worth checking**: empty graph, single node, disconnected components, duplicate edges, self-loops, cycles in a "tree" input, and recursion depth on large grids/graphs. For grid problems, confirm whether diagonals count, whether borders are included, and whether you can mutate the input to mark visited.

---

## BFS on Graphs

---

### Rotting Oranges `⚡ T1`

> [!example] Problem
> You are given an m x n grid where each cell can have one of three values:
> Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.
> Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
> 
> **Example 1:**
> ```
> Input: grid = [[2,1,1],[1,1,0],[0,1,1]]
> Output: 4
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[2,1,1],[0,1,1],[1,0,1]]
> Output: -1
> Explanation: The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[0,2]]
> Output: 0
> Explanation: Since there are already no fresh oranges at minute 0, the answer is just 0.
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 10
> - grid[i][j] is 0, 1, or 2.

> [!tip] Recognize · Gotcha
> **Signal:** "Simultaneous spread, minimum time" · **Gotcha:** Track fresh count — if fresh remain after BFS, return -1 (unreachable).

> [!info] Approach
> **Multi-source BFS — simultaneous spread from all rotten sources.** Rotting spreads simultaneously from all rotten sources. BFS levels naturally correspond to time steps; the first time a fresh orange is reached gives the minimum time to rot it. Seed queue with all initially rotten oranges at time 0, count fresh oranges. BFS level-by-level; each time a fresh orange is rotted, decrement fresh counter; track max time seen. Multi-source start avoids O(R × M×N) repeated BFS. Return max_time if fresh == 0, else -1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def oranges_rotting(grid):
>     rows, cols = len(grid), len(grid[0])
>     queue = deque()
>     fresh = 0
> 
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == 2:
>                 queue.append((r, c, 0))
>             elif grid[r][c] == 1:
>                 fresh += 1
> 
>     if fresh == 0:
>         return 0
> 
>     max_time = 0
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
>     while queue:
>         r, c, t = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
>                 grid[nr][nc] = 2
>                 fresh -= 1
>                 max_time = max(max_time, t + 1)
>                 queue.append((nr, nc, t + 1))
> 
>     return max_time if fresh == 0 else -1
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS with level-counting loop (`for _ in range(len(queue))`): cleaner separation of time steps but identical logic.
> - DFS: can't guarantee minimum time — BFS is canonical for shortest path.
> - Simulation (repeat until stable): O((M×N)²), wasteful.

---

### Number of Islands (BFS) `⚡ T1`

> [!example] Problem
> Given an m x n 2D binary grid grid which represents a map of '1's (land) and '0's (water), return the number of islands.
> An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are all surrounded by water.
> 
> **Example 1:**
> ```
> Input: grid = [
>   ["1","1","1","1","0"],
>   ["1","1","0","1","0"],
>   ["1","1","0","0","0"],
>   ["0","0","0","0","0"]
> ]
> Output: 1
> ```
> 
> **Example 2:**
> ```
> Input: grid = [
>   ["1","1","0","0","0"],
>   ["1","1","0","0","0"],
>   ["0","0","1","0","0"],
>   ["0","0","0","1","1"]
> ]
> Output: 3
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 300
> - grid[i][j] is '0' or '1'.

> [!tip] Recognize · Gotcha
> **Signal:** "Count connected components in grid" · **Gotcha:** 4-dir vs 8-dir neighbors — confirm with interviewer. Recursion overflow on large grids.

> [!info] Approach
> Each island is a connected component. BFS naturally fans out level-by-level from a source cell, marking all reachable land as visited. Iterate every cell; when '1' found, BFS to mark all connected land as visited ('0'), increment count. Seed the queue with the trigger cell; mark visited on enqueue (not dequeue) to prevent duplicate entries. Mutating the grid avoids an extra visited array.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def num_islands(grid):
>     if not grid:
>         return 0
>     rows, cols = len(grid), len(grid[0])
>     count = 0
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for r in range(rows):
>         for c in range(cols):
>             if grid[r][c] == '1':
>                 count += 1
>                 grid[r][c] = '0'
>                 queue = deque([(r, c)])
>                 while queue:
>                     cr, cc = queue.popleft()
>                     for dr, dc in dirs:
>                         nr, nc = cr+dr, cc+dc
>                         if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1':
>                             grid[nr][nc] = '0'
>                             queue.append((nr, nc))
>     return count
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) worst case for the queue/visited cells.

> [!tip] Alternatives
> - DFS sinking: same logic recursively; simpler code but risks recursion depth on large grids.
> - Union-Find: union adjacent '1' cells; count unique roots. O(M×N·α). Better for dynamic updates.

---

### Walls and Gates (LC 286) `⚡ T1`

> [!example] Problem
> You are given an `m x n` grid `rooms` initialized with these three possible values.
> 
> 	
> - `-1` A wall or an obstacle.
> 	
> - `0` A gate.
> 	
> - `INF` Infinity means an empty room. We use the value `2^31 - 1 = 2147483647` to represent `INF` as you may assume that the distance to a gate is less than `2147483647`.
> 
> Fill each empty room with the distance to *its nearest gate*. If it is impossible to reach a gate, it should be filled with `INF`.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]]
> **Output:** [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** rooms = [[-1]]
> **Output:** [[-1]]
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `m == rooms.length`
> 	
> - `n == rooms[i].length`
> 	
> - `1 <= m, n <= 250`
> 	
> - `rooms[i][j]` is `-1`, `0`, or `2^31 - 1`.

> [!tip] Recognize · Gotcha
> **Signal:** "Distance from each empty room to nearest gate" · **Gotcha:** Push all gates first; BFS naturally computes minimum distances without per-gate passes.

> [!info] Approach
> Multi-source BFS from all gates simultaneously guarantees every room is reached via the shortest path to any gate in O(M×N) rather than O(M×N × gates) from separate BFS per room. Seed queue with all gates (value 0); BFS outward; assign `dist[gate] + 1` to unvisited INF neighbors. Only enqueue cells that are INF — this acts as the visited guard. The first time a room is reached is always via its nearest gate.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def walls_and_gates(rooms):
>     if not rooms:
>         return
>     rows, cols = len(rooms), len(rooms[0])
>     INF = float('inf')
>     queue = deque()
>     for r in range(rows):
>         for c in range(cols):
>             if rooms[r][c] == 0:
>                 queue.append((r, c))
> 
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == INF:
>                 rooms[nr][nc] = rooms[r][c] + 1
>                 queue.append((nr, nc))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS from each gate separately: O(M×N × G) where G = number of gates — valid but far slower.
> - DFS from each gate: same O(M×N × G) issue; also won't guarantee shortest distance without revisit tracking.

---

### 01 Matrix (LC 542) `⚡ T1`

> [!example] Problem
> Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.
> The distance between two cells sharing a common edge is 1.
> 
> **Example 1:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[0,0,0]]
> Output: [[0,0,0],[0,1,0],[0,0,0]]
> ```
> 
> **Example 2:**
> ```
> Input: mat = [[0,0,0],[0,1,0],[1,1,1]]
> Output: [[0,0,0],[0,1,0],[1,2,1]]
> ```
> 
> **Constraints:**
> - m == mat.length
> - n == mat[i].length
> - 1 <= m, n <= 10^4
> - 1 <= m * n <= 10^4
> - mat[i][j] is either 0 or 1.
> - There is at least one 0 in mat.

> [!tip] Recognize · Gotcha
> **Signal:** "distance to nearest 0 for every cell" · **Gotcha:** Running BFS from every 1 is O((mn)²)

> [!info] Approach
> Multi-source BFS from all 0-cells simultaneously propagates shortest distances outward in O(M×N). The alternative (BFS from each 1-cell) is O(M²×N²). Seed queue with all 0-positions (distance 0); mark 1-cells as unvisited (distance INF); BFS expanding to unvisited neighbors with distance + 1. Initialize dist matrix with 0 for zeroes, INF for ones. Enqueue all zeroes at start. Only update a cell if current dist > neighbor dist + 1.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def update_matrix(mat):
>     rows, cols = len(mat), len(mat[0])
>     dist = [[0 if mat[r][c] == 0 else float('inf') for c in range(cols)] for r in range(rows)]
>     queue = deque((r, c) for r in range(rows) for c in range(cols) if mat[r][c] == 0)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while queue:
>         r, c = queue.popleft()
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] > dist[r][c] + 1:
>                 dist[nr][nc] = dist[r][c] + 1
>                 queue.append((nr, nc))
>     return dist
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - DP two-pass (top-left then bottom-right): O(M×N) time, O(1) extra space. Elegant but harder to reason about correctness.
> - DFS: can reach the same cell multiple times before finding minimum — not correct without full relaxation.

---

### Word Ladder `⚡ T1`

> Full walkthrough: [Word Ladder (BFS on Implicit Graph)](../algorithms/11-graph-algorithms.md#word-ladder-bfs-on-implicit-graph--t1).

---

### Find if Path Exists in a Graph `⚡ T1`

> [!example] Problem
> Given n nodes, a list of bidirectional edges, source and destination, determine if a valid path exists.

> [!tip] Recognize · Gotcha
> **Signal:** "Is there a path from source to destination?" · **Gotcha:** Union-Find: check `find(source) == find(destination)` after all union ops.

> [!info] Approach
> **Union-Find — reachability in O(E α(N)).** Union-Find answers "are they connected?" in near O(1) per query after O(E) union operations — no traversal needed. Union all edges; check if `find(source) == find(destination)`. Path compression + union by rank for optimal performance.

> [!note]- Python Solution
> ```python
> def valid_path(n, edges, source, destination):
>     parent = list(range(n))
>     rank = [0] * n
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]  # path compression
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         ra, rb = find(a), find(b)
>         if ra == rb:
>             return
>         if rank[ra] < rank[rb]:
>             ra, rb = rb, ra
>         parent[rb] = ra
>         if rank[ra] == rank[rb]:
>             rank[ra] += 1
> 
>     for a, b in edges:
>         union(a, b)
> 
>     return find(source) == find(destination)
> ```

> [!success] Complexity
> Time O(E·α(N)) ≈ O(E), Space O(N).

> [!tip] Alternatives
> - BFS/DFS: O(V+E), correct but does more work than needed for pure reachability.
> - Bidirectional BFS: useful if graph is large and path likely exists — meets in the middle.

---

### Snakes and Ladders `🎯 T2`

> [!example] Problem
> An n×n board numbered 1..n² boustrophedon-style from the bottom-left. From square s you may move to s+1..s+6; landing on a snake/ladder teleports you. Minimum dice rolls from 1 to n²?

> [!info] Approach
> Pure unweighted shortest path ⇒ BFS over squares. The entire difficulty is the **`square → (row, col)` decode**: `r, c = divmod(sq - 1, n)`, flip `c` on odd rows, and the board row is `n - 1 - r`. Write and dry-run the decode as its own helper before touching BFS — the mapping *is* the problem.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def snakesAndLadders(board):
>     n = len(board)
>     def cell(sq):
>         r, c = divmod(sq - 1, n)
>         if r % 2:
>             c = n - 1 - c
>         return n - 1 - r, c
> >
>     q, seen = deque([(1, 0)]), {1}
>     while q:
>         sq, moves = q.popleft()
>         if sq == n * n:
>             return moves
>         for nxt in range(sq + 1, min(sq + 6, n * n) + 1):
>             r, c = cell(nxt)
>             if board[r][c] != -1:
>                 nxt = board[r][c]
>             if nxt not in seen:
>                 seen.add(nxt)
>                 q.append((nxt, moves + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(n²); Space O(n²).

> [!warning] Gotcha
> Mark `seen` on the square you land on **after** the teleport, and never follow a second snake/ladder from the destination — one jump per roll.

---

### Bus Routes `🎯 T2`

> [!example] Problem
> `routes[i]` is the list of stops bus i cycles through. Minimum number of **buses** to get from stop `source` to stop `target`?

> [!tip] Recognize · Gotcha
> **Signal:** "Min buses to travel from source to target" · **Gotcha:** Build stop→bus map; BFS over buses, not stops — avoids revisiting the same bus.

> [!info] Approach
> The answer counts buses, so BFS must expand **route by route**, not stop by stop. Build `stop → routes through it`; BFS state = stop, but each expansion consumes an unvisited *route* and adds all its stops at `buses + 1`. Choosing the right node type for the graph is the entire problem — say why stops-as-nodes gives the wrong metric.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> >
> def numBusesToDestination(routes, source, target):
>     if source == target:
>         return 0
>     stop_routes = defaultdict(list)
>     for r, stops in enumerate(routes):
>         for s in stops:
>             stop_routes[s].append(r)
>     q, seen_r, seen_s = deque([(source, 0)]), set(), {source}
>     while q:
>         stop, buses = q.popleft()
>         for r in stop_routes[stop]:
>             if r in seen_r:
>                 continue
>             seen_r.add(r)
>             for s in routes[r]:
>                 if s == target:
>                     return buses + 1
>                 if s not in seen_s:
>                     seen_s.add(s)
>                     q.append((s, buses + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(total stops across routes); Space same.

> [!warning] Gotcha
> Two visited sets — routes **and** stops. Skipping either one turns the BFS quadratic on adversarial inputs.

---

### Word Ladder II `⚡ T1`

> Full walkthrough: [Word Ladder II (All Shortest Transformation Sequences)](../algorithms/11-graph-algorithms.md#word-ladder-ii-all-shortest-transformation-sequences--t1).

**Also try:**

- **Employee Importance** — Hash map + BFS over subordinate ids
- **Find Center of Star Graph** — O(1) — center appears in both the first and second edges

---

## DFS on Graphs

---

### Flood Fill `⚡ T1`

> [!example] Problem
> You are given an image represented by an m x n grid of integers image, where image[i][j] represents the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to perform a flood fill on the image starting from the pixel image[sr][sc].
> To perform a flood fill:
> Return the modified image after performing the flood fill.
> 
> **Example 1:**
> ```
> Input: image = [[1,1,1],[1,1,0],[1,0,1]], sr = 1, sc = 1, color = 2
> Output: [[2,2,2],[2,2,0],[2,0,1]]
> Explanation:
> 
> From the center of the image with position (sr, sc) = (1, 1) (i.e., the red pixel), all pixels connected by a path of the same color as the starting pixel (i.e., the blue pixels) are colored with the new color.
> Note the bottom corner is not colored 2, because it is not horizontally or vertically connected to the starting pixel.
> ```
> 
> **Example 2:**
> ```
> Input: image = [[0,0,0],[0,0,0]], sr = 0, sc = 0, color = 0
> Output: [[0,0,0],[0,0,0]]
> Explanation:
> The starting pixel is already colored with 0, which is the same as the target color. Therefore, no changes are made to the image.
> ```
> 
> **Constraints:**
> - m == image.length
> - n == image[i].length
> - 1 <= m, n <= 50
> - 0 <= image[i][j], color < 216
> - 0 <= sr < m
> - 0 <= sc < n

> [!tip] Recognize · Gotcha
> **Signal:** "Recolor connected region" · **Gotcha:** Skip if `newColor == oldColor` — avoids infinite loop.

> [!info] Approach
> **DFS recolor — guard against same-color infinite loop.** Connected-component traversal. Early return if original == new color: recursion would infinitely revisit cells (no termination condition). DFS from (sr, sc); recolor cells matching the original color. Guard with `if original == color: return image` before DFS.

> [!note]- Python Solution
> ```python
> def flood_fill(image, sr, sc, color):
>     original = image[sr][sc]
>     if original == color:
>         return image
>     rows, cols = len(image), len(image[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or image[r][c] != original:
>             return
>         image[r][c] = color
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     dfs(sr, sc)
>     return image
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS with deque: iterative, avoids recursion depth issues on large images.
> - Separate `visited` set instead of in-place mutation: same complexity but extra O(M×N) space.

---

### Max Area of Island `⚡ T1`

> [!example] Problem
> You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.
> The area of an island is the number of cells with a value 1 in the island.
> Return the maximum area of an island in grid. If there is no island, return 0.
> 
> **Example 1:**
> ```
> Input: grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
> Output: 6
> Explanation: The answer is not 11, because the island must be connected 4-directionally.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,0,0,0,0,0,0,0]]
> Output: 0
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 50
> - grid[i][j] is either 0 or 1.

> [!tip] Recognize · Gotcha
> **Signal:** Largest blob · **Gotcha:** Mark visited BEFORE recursing

> [!info] Approach
> **DFS returning component size — sink inline.** Variation on Number of Islands where we need the maximum component size. DFS function returns the count of cells in the component instead of just marking. `1 + sum of returns from 4 neighbors`. Sink cells inline; DFS returns 0 for non-land or out-of-bounds. `max(dfs(r,c) for all r,c)` — zero-cost for water cells.

> [!note]- Python Solution
> ```python
> def max_area_of_island(grid):
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
>             return 0
>         grid[r][c] = 0
>         return 1 + dfs(r+1,c) + dfs(r-1,c) + dfs(r,c+1) + dfs(r,c-1)
> 
>     return max(dfs(r, c) for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - BFS: count cells as dequeued. Same complexity.
> - Union-Find with size tracking: O(M×N·α); useful for dynamic grid updates.

---

### Surrounded Regions `⚡ T1`

> [!example] Problem
> You are given an m x n matrix board containing letters 'X' and 'O', capture regions that are surrounded:
> To capture a surrounded region, replace all 'O's with 'X's in-place within the original board. You do not need to return anything.
> 
> **Example 1:**
> ```
> Input: board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]
> Output: [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]
> Explanation:
> In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.
> ```
> 
> **Example 2:**
> ```
> Input: board = [["X"]]
> Output: [["X"]]
> ```
> 
> **Constraints:**
> - m == board.length
> - n == board[i].length
> - 1 <= m, n <= 200
> - board[i][j] is 'X' or 'O'.

> [!tip] Recognize · Gotcha
> **Signal:** "Flip interior isolated regions" · **Gotcha:** Don't BFS from every interior `O` — O(R²C²) vs O(RC) from borders.

> [!info] Approach
> **Reverse DFS — mark border-safe 'O's, then flip interior.** Directly checking if an 'O' region is surrounded requires backtracking to undo if DFS touches a border. Instead: find all border-connected 'O's first (safe cells), then flip everything else. DFS from every border 'O', mark safe cells with sentinel 'S'. Then: interior 'O' → 'X', 'S' → 'O'. Walk all 4 borders, DFS from each 'O' found there.

> [!note]- Python Solution
> ```python
> def solve(board):
>     if not board:
>         return
>     rows, cols = len(board), len(board[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != 'O':
>             return
>         board[r][c] = 'S'
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0)
>         dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c)
>         dfs(rows-1, c)
> 
>     for r in range(rows):
>         for c in range(cols):
>             if board[r][c] == 'O':   board[r][c] = 'X'
>             elif board[r][c] == 'S': board[r][c] = 'O'
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS from borders: iterative, avoids recursion stack overflow.
> - Union-Find with virtual border node: union all 'O's; any component containing the border node is safe. Elegant but more code.

---

### Pacific Atlantic Water Flow `⚡ T1`

> [!example] Problem
> There is an m x n rectangular island that borders both the Pacific Ocean and Atlantic Ocean. The Pacific Ocean touches the island's left and top edges, and the Atlantic Ocean touches the island's right and bottom edges.
> The island is partitioned into a grid of square cells. You are given an m x n integer matrix heights where heights[r][c] represents the height above sea level of the cell at coordinate (r, c).
> The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is less than or equal to the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.
> Return a 2D list of grid coordinates result where result[i] = [ri, ci] denotes that rain water can flow from cell (ri, ci) to both the Pacific and Atlantic oceans.
> 
> **Example 1:**
> ```
> Input: heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
> Output: [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
> Explanation: The following cells can flow to the Pacific and Atlantic oceans, as shown below:
> [0,4]: [0,4] -> Pacific Ocean 
>        [0,4] -> Atlantic Ocean
> [1,3]: [1,3] -> [0,3] -> Pacific Ocean 
>        [1,3] -> [1,4] -> Atlantic Ocean
> [1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
>        [1,4] -> Atlantic Ocean
> [2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
>        [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
> [3,0]: [3,0] -> Pacific Ocean 
>        [3,0] -> [4,0] -> Atlantic Ocean
> [3,1]: [3,1] -> [3,0] -> Pacific Ocean 
>        [3,1] -> [4,1] -> Atlantic Ocean
> [4,0]: [4,0] -> Pacific Ocean 
>        [4,0] -> Atlantic Ocean
> Note that there are other possible paths for these cells to flow to the Pacific and Atlantic oceans.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [[1]]
> Output: [[0,0]]
> Explanation: The water can flow from the only cell to the Pacific and Atlantic oceans.
> ```
> 
> **Constraints:**
> - m == heights.length
> - n == heights[r].length
> - 1 <= m, n <= 200
> - 0 <= heights[r][c] <= 10^5

> [!tip] Recognize · Gotcha
> **Signal:** "can reach both borders" · **Gotcha:** Searching downhill from every cell is O((mn)²)

> [!info] Approach
> **Reverse BFS from both ocean borders — intersect reachable sets.** Checking forward from each cell whether it reaches both oceans requires O(M²N²) DFS calls. Reverse: "which cells can be reached from the ocean borders?" — water flows uphill in reverse. BFS from all Pacific border cells (mark reachable); BFS from all Atlantic border cells; intersect. Reverse BFS condition — expand to neighbors with height >= current height (uphill in the reverse direction).

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def pacific_atlantic(heights):
>     rows, cols = len(heights), len(heights[0])
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     def bfs(starts):
>         visited = set(starts)
>         queue = deque(starts)
>         while queue:
>             r, c = queue.popleft()
>             for dr, dc in dirs:
>                 nr, nc = r+dr, c+dc
>                 if (0 <= nr < rows and 0 <= nc < cols
>                         and (nr, nc) not in visited
>                         and heights[nr][nc] >= heights[r][c]):
>                     visited.add((nr, nc))
>                     queue.append((nr, nc))
>         return visited
> 
>     pacific  = bfs([(r, 0) for r in range(rows)] + [(0, c) for c in range(cols)])
>     atlantic = bfs([(r, cols-1) for r in range(rows)] + [(rows-1, c) for c in range(cols)])
>     return [[r, c] for r, c in pacific & atlantic]
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N).

> [!tip] Alternatives
> - DFS from borders: same logic, recursive. Watch recursion depth on large grids.
> - Forward DFS with memoization per cell: O(M×N) with full memoization but harder to implement correctly.

---

### All Paths From Source to Target `⚡ T1`

> [!example] Problem
> Given a directed acyclic graph (DAG) of n nodes labeled from 0 to n - 1, find all possible paths from node 0 to node n - 1 and return them in any order.
> The graph is given as follows: graph[i] is a list of all nodes you can visit from node i (i.e., there is a directed edge from node i to node graph[i][j]).
> 
> **Example 1:**
> ```
> Input: graph = [[1,2],[3],[3],[]]
> Output: [[0,1,3],[0,2,3]]
> Explanation: There are two paths: 0 -> 1 -> 3 and 0 -> 2 -> 3.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[4,3,1],[3,2,4],[3],[4],[]]
> Output: [[0,4],[0,3,4],[0,1,3,4],[0,1,2,3,4],[0,1,4]]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 2 <= n <= 15
> - 0 <= graph[i][j] < n
> - graph[i][j] != i (i.e., there will be no self-loops).
> - All the elements of graph[i] are unique.
> - The input graph is guaranteed to be a DAG.

> [!tip] Recognize · Gotcha
> **Signal:** "All paths in DAG from 0 to n-1" · **Gotcha:** No cycle → no need for visited set; append path on reaching target.

> [!info] Approach
> **DFS backtracking on DAG — no visited set needed.** It's a DAG — no cycles, so DFS can never revisit a node on the current path. No visited set needed. DFS with backtracking — enumerate all paths. When node n-1 is reached, record a copy of the current path. `path.append(nei)`, recurse, `path.pop()`.

> [!note]- Python Solution
> ```python
> def all_paths_source_target(graph):
>     target = len(graph) - 1
>     result = []
> 
>     def dfs(node, path):
>         if node == target:
>             result.append(list(path))
>             return
>         for nei in graph[node]:
>             path.append(nei)
>             dfs(nei, path)
>             path.pop()
> 
>     dfs(0, [0])
>     return result
> ```

> [!success] Complexity
> Time O(2^V × V) worst case (exponential paths). Space O(V) recursion depth + O(2^V × V) output.

> [!tip] Alternatives
> - BFS with path tracking: store `(node, path)` in queue. More memory (all partial paths in queue simultaneously).
> - Memoization: cache paths from each node to target. Reduces redundant computation when paths converge.

---

### Number of Provinces (LC 547) `⚡ T1`

> Full walkthrough: [Number of Provinces (Matrix Form)](../algorithms/10-union-find.md#number-of-provinces-matrix-form--t1).

---

### Number of Enclaves (LC 1020) `⚡ T1`

> [!example] Problem
> You are given an m x n binary matrix grid, where 0 represents a sea cell and 1 represents a land cell.
> A move consists of walking from one land cell to another adjacent (4-directionally) land cell or walking off the boundary of the grid.
> Return the number of land cells in grid for which we cannot walk off the boundary of the grid in any number of moves.
> 
> **Example 1:**
> ```
> Input: grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
> Output: 3
> Explanation: There are three 1s that are enclosed by 0s, and one 1 that is not enclosed because its on the boundary.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,1,1,0],[0,0,1,0],[0,0,1,0],[0,0,0,0]]
> Output: 0
> Explanation: All 1s are either on the boundary or can reach the boundary.
> ```
> 
> **Constraints:**
> - m == grid.length
> - n == grid[i].length
> - 1 <= m, n <= 500
> - grid[i][j] is either 0 or 1.

> [!info] Approach
> Any land cell connected to the border can reach the sea — it is NOT an enclave. Mirror of Surrounded Regions: mark all border-reachable land, then count remaining interior land. DFS/BFS from every border land cell, mark visited. Count unvisited land cells in the interior. Walk all 4 borders; DFS from each '1' encountered, sinking to 0. After traversal, sum remaining 1-cells.

> [!note]- Python Solution
> ```python
> def num_enclaves(grid):
>     rows, cols = len(grid), len(grid[0])
> 
>     def dfs(r, c):
>         if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
>             return
>         grid[r][c] = 0
>         dfs(r+1, c)
>         dfs(r-1, c)
>         dfs(r, c+1)
>         dfs(r, c-1)
> 
>     for r in range(rows):
>         dfs(r, 0)
>         dfs(r, cols-1)
>     for c in range(cols):
>         dfs(0, c)
>         dfs(rows-1, c)
> 
>     return sum(grid[r][c] for r in range(rows) for c in range(cols))
> ```

> [!success] Complexity
> Time O(M×N), Space O(M×N) recursion stack.

> [!tip] Alternatives
> - BFS from borders: iterative, avoids recursion stack overflow on large grids.
> - Union-Find with virtual border node: union all land cells; union border land with a sentinel; count non-sentinel roots. Same complexity, more code.

---

### Clone Graph `⚡ T1`

> [!example] Problem
> Given a reference of a node in a connected undirected graph.
> Return a deep copy (clone) of the graph.
> Each node in the graph contains a value (int) and a list (List[Node]) of its neighbors.
> Test case format:
> For simplicity, each node's value is the same as the node's index (1-indexed). For example, the first node with val == 1, the second node with val == 2, and so on. The graph is represented in the test case using an adjacency list.
> An adjacency list is a collection of unordered lists used to represent a finite graph. Each list describes the set of neighbors of a node in the graph.
> The given node will always be the first node with val = 1. You must return the copy of the given node as a reference to the cloned graph.
> 
> **Example 1:**
> ```
> class Node {
>     public int val;
>     public List neighbors;
> }
> ```
> 
> **Example 2:**
> ```
> Input: adjList = [[2,4],[1,3],[2,4],[1,3]]
> Output: [[2,4],[1,3],[2,4],[1,3]]
> Explanation: There are 4 nodes in the graph.
> 1st node (val = 1)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 2nd node (val = 2)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> 3rd node (val = 3)'s neighbors are 2nd node (val = 2) and 4th node (val = 4).
> 4th node (val = 4)'s neighbors are 1st node (val = 1) and 3rd node (val = 3).
> ```
> 
> **Example 3:**
> ```
> Input: adjList = [[]]
> Output: [[]]
> Explanation: Note that the input contains one empty list. The graph consists of only one node with val = 1 and it does not have any neighbors.
> ```
> 
> **Example 4:**
> ```
> Input: adjList = []
> Output: []
> Explanation: This an empty graph, it does not have any nodes.
> ```
> 
> **Constraints:**
> - The number of nodes in the graph is in the range [0, 100].
> - 1 <= Node.val <= 100
> - Node.val is unique for each node.
> - There are no repeated edges and no self-loops in the graph.
> - The Graph is connected and all nodes can be visited starting from the given node.

> [!tip] Recognize · Gotcha
> **Signal:** "Deep copy graph with cycles" · **Gotcha:** Cycles require the map before recursion — avoids infinite loop.

> [!info] Approach
> **DFS with original→clone map — register before recursing.** Without pre-registration, revisiting a node (via a cycle) creates a new clone instead of returning the existing one — producing duplicates and infinite loops. `{original: clone}` map as memo; DFS from start. Create clone, register in map, then recurse to clone neighbors. Guard `if n in visited: return visited[n]` handles cycles. Register BEFORE recursing into neighbors.

> [!note]- Python Solution
> ```python
> def clone_graph(node):
>     if not node:
>         return None
>     visited = {}
> 
>     def dfs(n):
>         if n in visited:
>             return visited[n]
>         clone = Node(n.val)
>         visited[n] = clone  # register BEFORE recursing — critical for cycle safety
>         for nei in n.neighbors:
>             clone.neighbors.append(dfs(nei))
>         return clone
> 
>     return dfs(node)
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - BFS: use queue; same `visited` map; iterative. O(V+E)/O(V).
> - Two-pass: create all clones (V pass), then wire neighbors (E pass). Cleaner separation, same complexity.

---

### Find Eventual Safe States `⚡ T1`

> Full walkthrough: [Find Eventual Safe States (Reverse Graph / Kahn's)](../algorithms/11-graph-algorithms.md#find-eventual-safe-states-reverse-graph--kahns--t1).

---

## Topological Sort

---

### Course Schedule II `⚡ T1`

> [!example] Problem
> There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
> Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.
> 
> **Example 1:**
> ```
> Input: numCourses = 2, prerequisites = [[1,0]]
> Output: [0,1]
> Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
> ```
> 
> **Example 2:**
> ```
> Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
> Output: [0,2,1,3]
> Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
> So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
> ```
> 
> **Example 3:**
> ```
> Input: numCourses = 1, prerequisites = []
> Output: [0]
> ```
> 
> **Constraints:**
> - 1 <= numCourses <= 2000
> - 0 <= prerequisites.length <= numCourses * (numCourses - 1)
> - prerequisites[i].length == 2
> - 0 <= ai, bi < numCourses
> - ai != bi
> - All the pairs [ai, bi] are distinct.

> [!tip] Recognize · Gotcha
> **Signal:** "return an order" · **Gotcha:** Reverse the post-order at the end

> [!info] Approach
> **Kahn's topo sort — collect removal order.** Kahn's algorithm naturally produces a topological order — the BFS order of removal. Same algorithm as Course Schedule; collect nodes as they're removed. If `len(order) == numCourses`, it's valid; otherwise a cycle was detected. Append node to `order` as it's dequeued; return order or [].

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def find_order(numCourses, prerequisites):
>     graph = [[] for _ in range(numCourses)]
>     indegree = [0] * numCourses
>     for a, b in prerequisites:
>         graph[b].append(a)
>         indegree[a] += 1
> 
>     queue = deque(c for c in range(numCourses) if indegree[c] == 0)
>     order = []
>     while queue:
>         node = queue.popleft()
>         order.append(node)
>         for nei in graph[node]:
>             indegree[nei] -= 1
>             if indegree[nei] == 0:
>                 queue.append(nei)
> 
>     return order if len(order) == numCourses else []
> ```

> [!success] Complexity
> Time O(V+E), Space O(V+E).

> [!tip] Alternatives
> - DFS post-order: append node after all successors processed; reverse at end. O(V+E). Multiple valid orderings are possible — both Kahn's and DFS may give different correct answers.
> - Edge direction gotcha: for "a requires b", edge is `b → a` (b must come before a), not `a → b`.

---

### Minimum Number of Vertices to Reach All Nodes `⚡ T1`

> [!example] Problem
> Given a directed acyclic graph, with n vertices numbered from 0 to n-1, and an array edges where edges[i] = [fromi, toi] represents a directed edge from node fromi to node toi.
> Find the smallest set of vertices from which all nodes in the graph are reachable. It's guaranteed that a unique solution exists.
> Notice that you can return the vertices in any order.
> 
> **Example 1:**
> ```
> Input: n = 6, edges = [[0,1],[0,2],[2,5],[3,4],[4,2]]
> Output: [0,3]
> Explanation: It's not possible to reach all the nodes from a single vertex. From 0 we can reach [0,1,2,5]. From 3 we can reach [3,4,2,5]. So we output [0,3].
> ```
> 
> **Example 2:**
> ```
> Input: n = 5, edges = [[0,1],[2,1],[3,1],[1,4],[2,4]]
> Output: [0,2,3]
> Explanation: Notice that vertices 0, 3 and 2 are not reachable from any other node, so we must include them. Also any of these vertices can reach nodes 1 and 4.
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^5
> - 1 <= edges.length <= min(10^5, n * (n - 1) / 2)
> - edges[i].length == 2
> - 0 <= fromi, toi < n
> - All pairs (fromi, toi) are distinct.

> [!tip] Recognize · Gotcha
> **Signal:** "In DAG, find nodes with no incoming edges" · **Gotcha:** Any node reachable from another has in-degree ≥ 1 — not a required start.

> [!info] Approach
> **Nodes with in-degree 0 — the only possible starting set.** Any node with an incoming edge is reachable from its predecessor — it doesn't need to be in the starting set. A node with in-degree 0 cannot be reached from any other node, so it must be in the starting set. The answer is exactly the set of nodes with in-degree 0. Collect all destination nodes from edges — these have in-degree ≥ 1; return all nodes not in this set.

> [!note]- Python Solution
> ```python
> def find_smallest_set_of_vertices(n, edges):
>     has_incoming = set(v for _, v in edges)
>     return [i for i in range(n) if i not in has_incoming]
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - In-degree array: equivalent; compute `indegree[i]`, return nodes where it's 0.
> - Note: works only for DAGs. For general directed graphs, minimum vertex cover is NP-hard.

---

### Longest Path in a DAG `⚡ T1`

> [!example] Problem
> Find the length of the longest path in a directed acyclic graph (in terms of number of edges).

> [!info] Approach
> **Kahn's topo sort + DP — relax dp[v] = max(dp[u] + 1).** Only works on DAGs — cycles make the longest path undefined (infinite). Topological sort + DP: process nodes in topological order; `dp[node] = max(dp[predecessor] + 1)` for all incoming edges — no subproblem is accessed before it's solved. Kahn's to get topo order, then one DP pass. `dp[node] = max(dp[node], dp[prev] + 1)` as edges are relaxed during Kahn's.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def longest_path_dag(n, edges):
>     # edges: list of (u, v), directed u → v
>     graph   = [[] for _ in range(n)]
>     indegree = [0] * n
>     for u, v in edges:
>         graph[u].append(v)
>         indegree[v] += 1
> 
>     queue = deque(i for i in range(n) if indegree[i] == 0)
>     dp = [0] * n  # dp[node] = longest path ending at node
> 
>     while queue:
>         u = queue.popleft()
>         for v in graph[u]:
>             dp[v] = max(dp[v], dp[u] + 1)
>             indegree[v] -= 1
>             if indegree[v] == 0:
>                 queue.append(v)
> 
>     return max(dp)
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - DFS with memo dict on node — top-down. O(V+E). Same idea, you just say the cache out loud.
> - Bellman-Ford with negated weights: O(VE) — much slower; use only when you can't confirm DAG property.

**Also try:**

- **Minimum Height Trees (LC 310)** — The roots of minimum height trees are the "center" nodes of the tree — at most 2 nodes lying on the longest path (diameter)

---

## Shortest Path / Weighted

---

### Swim in Rising Water `⚡ T1`

> [!example] Problem
> You are given an n x n integer matrix grid where each value grid[i][j] represents the elevation at that point (i, j).
> It starts raining, and water gradually rises over time. At time t, the water level is t, meaning any cell with elevation less than equal to t is submerged or reachable.
> You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most t. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.
> Return the minimum time until you can reach the bottom right square (n - 1, n - 1) if you start at the top left square (0, 0).
> 
> **Example 1:**
> ```
> Input: grid = [[0,2],[1,3]]
> Output: 3
> Explanation:
> At time 0, you are in grid location (0, 0).
> You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
> You cannot reach point (1, 1) until time 3.
> When the depth of water is 3, we can swim anywhere inside the grid.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
> Output: 16
> Explanation: The final route is shown.
> We need to wait until time 16 so that (0, 0) and (4, 4) are connected.
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 50
> - 0 <= grid[i][j] < n2
> - Each value grid[i][j] is unique.

> [!tip] Recognize · Gotcha
> **Signal:** "Min time to reach bottom-right as water rises" · **Gotcha:** Dijkstra approach: `dist[r][c]` = min max-elevation path to `(r,c)`.

> [!info] Approach
> **Modified Dijkstra — minimize maximum edge weight (bottleneck path).** Minimize the maximum edge weight on any path → modified Dijkstra. `dist[r][c]` = minimum possible max-elevation to reach (r,c). Min-heap of `(max_elevation_so_far, r, c)`. Cost to reach neighbor = `max(dist[curr], grid[nr][nc])`. The first time we reach (n-1,n-1), we have the answer.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def swim_in_water(grid):
>     n = len(grid)
>     dist = [[float('inf')] * n for _ in range(n)]
>     dist[0][0] = grid[0][0]
>     heap = [(grid[0][0], 0, 0)]
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while heap:
>         t, r, c = heapq.heappop(heap)
>         if r == n-1 and c == n-1:
>             return t
>         if t > dist[r][c]:
>             continue
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < n and 0 <= nc < n:
>                 new_t = max(t, grid[nr][nc])
>                 if new_t < dist[nr][nc]:
>                     dist[nr][nc] = new_t
>                     heapq.heappush(heap, (new_t, nr, nc))
> 
>     return dist[n-1][n-1]
> ```

> [!success] Complexity
> Time O(n² log n), Space O(n²).

> [!tip] Alternatives
> - Binary search on answer T + BFS feasibility check: O(n² log n) total. Binary search over T ∈ [0, n²-1]; for each T, BFS if path exists using only cells ≤ T.
> - Union-Find with sorted cells: sort all cells by elevation; union adjacent cells as elevation rises; stop when (0,0) and (n-1,n-1) are connected. O(n² log n).

---

### Path with Minimum Effort (LC 1631) `⚡ T1`

> [!example] Problem
> You are a hiker preparing for an upcoming hike. You are given heights, a 2D array of size rows x columns, where heights[row][col] represents the height of cell (row, col). You are situated in the top-left cell, (0, 0), and you hope to travel to the bottom-right cell, (rows-1, columns-1) (i.e., 0-indexed). You can move up, down, left, or right, and you wish to find a route that requires the minimum effort.
> A route's effort is the maximum absolute difference in heights between two consecutive cells of the route.
> Return the minimum effort required to travel from the top-left cell to the bottom-right cell.
> 
> **Example 1:**
> ```
> Input: heights = [[1,2,2],[3,8,2],[5,3,5]]
> Output: 2
> Explanation: The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
> This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [[1,2,3],[3,8,4],[5,3,5]]
> Output: 1
> Explanation: The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].
> ```
> 
> **Example 3:**
> ```
> Input: heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
> Output: 0
> Explanation: This route does not require any effort.
> ```
> 
> **Constraints:**
> - rows == heights.length
> - columns == heights[i].length
> - 1 <= rows, columns <= 100
> - 1 <= heights[i][j] <= 10^6

> [!info] Approach
> Minimize the maximum edge weight on a path = bottleneck shortest path. Modified Dijkstra: `dist[r][c]` = minimum possible max-absolute-diff to reach (r,c); greedily process cells in order of current effort. Min-heap of `(effort, r, c)`. Transition: `new_effort = max(current_effort, abs(heights[nr][nc] - heights[r][c]))`. First pop of (rows-1, cols-1) from the heap is the answer. Mark visited on pop to avoid reprocessing.

> [!note]- Python Solution
> ```python
> import heapq
> 
> def minimum_effort_path(heights):
>     rows, cols = len(heights), len(heights[0])
>     dist = [[float('inf')] * cols for _ in range(rows)]
>     dist[0][0] = 0
>     heap = [(0, 0, 0)]  # (effort, r, c)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     while heap:
>         effort, r, c = heapq.heappop(heap)
>         if r == rows-1 and c == cols-1:
>             return effort
>         if effort > dist[r][c]:
>             continue
>         for dr, dc in dirs:
>             nr, nc = r+dr, c+dc
>             if 0 <= nr < rows and 0 <= nc < cols:
>                 new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
>                 if new_effort < dist[nr][nc]:
>                     dist[nr][nc] = new_effort
>                     heapq.heappush(heap, (new_effort, nr, nc))
> 
>     return dist[rows-1][cols-1]
> ```

> [!success] Complexity
> Time O(M×N log(M×N)), Space O(M×N).

> [!tip] Alternatives
> - Binary search on effort + BFS feasibility: O(M×N log(max_height)). Binary search on answer ∈ [0, 10^6]; BFS checks if path exists using only edges with diff ≤ mid.
> - Union-Find with sorted edges: sort all edges by absolute diff; union endpoints one by one; stop when (0,0) and (M-1,N-1) are connected. O(M×N log(M×N)).

**Also try:**

- **Network Delay Time (Dijkstra's)** — see [Network Delay Time](../algorithms/11-graph-algorithms.md#dijkstras-algorithm)
- **Shortest Path in a DAG** — In a DAG, a topological order guarantees that when a node is processed, all incoming dependencies are already finalized

---

## Bipartite / Coloring

---

### Is Graph Bipartite? `⚡ T1`

> [!example] Problem
> There is an undirected graph with n nodes, where each node is numbered between 0 and n - 1. You are given a 2D array graph, where graph[u] is an array of nodes that node u is adjacent to. More formally, for each v in graph[u], there is an undirected edge between node u and node v. The graph has the following properties:
> A graph is bipartite if the nodes can be partitioned into two independent sets A and B such that every edge in the graph connects a node in set A and a node in set B.
> Return true if and only if it is bipartite.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2,3],[0,2],[0,1,3],[0,2]]
> Output: false
> Explanation: There is no way to partition the nodes into two independent sets such that every edge connects a node in one and a node in the other.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1,3],[0,2],[1,3],[0,2]]
> Output: true
> Explanation: We can partition the nodes into two sets: {0, 2} and {1, 3}.
> ```
> 
> **Constraints:**
> - graph.length == n
> - 1 <= n <= 100
> - 0 <= graph[u].length < n
> - 0 <= graph[u][i] <= n - 1
> - graph[u] does not contain u.
> - All the values of graph[u] are unique.
> - If graph[u] contains v, then graph[v] contains u.

> [!tip] Recognize · Gotcha
> **Signal:** "2-color graph with no monochromatic edge" · **Gotcha:** Disconnected graph: run BFS/DFS from every unvisited node.

> [!info] Approach
> **BFS 2-coloring — alternating colors, fail on same-color neighbor.** A graph is bipartite iff it contains no odd-length cycle — equivalent to being 2-colorable. BFS/DFS assigning alternating colors (0/1); if any neighbor has the same color as the current node, not bipartite. Must handle disconnected components — run BFS/DFS from every unvisited node. Initialize all colors to -1 (uncolored). For each unvisited node, BFS assigning color 0; assign `1 - color[node]` to unvisited neighbors; return False if neighbor has same color.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def is_bipartite(graph):
>     n = len(graph)
>     color = [-1] * n
> 
>     for start in range(n):
>         if color[start] != -1:
>             continue
>         queue = deque([start])
>         color[start] = 0
>         while queue:
>             node = queue.popleft()
>             for nei in graph[node]:
>                 if color[nei] == -1:
>                     color[nei] = 1 - color[node]
>                     queue.append(nei)
>                 elif color[nei] == color[node]:
>                     return False
> 
>     return True
> ```

> [!success] Complexity
> Time O(V+E), Space O(V).

> [!tip] Alternatives
> - DFS coloring: same logic recursively. O(V+E). Stack overflow risk on deep graphs.
> - Odd-cycle detection: explicitly find cycles and check parity. Equivalent, more complex.

**Also try:**

- **Possible Bipartition (LC 886)** — see [Possible Bipartition](../algorithms/11-graph-algorithms.md#multi-source-bfs--special-bfs)

---

## Advanced

---

### Redundant Connection `⚡ T1`

> [!example] Problem
> In this problem, a tree is an undirected graph that is connected and has no cycles.
> You are given a graph that started as a tree with n nodes labeled from 1 to n, with one additional edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed. The graph is represented as an array edges of length n where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the graph.
> Return an edge that can be removed so that the resulting graph is a tree of n nodes. If there are multiple answers, return the answer that occurs last in the input.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[1,3],[2,3]]
> Output: [2,3]
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
> Output: [1,4]
> ```
> 
> **Constraints:**
> - n == edges.length
> - 3 <= n <= 1000
> - edges[i].length == 2
> - 1 <= ai < bi <= edges.length
> - ai != bi
> - There are no repeated edges.
> - The given graph is connected.

> [!tip] Recognize · Gotcha
> **Signal:** "Edge creating cycle in undirected graph" · **Gotcha:** If multiple redundant edges exist, return the last one (rightmost in input).

> [!info] Approach
> **Union-Find — first edge connecting already-connected nodes is redundant.** Adding one edge to a tree creates exactly one cycle. Process edges in order; if both endpoints share the same root (`find(u) == find(v)`), they're already connected — this edge creates a cycle and is redundant. Union by rank + path compression; return immediately on first cycle-forming edge. For each edge (a, b): if `union(a, b)` returns False (same component), return [a, b].

> [!note]- Python Solution
> ```python
> def find_redundant_connection(edges):
>     parent = list(range(len(edges) + 1))
>     rank   = [0] * (len(edges) + 1)
> 
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> 
>     def union(a, b):
>         ra, rb = find(a), find(b)
>         if ra == rb:
>             return False
>         if rank[ra] < rank[rb]:
>             ra, rb = rb, ra
>         parent[rb] = ra
>         if rank[ra] == rank[rb]:
>             rank[ra] += 1
>         return True
> 
>     for a, b in edges:
>         if not union(a, b):
>             return [a, b]
>     return []
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> - DFS cycle detection: for each edge, DFS to check if path already exists between endpoints. O(N²) — inefficient.
> - Note: Union-Find only correct here because the graph is undirected. For directed graphs, DFS back-edge detection or Kahn's is required.

**Also try:**

- **Minimum Spanning Tree (Kruskal's)** — Kruskal's — sort edges by weight, greedily add if no cycle. `⚡ T1`
- **Reconstruct Itinerary (LC 332)** — see [Reconstruct Itinerary (Hierholzer's)](../algorithms/11-graph-algorithms.md#eulerian-path)
- **Minimum Spanning Tree — Prim's Algorithm** — Prim's grows the MST greedily from any starting node, always adding the cheapest edge that connects the current MST to an unvisited node
- **All-Pairs Shortest Path — Floyd-Warshall** — Dijkstra's is per-source (O(V * E log V) total for all-pairs)

---

## See Also

[[union-find]] | [[binary-search]] | [[dynamic-programming]] | [[sorting]]
