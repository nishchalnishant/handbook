# Graph — Amazon SDE-2 Reference

---

## ⚡ Cheat Sheet (Quick Revision)

**3 questions to ask before writing any graph code:**
1. What am I looking for? → picks the algorithm
2. Directed or undirected? Weighted or unweighted? → changes the template
3. Could the graph be disconnected? → if yes, outer loop over all nodes

| Goal | Algorithm | Key detail |
|------|-----------|-----------|
| Shortest path, unweighted | BFS | mark visited on **enqueue** not dequeue |
| Shortest path, weighted (≥0) | Dijkstra | `if d > dist[u]: continue` for stale entries |
| Shortest path, negative weights | Bellman-Ford | copy dist each round, N-1 iterations |
| Connectivity / components | DFS + outer loop | count how many times outer loop fires |
| Ordering with dependencies | Topological Sort (Kahn's) | `len(order) != n` → cycle exists |
| Cycle in directed graph | 3-state DFS (0/1/2) | state 1 = "on current stack" |
| Cycle in undirected graph | DFS + parent tracking | `nei != parent` check |
| 2-colorable (bipartite) | BFS, flip colors | contradiction = not bipartite |
| Closest source distance | Multi-source BFS | seed all sources at distance 0 |
| "Can X reach Y?" cheaply | Reverse BFS/DFS from Y | run backwards, follow edges in reverse |

**BFS template (mark on enqueue):**
```python
visited = {start}; queue = deque([start])
while queue:
    node = queue.popleft()
    for nei in graph[node]:
        if nei not in visited:
            visited.add(nei); queue.append(nei)
```

**DFS components (outer loop mandatory for disconnected graphs):**
```python
for i in range(n):
    if i not in visited:
        visited.add(i); dfs(i); count += 1
```

**Topo sort — Kahn's (default for interviews):**
```python
queue = deque(i for i in range(n) if indegree[i] == 0)
while queue:
    node = queue.popleft(); order.append(node)
    for nei in graph[node]:
        indegree[nei] -= 1
        if indegree[nei] == 0: queue.append(nei)
return order if len(order) == n else []  # [] = cycle
```

**Dijkstra (stale check is mandatory):**
```python
dist[src] = 0; pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue       # ← never skip this
    for v, w in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w; heapq.heappush(pq, (dist[v], v))
```

**Cycle detection — directed (3 states):**
```python
# state: 0=unvisited, 1=in current path, 2=done
if state[node] == 1: return True   # cycle
if state[node] == 2: return False  # safe
```

**Common mistakes:**
- Forgetting outer loop → only visits one component
- Marking visited on dequeue → duplicate processing, wrong distances
- Using parent-tracking for directed graphs → wrong (use 3-state instead)
- Skipping `if d > dist[u]: continue` in Dijkstra → corrupted distances
- Not checking `len(order) == n` in topo sort → silently misses cycle

---

## How to Think About Graphs

Before touching code, ask three questions:

1. **What am I looking for?** Shortest path → BFS/Dijkstra. Reachability/grouping → DFS. Order with dependencies → Topo sort.
2. **What does an edge mean?** Directed (one-way) vs undirected (two-way). Weighted vs unweighted.
3. **Are there disconnected parts?** If yes, you need an outer loop over all nodes, not just one start node.

These three questions determine 90% of the structure before you write a line.

---

## Representations

**Why adjacency list?** For most interview problems, edges are sparse — a node connects to a few neighbors, not all n nodes. Adjacency list is O(V+E) space; adjacency matrix is O(V²). Use a matrix only when the input *gives* you one (LC 547, LC 924).

```python
from collections import defaultdict
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)
    graph[v].append(u)   # omit for directed graphs
```

`defaultdict(list)` means you never have to check "does this key exist" — accessing a missing node just returns `[]`, which is safe to iterate.

**Grid graph** — the grid IS the graph; neighbors are the 4 adjacent cells. No explicit adjacency list needed.

```python
dirs = [(0,1),(0,-1),(1,0),(-1,0)]
```

---

## BFS — Shortest Path / Level Order

**The mental model:** BFS explores in rings. Round 1 = all nodes 1 hop away. Round 2 = all nodes 2 hops away. This is exactly why BFS gives the *shortest* path in an unweighted graph — the first time you reach a node, you've used the fewest hops.

**Why a queue (not a stack)?** FIFO — you finish all nodes at distance d before moving to d+1. A stack (DFS) would dive deep immediately and wouldn't guarantee shortest path.

**Why mark visited on enqueue (not dequeue)?** If you wait until dequeue, the same node can be added to the queue multiple times from different neighbors. You'd process it multiple times and get wrong distances.

```python
from collections import deque

def bfs(graph, start):
    visited = {start}        # mark immediately when you decide to visit
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)      # mark here, not when you pop
                queue.append(nei)
```

**Returning distance — just carry it in the queue:**

```python
def bfs_dist(graph, start, end):
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        if node == end: return dist
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                queue.append((nei, dist + 1))
    return -1
```

No separate distance array needed — each queue entry carries its own distance. This works because BFS processes nodes in order of distance, so the first time you pop a node it's at minimum distance.

**Grid BFS — same logic, different neighbor generation:**

```python
def bfs_grid(grid, sr, sc):
    ROWS, COLS = len(grid), len(grid[0])
    queue = deque([(sr, sc)])
    visited = {(sr, sc)}
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr,nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc))
```

The bounds check `0 <= nr < ROWS and 0 <= nc < COLS` replaces the "is this a valid node" check you'd do in a regular graph.

---

## DFS — Connectivity / Reachability

**The mental model:** DFS commits to one path, goes as deep as possible, then backtracks. Use it when you don't care about the *length* of the path — just whether something is reachable, or to label/group nodes.

**Why recursion works here:** each recursive call = going one step deeper. The call stack IS the path you're currently on. When a call returns, you automatically backtrack.

**The visited set is mandatory** for graphs (unlike trees). Without it, you'll loop forever on cycles.

```python
def dfs(graph, node, visited):
    visited.add(node)
    for nei in graph[node]:
        if nei not in visited:
            dfs(graph, nei, visited)
```

**Counting connected components — the key insight:** if you run DFS from one node, you only reach nodes in *its* component. To count components, run DFS from every unvisited node; each time you start a fresh DFS, you've found a new component.

```python
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v); graph[v].append(u)
    visited = set()

    def dfs(node):
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                dfs(nei)

    count = 0
    for i in range(n):
        if i not in visited:
            visited.add(i)   # mark before DFS, not inside — avoids re-entry
            dfs(i)
            count += 1       # every time you start a fresh DFS = new component
    return count
```

**Grid DFS — mark in-place instead of a visited set:**

```python
def dfs(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]): return
    if grid[r][c] != '1': return
    grid[r][c] = '#'    # overwrite to mark visited — avoids a separate set
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r+dr, c+dc)
```

Overwriting the cell is safe when the problem says you can modify the grid, or when you're only asked for a count (not the original values).

---

## Topological Sort

**The mental model:** topo sort answers "in what order can I do these tasks, given that some tasks must come before others?" It only works on DAGs (directed, no cycles). If there's a cycle, no valid order exists.

**There are two algorithms — pick based on what you need:**

| | Kahn's (BFS) | DFS postorder |
|---|---|---|
| Returns | actual order | actual order (reversed) |
| Detects cycle | `len(order) != n` | returns False mid-DFS |
| Best for | when you need the order | when cycle detection is the main goal |

### Kahn's (BFS) — start from nodes with no dependencies

**Why indegree?** A node with `indegree=0` has no prerequisites — it can go first. When you process it, you remove it from the graph, which might free up more nodes. Repeat until nothing is left.

```python
def topo_kahn(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1           # v depends on u

    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1     # "remove" this node from the graph
            if indegree[nei] == 0:
                queue.append(nei)  # now this node has no remaining dependencies

    return order if len(order) == n else []   # len < n means a cycle exists
```

If `len(order) < n`, some nodes were never added to the queue — they're stuck in a cycle where everyone is waiting for someone else.

### DFS postorder — append AFTER all descendants are processed

**Why postorder?** A node must come *after* all its dependencies in topo order. In DFS, you finish a node's subtree before returning — so appending on return (postorder) gives you reverse topo order. Reverse at the end.

```python
def topo_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges: graph[u].append(v)
    state = [0] * n   # 0=unvisited, 1=in-path (currently on stack), 2=done

    result = []

    def dfs(node):
        if state[node] == 1: return False   # back edge = cycle
        if state[node] == 2: return True    # already fully processed, skip
        state[node] = 1                     # mark as "currently visiting"
        for nei in graph[node]:
            if not dfs(nei): return False
        state[node] = 2
        result.append(node)                 # append AFTER all descendants
        return True

    for i in range(n):
        if state[i] == 0:
            if not dfs(i): return []
    return result[::-1]
```

**Why 3 states (not just visited/unvisited)?** 2 states can't distinguish "visited in this path" from "visited in a previous path." State 1 (in-path) is the cycle detector — if you reach a node that's already on your current path, you have a cycle.

---

## Dijkstra — Weighted Shortest Path

**The mental model:** Dijkstra is like BFS but with a priority queue instead of a regular queue. Instead of "process all nodes d hops away first," it processes "the closest unfinished node first." This greedily builds the shortest path tree.

**Why it fails with negative weights:** Dijkstra assumes that once you've settled a node (popped from the heap), its distance is final. A negative edge could later provide a cheaper path to an already-settled node. Bellman-Ford handles negatives by re-relaxing edges repeatedly.

```python
import heapq

def dijkstra(n, adj, src):   # adj[u] = [(v, weight), ...]
    dist = [float('inf')] * n
    dist[src] = 0
    pq = [(0, src)]          # (distance, node)

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue      # stale entry — a shorter path was already found
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist
```

**Why `if d > dist[u]: continue`?** Python's heap doesn't support "decrease key," so when you find a better path to a node, you push a *new* entry. The old entry is now stale. The check skips it — without it, you'd re-process nodes you've already settled correctly.

---

## Connected Components — DFS

**The pattern to remember:** outer loop over all nodes → inner DFS → count how many times the outer loop fires. That count = number of components. This handles disconnected graphs naturally; a single DFS from one start node wouldn't.

```python
def count_components(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v); graph[v].append(u)
    visited = set()

    def dfs(node):
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                dfs(nei)

    count = 0
    for i in range(n):
        if i not in visited:
            visited.add(i)
            dfs(i)
            count += 1
    return count
```

---

## Cycle Detection

**Directed vs undirected — completely different approaches:**

In an **undirected** graph, every edge goes both ways. When you're at node A and came from B, you'll always see B as a neighbor — but that's not a cycle, it's just the edge you came from. Track the parent to ignore it.

In a **directed** graph, edges only go one way. A cycle exists when you reach a node that's *currently on your recursion stack* (you're in the middle of visiting it). That's the "in-path" state.

