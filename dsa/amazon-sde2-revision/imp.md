## ⚡ Cheat Sheet (Quick Revision)

**What's in this file and when to reach for each:**

| Topic | When you see this signal | The one thing to remember |
|-------|--------------------------|--------------------------|
| **Sorting** | custom order, sort by multiple keys | `sort()` returns None; use `cmp_to_key` when comparison needs two elements |
| **Prefix Sum + HashMap** | "how many subarrays with sum k" | seed `{0: 1}` before iterating; query before update |
| **Monotonic Stack** | next/prev greater/smaller element | left-to-right = prev; right-to-left = next; flip `>` vs `>=` for strict vs non-strict |
| **Heap** | Kth largest/smallest, median stream, top-K | Python is min-heap only — negate for max; `if d > dist[u]: continue` in Dijkstra |
| **DSU** | connected components, cycle in undirected, dynamic connectivity | `parent = list(range(n))` not `[0]*n`; `union()` returning False = already connected |
| **Topo Sort** | prerequisites, task ordering, "is this possible" | Kahn's default: `len(order) != n` → cycle; DFS postorder + reverse also works |
| **Trie** | prefix matching, autocomplete, word search | `trie = {}`; `node['$'] = True` marks end; traverse with `node = node[char]` |
| **Backtracking** | subsets, permutations, combinations, word search | choose → recurse → unchoose; `path[:]` not `path` when saving |

**DSU in 6 lines (write cold):**
```python
parent = list(range(n)); rank = [0] * n
def find(x):
    while parent[x] != x: 
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x
def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False
    if rank[a] < rank[b]: a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]: rank[a] += 1
    return True
```

**Monotonic stack — the 4 variants:**
```
Next smaller RIGHT  → right-to-left, pop if stack[-1] >= current
Next greater RIGHT  → right-to-left, pop if stack[-1] <= current
Prev smaller LEFT   → left-to-right, pop if stack[-1] >= current
Prev greater LEFT   → left-to-right, pop if stack[-1] <= current
```

**Prefix sum — the pattern:**
```python
seen = {0: 1}; prefix = 0
for n in nums:
    prefix += n
    count += seen.get(prefix - k, 0)   # query FIRST
    seen[prefix] = seen.get(prefix, 0) + 1  # then update
```

**Topo sort — Kahn's (cycle-safe default):**
```python
queue = deque(i for i in range(n) if indegree[i] == 0)
while queue:
    node = queue.popleft(); order.append(node)
    for nei in graph[node]:
        indegree[nei] -= 1
        if indegree[nei] == 0: queue.append(nei)
# len(order) != n → cycle exists
```

**Knapsack direction (most common DP mistake):**
- Backward `range(target, n-1, -1)` → 0/1 (each item once)
- Forward `range(n, target+1)` → unbounded (reuse allowed)

---

## Sorting Patterns

### sort() vs sorted()
```python
# sort() — modifies in place, returns None
array_2d = [[3, 'b'], [1, 'a'], [2, 'c']]
array_2d.sort(key=lambda x: x[0])

# sorted() — returns a new list, original unchanged
sorted_array = sorted(array_2d, key=lambda x: x[0])
```

### Sort by key (custom comparator)
```python
# Sort list of lists by second element descending
data = [[1, 3], [2, 1], [3, 2]]
data.sort(key=lambda x: x[1], reverse=True)   # [[1,3],[3,2],[2,1]]

# Sort strings by length, then alphabetically
words = ["banana", "fig", "apple", "kiwi"]
words.sort(key=lambda w: (len(w), w))          # tie-break: len first, then alpha

# Sort objects by multiple fields
intervals.sort(key=lambda x: (x[0], x[1]))    # by start, then end
```

### Zip → sort → unzip (sort one list by another)
```python
names = ["Charlie", "Alice", "Bob"]
scores = [85, 95, 90]

combined = list(zip(scores, names))
combined.sort()                                 # sorts by first item (scores)
sorted_scores, sorted_names = zip(*combined)

sorted_scores = list(sorted_scores)            # [85, 90, 95]
sorted_names  = list(sorted_names)             # ['Charlie', 'Bob', 'Alice']
```

