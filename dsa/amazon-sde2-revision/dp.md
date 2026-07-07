# Dynamic Programming — Amazon SDE-2 Reference

---

## ⚡ Cheat Sheet (Quick Revision)

**The 4 questions to answer before writing any code:**
1. What does `dp[i]` mean in English?
2. How does `dp[i]` depend on smaller states? (write the recurrence)
3. What are the base cases?
4. Where is the answer? (`dp[n]`, `max(dp)`, etc.)

**Always go: recursive → top-down (add memo) → bottom-up (flip direction)**

| Pattern | Signal | Key recurrence |
|---------|--------|---------------|
| 1D Linear | single sequence, choice at each step | `dp[i] = f(dp[i-1], dp[i-2])` |
| 2D Grid | matrix, move right/down | `dp[r][c] = f(dp[r-1][c], dp[r][c-1])` |
| Two Sequences | two strings, alignment/edit | `dp[i][j]` = answer for `s1[:i]`, `s2[:j]` |
| 0/1 Knapsack | take or leave, each item once | iterate capacity **backward** |
| Unbounded Knapsack | take or leave, reuse allowed | iterate capacity **forward** |
| Interval DP | burst/merge/cut subarrays | fill by increasing **length** |
| Tree DP | node answer needs children first | postorder DFS, return pair |
| Stock / State Machine | buy/sell with rules | track states: hold/sold/rest |

**Knapsack direction rule (the most common mistake):**
- Backward `range(target, n-1, -1)` → each item used **at most once**
- Forward `range(n, target+1)` → item reusable **unlimited times**

**Key tricks:**
- `dp[0] = 1` means "1 way to do nothing" (count problems) — derive from definition, don't guess
- LIS O(n log n): `tails` array is NOT the actual LIS, only `len(tails)` is valid
- Interval DP: fill by *length* not by l or r
- 2D string DP: `s1[i-1]` aligns with `dp[i]` (off-by-one is intentional for empty-string base case)
- Max product: track both `max_prod` and `min_prod` — negatives flip them

**Common problems by pattern:**
```
Climbing Stairs / House Robber / Decode Ways / Word Break → 1D Linear
Unique Paths / Min Path Sum / Maximal Square             → 2D Grid
LCS / Edit Distance                                      → Two Sequences
Coin Change / Partition Equal Subset / Target Sum        → Knapsack
LIS                                                      → Subsequence (O(n²) or O(n log n))
Burst Balloons                                           → Interval DP
House Robber III                                         → Tree DP
Buy/Sell Stock I/II/III/cooldown/fee                     → State Machine
```

---

## How to Think About Any DP Problem

Every DP problem is a recursion problem first. The mental journey is always:

```
1. Recursive   — "what if I just tried everything?"          (exponential, TLE)
2. Top-down    — "cache what I've already computed"          (O(n) time, O(n) space, easy to write)
3. Bottom-up   — "fill the table in dependency order"        (O(n) time, often O(1) space, no stack)
```

**In an interview, always start by talking through the recursive solution.** It forces you to identify:
- The subproblem: "what does f(i) mean?"
- The recurrence: "how does f(i) depend on smaller inputs?"
- The base cases: "when do I stop recursing?"

Once you have that, memoization is mechanical, and the table is just a flip of the recursion.

---

## The Framework (apply to every problem)

Before writing code, answer these four questions out loud:

1. **State definition** — what does `dp[i]` represent? (Make it an exact English sentence)
2. **Recurrence** — how does `dp[i]` depend on smaller states? (Write the math first)
3. **Base cases** — what are the trivially-known answers?
4. **Answer location** — is it `dp[n]`, `max(dp)`, or something else?

---

## Pattern 1 — 1D Linear

**Signal:** optimal substructure along a single sequence; decision at each step affects only nearby indices.

---

### Fibonacci / Climbing Stairs (LC 70)

**Problem:** You are climbing a staircase with `n` steps. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
- Example: `n=4` → 5 ways: (1,1,1,1), (1,1,2), (1,2,1), (2,1,1), (2,2)
- Constraint: `1 <= n <= 45`
- What makes it non-trivial: feels like a simple loop problem, but recognizing it as Fibonacci (each step depends on the previous two) is the unlock.

**Step 1 — Recursive (think out loud first)**
```python
# f(n) = f(n-1) + f(n-2)
# "to reach stair n, I came from n-1 or n-2"
# base cases: 1 way to reach stair 0 (do nothing), 1 way to reach stair 1
def climb(n):
    if n <= 1: return 1
    return climb(n-1) + climb(n-2)
# O(2^n) — recomputes the same subproblems over and over
```

**Step 2 — Top-down (cache repeated subproblems)**
```python
# Nothing changes in the logic — just add a cache
def climb(n, memo={}):
    if n <= 1: return 1
    if n in memo: return memo[n]   # already solved, return immediately
    memo[n] = climb(n-1, memo) + climb(n-2, memo)
    return memo[n]
# O(n) time, O(n) space — each subproblem solved exactly once
```

**Step 3 — Bottom-up (fill table from base cases up)**
```python
# Why bottom-up? dp[i] only needs dp[i-1] and dp[i-2].
# We can fill left-to-right since all dependencies are to the left.
def climb(n):
    if n <= 1: return 1
    a, b = 1, 1          # a = dp[i-2], b = dp[i-1]
    for _ in range(2, n+1):
        a, b = b, a + b  # dp[i] = dp[i-1] + dp[i-2]
    return b
# O(n) time, O(1) space — we only need the last two values
```

**Why the O(1) space trick works:** the table entry `dp[i]` only looks back 2 positions, so we never need the full table — just a rolling window.

---

### House Robber (LC 198)

