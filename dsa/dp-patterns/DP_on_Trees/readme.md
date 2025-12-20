# DP on Trees

## Introduction
DP on Trees involves solving problems on tree data structures where the solution for a node depends on the solutions of its children. This is usually implemented using Post-Order Traversal (DFS).

## Approach
1.  **Traversal**:
    -   Use Depth First Search (DFS).
    -   Process leaf nodes first (base cases) and move upwards to the root.

2.  **State Definition**:
    -   Usually, the recursive function returns a value regarding the subtree rooted at the current node.
    -   Sometimes multiple values are needed (e.g., "max independent set including root" vs "excluding root").

3.  **Transitions**:
    -   Combine results from all children to compute the result for the current node.
    -   Example (Diameter of Tree): Height of node = `1 + max(height(left), height(right))`. Diameter passing through node = `height(left) + height(right)`. Update global max diameter.

4.  **Types**:
    -   Rooting a tree (Re-rooting technique).
    -   Path problems.
    -   Knapsack on trees.


## Similar Problems
-   **Diameter of a Tree**: Longest path between two nodes (1 + left_depth + right_depth).
-   **Maximum Path Sum**: Max path sum where nodes have values (handles negatives).
-   **Binary Tree Cameras**: Min cameras to cover tree (State-based DP).
-   **Distribute Coins**: Balance coins so each node has 1 (Flow of excess/deficit).
-   **House Robber III**: Rob houses in a tree (no direct links).
-   **Max Independent Set**: Largest set of non-adjacent nodes (Similar to House Robber).
-   **Vertex Cover**: Smallest set of nodes covering all edges.
-   **Sum of Root-to-Leaf Paths**: Count or sum all paths.
