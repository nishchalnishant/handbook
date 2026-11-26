# DP on Trees

## Introduction
DP on Trees involves solving problems on tree data structures where the solution for a node depends on its children.

## Core Recursion Tree (Generic DFS)
```mermaid
graph TD
    A["Node u"] --> B["DFS(c1)"]
    A --> C["DFS(c2)"]
```

---

## Similar Problems

### 1. Diameter of a Tree
**Recursion Tree**:
```mermaid
graph TD
    A["Node(1)"] --> B["L: Height(2)=1"]
    A --> C["R: Height(3)=2"]
    B --> D["..."]
    C --> E["..."]
    A_D["Diameter = 1+2 = 3"]
```

### 2. Maximum Path Sum
**Recursion Tree (Node values: [-10, 9, 20])**:
```mermaid
graph TD
    A["-10"] --> B["9"]
    A --> C["20"]
    B --> B1["0 (Leaf)"]
    C --> C1["0 (Leaf)"]
```

### 3. Binary Tree Cameras
**Recursion Tree (States: 0:Needs, 1:Has, 2:Covered)**:
```mermaid
graph TD
    A["Node"] --> B["Left: 0"]
    A --> C["Right: 2"]
    A_S["Return: 1 (Add Camera)"]
```

### 4. Distribute Coins in Binary Tree
**Recursion Tree (Coins: [3, 0, 0])**:
```mermaid
graph TD
    A["3"] --> B["0"]
    A --> C["0"]
    B --> B_ret["deficit: -1"]
    C --> C_ret["deficit: -1"]
    A_ret["surplus: +1"]
```

### 5. House Robber III
**Recursion Tree (Pair: [Rob, Skip])**:
```mermaid
graph TD
    A["Node"] --> B["L: [10, 5]"]
    A --> C["R: [20, 15]"]
    A_R["Rob: Val + 5 + 15"]
    A_S["Skip: max(L) + max(R)"]
```

### 6. Max Independent Set
**Recursion Tree**: (Same logic as House Robber III with weights of 1).
