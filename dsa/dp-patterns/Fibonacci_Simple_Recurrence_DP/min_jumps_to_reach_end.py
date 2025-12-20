def jump_game_ii(nums):
    """
    Problem: Find minimum number of jumps to reach the last index.
    
    Approach: Greedy / DP related to Fibonacci/Bfs
    - We don't strictly use Recurrence DP O(N^2) because Greedy O(N) is better.
    - However, DP approach is: dp[i] = min(dp[j] + 1) for all j < i where j can reach i.
    
    Here providing the Optimal Greedy approach which is often the target for this problem.
    """
    if len(nums) <= 1:
        return 0
        
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest
            
    return jumps

# Example Usage
if __name__ == "__main__":
    nums = [2, 3, 1, 1, 4]
    print(f"Min jumps to reach end: {jump_game_ii(nums)}")
