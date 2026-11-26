---
tags: [coding, algorithms, recursion]
topic: Recursion & Backtracking
difficulty: mixed
---
# Recursion & Backtracking — Problem Reference by Pattern

## What this covers

> [!abstract] In this file
> **Covers:** Worked recursion problems by pattern: include/exclude, divide & conquer, pruning, graph recursion, memoized recursion, recursive parsing.
> **You'll be able to:** Write recursive solutions from the contract, not by tracing.
> **Prereqs:** Recursion lecture · **Pair with:** [Recursion lecture](../../03-algorithms/05-recursion.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Foundation — Include/Exclude](#foundation--includeexclude) · [Divide and Conquer (via Recursion)](#divide-and-conquer-via-recursion) · [Pruning & Constraints](#pruning--constraints) · [Foundation — Recursion Fundamentals](#foundation--recursion-fundamentals) · [Recursive Parsing / Evaluation](#recursive-parsing--evaluation) · [Graph — Recursive Traversal](#graph--recursive-traversal) · [Dynamic Programming Foundations (Recursive + Memo)](#dynamic-programming-foundations-recursive--memo)

> [!tip] If you only have 20 minutes
> **Do these first:** [Merge Sort](#merge-sort--t2) · [Pow(x, n) — Fast Exponentiation](#divide-and-conquer-via-recursion) · [Construct Binary Tree from Preorder and Inorder Traversal](#construct-binary-tree-from-preorder-and-inorder-traversal-lc-105--t2) · [Serialize and Deserialize Binary Tree](#serialize-and-deserialize-binary-tree-lc-297--t2) · [Subsets II](#subsets-ii-lc-90--t2) · [Permutations II](#permutations-ii-lc-47--t2) · [Word Search (Grid Backtracking)](#word-search-grid-backtracking--t1) · [Number of Islands](#number-of-islands-lc-200--t1) · [Decode String (Recursive)](#recursive-parsing--evaluation)
> **Template:** Trust the call: define `f(x)` in one sentence, handle the base case, assume `f(smaller)` works, combine.
> **Template:** Fast power: `half = pow(x, n // 2); return half * half * (x if n % 2 else 1)`; negative `n` → `1 / pow(x, -n)`.
> **Gotchas:** Missing/incorrect base case is the #1 bug · Python recursion limit ~1000 — mention `sys.setrecursionlimit` or iterative · recompute overlap ⇒ memoize (→ DP) · pass indices, not slices, to keep O(n) not O(n²).

---

> [!info] First Principles
> Recursion reduces a problem to a smaller identical subproblem; the call stack manages state across levels. Backtracking = DFS over a decision tree — "make choice → recurse → undo choice". The invariant at every recursive call: the partial solution satisfies all constraints imposed so far. Complexity: subsets O(2^n · n), permutations O(n! · n), combinations O(C(n,k) · k).

---

## Foundation — Include/Exclude

**Also try:**

- **Binary Tree Paths** — Tree structure is inherently recursive; each subtree is a smaller instance of the same problem

---

## Divide and Conquer (via Recursion)

---

### Merge Sort `🎯 T2`

> [!example] Problem
> Sort an array in O(n log n) using divide and conquer.

> [!info] Approach
> Sorting n items can be decomposed into sorting two halves independently (no overlap between halves) and merging in O(n). Recursion handles the split; the merge step is the key. Split array at midpoint, sort each half recursively, merge the two sorted halves. Base case = length ≤ 1. Split, conquer left, conquer right, merge in O(n) with two-pointer technique.

> [!note]- Python Solution
> ```python
> def merge_sort(nums):
>     if len(nums) <= 1:
>         return nums
>     mid = len(nums) // 2
>     left = mergeSort(nums[:mid])
>     right = mergeSort(nums[mid:])
>     return merge(left, right)
> 
> def merge(left, right):
>     result = []
>     i = j = 0
>     while i < len(left) and j < len(right):
>         if left[i] <= right[j]:
>             result.append(left[i])
>             i += 1
>         else:
>             result.append(right[j])
>             j += 1
>     result.extend(left[i:])
>     result.extend(right[j:])
>     return result
> ```

> [!success] Complexity
> Time O(n log n) — Master Theorem T(n) = 2T(n/2) + O(n), Case 2. Space O(n) merge buffer + O(log n) stack.

> [!tip] Alternatives
> Bottom-up iterative merge sort avoids O(log n) stack. TimSort (Python's sort) adds galloping for real-world speedups.

---

### Construct Binary Tree from Preorder and Inorder Traversal (LC 105) `🎯 T2`

> Full walkthrough: [Construct Binary Tree from Preorder and Inorder Traversal](../data-structures/08-tree.md#construct-binary-tree-from-preorder-and-inorder-traversal--t2).

---

### Serialize and Deserialize Binary Tree (LC 297) `🎯 T2`

> Full walkthrough: [Serialize and Deserialize Binary Tree](../data-structures/08-tree.md#serialize-and-deserialize-binary-tree--t2).

---

### Maximum Subarray — D&C (O(n log n)) `🎯 T2`

> [!example] Problem
> Same problem as [Maximum Subarray](../data-structures/01-array.md#maximum-subarray--t2) — this section covers the alternative approach only.

> [!info] Approach
> Illustrates D&C: split at mid; max subarray is entirely in left half, entirely in right half, or crosses the midpoint. Crossing case is O(n) per level; depth is O(log n). Recurse on left and right halves; compute max crossing sum by linear scan outward from `mid`. `max_cross` = max suffix of left + max prefix of right. Return `max(max_left, max_right, max_cross)`.

> [!note]- Python Solution
> ```python
> def max_sub_array(nums):
>     def helper(l, r):
>         if l == r:
>             return nums[l]
>         mid = (l + r) // 2
>         left_max = helper(l, mid)
>         right_max = helper(mid + 1, r)
>         # crossing sum
>         left_cross = cur = 0
>         for i in range(mid, l - 1, -1):
>             cur += nums[i]
>             left_cross = max(left_cross, cur)
>         right_cross = cur = 0
>         for i in range(mid + 1, r + 1):
>             cur += nums[i]
>             right_cross = max(right_cross, cur)
>         return max(left_max, right_max, left_cross + right_cross)
>     return helper(0, len(nums) - 1)
> ```

> [!success] Complexity
> Time O(n log n), Space O(log n) call stack.

> [!tip] Alternatives
> Kadane's algorithm is O(n) O(1) and preferred in production. D&C version is only asked to demonstrate the paradigm.

**Also try:**

- **Fibonacci (Memoized Recursion vs DP)** — Naive recursion `f(n) = f(n-1) + f(n-2)` recomputes the same `k` over and over
- **Pow(x, n) — Fast Exponentiation** — Naive O(n) multiplication is too slow for large `n`
- **Count of Inversions (Merge-Sort Based)** — During merge sort, when a right-half element is placed before left-half elements, all remaining left-half elements form inversions with it
- **Fast Doubling Fibonacci** — The recurrence can be reduced by halving `n`, which turns linear recursion into logarithmic recursion depth

---

## Pruning & Constraints

---

### Combination Sum II (No Reuse) `🎯 T2`

> Full walkthrough: [Combination Sum II (0/1 — no reuse)](06-backtracking.md#combination-sum-ii-01--no-reuse--t2).

---

### Word Search (Grid Backtracking) `⚡ T1`

> Full walkthrough: [Word Search (All Occurrences)](06-backtracking.md#word-search-all-occurrences--t1).

---

### Word Search II (Trie + Backtracking) `⚡ T1`

> Full walkthrough: [Word Search II](../data-structures/09-trie.md#word-search-ii--t1).

---

### Permutations II (LC 47) `🎯 T2`

> Full walkthrough: [Permutations II (with duplicates)](06-backtracking.md#permutations-ii-with-duplicates--t2).

---

### Subsets II (LC 90) `🎯 T2`

> Full walkthrough: [Subsets II (with duplicates)](06-backtracking.md#subsets-ii-with-duplicates--t2).

---

### Combinations (LC 77) `🎯 T2`

> Full walkthrough: [Combinations](06-backtracking.md#combinations--t2).

**Also try:**

- **Unique Binary Search Trees II** — Each integer `k` in `[1..n]` can be the root; values `1..k-1` form the left subtree and `k+1..n` form the right subtree
- **Expression Add Operators** — see [Expression Add Operators (LC 282)](06-backtracking.md#string-backtracking)
- **Robot Room Cleaner** — Unknown grid topology — must explore via state-space DFS

---

## Foundation — Recursion Fundamentals

**Also try:**

- **Binary Search (Recursive)** — The array is sorted — at each step the search space halves by comparing the midpoint
- **Tower of Hanoi** — The recurrence is T(n) = 2T(n-1) + 1
- **Print All Subsequences** — Each element has exactly two choices — include or exclude
- **Josephus Problem** — After each elimination the circle shrinks by 1 and the indices shift

---

## Recursive Parsing / Evaluation

**Also try:**

- **Decode String (Recursive)** — Nested brackets are naturally recursive — decoding the inner bracket is a subproblem of the same type
- **Basic Calculator II (LC 227)** — Operator precedence makes this a parsing problem

---

## Graph — Recursive Traversal

---

### Clone Graph (LC 133) `⚡ T1`

> Full walkthrough: [Clone Graph](../data-structures/11-graph.md#clone-graph--t1).

---

### Number of Islands (LC 200) `⚡ T1`

> Full walkthrough: [Number of Islands (BFS)](../data-structures/11-graph.md#number-of-islands-bfs--t1).

**Also try:**

- **Flatten Nested List Iterator** — Nested structure is recursively defined — a list element is either an integer (base case) or another list (recursive case)
- **Nested List Weight Sum** — Each nesting level increments the depth multiplier — a natural recursion where the depth parameter is passed down

---

## Dynamic Programming Foundations (Recursive + Memo)

---

### Climbing Stairs (Memoized Recursion) `🎯 T2`

> [!example] Problem
> Same problem as [Climbing Stairs](08-dynamic-programming.md#climbing-stairs--t2) — this section covers the alternative approach only.

> [!info] Approach
> Memoize `ways(n)` in a dict — same recurrence as Fibonacci. For k step sizes, sum over `ways(n - s)` for each valid step `s`.

> [!note]- Python Solution
> ```python
> def climb_stairs(n):
>     memo = {}
>
>     def ways(n):
>         if n in memo:
>             return memo[n]
>         if n <= 1:
>             return 1
>         memo[n] = ways(n - 1) + ways(n - 2)
>         return memo[n]
>
>     return ways(n)
>
> # Generalised: k distinct step sizes
> def climb_stairs_k(n, steps):
>     memo = {}
>
>     def dp(remaining):
>         if remaining in memo:
>             return memo[remaining]
>         if remaining == 0:
>             return 1
>         if remaining < 0:
>             return 0
>         memo[remaining] = sum(dp(remaining - s) for s in steps)
>         return memo[remaining]
>
>     return dp(n)
> ```

> [!success] Complexity
> Time O(n) with memoization (O(2^n) without). Space O(n) cache + O(n) call depth. Iterative reduces space to O(1).

> [!tip] Alternatives
> Iterative DP with two variables is O(1) space. Matrix exponentiation achieves O(log n) for Fibonacci-variant recurrences.

**Also try:**

- **Predict the Winner (LC 486)** — `dp(i, j)` = score advantage for the current player on subarray `[i, j]`

---

## See Also

[[dynamic-programming]] | [[backtracking]] | [[tree]] | [[stack]]
