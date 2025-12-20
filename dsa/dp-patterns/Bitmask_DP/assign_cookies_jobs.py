def distribute_cookies(cookies, k):
    """
    Problem: Leetcode 2305. Distribute cookies (integers) to k children to minimize the maximum unfairness (max cookies a child gets).
    Equivalent to: Assign jobs to k workers to minimize max load.
    
    Approach: Bitmask DP or Backtracking
    - Constraints N <= 8 usually allow 0(K^N) backtracking.
    - If N <= 16, Bitmask DP?
    - dp[mask] = min unfairness for distributing subset 'mask'.
    - But we need to define 'k' partitions. 
    - dp[i][mask] = min unfairness using i children for subset mask.
    - dp[i][mask] = min(max(dp[i-1][submask], sum(mask ^ submask))) for submasks.
    
    Time Complexity: O(3^N)
    Space Complexity: O(2^N * K)
    """
    n = len(cookies)
    sums = [0] * (1 << n)
    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if (mask >> i) & 1:
                s += cookies[i]
        sums[mask] = s
        
    dp = [[float('inf')] * (1 << n) for _ in range(k + 1)]
    dp[0][0] = 0
    
    for i in range(1, k + 1):
        for mask in range(1 << n):
            # Iterate submasks of mask
            sub = mask
            while sub > 0:
                # dp[i][mask] = min(..., max(dp[i-1][mask^sub], sums[sub]))
                prev = mask ^ sub
                val = max(dp[i-1][prev], sums[sub])
                dp[i][mask] = min(dp[i][mask], val)
                
                sub = (sub - 1) & mask
                
    return dp[k][(1 << n) - 1]

# Example Usage
if __name__ == "__main__":
    cookies = [8, 15, 10, 20, 8]
    k = 2
    print(f"Min unfairness: {distribute_cookies(cookies, k)}")
