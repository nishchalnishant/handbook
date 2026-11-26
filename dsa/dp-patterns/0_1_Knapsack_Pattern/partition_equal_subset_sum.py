def can_partition(nums):
    """
    Problem: Determine if the array can be partitioned into two subsets with equal sum.
    
    Approach: 0/1 Knapsack Pattern (Subset Sum Variation)
    - If total sum is odd, it's impossible.
    - If even, we need to find a subset with sum = total_sum / 2.
    
    Time Complexity: O(N * (Sum/2))
    Space Complexity: O(Sum/2)
    """
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    
    target = total_sum // 2
    
    # Standard Subset Sum problem
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    
    return dp[target]

# Example Usage
if __name__ == "__main__":
    nums = [1, 5, 11, 5]
    print(f"Can partition: {can_partition(nums)}")
