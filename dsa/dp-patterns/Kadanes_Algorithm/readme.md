# Kadane's Algorithm

## Introduction
Kadane's Algorithm is an efficient method to find the maximum sum subarray within a one-dimensional numeric array. It is a specific application of dynamic programming.

## Approach
1.  **State Definition**:
    -   `current_sum` keeps track of the maximum subarray sum ending at the current position.
    -   `max_so_far` keeps track of the global maximum sum found so far.

2.  **Recurrence Relation**:
    -   `current_sum = max(num, current_sum + num)`
        -   This decides whether to start a new subarray at the current number (`num`) or extend the existing subarray (`current_sum + num`).
    -   `max_so_far = max(max_so_far, current_sum)`

3.  **Base Case**:
    -   Initialize `current_sum` and `max_so_far` with the first element of the array (or a very small number if handling empty arrays isn't required).

4.  **Complexity**:
    -   Time Complexity: `O(n)` - Single pass.
    -   Space Complexity: `O(1)` - Only two variables are used.


## Similar Problems
-   **Maximum Circular Subarray Sum**: Max sum in circular array.
-   **Maximum Product Subarray**: Track min and max product at each step.
-   **Best Time to Buy and Sell Stock**: Maintain min price and check max profit.
-   **Stock II (Multiple Transactions)**: Accumulate positive slopes.
-   **Stock III (2 Transactions)**: Bidirectional DP or State Machine.
-   **Stock IV (k Transactions)**: Generalized version of Stock III.
-   **Max Subarray One Deletion**: Forward + Backward Kadane.
-   **Max Sum Rectangle**: 2D Kadane (Row accumulation).
