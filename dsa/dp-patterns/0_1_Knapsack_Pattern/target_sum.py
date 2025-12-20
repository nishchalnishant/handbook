def find_target_sum_ways(nums, target):
    """
    Problem: Assign '+' or '-' to each element to reach a target sum.
    
    Approach: 0/1 Knapsack Pattern
    - Let P be sum of positive elements, N be sum of negative elements (absolute val).
    - P - N = target
    - P + N = total_sum
    - Adding: 2P = target + total_sum => P = (target + total_sum) / 2
    - Problem reduces to: Find count of subsets with sum P.
    
    Time Complexity: O(N * Target)
    Space Complexity: O(Target)
    """
    total_sum = sum(nums)
    
    # Constraints check
    if abs(target) > total_sum or (total_sum + target) % 2 != 0:
        return 0
        
    subset_sum_target = (total_sum + target) // 2
    
    dp = [0] * (subset_sum_target + 1)
    dp[0] = 1

    for num in nums:
        for j in range(subset_sum_target, num - 1, -1):
            dp[j] += dp[j - num]
            
    return dp[subset_sum_target]

# Example Usage
if __name__ == "__main__":
    nums = [1, 1, 1, 1, 1]
    target = 3
    print(f"Ways to assign symbols for target {target}: {find_target_sum_ways(nums, target)}")
