class Solution:
    def isValid(self, s: str) -> bool:
        """
        Problem: Valid Parentheses
        Pattern: Stack
        """
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        
        for char in s:
            if char in mapping:
                top_element = stack.pop() if stack else '#'
                if mapping[char] != top_element:
                    return False
            else:
                stack.append(char)
        return not stack

    def simplifyPath(self, path: str) -> str:
        """
        Problem: Simplify Path
        Pattern: Stack
        """
        stack = []
        cur = ""
        
        for c in path + "/":
            if c == "/":
                if cur == "..":
                    if stack: stack.pop()
                elif cur != "" and cur != ".":
                    stack.append(cur)
                cur = ""
            else:
                cur += c
        return "/" + "/".join(stack)
