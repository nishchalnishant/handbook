# Fibonacci / Simple Recurrence DP

## Introduction
This pattern covers problems following a linear recurrence relation, like $F(n) = F(n-1) + F(n-2)$.

## Core Recursion Tree (Fibonacci 4)
```mermaid
graph TD
    A["F(4)"] --> B["F(3)"]
    A --> C["F(2)"]
    B --> D["F(2)"]
    B --> E["F(1)"]
    C --> F["F(1)"]
    C --> G["F(0)"]
```

---

## Similar Problems

### 1. Climbing Stairs
**Recursion Tree (Stairs=3)**:
```mermaid
graph TD
    A["Stair 3"] --> B["Stair 2 (1 step)"]
    A --> C["Stair 1 (2 steps)"]
    B --> D["Stair 1 (1 step)"]
    B --> E["Stair 0 (2 steps) - Done"]
```

### 2. House Robber
**Recursion Tree (idx:2, arr:[1, 2, 3])**:
```mermaid
graph TD
    A["Rob(2)"] --> B["Inc 2: 3 + Rob(0)"]
    A --> C["Exc 2: Rob(1)"]
```

### 3. Decode Ways
**Recursion Tree ('121')**:
```mermaid
graph TD
    A["'121'"] --> B["'1'|'21'"]
    A --> C["'12'|'1'"]
```

### 4. Tiling Problems
**Recursion Tree (N=3)**:
```mermaid
graph TD
    A["N=3"] --> B["Vertical: N=2"]
    A --> C["Horizontal: N=1"]
```

### 5. Catalan Numbers (BST Count)
**Recursion Tree (N=2)**:
```mermaid
graph TD
    A["N=2"] --> B["Root 1: BST(0)*BST(1)"]
    A --> C["Root 2: BST(1)*BST(0)"]
```

### 6. Paint Fence
**Recursion Tree (3 posts, 2 colors)**:
```mermaid
graph TD
    A["Post 3"] --> B["Same as 2"]
    A --> C["Diff from 2"]
```
*(Limited by rule: no 3 same in a row)*
