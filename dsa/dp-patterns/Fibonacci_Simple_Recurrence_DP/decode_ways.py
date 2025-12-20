def num_decodings(s):
    """
    Problem: Count ways to decode a string of digits (A=1, ... Z=26).
    
    Approach: Fibonacci variation
    - dp[i] = ways to decode string s[:i]
    - If s[i-1] is valid ('1'-'9'): add dp[i-1]
    - If s[i-2:i] is valid ('10'-'26'): add dp[i-2]
    
    Time Complexity: O(N)
    Space Complexity: O(1) (Optimized from O(N))
    """
    if not s or s[0] == '0':
        return 0
        
    prev2, prev1 = 1, 1 # dp[-1], dp[0]
    
    for i in range(1, len(s)):
        current = 0
        one_digit = int(s[i])
        two_digits = int(s[i-1:i+1])
        
        if one_digit != 0:
            current += prev1
        
        if 10 <= two_digits <= 26:
            current += prev2
            
        prev2, prev1 = prev1, current
        
    return prev1

# Example Usage
if __name__ == "__main__":
    s = "226"
    print(f"Ways to decode {s}: {num_decodings(s)}")
