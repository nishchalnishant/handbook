def solve_tiling_2xn(n):
    """
    Problem: Count ways to tile a 2xN board using 2x1 dominoes.
    
    Approach: Fibonacci Pattern
    - Place vertical: reduces to (n-1) problem.
    - Place horizontal: must include another horizontal below it, reduces to (n-2) problem.
    - dp[n] = dp[n-1] + dp[n-2]
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if n <= 2:
        return n
        
    prev2, prev1 = 1, 2
    
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev1 + prev2
        
    return prev1

# Example Usage
if __name__ == "__main__":
    n = 4
    print(f"Ways to tile 2x{n} board: {solve_tiling_2xn(n)}")
