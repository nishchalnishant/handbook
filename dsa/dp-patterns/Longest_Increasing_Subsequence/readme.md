# Longest Increasing Subsequence (LIS)

## Introduction
The LIS pattern involves finding the length of the longest strictly increasing subsequence.

## Core Recursion Tree (idx:0, prev:-inf)
```mermaid
graph TD
    A["LIS(idx:0, prev:-inf)"] --> B["Skip 10: LIS(1, -inf)"]
    A --> C["Include 10: 1 + LIS(1, 10)"]
```

---

## Similar Problems

### 1. Maximum Sum Increasing Subsequence
**Recursion Tree (idx:0, prev:-inf)**:
```mermaid
graph TD
    A["MSIS(0, -inf)"] --> B["Skip 10: MSIS(1, -inf)"]
    A --> C["Inc 10: 10 + MSIS(1, 10)"]
```

### 2. Russian Doll Envelopes
**Recursion Tree**: (Sort width, then LIS on height tree same as above).

### 3. Longest Bitonic Subsequence
**Recursion Tree**:
```mermaid
graph TD
    A["State(i)"] --> B["Inc: LIS(0...i)"]
    A --> C["Dec: LDS(i...n-1)"]
```

### 4. Box Stacking
**Recursion Tree**: (MSIS logic on sorted rotations).

### 5. Building Bridges
**Recursion Tree**: (Sort North, LIS on South).

### 6. Largest Divisible Subset
**Recursion Tree (arr:[1, 2, 4])**:
```mermaid
graph TD
    A["LDS(0, prev:1)"] --> B["Take 1: 1 + LDS(1, 1)"]
    B --> C["Take 2 (2%1=0): 1 + LDS(2, 2)"]
    C --> D["Take 4 (4%2=0): 1 + LDS(3, 4)"]
```
*(Divide-and-conquer logic)*
