# Tree — Google L3 Reference

---

## Node Definition

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

---

## The One Mental Model

At every node, ask: **"What do I need from my left child? From my right child? What do I return upward?"**

If you need a global answer (diameter, max path sum), use a `[best]` container and update it inside DFS while returning a local value upward.

---

## Traversals

```python
def preorder(root):    # node → left → right; use for serialize, copy
    if not root: return
    visit(root); preorder(root.left); preorder(root.right)

def inorder(root):     # left → node → right; BST → sorted order
    if not root: return
    inorder(root.left); visit(root); inorder(root.right)

def postorder(root):   # left → right → node; use when children must be done first
    if not root: return
    postorder(root.left); postorder(root.right); visit(root)
```

**Level order (BFS):**
```python
from collections import deque

def level_order(root):
    if not root: return []
    res, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):       # snapshot size = current level
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        res.append(level)
    return res
```

---

## Core Patterns

### Max Depth
```python
def max_depth(root):
    if not root: return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
```

### Diameter (longest path between any two nodes)
```python
def diameter(root):
    best = [0]
    def dfs(node):
        if not node: return 0
        l, r = dfs(node.left), dfs(node.right)
        best[0] = max(best[0], l + r)   # update global
        return 1 + max(l, r)            # return height upward
    dfs(root)
    return best[0]
```

### Max Path Sum (LC 124)
```python
def max_path_sum(root):
    best = [float('-inf')]
    def dfs(node):
        if not node: return 0
        l = max(dfs(node.left), 0)      # ignore negatives
        r = max(dfs(node.right), 0)
        best[0] = max(best[0], l + r + node.val)
        return node.val + max(l, r)
    dfs(root)
    return best[0]
```

### Lowest Common Ancestor (LC 236)
```python
def lca(root, p, q):
    if not root or root == p or root == q:
        return root
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    return root if left and right else left or right
```
**Rule:** found in both subtrees → current node is LCA. Found in one → bubble it up.

### Balanced Tree (LC 110)
```python
def is_balanced(root):
    def dfs(node):
        if not node: return 0
        l, r = dfs(node.left), dfs(node.right)
        if l == -1 or r == -1 or abs(l - r) > 1: return -1
        return 1 + max(l, r)
    return dfs(root) != -1
```

### Path Sum II — root-to-leaf paths (LC 113)
```python
def path_sum(root, target):
    res = []
    def dfs(node, remaining, path):
        if not node: return
        path.append(node.val)
        if not node.left and not node.right and remaining == node.val:
            res.append(path[:])          # snapshot — never append `path` directly
        dfs(node.left,  remaining - node.val, path)
        dfs(node.right, remaining - node.val, path)
        path.pop()                       # backtrack
    dfs(root, target, [])
    return res
```

### Right Side View (LC 199)
```python
def right_side_view(root):
    res = []
    def dfs(node, depth):
        if not node: return
        if depth == len(res): res.append(node.val)   # first node at this depth
        dfs(node.right, depth + 1)      # right first
        dfs(node.left,  depth + 1)
    dfs(root, 0)
    return res
```

### Good Nodes (LC 1448)
```python
def good_nodes(root):
    def dfs(node, max_so_far):
        if not node: return 0
        good = 1 if node.val >= max_so_far else 0
        max_so_far = max(max_so_far, node.val)
        return good + dfs(node.left, max_so_far) + dfs(node.right, max_so_far)
    return dfs(root, float('-inf'))
```

---

## BST Patterns

**Validate BST (LC 98) — pass bounds, not parent:**
```python
def is_valid_bst(root, lo=float('-inf'), hi=float('inf')):
    if not root: return True
    if not (lo < root.val < hi): return False
    return (is_valid_bst(root.left, lo, root.val) and
            is_valid_bst(root.right, root.val, hi))
```

**Kth Smallest in BST (LC 230) — inorder gives sorted:**
```python
def kth_smallest(root, k):
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node); node = node.left
        node = stack.pop()
        k -= 1
        if k == 0: return node.val
        node = node.right
```

**LCA in BST (LC 235) — use BST property:**
```python
def lca_bst(root, p, q):
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
```

**Insert / Delete in BST:**
```python
def insert_bst(root, val):
    if not root: return TreeNode(val)
    if val < root.val: root.left  = insert_bst(root.left, val)
    else:              root.right = insert_bst(root.right, val)
    return root

def delete_bst(root, key):
    if not root: return None
    if key < root.val:
        root.left = delete_bst(root.left, key)
    elif key > root.val:
        root.right = delete_bst(root.right, key)
    else:
        if not root.left: return root.right
        if not root.right: return root.left
        # find inorder successor (min of right subtree)
        cur = root.right
        while cur.left: cur = cur.left
        root.val = cur.val
        root.right = delete_bst(root.right, root.val)
    return root
```

