# Longest Increasing Subsequence (LIS)

## Introduction
The LIS pattern involves finding the length of the longest subsequence of a given sequence such that all elements of the subsequence are sorted in increasing order.

## Approach
1.  **State Definition**:
    -   `dp[i]` = length of the longest increasing subsequence ending at index `i`.

2.  **Recurrence Relation**:
    -   For each element `i` from `0` to `n-1`:
        -   Iterate through all previous elements `j` (`0` to `i-1`).
        -   If `arr[i] > arr[j]`:
            -   `dp[i] = max(dp[i], dp[j] + 1)`

3.  **Base Case**:
    -   `dp[i] = 1` for all `i` (Every element is an increasing subsequence of length 1).

4.  **Optimization**:
    -   The standard DP approach is `O(n^2)`.
    -   This can be optimized to `O(n log n)` using Binary Search (Patience Sorting approach).

## Similar Problems
-   **Maximum Sum Increasing Subsequence**: LIS with sum weights.
-   **Number of LIS**: Count all longest increasing subsequences.
-   **Russian Doll Envelopes**: Sorting + LIS on 2D dimensions.
-   **Longest Chain of Pairs**: Chain pairs (a,b) -> (c,d) where b < c.
-   **Longest Bitonic Subsequence**: Longest subsequence that increases then decreases.
-   **Box Stacking**: Stack boxes (rotations allowed, strictly smaller base).
-   **Building Bridges**: Max non-crossing bridges (sort N, LIS S).
-   **Largest Divisible Subset**: Subset where a%b==0 or b%a==0 for all pairs.
