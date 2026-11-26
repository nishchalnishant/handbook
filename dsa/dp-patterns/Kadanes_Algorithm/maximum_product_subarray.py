def max_product_subarray(nums):
    """
    Problem: Find subarray with largest product.
    
    Approach: Modified Kadane's
    - Keep track of both max_prod and min_prod because negative * negative = positive.
    - When current num is negative, swapping max_prod and min_prod helps.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not nums: return 0
    
    res = max(nums)
    curr_max, curr_min = 1, 1
    
    for n in nums:
        if n == 0:
            curr_max, curr_min = 1, 1
            continue
            
        tmp = curr_max * n
        curr_max = max(n * curr_max, n * curr_min, n)
        curr_min = min(tmp, n * curr_min, n)
        
        res = max(res, curr_max)
        
    return res

# Example Usage
if __name__ == "__main__":
    nums = [2, 3, -2, 4]
    print(f"Max product subarray: {max_product_subarray(nums)}")