**Directed graph — 3-state DFS:**

```python
state = [0] * n   # 0=unvisited, 1=in current path, 2=fully done

def has_cycle_directed(node):
    if state[node] == 1: return True    # back edge = cycle
    if state[node] == 2: return False   # already fully explored, safe
    state[node] = 1
    for nei in graph[node]:
        if has_cycle_directed(nei): return True
    state[node] = 2
    return False
```

**Undirected graph — track parent to avoid false positives:**

```python
def has_cycle_undirected(node, parent, visited, graph):
    visited.add(node)
    for nei in graph[node]:
        if nei not in visited:
            if has_cycle_undirected(nei, node, visited, graph): return True
        elif nei != parent:   # seen AND not the node we came from = real cycle
            return True
    return False

# Must call for all nodes (disconnected graphs):
for i in range(n):
    if i not in visited:
        if has_cycle_undirected(i, -1, visited, graph): return True
```

**LC 684 — Redundant Connection:** find the edge that *creates* a cycle. Process edges one by one, building the graph incrementally. The first edge where a path already exists between its two endpoints is the answer.

```python
def findRedundantConnection(edges):
    graph = defaultdict(set)

    def connected(u, v):
        # DFS to check if u can reach v in the graph built so far
        visited = set()
        stack = [u]
        while stack:
            node = stack.pop()
            if node == v: return True
            if node in visited: continue
            visited.add(node)
            stack.extend(graph[node])
        return False

    for u, v in edges:
        if connected(u, v):    # path already exists → adding this edge creates a cycle
            return [u, v]
        graph[u].add(v)
        graph[v].add(u)
    return []
```

