def count_subsets(nums, target):
    """
    Problem: Count the number of subsets with a sum equal to 'target'.
    
    Approach: 0/1 Knapsack Pattern
    - state: dp[j] = number of ways to achieve sum 'j'.
    - transition: dp[j] += dp[j - num]
    
    Time Complexity: O(N * Target)
    Space Complexity: O(Target)
    """
    dp = [0] * (target + 1)
    dp[0] = 1 # One way to get sum 0 (empty subset)

    for num in nums:
        for j in range(target, num - 1, -1):
            dp[j] += dp[j - num]
            
    return dp[target]

# Example Usage
if __name__ == "__main__":
    nums = [1, 2, 3, 3]
    target = 6
    print(f"Number of subsets with sum {target}: {count_subsets(nums, target)}")
