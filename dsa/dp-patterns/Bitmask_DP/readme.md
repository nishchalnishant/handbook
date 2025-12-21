# Bitmask DP

## Introduction
Bitmask DP is useful for problems that involve small constraints (usually $N \le 20$) where the state requires keeping track of a subset of elements.

## Core Recursion Tree (TSP Generic)
```mermaid
graph TD
    A["dp(mask=001, last=0)"] --> B["dp(mask=011, last=1)"]
    A --> C["dp(mask=101, last=2)"]
    B --> D["dp(mask=111, last=2)"]
```

---

## Similar Problems

### 1. Traveling Salesman Problem (TSP)
**Recursion Tree**: (Same as Core Recursion Tree above).

### 2. Minimum Incompatibility
**Recursion Tree (mask=1111, subset_size=2)**:
```mermaid
graph TD
    A["dp(1111)"] --> B["Submask 0011: dp(1100)"]
    A --> C["Submask 0101: dp(1010)"]
    A --> D["Submask 1001: dp(0110)"]
```

### 3. Assign Workers to Jobs
**Recursion Tree (Job 0, Workers {0,1,2})**:
```mermaid
graph TD
    A["Job 0, mask:000"] --> B["Assign W0: Job 1, mask:001"]
    A --> C["Assign W1: Job 1, mask:010"]
    A --> D["Assign W2: Job 1, mask:100"]
```

### 4. Max Student Compatibility
**Recursion Tree**: (Similar to Assignment Worker tree).

### 5. Partition to K Equal Sum Subsets
**Recursion Tree (target=5, mask=000)**:
```mermaid
graph TD
    A["mask:000, rem:5"] --> B["Take 2: mask:001, rem:3"]
    B --> C["Take 3: mask:011, rem:0 -> Reset to 5"]
    C --> D["mask:011, rem:5"]
```

### 6. Sudoku Solver (Bitmask Optimized)
**Recursion Tree**:
```mermaid
graph TD
    A["Cell(0,0), masks[R,C,B]"] --> B["Try 1 (if bit 1 clear)"]
    A --> C["Try 2 (if bit 2 clear)"]
```

### 7. Visit All Nodes
**Recursion Tree (BFS + Mask)**:
```mermaid
graph TD
    A["Node 0, mask:001"] --> B["Move to 1: Node 1, mask:011"]
    A --> C["Move to 2: Node 2, mask:101"]
```
