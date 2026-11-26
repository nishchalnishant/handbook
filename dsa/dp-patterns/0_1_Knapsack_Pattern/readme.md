# 0/1 Knapsack Pattern

## Introduction
The 0/1 Knapsack pattern is a classic dynamic programming problem where you are given a set of items, each with a weight and a value. The goal is to maximize the total value of items included in a knapsack without exceeding a given weight capacity `W`. "0/1" implies that each item can either be picked (1) or not picked (0).

## Core Recursion Tree (Base Problem)
For an item with `weight=2, value=3` and remaining capacity `W=3`:

```mermaid
graph TD
    A["Knapsack(i, W=3)"] --> B["Exclude: Knapsack(i-1, 3)"]
    A --> C["Include: 3 + Knapsack(i-1, 1)"]
```

---

## Similar Problems

### 1. Subset Sum
**Problem**: Check if there's a subset of numbers that adds up to a target sum.
**Recursion Tree (Target=5, arr=[2, 3])**:
```mermaid
graph TD
    A["SS(5, idx:0)"] --> B["Exclude 2: SS(5, idx:1)"]
    A --> C["Include 2: SS(3, idx:1)"]
    C --> D["Include 3: SS(0, idx:2) - True"]
```

### 2. Partition Equal Subset Sum
**Problem**: Can an array be partitioned into two subsets with equal sums?
**Recursion Tree (Sum=3, arr=[1, 2, 3])**:
```mermaid
graph TD
    A["Sum(3, idx:0)"] --> B["Inc 1: Sum(2, idx:1)"]
    A --> C["Exc 1: Sum(3, idx:1)"]
    B --> D["Inc 2: Sum(0) - Success"]
```

### 3. Count Subsets with Given Sum
**Problem**: Count the number of subsets that sum to a target.
**Recursion Tree (Target=3, arr=[1, 2])**:
```mermaid
graph TD
    A["Count(3, idx:0)"] --> B["Inc 1: Count(2, idx:1)"]
    A --> C["Exc 1: Count(3, idx:1)"]
    B --> D["Inc 2: Count(0) - (1)"]
    C --> E["Inc 2: Count(1) - (0)"]
```

### 4. Minimum Subset Sum Difference
**Problem**: Partition the array into two subsets $S_1$ and $S_2$ such that $|sum(S_1) - sum(S_2)|$ is minimized.
**Recursion Tree**: (Identical to Subset Sum logic - find achieving sum closest to $Total/2$).

### 5. Target Sum
**Problem**: Assign `+` or `-` to each element to reach a target sum.
**Recursion Tree (Target=1, arr=[1, 1])**:
```mermaid
graph TD
    A["TS(1, 0)"] --> B["+1: TS(0, 1)"]
    A --> C["-1: TS(2, 1)"]
    B --> D["+1: TS(-1, 2)"]
    B --> E["-1: TS(1, 2) - Success"]
```

### 6. Rod Cutting (Bounded)
**Problem**: Maximize profit by cutting a rod, where each length has a limited count.
**Recursion Tree**: (Similar to Knapsack split).

### 7. Assign Tasks
**Problem**: Maximize total importance of tasks within a time limit.
**Recursion Tree**: (Classic Knapsack tree).
