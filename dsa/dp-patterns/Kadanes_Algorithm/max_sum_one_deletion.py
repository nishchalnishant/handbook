def maximum_sum_one_deletion(arr):
    """
    Problem: Leetcode 1186. Max subarray sum with at most one deletion.
    
    Approach: Kadane's Variation
    - forward[i]: Max subarray ending at i.
    - backward[i]: Max subarray starting at i.
    - Result is max(forward[i-1] + backward[i+1]) or max(forward).
    
    Time Complexity: O(N)
    Space Complexity: O(N)
    """
    n = len(arr)
    if n == 1: return arr[0]
    
    fw = [0] * n
    bw = [0] * n
    
    # Forward Kadane
    current = arr[0]
    fw[0] = current
    max_so_far = current
    for i in range(1, n):
        current = max(arr[i], current + arr[i])
        fw[i] = current
        max_so_far = max(max_so_far, current)
        
    # Backward Kadane
    current = arr[n-1]
    bw[n-1] = current
    for i in range(n - 2, -1, -1):
        current = max(arr[i], current + arr[i])
        bw[i] = current
        
    # Check deletion point
    res = max_so_far
    for i in range(1, n - 1):
        res = max(res, fw[i-1] + bw[i+1])
        
    return res

# Example Usage
if __name__ == "__main__":
    arr = [1, -2, 0, 3]
    print(f"Max sum with one deletion: {maximum_sum_one_deletion(arr)}")