---

## Tree Construction

**From preorder + inorder (LC 105):**
```python
def build_tree(preorder, inorder):
    if not preorder: return None
    root = TreeNode(preorder[0])
    mid = inorder.index(preorder[0])
    root.left  = build_tree(preorder[1:mid+1], inorder[:mid])
    root.right = build_tree(preorder[mid+1:],  inorder[mid+1:])
    return root
```

**From inorder + postorder (LC 106):**
```python
def build_tree_post(inorder, postorder):
    if not inorder: return None
    root = TreeNode(postorder[-1])
    mid = inorder.index(postorder[-1])
    root.left  = build_tree_post(inorder[:mid],  postorder[:mid])
    root.right = build_tree_post(inorder[mid+1:], postorder[mid:-1])
    return root
```

---

## Serialize / Deserialize (LC 297)

```python
def serialize(root):
    res = []
    def dfs(node):
        if not node: res.append('N'); return
        res.append(str(node.val))
        dfs(node.left); dfs(node.right)
    dfs(root)
    return ','.join(res)

def deserialize(data):
    vals = iter(data.split(','))
    def dfs():
        v = next(vals)
        if v == 'N': return None
        node = TreeNode(int(v))
        node.left = dfs(); node.right = dfs()
        return node
    return dfs()
```

---

## Invert Tree (LC 226)

```python
def invert(root):
    if not root: return None
    root.left, root.right = invert(root.right), invert(root.left)
    return root
```

---

## Symmetric Tree (LC 101)

```python
def is_symmetric(root):
    def mirror(t1, t2):
        if not t1 and not t2: return True
        if not t1 or not t2: return False
        return t1.val == t2.val and mirror(t1.left, t2.right) and mirror(t1.right, t2.left)
    return mirror(root.left, root.right)
```

---

## Iterative DFS (avoid recursion limit)

```python
def preorder_iterative(root):
    if not root: return []
    stack, res = [root], []
    while stack:
        node = stack.pop()
        res.append(node.val)
        if node.right: stack.append(node.right)   # right first
        if node.left:  stack.append(node.left)
    return res
```

---

## Decision Table

| Situation | Approach |
|-----------|----------|
| Height / depth / sum | Postorder return value |
| Global max (diameter, max path sum) | Postorder + `best[0]` container |
| Root-to-leaf paths | DFS + path list + `path[:]` snapshot |
| Level-by-level | BFS with `len(queue)` snapshot |
| Sorted order from BST | Iterative inorder |
| Validate BST | Bounds DFS (`lo`, `hi`) |
| LCA general | Postorder bubble-up |
| LCA BST | Iterative direction comparison |
| Build tree from traversals | Preorder/postorder root + inorder split |

---

## Problems to Know Cold (L3)

| Problem | LC | Key trick |
|---------|----|-----------|
| Max Depth | 104 | `1 + max(left, right)` |
| Diameter | 543 | `best[0] = max(best[0], l+r)` |
| Max Path Sum | 124 | ignore negatives with `max(..., 0)` |
| Level Order | 102 | BFS, snapshot queue size per level |
| Right Side View | 199 | DFS right-first, append when `depth == len(res)` |
| Invert Tree | 226 | swap children recursively |
| Symmetric Tree | 101 | mirror(left, right) |
| Validate BST | 98 | pass `lo`/`hi` bounds, not parent |
| LCA | 236 | found in both → current node is LCA |
| LCA BST | 235 | walk left/right based on value comparison |
| Kth Smallest BST | 230 | iterative inorder, decrement k |
| Construct from preorder+inorder | 105 | root=preorder[0], split by inorder |
| Serialize / Deserialize | 297 | preorder DFS, 'N' for null |
| Path Sum II | 113 | DFS + path + `path[:]` + backtrack |
| Good Nodes | 1448 | pass max-so-far down |

---

## Common Mistakes

- `res.append(path)` instead of `res.append(path[:])` → all entries end up empty
- Validating BST by checking only immediate children → misses grandchild violations
- LCA: not handling `root == p or root == q` base case
- Level order: forgetting to snapshot `len(queue)` before iterating → wrong grouping
- Build tree: not using a hashmap for inorder index lookup → O(n²) per call
