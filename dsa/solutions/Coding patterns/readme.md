# Coding Patterns 🧩

A comprehensive collection of common coding interview patterns, strategies, and associated problems.

---

## 🎯 Two Pointers

**Pattern Description**: Use two pointers to iterate through an array or list, often used to find pairs or elements that meet specific criteria. Useful for sorted arrays or reversing.

### Strategies
- **Converging (Sorted Array Target Sum)**: Pointers move towards each other.
    - *Problems*: Container With Most Water, 3Sum, 4Sum, Boats to Save People.
- **Fast & Slow (Cycle Detection)**: "Tortoise and Hare" for cycles.
    - *Problems*: Linked List Cycle, Happy Number, Find the Duplicate Number.
- **Fixed Separation**: Maintain a gap (e.g., finding Nth node from end).
    - *Problems*: Remove Nth Node From End of List.
- **In-place Modification**: Modifying array without extra space.
    - *Problems*: Remove Duplicates, Move Zeroes.
- **Expanding From Center**: For palindromes.
    - *Problems*: Longest Palindromic Substring.

---

## 🪟 Sliding Window

**Pattern Description**: Maintain a "window" of elements to optimize calculations over contiguous subarrays.

### Strategies
- **Fixed Size**: Calculate metrics (sum, max) over fixed subarray length.
- **Variable Size**: Expand/contract based on conditions (e.g., sum < target).
- **Monotonic Queue**: Efficiently track max/min in the window.
- **Character Frequency**: Anagrams, substrings.

*Problems*: Longest Substring Without Repeating Characters, Minimum Window Substring, Sliding Window Maximum.

---

## 🌳 Tree Traversal (BFS/DFS)

**Pattern Description**: Systematically visiting all nodes in a tree.

### Strategies
- **BFS (Level Order)**: Process level by level using a Queue.
- **DFS (Pre/In/Post Order)**: Depth-first using Recursion or Stack.
- **LCA**: Lowest Common Ancestor findings.
- **Serialization**: Converting tree to string and back.

---

## 🕸️ Graph Traversal

**Pattern Description**: Exploring nodes and edges in general graphs.

### Strategies
- **Connected Components**: DFS/BFS to find islands or provinces.
- **Cycle Detection**: DFS recursion stack or Union-Find.
- **Topological Sort**: Kahn’s Algorithm (BFS) for dependencies.
- **Shortest Path**:
    - **BFS**: Unweighted graphs.
    - **Dijkstra**: Weighted graphs (non-negative).
    - **Bellman-Ford**: Negative weights.
- **Union-Find (DSU)**: Efficient connectivity checks.
- **MST**: Kruskal’s or Prim’s algorithm.

---

## 💡 Dynamic Programming (DP)

**Pattern Description**: Breaking problems into overlapping subproblems and optimal substructure.

### Categories
- **1D Array**: Fibonacci, Climbing Stairs, House Robber.
- **Grid / 2D**: Unique Paths, Minimum Path Sum.
- **Knapsack Variants**:
    - **0/1 Knapsack**: Item used once (Partition Equal Subset Sum).
    - **Unbounded**: Item used multiple times (Coin Change).
- **LCS (Longest Common Subsequence)**: String comparison (Edit Distance).
- **LIS (Longest Increasing Subsequence)**: O(n log n) optimizations.
- **Interval DP**: Operations on ranges (Matrix Chain Multiplication).
- **Bitmask DP**: Small constraint set representation.
- **State Machine**: Stock trading with cooldowns.

---

## 🔢 Binary Search

**Pattern Description**: O(log n) search on sorted data or answer spaces.

- **Standard**: Find target in sorted array.
- **Rotated Array**: Find min/target in rotated sorted array.
- **On Answer**: Search within a range of possible answers (e.g., Min Capacity).
- **Median of Arrays**: Hard variant for two sorted arrays.

---

## 🥞 Stack & Monotonic Stack

**Pattern Description**: LIFO for matching, history, or finding "next greater" elements.

- **Valid Parentheses**: Matching brackets.
- **Monotonic Stack**: Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram.
- **Expression Evaluation**: RPN, Basic Calculator.

---

## 🍢 Heaps (Priority Queue)

**Pattern Description**: Efficiently access min/max elements.

- **Top K Elements**: keep K largest/smallest seen so far.
- **Merge K Sorted**: Efficient merging.
- **Median Finder**: Two heaps (min & max) to track median stream.
- **Task Scheduling**: Greedy execution based on cost/frequency.

---

## 🔙 Backtracking

**Pattern Description**: Explore all potential solutions, backing up when a path fails.

- **Subsets / Permutations / Combinations**: Generating all variations.
- **Constraint Satisfaction**: N-Queens, Sudoku.
- **Path Finding**: Word Search in grid.

---

## 💰 Greedy

**Pattern Description**: Making the locally optimal choice at each step.

- **Intervals**: Activity Selection, Non-overlapping Intervals.
- **Jump Game**: Reachability.
- **Stock Trading**: Buying low, selling high (simple variants).

---

## 🧬 Bit Manipulation

**Pattern Description**: Direct bit-level operations for optimization.

- **XOR**: Single Number, Missing Number.
- **Counting Bits**: Brian Kernighan’s algorithm.
- **Power of Two**: `(n & (n-1)) == 0`.

---

## 🔗 Linked List Manipulation

- **In-place Reversal**: Reverse sublist or whole list.
- **Merging**: Merge sorted lists.
- **Cycle Detection**: Fast & Slow pointers.

---

## Detailed Technique Explanations

### Prefix Sum
**Concept**: Precompute cumulative sums to allow O(1) range sum queries (`sum[i..j] = P[j] - P[i-1]`).

### Kadane’s Algorithm
**Concept**: Find max contiguous subarray sum in O(n) by carrying forward positive sums and resetting on negative totals.

### Fast & Slow Pointers (Floyd’s Cycle Finding)
**Concept**: Use two pointers moving at different speeds. If they meet, there is a cycle.

### Monotonic Stack
**Concept**: Maintain a stack of indices/values that are strictly increasing or decreasing to find "Next Greater/Smaller Element" in O(n).

### Top 'K' Elements
**Concept**: Use a Min-Heap of size K to track the K largest elements seen in a stream or array.

### Modified Binary Search
**Concept**: Applied to "Rotated Sorted Arrays" or "Search Space" problems. Key is determining which half is sorted to eliminate the other half.
