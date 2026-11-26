class Solution:
    def decodeString(self, s: str) -> str:
        """
        Problem: Decode String
        Difficulty: Medium
        Time Complexity: O(maxK * n)
        Space Complexity: O(n)
        """
        stack = []
        
        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])
            else:
                substr = ""
                while stack[-1] != "[":
                    substr = stack.pop() + substr
                stack.pop() # pop [
                
                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k
                stack.append(int(k) * substr)
                
        return "".join(stack)
