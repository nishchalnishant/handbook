def largest_divisible_subset(nums):
    """
    Problem: Largest subset where every pair (a, b) satisfies a%b==0 or b%a==0.
    
    Approach: Sorting + DP (LIS variant)
    - Sort nums.
    - dp[i] = size of largest divisible subset ending at i.
    - If nums[i] % nums[j] == 0 (for j < i), extend subset.
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    if not nums: return []
    nums.sort()
    n = len(nums)
    dp = [1] * n
    prev = [-1] * n
    max_idx = 0
    
    for i in range(1, n):
        for j in range(i):
            if nums[i] % nums[j] == 0:
                if dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    prev[i] = j
                    
        if dp[i] > dp[max_idx]:
            max_idx = i
            
    res = []
    while max_idx != -1:
        res.append(nums[max_idx])
        max_idx = prev[max_idx]
        
    return res[::-1]

# Example Usage
if __name__ == "__main__":
    nums = [1, 2, 3] # [1, 2] or [1, 3]
    print(f"Largest Divisible Subset: {largest_divisible_subset(nums)}")
