# Unbounded Knapsack Pattern

## Introduction
The Unbounded Knapsack pattern allows for the repetition of items. Given a set of items with weights and values, and a capacity `W`, the goal is to maximize the total value where each item can be chosen any number of times.

## Approach
1.  **State Definition**:
    -   Let `dp[w]` be the maximum value attainable with capacity `w`.

2.  **Recurrence Relation**:
    -   Iterate through all capacity values from `0` to `W`.
    -   For each item `i` with weight `wt[i]` and value `val[i]`:
        -   If `w >= wt[i]`: `dp[w] = max(dp[w], dp[w - wt[i]] + val[i])`

3.  **Base Case**:
    -   `dp[0] = 0`

4.  **Key Difference from 0/1 Knapsack**:
    -   In 0/1 Knapsack 1D array optimization, we iterate backwards to avoid using the same item multiple times for the same capacity level.
    -   In Unbounded Knapsack, we iterate forwards because we *want* to consider the current item again for the same capacity state.


## Similar Problems
-   **Coin Change (Ways)**: Count combinations to make amount with unlimited coins.
-   **Coin Change (Min Coins)**: Find minimum coins needed.
-   **Unbounded Rod Cutting**: Rod cutting where we can cut any number of pieces of same length.
-   **Minimum Cost for Tickets**: Buying 1/7/30 day passes.
-   **Perfect Squares**: Min squares to sum to N.
-   **Combination Sum IV**: Target sum where order matters (Climbing Stairs variant).
-   **Word Break**: Segment string into dictionary words (Unbounded check).