Why add the edge AFTER the check? You're asking "does a path exist before this edge?" — if you add it first, you'd always find a path (the edge itself).

---

## Bipartite Check

**The mental model:** a graph is bipartite if you can color it with 2 colors such that no two adjacent nodes share a color. This is equivalent to asking: does the graph have any odd-length cycles? BFS makes this easy — alternate colors as you traverse.

**Why BFS works:** when you assign a color to a node, all its neighbors get the opposite color. If you ever try to assign a color that contradicts what's already there, you've found two adjacent nodes of the same color → not bipartite.

```python
def is_bipartite(graph):
    color = {}
    for start in range(len(graph)):
        if start in color: continue
        queue = deque([start])
        color[start] = 0
        while queue:
            node = queue.popleft()
            for nei in graph[node]:
                if nei not in color:
                    color[nei] = 1 - color[node]   # flip: 0→1, 1→0
                    queue.append(nei)
                elif color[nei] == color[node]:    # same color as neighbor = contradiction
                    return False
    return True
```

The outer loop over all `start` nodes handles disconnected graphs — each component gets independently checked.

---

## Multi-Source BFS

**The mental model:** instead of asking "shortest distance from A to all others," you ask "shortest distance from *any node in a set S* to all others." The trick: add all source nodes to the queue at the start, all at distance 0. BFS then expands outward from all of them simultaneously.

