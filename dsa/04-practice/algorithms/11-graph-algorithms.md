---
tags: [coding, algorithms, graph-algorithms]
topic: Graph Algorithms
difficulty: mixed
---
# Graph Algorithms — Problem Deep Dives

## What this covers

> [!abstract] In this file
> **Covers:** Worked graph-algorithm problems: Dijkstra, Bellman-Ford, Kahn's topological sort, cycle detection, 0-1 BFS, multi-source BFS, Prim's MST, coloring.
> **You'll be able to:** Choose and code the right shortest-path / ordering algorithm.
> **Prereqs:** Graph lecture · **Pair with:** [Graph lecture](../../02-data-structures/11-graphs.md) · [Graph problems](../data-structures/11-graph.md) · **Time:** 4 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Dijkstra's Algorithm](#dijkstras-algorithm) · [Bellman-Ford](#bellman-ford) · [Topological Sort (BFS — Kahn's)](#topological-sort-bfs--kahns) · [Strongly Connected Components / Bridges](#strongly-connected-components--bridges) · [Cycle Detection in Directed Graph](#cycle-detection-in-directed-graph) · [Eulerian Path](#eulerian-path) · [0-1 BFS](#0-1-bfs) · [Multi-source BFS / Special BFS](#multi-source-bfs--special-bfs) · [Minimum Spanning Tree — Prim's Algorithm](#minimum-spanning-tree--prims-algorithm) · [Graph Coloring](#graph-coloring)

> [!tip] If you only have 20 minutes
> **Do these first:** [Network Delay Time](#dijkstras-algorithm) · [Cheapest Flights Within K Stops](#cheapest-flights-within-k-stops--t1) · [Path with Maximum Probability](#dijkstras-algorithm) · [Find Eventual Safe States (Reverse Graph / Kahn's)](#find-eventual-safe-states-reverse-graph--kahns--t1) · [Word Ladder (BFS on Implicit Graph)](#word-ladder-bfs-on-implicit-graph--t1) · [Detect Cycle in Directed Graph (DFS 3-Color)](#cycle-detection-in-directed-graph) · [Min Cost to Connect All Points](#minimum-spanning-tree--prims-algorithm)
> **Template:** Dijkstra: `heap = [(0, src)]; while heap: d, u = heappop(heap); if d > dist[u]: continue; relax neighbors`.
> **Template:** K-limited paths: Bellman-Ford for `K+1` rounds, relaxing from a **copy** of last round's `dist`.
> **Gotchas:** Dijkstra fails with negative edges · Cheapest Flights: plain Dijkstra on cost is wrong — the state must include stops · BFS beats Dijkstra on unit weights · `💤 T3` here (Tarjan, TSP bitmask): name only.

---

## Dijkstra's Algorithm

**Also try:**

- **Network Delay Time** — Shortest paths from a single source with non-negative weights
- **Path with Maximum Probability** — Maximize a product along a path — same structure as shortest path but with max-product instead of min-sum
- **Evaluate Division (LC 399)** — Division is transitive — `a/c = (a/b) * (b/c)`
- **Cheapest Flights Within K Stops (Dijkstra variant)** — Bellman-Ford (next section) is the usual answer

---

## Bellman-Ford

---

### Cheapest Flights Within K Stops `⚡ T1`

> [!example] Problem
> There are `n` cities connected by `flights` where `flights[i] = [from, to, price]`. Given src, dst, and an integer `k`, return the **cheapest price** from `src` to `dst` with at most `k` stops. Return `-1` if no such route exists.
>
> ```
> Input: n=4, flights=[[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], src=0, dst=3, k=1
> Output: 700  (0→1→3, 1 stop)
> ```

> [!tip] Recognize · Gotcha
> **Signal:** Bellman-Ford / relax k times · **Gotcha:** **K stops** = at most `K+1` edges; **negative** edges not allowed in Dijkstra variant.

> [!failure] Tempting wrong approach
> Plain Dijkstra with one `dist[node]` — it discards a pricier path with fewer stops that may be the only valid one. Use Bellman-Ford for K+1 rounds on a *copy* of `dist`, or Dijkstra keyed on `(node, stops)`.

> [!info] Approach — Bellman-Ford (K+1 rounds)
> "At most k stops" means at most **k+1 edges**. Run Bellman-Ford for exactly k+1 rounds.
>
> **The copy trick:** Before each round, snapshot `dist` into `temp`. Relax edges using the *old* `dist` values, write updates into `temp`. Without this, a single round could chain 2+ hops, violating the k-stop constraint.
>
> **Key insight:** After round `i`, `dist[v]` = cheapest price to reach v using at most `i` edges.

> [!note]- Python Solution — Bellman-Ford
> ```python
> def findCheapestPrice(n, flights, src, dst, k):
>     INF = float('inf')
>     dist = [INF] * n
>     dist[src] = 0
>
>     for _ in range(k + 1):          # k stops = k+1 edges
>         temp = dist.copy()           # critical: snapshot before round
>         for u, v, price in flights:
>             if dist[u] != INF:
>                 temp[v] = min(temp[v], dist[u] + price)
>         dist = temp
>
>     return dist[dst] if dist[dst] != INF else -1
> ```

> [!note]- Python Solution — Dijkstra with State
> ```python
> import heapq
>
> def findCheapestPrice(n, flights, src, dst, k):
>     adj = {}
>     for u, v, w in flights:
>         adj.setdefault(u, []).append((v, w))
>
>     # (cost, node, stops_remaining)
>     heap = [(0, src, k + 1)]
>     best = {}   # (node, stops_remaining) -> min cost seen
>
>     while heap:
>         cost, node, stops = heapq.heappop(heap)
>         if node == dst:
>             return cost
>         if stops == 0:
>             continue
>         if (node, stops) in best and best[(node, stops)] <= cost:
>             continue
>         best[(node, stops)] = cost
>         for nei, w in adj.get(node, []):
>             heapq.heappush(heap, (cost + w, nei, stops - 1))
>
>     return -1
> ```

> [!success] Complexity
> - Bellman-Ford: Time O(k · E), Space O(n).
> - Dijkstra: Time O(E log(n · k)), Space O(n · k).

> [!tip] Edge Cases / Alternatives
> - `k = 0` means direct flight only — Bellman-Ford runs exactly 1 round.
> - Dijkstra is faster in practice but needs state `(node, stops_remaining)` to track hop count — standard Dijkstra without this state would ignore the k-stop constraint.
> - Bellman-Ford copy trick: if you update `dist` in-place during a round, you can chain unlimited hops within that round.

---

### Detect Negative Cycle `🎯 T2`

> [!example] Problem
> Given a weighted directed graph, determine whether it contains a **negative weight cycle** (a cycle whose total edge weight is negative).

> [!info] Approach
> Run standard Bellman-Ford for **V-1** rounds to compute shortest paths from an arbitrary source. Then do **one more relaxation pass**: if any edge `(u, v, w)` still satisfies `dist[u] + w < dist[v]`, a negative cycle is reachable — the cycle allows paths to be shortened indefinitely.
>
> For graphs that may be disconnected, add a virtual source node with a zero-weight edge to every node; this ensures all nodes are reachable.

> [!note]- Python Solution
> ```python
> def has_negative_cycle(n, edges):
>     """edges: list of (u, v, weight), nodes 0-indexed"""
>     INF = float('inf')
>     dist = [0] * n              # start all at 0: handles disconnected graphs
>                                  # (equivalent to a virtual source → all nodes)
>
>     for _ in range(n - 1):
>         for u, v, w in edges:
>             if dist[u] + w < dist[v]:
>                 dist[v] = dist[u] + w
>
>     # V-th relaxation: if anything improves, negative cycle exists
>     for u, v, w in edges:
>         if dist[u] + w < dist[v]:
>             return True
>
>     return False
> ```

> [!success] Complexity
> Time O(V · E), Space O(V).

> [!tip] Edge Cases / Alternatives
> - Initialising `dist` to all zeros (rather than INF) is a standard trick that handles disconnected graphs without a real source node.
> - Floyd-Warshall detects negative cycles differently: after the algorithm, check if any `dist[i][i] < 0`.

**Also try:**

- **Bellman-Ford (Negative Weights)** — Dijkstra does not work with negative edges
- **Find the City with the Smallest Number of Neighbors at a Threshold Distance (Floyd-Warshall)** — Need all-pairs shortest paths

---

## Topological Sort (BFS — Kahn's)

**Also try:**

- **Sequence Reconstruction (Check Unique Topo Order)** — `nums` is the unique shortest supersequence iff the topological order derived from all constraints is unique — meaning at every step, exactl…
- **Find All Possible Recipes from Given Supplies** — Recipe dependencies form a DAG

---

## Strongly Connected Components / Bridges

---

### Critical Connections in a Network (Tarjan's Bridges) `💤 T3`

> [!example] Problem
> There are n servers numbered from 0 to n - 1 connected by undirected server-to-server connections forming a network where connections[i] = [ai, bi] represents a connection between servers ai and bi. Any server can reach other servers directly or indirectly through the network.
> A critical connection is a connection that, if removed, will make some servers unable to reach some other server.
> Return all critical connections in the network in any order.
> 
> **Example 1:**
> ```
> Input: n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]
> Output: [[1,3]]
> Explanation: [[3,1]] is also accepted.
> ```
> 
> **Example 2:**
> ```
> Input: n = 2, connections = [[0,1]]
> Output: [[0,1]]
> ```
> 
> **Constraints:**
> - 2 <= n <= 10^5
> - n - 1 <= connections.length <= 10^5
> - 0 <= ai, bi <= n - 1
> - ai != bi
> - There are no repeated connections.

> [!info] Approach
> A bridge is an edge with no alternative path — its removal increases connected components. Tarjan's bridge-finding: DFS assigns `disc[]` (discovery time) and `low[]` (earliest disc reachable from subtree). Edge `(u,v)` is a bridge iff `low[v] > disc[u]`. DFS from any node. When backtracking from child `v` to parent `u`: `low[u] = min(low[u], low[v])`. For already-visited back edges (non-parent): `low[u] = min(low[u], disc[v])`. Bridge condition: `low[v] > disc[u]`.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def critical_connections(n, connections):
>     graph = defaultdict(list)
>     for u, v in connections:
>         graph[u].append(v)
>         graph[v].append(u)
> 
>     disc = [-1] * n
>     low = [-1] * n
>     timer = [0]
>     bridges = []
> 
>     def dfs(u, parent):
>         disc[u] = low[u] = timer[0]
>         timer[0] += 1
>         for v in graph[u]:
>             if v == parent:
>                 continue
>             if disc[v] == -1:
>                 dfs(v, u)
>                 low[u] = min(low[u], low[v])
>                 if low[v] > disc[u]:        # bridge condition
>                     bridges.append([u, v])
>             else:
>                 low[u] = min(low[u], disc[v])
> 
>     dfs(0, -1)
>     return bridges
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> Naive — remove each edge, check connectivity: O(E·(V+E)). Articulation-point variant for cut vertices. Multi-edge graphs: track parent edge index, not node.

---

### Find Eventual Safe States (Reverse Graph / Kahn's) `⚡ T1`

> [!example] Problem
> There is a directed graph of n nodes with each node labeled from 0 to n - 1. The graph is represented by a 0-indexed 2D integer array graph where graph[i] is an integer array of nodes adjacent to node i, meaning there is an edge from node i to each node in graph[i].
> A node is a terminal node if there are no outgoing edges. A node is a safe node if every possible path starting from that node leads to a terminal node (or another safe node).
> Return an array containing all the safe nodes of the graph. The answer should be sorted in ascending order.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2],[2,3],[5],[0],[5],[],[]]
> Output: [2,4,5,6]
> Explanation: The given graph is shown above.
> Nodes 5 and 6 are terminal nodes as there are no outgoing edges from either of them.
> Every path starting at nodes 2, 4, 5, and 6 all lead to either node 5 or 6.
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1,2,3,4],[1,2],[3,4],[0,4],[]]
> Output: [4]
> Explanation:
> Only node 4 is a terminal node, and every path starting at node 4 leads to node 4.
> ```
> 
> **Constraints:**
> - n == graph.length
> - 1 <= n <= 10^4
> - 0 <= graph[i].length <= n
> - 0 <= graph[i][j] <= n - 1
> - graph[i] is sorted in a strictly increasing order.
> - The graph may contain self-loops.
> - The number of edges in the graph will be in the range [1, 4 * 10^4].

> [!tip] Recognize · Gotcha
> **Signal:** "Nodes that don't lead to a cycle" · **Gotcha:** Alternatively: DFS with 3-color (white/gray/black); gray = cycle.

> [!info] Approach
> Unsafe nodes are those on or leading to cycles. In the reversed graph, terminal nodes (out-degree 0 in original) have in-degree 0. Topological sort on the reversed graph pulls in nodes that only lead to "safe" destinations. Reverse all edges. Kahn's BFS — nodes with out-degree 0 in original become sources. `outdegree[u]` = original out-degree. Initialize queue with `outdegree[u] == 0`. When a node is processed safe, decrement predecessors' outdegree; add them if 0.

> [!note]- Python Solution
> ```python
> from collections import deque, defaultdict
> 
> def eventual_safe_nodes(graph):
>     n = len(graph)
>     reverse = defaultdict(list)
>     outdegree = [0] * n
> 
>     for u, neighbors in enumerate(graph):
>         for v in neighbors:
>             reverse[v].append(u)
>             outdegree[u] += 1
> 
>     q = deque(i for i in range(n) if outdegree[i] == 0)
>     safe = set()
> 
>     while q:
>         node = q.popleft()
>         safe.add(node)
>         for nb in reverse[node]:
>             outdegree[nb] -= 1
>             if outdegree[nb] == 0:
>                 q.append(nb)
> 
>     return sorted(safe)
> ```

> [!success] Complexity
> Time O(V + E), Space O(V + E).

> [!tip] Alternatives
> DFS with 3-color marking — node is safe iff all successors are safe. Memoize per node. Same O(V + E) but Kahn's is cleaner.

---

## Cycle Detection in Directed Graph

**Also try:**

- **Detect Cycle in Directed Graph (DFS 3-Color)** — Kahn's BFS detects cycles implicitly via count, but DFS 3-color is the canonical O(V+E) approach that also identifies the cycle

---

## Eulerian Path

**Also try:**

- **Reconstruct Itinerary (Hierholzer's)** — "Use every edge exactly once" = Eulerian path in a directed graph

---

## 0-1 BFS

---

### Open the Lock (Unweighted BFS Variant) `⚡ T1`

> Full walkthrough: [Open the Lock](../data-structures/06-queue.md#open-the-lock--t1).

---

## Multi-source BFS / Special BFS

---

### Word Ladder (BFS on Implicit Graph) `⚡ T1`

> [!example] Problem
> A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
> Given two words, beginWord and endWord, and a dictionary wordList, return the number of words in the shortest transformation sequence from beginWord to endWord, or 0 if no such sequence exists.
> 
> **Example 1:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: 5
> Explanation: One shortest transformation sequence is "hit" -> "hot" -> "dot" -> "dog" -> cog", which is 5 words long.
> ```
> 
> **Example 2:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
> Output: 0
> Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
> ```
> 
> **Constraints:**
> - 1 <= beginWord.length <= 10
> - endWord.length == beginWord.length
> - 1 <= wordList.length <= 5000
> - wordList[i].length == beginWord.length
> - beginWord, endWord, and wordList[i] consist of lowercase English letters.
> - beginWord != endWord
> - All the words in wordList are unique.

> [!tip] Recognize · Gotcha
> **Signal:** "Minimum transformation steps" · **Gotcha:** Remove word from set when visited — prevents revisit and cycles. Bidirectional BFS halves explored nodes for follow-up.

> [!failure] Tempting wrong approach
> Building edges by comparing every word pair — O(N²·L). Try 26 letters per position (or wildcard buckets) and remove words from the set when enqueued.

> [!info] Approach
> Nodes = words, edges = one-letter-apart pairs. Unweighted BFS gives shortest path. The graph is implicit — never enumerate all pairs (O(N²·L)) — instead generate neighbors by substitution. BFS where each level = one transformation. For each word, try replacing each position with `a-z` and check against the word set. Remove visited words from `word_set` immediately (not just a visited set) to prevent revisits efficiently.

> [!note]- Python Solution
> ```python
> from collections import deque
> 
> def ladder_length(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return 0
> 
>     q: deque[tuple[str, int]] = deque([(beginWord, 1)])
>     visited = {beginWord}
> 
>     while q:
>         word, length = q.popleft()
>         for i in range(len(word)):
>             for c in 'abcdefghijklmnopqrstuvwxyz':
>                 new_word = word[:i] + c + word[i+1:]
>                 if new_word == endWord:
>                     return length + 1
>                 if new_word in word_set and new_word not in visited:
>                     visited.add(new_word)
>                     q.append((new_word, length + 1))
> 
>     return 0
> ```

> [!success] Complexity
> Time O(M² · N) where M = word length, N = wordList size. Space O(M · N).

> [!tip] Alternatives
> Bidirectional BFS — expand from both ends; reduces to O(M² · √N) in practice. Preprocessing: bucket words by `*at` pattern (replace each char with `*`) reduces neighbor generation to O(M·N).

---

### Word Ladder II (All Shortest Transformation Sequences) `⚡ T1`

> [!example] Problem
> A transformation sequence from word beginWord to word endWord using a dictionary wordList is a sequence of words beginWord -> s1 -> s2 -> ... -> sk such that:
> Given two words, beginWord and endWord, and a dictionary wordList, return all the shortest transformation sequences from beginWord to endWord, or an empty list if no such sequence exists. Each sequence should be returned as a list of the words [beginWord, s1, s2, ..., sk].
> 
> **Example 1:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log","cog"]
> Output: [["hit","hot","dot","dog","cog"],["hit","hot","lot","log","cog"]]
> Explanation: There are 2 shortest transformation sequences:
> "hit" -> "hot" -> "dot" -> "dog" -> "cog"
> "hit" -> "hot" -> "lot" -> "log" -> "cog"
> ```
> 
> **Example 2:**
> ```
> Input: beginWord = "hit", endWord = "cog", wordList = ["hot","dot","dog","lot","log"]
> Output: []
> Explanation: The endWord "cog" is not in wordList, therefore there is no valid transformation sequence.
> ```
> 
> **Constraints:**
> - 1 <= beginWord.length <= 5
> - endWord.length == beginWord.length
> - 1 <= wordList.length <= 500
> - wordList[i].length == beginWord.length
> - beginWord, endWord, and wordList[i] consist of lowercase English letters.
> - beginWord != endWord
> - All the words in wordList are unique.
> - The sum of all shortest transformation sequences does not exceed 10^5.

> [!info] Approach
> Finding all shortest paths requires BFS to establish the level structure (shortest distance to each node), then backtracking to reconstruct paths — DFS alone is exponential without the level constraint. Two-phase: BFS to build a DAG of "parent → children" edges that lie on shortest paths; then DFS/backtracking on that DAG to enumerate all paths. BFS level-by-level. For each word, generate all 1-letter variants in the word set. Record `parents[new_word].add(word)`. Remove words from the set only after the full level is processed (so multiple parents at the same level can be recorded). Then DFS from `endWord` back to `beginWord` using the `parents` map.

> [!note]- Python Solution
> ```python
> from collections import defaultdict, deque
> 
> def find_ladders(beginWord, endWord, wordList):
>     word_set = set(wordList)
>     if endWord not in word_set:
>         return []
> 
>     parents = defaultdict(set)
>     current_level = {beginWord}
>     found = False
> 
>     while current_level and not found:
>         word_set -= current_level      # remove current level to prevent back-edges
>         next_level = set()
>         for word in current_level:
>             for i in range(len(word)):
>                 for c in 'abcdefghijklmnopqrstuvwxyz':
>                     new_word = word[:i] + c + word[i+1:]
>                     if new_word in word_set:
>                         next_level.add(new_word)
>                         parents[new_word].add(word)
>                         if new_word == endWord:
>                             found = True
>         current_level = next_level
> 
>     if not found:
>         return []
> 
>     # Backtrack from endWord to beginWord
>     result = []
> 
>     def backtrack(word, path):
>         if word == beginWord:
>             result.append(path[::-1])
>             return
>         for parent in parents[word]:
>             path.append(parent)
>             backtrack(parent, path)
>             path.pop()
> 
>     backtrack(endWord, [endWord])
>     return result
> ```

> [!success] Complexity
> Time O(M² · N + P) where M = word length, N = wordList size, P = total characters in all output paths. Space O(M · N).

> [!tip] Alternatives
> BFS + DFS without the parent-map — enumerate during DFS and prune by depth; same complexity but harder to implement correctly. Bidirectional BFS reduces the search space but makes parent tracking trickier.

---

### Shortest Path Visiting All Nodes (LC 847) `💤 T3`

> [!example] Problem
> You have an undirected, connected graph of n nodes labeled from 0 to n - 1. You are given an array graph where graph[i] is a list of all the nodes connected with node i by an edge.
> Return the length of the shortest path that visits every node. You may start and stop at any node, you may revisit nodes multiple times, and you may reuse edges.
> 
> **Example 1:**
> ```
> Input: graph = [[1,2,3],[0],[0],[0]]
> Output: 4
> Explanation: One possible path is [1,0,2,0,3]
> ```
> 
> **Example 2:**
> ```
> Input: graph = [[1],[0,2,4],[1,3,4],[2],[1,2]]
> Output: 4
> Explanation: One possible path is [0,1,4,2,3]
> ```
> 
> **Constraints:**
> - n == graph.length
> - 1 <= n <= 12
> - 0 <= graph[i].length < n
> - graph[i] does not contain i.
> - If graph[a] contains b, then graph[b] contains a.
> - The input graph is always connected.

> [!info] Approach
> This is TSP-like. With n ≤ 12, use BFS with bitmask state: `(node, visited_mask)`. BFS gives the shortest path. There are `n * 2^n` states — manageable for small n. Initialize queue with all `(node, 1 << node)` for every node (start from any node). BFS until `mask == (1 << n) - 1` (all visited). Visited set: `{(node, mask)}`. Dequeue state, try all neighbours. Update mask with `mask | (1 << neighbour)`.

> [!note]- Python Solution
> ```python
> from collections import deque
> >
> def shortest_path_length(graph):
>     n = len(graph)
>     full_mask = (1 << n) - 1
>     if n == 1:
>         return 0
>     queue = deque()
>     visited = set()
>     for i in range(n):
>         mask = 1 << i
>         queue.append((i, mask, 0))
>         visited.add((i, mask))
>     while queue:
>         node, mask, dist = queue.popleft()
>         for neighbor in graph[node]:
>             new_mask = mask | (1 << neighbor)
>             if new_mask == full_mask:
>                 return dist + 1
>             if (neighbor, new_mask) not in visited:
>                 visited.add((neighbor, new_mask))
>                 queue.append((neighbor, new_mask, dist + 1))
>     return -1
> ```

> [!success] Complexity
> Time O(n * 2^n), Space O(n * 2^n).

> [!tip] Alternatives
> - DP with bitmask (like TSP): `dp[mask][node]` = shortest path visiting exactly the nodes in mask and ending at `node`. Fills in O(n² * 2^n). BFS is simpler for unweighted graphs.

---

### Travelling Salesman Problem — Bitmask DP `💤 T3`

> [!example] Problem
> Given `n` cities and a distance matrix, find the shortest route that visits every city exactly once and returns to the starting city. Classic TSP.

> [!info] Approach
> Brute force is O(n!). Bitmask DP reduces to O(n² * 2^n) — tractable for n ≤ 20. `dp[mask][i]` = minimum cost to reach city `i` having visited exactly the cities in `mask`. Transition: for each unvisited city `j`, `dp[mask | (1<<j)][j] = min(..., dp[mask][i] + dist[i][j])`. Start with `dp[1][0] = 0` (started at city 0). Answer: `min(dp[full_mask][i] + dist[i][0])` for all `i`.

> [!note]- Python Solution
> ```python
> def tsp(dist):
>     n = len(dist)
>     full_mask = (1 << n) - 1
>     INF = float('inf')
>     dp = [[INF] * n for _ in range(1 << n)]
>     dp[1][0] = 0
>     for mask in range(1 << n):
>         for i in range(n):
>             if dp[mask][i] == INF:
>                 continue
>             if not (mask >> i & 1):
>                 continue
>             for j in range(n):
>                 if mask >> j & 1:
>                     continue
>                 new_mask = mask | (1 << j)
>                 if dp[new_mask][j] > dp[mask][i] + dist[i][j]:
>                     dp[new_mask][j] = dp[mask][i] + dist[i][j]
>     return min(dp[full_mask][i] + dist[i][0] for i in range(n))
> ```

> [!success] Complexity
> Time O(n² * 2^n), Space O(n * 2^n).

> [!tip] Alternatives
> - Held-Karp algorithm: same DP, just the classic name. O(n² * 2^n) is optimal for exact TSP.
> - For approximate TSP: Christofides' algorithm (1.5x approximation), or 2-opt local search for large instances.
> - Pattern shared with: Shortest Path Visiting All Nodes (LC 847), painting fence with k colors.

**Also try:**

- **Possible Bipartition** — "Split into two groups with no conflicts" = 2-color the conflict graph = bipartite check

---

## Minimum Spanning Tree — Prim's Algorithm

**Also try:**

- **Min Cost to Connect All Points (LC 1584)** — see [Min Cost to Connect All Points](10-union-find.md#mst-kruskals)

---

## Graph Coloring

**Also try:**

- **M-Coloring Problem (Backtracking)** — Graph coloring is NP-complete in general; backtracking with pruning is the standard approach for exact solutions on small graphs

---

## See Also

[[graph]] | [[union-find]] | [[dynamic-programming]] | [[binary-search]]
[[graph]] | [[dynamic-programming]] | [[union-find]] | [[binary-search]]
