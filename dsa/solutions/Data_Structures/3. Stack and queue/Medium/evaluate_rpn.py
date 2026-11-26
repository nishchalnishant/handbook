from typing import List

class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        """
        Problem: Evaluate Reverse Polish Notation
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(n)
        """
        stack = []
        for c in tokens:
            if c == "+":
                stack.append(stack.pop() + stack.pop())
            elif c == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a)
            elif c == "*":
                stack.append(stack.pop() * stack.pop())
            elif c == "/":
                a, b = stack.pop(), stack.pop()
                # Ensure integer division truncates towards zero
                stack.append(int(b / a))
            else:
                stack.append(int(c))
        return stack[0]
