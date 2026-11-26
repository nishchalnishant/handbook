def hamiltonian_path(n, edges):
    """
    Problem: Check if a Hamiltonian Path exists (visits every vertex exactly once).
    
    Approach: Bitmask DP
    - dp[mask][i] = True if path visiting nodes in 'mask' ending at `i` exists.
    - Transition: dp[mask][i] is True if exists j such that dp[mask^(1<<i)][j] is True and (j, i) in edges.
    
    Time Complexity: O(2^N * N^2)
    Space Complexity: O(2^N * N)
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
        
    dp = [[False] * n for _ in range(1 << n)]
    
    for i in range(n):
        dp[1 << i][i] = True
        
    for mask in range(1, 1 << n):
        for i in range(n):
            if (mask >> i) & 1:
                prev_mask = mask ^ (1 << i)
                if prev_mask == 0: continue
                
                for j in adj[i]:
                    if (prev_mask >> j) & 1:
                        if dp[prev_mask][j]:
                            dp[mask][i] = True
                            break
                            
    last_mask = (1 << n) - 1
    for i in range(n):
        if dp[last_mask][i]:
            return True
            
    return False

# Example Usage
if __name__ == "__main__":
    n = 4
    edges = [(0,1), (1,2), (2,3)]
    print(f"Hamiltonian Path Exists: {hamiltonian_path(n, edges)}")
