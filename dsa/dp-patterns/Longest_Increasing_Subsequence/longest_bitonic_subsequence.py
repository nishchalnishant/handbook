def longest_bitonic_subsequence(arr):
    """
    Problem: Find length of longest bitonic subsequence (increases then decreases).
    
    Approach: LIS Pattern
    - Compute LIS ending at i -> `lis[i]`
    - Compute LDS starting at i (or LIS on reversed array) -> `lds[i]`
    - Result is max(lis[i] + lds[i] - 1) for all i.
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    n = len(arr)
    if n == 0: return 0
    
    lis = [1] * n
    for i in range(1, n):
        for j in range(i):
            if arr[i] > arr[j]:
                lis[i] = max(lis[i], lis[j] + 1)
                
    lds = [1] * n
    for i in range(n - 2, -1, -1):
        for j in range(n - 1, i, -1):
            if arr[i] > arr[j]:
                lds[i] = max(lds[i], lds[j] + 1)
                
    return max(lis[i] + lds[i] - 1 for i in range(n))

# Example Usage
if __name__ == "__main__":
    arr = [1, 11, 2, 10, 4, 5, 2, 1]
    print(f"Longest Bitonic Subsequence: {longest_bitonic_subsequence(arr)}")
