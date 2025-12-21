# Grid DP

## Introduction
Grid DP involves problems on 2D matrices, often finding paths or optimal arrangements.

## Core Recursion Tree (Path sum)
```mermaid
graph TD
    A["(0,0)"] --> B["(0,1) R"]
    A --> C["(1,0) D"]
```

---

## Similar Problems

### 1. Unique Paths I/II
**Recursion Tree (2x2 Grid)**:
```mermaid
graph TD
    A["(0,0)"] --> B["(0,1)"]
    A --> C["(1,0)"]
    B --> D["(1,1) - Path 1"]
    C --> D["(1,1) - Path 2"]
```

### 2. Minimum Path Sum
**Recursion Tree**: (Same as Unique Paths, but minimizing cumulative cell value).

### 3. Dungeon Game
**Recursion Tree (Reverse state)**:
```mermaid
graph TD
    A["(2,2) Need: 1"] --> B["(2,1) Need: max(1, 1-val)"]
    A --> C["(1,2) Need: max(1, 1-val)"]
```

### 4. Gold Mine
**Recursion Tree (Current: (r, c))**:
```mermaid
graph TD
    A["(r, c)"] --> B["(r-1, c+1)"]
    A --> C["(r, c+1)"]
    A --> D["(r+1, c+1)"]
```

### 5. Cherry Pickup
**Recursion Tree (Person 1 at r1,c1; Person 2 at r2,c2)**:
```mermaid
graph TD
    A["(r1,c1), (r2,c2)"] --> B["(r1+1,c1), (r2+1,c2)"]
    A --> C["(r1+1,c1), (r2,c2+1)"]
    A --> D["(r1,c1+1), (r2+1,c2)"]
    A --> E["(r1,c1+1), (r2,c2+1)"]
```

### 6. Maximal Square
**Recursion Tree (Square side at r,c)**:
```mermaid
graph TD
    A["Side(r, c)"] --> B["Side(r-1, c)"]
    A --> C["Side(r, c-1)"]
    A --> D["Side(r-1, c-1)"]
```

### 7. Increasing Paths
**Recursion Tree (Start at (r, c))**:
```mermaid
graph TD
    A["(r, c)"] --> B["Next neighbor (if larger)"]
    B --> C["..."]
```
*(DFS exploration)*
