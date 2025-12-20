# Dynamic Programming Overview 🧠

Break problem into overlapping subproblems and store results (Memoization/Tabulation).

## Concepts
- **Top-Down**: Recursion + Memoization.
- **Bottom-Up**: Iteration + Tabulation.
- **State**: Variables defining a subproblem.

---

## Problems & Solutions

### Easy
1. **[Climbing Stairs](Easy/climbing_stairs.py)**
   - Count ways to reach top.
2. **[Fibonacci](../11.%20Recursion/Easy/fibonacci.py)**
   - DP/Recursion optimization.

### Medium
1. **[Coin Change](Medium/coin_change.py)**
   - Min coins to make amount.
2. **[House Robber](Medium/house_robber.py)**
   - Max loot without alerting police (adjacent houses).
3. **[Longest Increasing Subsequence](Medium/longest_increasing_subsequence.py)**
   - Find length of longest increasing subsequence.

### Hard
1. **[Edit Distance](Hard/edit_distance.py)**
   - Min operations to convert word1 to word2.

---

## Tips for Interviews
- **Space Optimization**: Often can reduce O(n) space to O(1) if you only need last few states (e.g. Fibonacci, House Robber).
