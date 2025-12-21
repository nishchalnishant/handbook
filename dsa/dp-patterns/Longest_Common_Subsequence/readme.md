# Longest Common Subsequence (LCS)

## Introduction
The LCS pattern involves finding the longest subsequence present in two sequences (strings or arrays) in the same relative order but not necessarily contiguous. This pattern is fundamental for string manipulation and comparison problems.

## Approach
1.  **State Definition**:
    -   `dp[i][j]` represents the length of the properties (e.g., LCS) for the first `i` characters of string `s1` and the first `j` characters of string `s2`.

2.  **Recurrence Relation**:
    -   If `s1[i-1] == s2[j-1]` (matching characters):
        -   `dp[i][j] = 1 + dp[i-1][j-1]`
    -   If `s1[i-1] != s2[j-1]` (different characters):
        -   `dp[i][j] = max(dp[i-1][j], dp[i][j-1])` (Skip char from s1 or skip char from s2)

3.  **Base Case**:
    -   `dp[i][0] = 0` and `dp[0][j] = 0` (Empty string comparisons).

4.  **Variations**:
    -   Longest Common Substring (reset to 0 on mismatch).
    -   Shortest Common Supersequence.
    -   Minimum insertions/deletions to convert s1 to s2.

## Similar Problems
-   **Longest Common Substring**: Contiguous version of LCS.
-   **Edit Distance**: Min operations to convert one string to another.
-   **Longest Palindromic Subsequence**: LCS of string and its reverse.
-   **Shortest Common Supersequence**: Shortest string containing both strings.
-   **Distinct Subsequences**: Count ways t is subsequence of s.
-   **Wildcard Matching**: Matching with `?` and `*`.
-   **Regular Expression Matching**: Matching with `.` and `*` (preceding element logic).