**Problem:** You are a robber planning to rob houses along a street. Each house has some money. You cannot rob two adjacent houses (the alarm will trigger). Given an array `nums` where `nums[i]` is the money in house `i`, return the maximum amount you can rob.
- Example: `nums=[2,7,9,3,1]` → 12 (rob houses 0,2,4: 2+9+1=12)
- Constraint: `1 <= nums.length <= 100`, `0 <= nums[i] <= 400`
- What makes it non-trivial: skipping one house is not enough — you might need to skip two in a row if it's more profitable. The greedy "always take the bigger neighbor" approach fails.

**Step 1 — Recursive**
```python
# f(i) = max money robbing houses 0..i
# At house i: either rob it (+ skip i-1) or skip it
def rob(nums, i):
    if i < 0: return 0
    if i == 0: return nums[0]
    return max(
        rob(nums, i-1),           # skip house i
        rob(nums, i-2) + nums[i]  # rob house i, skip i-1
    )
# Call: rob(nums, len(nums)-1)
# O(2^n) — exponential overlapping subproblems
```

**Step 2 — Top-down**
```python
def rob(nums):
    memo = {}
    def dp(i):
        if i < 0: return 0
        if i == 0: return nums[0]
        if i in memo: return memo[i]
        memo[i] = max(dp(i-1), dp(i-2) + nums[i])
        return memo[i]
    return dp(len(nums)-1)
# O(n) time, O(n) space
```

**Step 3 — Bottom-up**
```python
# dp[i] = max(dp[i-1], dp[i-2] + nums[i])
# Fill left to right. Only need last two values → O(1) space.
def rob(nums):
    prev2, prev1 = 0, 0
    for n in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + n)
    return prev1
```

**Key insight:** at every house, you have exactly two choices — rob or skip. The recurrence naturally captures this binary decision. Once you see "take or skip at each step," it's always this pattern.

---

### Decode Ways (LC 91)

**Problem:** A message containing letters `A-Z` is encoded as `"1"-"26"`. Given a string of digits `s`, return the number of ways to decode it. `'0'` cannot stand alone (no 0th letter), and two-digit codes only go up to `26`.
- Example: `s="226"` → 3 ways: (2,26), (22,6), (2,2,6) → "BZ", "VF", "BBF"
- Example: `s="06"` → 0 ways (leading zero is always invalid)
- Constraint: `1 <= s.length <= 100`, digits only
- What makes it non-trivial: zeros can invalidate a position entirely. The branching (take 1 digit vs 2 digits) creates overlapping subproblems. Edge cases with `'0'` are easy to mis-handle.

**Step 1 — Recursive**
```python
# f(i) = number of ways to decode s[i:]
# At position i: take 1 digit (if valid) + take 2 digits (if valid)
def decode(s, i):
    if i == len(s): return 1       # decoded everything: 1 valid way
    if s[i] == '0': return 0       # leading zero: invalid
    ways = decode(s, i+1)          # always try 1-digit
    if i+1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
        ways += decode(s, i+2)     # try 2-digit if it's 10-26
    return ways
# O(2^n) — exponential
```

**Step 2 — Top-down**
```python
def numDecodings(s):
    memo = {}
    def dp(i):
        if i == len(s): return 1
        if s[i] == '0': return 0
        if i in memo: return memo[i]
        ways = dp(i+1)
        if i+1 < len(s) and 10 <= int(s[i:i+2]) <= 26:
            ways += dp(i+2)
        memo[i] = ways
        return ways
    return dp(0)
```

**Step 3 — Bottom-up**
```python
# Build from right to left (matches recursive direction)
# dp[i] = ways to decode s[i:]
# dp[n] = 1 (base case: empty suffix)
def numDecodings(s):
    n = len(s)
    dp = [0] * (n+1)
    dp[n] = 1
    for i in range(n-1, -1, -1):
        if s[i] == '0':
            dp[i] = 0
        else:
            dp[i] = dp[i+1]
            if i+1 < n and 10 <= int(s[i:i+2]) <= 26:
                dp[i] += dp[i+2]
    return dp[0]
```

**Why fill right-to-left?** The recursion is `f(i)` depends on `f(i+1)` and `f(i+2)` — rightward dependencies. So we fill from the right so those answers exist when we need them.

---

### Maximum Product Subarray (LC 152)

