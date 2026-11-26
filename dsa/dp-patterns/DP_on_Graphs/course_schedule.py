def can_finish(numCourses, prerequisites):
    """
    Problem: Can you finish all courses given prereqs? (Detect Cycle in DAG).
    Conceptually related to path problems/DP state dependencies.
    
    Approach: DFS with states (Graph Coloring)
    - 0: Unvisited
    - 1: Visiting (Current Path)
    - 2: Visited (Completed)
    - If we meet node with state 1, cycle exists -> False.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    """
    adj = [[] for _ in range(numCourses)]
    for dest, src in prerequisites:
        adj[src].append(dest)
        
    visited = [0] * numCourses
    
    def dfs(u):
        if visited[u] == 1: return False # Cycle
        if visited[u] == 2: return True
        
        visited[u] = 1
        for v in adj[u]:
            if not dfs(v):
                return False
        visited[u] = 2
        return True
        
    for i in range(numCourses):
        if not dfs(i):
            return False
            
    return True

# Example Usage
if __name__ == "__main__":
    n = 2
    prereqs = [[1,0], [0,1]] # Cycle
    print(f"Can finish courses: {can_finish(n, prereqs)}")