### Custom comparator with functools.cmp_to_key
```python
from functools import cmp_to_key

# Largest number (LC 179): "9" > "34" because "934" > "349"
def compare(a, b):
    if a + b > b + a: return -1   # a should come first
    if a + b < b + a: return 1
    return 0

nums = [3, 30, 34, 5, 9]
strs = list(map(str, nums))
strs.sort(key=cmp_to_key(compare))
result = ''.join(strs)             # "9534330"
```

### Sort with index tracking
```python
# Keep original indices after sorting
nums = [40, 10, 30, 20]
indexed = sorted(enumerate(nums), key=lambda x: x[1])
# [(1,10), (3,20), (2,30), (0,40)]
original_indices = [i for i, v in indexed]   # [1, 3, 2, 0]
```

### Gotchas
- `sort()` returns `None` — never do `arr = arr.sort()`
- `reverse=True` reverses the ENTIRE key, including tie-breaks — use `-x` for selective reversal: `key=lambda x: (-x[0], x[1])`
- `cmp_to_key` is needed when comparison depends on two elements together (e.g., string concatenation)

---

## Prefix Sum + HashMap

**Core idea:** `prefix[i]` = sum of `nums[0..i-1]`. Subarray sum `nums[i..j]` = `prefix[j+1] - prefix[i]`.
Combine with a hashmap to answer "how many subarrays have sum = k" in O(n).

**The one setup rule:** seed the map with `{0: 1}` before iterating — this handles subarrays that start at index 0.

```python
def subarray_sum(nums, k):
    count = 0
    prefix = 0
    seen = {0: 1}           # seed: empty prefix has sum 0
    for n in nums:
        prefix += n
        count += seen.get(prefix - k, 0)   # how many prefixes make target
        seen[prefix] = seen.get(prefix, 0) + 1
    return count
```

**Variants and what changes:**

| Problem | What to store in map | Query |
|---------|---------------------|-------|
| Subarray sum = k (LC 560) | `prefix → count` | `seen[prefix - k]` |
| Subarray sum divisible by k (LC 974) | `prefix % k → count` | `seen[(prefix % k)]`; normalize negative mod: `prefix % k` in Python is always non-negative |
| Longest subarray with sum = k | `prefix → first index seen` | `i - seen[prefix - k]`; only store index if not already in map |
| Binary array: equal 0s and 1s (LC 525) | replace 0→-1, then sum=0 variant | same as sum=k with k=0 |
| Submatrix sum = k (LC 1074) | fix two row bounds, collapse columns to 1D, apply LC 560 | O(n²·m) |

**The 3 gotchas:**

1. **Forget `{0: 1}` seed** → misses subarrays starting at index 0. Always seed.
2. **Update map AFTER querying** → if you update first, a subarray `[i..i]` can use its own prefix as the "previous" prefix and double-count.
3. **Negative numbers** → sliding window breaks; prefix sum + hashmap still works fine.

**When prefix sum alone isn't enough (need the map):**
- "How many" subarrays → map stores counts
- "Longest" subarray → map stores first-seen index
- Static queries on a fixed array → plain prefix array, no map needed

---

---

## Monotonic Increasing Stack



-------------------

summary 

these are the monotonic stack points 
- iterate from right to left 
- chek if the stack is empty
- if yes just push the current element in the stack
- if not check if the top most element is less than the current one, if yes just push the element to it if no pop till we find an element less than current element

modify this to get different variations

Next Smaller to Right: Iterate right-to-left, pop if stack[-1] >= current
Next Greater to Right: Iterate right-to-left, pop if stack[-1] <= current
Next Smaller to Left: Iterate left-to-right, pop if stack[-1] >= current
Next Greater to Left: Iterate left-to-right, pop if stack[-1] <= current

