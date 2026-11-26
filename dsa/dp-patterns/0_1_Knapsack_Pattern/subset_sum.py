def subset_sum(nums, target):
    """
    Problem: Check if there exists a subset of the given array 'nums' whose sum is equal to 'target'.
    
    Approach: 0/1 Knapsack Pattern
    - state: dp[i][j] = True if a sum of 'j' can be achieved using the first 'i' items.
    - transition:
        - Exclude item: dp[i][j] = dp[i-1][j]
        - Include item: dp[i][j] = dp[i-1][j - nums[i-1]] (if j >= nums[i-1])
    
    Time Complexity: O(N * Target)
    Space Complexity: O(Target) (Optimized 1D array)
    """
    n = len(nums)
    # dp[j] stores whether sum 'j' is reachable
    dp = [False] * (target + 1)
    dp[0] = True  # Sum 0 is always reachable (empty subset)

    for num in nums:
        # Iterate backwards to avoid using the same element multiple times for the same sum
        for j in range(target, num - 1, -1):
            if dp[j - num]:
                dp[j] = True
    
    return dp[target]

# Example Usage
if __name__ == "__main__":
    nums = [3, 34, 4, 12, 5, 2]
    target = 9
    print(f"Subset with sum {target} exists: {subset_sum(nums, target)}")
