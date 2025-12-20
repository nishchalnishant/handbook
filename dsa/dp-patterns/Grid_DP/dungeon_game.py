def calculate_minimum_hp(dungeon):
    """
    Problem: Knight needs min initial HP to reach bottom-right. Rooms have daemons (-) or orbs (+). HP must never drop <= 0.
    
    Approach: Grid DP (Reverse)
    - Start from bottom-right (Princess).
    - dp[i][j] = min HP needed at (i, j) to reach target safe.
    - dp[i][j] = max(1, min(right_needed, down_needed) - dungeon[i][j])
    - If dungeon[i][j] is positive (orb), we need less HP coming in.
    - If dungeon[i][j] is negative (damage), we need more HP.
    
    Time Complexity: O(M*N)
    Space Complexity: O(N)
    """
    m, n = len(dungeon), len(dungeon[0])
    dp = [float('inf')] * (n + 1)
    dp[n-1] = 1 # Need at least 1 HP at princess if value was 0
    
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            need = min(dp[j], dp[j+1]) - dungeon[i][j]
            dp[j] = max(1, need)
            
    return dp[0]

# Example Usage
if __name__ == "__main__":
    dungeon = [[-2,-3,3],[-5,-10,1],[10,30,-5]]
    print(f"Min Initial HP: {calculate_minimum_hp(dungeon)}")
