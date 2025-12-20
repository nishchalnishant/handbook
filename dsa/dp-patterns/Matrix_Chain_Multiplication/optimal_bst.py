def optimal_bst(keys, freq):
    """
    Problem: Given keys and frequencies, build BST to minimize cost (depth * freq).
    
    Approach: MCM Pattern
    - dp[i][j] = min cost for keys[i...j].
    - Cost includes sum of frequencies for i...j (as they all go 1 level deeper) + cost of left + cost of right.
    
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    """
    n = len(keys)
    # Sum of freq from i to j
    prefix_sum = [0] * (n + 1)
    for i in range(n):
        prefix_sum[i+1] = prefix_sum[i] + freq[i]
        
    def get_sum(i, j):
        return prefix_sum[j+1] - prefix_sum[i]
        
    dp = [[0] * n for _ in range(n)]
    
    # Initialization for length 1
    for i in range(n):
        dp[i][i] = freq[i]
        
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            s = get_sum(i, j)
            
            for k in range(i, j + 1):
                left = dp[i][k-1] if k > i else 0
                right = dp[k+1][j] if k < j else 0
                dp[i][j] = min(dp[i][j], left + right + s)
                
    return dp[0][n-1]

# Example Usage
if __name__ == "__main__":
    keys = [10, 12, 20]
    freq = [34, 8, 50]
    print(f"Optimal BST Cost: {optimal_bst(keys, freq)}")
