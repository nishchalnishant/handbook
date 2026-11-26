# Disjoint Set Union (DSU / Union-Find)

---

## ⚡ Cheat Sheet (Quick Revision)

**When to use DSU:**
| Signal | Use DSU? |
|--------|----------|
| "connected components" in undirected graph | Yes |
| "are these two nodes in the same group?" | Yes |
| "cycle detection" in **undirected** graph | Yes |
| nodes merging dynamically over time | Yes |
| directed graph cycle detection | No — use topo sort (Kahn's) |
| shortest path | No — use BFS/Dijkstra |

**The template (write this cold):**
```python
parent = list(range(n))   # NOT [0]*n — each node is its own root
rank   = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path halving (compression)
        x = parent[x]
    return x

def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False            # already connected → False = no merge happened
    if rank[a] < rank[b]: a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]: rank[a] += 1
    return True                        # merged → True
```

**The 3 bugs everyone makes:**
1. `parent = [0] * n` — wrong. Every node's parent is `0`, not itself. Use `list(range(n))`.
2. Forgetting `return False` when `a == b` — cycle detection breaks silently.
3. Calling `find(a)` and `find(b)` after union — they may have changed; always `find` first.

---

## What It Does

DSU maintains a collection of **disjoint sets** (groups with no overlap). It supports two operations in nearly O(1) amortized time:
- `find(x)` — which group does `x` belong to? Returns the **root** of x's set.
- `union(a, b)` — merge the groups containing `a` and `b`.

The "nearly O(1)" is O(α(n)) where α is the inverse Ackermann function — effectively constant for all practical inputs.

---

## Why It Works (Mental Model)

Think of each group as a **tree**. Every node points to its parent. The root points to itself.

```
Initial (n=5):     After union(0,1), union(2,3):
0  1  2  3  4       0    2    4
↑  ↑  ↑  ↑  ↑      |    |
(each is its own root)   1    3
```

`find(x)` walks up to the root — that root is the group's ID.
`union(a, b)` attaches one root under the other.

**Without optimizations:** `find` can take O(n) in the worst case (degenerate chain).

**With path compression:** after `find(x)`, every node on the path points directly toward the root — future finds on those nodes are O(1).

**With union by rank:** always attach the shorter tree under the taller one — prevents chains from forming.

Together: amortized O(α(n)) ≈ O(1).

---

## Path Compression — Two Variants

**Full compression** (recursive, two-pass):
```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # every node points directly to root
    return parent[x]
# Clean but uses O(n) stack space on a degenerate tree
```

**Path halving** (iterative, one-pass) — preferred in interviews:
```python
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # skip one level (halve the path)
        x = parent[x]
    return x
# No recursion stack, same amortized complexity
```

Both achieve the same amortized complexity. Use path halving to avoid recursion depth issues.

---

## Union by Rank vs Union by Size

**By rank** (height upper bound — what the template uses):
```python
if rank[a] < rank[b]: a, b = b, a   # a becomes the "taller" root
parent[b] = a
if rank[a] == rank[b]: rank[a] += 1  # only increase rank when heights are equal
```

**By size** (node count — sometimes cleaner when you need component sizes):
```python
size = [1] * n

def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False
    if size[a] < size[b]: a, b = b, a
    parent[b] = a
    size[a] += size[b]   # root a absorbs b's count
    return True

def component_size(x):
    return size[find(x)]
```

Use `size` when the problem asks "how many nodes in this component?" — `size[find(x)]` gives it in O(1).

---

## Common Interview Patterns

### Pattern 1 — Count Connected Components

**Problem:** given `n` nodes and a list of edges, how many connected components are there?

```python
def countComponents(n, edges):
    parent = list(range(n))
    rank   = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return False
        if rank[a] < rank[b]: a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]: rank[a] += 1
        return True

    components = n
    for u, v in edges:
        if union(u, v):
            components -= 1    # each successful merge reduces count by 1
    return components
```

**Key:** start with `n` components. Every successful `union` reduces the count by 1.

---

### Pattern 2 — Cycle Detection in Undirected Graph

**Problem:** does this undirected graph contain a cycle?

```python
def hasCycle(n, edges):
    parent = list(range(n))
    rank   = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return False
        if rank[a] < rank[b]: a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]: rank[a] += 1
        return True

    for u, v in edges:
        if not union(u, v):   # union returned False = already in same component
            return True       # adding this edge creates a cycle
    return False
```

**Key:** `union` returns `False` when both nodes are already in the same component. Adding an edge between them would create a cycle.

> **Important:** this only works for **undirected** graphs. For directed graphs, use Kahn's topo sort or 3-state DFS.

---

### Pattern 3 — Dynamic Connectivity (edges added over time)

**Problem:** process a sequence of "connect" and "query" operations online.

```python
# Typical problem: "Number of Islands II" (LC 305)
# Starts with all water, land cells appear one at a time
# After each addition, report number of islands

def numIslands2(m, n, positions):
    parent = {}; rank = {}; count = [0]

    def find(x):
        if x not in parent: return x
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return
        if rank.get(a, 0) < rank.get(b, 0): a, b = b, a
        parent[b] = a
        if rank.get(a, 0) == rank.get(b, 0):
            rank[a] = rank.get(a, 0) + 1
        count[0] -= 1

    result = []
    for r, c in positions:
        if (r, c) in parent:
            result.append(count[0]); continue
        parent[(r, c)] = (r, c)
        rank[(r, c)] = 0
        count[0] += 1
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            nr, nc = r+dr, c+dc
            if (nr, nc) in parent:
                union((r, c), (nr, nc))
        result.append(count[0])
    return result
```

---

### Pattern 4 — Redundant Connection (LC 684)

**Problem:** given a tree with one extra edge added, find the redundant edge.

```python
def findRedundantConnection(edges):
    n = len(edges)
    parent = list(range(n+1))
    rank   = [0] * (n+1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return False
        if rank[a] < rank[b]: a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]: rank[a] += 1
        return True

    for u, v in edges:
        if not union(u, v):
            return [u, v]   # this edge connects two already-connected nodes
```

---

### Pattern 5 — Accounts Merge (LC 721)

**Problem:** merge accounts that share a common email. Each account is `[name, email1, email2, ...]`.

```python
from collections import defaultdict

def accountsMerge(accounts):
    parent = {}

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        parent[find(a)] = find(b)

    email_to_name = {}
    for account in accounts:
        name = account[0]
        for email in account[1:]:
            if email not in parent:
                parent[email] = email
            email_to_name[email] = name
            union(account[1], email)   # connect all emails in this account to the first

    groups = defaultdict(list)
    for email in parent:
        groups[find(email)].append(email)

    return [[email_to_name[root]] + sorted(emails)
            for root, emails in groups.items()]
```

**Key:** use emails as DSU nodes (strings, not ints). The root email becomes the group representative.

---

### Pattern 6 — Minimum Spanning Tree (Kruskal's)

**Problem:** find MST of a weighted undirected graph.

```python
def minCostConnectPoints(points):
    n = len(points)
    parent = list(range(n)); rank = [0] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        a, b = find(a), find(b)
        if a == b: return False
        if rank[a] < rank[b]: a, b = b, a
        parent[b] = a
        if rank[a] == rank[b]: rank[a] += 1
        return True

    # Build all edges sorted by weight
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            dist = abs(points[i][0]-points[j][0]) + abs(points[i][1]-points[j][1])
            edges.append((dist, i, j))
    edges.sort()

    total, added = 0, 0
    for cost, u, v in edges:
        if union(u, v):
            total += cost
            added += 1
            if added == n-1: break   # MST has exactly n-1 edges
    return total
```

**Key insight behind Kruskal's:** greedily add the cheapest edge that connects two different components. DSU tells you in O(1) whether two nodes are already connected.

---

## Nodes That Aren't Integers

When nodes are strings or tuples, use a dictionary instead of an array:

```python
parent = {}

def find(x):
    if x not in parent: parent[x] = x
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x

def union(a, b):
    a, b = find(a), find(b)
    if a != b: parent[b] = a
```

Drop `rank` for simplicity when you don't need union by rank (acceptable in most interview problems where the graph is small enough).

---

## Complexity

| Operation | Time (amortized) | Space |
|-----------|-----------------|-------|
| `find(x)` | O(α(n)) ≈ O(1) | — |
| `union(a, b)` | O(α(n)) ≈ O(1) | — |
| Initialize | O(n) | O(n) |

α(n) = inverse Ackermann function. For n < 10^600, α(n) ≤ 4. Treat it as constant.

---

## DSU vs BFS/DFS for Connected Components

| | DSU | BFS/DFS |
|--|-----|---------|
| Static graph (edges fixed) | Both work | Both work |
| Dynamic graph (edges added online) | DSU only | Must rebuild |
| Need the actual path between nodes | No | Yes |
| Cycle detection (undirected) | Yes | Yes |
| Cycle detection (directed) | No — use topo sort | Yes (3-state DFS) |
| Component size query | Yes (with size array) | Yes |
| Simplicity | Slightly more setup | Often simpler |

**Rule of thumb:** if edges are added dynamically or you just need "same component?" queries, use DSU. If you need traversal order, paths, or distances, use BFS/DFS.

---

## Problems to Know

| Problem | LC | Pattern | Key observation |
|---------|----|---------|----------------|
| Number of Connected Components | 323 | count components | `components = n`, decrement on each merge |
| Redundant Connection | 684 | cycle detection | first edge where `union` returns False |
| Graph Valid Tree | 261 | cycle + connectivity | no cycle AND exactly `n-1` edges |
| Accounts Merge | 721 | string nodes | emails as DSU keys, group by root |
| Number of Islands II | 305 | dynamic connectivity | add cells one by one, union neighbors |
| Min Cost to Connect All Points | 1584 | Kruskal's MST | sort edges, union greedily |
| Satisfiability of Equality Equations | 990 | two-pass | process `==` first, then check `!=` |
| Swim in Rising Water | 778 | MST variant | binary search or Kruskal's on grid |

---

## Satisfiability of Equality Equations (LC 990) — Two-Pass Pattern

**Problem:** given equations like `["a==b","b!=c","c==a"]`, return whether all are satisfiable simultaneously.

```python
def equationsPossible(equations):
    parent = list(range(26))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    # Pass 1: process all == equations first
    for eq in equations:
        if eq[1] == '=':
            union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))

    # Pass 2: check all != equations don't contradict
    for eq in equations:
        if eq[1] == '!':
            if find(ord(eq[0]) - ord('a')) == find(ord(eq[3]) - ord('a')):
                return False   # != but same component → contradiction
    return True
```

**Key:** process equality constraints first (build the components), then verify inequality constraints don't contradict them. Order matters.
