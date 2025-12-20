def rob(nums):
    """
    Problem: Maximize money robbed without alerting police (cannot rob adjacent houses).
    
    Approach: Fibonacci variation
    - dp[i] = max(dp[i-1], dp[i-2] + nums[i])
    - Rob current house 'i' -> can't rob 'i-1', take dp[i-2]
    - Skip current house 'i' -> take max of 'i-1'
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if not nums:
        return 0
        
    prev2, prev1 = 0, 0
    
    for num in nums:
        current = max(prev1, prev2 + num)
        prev2, prev1 = prev1, current
        
    return prev1

# Example Usage
if __name__ == "__main__":
    nums = [1, 2, 3, 1]
    print(f"Max items robbed: {rob(nums)}")
