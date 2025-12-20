def paint_fence(n, k):
    """
    Problem: Ways to paint N fence posts with K colors such that no more than 2 adjacent posts have same color.
    
    Approach: Fibonacci variation
    - same[i]: Ways where i and i-1 have same color = diff[i-1] * 1
    - diff[i]: Ways where i and i-1 have different colors = (same[i-1] + diff[i-1]) * (k-1)
    - total[i] = same[i] + diff[i]
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if n == 0: return 0
    if n == 1: return k
    
    same = k # Post 2 same as 1
    diff = k * (k - 1) # Post 2 diff from 1
    
    for i in range(3, n + 1):
        prev_diff = diff
        prev_same = same
        
        same = prev_diff
        diff = (prev_same + prev_diff) * (k - 1)
        
    return same + diff

# Example Usage
if __name__ == "__main__":
    n = 3
    k = 2
    print(f"Ways to paint fence: {paint_fence(n, k)}")