**Why this works:** BFS guarantees each node is reached at its minimum distance. If you seed multiple sources at distance 0, the minimum distance to any node is automatically the distance to its closest source.

```python
queue = deque()
visited = set()
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == TARGET:
            queue.append((r, c, 0))
            visited.add((r, c))
# then standard BFS from queue — no special handling needed
```

Classic uses: Rotting Oranges (all rotten oranges at t=0), Walls and Gates (all gates at distance 0), 01 Matrix (all 0-cells are sources).

---

## Reverse DFS / BFS (Pacific Atlantic pattern)

**The mental model:** sometimes the forward direction is expensive. "Can water flow from (r,c) to the Pacific?" requires simulating downhill flow for every cell — O(n²·n²) naively. Flip it: "what cells can the Pacific *reach* going uphill?" Run DFS *from the ocean border inward*, following cells that are equal or higher. Same answer, single pass.

**When to use this:** whenever "can X reach Y?" is expensive but "what can Y reach?" is cheap, reverse the direction.

```python
def dfs(r, c, visit, prev_height):
    if (r,c) in visit or r<0 or r>=ROWS or c<0 or c>=COLS: return
    if grid[r][c] < prev_height: return    # can't flow uphill from ocean's perspective
    visit.add((r, c))
    for dr, dc in dirs:
        dfs(r+dr, c+dc, visit, grid[r][c])
```

Run from all Pacific border cells into `pacific` set, all Atlantic border cells into `atlantic` set. Answer = intersection.

---

## Word Ladder (BFS + string transformation)

**The mental model:** each word is a node. Two words are connected if they differ by exactly one letter. You want the shortest path from `beginWord` to `endWord` — that's BFS on this implicit graph. You never build the graph explicitly; you generate neighbors on the fly.

**Key trick:** instead of comparing every word in `wordList` to the current word (O(n·L)), generate all possible 1-letter variants (O(26·L)) and check if they're in the word set (O(1) with a set). Much faster.

