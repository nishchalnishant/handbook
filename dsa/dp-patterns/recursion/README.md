# Recursion: The Foundation of Dynamic Programming

Recursion is a process where a function calls itself as a subroutine. This allows the function to be repeated several times, as it can call itself during its execution. Recursion is the "mother of all DP problems" because every DP solution can be first thought of as a recursive solution (top-down) before being optimized with memoization or converted to an iterative approach (bottom-up).

## How to Solve Recursion Problems

1.  **Define the Base Case**: What is the simplest possible input that can be solved immediately? This is the termination condition for the recursion.
2.  **Define the Recursive Step**: How can you break down the problem into smaller subproblems of the same type?
3.  **Combine the Results**: How do you use the results of the subproblems to solve the original problem?
4.  **Trust the Recursion**: Assume the recursive call works correctly for smaller inputs.

## Problem Roadmap

### Easy Problems
1.  **Factorial**: Calculate $n!$.
2.  **Fibonacci**: Find the $n$-th Fibonacci number.
3.  **Sum of Digits**: Find the sum of digits of a number.
4.  **Power (x, n)**: Calculate $x^n$.
5.  **Reverse a String**: Reverse a given string recursively.
6.  **Palindrome Check**: Check if a string is a palindrome.
7.  **Count Set Bits**: Count the number of 1s in the binary representation of a number.
8.  **Array Sum**: Calculate the sum of elements in an array.
9.  **Binary Search**: Implement binary search recursively.
10. **Length of String**: Find the length of a string recursively.

### Medium Problems
1.  **Subsets (Power Set)**: Generate all possible subsets of a set.
2.  **Permutations**: Generate all permutations of a string or array.
3.  **Tower of Hanoi**: Solve the classic Tower of Hanoi puzzle.
4.  **Combination Sum**: Find all combinations that sum to a target value.
5.  **Letter Combinations of a Phone Number**: Map digits to letters.
6.  **Generate Parentheses**: Generate all valid combinations of $n$ pairs of parentheses.
7.  **Subset Sum**: Check if a subset exists with a given sum.
8.  **Josephus Problem**: Find the survivor in a circle of people.
9.  **String to Integer (atoi)**: Implement atoi recursively.
10. **Binary Tree Traversal**: Pre-order, In-order, and Post-order traversals.

### Hard Problems
1.  **N-Queens**: Place $n$ queens on an $n \times n$ chessboard such that no two queens attack each other.
2.  **Sudoku Solver**: Solve a given Sudoku board.
3.  **Word Search II**: Find all words from a dictionary in a 2D grid.
4.  **Palindromic Partitioning**: Partition a string into all possible palindromes.
5.  **Wildcard Matching**: Implement wildcard pattern matching with '?' and '*'.
6.  **Regular Expression Matching**: Implement regex matching with '.' and '*'.
7.  **Flatten a Nested List**: Flatten a multi-level list.
8.  **K-th Permutation Sequence**: Find the $k$-th permutation of a set.
9.  **Rat in a Maze**: Find all paths from start to end in a maze.
10. **M-Coloring Problem**: Color a graph with $m$ colors such that no two adjacent vertices have the same color.
