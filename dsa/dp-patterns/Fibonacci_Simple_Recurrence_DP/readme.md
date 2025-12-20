# Fibonacci / Simple Recurrence DP

## Introduction
This pattern covers problems that can be broken down into smaller subproblems that follow a simple linear recurrence relation, similar to the Fibonacci sequence. These are often introductory DP problems.

## Approach
1.  **Identify Recurrence**:
    -   Find how the value at step `n` depends on previous steps (e.g., `n-1`, `n-2`).
    -   Standard Example: `F(n) = F(n-1) + F(n-2)` (Climbing Stairs, Tiling).

2.  **State Definition**:
    -   `dp[i]` usually represents the number of ways or the optimal value to reach step `i`.

3.  **Base Cases**:
    -   Define the values for the smallest inputs (e.g., `dp[0]`, `dp[1]`).

4.  **Implementation**:
    -   **Tabulation**: Fill an array from `0` to `n`.
    -   **Space Optimization**: Often, you only need the last few values, so you can solve these in `O(1)` space using variables instead of an array.

## Similar Problems
-   **Climbing Stairs**: Basic Fibonacci (1 or 2 steps).
-   **Min Cost Climbing Stairs**: Fibonacci with weights.
-   **Tribonacci**: Recurrence `T(n) = T(n-1) + T(n-2) + T(n-3)`.
-   **Decode Ways**: Count interpretations of digits (similar to climbing stairs).
-   **House Robber I/II**: Non-adjacent elements. II is circular.
-   **Paint Fence**: Coloring posts with constraint on adjacent colors.
-   **Tiling Problems**: Dominos on grid (`f(n) = f(n-1) + f(n-2)`).
-   **Catalan Numbers**: Unique BSTs, Balanced Parentheses (Recursion with loop).
-   **N-th Stair (1,2,3 steps)**: Generalization of climbing stairs.
