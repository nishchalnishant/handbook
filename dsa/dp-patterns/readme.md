# DP Patterns & Recursion Foundation

Welcome to the definitive guide for mastering **Dynamic Programming** and **Recursion**. This repository is designed to take you from basic recursive thinking to advanced DP optimizations through structured patterns.

> "To understand recursion, one must first understand recursion."

---

## 🧩 Recursion Masterclass

Recursion is the engine behind most Dynamic Programming solutions. Before you can master DP, you must be comfortable with the recursive process of breaking down a large problem into smaller subproblems.

### [Browse Recursion Foundations](/recursion/README.md)

- **[Easy Problems](/recursion/easy/README.md)**: Factorial, Fibonacci, Palindrome Check, Binary Search.
- **[Medium Problems](/recursion/medium/README.md)**: Backtracking, Subsets, Permutations, Combination Sum.
- **[Hard Problems](/recursion/hard/README.md)**: N-Queens, Sudoku Solver, Regex Matching, Word Break.

---

## 📂 DP Patterns

Dynamic Programming is best learned by identifying recurring patterns. We have categorized the most common DP problems into 11 logical patterns:

| Pattern | Description |
| :--- | :--- |
| **[0/1 Knapsack](/0_1_Knapsack_Pattern/README.md)** | Picking items with limited capacity. |
| **[Unbounded Knapsack](/Unbounded_Knapsack_Pattern/README.md)** | Items with unlimited repetition. |
| **[Fibonacci / Simple Recurrence](/Fibonacci_Simple_Recurrence_DP/README.md)** | Problems following linear recurrence. |
| **[Longest Common Subsequence](/Longest_Common_Subsequence/README.md)** | String comparison and matching. |
| **[Longest Increasing Subsequence](/Longest_Increasing_Subsequence/README.md)** | Finding order in sequences. |
| **[Kadane's Algorithm](/Kadanes_Algorithm/README.md)** | Efficient subarray optimizations. |
| **[Matrix Chain Multiplication](/Matrix_Chain_Multiplication/README.md)** | Optimal parenthesization (Interval DP). |
| **[DP on Trees](/DP_on_Trees/README.md)** | Optimization on tree structures. |
| **[DP on Graphs](/DP_on_Graphs/README.md)** | Pathfinding and subgraph optimizations. |
| **[Grid DP](/Grid_DP/README.md)** | Pathfinding and optimization in 2D grids. |
| **[Bitmask DP](/Bitmask_DP/README.md)** | Optimization over small subsets ($N \le 20$). |

---

## 🛠️ The DP Workflow

Every DP solution follows this proven evolution:

1.  **Identify Recursion**: Define the state and base cases.
2.  **Add Memoization**: Store results to avoid redundant work (Top-Down).
3.  **Implement Tabulation**: Build the table iteratively (Bottom-Up).
4.  **Space Optimization**: Reduce the DP table size if possible.

---

## 📊 Visual Learning
Every problem in this documentation includes a **Mermaid Recursion Tree** to help you visualize how the state transitions work.

```mermaid
graph TD
    A["Problem(State)"] --> B["Option 1"]
    A --> C["Option 2"]
    B --> D["Subproblem"]
    C --> E["Subproblem"]
```

---
*Created with ❤️ for the developer community.*