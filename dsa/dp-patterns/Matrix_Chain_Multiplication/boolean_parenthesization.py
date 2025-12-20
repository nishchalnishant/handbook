def count_eval(s):
    """
    Problem: Count ways to parenthesize a boolean expression (T, F, &, |, ^) to evaluate to True.
    
    Approach: MCM Pattern
    - dp_true[i][j] = ways s[i...j] evaluates to True
    - dp_false[i][j] = ways s[i...j] evaluates to False
    - Split at operator k. Calculate left_true, left_false, right_true, right_false.
    - Combine based on operator (e.g., if '&': T = LT*RT, F = LT*RF + LF*RT + LF*RF)
    
    Time Complexity: O(N^3)
    Space Complexity: O(N^2)
    """
    # Simply using recursion with memoization as it's cleaner to implement for complex parsing
    memo = {}

    def solve(i, j, is_true):
        if i > j: return 0
        if i == j:
            if is_true: return 1 if s[i] == 'T' else 0
            else: return 1 if s[i] == 'F' else 0
        state = (i, j, is_true)
        if state in memo: return memo[state]
        
        ans = 0
        for k in range(i + 1, j, 2): # Iterate operators
            l_t = solve(i, k - 1, True)
            l_f = solve(i, k - 1, False)
            r_t = solve(k + 1, j, True)
            r_f = solve(k + 1, j, False)
            
            if s[k] == '&':
                if is_true: ans += l_t * r_t
                else: ans += l_t * r_f + l_f * r_t + l_f * r_f
            elif s[k] == '|':
                if is_true: ans += l_t * r_t + l_t * r_f + l_f * r_t
                else: ans += l_f * r_f
            elif s[k] == '^':
                if is_true: ans += l_t * r_f + l_f * r_t
                else: ans += l_t * r_t + l_f * r_f
        
        memo[state] = ans
        return ans

    return solve(0, len(s) - 1, True)

# Example Usage
if __name__ == "__main__":
    # T|T&F^T
    s = "T|T&F^T"
    print(f"Ways to evaluate to True: {count_eval(s)}")
