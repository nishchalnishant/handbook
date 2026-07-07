# DFS — All Variations

---

## ⚡ Cheat Sheet (Quick Revision)

**3 questions before writing DFS:**
1. What am I tracking on the way **down**? (path, remaining target, depth)
2. What do I return on the way **up**? (value to combine, True/False, nothing)
3. Do I need to **undo** anything on backtrack? (path.pop(), restore grid cell)

| Situation | Variation | Key detail |
|-----------|-----------|-----------|
| Tree height / sum / min | Return value, postorder | `return 1 + max(left, right)` |
| Tree global max (diameter, max path) | Return value + `best[0]` | update global with `l+r`, return `max(l,r)+1` upward |
| All root-to-leaf paths | Path tracking | `res.append(path[:])` — snapshot, not reference |
| Lowest common ancestor | LCA postorder | both sides non-None → current node is LCA |
| Connected components | Graph DFS + outer loop | mark visited before recursing |
| Island count / flood fill | Grid DFS | bounds check before `grid[r][c]` access |
| Cycle in directed graph | 3-state (0/1/2) | state 1 = on current stack = cycle if revisited |
| Cycle in undirected graph | DFS + parent | `elif nei != parent: return True` |
| Subsets / permutations | Backtracking | choose → recurse → unchoose |
| Topological order | Postorder + reverse | append node AFTER all descendants |
| Very deep tree | Iterative DFS | explicit stack, right pushed before left |

**The 4 rules that never change:**
1. Base case first — check `if not node` before anything else
2. Mark visited before recursing — not after
3. Snapshot mutable state — `path[:]` not `path` when saving to results
4. Backtrack after recursing — every `append` needs a matching `pop`

**Return value pattern (most common):**
```python
def dfs(node):
    if not node: return BASE          # 0 for sum/depth, inf for min, True for validity
    left = dfs(node.left)
    right = dfs(node.right)
    return COMBINE(left, right, node.val)
```

**Global max pattern (diameter / max path sum):**
```python
best = [0]
def dfs(node):
    if not node: return 0
    l, r = dfs(node.left), dfs(node.right)
    best[0] = max(best[0], l + r)    # spans across node — update global
    return 1 + max(l, r)             # only one branch goes upward
```

**Backtracking pattern:**
```python
def backtrack(start, path):
    result.append(path[:])           # snapshot
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)       # i+1 = no reuse; i = reuse allowed
        path.pop()
```

**3-state cycle detection (directed):**
```python
# 0=unvisited, 1=in current path, 2=done
if state[node] == 1: return True    # cycle
if state[node] == 2: return False   # safe, already finished
state[node] = 1
for nei in graph[node]:
    if dfs(nei): return True
state[node] = 2
result.append(node)                 # postorder → reverse for topo sort
```

**Common mistakes:**
- Using 3-state for undirected graphs → false positives (every edge looks like a back edge)
- `res.append(path)` instead of `path[:]` → all results are empty lists at the end
- Not marking visited before recursing → infinite loop on cycles
- Forgetting `path.pop()` → path accumulates across branches

---

One idea: go deep, backtrack, repeat. Everything below is a variation of that.

---

## How to Think About DFS

DFS answers the question: "what can I reach from here, and what does the path look like?"

The core mental model: you're exploring a maze. You pick a corridor, follow it until you hit a dead end or the exit, then backtrack to the last fork and try the next corridor. The recursion stack IS the path you're currently on — each stack frame is one step deeper into the maze.

**Three things to decide before writing DFS:**
1. **What am I tracking on the way down?** (remaining target, current path, current depth)
2. **What do I return on the way up?** (a value to combine, True/False, or nothing)
3. **Do I need to undo anything when I backtrack?** (path.pop(), restore grid cell)

If you answer these three, the code writes itself.

---

## The Core Template

```python
def dfs(node, visited):
    if base_case:
        return
    visited.add(node)
    for neighbor in get_neighbors(node):
        if neighbor not in visited:
            dfs(neighbor, visited)
```

---

## Variation 1 — Binary Tree: Preorder / Inorder / Postorder

**The mental model:** the three orders are just about *when* you process the current node relative to its children.

- **Preorder** (node → left → right): you process the node the moment you arrive. Useful when the parent's value is needed before exploring children — serialization, copying.
- **Inorder** (left → node → right): you process the node *between* its children. For a BST, left subtree < node < right subtree, so inorder gives sorted output.
- **Postorder** (left → right → node): you process the node only after both children return. Use when the node's answer depends on children's answers — subtree size, height, diameter.

