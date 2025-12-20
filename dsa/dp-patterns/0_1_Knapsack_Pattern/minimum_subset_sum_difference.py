def min_subset_sum_diff(nums):
    """
    Problem: Partition array into two subsets such that the absolute difference of their sums is minimized.
    
    Approach: 0/1 Knapsack Pattern
    - Find all reachable sums up to total_sum // 2.
    - Let S1 be the largest reachable sum <= total_sum // 2.
    - S2 will be total_sum - S1.
    - Diff = S2 - S1 = total_sum - 2 * S1.
    
    Time Complexity: O(N * Sum)
    Space Complexity: O(Sum)
    """
    total_sum = sum(nums)
    target = total_sum // 2
    
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    
    # Find list reachable sum closest to target
    for j in range(target, -1, -1):
        if dp[j]:
            return total_sum - 2 * j
            
    return total_sum

# Example Usage
if __name__ == "__main__":
    nums = [1, 6, 11, 5]
    print(f"Minimum subset difference: {min_subset_sum_diff(nums)}")
