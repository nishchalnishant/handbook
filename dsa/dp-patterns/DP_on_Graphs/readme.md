# DP on Graphs

## Introduction
General Graph DP problems involve finding shortest paths, counting paths, or finding specific subgraphs.

## Core Recursion Tree (DAG Longest Path)
```mermaid
graph TD
    A["Longest(u)"] --> B["1 + Longest(v1)"]
    A --> C["1 + Longest(v2)"]
```

---

## Similar Problems

### 1. Longest Path in a DAG
**Recursion Tree**: (Same as Core Recursion Tree above).

### 2. Shortest Path in DAG
**Recursion Tree**: (Same as Longest Path, but using `min`).

### 3. Course Schedule
**Recursion Tree (Cycle Detection)**:
```mermaid
graph TD
    A["Course 0"] --> B["Course 1"]
    B --> C["Course 2"]
    C --> A["Back to 0 (Cycle)"]
```

### 4. Cheapest Flights Within K Stops
**Recursion Tree (Src:A, Dst:C, K:1)**:
```mermaid
graph TD
    A["A, stops:0"] --> B["B, stops:1"]
    A --> C["C, stops:1 - Success"]
    B --> B1["C, stops:2 - Fail (K=1)"]
```

### 5. Hamiltonian Path
**Recursion Tree (Mask=001, node=0)**:
```mermaid
graph TD
    A["mask:001, node:0"] --> B["mask:011, node:1"]
    B --> C["mask:111, node:2 - Full!"]
```

### 6. Word Ladder II
**Recursion Tree (hit -> cog)**:
```mermaid
graph TD
    A["hit"] --> B["hot"]
    B --> C["dot"]
    B --> D["lot"]
    C --> E["dog"]
    E --> F["cog - Success"]
```
*(Visualization of BFS/DFS search path)*
