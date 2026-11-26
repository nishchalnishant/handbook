def num_trees(n):
    """
    Problem: Number of structurally unique BSTs with n nodes.
    Also: Number of valid parentheses combinations.
    
    Approach: Catalan Number DP
    - G(n) = sum(G(i-1) * G(n-i)) for i in 1..n
    - Root is i, left has i-1 nodes, right has n-i nodes.
    
    Time Complexity: O(N^2)
    Space Complexity: O(N)
    """
    dp = [0] * (n + 1)
    dp[0] = 1
    dp[1] = 1
    
    for i in range(2, n + 1):
        for j in range(1, i + 1):
            dp[i] += dp[j-1] * dp[i-j]
            
    return dp[n]

# Example Usage
if __name__ == "__main__":
    n = 3
    print(f"Unique BSTs with {n} nodes: {num_trees(n)}")
