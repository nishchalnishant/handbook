# Grid DP

## Introduction
Grid DP refers to dynamic programming problems on 2D grids (matrices). The goal is often to find the number of paths, minimum/maximum path sum, or optimal arrangement from a start point (usually top-left) to an end point (usually bottom-right).

## Approach
1.  **State Definition**:
    -   `dp[r][c]` = result for the cell at row `r` and column `c`.

2.  **Transitions**:
    -   Determine valid moves (e.g., Right and Down).
    -   `dp[r][c]` will depend on previous cells like `dp[r-1][c]` (Top) and `dp[r][c-1]` (Left).
    -   Example (Min Path Sum): `dp[r][c] = grid[r][c] + min(dp[r-1][c], dp[r][c-1])`.

3.  **Base Case**:
    -   `dp[0][0] = grid[0][0]`.
    -   Handle first row and first column separately (can only come from one direction).

4.  **Optimization**:
    -   Space can often be optimized from `O(N*M)` to `O(M)` (using only the previous row) or even `O(1)` (modifying grid in-place if allowed).


## Similar Problems

-   **Unique Paths I/II**: Count paths from TL to BR (II has obstacles).
-   **Minimum Path Sum**: Minimize cost path.
-   **Dungeon Game**: Min initial health to survive path (Reverse DP).
-   **Gold Mine**: Maximize collection with directional constraints.
-   **Cherry Pickup**: Maximize value on round trip (2 concurrent paths).
-   **Maximal Square**: Largest square of 1s in matrix.
-   **Maximal Rectangle**: Largest rectangle of 1s (Histogram variation).
-   **Min Falling Path Sum**: Min sum path from row 0 to N-1 with variable columns.
-   **Increasing Paths**: Count strictly increasing paths (Memoized DFS).

