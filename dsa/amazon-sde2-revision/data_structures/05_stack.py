"""
Stack patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Popping from an empty stack.\n- Using a stack when a simple counter would suffice (e.g., Valid Parentheses with only one type of bracket).\n- Not clearing or processing remaining elements in the stack after the main loop.

Common Variants:
- Valid Parentheses\n- Min Stack (store tuples of (val, current_min))\n- Expression Evaluation (Reverse Polish Notation)\n- Monotonic Stack (Next Greater Element)

General Tips & Best Practices:
- In Python, a simple list `[]` acts as an O(1) stack with `.append()` and `.pop()`.\n- Stacks are great for 'matching' problems or reversing order.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List

class StackSolutions:
    # -----------------------------------------------------------------------
    # 3. Daily Temperatures — T1
    # Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the i^th day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.
    # Example: temperatures = [73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]
    # Constraints: 1 <= temperatures.length <= 10^5, 30 <= temperatures[i] <= 100
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """Daily Temperatures: Use a decreasing monotonic stack of indices."""
        res = [0] * len(temperatures)
        stack = []  # stores indices
        for i, t in enumerate(temperatures):
            while stack and t > temperatures[stack[-1]]:
                stack_idx = stack.pop()
                res[stack_idx] = i - stack_idx
            stack.append(i)
        return res

    # -----------------------------------------------------------------------
    # 4. Largest Rectangle in Histogram — T1
    # Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
    # Example: heights = [2,1,5,6,2,3] → 10
    # Constraints: 1 <= heights.length <= 10^5, 0 <= heights[i] <= 10^4
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def largestRectangleArea(self, heights: List[int]) -> int:
        max_area = 0
        stack = [] # pair: (index, height)

        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                index, height = stack.pop()
                max_area = max(max_area, height * (i - index))
                start = index
            stack.append((start, h))

        for i, h in stack:
            max_area = max(max_area, h * (len(heights) - i))
        return max_area

class MinStack:
    # -----------------------------------------------------------------------
    # 1. Min Stack (LC 155) — T2
    # Design a stack that supports push, pop, top, and retrieving the minimum element in constant time. Implement the MinStack class: You must implement a solution with O(1) time complexity for each function.
    # Constraints: 2^31 <= val <= 2^31 - 1, Methods pop, top and getMin operations will always be called on non-empty stacks, At most 3 * 10^4 calls will be made to push, pop, top, and getMin
    # Time: O(1) per operation, Space: O(n)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        # Push value to the main stack
        self.stack.append(val)
        # Find the new minimum value at this stack level
        val = min(val, self.min_stack[-1] if self.min_stack else val)
        # Push new minimum value to min_stack
        self.min_stack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

class StackSolutionsT2:
    # -----------------------------------------------------------------------
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # Map values to their index in nums1
        nums1Idx = {n: i for i, n in enumerate(nums1)}
        res = [-1] * len(nums1)
        stack = []

        for i in range(len(nums2)):
            cur = nums2[i]
            # Pop elements from stack that are smaller than the current element
            while stack and cur > stack[-1]:
                val = stack.pop()
                if val in nums1Idx:
                    res[nums1Idx[val]] = cur
            # Push current element to the stack
            stack.append(cur)
        return res

    # -----------------------------------------------------------------------
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [-1] * n
        stack = []

        # Iterate twice over array to simulate circularity
        for i in range(2 * n):
            # Pop indices whose next greater element is the current element
            while stack and nums[stack[-1]] < nums[i % n]:
                res[stack.pop()] = nums[i % n]
            # Only append indices from the first pass
            if i < n:
                stack.append(i)
        return res

    # -----------------------------------------------------------------------
    # 5. Evaluate RPN (LC 150) — T2
    # Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, *, and /.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def evalRPN(self, tokens: List[str]) -> int:
        """Evaluate RPN (LC 150): Use a stack to evaluate the RPN expression in a single pass."""
        # Stack to hold integer operands
        stack = []
        # Process each token sequentially
        for t in tokens:
            # Addition operator
            if t == "+": stack.append(stack.pop() + stack.pop())
            # Subtraction operator: order of popped operands matters
            elif t == "-":
                a, b = stack.pop(), stack.pop()
                stack.append(b - a)
            # Multiplication operator
            elif t == "*": stack.append(stack.pop() * stack.pop())
            # Division operator: truncate toward zero
            elif t == "/":
                a, b = stack.pop(), stack.pop()
                stack.append(int(b / a))
            # Integer operand
            else:
                stack.append(int(t))
        # Return the final RPN evaluation result
        return stack[0]

    # -----------------------------------------------------------------------
    # 6. Decode String (LC 394) — T2
    # Given an encoded string, return its decoded string. The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer. You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4]. The test cases are generated so that the length of the output will never exceed 10^5.
    # Example: s = "3[a]2[bc]" → "aaabcbc"
    # Constraints: 1 <= s.length <= 30, s consists of lowercase English letters, digits, and square brackets '[]', s is guaranteed to be a valid input, All the integers in s are in the range [1, 300]
    # Time: O(n * k), Space: O(n * k)
    # -----------------------------------------------------------------------
    def decodeString(self, s: str) -> str:
        stack = []
        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])
            else:
                substr = ""
                while stack[-1] != "[":
                    substr = stack.pop() + substr
                stack.pop() # pop "["

                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k
                stack.append(int(k) * substr)
        return "".join(stack)

    # -----------------------------------------------------------------------
    # 8. Asteroid Collision (LC 735) — T2
    # We are given an array asteroids of integers representing asteroids in a row. The indices of the asteroid in the array represent their relative position in space. For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed. Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.
    # Example: asteroids = [5,10,-5] → [5,10]
    # Constraints: 2 <= asteroids.length <= 10^4, 1000 <= asteroids[i] <= 1000, asteroids[i] != 0
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        stack = []
        for a in asteroids:
            # Collision only happens when moving left (a < 0) meets moving right (stack top > 0)
            while stack and a < 0 and stack[-1] > 0:
                diff = a + stack[-1]
                # If left-moving is larger, destroy the right-moving asteroid
                if diff < 0: stack.pop()
                # If right-moving is larger, destroy the left-moving asteroid
                elif diff > 0: a = 0
                # Both explode on equal sizes
                else:
                    a = 0
                    stack.pop()
            # If current asteroid survived, add it to stack
            if a: stack.append(a)
        return stack

    # -----------------------------------------------------------------------
    def removeKdigits(self, num: str, k: int) -> str:
        # Monotonically increasing stack of digits
        stack = []
        for c in num:
            # While we have removals left and the previous digit is larger than current
            while k > 0 and stack and stack[-1] > c:
                # Decrement removal count
                k -= 1
                # Remove the larger digit
                stack.pop()
            # Push current digit
            stack.append(c)

        # Truncate any remaining removals from the end
        stack = stack[:len(stack) - k]
        # Join digits and strip leading zeros
        res = "".join(stack).lstrip("0")
        # Return result or '0' if empty
        return res if res else "0"

    # -----------------------------------------------------------------------
    # 11. Basic Calculator II (LC 227) — T2
    # Given a string s which represents an expression, evaluate this expression and return its value. The integer division should truncate toward zero. You may assume that the given expression is always valid. All intermediate results will be in the range of [-2^31, 2^31 - 1]. Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
    # Example: s = "3+2*2" → 7
    # Constraints: 1 <= s.length <= 3 * 10^5, s consists of integers and operators ('+', '-', '*', '/') separated by some number of spaces, s represents a valid expression, All the integers in the expression are non-negative integers in the range [0, 2^31 - 1], The answer is guaranteed to fit in a 32-bit integer
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def calculateII(self, s: str) -> int:
        if not s: return 0
        stack, num, sign = [], 0, "+"
        for i in range(len(s)):
            # Form multi-digit numbers
            if s[i].isdigit():
                num = num * 10 + ord(s[i]) - ord("0")
            # If current character is an operator or it is the end of the string
            if (not s[i].isdigit() and not s[i].isspace()) or i == len(s) - 1:
                if sign == "-":
                    stack.append(-num)
                elif sign == "+":
                    stack.append(num)
                elif sign == "*":
                    stack.append(stack.pop() * num)
                else:
                    tmp = stack.pop()
                    # Integer division truncating toward zero
                    if tmp // num < 0 and tmp % num != 0:
                        stack.append(tmp // num + 1)
                    else:
                        stack.append(tmp // num)
                sign = s[i]
                num = 0
        return sum(stack)


# 12. Online Stock Span (LC 901) — monotonic stack
# Time: O(1) amortized per next(), Space: O(n)
class StockSpanner:
    """Online Stock Span (LC 901). O(1) amortized per next()."""
    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        """Online Stock Span (LC 901). O(1) amortized per next()."""
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]
        self.stack.append((price, span))
        return span


class StackSolutionsL4:
    # -----------------------------------------------------------------------
    # 4. Buildings With an Ocean View (LC 1762)
    # There are n buildings in a row. The ocean is to the right. A building has an ocean view if all buildings to its right are shorter. Return a list of indices (ascending) of buildings with an ocean view.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def findBuildings(self, heights: List[int]) -> List[int]:
        n = len(heights)
        # Holds indices of buildings with ocean view
        ans = []
        # Tallest building seen so far from the right
        max_right = 0
        # Iterate right-to-left
        for i in range(n - 1, -1, -1):
            # Building can see ocean if it is taller than all buildings to its right
            if heights[i] > max_right:
                ans.append(i)
                # Update maximum height seen so far
                max_right = heights[i]
        # Reverse list back to original left-to-right order
        return ans[::-1]

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 5. Maximum Score From Removing Substrings (LC 1717)
    # Given string s and integers x, y, you can remove "ab" to gain x points or remove "ba" to gain y points, any number of times. Return the maximum score.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def maximumGain(self, s: str, x: int, y: int) -> int:
        def remove(string: str, pair: str, pts: int) -> tuple:
            """Removes a value from the underlying data structure when present."""
            # Stack to process removals
            stack: List[str] = []
            score = 0
            for c in string:
                # Check if last character and current form the target pair
                if stack and stack[-1] == pair[0] and c == pair[1]:
                    # Remove matching pair
                    stack.pop()
                    # Add points
                    score += pts
                else:
                    # Push current character
                    stack.append(c)
            # Return remaining string and score
            return "".join(stack), score

        if x >= y:
            s, s1 = remove(s, "ab", x)
            s, s2 = remove(s, "ba", y)
        else:
            s, s1 = remove(s, "ba", y)
            s, s2 = remove(s, "ab", x)
        return s1 + s2

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 6. Score of Parentheses (LC 856)
    # Given a balanced parentheses string s, return its score. Rules: "()" has score 1; "AB" has score A+B; "(A)" has score 2*A.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def scoreOfParentheses(self, s: str) -> int:
        # Initialize stack with outermost frame score 0
        stack = [0]
        for c in s:
            # Start new frame score on '('
            if c == '(':
                stack.append(0)
            # Resolve frame score on ')'
            else:
                v = stack.pop()
                # Inner score is 2*v (nested) or 1 (base empty parentheses case)
                stack[-1] += max(2 * v, 1)
        # Return outermost frame score
        return stack[0]

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 7. Exclusive Time of Functions (LC 636)
    # On a single-threaded CPU, n functions (0-indexed) run. Given a list of logs "id:start/end:timestamp", return an array of the exclusive time for each function.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        # Result array to hold exclusive time for each function
        res = [0] * n
        # Stack to track function call execution states
        stack: List[int] = []
        # Previous timestamp marker
        prev = 0
        for log in logs:
            # Parse log fields
            parts = log.split(':')
            fid, typ, ts = int(parts[0]), parts[1], int(parts[2])
            # Process function start event
            if typ == 'start':
                # Accumulate time for currently running function on stack
                if stack:
                    res[stack[-1]] += ts - prev
                # Push new function
                stack.append(fid)
                prev = ts
            # Process function end event
            else:
                # Accumulate final run time and pop function from stack
                res[stack.pop()] += ts - prev + 1
                # Set prev to start of next interval
                prev = ts + 1
        return res


if __name__ == "__main__":
    sol = StackSolutions()
    sol2 = StackSolutionsT2()

    # dailyTemperatures
    assert sol.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert sol.dailyTemperatures([30, 40, 50, 60]) == [1, 1, 1, 0]

    # largestRectangleArea
    assert sol.largestRectangleArea([2, 1, 5, 6, 2, 3]) == 10
    assert sol.largestRectangleArea([2, 4]) == 4

    # MinStack
    ms = MinStack()
    ms.push(-2); ms.push(0); ms.push(-3)
    assert ms.getMin() == -3
    ms.pop()
    assert ms.top() == 0
    assert ms.getMin() == -2

    # nextGreaterElement
    assert sol2.nextGreaterElement([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
    assert sol2.nextGreaterElement([2, 4], [1, 2, 3, 4]) == [3, -1]

    # nextGreaterElements (circular)
    assert sol2.nextGreaterElements([1, 2, 1]) == [2, -1, 2]

    # evalRPN
    assert sol2.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert sol2.evalRPN(["4", "13", "5", "/", "+"]) == 6

    # decodeString
    assert sol2.decodeString("3[a]2[bc]") == "aaabcbc"
    assert sol2.decodeString("3[a2[c]]") == "accaccacc"

    # asteroidCollision
    assert sol2.asteroidCollision([5, 10, -5]) == [5, 10]
    assert sol2.asteroidCollision([8, -8]) == []
    assert sol2.asteroidCollision([10, 2, -5]) == [10]

    # removeKdigits
    assert sol2.removeKdigits("1432219", 3) == "1219"
    assert sol2.removeKdigits("10200", 1) == "200"
    assert sol2.removeKdigits("10", 2) == "0"

    # calculateII (Basic Calculator II)
    assert sol2.calculateII("3+2*2") == 7
    assert sol2.calculateII(" 3/2 ") == 1
    assert sol2.calculateII(" 3+5 / 2 ") == 5

    # StockSpanner
    sp = StockSpanner()
    assert sp.next(100) == 1
    assert sp.next(80) == 1
    assert sp.next(60) == 1
    assert sp.next(70) == 2
    assert sp.next(60) == 1
    assert sp.next(75) == 4
    assert sp.next(85) == 6

    # ── StackSolutionsL4 tests ────────────────────────────────────────────
    l4 = StackSolutionsL4()

    # findBuildings (LC 1762)
    assert l4.findBuildings([4, 2, 3, 1]) == [0, 2, 3]
    assert l4.findBuildings([4, 3, 2, 1]) == [0, 1, 2, 3]
    assert l4.findBuildings([1, 3, 2, 4]) == [3]

    # maximumGain (LC 1717)
    assert l4.maximumGain("cdbcbbaaabab", 4, 5) == 19
    assert l4.maximumGain("aabbaaxybbaabb", 5, 4) == 20

    # scoreOfParentheses (LC 856)
    assert l4.scoreOfParentheses("()") == 1
    assert l4.scoreOfParentheses("(())") == 2
    assert l4.scoreOfParentheses("()()") == 2
    assert l4.scoreOfParentheses("(()(()))") == 6

    # exclusiveTime (LC 636)
    assert l4.exclusiveTime(2, ["0:start:0","1:start:2","1:end:5","0:end:6"]) == [3, 4]
    assert l4.exclusiveTime(1, ["0:start:0","0:start:2","0:end:5","0:start:6","0:end:6","0:end:7"]) == [8]

    print("All stack tests passed.")
