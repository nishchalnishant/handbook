# Unbounded Knapsack Pattern

## Introduction
The Unbounded Knapsack pattern allows for the repetition of items.

## Core Recursion Tree (W:4, wt:2)
```mermaid
graph TD
    A["UK(W=4)"] --> B["Use wt:2: UK(2)"]
    B --> C["Use wt:2: UK(0)"]
```

---

## Similar Problems

### 1. Coin Change (Ways)
**Recursion Tree (Amount:4, Coins:[1, 2])**:
```mermaid
graph TD
    A["Ways(4)"] --> B["Use 1: Ways(3)"]
    A --> C["Use 2: Ways(2)"]
    B --> D["Use 1: Ways(2)"]
    C --> E["Use 2: Ways(0) - Success"]
```

### 2. Coin Change (Min Coins)
**Recursion Tree**: (Same as Ways, but taking `min(1 + recursive_call)`).

### 3. Rod Cutting (Unbounded)
**Recursion Tree**: (Same as UK generic).

### 4. Minimum Cost for Tickets
**Recursion Tree (Day 1, passes [1, 7])**:
```mermaid
graph TD
    A["Day 1"] --> B["1-day: Cost + Day 2"]
    A --> C["7-day: Cost + Day 8"]
```

### 5. Perfect Squares
**Recursion Tree (N=5, squares: [1, 4])**:
```mermaid
graph TD
    A["N=5"] --> B["Use 1: 1 + N=4"]
    A --> C["Use 4: 1 + N=1"]
    B --> D["Use 4: 1 + N=0 - Success"]
```

### 6. Word Break
**Recursion Tree (s:'leetcode', dict:['leet', 'code'])**:
```mermaid
graph TD
    A["'leetcode'"] --> B["Match 'leet': Solve('code')"]
    B --> C["Match 'code': Solve('') - Success"]
```
*(Visualization of dictionary matching)*
