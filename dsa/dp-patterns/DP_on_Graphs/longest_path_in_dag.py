def longest_path_dag(n, edges):
    """
    Problem: Find the length of the longest path in a Directed Acyclic Graph.
    
    Approach: DP on Graphs (Memoized DFS)
    - dp[u] = longest path starting from u.
    - dp[u] = 1 + max(dp[v]) for all neighbors v.
    - If no neighbors, dp[u] = 0.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        
    memo = {}
    
    def dfs(u):
        if u in memo: return memo[u]
        
        max_dist = 0
        for v in adj[u]:
            max_dist = max(max_dist, 1 + dfs(v))
            
        memo[u] = max_dist
        return max_dist
        
    # Run from all nodes as graph might not be connected or we don't know start
    ans = 0
    for i in range(n):
        ans = max(ans, dfs(i))
        
    return ans

# Example Usage
if __name__ == "__main__":
    n = 5
    edges = [[0,1], [1,2], [2,3], [0,4]]
    # Path 0->1->2->3 length 3
    print(f"Longest path in DAG: {longest_path_dag(n, edges)}")