----------------
```python
# 1. Previous smaller number (Next smaller to the LEFT)
stack=[]
result=[-1]*len(arr)
for i, j in enumerate(arr):
    while stack and stack[-1] >= j:
        stack.pop()
    if stack:
        result[i]=stack[-1]
    stack.append(j)

# 2. Previous greater number (Next greater to the LEFT)
stack=[]
result=[-1]*len(arr)
for i, j in enumerate(arr):
    while stack and stack[-1] <= j:
        stack.pop()
    if stack:
        result[i]=stack[-1]
    stack.append(j)

# 3. Next greater number to the RIGHT
stack=[]
result=[-1]*len(arr)
for i in range(len(arr)-1, -1, -1):
    j = arr[i]
    while stack and stack[-1] <= j:
        stack.pop()
    if stack:
        result[i]=stack[-1]
    stack.append(j)

# 4. Next smaller number to the RIGHT
stack=[]
result=[-1]*len(arr)
for i in range(len(arr)-1, -1, -1):
    j = arr[i]
    while stack and stack[-1] >= j:
        stack.pop()
    if stack:
        result[i]=stack[-1]
    stack.append(j)
```

**Mental model:** stack stays increasing bottom→top. When you see something smaller, pop until the invariant holds. Every pop tells you: "the element I'm popping just found its **next smaller element** on the right (current `i`) and its **previous smaller element** on the left (new stack top)."

```python
stack = []          # stores indices
for i, x in enumerate(arr):
    while stack and arr[stack[-1]] >= x:   # pop anything >= x (strict increase)
        stack.pop()
    stack.append(i)
```

**What you get after the loop:** `stack` holds indices of elements with no smaller element to their right, in increasing order of value.

**Next smaller element (classic use):**
```python
def next_smaller(arr):
    n = len(arr)
    res = [-1] * n
    stack = []
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] > x:   # strictly greater → x is next smaller
            res[stack.pop()] = i
        stack.append(i)
    return res
```

**Previous smaller element:**
```python
def prev_smaller(arr):
    n = len(arr)
    res = [-1] * n
    stack = []
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] >= x:
            stack.pop()
        res[i] = stack[-1] if stack else -1   # top is previous smaller
        stack.append(i)
    return res
```

**The one rule to remember:**
- `>` in the while condition → strictly increasing stack → finds next/prev **smaller or equal**
- `>=` in the while condition → non-strictly increasing stack → finds next/prev **strictly smaller**

**Problems that use this directly:**

| Problem | LC | What to track |
|---------|----|---------------|
| Daily Temperatures | 739 | next greater → use decreasing stack (flip condition) |
| Largest Rectangle in Histogram | 84 | prev + next smaller, multiply width × height |
| Trapping Rain Water | 42 | prev + next greater (decreasing stack) |
| Sum of Subarray Minimums | 907 | prev smaller + next smaller, count contribution |
| Car Fleet | 853 | decreasing stack on (position, time) |

---

## Heap

**Min-heap only in Python. Negate for max-heap.**

```python
import heapq

hp = []
heapq.heappush(hp, val)               # push — O(log N)
val = heapq.heappop(hp)               # pop min — O(log N)
top = hp[0]                           # peek min — O(1)
heapq.heapify(lst)                    # build heap in-place — O(N)
val = heapq.heappushpop(hp, x)        # push x then pop min (more efficient than two calls)
val = heapq.heapreplace(hp, x)        # pop min THEN push x (heap must be non-empty)
heapq.nlargest(k, lst)                # k largest elements — O(N log K)
heapq.nsmallest(k, lst)               # k smallest elements — O(N log K)
```

**Max-heap:**
```python
heapq.heappush(hp, -val)
val = -heapq.heappop(hp)
top = -hp[0]
```

**Tuple heap** (sort by priority, break ties with a counter):
```python
import itertools
counter = itertools.count()
heapq.heappush(hp, (priority, next(counter), obj))  # counter breaks ties when obj isn't comparable
```

**Pattern 1 — Kth largest (size-K min-heap):**
```python
def kth_largest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)    # evict smallest — keeps K largest
    return heap[0]                 # root = Kth largest
# Why min-heap? Anything smaller than the Kth largest gets evicted,
# leaving exactly the K largest with the minimum of them at root.
```

