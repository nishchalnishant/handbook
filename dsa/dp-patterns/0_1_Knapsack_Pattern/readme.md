# 0/1 Knapsack Pattern

## Introduction
The 0/1 Knapsack pattern is a classic dynamic programming problem where you are given a set of items, each with a weight and a value. The goal is to maximize the total value of items included in a knapsack without exceeding a given weight capacity `W`. "0/1" implies that each item can either be picked (1) or not picked (0); you cannot break items.

## Approach
1.  **State Definition**:
    -   Let `dp[i][w]` represent the maximum value attainable using a subset of the first `i` items with a total weight capacity of `w`.

2.  **Recurrence Relation**:
    -   For each item `i` with weight `wt[i]` and value `val[i]`:
        -   **Exclude Item**: `dp[i-1][w]` (Value without including current item)
        -   **Include Item**: `val[i] + dp[i-1][w-wt[i]]` (Value including current item, if `w >= wt[i]`)
    -   `dp[i][w] = max(dp[i-1][w], val[i] + dp[i-1][w-wt[i]])`

3.  **Base Case**:
    -   `dp[0][w] = 0` (0 items have 0 value)
    -   `dp[i][0] = 0` (0 capacity can hold 0 value)

4.  **Space Optimization**:
    -   Since `dp[i][w]` only depends on the previous row `dp[i-1]`, we can optimize space to `O(W)` by iterating backwards.


## Similar Problems
-   **Subset Sum**: Check if a subset exists with a specific sum.
-   **Partition Equal Subset Sum**: Can array be split into two subsets of equal sum?
-   **Count Subsets with Given Sum**: Variation where we count paths instead of just checking existence.
-   **Minimum Subset Sum Difference**: Partition into two subsets to minimize difference.
-   **Target Sum**: Assign `+` or `-` to elements to satisfy equation.
-   **Rod Cutting (Bounded)**: Maximize profit with limited pieces.
-   **Assign Tasks**: Maximize importance within time limit (Knapsack).
