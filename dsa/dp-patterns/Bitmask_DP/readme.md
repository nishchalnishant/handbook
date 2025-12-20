# Bitmask DP

## Introduction
Bitmask DP is useful for problems that involve small constraints (usually N <= 20) where the state requires keeping track of a subset of elements. A bitmask (integer) is used to represent the set of included elements (1 for included, 0 for excluded).

## Approach
1.  **State Representation**:
    -   Use an integer `mask` where the `i-th` bit being set means the `i-th` element is "visited" or "taken".
    -   State often looks like `dp[mask][last_element]` or simply `dp[mask]`.

2.  **Transitions**:
    -   Iterate through all possible next elements to add to the current mask.
    -   `new_mask = mask | (1 << next_element_index)`.
    -   Update `dp[new_mask]` based on `dp[mask]`.

3.  **Complexity**:
    -   Time Complexity usually involves `O(2^N * N)` or `O(2^N * N^2)`.
    -   This is exponential but feasible for small `N`.

4.  **Common Problems**:
    -   Traveling Salesperson Problem (TSP).
    -   Assignment Problems.
    -   Partitioning into K subsets.

## ## Similar Problems
-   **Traveling Salesman Problem**: Shortest route visiting all cities (Classic Bitmask).
-   **Minimum Incompatibility**: Partition into equal subsets with constraint (Bitmask + Submask iter).
-   **Assign Workers to Jobs**: Minimize unfairness/cost (Bitmask / Branch & Bound).
-   **Max Student Compatibility**: Bipartite matching max score (Bitmask over one set).
-   **Partition to K Equal Sum Subsets**: Check if possible (Bitmask state = current subset sum).
-   **Sudoku Solver**: Bitmask to fast track row/col/box constraints.
-   **Visit All Nodes**: Shortest path in graph visiting all nodes (BFS + Bitmask State).


