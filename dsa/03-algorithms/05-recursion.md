# Recursion — Complete Reference

## What this covers

> [!abstract] In this file
> **Covers:** Recursion from first principles: the 4-step recipe, 8 recursion patterns (subsets, permutations, divide & combine, tree/graph DFS, N-Queens, memo bridge), common bugs and complexity.
> **You'll be able to:** Design any recursion by stating base case, choice and contract; draw the call tree to get complexity; know when to switch to iteration or memoization.
> **Prereqs:** None · **Pair with:** [Recursion problems](../04-practice/algorithms/05-recursion.md) · [Recursion & DP masterclass](07-recursion-to-dp.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Core Idea](#core-idea) · [Pattern Taxonomy](#pattern-taxonomy) · [Theory & Mental Models](#theory--mental-models) · [Universal Recursion Recipe (Aditya Verma 4-Step)](#universal-recursion-recipe-aditya-verma-4-step) · [Pattern Map](#pattern-map) · [Pattern 1 — Include / Exclude (Subsets)](#pattern-1--include--exclude-subsets) · [Pattern 2 — Permutations](#pattern-2--permutations) · [Pattern 3 — IP/OP String Building](#pattern-3--ipop-string-building) · [Pattern 4 — Divide & Combine](#pattern-4--divide--combine) · [Pattern 5 — Mathematical Recursion](#pattern-5--mathematical-recursion) · [Patterns 6–8 — Where they live](#patterns-68--where-they-live) · [Common Bugs — The 15](#common-bugs--the-15) · [Complexity Cheatsheet](#complexity-cheatsheet) · [L3 Interview Communication Framework](#l3-interview-communication-framework) · [When NOT to Use Recursion](#when-not-to-use-recursion) · [Signal → Pattern Map](#signal--pattern-map) · [Interview Questions — Logic & Trickiness](#interview-questions--logic--trickiness) · [Flashcards](#flashcards)

---

## Core Idea

```
WHY Recursion exists
└── Problems with self-similar structure: solution = f(smaller version of problem)
    ├── Trees: height(T) = 1 + max(height(L), height(R))
    ├── Strings: reverse(s) = reverse(s[1:]) + s[0]
    ├── Combinatorics: permutations(n) = n × permutations(n-1)
    └── Graphs: DFS = visit + recurse on unvisited neighbors

WHAT it is
└── A function that calls itself on a strictly smaller input
    ├── Base case: smallest input, handled directly — no recursion
    ├── Recursive case: reduce to smaller subproblem, trust the recursion
    └── Return: combine subproblem result with current node's contribution

HOW it works
├── The call stack is your explicit state machine
│   ├── Each frame holds: current node/index, partial result, local variables
│   ├── Returning from a frame = undoing that decision (backtracking for free)
│   └── Stack depth = recursion depth = O(h) space
├── Two canonical information-flow directions on trees
│   ├── Return-up (post-order): children compute → parent aggregates
│   └── Pass-down (pre-order): parent passes context to children
└── Memoization bridge to DP
    ├── Overlapping subproblems? → cache (state → result)
    └── State = function arguments → becomes dp table dimensions

WHEN to use
├── "Generate all X" → backtracking
├── "Find any valid assignment" → backtracking + constraint pruning
├── "Tree/graph property" → structural DFS
├── Problem has optimal substructure → memoize → DP
└── Divide problem into independent subproblems → divide & conquer

WHAT can go wrong
├── Missing base case → infinite recursion / stack overflow
├── Not making progress → infinite loop (must call on strictly smaller input)
├── Forgetting to undo mutation → corrupted sibling branches
├── Python recursion limit ~1000 → sys.setrecursionlimit or convert to iterative
└── Mutable list in @lru_cache → unhashable type error; use tuples
```

---

## Pattern Taxonomy

```
RECURSION
├── BASE CASE
│   ├── Empty input (n==0, node==None, i==len(s))
│   ├── Single element (n==1, leaf node)
│   └── Constraint met (remaining==0, target found)
│
├── RECURSIVE CASE
│   ├── Include / Exclude → subsets, knapsack
│   ├── Choose next → permutations, combinations
│   ├── Split & solve → divide-and-conquer, interval DP
│   ├── Traverse → tree DFS, graph DFS
│   └── Match & advance → regex, wildcard
│
├── RETURN VALUE DESIGN (most important decision)
│   ├── Single value → height, count, bool
│   ├── Tuple → (rob, skip), (is_bst, size, min, max)
│   └── Global + local → diameter, max path sum
│
└── OPTIMIZATIONS
    ├── Memoize overlapping subproblems → top-down DP
    ├── Convert to iterative → avoid stack overflow
    ├── Prune early → backtracking (remaining < 0, constraint violated)
    └── Space optimize after tabulation → rolling array
```

> [!warning] Common mistakes
> - Appending `path` instead of `path[:]` — every result aliases the same list and ends up empty.
> - Graph DFS: marking visited *after* recursing — revisits and infinite loops.
> - Directed cycle detection with a plain `visited` set — needs 3 colors (white/gray/black).
> - Combination dedup with `i > 0` instead of `i > start` — drops valid combos that reuse a value at a deeper level.
> - Permutation dedup with `used[i-1]` instead of `not used[i-1]`.
> - Full list → [Common Bugs — The 15](#common-bugs--the-15).

---

## Theory & Mental Models

### Five Recursion Types

| Type | Structure | Example |
| :--- | :--- | :--- |
| **Linear** | f(n) calls f(n-1) | Factorial, linked-list traversal |
| **Binary `🎯 T2`** | f(n) calls f(left) + f(right) | Tree traversal, merge sort |
| **Multi-branch** | f(n) calls f(n-c1), f(n-c2)... | Coin change, climbing stairs |
| **Exponential (backtracking)** | 2^n branches | Subsets, permutations |
| **Tail** | Result fully computed before recursive call | Accumulator-style fib |

### Iterative Conversion Templates

```python
# Preorder DFS (iterative)
def preorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.right: stack.append(node.right)  # right first (LIFO)
        if node.left:  stack.append(node.left)
    return result

# Inorder DFS (iterative)
def inorder_iterative(root):
    stack, result, curr = [], [], root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# Postorder DFS (iterative — reverse trick)
def postorder_iterative(root):
    if not root: return []
    stack, result = [root], []
    while stack:
        node = stack.pop()
        result.append(node.val)
        if node.left:  stack.append(node.left)   # left first (reversed at end)
        if node.right: stack.append(node.right)
    return result[::-1]
```

### Python Recursion Limit

```python
import sys
sys.setrecursionlimit(10**5)   # stopgap; prefer iterative for prod code
```

### Memoization with `@lru_cache`

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def solve(i, j):            # args must be hashable (int, str, tuple — NOT list)
    ...

solve.cache_clear()         # call between test cases to avoid stale state
```

---

## Universal Recursion Recipe (Aditya Verma 4-Step)

```
Step 1 — DRAW THE CHOICE DIAGRAM
         Identify what choices exist at each level of the recursion tree.
         For include/exclude: 2 branches. For permutations: n branches.

Step 2 — WRITE IP/OP (Input/Output signature)
         IP = what changes per call (shrinks — index, remaining capacity, string suffix)
         OP = what you're building (path, count, running sum)
         Base case = when IP is exhausted or constraint is met.

Step 3 — CODE
         Write the recursive function: handle base case, then make choices.
         Trust the recursion — don't trace the full tree mentally.

Step 4 — CONVERT TO DP (if overlapping subproblems)
         State = function arguments → dp table dimensions
         Memoize → top-down done; then tabulate bottom-up for stack safety.
```

> [!IMPORTANT]
> The **state** in the recursive version directly becomes the **dp table dimensions**. If the recursion is `solve(i, w)`, your table is `dp[i][w]`. Never skip to the table without writing the recursion first.

---

## Pattern Map

| # | Pattern | Signal | Key Code Element |
| :--- | :--- | :--- | :--- |
| 1 | **Include/Exclude** | "all subsets / power set" | 2 branches at each index |
| 2 | **Permutations `🎯 T2`** | "all orderings / arrangements" | `used[]` array or swap-based |
| 3 | **IP/OP String Building** | "generate strings with constraints" | validity guard on each branch |
| 4 | **Divide & Combine** | "split → solve independently → merge" | `solve(left) + solve(right)` |
| 5 | **Mathematical** | "power, Hanoi, Josephus" | mathematical recurrence |
| 6 | **Tree/Graph DFS** → [Tree](../02-data-structures/08-tree.md), [Graphs](../02-data-structures/11-graphs.md) | "tree property / graph traversal" | structural post/pre-order |
| 7 | **N-Queens / Constraint Satisfaction** → [Backtracking](06-backtracking.md) | "place N things with constraints" | clash sets / bitmask |
| 8 | **Memoization Bridge** → [Recursion → DP](07-recursion-to-dp.md) | "recursion TLEs → overlapping subproblems" | `@lru_cache` + same state |

---

## Pattern 1 — Include / Exclude (Subsets)

**Signal:** "find all subsets", "power set", "count subsets with property"

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])         # record at EVERY node (not just leaves)
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result

def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    def backtrack(start: int, current: list[int]) -> None:
        result.append(current[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i-1]:
                continue               # skip duplicate at same level
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    backtrack(0, [])
    return result
```

> [!CAUTION]
> Duplicate dedup guard is `i > start` (NOT `i > 0`). This skips duplicates at the same recursion level but allows the same value to appear across different levels.

---

## Pattern 2 — Permutations

**Signal:** "all orderings", "all arrangements", "order matters"

```python
# Standard: used-array approach
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)
    def backtrack(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    backtrack([])
    return result

# Swap-based: avoids used array (useful for in-place operations)
def permute_swap(nums: list[int]) -> list[list[int]]:
    result = []
    def backtrack(start: int) -> None:
        if start == len(nums):
            result.append(nums[:])
            return
        for i in range(start, len(nums)):
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]   # undo
    backtrack(0)
    return result

# Unique permutations (duplicates in input)
def permute_unique(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    used = [False] * len(nums)
    def backtrack(current: list[int]) -> None:
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i in range(len(nums)):
            if used[i]: continue
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue           # skip same-value sibling (not used[i-1] = sibling, not ancestor)
            used[i] = True
            current.append(nums[i])
            backtrack(current)
            current.pop()
            used[i] = False
    backtrack([])
    return result
```

---

## Pattern 3 — IP/OP String Building

**Signal:** "generate all valid strings", "generate parentheses", "letter case permutation"

```python
def generate_parentheses(n: int) -> list[str]:
    result = []
    def backtrack(open_count: int, close_count: int, current: list[str]) -> None:
        if len(current) == 2 * n:
            result.append(''.join(current))
            return
        if open_count < n:
            current.append('(')
            backtrack(open_count + 1, close_count, current)
            current.pop()
        if close_count < open_count:
            current.append(')')
            backtrack(open_count, close_count + 1, current)
            current.pop()
    backtrack(0, 0, [])
    return result

def letter_case_permutation(s: str) -> list[str]:
    result = []
    def backtrack(i: int, current: list[str]) -> None:
        if i == len(s):
            result.append(''.join(current))
            return
        if s[i].isdigit():
            current.append(s[i])
            backtrack(i + 1, current)
            current.pop()
        else:
            for ch in [s[i].lower(), s[i].upper()]:
                current.append(ch)
                backtrack(i + 1, current)
                current.pop()
    backtrack(0, [])
    return result
```

---

## Pattern 4 — Divide & Combine

**Signal:** "different ways to evaluate", "split and combine results independently"

```python
def different_ways(expression: str) -> list[int]:
    from functools import lru_cache
    @lru_cache(maxsize=None)
    def solve(expr: str) -> list[int]:
        results = []
        for i, ch in enumerate(expr):
            if ch in '+-*':
                for left in solve(expr[:i]):
                    for right in solve(expr[i+1:]):
                        if ch == '+': results.append(left + right)
                        elif ch == '-': results.append(left - right)
                        elif ch == '*': results.append(left * right)
        if not results:
            results.append(int(expr))   # pure number, no operator
        return results
    return solve(expression)

def merge_sort(nums: list[int]) -> list[int]:
    if len(nums) <= 1: return nums
    mid = len(nums) // 2
    left  = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]: merged.append(left[i]); i += 1
        else: merged.append(right[j]); j += 1
    return merged + left[i:] + right[j:]
```

---

## Pattern 5 — Mathematical Recursion

**Signal:** "fast exponentiation", "Tower of Hanoi", "Josephus problem"

```python
def my_pow(x: float, n: int) -> float:
    """Fast exponentiation: O(log N)"""
    if n == 0: return 1
    if n < 0:  return 1 / my_pow(x, -n)
    if n % 2 == 0:
        half = my_pow(x, n // 2)
        return half * half
    return x * my_pow(x, n - 1)

def hanoi(n: int, src: str, dst: str, aux: str) -> None:
    """Tower of Hanoi: 2^n - 1 moves"""
    if n == 0: return
    hanoi(n-1, src, aux, dst)
    print(f"Move disk {n} from {src} to {dst}")
    hanoi(n-1, aux, dst, src)

def josephus(n: int, k: int) -> int:
    """0-indexed position of the survivor. O(N) time."""
    if n == 1: return 0
    return (josephus(n-1, k) + k) % n
```

---

## Patterns 6–8 — Where they live

Recursion on structures is taught with the structure, not here:

| Pattern | Signal | Go to |
| :--- | :--- | :--- |
| **Tree DFS** (height, diameter, path sum, LCA, serialize) | "tree property" | [Tree](../02-data-structures/08-tree.md) |
| **Graph DFS** (islands, cycle detection, topo, bridges) | "connected / reachable / order" | [Graphs](../02-data-structures/11-graphs.md) |
| **Combinations, N-Queens, Sudoku, word search** | "all valid placements / combinations" | [Backtracking](06-backtracking.md) |
| **Memoization bridge** (recursion TLEs) | "overlapping subproblems" | [Recursion → DP](07-recursion-to-dp.md) |
| **String recursion** (parsing, decode string, regex match) | "nested / grammar" | [String algorithms](12-string-algorithms.md), [Stack](../02-data-structures/05-stack.md) |

---

## Common Bugs — The 15

| # | Bug | Fix |
| :--- | :--- | :--- |
| 1 | **Missing snapshot** — `result.append(current)` records reference | `result.append(current[:])` |
| 2 | **Mutable default argument** — `def f(path=[])` persists across calls | Use `None` sentinel; initialize inside |
| 3 | **Unhashable args in `@lru_cache`** — passing a list | Only pass hashable types (int, str, tuple) |
| 4 | **Wrong duplicate guard** — `i > 0` allows wrong dedup | Use `i > start` for subsets/combos |
| 5 | **Wrong permutation dedup** — `used[i-1]` vs `not used[i-1]` | `if i > 0 and nums[i]==nums[i-1] and not used[i-1]: continue` |
| 6 | **Forgetting to restore state** — `path.pop()` missing | Always undo mutations before returning |
| 7 | **Combination sum reuse `🎯 T2`** — `i+1` when reuse intended | `backtrack(i, ...)` (same `i`) for reuse; `i+1` for once-each |
| 8 | **Python recursion depth** — default limit ~1000 | `sys.setrecursionlimit(10**5)` or convert to iterative |
| 9 | **Regex `*` zero-occurrence** — forgetting `dp(i, j+2)` | Skip branch: `dp(i, j+2)` OR consume: `first_match and dp(i+1, j)` |
| 10 | **BST validation** — only checking immediate parent | Pass `(lo, hi)` range; check full ancestry |
| 11 | **Graph DFS visited timing** — marking after recursion | Mark visited BEFORE recursing into neighbors |
| 12 | **Directed cycle detection** — single visited set insufficient | 3-color: 0=white, 1=gray(in-stack), 2=black(done) |
| 13 | **LCA null check order** — `.val` before null check | Check `not root` before accessing `root.val` |
| 14 | **Forgetting to reset `used[]` after pop** | `used[i] = False` after `current.pop()` |
| 15 | **Empty generating functions** — `['']` vs `[]` | Empty digits in letter combinations → `[]` not `['']` |

### Bug Examples

```python
# Bug 1: snapshot
result.append(current[:])      # correct — copy
result.append(current)         # wrong — reference to same list

# Bug 3: unhashable
@lru_cache(maxsize=None)
def solve(i, remaining):       # OK: both ints
    ...
def solve(i, nums):            # WRONG: list is unhashable
    ...
# Fix: pass tuple(nums) or move nums to outer scope

# Bug 4/5: duplicate guard
if i > start and nums[i] == nums[i-1]: continue   # subsets/combos
if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue  # permutations

# Bug 9: regex '*' zero occurrence
if j + 1 < len(p) and p[j+1] == '*':
    return dp(i, j+2) or (first_match and dp(i+1, j))
    #      ^^^^^^^^^^^         skip 0 occurrences
```

---

## Complexity Cheatsheet

| Problem | Time | Space | Note |
| :--- | :--- | :--- | :--- |
| Subsets | O(2^n · n) | O(n) stack | 2 choices per element |
| Permutations | O(n! · n) | O(n) stack | n choices per position |
| Combinations C(n,k) | O(C(n,k) · k) | O(k) stack | |
| Combination Sum | O(2^target) | O(target) | small denominations worst case |
| N-Queens | O(n!) | O(n) | bitmask reduces constant |
| Graph DFS | O(V+E) | O(V) | each edge once |
| Tree DFS | O(n) | O(h) | h = height; skewed = O(n) |
| Regex/Interleaving (memo) | O(m·n) | O(m·n) | |

### Master Theorem (divide-and-conquer)

`T(n) = aT(n/b) + O(n^d)`

| Condition | Result | Example |
| :--- | :--- | :--- |
| `d > log_b(a)` | O(n^d) | Binary search: a=1, b=2, d=0 → O(1) |
| `d == log_b(a)` | O(n^d · log n) | Merge sort: a=2, b=2, d=1 → O(n log n) |
| `d < log_b(a)` | O(n^(log_b a)) | Strassen: a=7, b=2, d=2 → O(n^2.81) |

---

## L3 Interview Communication Framework

1. **State IP/OP** — "My function takes X and produces Y"
2. **Draw the tree** — trace a small example to ground the approach
3. **Identify base case** — "We stop when index == length / remaining == 0 / node is None"
4. **State choices** — "At each step, we branch into: include / exclude / try each neighbor"
5. **State invariant** — "Each recursive call operates on a strictly smaller subproblem"
6. **Call out pruning** — "We prune when remaining < 0 / constraint is already violated"
7. **Mention complexity** — "O(2^n) states × O(n) per state = O(n·2^n)"

---

## When NOT to Use Recursion

| Situation | Better Alternative |
| :--- | :--- |
| Need only optimal value (not all solutions) + overlapping subproblems | DP tabulation |
| Very deep recursion (n > 10^4) | Iterative + explicit stack |
| Simple linear scan | Loop |
| BFS / level-order traversal | Queue-based BFS |
| Union-Find (connectivity queries) | Union-Find data structure |
| No overlapping subproblems + just one path | Greedy |

---

## Signal → Pattern Map

| Signal in Problem | Pattern |
| :--- | :--- |
| "all subsets / power set" | Include/Exclude |
| "all permutations / orderings" | Permutations (used-set) |
| "all combinations of size k" | Combinations (start index) |
| "combination sum / partition" | Combination Sum (start + remaining) |
| "generate valid strings / parentheses" | IP/OP with validity guard |
| "tree height / diameter / LCA" | Tree DFS (return-up) |
| "BST validation / range constraint" | Tree DFS (pass-down) |
| "graph components / flood fill" | Graph DFS + visited set |
| "cycle in directed graph" | 3-color DFS |
| "topological order / course schedule" | Post-order DFS, reverse |
| "regex / wildcard matching" | Memoized string recursion |
| "expression evaluation / operators" | Backtracking + prev tracking |
| "Sudoku / N-Queens" | Constraint satisfaction backtracking |
| "slow recursion / TLE" | Memoize → tabulate |
| "recursion → DP" | State = args → table dimensions |

---

## Interview Questions — Logic & Trickiness

| Question | Variant | Click moment | Core logic | Gotchas |
|---|---|---|---|---|
| ⚡ T1 · Medium — Word Search (LC 79) | Grid backtracking | "does the word exist in the grid" | Mark cell `'#'`, recurse 4 ways, restore | Restore even on failure |
| ⚡ T1 · Hard — Word Search II (LC 212) | Trie + backtracking | Many words, one grid | One DFS walks the trie; prune dead branches | Clear `word` at the node once found to avoid duplicates |
| ⚡ T1 · Easy — Flood Fill (LC 733) | DFS in place | "recolor connected region" | Spread to same-colored neighbors | `original == color` → return early, or it loops forever |
| ⚡ T1 · Medium — Number of Islands (LC 200) | DFS flood | Count connected `'1'` blobs | Sink each island cell to `'#'` | 4-directional only |
| ⚡ T1 · Medium — Max Area of Island (LC 695) | DFS + area count | Largest blob | Return `1 + sum(dfs(neighbors))` | Mark visited BEFORE recursing |
| ⚡ T1 · Medium — Clone Graph (LC 133) | DFS + memo | Deep copy with cycles | Register clone before recursing | Key by original node, not `val` |
| ⚡ T1 · Medium — Course Schedule (LC 207) | 3-color cycle | "can all courses finish" | Back edge = neighbor is gray | `color==2` = already safe, skip |
| ⚡ T1 · Medium — Course Schedule II (LC 210) | Topo sort DFS | "return an order" | Append node after all descendants | Reverse the post-order at the end |
| 🎯 T2 · Medium — Subsets (LC 78) | Include/Exclude | "all subsets" | Record at every node, not only leaves | `2^N` outputs — say it before coding |
| 🎯 T2 · Medium — Subsets II (LC 90) | Include/Exclude + dedup | Duplicates in input | Sort; skip same value at same level | `i > start`, not `i > 0` |
| 🎯 T2 · Medium — Permutations (LC 46) | Used-set | "all orderings" | Pick any unused element each level | Unmark `used[i]` after recursing |
| 🎯 T2 · Medium — Permutations II (LC 47) | Used-set + dedup | Orderings with duplicates | Sort + `if i>0 and nums[i]==nums[i-1] and not used[i-1]: continue` | `not used[i-1]` = sibling skip, not ancestor |
| 🎯 T2 · Medium — Combinations (LC 77) | Start index | "choose k of 1..n" | Loop from `start`; recurse `i+1` | Prune: loop only to `n-(k-len)+1` |
| 🎯 T2 · Medium — Combination Sum (LC 39) | Unlimited reuse | Reuse allowed | Recurse `backtrack(i, ...)` — same index | Sort + `break` once over remaining |
| 🎯 T2 · Medium — Combination Sum II (LC 40) | Each once, dup input | No reuse, duplicates | Recurse `i+1` + sibling-skip guard | `i > start` not `i > 0` |
| 🎯 T2 · Medium — Combination Sum III (LC 216) | K digits 1–9 | Fixed count + target | Base: `len==k` AND `remaining==0` | Range is 1..9 only |
| 🎯 T2 · Medium — Combination Sum IV (LC 377) | Order matters → DP | "count", order distinct | Amount outer loop = counts permutations | It's DP, not backtracking — enumerating TLEs |
| 🎯 T2 · Medium — Letter Combinations (LC 17) | IP/OP | Digit → letters | One level per digit | Empty input → `[]`, not `['']` |
| 🎯 T2 · Medium — Letter Case Permutation (LC 784) | IP/OP | Toggle case | Branch on letters; pass digits through | Only letters branch |
| 🎯 T2 · Medium — Restore IP Addresses (LC 93) | Partition + validate | Exactly 4 parts | Try lengths 1–3 per part | Reject leading zero (`len>1 and s[0]=='0'`) and `>255` |
| 🎯 T2 · Medium — Generate Parentheses (LC 22) | IP/OP + guard | "all valid strings" | `(` if `open < n`; `)` if `close < open` | Both counts needed |
| 🎯 T2 · Medium — Palindrome Partitioning (LC 131) | Partition | "all palindrome splits" | Recurse only when the prefix is a palindrome | Precompute `is_pal[i][j]` |
| 🎯 T2 · Hard — N-Queens (LC 51) | Constraint satisfaction | Place one per row | Column + `r-c` + `r+c` sets | Sets give O(1) clash check |
| 🎯 T2 · Hard — Sudoku Solver (LC 37) | Constraint satisfaction | Fill blanks | 9 branches per cell; return on first valid | Return `True` up the stack to stop |
| 🎯 T2 · Easy — Binary Tree Paths (LC 257) | Tree DFS pass-down | "all root-to-leaf paths" | Pass path down; record at leaf | Leaf = no left AND no right |
| 🎯 T2 · Easy — Path Sum (LC 112) | Tree DFS pass-down | Root-to-leaf target | Subtract `node.val` per level | Leaf check, not null check |
| 🎯 T2 · Medium — Path Sum II (LC 113) | Tree DFS + backtrack | "all paths" | `path.pop()` on return | Snapshot `path[:]` |
| 🎯 T2 · Medium — Path Sum III (LC 437) | Prefix sum on tree | Any downward path | `count[curr - target]` | Decrement prefix count on return |
| 🎯 T2 · Hard — Binary Tree Max Path Sum (LC 124) | Global + local | Path may bend | Clip negatives: `max(gain(child), 0)` | Update global with both arms; return one arm |
| 🎯 T2 · Medium — Validate BST (LC 98) | Pass-down range | BST property | Pass `(lo, hi)` down | Check whole ancestry, not just the parent |
| 🎯 T2 · Medium — LCA of BST (LC 235) | BST divergence | BST + two nodes | Both < root → left; both > → right; else root | Compare values |
| 🎯 T2 · Medium — LCA of Binary Tree (LC 236) | Sentinel propagation | General tree | Both sides non-null → current is LCA | Check `root in (p, q)` first |
| 🎯 T2 · Medium — Kth Smallest in BST (LC 230) | Inorder + count | "k-th smallest" | Inorder is sorted; stop at k | Short-circuit once found |
| 🎯 T2 · Hard — Serialize/Deserialize (LC 297) | Preorder + iterator | Round-trip a tree | Preorder with `'#'` for nulls | Use `iter()` for stateful token reads |
| 🎯 T2 · Medium — House Robber III (LC 337) | Tuple return | Adjacent-parent constraint | Return `(rob_this, skip_this)` | Returning one value loses a choice |
| 🎯 T2 · Medium — Unique BSTs II (LC 95) | Structural D&C | "all structurally unique BSTs" | For each root `k`, combine left × right lists | `[None]` for empty range, not `[]` |
| 🎯 T2 · Medium — All Paths Source→Target (LC 797) | DFS backtrack | DAG, all paths | DFS with path stack | DAG → no visited set needed; snapshot path |
| 🎯 T2 · Medium — Surrounded Regions (LC 130) | Reverse DFS | "capture enclosed" | Mark border-connected `O` safe first | 3 states: X, O, safe |
| 🎯 T2 · Medium — Decode String (LC 394) | Recursive descent | Nested brackets | `[` recurses; `]` returns | Pass and return index `i` |
| 🎯 T2 · Medium — Word Break (LC 139) | Memoized recursion | "can it be segmented" | `dp(i)` = any word matches at `i` and `dp(i+len)` | O(2^N) without memo |
| 🎯 T2 · Medium — Coin Change (LC 322) | Memoized recursion | Min coins | `rem < 0 → inf`; min over coins | Return `-1` when result is `inf` |
| 🎯 T2 · Hard — Regular Expression Matching (LC 10) | Memoized recursion | `.` and `*` | `*` = zero or more of the PRECEDING char | Zero-occurrence branch: `dp(i, j+2)` |
| 🎯 T2 · Hard — Wildcard Matching (LC 44) | Memoized recursion | `?` and `*` | `*` matches any sequence | `dp(i+1,j)` consumes; `dp(i,j+1)` = empty `*` |
| 🎯 T2 · Hard — Expression Add Operators (LC 282) | Backtracking | Insert `+ - *` | Track `prev` operand to undo for `*` | Leading zero → `break`, not `continue` |
| 💤 T3 · Hard — Robot Room Cleaner (LC 489) | State-space search | Unknown grid, robot API | Track `(r, c)` visited; move, rotate, back off | Must physically back out after each branch |

---

## Flashcards

**Your backtracking result list contains N copies of the same final state. What went wrong?** #flashcard
`result.append(current)` stored a **reference** to the path list, which every later mutation and `pop()` continues to edit. Append a snapshot: `result.append(current[:])`. Immutable accumulators (str, tuple, int) do not need this.

**Why is the duplicate guard `i > start` for subsets/combinations but `not used[i-1]` for permutations?** #flashcard
In combinations, `i > start` skips a repeated value only among siblings *at the same depth*, preserving its use deeper in the branch. Permutations revisit all indices, so sameness must be judged by whether the identical prior value is currently placed: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue` — skip only when the twin is unused, meaning this branch was already explored.

**In graph DFS, why must a node be marked visited before recursing rather than after?** #flashcard
Marking after recursion lets a cycle re-enter a node already on the call stack, causing infinite recursion or exponential revisits. Mark on entry — the analogue of marking on *enqueue* in BFS.

**Why is a single visited set insufficient for cycle detection in a directed graph?** #flashcard
It cannot distinguish "already fully processed" from "currently on the recursion stack" — a cross-edge into a finished node is legal, a back-edge into an in-progress node is a cycle. Use 3-coloring: white unvisited, **gray in-stack**, black done. A cycle exists exactly when you reach a gray node.

**Combination Sum: when do you recurse with `i` versus `i + 1`?** #flashcard
`backtrack(i, ...)` — same index — allows the element to be reused unboundedly (LC 39). `backtrack(i + 1, ...)` consumes it once (LC 40). Passing `i + 1` when reuse was intended silently loses valid combinations rather than erroring.

**Python raises `RecursionError` on a deep but correct recursion. What are your two options?** #flashcard
Raise the ceiling with `sys.setrecursionlimit(10**5)`, or convert to an explicit stack / iterative form. Say out loud that CPython's ~1000-frame default is an implementation limit, not an algorithmic one — for `n > 10^4`, prefer the iterative version or bottom-up DP.
