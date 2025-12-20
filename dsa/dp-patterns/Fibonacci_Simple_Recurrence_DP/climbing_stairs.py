def climb_stairs(n):
    """
    Problem: Count ways to reach the top of 'n' stairs, taking 1 or 2 steps at a time.
    
    Approach: Fibonacci Pattern
    - dp[i] = dp[i-1] + dp[i-2]
    
    Time Complexity: O(N)
    Space Complexity: O(1) (Optimized from O(N))
    """
    if n <= 1:
        return 1
        
    prev2, prev1 = 1, 1 # Ways for step 0 and step 1
    
    for _ in range(2, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
        
    return prev1

# Example Usage
if __name__ == "__main__":
    n = 5
    print(f"Ways to climb {n} stairs: {climb_stairs(n)}")
