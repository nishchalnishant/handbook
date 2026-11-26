# Backtracking 🔙

## Description
Backtracking is an algorithmic-technique for solving problems recursively by trying to build a solution incrementally, one piece at a time, removing those solutions that fail to satisfy the constraints of the problem at any point of time.

## Strategies

### 1. Subsets / Combinations
- **Concept**: Iterate through elements, making a choice to Include or Exclude the current element, then recurse.
- **Problems**:
    - Subsets
    - Combination Sum
    - Subsets II
    - Combination Sum II
    - Letter Combinations of a Phone Number

### 2. Permutations
- **Concept**: Ordering matters. Iterate through available numbers, adding valid ones to the current path and marking them as used.
- **Problems**:
    - Permutations
    - Permutations II (Unique)

### 3. Grid Search (DFS Backtracking)
- **Concept**: Move through a grid (up, down, left, right). Mark cells visited before moving, and unmark (backtrack) after returning.
- **Problems**:
    - Word Search
    - Unique Paths III

### 4. Constraint Satisfaction (N-Queens)
- **Concept**: Place items such that they don't attack/invalidate each other.
- **Problems**:
    - N-Queens
    - Sudoku Solver
    - Palindrome Partitioning
    - Restore IP Addresses
