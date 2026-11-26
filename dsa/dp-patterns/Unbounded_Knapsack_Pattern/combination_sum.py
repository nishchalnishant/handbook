def combination_sum_4(nums, target):
    """
    Problem: Find number of combinations (permutations allowed!) that add up to target.
    (Note: Leetcode calls it Combination Sum IV, but it's really counting permutations).
    
    Approach: Unbounded Knapsack / Coin Change Ways (Order matters)
    - If order matters: outer loop target, inner loop nums.
    - dp[i] = sum(dp[i - num]) for num in nums.
    - This is exactly like Climbing Stairs but with variable steps.
    
    Time Complexity: O(Target * N)
    Space Complexity: O(Target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1
    
    for i in range(1, target + 1):
        for num in nums:
            if i >= num:
                dp[i] += dp[i - num]
                
    return dp[target]

# Example Usage
if __name__ == "__main__":
    nums = [1, 2, 3]
    target = 4
    print(f"Combinations: {combination_sum_4(nums, target)}")
