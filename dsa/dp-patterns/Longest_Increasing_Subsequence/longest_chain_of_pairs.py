def find_longest_chain(pairs):
    """
    Problem: Longest chain of pairs (a, b) (c, d) such that b < c.
    
    Approach: LIS / Greedy Interval Scheduling
    - Sort pairs by second element (end time).
    - Greedy strategy usually works: pick pair with earliest end time that chain continues.
    - DP approach also valid (LIS type). Here showing Greedy as it's O(N log N) vs DP O(N^2) (though DP on sorted is also possible).
    
    Time Complexity: O(N log N)
    Space Complexity: O(1)
    """
    pairs.sort(key=lambda x: x[1])
    current, ans = float('-inf'), 0
    
    for head, tail in pairs:
        if current < head:
            current = tail
            ans += 1
            
    return ans

# Example Usage
if __name__ == "__main__":
    pairs = [[1,2], [2,3], [3,4]]
    print(f"Longest chain length: {find_longest_chain(pairs)}")
