def max_sum_is(arr):
    """
    Problem: Find the maximum sum of a subsequence that is increasing.
    
    Approach: LIS Pattern
    - dp[i] = max sum of increasing subsequence ending at index i.
    - Initialize dp[i] = arr[i]
    - If arr[j] < arr[i], dp[i] = max(dp[i], dp[j] + arr[i])
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    n = len(arr)
    dp = arr[:]
    
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                dp[i] = max(dp[i], dp[j] + arr[i])
                
    return max(dp) if arr else 0

# Example Usage
if __name__ == "__main__":
    arr = [1, 101, 2, 3, 100]
    print(f"Max Sum Increasing Subsequence: {max_sum_is(arr)}")