**Pattern 2 — Kth smallest (size-K max-heap):**
```python
def kth_smallest(nums, k):
    heap = []
    for n in nums:
        heapq.heappush(heap, -n)
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]
```

**Pattern 3 — Top K frequent:**
```python
def top_k_frequent(nums, k):
    count = {}
    for n in nums: count[n] = count.get(n, 0) + 1
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)    # evict least frequent
    return [num for freq, num in heap]

# One-liner alternative:
return [x for x, _ in collections.Counter(nums).most_common(k)]
```

**Pattern 4 — K closest points to origin:**
```python
def k_closest(points, k):
    heap = []
    for x, y in points:
        dist = x*x + y*y
        heapq.heappush(heap, (-dist, x, y))   # max-heap by distance
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
```

**Pattern 5 — Two heaps (median stream):**
```python
lo, hi = [], []   # lo=max-heap (negate), hi=min-heap

def add_num(num):
    heapq.heappush(lo, -num)
    heapq.heappush(hi, -heapq.heappop(lo))   # ensure max(lo) <= min(hi)
    if len(hi) > len(lo):
        heapq.heappush(lo, -heapq.heappop(hi))

def find_median():
    if len(lo) > len(hi): return float(-lo[0])
    return (-lo[0] + hi[0]) / 2.0
```
Rule: always push to `lo` first → fix `lo<=hi` invariant → rebalance sizes.

**Pattern 6 — Merge K sorted lists:**
```python
heap = []
for i, lst in enumerate(lists):
    if lst: heapq.heappush(heap, (lst[0], i, 0))

result = []
while heap:
    val, i, j = heapq.heappop(heap)
    result.append(val)
    if j + 1 < len(lists[i]):
        heapq.heappush(heap, (lists[i][j+1], i, j+1))
```

**Pattern 7 — Task Scheduler (max-heap + cooldown queue):**
```python
def least_interval(tasks, n):
    count = collections.Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)
    time = 0
    queue = collections.deque()   # (remaining_count, available_at_time)

    while max_heap or queue:
        time += 1
        if max_heap:
            cnt = 1 + heapq.heappop(max_heap)   # decrement (negated, so +1)
            if cnt:
                queue.append((cnt, time + n))
        if queue and queue[0][1] == time:
            heapq.heappush(max_heap, queue.popleft()[0])
    return time
```

**Pattern 8 — Dijkstra:**
```python
dist = [float('inf')] * n; dist[src] = 0
pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist[u]: continue          # stale entry — skip
    for v, w in adj[u]:
        if dist[u] + w < dist[v]:
            dist[v] = dist[u] + w
            heapq.heappush(pq, (dist[v], v))
```

**Gotchas:**
- Max-heap: negate on **both** push and pop
- Two heaps: push order matters — `lo` first always
- Dijkstra: `if d > dist[u]: continue` is mandatory — without it you reprocess settled nodes
- Tuple heap with non-comparable objects: add `itertools.count()` tiebreaker
- `heapreplace` requires heap to be non-empty; `heappushpop` is safe on empty heap

**Complexity:**

| Op | Time |
|----|------|
| push / pop | O(log N) |
| heapify | O(N) |
| peek `hp[0]` | O(1) |
| nlargest / nsmallest | O(N log K) |
| size-K maintenance | O(N log K) total |

**Problems to know cold:**

| Problem | LC | Pattern |
|---------|----|---------|
| Kth Largest Element | 215 | size-K min-heap |
| K Closest Points | 973 | size-K max-heap |
| Top K Frequent | 347 | size-K min-heap by freq |
| Median from Data Stream | 295 | two heaps |
| Merge K Sorted Lists | 23 | heap + index tracking |
| Task Scheduler | 621 | max-heap + cooldown queue |
| Network Delay Time | 743 | Dijkstra |
| Kth Largest in Stream | 703 | size-K min-heap, persistent |
| Reorganize String | 767 | max-heap, greedy place most frequent |
| Design Twitter | 355 | heap merge of K user feeds |


