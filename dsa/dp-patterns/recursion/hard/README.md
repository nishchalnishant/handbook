# Hard Recursion Problems - Detailed Guide

Hard recursion problems typically involve complex constraints, optimizing search spaces (pruning), or handling multiple recursive branches with memoization.

---

## 1. N-Queens
**Description**: Place $N$ queens on an $N \times N$ chessboard such that no two queens attack each other.
**Process**:
- Try placing a queen in each row.
- For each row, iterate through columns and check if it's "safe".
- Backtrack if no position works.

**Recursion Tree (Simplified for 4-Queens)**:
```mermaid
graph TD
    Root["Board Empty"] --> Q11["Q at (0,0)"]
    Root --> Q12["Q at (0,1)"]
    Q11 --> Q23["Q at (1,2)"]
    Q11 --> Q24["Q at (1,3)"]
    Q23 --> Fail["No space in Row 2"]
```

---

## 2. Sudoku Solver
**Description**: Fill a 9x9 grid so each row, column, and 3x3 subgrid contains digits 1-9.
**Process**:
- Find an empty cell. Try digits 1-9.
- If valid, recurse. Backtrack if dead end.

**Recursion Tree (Logic Branch)**:
```mermaid
graph TD
    Empty["Board[...] = '.'"] --> Try1["Try '1'"]
    Empty --> Try2["Try '2'"]
    Try1 --> Valid["Valid? Recurse(...)"]
    Try1 --> Invalid["Invalid? Backtrack"]
```

---

## 3. Word Search II
**Description**: Given a grid of characters and a list of words, find all words in the grid.
**Process**:
- DFS from each cell. Mask visited cells with '#'.
- Check 4 neighbors.

**Recursion Tree (DFS search for 'CAT')**:
```mermaid
graph TD
    C["'C' at (0,0)"] --> A["'A' at (0,1)"]
    C --> A2["'A' at (1,0)"]
    A --> T["'T' at (0,2) - Found!"]
```

---

## 4. Palindromic Partitioning
**Description**: Partition a string into all possible palindromes.
**Process**:
- Check if prefix is palindrome. Recurse for remaining suffix.

**Recursion Tree (for "aab")**:
```mermaid
graph TD
    Root["'aab'"] --> A1["'a' | 'ab'"]
    Root --> A2["'aa' | 'b'"]
    A1 --> B1["'a' | 'a' | 'b'"]
    A2 --> B2["'aa' | 'b'"]
```

---

## 5. Wildcard Matching
**Description**: Implement pattern matching with `?` and `*`.
**Process**:
- If `*`, branches into `skip *` or `consume char`.

**Recursion Tree (s:'aa', p:'a*')**:
```mermaid
graph TD
    A["match('aa', 'a*')"] --> B["match('a', '*')"]
    B --> C["match('a', '') - Skip *"]
    B --> D["match('', '*') - Consume 'a'"]
    D --> E["match('', '') - Skip * - Success"]
```

---

## 6. Regular Expression Matching
**Description**: Implement matching with `.` and `*`.
**Process**:
- `*` is more complex: zero or more of *preceding* char.

**Recursion Tree (s:'aa', p:'a*')**:
```mermaid
graph TD
    A["match('aa', 'a*')"] --> B["match('aa', '') - Zero occurrences"]
    A --> C["match('a', 'a*') - One occurrence"]
    C --> D["match('', 'a*') - Two occurrences"]
    D --> E["match('', '') - Success"]
```

---

## 7. Flatten a Nested List
**Description**: Convert a multi-level list into a single-level list.
**Process**:
- If element is list, recurse. Else append.

**Recursion Tree ([1, [2, 3]])**:
```mermaid
graph TD
    Root["[1, [2,3]]"] --> E1["1 (Append)"]
    Root --> E2["[2, 3] (Recurse)"]
    E2 --> E21["2 (Append)"]
    E2 --> E22["3 (Append)"]
```

---

## 8. K-th Permutation Sequence
**Description**: Find the $k$-th permutation using factorial logic.
**Process**:
- Narrow down the grouping using factorials.

**Recursion Tree (n=3, k=3 group choice)**:
```mermaid
graph TD
    Root["n=3, k=3"] --> G1["Group 1 (starts with 1)"]
    Root --> G2["Group 2 (starts with 2) - Selected"]
    G2 --> Sub["n=2, k=1"]
```

---

## 9. Rat in a Maze
**Description**: Find paths in a maze with obstacles.
**Process**:
- 4-direction DFS with backtracking.

**Recursion Tree (Path search)**:
```mermaid
graph TD
    S["(0,0)"] --> D["(1,0)"]
    S --> R["(0,1)"]
    D --> DR["(1,1)"]
```

---

## 10. M-Coloring Problem
**Description**: Color vertices such that no adjacent vertices share a color.
**Process**:
- Try $M$ colors for each vertex.

**Recursion Tree (3 nodes, 2 colors)**:
```mermaid
graph TD
    V1["Node 0: Red"] --> V2R["Node 1: Red (Fail)"]
    V1 --> V2B["Node 1: Blue (Valid)"]
    V2B --> V3B["Node 2: Blue (Fail)"]
```
 Riverside,
---