```python
def preorder(root):       # node → left → right
    if not root: return
    print(root.val)
    preorder(root.left)
    preorder(root.right)

def inorder(root):        # left → node → right  (gives sorted order for BST)
    if not root: return
    inorder(root.left)
    print(root.val)
    inorder(root.right)

def postorder(root):      # left → right → node  (children before parent)
    if not root: return
    postorder(root.left)
    postorder(root.right)
    print(root.val)
```

**When to use:**
- Preorder: serialize tree, copy tree, prefix expression
- Inorder: BST sorted output, kth smallest, validate BST
- Postorder: delete tree, compute subtree values (diameter, max path sum)

---

## Variation 2 — Tree: Return Value Pattern (most common at L3)

**The mental model:** postorder DFS where each call returns a value upward, and the parent combines children's values to compute its own answer.

The shape is always:
1. Ask left child: `left = dfs(node.left)`
2. Ask right child: `right = dfs(node.right)`
3. Combine + return: `return f(left, right, node.val)`

**Why postorder?** Because the parent needs the children's answers before it can compute its own. You can't know a node's height until you know how tall both subtrees are.

**The global-max pattern:** when the answer can span *across* a node (not just through it upward), update a global variable at each node, but return only the "upward useful" portion. Diameter and max path sum both use this.

```python
def dfs(node):
    if not node:
        return BASE_VALUE       # 0 for sum/depth, float('inf') for min, True for validity

    left  = dfs(node.left)
    right = dfs(node.right)

    # combine left + right + node.val → return result upward
    return COMBINE(left, right, node.val)
```

**Max depth:**
```python
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
# "my height = 1 (me) + taller of my two subtrees"
```

**Diameter (global max, local return):**
```python
def diameter(root):
    best = [0]
    def dfs(node):
        if not node: return 0
        l, r = dfs(node.left), dfs(node.right)
        best[0] = max(best[0], l + r)   # diameter through this node = l + r
        return 1 + max(l, r)            # but upward, only one branch can be used
    dfs(root)
    return best[0]
# Why two values? The path through a node can use both branches (l+r),
# but its parent can only extend one branch. So update global with l+r,
# return max(l,r)+1 upward.
```

**Max path sum (same shape as diameter):**
```python
def max_path_sum(root):
    best = [float('-inf')]
    def dfs(node):
        if not node: return 0
        l = max(dfs(node.left), 0)      # ignore negative branches — don't extend them
        r = max(dfs(node.right), 0)
        best[0] = max(best[0], l + r + node.val)
        return node.val + max(l, r)
    dfs(root)
    return best[0]
# The max(branch, 0) trick: if a subtree's contribution is negative, treat it as 0
# (don't include it in the path). This handles all-negative trees correctly.
```

**Balanced tree:**
```python
def is_balanced(root):
    def dfs(node):
        if not node: return 0
        l = dfs(node.left)
        r = dfs(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1:
            return -1               # -1 = unbalanced signal propagated upward
        return 1 + max(l, r)
    return dfs(root) != -1
# Sentinel value trick: use -1 as "poison" — once any subtree is unbalanced,
# -1 bubbles all the way up without extra checks.
```

---

## Variation 3 — Tree: Path Tracking

**The mental model:** carry a running path list down through the recursion. Add the current node on the way in, record a snapshot when you hit a target condition, then remove it on the way out (backtrack). The list always reflects exactly the nodes on the current root-to-here path.

**Why `path[:]` not `path`?** `path` is a reference to the same list object. By the time the caller uses it, the list will have been modified by subsequent backtracking. `path[:]` creates a snapshot copy at this exact moment.

```python
def path_sum(root, target):
    res = []
    def dfs(node, remaining, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            res.append(path[:])         # snapshot — never append path directly
        dfs(node.left,  remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        path.pop()                      # backtrack: undo before returning to parent
    dfs(root, target, [])
    return res
```

**The backtrack rule:** every `append` must have a matching `pop` on the way out. The path list must be in the same state when you return as when you entered.

---

## Variation 4 — Tree: LCA (Lowest Common Ancestor)

**The mental model:** do postorder DFS. At each node, ask both subtrees: "do you contain p or q?" The first node where both subtrees answer yes (or the node itself is p or q) is the LCA.

**Why does this work?** If both left and right return non-None, the current node is the split point — one target is in each subtree, so this node is their deepest common ancestor. If only one side returns non-None, bubble that result upward (both targets are on the same side).

