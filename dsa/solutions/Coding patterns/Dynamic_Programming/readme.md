# Dynamic Programming (DP) 💡

## Description
Dynamic Programming involves breaking down complex problems into simpler overlapping subproblems and storing their solutions (memoization) or solving them bottom-up (tabulation) to avoid redundant computations.

## Categories

### 1. 1D DP (Fibonacci & Linear)
- **Concept**: Current state depends on previous few states.
- **Problems**:
    - Climbing Stairs
    - House Robber
    - Fibonacci Number
    - Word Break
    - Maximum Product Subarray

### 2. Grid / 2D DP
- **Concept**: Minimum path sum or counting paths in a grid.
- **Problems**:
    - Unique Paths
    - Minimum Path Sum
    - Dungeon Game

### 3. Knapsack Variants
- **0/1 Knapsack**: Each item can be picked at most once.
    - *Problems*: Partition Equal Subset Sum, Target Sum.
- **Unbounded Knapsack**: Items can be picked multiple times.
    - *Problems*: Coin Change, Coin Change 2, Combination Sum IV.

### 4. Longest Common Subsequence (LCS)
- **Concept**: Matching characters between two strings.
- **Problems**:
    - Longest Common Subsequence
    - Edit Distance
    - Delete Operation for Two Strings

### 5. Longest Increasing Subsequence (LIS)
- **Concept**: Finding longest subsequence where elements are strictly increasing. Can be O(N^2) or O(N log N).
- **Problems**:
    - Longest Increasing Subsequence
    - Russian Doll Envelopes

### 6. Interval DP
- **Concept**: Operations on ranges or merging intervals.
- **Problems**:
    - Matrix Chain Multiplication
    - Burst Balloons
    - Longest Palindromic Subsequence
    - Palindromic Substrings

### 7. Bitmask DP
- **Concept**: Using bits to represent the state of visited nodes or included items (useful when N <= 20).
- **Problems**:
    - Partition to K Equal Sum Subsets
    - Shortest Path Visiting All Nodes

### 8. State Machine DP
- **Concept**: Modeling problem as state transitions (e.g., Hold, Sold, Cooldown).
- **Problems**:
    - Best Time to Buy and Sell Stock with Cooldown
    - Best Time to Buy and Sell Stock III
