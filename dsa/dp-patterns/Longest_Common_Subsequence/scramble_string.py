def is_scramble(s1, s2):
    """
    Problem: Leetcode 87. Check if s2 is a scrambled version of s1.
    Scrambling involves binary splitting and potentially swapping children.
    
    Approach: Interval DP / Partition
    - Recursion with Memoization.
    - Try all split points k. Check if (left1~left2 AND right1~right2) OR (left1~right2 AND right1~left2 [swap]).
    
    Time Complexity: O(N^4)
    Space Complexity: O(N^3)
    """
    memo = {}
    
    def solve(str1, str2):
        if (str1, str2) in memo: return memo[(str1, str2)]
        if str1 == str2: return True
        if sorted(str1) != sorted(str2): return False
        
        n = len(str1)
        for i in range(1, n):
            # No Swap
            if solve(str1[:i], str2[:i]) and solve(str1[i:], str2[i:]):
                memo[(str1, str2)] = True
                return True
            # Swap
            if solve(str1[:i], str2[n-i:]) and solve(str1[i:], str2[:n-i]):
                memo[(str1, str2)] = True
                return True
                
        memo[(str1, str2)] = False
        return False
        
    return solve(s1, s2)

# Example Usage
if __name__ == "__main__":
    s1, s2 = "great", "rgeat"
    print(f"Is scrambled: {is_scramble(s1, s2)}")