```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root         # found one of the targets (or ran out of tree)
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    return root if left and right else left or right
# both sides found something → current node is LCA
# one side found something → pass it up (the other target is deeper on that side)
```

---

## Variation 5 — Graph DFS (adjacency list)

**The mental model:** same as tree DFS, but graphs can have cycles, so you need a `visited` set. Without it, you'd follow edges in circles forever.

**Why mark visited before recursing (not after)?** If you mark after, and there's a cycle A→B→A, you'd call `dfs(A)` again from B before A is marked — infinite recursion.

```python
def dfs(graph, node, visited):
    visited.add(node)               # mark immediately when you enter
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

# Count connected components — outer loop handles disconnected graphs
def count_components(n, edges):
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            dfs(graph, node, visited)
            count += 1              # each fresh DFS = one new component
    return count
```

**Why the outer loop?** A single DFS from node 0 only reaches nodes connected to 0. If the graph is disconnected, other components are invisible without the outer loop. Always outer-loop over all nodes when the graph might be disconnected.

---

## Variation 6 — Grid DFS (2D matrix)

**The mental model:** the grid IS the graph. Each cell is a node; its neighbors are the 4 adjacent cells. DFS floods out from a starting cell, marking cells as visited as it goes.

**Two ways to track visited:**
- `visited` set: non-destructive, needed when you can't modify the input
- In-place marking (overwrite the cell): saves memory, fine when you can mutate the grid or only need a count

```python
def dfs(grid, r, c, visited):
    ROWS, COLS = len(grid), len(grid[0])
    if r < 0 or r >= ROWS or c < 0 or c >= COLS:
        return
    if (r, c) in visited or grid[r][c] == '0':
        return
    visited.add((r, c))
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r+dr, c+dc, visited)
```

**In-place marking (no visited set — mutate grid):**
```python
def dfs(grid, r, c):
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return
    if grid[r][c] != '1':
        return
    grid[r][c] = '#'               # mark visited in-place
    for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
        dfs(grid, r+dr, c+dc)
```

**Number of Islands — same outer-loop pattern as connected components:**
```python
def num_islands(grid):
    count = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == '1':
                dfs(grid, r, c)     # floods the entire island, marking it '#'
                count += 1          # every time you start a flood = new island
    return count
```

**Bounds check order matters:** check `r < 0 or r >= ROWS or c < 0 or c >= COLS` *before* accessing `grid[r][c]` — Python doesn't short-circuit array access.

---

## Variation 7 — Cycle Detection in Directed Graph

**The mental model:** a cycle in a directed graph means you can follow edges and loop back to a node you're currently visiting. "Currently visiting" is the key — if you've *fully finished* a node (explored all its descendants), revisiting it doesn't create a cycle.

**Why 3 states instead of 2?** With 2 states (visited/unvisited), you can't tell whether a node was visited in this current path or in a completely different path. State 1 = "I'm in the middle of exploring this node right now" = on the current stack. Reaching a state-1 node means you've looped back.

```python
def has_cycle(n, edges):
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    state = [0] * n         # 0=unvisited, 1=in-path (on current stack), 2=done

    def dfs(node):
        if state[node] == 1: return True    # back edge → cycle
        if state[node] == 2: return False   # already fully explored, safe to skip
        state[node] = 1
        for nei in graph[node]:
            if dfs(nei): return True
        state[node] = 2                     # mark done only after all descendants explored
        return False

    return any(dfs(i) for i in range(n) if state[i] == 0)
```

**For undirected graph**, 3 states aren't needed — use parent tracking instead. The reason: in an undirected graph, every edge u-v appears as both u→v and v→u. When you're at v having come from u, you'll see u as a neighbor — but that's just the edge you came from, not a cycle. Track `parent` to ignore it.

```python
def dfs(node, parent, visited, graph):
    visited.add(node)
    for nei in graph[node]:
        if nei not in visited:
            if dfs(nei, node, visited, graph):
                return True
        elif nei != parent:             # seen AND not the edge we came from = real cycle
            return True
    return False
```

**The trap:** don't use 3-state coloring for undirected graphs — the parent edge always looks like a "back edge" with that approach, giving false positives.

---

## Variation 8 — Backtracking DFS

**The mental model:** explore every possible choice, but undo each choice after you're done with it so the next branch starts from a clean state. Think of it as a decision tree — at each node you try all options, recurse, then undo.

**The three-step pattern:**
1. **Choose:** add to path / mark as used
2. **Explore:** recurse
3. **Unchoose:** remove from path / unmark