binary 

```python
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        Approach: Uses a divide-and-conquer pairwise merge strategy. In each pass, adjacent pairs of lists are merged using a standard two-pointer merge, halving the number of lists each round. This continues until a single sorted list remains. It avoids using a heap entirely and achieves O(n log k) with O(1) auxiliary space per merge.

        Key Insight: By pairing and merging lists bottom-up (like merge sort), each node is touched O(log k) times across all rounds, giving the same asymptotic complexity as a heap approach but with simpler constant factors and no heap overhead.

        Gotchas:
        - When the number of lists is odd, the last list in a round has no pair and must be passed through unchanged (handled by the `if (i+1) < len(lists)` guard that substitutes None as l2).
        - An empty `lists` input or a list containing only None nodes must return None without crashing.
        - The inner `mergeList` dummy-node pattern is required; directly stitching nodes without a dummy forces messy head-initialization logic.
        - Forgetting to advance `tail = tail.next` inside the while loop creates an infinite loop.

        Tricks:
        - Using a dummy ListNode as the head sentinel in `mergeList` eliminates the special case of an empty result list.
        - Iterating with `range(0, len(lists), 2)` cleanly handles both even and odd list counts in one loop.
        - Replacing `lists` with `mergedLists` in-place each round keeps the loop concise without extra index tracking.
        """
        if not lists or len(lists) == 0:
            return None
        # Pairwise merge lists until only one list remains.
        while len(lists) > 1:
            mergedLists = []
            for i in range(0, len(lists), 2):
                l1 = lists[i]
                # If there's no pair for the last list, use None.
                l2 = lists[i + 1] if (i + 1) < len(lists) else None
                mergedLists.append(self.mergeList(l1, l2))
            lists = mergedLists
        return lists[0]

    def mergeList(self, l1, l2):
        """Solves or supports the merge list interview problem."""
        dummy = ListNode()
        tail = dummy
        # Merge nodes of l1 and l2 in sorted order.
        while l1 and l2:
            if l1.val < l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        # Append remaining nodes from either list.
        if l1:
            tail.next = l1
        if l2:
            tail.next = l2
        return dummy.next
```

---

## Union-Find (DSU) — No Class Required

Write DSU cold with just two arrays. No class, no `__init__`, ~6 lines of logic.

```python
parent = list(range(n))   # parent[i] = i → each node is its own root
rank = [0] * n

def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]  # path halving (compression)
        x = parent[x]
    return x

def union(a, b):
    a, b = find(a), find(b)
    if a == b: return False           # already same component
    if rank[a] < rank[b]: a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]: rank[a] += 1
    return True                       # True = merge happened
```

**Track component count separately:**
```python
components = n
for u, v in edges:
    if union(u, v):
        components -= 1
```

**Check connectivity without union:**
```python
if find(start) == find(end):   # same root = connected
    return t
```

**Two independent DSUs (LC 1579 — Alice & Bob):**
```python
def make_dsu(size):
    return list(range(size)), [0] * size

def find(parent, x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]; x = parent[x]
    return x

def union(parent, rank, a, b):
    a, b = find(parent, a), find(parent, b)
    if a == b: return False
    if rank[a] < rank[b]: a, b = b, a
    parent[b] = a
    if rank[a] == rank[b]: rank[a] += 1
    return True

pa, ra = make_dsu(n + 1)
pb, rb = make_dsu(n + 1)
```

---

### Problem patterns

**LC 323 — Count Connected Components**
```python
components = n
for u, v in edges:
    if union(u, v): components -= 1
return components
```

**LC 684 — Redundant Connection (cycle detection)**
```python
# first edge where both endpoints already share a root = the redundant one
for u, v in edges:
    if not union(u, v): return [u, v]
```

**LC 261 — Valid Tree**
```python
if len(edges) != n - 1: return False
for u, v in edges:
    if not union(u, v): return False   # cycle found
return True
```