```python
def ladder_length(beginWord, endWord, wordList):
    words = set(wordList)
    if endWord not in words: return 0
    queue = deque([(beginWord, 1)])
    visited = {beginWord}
    while queue:
        word, length = queue.popleft()
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                nw = word[:i] + c + word[i+1:]
                if nw == endWord: return length + 1
                if nw in words and nw not in visited:
                    visited.add(nw)
                    queue.append((nw, length + 1))
    return 0
```

---

## Bellman-Ford — Shortest Path with Negative Weights / K-Stop Constraint

**The mental model:** relax all edges repeatedly. After k iterations, `dist[v]` = shortest path using at most k edges. For standard shortest path, run n-1 iterations (longest possible path without cycles). For "K stops" problems, run k+1 iterations.

**Why copy dist each round?** You want to count hops, not allow multiple relaxations in the same round. If you update `dist` in-place, a chain of relaxations in one pass can give you a path that uses more edges than allowed. The copy enforces "one edge per round."

```python
def bellman_ford(n, edges, src, k=None):
    dist = [float('inf')] * n
    dist[src] = 0
    iters = k if k is not None else n - 1
    for _ in range(iters):
        temp = dist[:]          # copy before each round — prevents multi-hop in one pass
        for u, v, w in edges:
            if dist[u] + w < temp[v]:
                temp[v] = dist[u] + w
        dist = temp
    return dist
```

LC 787 (K stops): pass `k = k+1` (K stops = K+1 edges).

---

## Problems to Know Cold (L3)

| Problem | LC | Pattern |
|---------|----|---------|
| Number of Islands | 200 | Grid DFS |
| Clone Graph | 133 | DFS + hashmap |
| Pacific Atlantic Water Flow | 417 | Reverse DFS from borders |
| Course Schedule | 207 | Topo sort / cycle detect |
| Course Schedule II | 210 | Topo sort (Kahn's) |
| Word Ladder | 127 | BFS + string transform |
| All Paths Source to Target | 797 | DFS backtracking on DAG |
| Rotting Oranges | 994 | Multi-source BFS |
| Network Delay Time | 743 | Dijkstra |
| Cheapest Flights K Stops | 787 | Bellman-Ford |
| Redundant Connection | 684 | DFS cycle detection (edge-by-edge) |
| Number of Connected Components | 323 | DFS count |
| Is Graph Bipartite | 785 | BFS 2-coloring |
| Alien Dictionary | 269 | Topo sort on characters |

---

## Decision Table

| Situation | Algorithm | Why |
|-----------|-----------|-----|
| Shortest path, unweighted | BFS | explores by hop count |
| Shortest path, weighted (no neg) | Dijkstra | greedily settles closest node first |
| Shortest path, negative weights | Bellman-Ford | re-relaxes all edges k times |
| Connectivity, components | DFS (outer loop counts) | DFS floods one component; outer loop counts how many times it fires |
| Cycle in directed graph | 3-state DFS / Kahn's | needs to distinguish "in current path" from "already done" |
| Cycle in undirected graph | DFS with parent tracking | must ignore the edge you came from |
| Ordering with dependencies | Topological Sort | BFS from zero-indegree nodes, or DFS postorder |
| Multi-source shortest dist | Multi-source BFS | seed all sources at distance 0 |
| 2-colorable | BFS bipartite check | alternate colors, catch contradictions |

---

## Common Mistakes

- **Forgetting disconnected graphs** — a single BFS/DFS from one node only covers its component. Always outer-loop over all nodes if the graph might be disconnected.
- **Marking visited on dequeue instead of enqueue** — the same node gets enqueued multiple times, leading to duplicate processing and wrong distances.
- **Using parent-tracking DFS for directed graphs** — parent trick only suppresses the reverse of the edge you came from. In directed graphs, there's no reverse edge, so use 3-state DFS instead.
- **Dijkstra: missing `if d > dist[u]: continue`** — without this, stale heap entries cause you to re-process already-settled nodes and potentially corrupt distances.
- **Topological sort: not checking `len(order) == n`** — if a cycle exists, some nodes never reach indegree 0 and are silently skipped. The length check catches this.
- **Bellman-Ford: updating dist in-place** — allows a chain of relaxations in one pass, effectively using more edges than intended. Always copy before each round.
