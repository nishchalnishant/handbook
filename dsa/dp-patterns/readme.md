# Dynamic Programming Patterns

Welcome to the Dynamic Programming (DP) Patterns repository. This project is a comprehensive collection of common DP patterns, their fundamental concepts, and implementations for various similar problems.

## DP Patterns Covered

This repository is organized into specific folders for each DP pattern. Each folder contains a detailed `readme.md` explaining the approach and Python implementations of related problems.

-   [**0/1 Knapsack Pattern**](./0_1_Knapsack_Pattern)
-   [**Unbounded Knapsack Pattern**](./Unbounded_Knapsack_Pattern)
-   [**Fibonacci / Simple Recurrence DP**](./Fibonacci_Simple_Recurrence_DP)
-   [**Longest Common Subsequence (LCS)**](./Longest_Common_Subsequence)
-   [**Longest Increasing Subsequence (LIS)**](./Longest_Increasing_Subsequence)
-   [**Kadane's Algorithm**](./Kadanes_Algorithm)
-   [**Matrix Chain Multiplication (MCM)**](./Matrix_Chain_Multiplication)
-   [**DP on Trees**](./DP_on_Trees)
-   [**DP on Graphs**](./DP_on_Graphs)
-   [**Grid DP (2D DP)**](./Grid_DP)
-   [**Bitmask DP**](./Bitmask_DP)

---

## How to Solve DP Problems

The recommended workflow for solving any DP problem follows these steps:

1.  **Recursive Solution**: Start with a plain recursive approach by breaking the problem into subproblems.
2.  **Memoization (Top-Down)**: Add a caching mechanism (usually a dictionary or an array) to store results of recursive calls, preventing redundant calculations.
3.  **Tabulation (Bottom-Up)**: Convert the memoized solution into an iterative one, filling a table based on base cases and previously computed results.

### When to use DP?

-   **Optimal Substructure**: The optimal solution to the problem can be constructed from the optimal solutions of its subproblems.
-   **Overlapping Subproblems**: The recursive solution visits the same subproblems multiple times.

---

## Recursion Strategy

Effective recursion requires a clear strategy:

1.  **Smallest Possible Input (Base Case)**: Identify the simplest case where the answer is known immediately.
2.  **Choice Diagram**: Visualize the choices available at each step.
3.  **Input Reduction**: Ensure that each successive recursive call reduces the input size, eventually reaching the base case.

### Generic Recursion Structure

```python
def solve(params):
    # 1. Base Condition
    if condition_for_smallest_input:
        return result
    
    # 2. Choice Diagram & Recursive Calls
    # Make decisions and call solve(reduced_params)
    res = some_function(solve(reduced_params_1), solve(reduced_params_2))
    
    return res
```

---

## Transitioning to DP

### From Recursion to Memoization
1.  Identify the variables that change across recursive calls.
2.  Initialize a storage structure (array or hash map) using these variables as keys/indices.
3.  Before calculating, check if `storage[key]` exists.
4.  Store the result in `storage[key]` before returning.

### From Memoization to Tabulation
Tabulation skips the recursion overhead and builds the solution iteratively.

-   **Step 1**: Initialize an array or matrix ($N$ variables changing $\rightarrow$ $N$-dimensional matrix).
-   **Step 2**: Fill in base cases (typically row 0 or column 0).
-   **Step 3**: Use the recurrence relation to fill the rest of the table using loops.

#### Example: 0/1 Knapsack (Tabulation)

```python
def knapsack(wt, val, W, n):
    # Initialize DP table
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Fill table
    for i in range(1, n + 1):
        for j in range(1, W + 1):
            if wt[i-1] <= j:
                # Max of (included, excluded)
                dp[i][j] = max(val[i-1] + dp[i-1][j-wt[i-1]], dp[i-1][j])
            else:
                # Excluded
                dp[i][j] = dp[i-1][j]
                
    return dp[n][W]
```

---

## Project Structure

```text
.
├── 0_1_Knapsack_Pattern/
├── Bitmask_DP/
├── DP_on_Trees/
├── Grid_DP/
└── ... (other patterns)
```

Each pattern folder follows a consistent structure:
- `readme.md`: Theoretical overview and problem list.
- `problem_name.py`: Optimized Python implementation.