**LC 547 — Number of Provinces (adjacency matrix)**
```python
for i in range(n):
    for j in range(i+1, n):
        if isConnected[i][j] == 1:
            if union(i, j): components -= 1
```

**LC 1319 — Make Network Connected**
```python
if len(connections) < n - 1: return -1
components = n
for u, v in connections:
    if union(u, v): components -= 1
return components - 1
```

**LC 305 — Number of Islands II (dynamic grid)**
```python
# map (r,c) → r*n+c for 1D parent array; start with components=0
components += 1
for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
    if in_bounds and grid[nr][nc] == 1:
        if union(r*n+c, nr*n+nc): components -= 1
```

**LC 721 — Accounts Merge**
```python
emailToAcc = {}
for i, account in enumerate(accounts):
    for email in account[1:]:
        if email in emailToAcc: union(i, emailToAcc[email])
        else: emailToAcc[email] = i
# group by find(i) → list of emails, then sort
```

**LC 1202 — Smallest String with Swaps**
```python
for a, b in pairs: union(a, b)
groups = defaultdict(list)
for i in range(n): groups[find(i)].append(i)
for indices in groups.values():
    chars = sorted(s[i] for i in indices)
    for i, idx in enumerate(sorted(indices)): result[idx] = chars[i]
```

**LC 990 — Equations Possible**
```python
# two-pass: union all == first, then check != for contradictions
for eq in equations:
    if eq[1] == '=': union(ord(eq[0])-ord('a'), ord(eq[3])-ord('a'))
for eq in equations:
    if eq[1] == '!':
        if find(ord(eq[0])-ord('a')) == find(ord(eq[3])-ord('a')): return False
```

**LC 947 — Remove Stones**
```python
row_rep, col_rep = {}, {}
for i, (r, c) in enumerate(stones):
    if r in row_rep: union(i, row_rep[r])
    else: row_rep[r] = i
    if c in col_rep: union(i, col_rep[c])
    else: col_rep[c] = i
return n - len({find(i) for i in range(n)})
```

**LC 399 — Evaluate Division (weighted DSU)**
```python
# weight[x] = x / parent[x]; path compression multiplies weights up to root
def find(x):
    if parent[x] != x:
        root, w = find(parent[x])
        parent[x] = root; weight[x] *= w
    return parent[x], weight[x]
# c/d = wc/wd if same root, else -1.0
```

**LC 778 — Swim in Water (Kruskal variant)**
```python
edges = [(max(grid[r][c], grid[r][c+1]), r*n+c, r*n+c+1), ...]
edges.sort()
for t, u, v in edges:
    union(u, v)
    if find(start) == find(end): return t
```

**LC 924 — Minimize Malware Spread**
```python
comp_size = Counter(find(i) for i in range(n))
infected_per_comp = Counter(find(node) for node in initial)
# pick node in sorted(initial) where infected_per_comp[root]==1 and comp_size is max
```

**LC 1579 — Remove Max Edges (two independent DSUs)**
```python
# process type-3 (shared) edges first; track comp_a and comp_b separately
# edge removable if it didn't connect either graph (union returned False for both)
# at end: comp_a == 1 and comp_b == 1 means both fully connected
```

---

### Gotchas
- `parent = list(range(n))` not `[0]*n` — each node starts as its own root
- 1-indexed problems (LC 684, 1579): use `n+1` size, index 0 is unused
- `union()` returns `False` = already connected = redundant edge / cycle detected
- Weighted DSU (LC 399): path compression must multiply weights, not just redirect pointer
- Two-DSU problems: pass `parent` and `rank` arrays explicitly to `find`/`union`

---

## Topological Sort — Why It Exists and Where to Use It

### The core idea

Topo sort answers one question: **given a set of tasks where some tasks must happen before others, in what order do I do them?**

More precisely: given a directed graph where an edge `A → B` means "A must come before B," topo sort gives you a linear ordering of all nodes such that every edge points forward in that ordering.