```python
def backtrack(start, path):
    result.append(path[:])         # record current state (snapshot!)
    for i in range(start, len(nums)):
        path.append(nums[i])
        backtrack(i + 1, path)     # i+1: no reuse. i: reuse allowed
        path.pop()                 # undo — must match every append
```

**Why `i+1` vs `i`?** `i+1` means "don't pick the same index twice" (combinations/subsets). `i` means "you can pick this element again" (combinations with repetition). The start index controls reuse.

**Pruning duplicates** (when input has duplicates, e.g. LC 40):
```python
nums.sort()          # sort first so duplicates are adjacent
for i in range(start, len(nums)):
    if i > start and nums[i] == nums[i-1]:
        continue     # skip duplicate at same recursion level
```

**Word Search on grid:**
```python
def exist(board, word):
    ROWS, COLS = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word): return True          # matched all characters
        if r < 0 or r >= ROWS or c < 0 or c >= COLS: return False
        if board[r][c] != word[i]: return False
        tmp, board[r][c] = board[r][c], '#'    # choose: mark visited
        found = any(dfs(r+dr, c+dc, i+1) for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)])
        board[r][c] = tmp                       # unchoose: restore (backtrack)
        return found

    return any(dfs(r, c, 0) for r in range(ROWS) for c in range(COLS))
# Why overwrite and restore? The same cell can't be used twice in one path,
# but it can be used in a different path starting from a different root.
# Restoring after recursion makes it available for other paths.
```

---

## Variation 9 — DFS on DAG (Topological Sort)

**The mental model:** in a DAG, every node must come after all nodes that point to it. DFS postorder gives this naturally — you finish a node only after all its descendants are done. Reverse postorder = topological order.

**Why reverse?** If A → B → C, DFS visits A first, dives to C (no more children), appends C, backtracks to B, appends B, backtracks to A, appends A. Postorder gives [C, B, A]. Reversed: [A, B, C] = correct topo order (A before B before C).

```python
def topo_sort_dfs(n, edges):
    graph = collections.defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                dfs(nei)
        result.append(node)         # postorder: append AFTER all descendants done

    for i in range(n):
        if i not in visited:
            dfs(i)

    return result[::-1]             # reverse postorder = topological order
```

**Note:** this version doesn't detect cycles. For cycle detection during topo sort, use the 3-state version from Variation 7.

---

## Variation 10 — Iterative DFS (when recursion limit is a concern)

**The mental model:** replace the call stack with an explicit stack data structure. Each `stack.pop()` is equivalent to "return from the current recursive call."

**When to use:** Python's default recursion limit is ~1000. For very deep trees (linked-list shaped) or large grids, iterative DFS avoids `RecursionError`.

```python
def dfs_iterative(root):
    if not root: return []
    stack = [root]
    result = []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)   # right pushed first → left popped first
        if node.left:  stack.append(node.left)
    return result
# Stack is LIFO, so push right before left to process left first (matching recursive preorder)
```

**For graphs:**
```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    while stack:
        node = stack.pop()
        if node in visited: continue    # may be pushed multiple times before popping
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                stack.append(nei)
```

**Why `if node in visited: continue` instead of checking before push?** In iterative DFS, the same node can be pushed by multiple neighbors before it's ever popped. Checking at pop time is simpler and correct; checking at push time also works but requires more care.

---

## Which Variation to Use

| Situation | Variation |
|-----------|-----------|
| Tree height / depth / sum | Return value (V2) |
| Tree global max (diameter, max path) | Return value + `best[0]` container (V2) |
| Find all root-to-leaf paths | Path tracking (V3) |
| Lowest common ancestor | LCA (V4) |
| Connected components / reachability | Graph DFS (V5) |
| Island count / flood fill | Grid DFS (V6) |
| Cycle detection in directed graph | 3-state coloring (V7) |
| Cycle detection in undirected graph | Parent tracking (V7) |
| Subsets / permutations / word search | Backtracking (V8) |
| Topological ordering | Postorder DFS (V9) |
| Very deep tree / recursion limit hit | Iterative (V10) |

---

## The 4 Things That Never Change

1. **Base case first** — always check `if not node` or boundary before recursing. Without it, you'll dereference None.
2. **Mark visited before recursing** — not after, or a cycle will cause infinite recursion before you ever mark anything.
3. **Snapshot mutable state** — `path[:]` not `path` when appending to results. Appending the list itself appends a reference; the list will be empty by the time you read it.
4. **Backtrack after recursing** — undo any mutation (grid cell, path, visited set in backtracking) before returning. The state on return must match the state on entry, or other branches start with corrupted state.
