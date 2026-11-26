def cherry_pickup(grid):
    """
    Problem: Leetcode 741. Collect cherries from (0,0) to (N-1,N-1) and back to (0,0).
    Move Right or Down only on way there, Left or Up on way back.
    Equiv: Two people moving from (0,0) to (N-1,N-1) simultaneously.
    
    Approach: Grid DP (3D State)
    - dp[r1][c1][c2] = max cherries for two people at (r1, c1) and (r2, c2).
    - Note: r1 + c1 == r2 + c2 == steps. So r2 is determined by others.
    - r2 = r1 + c1 - c2.
    
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    """
    N = len(grid)
    memo = {}
    
    def solve(r1, c1, c2):
        r2 = r1 + c1 - c2
        if r1 == N or c1 == N or r2 == N or c2 == N or \
           grid[r1][c1] == -1 or grid[r2][c2] == -1:
            return float('-inf')
            
        if r1 == N - 1 and c1 == N - 1:
            return grid[r1][c1]
            
        state = (r1, c1, c2)
        if state in memo: return memo[state]
        
        # Current cell value
        res = grid[r1][c1]
        if c1 != c2: # Avoid double counting if both on same cell
            res += grid[r2][c2]
            
        # Transitions: RR, RD, DR, DD
        max_next = max(solve(r1, c1 + 1, c2 + 1),      # Right, Right
                       solve(r1, c1 + 1, c2),          # Right, Down
                       solve(r1 + 1, c1, c2 + 1),      # Down, Right
                       solve(r1 + 1, c1, c2))          # Down, Down
                       
        memo[state] = res + max_next
        return memo[state]
        
    ans = solve(0, 0, 0)
    return max(0, ans)

# Example Usage
if __name__ == "__main__":
    grid = [[0, 1, -1],
            [1, 0, -1],
            [1, 1,  1]]
    print(f"Max Cherries: {cherry_pickup(grid)}")
