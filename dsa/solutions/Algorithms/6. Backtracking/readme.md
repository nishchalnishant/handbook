# Backtracking Overview ↩️

Build solution candidates incrementally and abandon ("backtrack") as soon as it determines the candidate cannot possibly be a valid solution.

## Concepts
- **Explore**: Recursive Depth First Search.
- **Constraints**: Check validity at each step.
- **Pruning**: Stop early if current path is invalid.

---

## Problems & Solutions

### Medium
1. **[Permutations](Medium/permutations.py)**
   - Generate all possible orderings.
2. **[Subsets](Medium/subsets.py)**
   - Generate power set.
3. **[Combination Sum](Medium/combination_sum.py)**
   - Find combinations summing to target.
4. **[Word Search](Medium/word_search.py)**
   - Exist in 2D grid?
5. **[Generate Parentheses](../3.%20Stack%20and%20queue/Medium/generate_parentheses.py)**
   - Valid parenthesis combinations.

### Hard
1. **[N-Queens](Hard/n_queens.py)**
   - Place N queens on NxN board without attacking.
2. **[Sudoku Solver](Hard/sudoku_solver.py)**
   - Fill sudoku board.

---

## Tips for Interviews
- **State Space Tree**: Visualize the recursion tree.
- **Complexity**: Often O(N!), O(2^N).
- **Mutable vs Immutable**: Be careful passing lists in recursion (copy if needed).
