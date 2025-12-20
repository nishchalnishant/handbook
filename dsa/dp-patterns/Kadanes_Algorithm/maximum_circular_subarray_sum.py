def max_circular_subarray_sum(nums):
    """
    Problem: Find maximum subarray sum in a circular array.
    
    Approach: Kadane's Algorithm
    - Case 1: Max sum is in non-circular part (Normal Kadane).
    - Case 2: Max sum wraps around.
        - Wrap around sum = Total Sum - Min Subarray Sum.
    - Result = Max(Case 1, Case 2).
    - Corner case: If all numbers are negative, Max Circular Sum is just the max element (Case 1), as Total-Min would give 0 (empty subarray implication).
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    def kadane(arr):
        max_so_far, curr_max = float('-inf'), 0
        for x in arr:
            curr_max = max(x, curr_max + x)
            max_so_far = max(max_so_far, curr_max)
        return max_so_far
        
    def min_kadane(arr):
        min_so_far, curr_min = float('inf'), 0
        for x in arr:
            curr_min = min(x, curr_min + x)
            min_so_far = min(min_so_far, curr_min)
        return min_so_far

    max_kadane = kadane(nums)
    if max_kadane < 0: # All negative
        return max_kadane
        
    total_sum = sum(nums)
    min_k = min_kadane(nums)
    max_circular = total_sum - min_k
    
    return max(max_kadane, max_circular)

# Example Usage
if __name__ == "__main__":
    nums = [5, -3, 5]
    print(f"Max circular sum: {max_circular_subarray_sum(nums)}")
