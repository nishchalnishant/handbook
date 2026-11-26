def tribonacci(n):
    """
    Problem: T(n) = T(n-1) + T(n-2) + T(n-3).
    
    Approach: DP with 3 variables.
    
    Time Complexity: O(N)
    Space Complexity: O(1)
    """
    if n == 0: return 0
    if n <= 2: return 1
    
    t0, t1, t2 = 0, 1, 1
    for _ in range(3, n + 1):
        tn = t0 + t1 + t2
        t0, t1, t2 = t1, t2, tn
        
    return t2

# Example Usage
if __name__ == "__main__":
    n = 25
    print(f"Tribonacci({n}): {tribonacci(n)}")
