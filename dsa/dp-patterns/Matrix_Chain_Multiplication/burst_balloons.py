def max_coins(nums):
    """
    Problem: Leetcode 312. Burst Balloons.
    Given n balloons, burst index i to get nums[i-1]*nums[i]*nums[i+1] coins. Maximize coins.
    
    Approach: MCM Pattern (Interval DP)
    - Add 1 to start and end of array.
    - dp[i][j] = max coins from bursting balloons strictly between i and j.
    - k is the LAST balloon to burst in (i, j).
    - dp[i][j] = max(dp[i][k] + dp[k][j] + nums[i]*nums[k]*nums[j]) for k in (i, j).
    
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    """
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n): # Length of range (i, j)
        for i in range(n - length):
            j = i + length
            for k in range(i + 1, j):
                dp[i][j] = max(dp[i][j], 
                               dp[i][k] + dp[k][j] + nums[i] * nums[k] * nums[j])
                               
    return dp[0][n-1]

# Example Usage
if __name__ == "__main__":
    nums = [3, 1, 5, 8]
    print(f"Max coins: {max_coins(nums)}")
