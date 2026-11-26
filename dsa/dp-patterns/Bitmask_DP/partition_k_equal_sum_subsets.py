def can_partition_k_subsets(nums, k):
    """
    Problem: Partition array into k subsets of equal sum.
    
    Approach: Bitmask DP
    - Target sum per subset = sum(nums) / k.
    - dp[mask] = current sum of the subset being built using elements in mask.
    - If dp[mask] == -1, state is invalid.
    - If dp[mask] reached target, we reset sum to 0 for next subset?
    - Better: dp[mask] = (current_sum_of_partial_subset) % target.
      If remainder is 0, it means we completed a subset.
    
    Time Complexity: O(2^N * N)
    Space Complexity: O(2^N)
    """
    total = sum(nums)
    if total % k != 0: return False
    target = total // k
    n = len(nums)
    
    # dp[mask] stores the current sum of the subset we are filling.
    # If a subset is filled (sum == target), we store 0 to indicate distinct fresh start.
    dp = [-1] * (1 << n)
    dp[0] = 0
    
    for mask in range(1 << n):
        if dp[mask] == -1: continue
        
        for i in range(n):
            if not ((mask >> i) & 1):
                new_sum = dp[mask] + nums[i]
                if new_sum <= target:
                    new_mask = mask | (1 << i)
                    if new_sum == target:
                        dp[new_mask] = 0
                    else:
                        dp[new_mask] = new_sum
                        
    return dp[(1 << n) - 1] == 0

# Example Usage
if __name__ == "__main__":
    nums = [4, 3, 2, 3, 5, 2, 1]
    k = 4
    print(f"Can partition into {k}: {can_partition_k_subsets(nums, k)}")
