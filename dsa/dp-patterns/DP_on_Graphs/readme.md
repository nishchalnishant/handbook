# DP on Graphs

## Introduction
General Graph DP problems are more complex than Tree DP because graphs can have cycles. These problems often involve finding shortest paths, counting paths, or finding specific subgraphs (like Hamiltonian paths).

## Approach
1.  **DAGs (Directed Acyclic Graphs)**:
    -   If the graph is a DAG, we can use Topological Sort or Memoized DFS.
    -   `dp[u]` depends on `dp[v]` for all edges `u -> v`.

2.  **General Graphs**:
    -   Often requires **Bitmask DP** to keep track of visited nodes to avoid cycles or satisfy constraints (e.g., Traveling Salesperson Problem).
    -   State: `dp[mask][current_node]`. `mask` represents the set of visited nodes.

3.  **Floyd-Warshall / Bellman-Ford**:
    -   These are classic DP algorithms for shortest paths.
    -   Floyd-Warshall: `dp[k][i][j]` = shortest path from `i` to `j` using only first `k` vertices as intermediates.


## Similar Problems
-   **Longest Path in a DAG**: Finds critical path.
-   **Shortest Path in DAG**: Single source shortest path.
-   **Course Schedule**: Cycle detection / Topological ordering.
-   **Cheapest Flights**: Shortest path with 'K' edges constraint.
-   **TSP**: Bitmask DP over graph nodes.
-   **Hamiltonian Path**: Path visiting every node exactly once.
-   **Word Ladder II**: Shortest transformation sequences (BFS/Graph DP).
-   **Frog Jump**: Cross river with dynamic jump sizes.