**Problem:** Given an integer array `nums`, find a contiguous subarray that has the largest product and return that product.
- Example: `nums=[2,3,-2,4]` → 6 (subarray [2,3])
- Example: `nums=[-2,0,-1]` → 0 (the zero resets the product)
- Constraint: `1 <= nums.length <= 2*10^4`, `-10 <= nums[i] <= 10`
- What makes it non-trivial: a negative times a negative = positive, so the minimum-so-far can flip to become the maximum when multiplied by a negative number. Standard max-subarray (Kadane's) doesn't handle this — you must track both min and max products simultaneously.

**Why DP?** Because negatives can flip a tiny min into a huge max. You must track both.

**Step 1 — Recursive**
```python
# This one doesn't have a clean recursive decomposition like the others.
# The key insight comes from observing: at each index i, the answer either
# - starts fresh at nums[i], OR
# - extends the subarray ending at i-1.
# But extending means the subarray ending at i-1 could have a max AND a min
# (the min matters because nums[i] could be negative).
# So this is a "carry state forward" DP, not a search tree recursion.
```

**Step 2 — Top-down (state: index + whether we're tracking max or min)**
```python
# Instead of full memoization, recognize that at each step you need:
# max_ending_here, min_ending_here
# This is O(n) by nature, so top-down adds no benefit here.
# Skip directly to bottom-up.
```

**Step 3 — Bottom-up**
```python
def maxProduct(nums):
    max_prod = min_prod = res = nums[0]
    for n in nums[1:]:
        # nums[i] could be negative — flip max and min
        candidates = (n, max_prod * n, min_prod * n)
        max_prod = max(candidates)
        min_prod = min(candidates)
        res = max(res, max_prod)
    return res
```

**The key insight to say in an interview:** "A negative times a negative becomes positive, so the minimum product could become the maximum. I need to track both."

---

### Word Break (LC 139)

**Problem:** Given a string `s` and a dictionary of strings `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words. Words in the dictionary can be reused.
- Example: `s="leetcode"`, `wordDict=["leet","code"]` → true ("leet code")
- Example: `s="catsandog"`, `wordDict=["cats","dog","sand","and","cat"]` → false (no valid split)
- Constraint: `1 <= s.length <= 300`, dict has 1–1000 words
- What makes it non-trivial: you can't greedily match the longest prefix — a greedy choice may block a valid segmentation. All possible splits must be explored, but many subproblems repeat.

**Step 1 — Recursive**
```python
# f(i) = can s[i:] be fully segmented?
# Try every word as the next segment starting at i
def wb(s, i, word_set):
    if i == len(s): return True    # reached end: success
    for j in range(i+1, len(s)+1):
        if s[i:j] in word_set and wb(s, j, word_set):
            return True
    return False
# O(2^n) — same substring checked many times
```

**Step 2 — Top-down**
```python
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    memo = {}
    def dp(i):
        if i == len(s): return True
        if i in memo: return memo[i]
        for j in range(i+1, len(s)+1):
            if s[i:j] in word_set and dp(j):
                memo[i] = True
                return True
        memo[i] = False
        return False
    return dp(0)
```

**Step 3 — Bottom-up**
```python
# dp[i] = can s[:i] be segmented?
# dp[0] = True (empty string is trivially segmented)
# Fill left to right: for each position i, try all j < i
def wordBreak(s, wordDict):
    word_set = set(wordDict)
    dp = [False] * (len(s)+1)
    dp[0] = True
    for i in range(1, len(s)+1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[-1]
```

---

## Pattern 2 — 2D Grid

**Signal:** 2D matrix, moves restricted to right/down (or similar). State = position `(r, c)`.

---

### Unique Paths (LC 62)

**Problem:** A robot is on an `m x n` grid at the top-left corner. It can only move right or down. Count the number of unique paths to reach the bottom-right corner.
- Example: `m=3, n=7` → 28 paths
- Example: `m=3, n=2` → 3 paths: right-down-down, down-right-down, down-down-right
- Constraint: `1 <= m, n <= 100`
- What makes it non-trivial: brute-force enumeration of all paths is exponential. The key insight is that the number of ways to reach `(r,c)` depends only on the cell above and the cell to the left — classic 2D DP decomposition.

**Step 1 — Recursive**
```python
# f(r, c) = number of ways to reach (r, c) from (0, 0)
# Can only come from above (r-1, c) or from left (r, c-1)
def paths(r, c):
    if r == 0 or c == 0: return 1  # only 1 way along edges
    return paths(r-1, c) + paths(r, c-1)
# O(2^(m+n)) — exponential overlapping calls
```

**Step 2 — Top-down**
```python
def uniquePaths(m, n):
    memo = {}
    def dp(r, c):
        if r == 0 or c == 0: return 1
        if (r, c) in memo: return memo[(r, c)]
        memo[(r, c)] = dp(r-1, c) + dp(r, c-1)
        return memo[(r, c)]
    return dp(m-1, n-1)
```

**Step 3 — Bottom-up**
```python
# Fill row by row, left to right. Each cell depends only on the cell above and left.
def uniquePaths(m, n):
    dp = [[1]*n for _ in range(m)]   # edges all = 1 (base case)
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]
    return dp[m-1][n-1]
```

---

### Minimum Path Sum (LC 64)

**Problem:** Given an `m x n` grid filled with non-negative numbers, find a path from the top-left to the bottom-right (moving only right or down) that minimizes the sum of all numbers along the path.
- Example: `grid=[[1,3,1],[1,5,1],[4,2,1]]` → 7 (path: 1→3→1→1→1)
- Constraint: `1 <= m, n <= 200`, `0 <= grid[i][j] <= 200`
- What makes it non-trivial: unlike Unique Paths (counting), you need to minimize — but the same DP structure applies. The in-place trick (overwriting the grid with cumulative costs) is a common interview space-optimization move.

**Step 1 — Recursive**
```python
# f(r, c) = min cost to reach (r, c)
def min_path(grid, r, c):
    if r == 0 and c == 0: return grid[0][0]
    if r == 0: return grid[0][c] + min_path(grid, 0, c-1)   # top row: only left
    if c == 0: return grid[r][0] + min_path(grid, r-1, 0)   # left col: only up
    return grid[r][c] + min(min_path(grid, r-1, c), min_path(grid, r, c-1))
```

**Step 2 — Top-down**
```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    memo = {}
    def dp(r, c):
        if r == 0 and c == 0: return grid[0][0]
        if (r, c) in memo: return memo[(r, c)]
        if r == 0: res = grid[r][c] + dp(r, c-1)
        elif c == 0: res = grid[r][c] + dp(r-1, c)
        else: res = grid[r][c] + min(dp(r-1, c), dp(r, c-1))
        memo[(r, c)] = res
        return res
    return dp(m-1, n-1)
```

**Step 3 — Bottom-up**
```python
def minPathSum(grid):
    m, n = len(grid), len(grid[0])
    for r in range(m):
        for c in range(n):
            if r == 0 and c == 0: continue
            top  = grid[r-1][c] if r > 0 else float('inf')
            left = grid[r][c-1] if c > 0 else float('inf')
            grid[r][c] += min(top, left)
    return grid[m-1][n-1]
# Modifies grid in-place to save space — state is carried in the grid itself
```

---

### Maximal Square (LC 221)

**Problem:** Given an `m x n` binary matrix filled with `'0'`s and `'1'`s, find the largest square containing only `'1'`s and return its area.
- Example: `matrix=[["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]` → 4 (2×2 square)
- Constraint: `1 <= m, n <= 300`, values are `'0'` or `'1'` (strings, not ints)
- What makes it non-trivial: the recurrence is not obvious. `dp[r][c]` = side length of the largest square with bottom-right corner at `(r,c)`, and it equals `min(top, left, diagonal) + 1`. That minimum comes from the "weakest wall" of the square — the tightest constraint in any direction.

**Step 1 — Recursive (and WHY this recurrence)**
```python
# f(r, c) = side length of largest square with bottom-right corner at (r, c)
# KEY INSIGHT: if matrix[r][c] == '1', then the square at (r,c) is limited
# by the smallest square in the three neighbors: top, left, top-left diagonal.
# Think of it as: the square at (r,c) can only be as big as the smallest
# "square room" that fits in each direction.
def max_sq(matrix, r, c):
    if r < 0 or c < 0 or matrix[r][c] == '0': return 0
    top      = max_sq(matrix, r-1, c)
    left     = max_sq(matrix, r, c-1)
    diagonal = max_sq(matrix, r-1, c-1)
    return min(top, left, diagonal) + 1
```

**Step 2 — Top-down**
```python
def maximalSquare(matrix):
    rows, cols = len(matrix), len(matrix[0])
    memo = {}
    best = [0]
    def dp(r, c):
        if r < 0 or c < 0 or matrix[r][c] == '0': return 0
        if (r, c) in memo: return memo[(r, c)]
        side = min(dp(r-1, c), dp(r, c-1), dp(r-1, c-1)) + 1
        memo[(r, c)] = side
        best[0] = max(best[0], side)
        return side
    for r in range(rows):
        for c in range(cols):
            dp(r, c)
    return best[0] ** 2
```

**Step 3 — Bottom-up**
```python
def maximalSquare(matrix):
    rows, cols = len(matrix), len(matrix[0])
    dp = [[0]*(cols+1) for _ in range(rows+1)]   # +1 for boundary
    best = 0
    for r in range(1, rows+1):
        for c in range(1, cols+1):
            if matrix[r-1][c-1] == '1':
                dp[r][c] = min(dp[r-1][c], dp[r][c-1], dp[r-1][c-1]) + 1
                best = max(best, dp[r][c])
    return best * best
```

---

## Pattern 3 — Two Sequences (String DP)

**Signal:** two strings, need alignment / edit operations / common subsequences.
**State:** `dp[i][j]` = answer considering `s1[:i]` and `s2[:j]`.

---

### Longest Common Subsequence (LC 1143)

**Problem:** Given two strings `text1` and `text2`, return the length of their longest common subsequence. A subsequence is a sequence derived by deleting some characters without changing the relative order of remaining characters. A common subsequence appears in both strings.
- Example: `text1="abcde"`, `text2="ace"` → 3 (subsequence "ace")
- Example: `text1="abc"`, `text2="def"` → 0 (no common characters)
- Constraint: `1 <= text1.length, text2.length <= 1000`
- What makes it non-trivial: unlike a common substring (must be contiguous), a subsequence can skip characters. When characters match, you extend the answer. When they don't, you have two choices — drop from text1 or drop from text2 — and must try both.

**Step 1 — Recursive**
```python
# f(i, j) = LCS of s1[:i] and s2[:j]
# Two cases:
#   - last chars match: f(i,j) = f(i-1, j-1) + 1
#   - don't match: try skipping from either string
def lcs(s1, s2, i, j):
    if i == 0 or j == 0: return 0    # one string exhausted
    if s1[i-1] == s2[j-1]:
        return lcs(s1, s2, i-1, j-1) + 1
    return max(lcs(s1, s2, i-1, j), lcs(s1, s2, i, j-1))
# O(2^(m+n)) — many repeated subproblems
```

**Step 2 — Top-down**
```python
def longestCommonSubsequence(s1, s2):
    memo = {}
    def dp(i, j):
        if i == 0 or j == 0: return 0
        if (i, j) in memo: return memo[(i, j)]
        if s1[i-1] == s2[j-1]:
            memo[(i, j)] = dp(i-1, j-1) + 1
        else:
            memo[(i, j)] = max(dp(i-1, j), dp(i, j-1))
        return memo[(i, j)]
    return dp(len(s1), len(s2))
```

**Step 3 — Bottom-up**
```python
def longestCommonSubsequence(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]
# Index trick: s1[i-1] is the i-th character; dp[i] corresponds to first i chars
```

---

### Edit Distance (LC 72)

**Problem:** Given two strings `word1` and `word2`, return the minimum number of operations (insert a character, delete a character, or replace a character) required to convert `word1` into `word2`.
- Example: `word1="horse"`, `word2="ros"` → 3 (horse→rorse→rose→ros)
- Example: `word1="intention"`, `word2="execution"` → 5
- Constraint: `0 <= word1.length, word2.length <= 500`
- What makes it non-trivial: there are three operations with different state transitions. At each mismatch you must try all three and pick the cheapest — brute force tries all 3^n combinations. The DP table `dp[i][j]` represents "min cost to align first i chars of word1 with first j chars of word2" and builds from subproblems for all three operations.

**Step 1 — Recursive**
```python
# f(i, j) = min ops to convert s1[:i] to s2[:j]
# If last chars match: no cost, solve f(i-1, j-1)
# If not: try all 3 operations and take the min
#   - delete from s1:   f(i-1, j)   [remove s1[i-1]]
#   - insert into s1:   f(i, j-1)   [add s2[j-1] to match]
#   - replace in s1:    f(i-1, j-1) [change s1[i-1] to s2[j-1]]
def edit(s1, s2, i, j):
    if i == 0: return j    # insert j chars into empty s1
    if j == 0: return i    # delete all of s1
    if s1[i-1] == s2[j-1]:
        return edit(s1, s2, i-1, j-1)
    return 1 + min(
        edit(s1, s2, i-1, j),    # delete
        edit(s1, s2, i, j-1),    # insert
        edit(s1, s2, i-1, j-1)   # replace
    )
```

**Step 2 — Top-down**
```python
def minDistance(s1, s2):
    memo = {}
    def dp(i, j):
        if i == 0: return j
        if j == 0: return i
        if (i, j) in memo: return memo[(i, j)]
        if s1[i-1] == s2[j-1]:
            memo[(i, j)] = dp(i-1, j-1)
        else:
            memo[(i, j)] = 1 + min(dp(i-1, j), dp(i, j-1), dp(i-1, j-1))
        return memo[(i, j)]
    return dp(len(s1), len(s2))
```

**Step 3 — Bottom-up**
```python
def minDistance(s1, s2):
    m, n = len(s1), len(s2)
    # dp[i][j] = edit distance between s1[:i] and s2[:j]
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1): dp[i][0] = i    # delete all of s1
    for j in range(n+1): dp[0][j] = j    # insert all of s2
    for i in range(1, m+1):
        for j in range(1, n+1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    return dp[m][n]
```

**How to remember the 3 operations:**
- `dp[i-1][j]` → one fewer char in s1 (we deleted from s1)
- `dp[i][j-1]` → one fewer char in s2 (we inserted into s1 to match s2)
- `dp[i-1][j-1]` → both shrink (we replaced)

---

## Pattern 4 — Knapsack

**Signal:** pick items from a set, constrained by total capacity. "Take or leave" decision at each item.

---

### Coin Change (LC 322) — unbounded knapsack

**Problem:** Given an array of coin denominations `coins` and an integer `amount`, return the fewest number of coins needed to make up that amount. If it is impossible, return `-1`. You have an unlimited supply of each coin.
- Example: `coins=[1,5,11]`, `amount=15` → 3 coins (5+5+5, not 11+1+1+1+1 = 5)
- Example: `coins=[2]`, `amount=3` → -1 (impossible)
- Constraint: `1 <= coins.length <= 12`, `1 <= amount <= 10^4`
- What makes it non-trivial: greedy (always pick the largest coin) fails — e.g., `coins=[1,3,4]`, `amount=6` → greedy gives 4+1+1=3 coins, but 3+3=2 coins is optimal. Must explore all combinations; DP avoids recomputing the same subamounts.

**Step 1 — Recursive**
```python
# f(amount) = min coins to make this amount
# At each call: try every coin; take the one that leaves the best subproblem
def coin_change(coins, amount):
    if amount == 0: return 0
    if amount < 0: return float('inf')
    best = float('inf')
    for c in coins:
        sub = coin_change(coins, amount - c)
        if sub != float('inf'):
            best = min(best, sub + 1)
    return best
# O(amount^len(coins)) — exponential
```

**Step 2 — Top-down**
```python
def coinChange(coins, amount):
    memo = {}
    def dp(amt):
        if amt == 0: return 0
        if amt < 0: return float('inf')
        if amt in memo: return memo[amt]
        memo[amt] = min(dp(amt - c) + 1 for c in coins)
        return memo[amt]
    res = dp(amount)
    return res if res != float('inf') else -1
```

**Step 3 — Bottom-up**
```python
def coinChange(coins, amount):
    dp = [float('inf')] * (amount+1)
    dp[0] = 0                          # 0 coins needed for amount 0
    for amt in range(1, amount+1):
        for c in coins:
            if amt >= c:
                dp[amt] = min(dp[amt], dp[amt-c] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
# Outer loop: amounts 1..amount (NOT coins first — this allows reuse)
```

**Why unbounded?** We iterate amounts in the outer loop and coins in the inner loop. Each coin can be picked multiple times because we look at `dp[amt - c]` which was already computed with that same coin available.

---

### Partition Equal Subset Sum (LC 416) — 0/1 knapsack

**Problem:** Given a non-empty array `nums` of positive integers, determine if it can be partitioned into two subsets with equal sums. Each element must go to exactly one subset.
- Example: `nums=[1,5,11,5]` → true (subsets {1,5,5} and {11})
- Example: `nums=[1,2,3,5]` → false (no valid partition exists)
- Constraint: `1 <= nums.length <= 200`, `1 <= nums[i] <= 100`
- What makes it non-trivial: this is NP in general (subset sum), but the constraint sizes make O(n × sum) DP feasible. The reduction — "can any subset sum to `total/2`?" — must come before the algorithm. Also, if `total` is odd, return immediately.

**Step 1 — Recursive**
```python
# Reduce to: can we find a subset summing to total/2?
# f(i, remaining) = can we pick from nums[i:] to hit 'remaining'?
def can_partition(nums, i, remaining):
    if remaining == 0: return True
    if i == len(nums) or remaining < 0: return False
    # two choices: take nums[i] or skip it
    return (can_partition(nums, i+1, remaining - nums[i]) or
            can_partition(nums, i+1, remaining))
```

**Step 2 — Top-down**
```python
def canPartition(nums):
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    memo = {}
    def dp(i, rem):
        if rem == 0: return True
        if i == len(nums) or rem < 0: return False
        if (i, rem) in memo: return memo[(i, rem)]
        memo[(i, rem)] = dp(i+1, rem - nums[i]) or dp(i+1, rem)
        return memo[(i, rem)]
    return dp(0, target)
```

**Step 3 — Bottom-up**
```python
def canPartition(nums):
    total = sum(nums)
    if total % 2: return False
    target = total // 2
    # dp[j] = can we achieve sum j using items seen so far
    dp = [False] * (target+1)
    dp[0] = True
    for n in nums:
        # Iterate BACKWARDS to avoid using the same item twice (0/1 constraint)
        for j in range(target, n-1, -1):
            dp[j] = dp[j] or dp[j-n]
    return dp[target]
```

**The one rule for knapsack direction:**
- **Backward** (`range(target, n-1, -1)`) → each item used **at most once** (0/1 knapsack)
- **Forward** (`range(n, target+1)`) → each item used **unlimited times** (unbounded)

**Why?** Backward means when we update `dp[j]`, `dp[j-n]` still reflects the state *before* adding item `n`. Forward means `dp[j-n]` may already include item `n`, so we reuse it.

---

### Target Sum (LC 494)

**Problem:** Given an integer array `nums` and an integer `target`, assign `+` or `-` to each number, then sum them. Count the number of different ways to reach `target`.
- Example: `nums=[1,1,1,1,1]`, `target=3` → 5 ways (3 positives, 2 negatives: C(5,2)=10/2... actually 5 distinct assignments)
- Example: `nums=[1]`, `target=1` → 1 way (+1)
- Constraint: `1 <= nums.length <= 20`, `0 <= nums[i] <= 1000`, `-1000 <= target <= 1000`
- What makes it non-trivial: the top-down state `(i, current_sum)` has a negative sum component, making the memo key a tuple not a simple index. The bottom-up O(n×sum) reduction via the math trick `P = (total + target) / 2` is not obvious and is the "interview bonus" move.

**Step 1 — Recursive**
```python
# f(i, current_sum) = ways to assign signs to nums[i:] to reach target - current_sum
def target_sum(nums, i, current):
    if i == len(nums):
        return 1 if current == 0 else 0
    return (target_sum(nums, i+1, current - nums[i]) +   # assign +
            target_sum(nums, i+1, current + nums[i]))    # assign -
# Call: target_sum(nums, 0, target)
```

**Step 2 — Top-down**
```python
def findTargetSumWays(nums, target):
    memo = {}
    def dp(i, current):
        if i == len(nums):
            return 1 if current == 0 else 0
        if (i, current) in memo: return memo[(i, current)]
        memo[(i, current)] = dp(i+1, current - nums[i]) + dp(i+1, current + nums[i])
        return memo[(i, current)]
    return dp(0, target)
```

**Step 3 — Bottom-up (math reduction to subset sum)**
```python
# Math trick: let P = sum of + nums, N = sum of - nums
# P + N = total, P - N = target  →  P = (total + target) / 2
# So count subsets that sum to P — reduces to coin change II style
def findTargetSumWays(nums, target):
    total = sum(nums)
    if (total + target) % 2 or abs(target) > total: return 0
    s = (total + target) // 2
    dp = [0] * (s+1)
    dp[0] = 1
    for n in nums:
        for j in range(s, n-1, -1):    # backward = 0/1 (each num used once)
            dp[j] += dp[j-n]
    return dp[s]
```

---

### Coin Change II (LC 518) — count ways, unbounded

**Problem:** Given an array of coin denominations `coins` and an integer `amount`, return the number of distinct combinations that sum to `amount`. Each coin can be used any number of times. Order does not matter (so [1,2] and [2,1] count as one combination).
- Example: `coins=[1,2,5]`, `amount=5` → 4 (5; 2+2+1; 2+1+1+1; 1+1+1+1+1)
- Example: `coins=[2]`, `amount=3` → 0
- Constraint: `1 <= coins.length <= 300`, `0 <= amount <= 5000`
- What makes it non-trivial: this is combinations (order doesn't matter), not permutations. To avoid counting [1,2] and [2,1] separately, the coin must be the outer loop and amount the inner loop — the opposite loop order from Coin Change I, and for a subtle reason.

**Step 1 — Recursive**
```python
# f(i, amount) = ways to make 'amount' using coins[i:]
def count_ways(coins, i, amount):
    if amount == 0: return 1
    if i == len(coins) or amount < 0: return 0
    # take coins[i] (stay at i for reuse) or skip it
    return count_ways(coins, i, amount - coins[i]) + count_ways(coins, i+1, amount)
```

**Step 2 — Top-down**
```python
def change(amount, coins):
    memo = {}
    def dp(i, amt):
        if amt == 0: return 1
        if i == len(coins) or amt < 0: return 0
        if (i, amt) in memo: return memo[(i, amt)]
        memo[(i, amt)] = dp(i, amt - coins[i]) + dp(i+1, amt)
        return memo[(i, amt)]
    return dp(0, amount)
```

**Step 3 — Bottom-up**
```python
def change(amount, coins):
    dp = [0] * (amount+1)
    dp[0] = 1
    for c in coins:
        for i in range(c, amount+1):    # forward = unbounded (can reuse coin c)
            dp[i] += dp[i-c]
    return dp[amount]
# NOTE: coins in outer loop here avoids counting same combination twice
# (different order from coin change I which had amounts in outer loop)
```

---

## Pattern 5 — Subsequences

### Longest Increasing Subsequence (LC 300)

**Problem:** Given an integer array `nums`, return the length of the longest strictly increasing subsequence (elements must be strictly increasing, but do not need to be contiguous).
- Example: `nums=[10,9,2,5,3,7,101,18]` → 4 (subsequence [2,3,7,101])
- Example: `nums=[0,1,0,3,2,3]` → 4 (subsequence [0,1,2,3])
- Constraint: `1 <= nums.length <= 2500`, `-10^4 <= nums[i] <= 10^4`
- What makes it non-trivial: two solutions exist — O(n²) DP (anchor at each index, look back at all valid predecessors) and O(n log n) with binary search on a `tails` array. The O(n log n) approach is the interview target. The `tails` array is a patience-sorting structure: it does NOT store the actual LIS, only its length is valid.

**Step 1 — Recursive**
```python
# f(i) = length of LIS ending at index i (nums[i] MUST be the last element)
def lis(nums, i):
    best = 1
    for j in range(i):
        if nums[j] < nums[i]:
            best = max(best, lis(nums, j) + 1)
    return best
# Call: max(lis(nums, i) for i in range(len(nums)))
# O(2^n) — many repeated subproblems
```

**Step 2 — Top-down**
```python
def lengthOfLIS(nums):
    memo = {}
    def dp(i):
        if i in memo: return memo[i]
        memo[i] = 1
        for j in range(i):
            if nums[j] < nums[i]:
                memo[i] = max(memo[i], dp(j) + 1)
        return memo[i]
    return max(dp(i) for i in range(len(nums)))
# O(n²) — each pair (i,j) checked once
```

**Step 3 — Bottom-up O(n²)**
```python
def lengthOfLIS(nums):
    dp = [1] * len(nums)      # every element is an LIS of length 1 by itself
    for i in range(len(nums)):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

**Step 4 — O(n log n) with binary search (bonus, worth knowing)**
```python
from bisect import bisect_left

def lengthOfLIS(nums):
    tails = []    # tails[i] = smallest tail element of all LIS of length i+1
    for n in nums:
        pos = bisect_left(tails, n)
        if pos == len(tails):
            tails.append(n)    # extend LIS by 1
        else:
            tails[pos] = n     # replace to keep tails minimal
    return len(tails)
# IMPORTANT: tails is NOT the actual LIS — only its length is valid
```

**Why `tails` works:** we keep the minimum possible last element for each LIS length. Smaller tail = more room to extend later. When a new number comes in, binary search tells us the longest LIS it can extend.

---

## Pattern 6 — Interval DP

**State:** `dp[l][r]` = optimal answer for subarray `nums[l..r]`.
**Signal:** "burst", "merge", "cut" problems on contiguous subarrays.
**Order:** fill by increasing interval *length* — short intervals before long ones.

---

### Burst Balloons (LC 312)

**Problem:** You have `n` balloons indexed from `0` to `n-1`. Each balloon has a number `nums[i]`. If you burst balloon `i`, you get `nums[left] * nums[i] * nums[right]` coins, where `left` and `right` are the indices of the adjacent un-bursted balloons. After bursting, the neighbors close in. Burst all balloons to maximize total coins. Treat out-of-bound balloons as having value 1.
- Example: `nums=[3,1,5,8]` → 167 (burst order: 1→5→3→8 yields 3×1×5 + 3×5×8 + 1×3×8 + 1×8×1 = 15+120+24+8=167)
- Constraint: `1 <= n <= 300`, `0 <= nums[i] <= 100`
- What makes it non-trivial: when you burst a balloon, the neighbors of its neighbors become adjacent — forward simulation makes the state space explode. The inversion: think about which balloon is burst **last** in a range, not first. That balloon's two neighbors are the fixed boundaries, so their values are stable. This turns a messy forward problem into a clean interval DP.

**Why is this hard?** When you burst balloon i, its neighbors change — making a straightforward "try bursting each first" recursive solution tricky.

**The inversion trick:** think about which balloon is burst LAST in range (l, r), not first.
```python
# f(l, r) = max coins from bursting all balloons strictly between l and r
# k = last balloon burst in (l, r): it multiplies nums[l]*nums[k]*nums[r] (the borders are still alive)
def burst(nums, l, r, memo):
    if r - l < 2: return 0    # no balloons between l and r
    if (l, r) in memo: return memo[(l, r)]
    best = 0
    for k in range(l+1, r):  # k is the LAST balloon burst in (l,r)
        coins = nums[l] * nums[k] * nums[r]
        best = max(best, burst(nums, l, k, memo) + coins + burst(nums, k, r, memo))
    memo[(l, r)] = best
    return best

def maxCoins(nums):
    nums = [1] + nums + [1]   # virtual boundary balloons
    memo = {}
    return burst(nums, 0, len(nums)-1, memo)
```

**Bottom-up (fill by interval length)**
```python
def maxCoins(nums):
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0]*n for _ in range(n)]
    for length in range(2, n):         # interval length (l to r, exclusive interior)
        for l in range(n - length):
            r = l + length
            for k in range(l+1, r):    # k = last burst in (l,r)
                dp[l][r] = max(dp[l][r],
                               dp[l][k] + nums[l]*nums[k]*nums[r] + dp[k][r])
    return dp[0][n-1]
```

---

## Pattern 7 — DP on Trees

Run postorder DFS. Return what the parent needs; update a global result inside.

---

### House Robber III (LC 337)

**Problem:** A thief found a binary tree where each node has a value representing money. He cannot rob two directly connected nodes (parent and child). Return the maximum amount he can rob.
- Example: tree `[3,2,3,null,3,null,1]` → 7 (rob nodes 3, 3, 1 — the root and both leaves)
- Example: tree `[3,4,5,1,3,null,1]` → 9 (rob the two middle children: 4+5=9)
- Constraint: tree has up to 10^4 nodes, `-400 <= node.val <= 400`
- What makes it non-trivial: unlike the linear house robber (skip one, take the next), a tree has branching — each node has two children and a parent. The key insight is that each DFS call returns a **pair** `(rob_this, skip_this)` so the parent can make the optimal choice without re-visiting children. This eliminates the need for a memo entirely.

**Step 1 — Recursive (brute force)**
```python
# At each node: rob it (skip children) OR skip it (children can be robbed or not)
def rob(root):
    if not root: return 0
    # rob this node: skip its children, but can use grandchildren
    rob_this = root.val
    if root.left:
        rob_this += rob(root.left.left) + rob(root.left.right)
    if root.right:
        rob_this += rob(root.right.left) + rob(root.right.right)
    skip_this = rob(root.left) + rob(root.right)
    return max(rob_this, skip_this)
# O(2^n) — recomputes subtrees repeatedly
```

**Step 2 — Top-down**
```python
def rob(root):
    memo = {}
    def dp(node):
        if not node: return 0
        if node in memo: return memo[node]
        rob_this = node.val
        if node.left:
            rob_this += dp(node.left.left) + dp(node.left.right)
        if node.right:
            rob_this += dp(node.right.left) + dp(node.right.right)
        skip_this = dp(node.left) + dp(node.right)
        memo[node] = max(rob_this, skip_this)
        return memo[node]
    return dp(root)
```

**Step 3 — Bottom-up (return pair from each node)**
```python
# Instead of memoizing nodes, return (rob_this, skip_this) from each DFS call.
# This avoids the memo entirely — each node computed exactly once bottom-up.
def rob(root):
    def dfs(node):
        if not node: return 0, 0    # (rob_this_node, skip_this_node)
        l_rob, l_skip = dfs(node.left)
        r_rob, r_skip = dfs(node.right)
        rob_this  = node.val + l_skip + r_skip
        skip_this = max(l_rob, l_skip) + max(r_rob, r_skip)
        return rob_this, skip_this
    return max(dfs(root))
# O(n) time, O(h) space (h = tree height, for recursion stack)
```

**Key insight:** returning a pair `(rob, skip)` from each call eliminates the need for memoization because each node is visited once and gives back everything the parent needs.

---

## Stock Problems (1D DP variants)

These are state machine DPs — track what state you're currently in.

**LC 121 (one transaction):**
```python
# State: min price seen so far
# Recurrence: profit = max(profit, price - min_price)
min_p, profit = float('inf'), 0
for p in prices:
    min_p = min(min_p, p)
    profit = max(profit, p - min_p)
return profit
```

**LC 123 (2 transactions) — 4-state machine:**
```python
# States: buy1 → sell1 → buy2 → sell2
# Each transition is either "hold" or "execute"
buy1 = buy2 = float('-inf')
sell1 = sell2 = 0
for p in prices:
    buy1  = max(buy1,  -p)           # best gain after buying first time
    sell1 = max(sell1, buy1 + p)     # best gain after selling first time
    buy2  = max(buy2,  sell1 - p)    # best gain after buying second time
    buy2  = max(buy2,  sell1 - p)
    sell2 = max(sell2, buy2 + p)     # best gain after selling second time
return sell2
```

| Problem | State to track | Key idea |
|---------|---------------|----------|
| LC 121 — one transaction | `min_price` | scan left to right |
| LC 122 — unlimited | running profit | take every positive gap |
| LC 123 — at most 2 | buy1, sell1, buy2, sell2 | 4-state machine |
| LC 309 — cooldown | hold, sold, rest | 3-state machine |
| LC 714 — with fee | hold, cash | `cash = max(cash, hold+price-fee)` |

---

## Decision Table

| Signal in the problem | Pattern to use |
|-----------------------|----------------|
| 1D array, choices at each step affecting neighbors | 1D Linear DP |
| 2D grid, move right/down only | 2D Grid DP |
| Two strings, alignment / edit operations | Two-Sequence DP |
| Pick items with capacity limit, "take or leave" | Knapsack |
| "Burst", "cut", "merge" on contiguous subarray | Interval DP |
| Tree nodes, need children's result before parent's | Tree DP (postorder DFS) |
| Buy/sell with transaction rules | Stock state machine |
| Count subsequences / number of ways | Count DP (`dp[j] += dp[j-n]`) |

---

## How to Approach in an Interview

1. **Say the recurrence out loud.** "f(i) equals..." before writing a single line of code.
2. **Write recursive first** if the interviewer doesn't stop you — it proves you understand the substructure.
3. **Add memo to convert to top-down.** Takes 2 lines and immediately gives O(n).
4. **Flip to bottom-up** when you want to discuss space optimization.
5. **For the order of loops in bottom-up:** your base cases must be filled before you need them. Let the recursion direction guide you.

---

## Problems to Know Cold (L3)

| Problem | LC | Pattern | Interview signal |
|---------|----|---------|-----------------|
| Climbing Stairs | 70 | 1D linear | "how many ways" |
| House Robber | 198 | 1D linear | "non-adjacent" |
| Decode Ways | 91 | 1D linear | "count decodings" |
| Word Break | 139 | 1D linear | "can it be split" |
| Maximum Product Subarray | 152 | 1D (track min too) | "max product" |
| Unique Paths | 62 | 2D grid | grid + right/down |
| Maximal Square | 221 | 2D grid | matrix of 0s and 1s |
| LCS | 1143 | Two sequences | "common subsequence" |
| Edit Distance | 72 | Two sequences | "min operations" |
| Coin Change | 322 | Knapsack unbounded | "min coins" |
| Partition Equal Subset Sum | 416 | Knapsack 0/1 | "split into equal halves" |
| Target Sum | 494 | Knapsack (subset count) | "count ways with +/-" |
| LIS | 300 | Subsequence | "longest increasing" |
| Burst Balloons | 312 | Interval DP | "remove elements, gain scores" |
| House Robber III | 337 | Tree DP | tree + non-adjacent |
| Best Time to Buy/Sell I/II/III | 121/122/123 | State machine | stock prices |

---

## Common Mistakes

- `arr = arr.sort()` → sort returns None; arr is now None. Use `arr.sort()` alone.
- **Wrong knapsack direction:** backward for 0/1, forward for unbounded — mixing gives wrong counts.
- **Off-by-one in base cases:** `dp[0] = 1` (1 way to make sum 0) vs `dp[0] = 0` — derive from the subproblem definition, don't guess.
- **LIS O(n log n):** `tails` array is NOT the actual LIS — only `len(tails)` is correct.
- **Interval DP:** fill by increasing *length*, not by l or r — otherwise you use a result that hasn't been computed yet.
- **2D string DP index mismatch:** `s1[i-1]` aligns with `dp[i]`, not `dp[i-1]` — the +1 offset exists so `dp[0]` is the empty-string base case.