This only works on a **DAG** (directed acyclic graph). If there's a cycle (A → B → A), no valid ordering exists — A can't come before B if B must also come before A.

### The two algorithms

You already know both, but here's when to reach for each:

**Kahn's (BFS from zero-indegree nodes)** — use when:
- You need to detect whether a valid ordering exists (check `len(order) == n`)
- The order itself matters and you want the "earliest available" node at each step
- Easier to reason about iteratively

**DFS postorder + reverse** — use when:
- You want minimal code (fewer variables)
- Cycle detection is secondary (DFS naturally backtracks)

### What "reverse DFS postorder" actually means

When you run DFS on a DAG:
- You enter a node, recurse through all its descendants, then append the node to a list
- This means a node only gets appended *after everything it points to* is already appended
- The list ends up in reverse dependency order: leaves first, roots last
- Reversing gives you roots first, leaves last = topological order

Concrete trace — `A → B → C`:
```
DFS enters A → goes to B → goes to C → C has no neighbors → append C → back to B → append B → back to A → append A
list = [C, B, A]
reversed = [A, B, C]  ← topological order: A before B before C
```

The reversal isn't a trick — it's a consequence of postorder (children before parents).

### Where it actually shows up in problems

The word "topological sort" rarely appears in a problem statement. Instead you see these signals:

| Signal phrase | What it's really asking |
|---|---|
| "Course prerequisites" | Can you finish all courses? What order? |
| "Task scheduling with dependencies" | Is there a valid build/execution order? |
| "Compile order of files" | Which files depend on which? |
| "Find if a sequence is possible" | Does a valid ordering exist (no cycle)? |
| "Alien dictionary order" | Derive character ordering from word comparisons |
| "Parallel courses" (LC 1136) | How many rounds to finish all (longest path in DAG)? |

**The hidden use:** topo sort isn't just for finding the order — it's often the *preprocessing step* that enables DP on a DAG. Once you have nodes in topo order, you can process them left-to-right and guarantee all dependencies are resolved before you use them.

### Kahn's — the canonical template

```python
from collections import defaultdict, deque

def topo_sort(n, edges):
    graph = defaultdict(list)
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1       # v has one more prerequisite

    # start with all nodes that have no prerequisites
    queue = deque(i for i in range(n) if indegree[i] == 0)
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1           # "remove" this node from the graph
            if indegree[nei] == 0:
                queue.append(nei)        # nei's last prerequisite is done

    return order if len(order) == n else []  # [] = cycle exists
```

