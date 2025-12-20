class Solution:
    def calculate(self, s: str) -> int:
        """
        Problem: Basic Calculator
        Difficulty: Hard
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        res = 0
        num = 0
        sign = 1
        stack = []
        
        for c in s:
            if c.isdigit():
                num = num * 10 + int(c)
            elif c == '+':
                res += sign * num
                num = 0
                sign = 1
            elif c == '-':
                res += sign * num
                num = 0
                sign = -1
            elif c == '(':
                stack.append(res)
                stack.append(sign)
                sign = 1
                res = 0
            elif c == ')':
                res += sign * num
                res *= stack.pop()
                res += stack.pop()
                num = 0
        return res + sign * num
