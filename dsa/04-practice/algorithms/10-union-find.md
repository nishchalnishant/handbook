---
tags: [coding, algorithms, union-find]
topic: Union-Find (DSU)
difficulty: mixed
---
# Union-Find — Problem Deep Dives

## What this covers

> [!abstract] In this file
> **Covers:** Worked DSU problems: template, connectivity, weighted DSU, Kruskal, offline union, grid DSU.
> **You'll be able to:** Spot DSU problems and code the template in 2 min.
> **Prereqs:** Union-Find lecture · **Pair with:** [Union-Find lecture](../../03-algorithms/10-union-find.md) · **Time:** 2 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [DSU Template](#dsu-template) · [Basic Union-Find](#basic-union-find) · [Weighted / Ranked Union-Find](#weighted--ranked-union-find) · [MST (Kruskal's)](#mst-kruskals) · [Dynamic / Offline Union-Find](#dynamic--offline-union-find) · [DSU for Other Problems](#dsu-for-other-problems) · [Directed Graph Union-Find](#directed-graph-union-find) · [Grid / Coordinate Union-Find](#grid--coordinate-union-find) · [Weighted / Partial Swap Union-Find](#weighted--partial-swap-union-find) · [Connectivity With Constraints](#connectivity-with-constraints)

> [!tip] If you only have 20 minutes
> **Do these first:** [Number of Connected Components in an Undirected Graph](#basic-union-find) · [Graph Valid Tree](#graph-valid-tree--t1) · [Accounts Merge (Email Graph)](#accounts-merge-email-graph--t1) · [Satisfiability of Equality Equations](#satisfiability-of-equality-equations--t1) · [Number of Islands II](#number-of-islands-ii--t1) · [Redundant Connection II (LC 685, Directed Graph)](#redundant-connection-ii-lc-685-directed-graph--t1) · [Making a Large Island](#making-a-large-island--t1) · [Min Cost to Connect All Points](#mst-kruskals)
> **Template:** `def find(x): while p[x] != x: p[x] = p[p[x]]; x = p[x]; return x` · `union` returns `False` if already joined — that is your cycle detector.
> **Template:** Kruskal: sort edges by weight, union if `find(u) != find(v)`, stop at `n-1` edges.
> **Gotchas:** Always compare roots, never `p[u] == p[v]` · track `components -= 1` on successful union · Graph Valid Tree = exactly `n-1` edges AND no cycle · map non-integer keys (emails, cells) to ids first.

---

## DSU Template

> [!note]- DSU Class (Python)
> ```python
> class DSU:
>     def __init__(self, n):
>         self.parent = list(range(n))
>         self.rank = [0] * n
>         self.size = [1] * n
>         self.components = n
> 
>     def find(self, x):
>         if self.parent[x] != x:
>             self.parent[x] = self.find(self.parent[x])  # path compression
>         return self.parent[x]
> 
>     def union(self, x, y):
>         rx, ry = self.find(x), self.find(y)
>         if rx == ry:
>             return False          # already connected
>             cycle in undirected graph
>         if self.rank[rx] < self.rank[ry]:
>             rx, ry = ry, rx
>         self.parent[ry] = rx
>         self.size[rx] += self.size[ry]
>         if self.rank[rx] == self.rank[ry]:
>             self.rank[rx] += 1
>         self.components -= 1
>         return True
> 
>     def connected(self, x, y):
>         return self.find(x) == self.find(y)
> 
>     def component_size(self, x):
>         return self.size[self.find(x)]
> ```

> [!info] Core Invariants
> All nodes in the same component share the same root after `find`. Path compression + union by rank gives amortized O(α(n)) ≈ O(1) per operation.

---

## Basic Union-Find

---

### Number of Provinces (Matrix Form) `⚡ T1`

> [!example] Problem
> There are n cities. Some of them are connected, while some are not. If city a is connected directly with city b, and city b is connected directly with city c, then city a is connected indirectly with city c.
> A province is a group of directly or indirectly connected cities and no other cities outside of the group.
> You are given an n x n matrix isConnected where isConnected[i][j] = 1 if the ith city and the jth city are directly connected, and isConnected[i][j] = 0 otherwise.
> Return the total number of provinces.
> 
> **Example 1:**
> ```
> Input: isConnected = [[1,1,0],[1,1,0],[0,0,1]]
> Output: 2
> ```
> 
> **Example 2:**
> ```
> Input: isConnected = [[1,0,0],[0,1,0],[0,0,1]]
> Output: 3
> ```
> 
> **Constraints:**
> - 1 <= n <= 200
> - n == isConnected.length
> - n == isConnected[i].length
> - isConnected[i][j] is 1 or 0.
> - isConnected[i][i] == 1
> - isConnected[i][j] == isConnected[j][i]

> [!info] Approach
> Adjacency matrix encodes undirected edges. Treat `isConnected[i][j] == 1` as edge `(i, j)`. Iterate upper triangle, union connected pairs; count components. Only process upper triangle (`j > i`) to avoid redundant unions and double-decrementing.

> [!note]- Python Solution
> ```python
> def find_circle_num(isConnected):
>     n = len(isConnected)
>     dsu = DSU(n)
>     for i in range(n):
>         for j in range(i + 1, n):    # upper triangle only
>             if isConnected[i][j] == 1:
>                 dsu.union(i, j)
>     return dsu.components
> ```

> [!success] Complexity
> Time O(V²·α(V)) ≈ O(V²), Space O(V).

> [!tip] Alternatives
> DFS on adjacency matrix — same O(V²). DSU more explicit about component counting.

---

### Graph Valid Tree `⚡ T1`

> [!example] Problem
> You have a graph of `n` nodes labeled from `0` to `n - 1`. You are given an integer n and a list of `edges` where `edges[i] = [a_i, b_i]` indicates that there is an undirected edge between nodes `a_i` and `b_i` in the graph.
> 
> Return `true` *if the edges of the given graph make up a valid tree, and* `false` *otherwise*.
> 
>  
> 
> Example 1:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[0,2],[0,3],[1,4]]
> **Output:** true
> 
> ```
> 
> Example 2:
> 
> ```
> 
> **Input:** n = 5, edges = [[0,1],[1,2],[2,3],[1,3],[1,4]]
> **Output:** false
> 
> ```
> 
>  
> 
> **Constraints:**
> 
> 	
> - `1 <= n <= 2000`
> 	
> - `0 <= edges.length <= 5000`
> 	
> - `edges[i].length == 2`
> 	
> - `0 <= a_i, b_i < n`
> 	
> - `a_i != b_i`
> 	
> - There are no self-loops or repeated edges.

> [!failure] Tempting wrong approach
> Checking only "no cycle" — a forest also has none. Also require exactly `n - 1` edges (equivalently, one component).

> [!info] Approach
> A valid tree on `n` nodes has exactly `n-1` edges and no cycles — equivalently, it is connected and acyclic. DSU cycle detection + single-component check. Short-circuit if `len(edges) != n-1`. Process edges; if any union returns `False` (cycle) → not a tree.

> [!note]- Python Solution
> ```python
> def valid_tree(n, edges):
>     if len(edges) != n - 1:
>         return False            # necessary condition
>     dsu = DSU(n)
>     for u, v in edges:
>         if not dsu.union(u, v):
>             return False        # cycle detected
>     return dsu.components == 1
> ```

> [!success] Complexity
> Time O(E·α(V)) ≈ O(E), Space O(V).

> [!tip] Alternatives
> DFS — check connected + no cycle. Both correct; DSU is more declarative.

---

### Satisfiability of Equality Equations `⚡ T1`

> [!example] Problem
> You are given an array of strings equations that represent relationships between variables where each string equations[i] is of length 4 and takes one of two different forms: "xi==yi" or "xi!=yi".Here, xi and yi are lowercase letters (not necessarily different) that represent one-letter variable names.
> Return true if it is possible to assign integers to variable names so as to satisfy all the given equations, or false otherwise.
> 
> **Example 1:**
> ```
> Input: equations = ["a==b","b!=a"]
> Output: false
> Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
> There is no way to assign the variables to satisfy both equations.
> ```
> 
> **Example 2:**
> ```
> Input: equations = ["b==a","a==b"]
> Output: true
> Explanation: We could assign a = 1 and b = 1 to satisfy both equations.
> ```
> 
> **Constraints:**
> - 1 <= equations.length <= 500
> - equations[i].length == 4
> - equations[i][0] is a lowercase letter.
> - equations[i][1] is either '=' or '!'.
> - equations[i][2] is '='.
> - equations[i][3] is a lowercase letter.

> [!info] Approach
> `==` is transitive. Must union all equal pairs before checking inequalities — single-pass fails on ordering. Pass 1: union all `==` pairs. Pass 2: verify no `!=` pair has both sides in the same component. 26 lowercase letters → DSU of size 26. If `find(x) == find(y)` for a `!=` constraint → contradiction.

> [!note]- Python Solution
> ```python
> def equations_possible(equations):
>     dsu = DSU(26)   # 26 lowercase letters
> 
>     for eq in equations:
>         if eq[1] == '=':    # "a==b"
>             dsu.union(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a'))
> 
>     for eq in equations:
>         if eq[1] == '!':    # "a!=b"
>             if dsu.connected(ord(eq[0]) - ord('a'), ord(eq[3]) - ord('a')):
>                 return False
> 
>     return True
> ```

> [!success] Complexity
> Time O(26·α(26)) = O(1), Space O(26) = O(1).

> [!tip] Alternatives
> Graph coloring / BFS — build equality groups then check inequality constraints. DSU is cleaner.

**Also try:**

- **Number of Connected Components in an Undirected Graph** — BFS/DFS counts components in O(V+E) per call — fine for one-shot

---

## Weighted / Ranked Union-Find

---

### Accounts Merge (Email Graph) `⚡ T1`

> [!example] Problem
> Given a list of accounts where each element accounts[i] is a list of strings, where the first element accounts[i][0] is a name, and the rest of the elements are emails representing emails of the account.
> Now, we would like to merge these accounts. Two accounts definitely belong to the same person if there is some common email to both accounts. Note that even if two accounts have the same name, they may belong to different people as people could have the same name. A person can have any number of accounts initially, but all of their accounts definitely have the same name.
> After merging the accounts, return the accounts in the following format: the first element of each account is the name, and the rest of the elements are emails in sorted order. The accounts themselves can be returned in any order.
> 
> **Example 1:**
> ```
> Input: accounts = [["John","johnsmith@mail.com","john_newyork@mail.com"],["John","johnsmith@mail.com","john00@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Output: [["John","john00@mail.com","john_newyork@mail.com","johnsmith@mail.com"],["Mary","mary@mail.com"],["John","johnnybravo@mail.com"]]
> Explanation:
> The first and second John's are the same person as they have the common email "johnsmith@mail.com".
> The third John and Mary are different people as none of their email addresses are used by other accounts.
> We could return these lists in any order, for example the answer [['Mary', 'mary@mail.com'], ['John', 'johnnybravo@mail.com'], 
> ['John', 'john00@mail.com', 'john_newyork@mail.com', 'johnsmith@mail.com']] would still be accepted.
> ```
> 
> **Example 2:**
> ```
> Input: accounts = [["Gabe","Gabe0@m.co","Gabe3@m.co","Gabe1@m.co"],["Kevin","Kevin3@m.co","Kevin5@m.co","Kevin0@m.co"],["Ethan","Ethan5@m.co","Ethan4@m.co","Ethan0@m.co"],["Hanzo","Hanzo3@m.co","Hanzo1@m.co","Hanzo0@m.co"],["Fern","Fern5@m.co","Fern1@m.co","Fern0@m.co"]]
> Output: [["Ethan","Ethan0@m.co","Ethan4@m.co","Ethan5@m.co"],["Gabe","Gabe0@m.co","Gabe1@m.co","Gabe3@m.co"],["Hanzo","Hanzo0@m.co","Hanzo1@m.co","Hanzo3@m.co"],["Kevin","Kevin0@m.co","Kevin3@m.co","Kevin5@m.co"],["Fern","Fern0@m.co","Fern1@m.co","Fern5@m.co"]]
> ```
> 
> **Constraints:**
> - 1 <= accounts.length <= 1000
> - 2 <= accounts[i].length <= 10
> - 1 <= accounts[i][j].length <= 30
> - accounts[i][0] consists of English letters.
> - accounts[i][j] (for j > 0) is a valid email.

> [!failure] Tempting wrong approach
> Merging by account name — different people share names. Union on emails; names are only labels.

> [!info] Approach
> Emails are the identity key, not names. Accounts sharing any email are the same person — transitive merging is DSU. DSU over all unique emails (map each to integer index). Union all emails within an account. Group by DSU root; sort per group. Map `email → index`. For each account, union the first email with all subsequent ones. After all unions, group indices by root.

> [!note]- Python Solution
> ```python
> from collections import defaultdict
> 
> def accounts_merge(accounts):
>     email_to_idx = {}
>     email_to_name = {}
> 
>     for account in accounts:
>         name = account[0]
>         for email in account[1:]:
>             if email not in email_to_idx:
>                 email_to_idx[email] = len(email_to_idx)
>             email_to_name[email] = name
> 
>     dsu = DSU(len(email_to_idx))
> 
>     for account in accounts:
>         first_idx = email_to_idx[account[1]]
>         for email in account[2:]:
>             dsu.union(first_idx, email_to_idx[email])
> 
>     root_to_emails = defaultdict(list)
>     for email, idx in email_to_idx.items():
>         root_to_emails[dsu.find(idx)].append(email)
> 
>     result = []
>     for root, emails in root_to_emails.items():
>         name = email_to_name[emails[0]]
>         result.append([name] + sorted(emails))
> 
>     return result
> ```

> [!success] Complexity
> Time O(N·K·log(N·K)) dominated by sorting, Space O(N·K).

> [!tip] Alternatives
> BFS on email adjacency graph — build `email → [co-account emails]` map, BFS for components. Same complexity, more code.

**Also try:**

- **Evaluate Division (Weighted DSU)** — Variables are nodes; edges are ratios

---

## MST (Kruskal's)

**Also try:**

- **Min Cost to Connect All Points** — Complete graph MST
- **Critical Connections / Pseudo-Critical Edges in MST** — An edge is critical if excluding it raises MST cost

---

## Dynamic / Offline Union-Find

---

### Number of Islands II `⚡ T1`

> [!example] Problem
> An `m x n` grid starts as all water. `positions[i] = [r, c]` turns cell `(r, c)` into land. After each operation return the number of islands (4-directionally connected land).
>
> **Example:** `m=3, n=3, positions=[[0,0],[0,1],[1,2],[2,1]]` → `[1,1,2,3]`

> [!info] Approach
> Islands are connected components growing dynamically. Re-running BFS is O(M·N) per operation. DSU handles each addition in O(α) — orders of magnitude faster. DSU on 2D grid encoded as `r*cols + c`. On `addLand`, increment component count, then union with adjacent land cells. Track which cells are land (set). Skip duplicate additions. DSU's `union` automatically decrements component count on merge.

> [!note]- Python Solution
> ```python
> def num_islands2(m, n, positions):
>     dsu = DSU(m * n)
>     dsu.components = 0       # override: start with 0 islands
>     land = set()
>     result = []
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for r, c in positions:
>         idx = r * n + c
>         if idx in land:
>             result.append(dsu.components)
>             continue
>         land.add(idx)
>         dsu.components += 1          # new land cell = new island
>         for dr, dc in dirs:
>             nr, nc = r + dr, c + dc
>             nidx = nr * n + nc
>             if 0 <= nr < m and 0 <= nc < n and nidx in land:
>                 dsu.union(idx, nidx)  # merges components, decrements count
>         result.append(dsu.components)
> 
>     return result
> ```

> [!success] Complexity
> Time O(K·α(M·N)) where K = operations, Space O(M·N).

> [!tip] Alternatives
> Re-run BFS after each addition — O(K·M·N). Offline: process in reverse (deletions → additions). DSU is optimal for online queries.

**Also try:**

- **Minimize Malware Spread** — Malware spreads to the entire connected component

---

## DSU for Other Problems

---

### Longest Consecutive Sequence (DSU Approach) `⚡ T1`

> [!example] Problem
> Same problem as [Longest Consecutive Sequence](../data-structures/02-hashing.md#longest-consecutive-sequence--t1) — this section covers the alternative approach only.

> [!info] Approach
> `x` and `x+1` belong to the same consecutive run — union them. The largest component size is the answer. Map each value to an index; union `x` with `x+1` if `x+1` exists. Max component size = answer. Build `val → index` map. For each value, if `val+1` exists, union their indices.

> [!note]- Python Solution
> ```python
> def longest_consecutive(nums):
>     if not nums:
>         return 0
>     val_to_idx = {v: i for i, v in enumerate(nums)}
>     dsu = DSU(len(nums))
> 
>     for val, idx in val_to_idx.items():
>         if val + 1 in val_to_idx:
>             dsu.union(idx, val_to_idx[val + 1])
> 
>     return max(dsu.component_size(i) for i in range(len(nums)))
> ```

> [!success] Complexity
> Time O(N·α(N)) ≈ O(N), Space O(N).

> [!tip] Alternatives
> Hash set (canonical) — for each `x` where `x-1` not in set (sequence start), expand right. O(N), simpler. DSU is a valid alternative but hash set is preferred in interviews for this problem.

**Also try:**

- **Path with Maximum Probability (Weighted DSU)** — For general graphs Dijkstra (max-heap variant) is canonical and handles multiple alternate paths

---

## Directed Graph Union-Find

---

### Redundant Connection II (LC 685, Directed Graph) `⚡ T1`

> [!example] Problem
> In this problem, a rooted tree is a directed graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.
> The given input is a directed graph that started as a rooted tree with n nodes (with distinct values from 1 to n), with one additional directed edge added. The added edge has two different vertices chosen from 1 to n, and was not an edge that already existed.
> The resulting graph is given as a 2D-array of edges. Each element of edges is a pair [ui, vi] that represents a directed edge connecting nodes ui and vi, where ui is a parent of child vi.
> Return an edge that can be removed so that the resulting graph is a rooted tree of n nodes. If there are multiple answers, return the answer that occurs last in the given 2D-array.
> 
> **Example 1:**
> ```
> Input: edges = [[1,2],[1,3],[2,3]]
> Output: [2,3]
> ```
> 
> **Example 2:**
> ```
> Input: edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
> Output: [4,1]
> ```
> 
> **Constraints:**
> - n == edges.length
> - 3 <= n <= 1000
> - edges[i].length == 2
> - 1 <= ui, vi <= n
> - ui != vi

> [!info] Approach
> In a directed rooted tree, every node except the root has exactly one parent. Adding an edge creates either: (a) a node with two parents, or (b) a cycle, or both. We must identify which case applies and choose the correct redundant edge. First pass: find any node with two incoming edges (`cand1`, `cand2`). If found, one of them is the answer. Second pass: use Union-Find ignoring one candidate. If a cycle forms, the other candidate (or the cycle-forming edge) is the answer.

>   1. Scan edges; track `parent` for each node. If a node already has a parent, record `cand1 = prev_edge`, `cand2 = current_edge` and skip `cand2`.
>   2. Run Union-Find on remaining edges. If a cycle forms and `cand1` exists, return `cand1`; else return the cycle edge. If no cycle and `cand2` exists, return `cand2`.

> [!note]- Python Solution
> ```python
> def find_redundant_directed_connection(edges):
>     n = len(edges)
>     parent = list(range(n + 1))
>     cand1 = cand2 = None
>     node_parent = {}
>     filtered = []
>     for u, v in edges:
>         if v in node_parent:
>             cand1 = [node_parent[v], v]
>             cand2 = [u, v]
>         else:
>             node_parent[v] = u
>             filtered.append([u, v])
> >
>     def find(x):
>         while parent[x] != x:
>             parent[x] = parent[parent[x]]
>             x = parent[x]
>         return x
> >
>     def union(u, v):
>         pu = find(u)
>         pv = find(v)
>         if pu == pv:
>             return False
>         parent[pu] = pv
>         return True
> >
>     for u, v in filtered:
>         if not union(u, v):
>             return cand1 if cand1 else [u, v]
>     return cand2
> ```

> [!success] Complexity
> Time O(E α(E)), Space O(E).

> [!tip] Alternatives
> - Pure DFS cycle detection: works but harder to correctly handle the "two parents" case.
> - Key insight: the two cases (double-parent vs pure cycle) require different edge choices; the filtering step separates them cleanly.

---

## Grid / Coordinate Union-Find

**Also try:**

- **Most Stones Removed with Same Row or Column** — Stones in the same connected component (row/column sharing is transitive) can all be reduced to 1 stone

---

## Weighted / Partial Swap Union-Find

**Also try:**

- **Minimize Hamming Distance After Swap Operations** — Swap pairs define groups of indices that can be freely rearranged among themselves
- **Smallest String With Swaps (LC 1202)** — Indices connected by swap pairs (directly or transitively) can be rearranged freely

---

## Connectivity With Constraints

---

### Making a Large Island `⚡ T1`

> [!example] Problem
> You are given an n x n binary matrix grid. You are allowed to change at most one 0 to be 1.
> Return the size of the largest island in grid after applying this operation.
> An island is a 4-directionally connected group of 1s.
> 
> **Example 1:**
> ```
> Input: grid = [[1,0],[0,1]]
> Output: 3
> Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.
> ```
> 
> **Example 2:**
> ```
> Input: grid = [[1,1],[1,0]]
> Output: 4
> Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.
> ```
> 
> **Example 3:**
> ```
> Input: grid = [[1,1],[1,1]]
> Output: 4
> Explanation: Can't change any 0 to 1, only one island with area = 4.
> ```
> 
> **Constraints:**
> - n == grid.length
> - n == grid[i].length
> - 1 <= n <= 500
> - grid[i][j] is either 0 or 1.

> [!info] Approach
> After flipping a 0, the new cell connects up to 4 adjacent islands. Island sizes are needed instantly → DSU component sizes. Build DSU over existing 1-cells. For each 0-cell, sum sizes of distinct adjacent components + 1. Track overall max. Label each cell's DSU root. For each 0-cell, collect unique roots of neighboring 1-cells (avoid double-counting same component), sum their sizes.

> [!note]- Python Solution
> ```python
> def largest_island(grid):
>     n = len(grid)
>     dsu = DSU(n * n)
>     dirs = [(1,0),(-1,0),(0,1),(0,-1)]
> 
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 1:
>                 for dr, dc in dirs:
>                     nr, nc = r + dr, c + dc
>                     if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
>                         dsu.union(r*n+c, nr*n+nc)
> 
>     best = max((dsu.component_size(r*n+c) for r in range(n)
>                 for c in range(n) if grid[r][c] == 1), default=0)
> 
>     for r in range(n):
>         for c in range(n):
>             if grid[r][c] == 0:
>                 seen_roots = set()
>                 gain = 1
>                 for dr, dc in dirs:
>                     nr, nc = r + dr, c + dc
>                     if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
>                         root = dsu.find(nr*n+nc)
>                         if root not in seen_roots:
>                             gain += dsu.component_size(nr*n+nc)
>                             seen_roots.add(root)
>                 best = max(best, gain)
> 
>     return best
> ```

> [!success] Complexity
> Time O(N²·α(N²)) ≈ O(N²), Space O(N²).

> [!tip] Alternatives
> BFS to label islands and record sizes — O(N²). Same idea, slightly more setup. DSU makes the component-size lookup natural.

**Also try:**

- **Minimum Cost to Make at Least One Valid Path in a Grid** — Edge weights are 0 (follow direction) or 1 (change direction)
- **Remove Max Number of Edges to Keep Graph Fully Traversable** — We want minimal spanning forest for Alice and Bob independently
- **Number of Good Paths** — Process nodes in increasing order of value
- **Largest Component Size by Common Factor** — Shared prime factors link numbers together transitively

---

## See Also

[[graph]] | [[graph-algorithms]] | [[sorting]]
[[graph]] | [[sorting]] | [[backtracking]] | [[dynamic-programming]]
