# Matrix Chain Multiplication (MCM)

## Introduction
The MCM pattern involves determining the most efficient way to multiply a given sequence of matrices. The problem isn't to perform the multiplication, but to decide the order in which to perform the multiplications (parenthesization) to minimize the number of scalar multiplications.

## Approach
1.  **State Definition**:
    -   `dp[i][j]` = minimum number of scalar multiplications needed to compute the matrix chain from index `i` to `j`.

2.  **Recurrence Relation**:
    -   To calculate `dp[i][j]`, we can split the chain at any `k` between `i` and `j` (`i <= k < j`).
    -   `dp[i][j] = min(dp[i][k] + dp[k+1][j] + cost(i, k, j))`
        -   Where `cost(i, k, j)` is the cost of multiplying the resulting two matrices (dimensions `arr[i-1] x arr[k]` and `arr[k] x arr[j]`).

3.  **Base Case**:
    -   `dp[i][i] = 0` (Simple matrix requires 0 multiplications).

4.  **Partition DP**:
    -   This pattern is a general "Interval DP" or "Partition DP" where we solve for every interval length `L` from 2 to `n`.


## Similar Problems
-   **Burst Balloons**: Maximize coins by bursting balloons.
-   **Palindrome Partitioning**: Min cuts to make all substrings palindromes.
-   **Boolean Parenthesization**: Parse expression to evaluate to True.
-   **Evaluate to True**: Same as Boolean Parenthesization.
-   **Minimum Score Triangulation**: Triangulate polygon to minimize score.
-   **Stick Cutting**: Min cost to cut stick at given points.
-   **Optimal BST**: Minimize search cost given frequencies.
-   **Scramble String**: Verification using interval DP (also listed in LCS).
