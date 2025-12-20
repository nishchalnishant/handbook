# Recursion Overview

Function calls itself to solve smaller instances of the problem.

## Concepts
- **Base Case**: Condition to stop recursion.
- **Recursive Step**: Reduce problem size.
- **Stack Overflow**: Risk of deep recursion.
- **Tail Recursion**: Optimization where recursive call is last.

---

## Problems & Solutions

### Easy
1. **[Factorial](Easy/factorial.py)**
   - n! = n * (n-1)!
2. **[Fibonacci](Easy/fibonacci.py)**
   - F(n) = F(n-1) + F(n-2).
3. **[Power of Two (Recursive)](Easy/power_of_two.py)**
   - n == 1 or (n%2==0 and check(n/2)).

### Medium
1. **[Pow(x, n)](../5.%20Divide%20and%20concuer/Medium/pow_x_n.py)**
   - Fast Exponentiation.
2. **[Tower of Hanoi](Medium/tower_of_hanoi.py)**
   - Move disks with auxiliary peg.
3. **[K-th Symbol in Grammar](Medium/kth_symbol.py)**
   - Recursively determine symbol.

### Hard
1. **[N-Queens](../6.%20Backtracking/Hard/n_queens.py)**
   - Backtracking is form of recursion.
2. **[Regular Expression Matching](Hard/regex_matching.py)**
   - DP/Recursion with wildcards.

---

## Tips for Interviews
- **Memoization**: Cache results to avoid re-computation (Top-Down DP).
- **Complexity**: Draw the recursion tree to analyze time/space.
