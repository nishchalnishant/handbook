# Matrix Chain Multiplication (MCM)

## Introduction
The MCM pattern involves optimal parenthesization of a sequence of operations to minimize total cost.

## Core Recursion Tree (Split [1, 4] at k)
```mermaid
graph TD
    A["Solve(1, 4)"] --> B["k=1: (A)*(BCD)"]
    A --> C["k=2: (AB)*(CD)"]
    A --> D["k=3: (ABC)*(D)"]
```

---

## Similar Problems

### 1. Burst Balloons
**Recursion Tree (Range [i, j], last burst k)**:
```mermaid
graph TD
    A["Burst(1, 3)"] --> B["k=1: B(2,3) + last(1)"]
    A --> C["k=2: B(1,1)+B(3,3) + last(2)"]
    A --> D["k=3: B(1,2) + last(3)"]
```

### 2. Palindrome Partitioning
**Recursion Tree (String 'aab')**:
```mermaid
graph TD
    A["'aab'"] --> B["'a' | 'ab'"]
    A --> C["'aa' | 'b'"]
    B --> D["'a'|'a'|'b'"]
```

### 3. Boolean Parenthesization
**Recursion Tree (Exp: T|F&T, target:True)**:
```mermaid
graph TD
    A["T|F&T, target:T"] --> B["Split at |: (T,T)|(F&T,F/T)"]
    A --> C["Split at &: (T|F,F/T)&(T,T)"]
```

### 4. Optimal Binary Search Tree
**Recursion Tree (Keys: [1,2,3])**:
```mermaid
graph TD
    A["Range(1,3)"] --> B["Root 1: Range(2,3)"]
    A --> C["Root 2: R(1,1)+R(3,3)"]
    A --> D["Root 3: Range(1,2)"]
```

### 5. Stick Cutting
**Recursion Tree (Stick length 7, cuts [1,3,4,5])**:
```mermaid
graph TD
    A["Solve(0, 7)"] --> B["Cut at 1: S(0,1)+S(1,7)"]
    A --> C["Cut at 3: S(0,3)+S(3,7)"]
    A --> D["Cut at 4: S(0,4)+S(4,7)"]
```
*(Interval DP logic)*