**Why `len(order) == n` detects a cycle:** nodes in a cycle never reach `indegree == 0` (they're always waiting on each other), so they never enter the queue. If the output is shorter than `n`, some nodes were stuck.

### DFS postorder — the minimal template

```python
def topo_sort_dfs(n, edges):
    graph = defaultdict(list)
    for u, v in edges: graph[u].append(v)
    visited = set()
    result = []

    def dfs(node):
        visited.add(node)
        for nei in graph[node]:
            if nei not in visited:
                dfs(nei)
        result.append(node)     # append AFTER all descendants

    for i in range(n):
        if i not in visited:
            dfs(i)

    return result[::-1]
```

Note: this version doesn't detect cycles (it uses a 2-state visited, not 3-state). For cycle detection add the 3-state coloring from `dfs.md`.

### Problem patterns

**LC 207 — Course Schedule (can you finish all courses?)**
```python
# Build graph: prereq → course
# Run topo sort; if len(order) == numCourses → True
# Cycle in graph = impossible to finish
```

**LC 210 — Course Schedule II (return the order)**
```python
# Same as 207 but return the order array instead of True/False
return order if len(order) == n else []
```

**LC 269 — Alien Dictionary (derive character order)**
```python
# Compare adjacent words to find ordering constraints between characters
# "abc" before "acd" → b comes before c in alien alphabet → edge b→c
# Run topo sort on characters; cycle = invalid input
```

**LC 1136 / 630 — Course Schedule III / Parallel Courses**
```python
# After topo sort, run DP: dp[node] = max(dp[prereq] for prereq of node) + 1
# Answer = max(dp) = longest path in DAG = minimum number of rounds
```

**LC 2115 — Find All Possible Recipes (multi-source)**
```python
# Ingredients with no prerequisites = sources (indegree 0)
# Recipes depend on ingredients/other recipes = regular topo sort
# Collect all recipes that appear in the output order
```

### The real insight: topo sort = safe processing order

Think of it this way: topo sort gives you an order where you can process each node *knowing all its dependencies are already done*. This is why it's the prerequisite for DP on DAGs — you can fill a DP table left-to-right in topo order without ever needing a value that hasn't been computed yet.

Without topo sort, you'd need recursion + memo to handle "what if a dependency hasn't been computed yet?" With topo sort, that problem disappears.

---

## Trie (Prefix Tree) — Dictionary Shortcut

In interviews, you can often skip writing out `class TrieNode` and `class Trie` entirely. You can implement a fully functional Trie using just nested Python dictionaries!

**Inserting into a Dictionary Trie:**
```python
trie = {}
words = ["apple", "app"]

for word in words:
    node = trie
    for char in word:
        if char not in node:
            node[char] = {}      # Create a new nested dictionary
        node = node[char]        # Move down to the next level
    
    node['$'] = True             # Mark the end of this specific word
```
*(After this runs, `trie` looks like: `{'a': {'p': {'p': {'$': True, 'l': {'e': {'$': True}}}}}}`)*

**Searching in a Dictionary Trie:**
```python
def search(word):
    node = trie
    for char in word:
        if char not in node:
            return False         # Path doesn't exist
        node = node[char]        # Move down
        
    return '$' in node           # Did we end on a valid word boundary?
```

**Why this is awesome:**
1. Saves ~15 lines of Object-Oriented boilerplate code.
2. Naturally handles all character types (unlike array-based tries `children = [None]*26` which break on symbols/caps).
3. Easily extendable (e.g., store the full word at the end marker: `node['$'] = word`).


backtracking 

```python
def backtrack(path, options):
    if base_case_condition(path):
        res.append(path[:])  # CRITICAL: Always append a COPY of the path!
        return

    for choice in options:
        if violates_constraints(choice):
            continue

        path.append(choice)       # 1. Make choice
        backtrack(path, options)  # 2. Explore recursively
        path.pop()                # 3. Undo choice (Backtrack)
```

### Templates with Constraints

The most common constraint in backtracking is controlling **what elements we are allowed to pick next**. This changes drastically depending on if you are building Subsets/Combinations or Permutations.

**1. Subsets & Combinations (Order DOES NOT matter)**
*Constraint:* You can only pick elements that come *after* your current position to avoid duplicates like `[1,2]` and `[2,1]`.
*Solution:* Use a `start_index` constraint.
```python
def subsets(nums):
    res = []
    nums.sort() # Only needed if input has duplicate numbers
    
    def backtrack(start_index, path):
        # Base case: For subsets, we save every valid path we build
        res.append(path[:]) 

        for i in range(start_index, len(nums)):
            # Constraint: Skip duplicate numbers at the same tree level
            if i > start_index and nums[i] == nums[i-1]:
                continue
                
            path.append(nums[i])
            # Constraint: Pass 'i + 1' so we never reuse the same element
            backtrack(i + 1, path)
            path.pop()
            
    backtrack(0, [])
    return res
```

**2. Permutations (Order DOES matter)**
*Constraint:* You can pick *any* element, but you cannot reuse an element that is already in your current path.
*Solution:* Iterate from `0` every time, but use a `visited` array constraint.
```python
def permutations(nums):
    res = []
    visited = [False] * len(nums)
    
    def backtrack(path):
        # Base case: Path is full
        if len(path) == len(nums):
            res.append(path[:])
            return

        for i in range(len(nums)):
            # Constraint: If we already used this exact element, skip it
            if visited[i]:
                continue
                
            visited[i] = True
            path.append(nums[i])
            backtrack(path)
            path.pop()
            visited[i] = False
            
    backtrack([])
    return res
```