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
    # 1. Valid Parentheses (LC 20) — T1
    # Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if:
    # Example: s = "()" → true
    # Constraints: 1 <= s.length <= 10^4, s consists of parentheses only '()[]{}'
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def isValid(self, s: str) -> bool:
        """Valid Parentheses (LC 20): Use a stack to track unmatched open brackets."""
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

    # -----------------------------------------------------------------------
    # 2. Trapping Rain Water (LC 42) — T1
    # Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
    # Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] → 6
    # Constraints: n == height.length, 1 <= n <= 2 * 10^4, 0 <= height[i] <= 10^5
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def trap_stack(self, height: List[int]) -> int:
        # Stack storing indices of boundaries
        stack = []
        res = 0
        for i, h in enumerate(height):
            # While stack is not empty and current height is greater than stack top
            while stack and h > height[stack[-1]]:
                top = stack.pop()
                # Break if no left boundary exists
                if not stack: break
                # Calculate distance between current index and new top of the stack
                distance = i - stack[-1] - 1
                # Bounded height is the min of boundaries minus the floor height
                bounded_height = min(h, height[stack[-1]]) - height[top]
                res += distance * bounded_height
            # Add current index to the stack
            stack.append(i)
        return res

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

class MyQueue:
    # -----------------------------------------------------------------------
    # 2. Implement Queue using Stacks (LC 232) — T2
    # Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (push, peek, pop, and empty). Implement the MyQueue class: Notes: size, and is empty operations are valid. using a list or deque (double-ended queue) as long as you use only a stack's standard operations.
    # Constraints: 1 <= x <= 9, At most 100 calls will be made to push, pop, peek, and empty, All the calls to pop and peek are valid, Follow-up: Can you implement the queue such that each operation is amortized O(1) time complexity?, In other words, performing n operations will take overall O(n) time even if one of those operations, may take longer
    # Time: O(1) amortized per operation, Space: O(n)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.s1 = []
        self.s2 = []

    def push(self, x: int) -> None:
        # Always append incoming elements to s1
        self.s1.append(x)

    def pop(self) -> int:
        self.peek()
        return self.s2.pop()

    def peek(self) -> int:
        # If output stack s2 is empty, transfer all elements from s1 to s2
        if not self.s2:
            while self.s1:
                self.s2.append(self.s1.pop())
        # Return top of output stack s2
        return self.s2[-1]

    def empty(self) -> bool:
        return max(len(self.s1), len(self.s2)) == 0

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
    # 7. Maximal Rectangle (LC 85) — T2
    # Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.
    # Example: matrix = → 6
    # Constraints: rows == matrix.length, cols == matrix[i].length, 1 <= rows, cols <= 200, matrix[i][j] is '0' or '1'
    # Time: O(rows * cols), Space: O(cols)
    # -----------------------------------------------------------------------
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        if not matrix: return 0
        max_area = 0
        dp = [0] * len(matrix[0])

        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == "1": dp[c] += 1
                else: dp[c] = 0

            # Re-use largest rectangle in histogram logic
            stack = []
            for i, h in enumerate(dp):
                start = i
                while stack and stack[-1][1] > h:
                    index, height = stack.pop()
                    max_area = max(max_area, height * (i - index))
                    start = index
                stack.append((start, h))
            for i, h in stack:
                max_area = max(max_area, h * (len(dp) - i))
        return max_area

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
    # 10. Basic Calculator (LC 224) — T2
    # Given a string s representing a valid expression, implement a basic calculator to evaluate it, and return the result of the evaluation. Note: You are not allowed to use any built-in function which evaluates strings as mathematical expressions, such as eval().
    # Example: s = "1 + 1" → 2
    # Constraints: 1 <= s.length <= 3 * 10^5, s consists of digits, '+', '-', '(', ')', and ' ', s represents a valid expression, '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid), '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid), There will be no two consecutive operators in the input, Every number and running calculation will fit in a signed 32-bit integer
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def calculate(self, s: str) -> int:
        # res: current level result, num: active parsing number, sign: +1 or -1
        res, num, sign, stack = 0, 0, 1, []
        for c in s:
            # Accumulate multi-digit numbers
            if c.isdigit():
                num = 10 * num + int(c)
            # Add previous number to result and update sign
            elif c in "+-":
                res += sign * num
                num = 0
                sign = 1 if c == "+" else -1
            # Push current result and sign onto stack, reset for sub-expression
            elif c == "(":
                stack.append(res)
                stack.append(sign)
                sign = 1
                res = 0
            # Resolve sub-expression: add last number and apply popped sign/result
            elif c == ")":
                res += sign * num
                num = 0
                res *= stack.pop()
                res += stack.pop()
        # Add the final parsed number to the result
        return res + sign * num

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
    # 1. Longest Valid Parentheses (LC 32)
    # Given a string containing just '(' and ')', return the length of the longest valid (well-formed) parentheses substring.
    # Constraints: ─────────────────────────────────────────────────────────────────────────
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    """Online Stock Span (LC 901). O(1) amortized per next()."""
    def longestValidParentheses(self, s: str) -> int:
        """Longest Valid Parentheses (LC 32): Use a stack initialized with sentinel -1."""
        # Stack initialized with index base sentinel -1
        stack = [-1]
        max_len = 0
        for i, c in enumerate(s):
            # Push index of opening parenthesis
            if c == '(':
                stack.append(i)
            # Encountered closing parenthesis
            else:
                # Pop matching index / sentinel
                stack.pop()
                # If stack is empty, push current index as new base sentinel
                if not stack:
                    stack.append(i)
                # Compute valid window length
                else:
                    max_len = max(max_len, i - stack[-1])
        return max_len

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 2. Maximum Score of a Good Subarray (LC 1793)
    # Given an integer array nums (0-indexed) and an integer k, return the maximum score of a good subarray. A subarray [i..j] is good if i <= k <= j. The score of [i..j] is min(nums[i..j]) * (j - i + 1).
    # Constraints: ─────────────────────────────────────────────────────────────────────────
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def maximumScore(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Left boundary index where nums[left] < nums[i]
        left = [-1] * n
        # Right boundary index where nums[right] < nums[i]
        right = [n] * n
        stack: List[int] = []

        # Find boundaries using a monotonic stack
        for i in range(n):
            # Resolve right boundaries for popped elements
            while stack and nums[stack[-1]] >= nums[i]:
                right[stack.pop()] = i
            # Node on stack is the left boundary for current element
            if stack:
                left[i] = stack[-1]
            stack.append(i)

        ans = 0
        # Calculate scores of all subarrays that contain index k
        for i in range(n):
            # Subarray spans left[i]+1 to right[i]-1 and must include index k
            if left[i] < k < right[i]:
                # Score is minimum height * width
                ans = max(ans, nums[i] * (right[i] - left[i] - 1))
        return ans

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 3. Number of Visible People in a Queue (LC 1944)
    # There are n people standing in a queue, each with a distinct height heights[i]. Person i can see person j (j > i) iff for all k with i < k < j, heights[k] < min(heights[i], heights[j]). Return an array answer where answer[i] is the number of people person i can see.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def canSeePersonsCount(self, heights: List[int]) -> List[int]:
        n = len(heights)
        # Result array for each person's visible count
        ans = [0] * n
        # Monotonically decreasing heights stack from right to left
        stack: List[int] = []
        for i in range(n - 1, -1, -1):
            count = 0
            # Pop shorter people who are directly visible and then blocked
            while stack and heights[i] > stack[-1]:
                stack.pop()
                count += 1
            # If stack is not empty, the next taller person is also visible
            if stack:
                count += 1
            ans[i] = count
            # Push current person's height
            stack.append(heights[i])
        return ans

    # ─────────────────────────────────────────────────────────────────────────
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

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 8. Tag Validator (LC 591)
    # Given a code snippet, validate it according to: CDATA (<![CDATA[...]]>), or text.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def isValidTag(self, code: str) -> bool:
        stack: List[str] = []
        i = 0
        n = len(code)
        # Must start with an open tag
        if not code.startswith('<') or code.startswith('</'):
            return False
        while i < n:
            if code[i] == '<':
                if code[i:i+9] == '<![CDATA[':
                    end = code.find(']]>', i + 9)
                    if end == -1:
                        return False
                    i = end + 3
                elif code[i+1:i+2] == '/':
                    end = code.find('>', i + 2)
                    if end == -1:
                        return False
                    tag = code[i+2:end]
                    if not stack or stack[-1] != tag:
                        return False
                    stack.pop()
                    i = end + 1
                    # After outermost tag closed, nothing should remain valid
                    if not stack and i < n:
                        return False
                else:
                    end = code.find('>', i + 1)
                    if end == -1:
                        return False
                    tag = code[i+1:end]
                    if not (1 <= len(tag) <= 9 and tag.isupper() and tag.isalpha()):
                        return False
                    stack.append(tag)
                    i = end + 1
            else:
                if not stack:
                    return False
                i += 1
        return not stack

    # ─────────────────────────────────────────────────────────────────────────
    # -----------------------------------------------------------------------
    # 9. Make the String Great (LC 1544)
    # Given a string s of lower and upper case letters. A string is "great" if there are no two adjacent characters s[i] and s[i+1] where they are the same letter but different cases. Remove such pairs repeatedly. Return the resulting great string (answer is unique).
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def makeGood(self, s: str) -> str:
        """Make the String Great (LC 1544): Use a stack and process each character."""
        # Stack to build the good string
        stack: List[str] = []
        for c in s:
            # Check if stack top and current char are same letter but opposite case
            if stack and abs(ord(stack[-1]) - ord(c)) == 32:
                # Remove canceling characters
                stack.pop()
            else:
                # Push valid character
                stack.append(c)
        # Return resulting good string
        return "".join(stack)


if __name__ == "__main__":
    sol = StackSolutions()
    sol2 = StackSolutionsT2()

    # isValid
    assert sol.isValid("()[]{}") == True
    assert sol.isValid("(]") == False
    assert sol.isValid("{[]}") == True

    # trap_stack
    assert sol.trap_stack([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert sol.trap_stack([4, 2, 0, 3, 2, 5]) == 9

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

    # MyQueue
    q = MyQueue()
    q.push(1); q.push(2)
    assert q.peek() == 1
    assert q.pop() == 1
    assert q.empty() == False

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

    # maximalRectangle
    assert sol2.maximalRectangle([["1","0","1","0","0"],["1","0","1","1","1"],
                                   ["1","1","1","1","1"],["1","0","0","1","0"]]) == 6

    # asteroidCollision
    assert sol2.asteroidCollision([5, 10, -5]) == [5, 10]
    assert sol2.asteroidCollision([8, -8]) == []
    assert sol2.asteroidCollision([10, 2, -5]) == [10]

    # removeKdigits
    assert sol2.removeKdigits("1432219", 3) == "1219"
    assert sol2.removeKdigits("10200", 1) == "200"
    assert sol2.removeKdigits("10", 2) == "0"

    # calculate (Basic Calculator I)
    assert sol2.calculate("1 + 1") == 2
    assert sol2.calculate(" 2-1 + 2 ") == 3
    assert sol2.calculate("(1+(4+5+2)-3)+(6+8)") == 23

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

    # longestValidParentheses (LC 32)
    assert l4.longestValidParentheses("(()") == 2
    assert l4.longestValidParentheses(")()())") == 4
    assert l4.longestValidParentheses("") == 0
    assert l4.longestValidParentheses("()") == 2
    assert l4.longestValidParentheses("()()") == 4

    # maximumScore (LC 2104)
    assert l4.maximumScore([1, 4, 3, 7, 4, 5], 3) == 15
    assert l4.maximumScore([5, 5, 4, 5, 4, 1, 1, 1], 0) == 20

    # canSeePersonsCount (LC 1944)
    assert l4.canSeePersonsCount([10, 6, 8, 5, 11, 9]) == [3, 1, 2, 1, 1, 0]
    assert l4.canSeePersonsCount([5, 1, 2, 3, 10]) == [4, 1, 1, 1, 0]

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

    # isValidTag (LC 591)
    assert l4.isValidTag("<DIV>This is the first line <![CDATA[<div>]]></DIV>") == True
    assert l4.isValidTag("<DIV>>>  ![cdata[]] <![CDATA[<div>]]>]]>>]</DIV>") == True
    assert l4.isValidTag("<A>  <B> </A>   </B>") == False
    assert l4.isValidTag("<DIV>  div tag is not closed  <DIV>") == False
    assert l4.isValidTag("<DIV>  unmatched <  </DIV>") == False

    # makeGood (LC 1544)
    assert l4.makeGood("leEeetcode") == "leetcode"
    assert l4.makeGood("abBAcC") == ""
    assert l4.makeGood("s") == "s"

    print("All stack tests passed.")
