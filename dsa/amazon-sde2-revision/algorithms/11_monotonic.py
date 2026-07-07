"""
Monotonic Stack/Queue patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Popping condition: Confusing `>` with `>=` when duplicate elements exist.\n- Forgetting to process elements remaining in the stack after the main loop.\n- Storing values instead of indices in the stack (indices are usually needed for width/distance calculations).

Common Variants:
- Next Greater Element (I, II, III)\n- Largest Rectangle in Histogram\n- Sliding Window Maximum (Monotonic Queue)

General Tips & Best Practices:
- Use a monotonically increasing stack to find the 'next smaller' element.\n- Use a monotonically decreasing stack to find the 'next greater' element.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

import collections
from typing import List


class MonotonicSolutions:

    # -------------------------------------------------------------------------
    # 1. Daily Temperatures (LC 739) — T1
    # Given temps[i], return answer[i] = days until a warmer temperature.
    # If no future warmer day exists, answer[i] = 0.
    # Example: temps=[73,74,75,71,69,72,76,73] → [1,1,4,2,1,1,0,0]
    # Constraints: 1 <= n <= 1e5, 30 <= temps[i] <= 100
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        # Get the length of the temperatures array
        n = len(temperatures)
        # Initialize the answer array with zeros, representing no warmer day found
        answer = [0] * n
        # Initialize an empty stack to store indices, maintaining monotonic decreasing temperatures
        stack = []
        # Iterate through temperatures with index and value
        for i, t in enumerate(temperatures):
            # While stack is not empty and current temperature is greater than temperature at stack top index
            while stack and temperatures[stack[-1]] < t:
                # Pop the index from stack as we found a warmer temperature
                j = stack.pop()
                # Calculate the difference in days and store it in answer
                answer[j] = i - j
            # Push the current index onto the stack
            stack.append(i)
        return answer

    # -------------------------------------------------------------------------
    # 2. Next Greater Element I (LC 496) — T1
    # nums1 is a subset of nums2 (all unique). For each x in nums1 find the
    # first element in nums2 to the right of x that is greater than x.
    # Return -1 if none exists.
    # Example: nums1=[4,1,2], nums2=[1,3,4,2] → [-1,3,-1]
    # Constraints: 1 <= m <= 1000, 1 <= n <= 1e4, all unique
    # Time: O(m+n), Space: O(m+n)
    # -------------------------------------------------------------------------
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        # Map to store the next greater element for each value in nums2
        next_greater = {}
        # Monotonically decreasing stack of values
        stack = []
        # Iterate through values in nums2
        for val in nums2:
            # While stack is not empty and current value is greater than the stack top value
            while stack and stack[-1] < val:
                # Pop from stack and map its next greater value to the current val
                next_greater[stack.pop()] = val
            # Push the current value onto the stack
            stack.append(val)
        # For each element in nums1, query the map or return -1 if not present
        return [next_greater.get(x, -1) for x in nums1]

    # -------------------------------------------------------------------------
    # 3. Next Greater Element II (LC 503) — T1
    # Circular array — wrap around. Return next greater element for each pos.
    # Example: nums=[1,2,1] → [2,-1,2]
    # Constraints: 1 <= n <= 1e4
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        # Get the length of the array
        n = len(nums)
        # Initialize the result array with -1
        result = [-1] * n
        # Monotonically decreasing stack of indices
        stack = []
        # Loop through the array twice to simulate circular behavior
        for i in range(2 * n):
            # Compute the cyclic index
            idx = i % n
            # While stack has indices and the corresponding element is less than the current element
            while stack and nums[stack[-1]] < nums[idx]:
                # Pop the index and record its next greater element
                result[stack.pop()] = nums[idx]
            # Only push indices onto the stack in the first pass to avoid duplication
            if i < n:
                stack.append(idx)
        return result

    # -------------------------------------------------------------------------
    # 4. Next Greater Element III (LC 556) — T2
    # Given integer n, find the smallest integer greater than n that uses the
    # same digits. Return -1 if impossible or exceeds 32-bit signed int.
    # Example: n=12 → 21; n=21 → -1
    # Constraints: 1 <= n <= 2^31 - 1
    # Time: O(d log d) where d = number of digits, Space: O(d)
    # -------------------------------------------------------------------------
    def nextGreaterElementIII(self, n: int) -> int:
        # Convert integer to a list of digit characters
        digits = list(str(n))
        # Find the number of digits
        d = len(digits)
        # Step 1: find pivot — rightmost i where digits[i] < digits[i+1]
        i = d - 2
        # Decrement i until we find the pivot or reach the start
        while i >= 0 and digits[i] >= digits[i + 1]:
            i -= 1
        # If no such pivot exists, digits are in descending order, so no larger permutation exists
        if i < 0:
            return -1
        # Step 2: find smallest digit to right of pivot that is > pivot digit
        j = d - 1
        # Decrement j until we find a digit greater than digits[i]
        while digits[j] <= digits[i]:
            j -= 1
        # Swap the pivot digit with the identified digit
        digits[i], digits[j] = digits[j], digits[i]
        # Step 3: reverse suffix after pivot
        digits[i + 1:] = digits[i + 1:][::-1]
        result = int("".join(digits))
        return result if result <= 2**31 - 1 else -1

    # -------------------------------------------------------------------------
    # 5. Next Smaller Element — classic variant — T1
    # For each element find the index of the first smaller element to its right.
    # Return -1 if none. (Interview classic; not a dedicated LC problem.)
    # Example: nums=[4,5,2,10,8] → [2,2,-1,4,-1] (indices of smaller elems)
    #   4→index 2 (value 2), 5→index 2 (value 2), 2→none, 10→index 4 (value 8),
    #   8→none
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def nextSmallerElement(self, nums: List[int]) -> List[int]:
        """Next Smaller Element: Monotonic increasing stack (pop when we see something smaller)."""
        # Get the length of the array
        n = len(nums)
        # Initialize result array with -1
        result = [-1] * n
        # Monotonically increasing stack of indices
        stack = []
        # Iterate through the elements
        for i, val in enumerate(nums):
            # While stack is not empty and current value is less than the element at the top index
            while stack and nums[stack[-1]] > val:
                # Pop index and store the current index as its next smaller element
                result[stack.pop()] = i
            # Push the current index onto the stack
            stack.append(i)
        return result

    # -------------------------------------------------------------------------
    # 6. Largest Rectangle in Histogram (LC 84) — T2
    # Given bar heights, find the largest rectangle area.
    # Example: heights=[2,1,5,6,2,3] → 10
    # Constraints: 1 <= n <= 1e5, 0 <= heights[i] <= 1e4
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def largestRectangleArea(self, heights: List[int]) -> int:
        # Monotonic increasing stack initialized with a sentinel -1
        stack = [-1]
        # Track the maximum area found so far
        max_area = 0
        # Iterate over heights with a trailing sentinel 0 to flush the remaining bars
        for i, h in enumerate(heights + [0]):
            # While stack contains elements (other than sentinel) and current height is less than stack top height
            while stack[-1] != -1 and heights[stack[-1]] >= h:
                # Pop the bar index to calculate its rectangle area
                height = heights[stack.pop()]
                # The width extends from the popped index to the new top of stack
                width = i - stack[-1] - 1
                # Update max_area if the current rectangle is larger
                max_area = max(max_area, height * width)
            # Push current index onto the stack
            stack.append(i)
        return max_area

    # -------------------------------------------------------------------------
    # 7. Sum of Subarray Minimums (LC 907) — T2
    # Sum of min(subarray) for every subarray. Return result mod 1e9+7.
    # Example: arr=[3,1,2,4] → 17
    # Constraints: 1 <= n <= 3e4, 1 <= arr[i] <= 3e4
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def sumSubarrayMins(self, arr: List[int]) -> int:
        # Define modulo constant
        MOD = 10**9 + 7
        # Get length of array
        n = len(arr)
        # Distance to previous less-or-equal element
        left = [0] * n
        # Distance to next less element
        right = [0] * n
        # Initialize empty stack
        stack = []

        # left pass: previous less-or-equal
        for i in range(n):
            # Pop elements that are strictly greater to maintain monotonic increasing stack
            while stack and arr[stack[-1]] > arr[i]:
                stack.pop()
            # Calculate distance to previous less-or-equal element
            left[i] = i - stack[-1] if stack else i + 1
            # Push current index
            stack.append(i)

        # Reset stack for right pass
        stack = []
        # right pass: next less (strict to avoid double count)
        for i in range(n - 1, -1, -1):
            # Pop elements that are greater-or-equal to maintain monotonic increasing stack
            while stack and arr[stack[-1]] >= arr[i]:
                stack.pop()
            # Calculate distance to next less element
            right[i] = stack[-1] - i if stack else n - i
            # Push current index
            stack.append(i)

        # Calculate total sum of subarray minimum contributions and apply modulo
        return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD

    # -------------------------------------------------------------------------
    # 8. Sum of Subarray Ranges (LC 2104) — T2
    # Sum of (max - min) for every subarray.
    # Example: nums=[1,2,3] → 4
    # Constraints: 1 <= n <= 1000, -1e9 <= nums[i] <= 1e9
    # Time: O(n), Space: O(n)   [O(n^2) brute force also accepted for n<=1000]
    # -------------------------------------------------------------------------
    def subArrayRanges(self, nums: List[int]) -> int:
        def sum_contributions(arr: List[int], find_max: bool) -> int:
            # Get the length of the array
            n = len(arr)
            # Distance arrays to previous and next boundaries
            left = [0] * n
            right = [0] * n
            # Initialize empty stack
            stack = []
            # Define comparison logic depending on whether we want subarray maxes or mins
            if find_max:
                # For maxes, pop when stack top is less than current (for left pass)
                left_cmp = lambda a, b: a < b   # pop when stack top < current
                # and when stack top is less-or-equal to current (for right pass)
                right_cmp = lambda a, b: a <= b # pop when stack top <= current
            else:
                # For mins, pop when stack top is greater than current (for left pass)
                left_cmp = lambda a, b: a > b
                # and when stack top is greater-or-equal to current (for right pass)
                right_cmp = lambda a, b: a >= b
            # Left pass to calculate previous boundary distances
            for i in range(n):
                while stack and left_cmp(arr[stack[-1]], arr[i]):
                    stack.pop()
                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)
            # Reset stack for right pass
            stack = []
            # Right pass to calculate next boundary distances
            for i in range(n - 1, -1, -1):
                while stack and right_cmp(arr[stack[-1]], arr[i]):
                    stack.pop()
                right[i] = stack[-1] - i if stack else n - i
                stack.append(i)
            # Return sum of all contributions
            return sum(arr[i] * left[i] * right[i] for i in range(n))

        # Range sum is sum of subarray maximums minus sum of subarray minimums
        return sum_contributions(nums, True) - sum_contributions(nums, False)

    # -------------------------------------------------------------------------
    # 9. Online Stock Span (LC 901) — T1
    # Design a class that collects stock prices and returns the span for today:
    # number of consecutive days (ending today) where price <= today's price.
    # Example: prices=[100,80,60,70,60,75,85] → spans=[1,1,1,2,1,4,6]
    # Time: O(1) amortised per call, Space: O(n)
    # -------------------------------------------------------------------------
    # Implemented as a separate class below; wrapper method provided here.
    def stockSpanDemo(self) -> "StockSpanner":
        # Return a new instance of StockSpanner
        return StockSpanner()

    # -------------------------------------------------------------------------
    # 10. Maximum Width Ramp (LC 962) — T2
    # A ramp is a pair (i,j) with i<j and nums[i]<=nums[j]. Maximise j-i.
    # Example: nums=[6,0,8,2,1,5] → 4  (i=1,j=5)
    # Constraints: 2 <= n <= 5e4, 0 <= nums[i] <= 5e4
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def maxWidthRamp(self, nums: List[int]) -> int:
        # Get length of array
        n = len(nums)
        # build strictly decreasing stack (left candidates)
        stack = []
        for i in range(n):
            if not stack or nums[i] < nums[stack[-1]]:
                stack.append(i)
        # Track maximum width found
        max_width = 0
        # Scan right-to-left to find the largest width
        for j in range(n - 1, -1, -1):
            # While stack has indices and current element is greater than or equal to element at stack top index
            while stack and nums[j] >= nums[stack[-1]]:
                # Calculate width and update max_width
                max_width = max(max_width, j - stack.pop())
        return max_width

    # -------------------------------------------------------------------------
    # 11. Sliding Window Maximum (LC 239) — T2
    # Return the max of each window of size k as it slides over nums.
    # Example: nums=[1,3,-1,-3,5,3,6,7], k=3 → [3,3,5,5,6,7]
    # Constraints: 1 <= n <= 1e5, -1e4 <= nums[i] <= 1e4, 1 <= k <= n
    # Time: O(n), Space: O(k)
    # -------------------------------------------------------------------------
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # Deque to store indices, maintaining monotonic decreasing order of values
        dq = collections.deque()
        # List to store maximum values of each window
        result = []
        # Iterate over array elements
        for i, val in enumerate(nums):
            # Remove indices that have slid out of the current window boundary
            while dq and dq[0] < i - k + 1:
                dq.popleft()
            # Remove elements from back that are smaller than current value to maintain decreasing order
            while dq and nums[dq[-1]] < val:
                dq.pop()
            # Append current index to the deque
            dq.append(i)
            # Once we've processed at least k elements, record the maximum (at the front of deque)
            if i >= k - 1:
                result.append(nums[dq[0]])
        return result

    # -------------------------------------------------------------------------
    # 12. Constrained Subsequence Sum (LC 1425) — T3
    # Choose a non-empty subsequence of nums such that for any two consecutive
    # chosen indices i < j, j - i <= k. Maximise the sum.
    # Example: nums=[10,2,-10,5,20], k=2 → 37
    # Constraints: 1 <= n <= 1e5, -1e4 <= nums[i] <= 1e4, 1 <= k <= n
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        # Get length of nums
        n = len(nums)
        # DP array to store the maximum subsequence sum ending at each index
        dp = [0] * n
        # Deque to store indices of DP values, keeping them in monotonic decreasing order
        dq = collections.deque()
        # Iterate through the elements
        for i in range(n):
            # Remove indices that are further than k distance back from current index
            while dq and dq[0] < i - k:
                dq.popleft()
            # Get the best previous sum from the front of the deque (or 0 if empty/negative)
            best_prev = dp[dq[0]] if dq else 0
            # Calculate DP value: current number plus the best valid previous subsequence sum (if positive)
            dp[i] = nums[i] + max(0, best_prev)
            # Maintain decreasing order in the deque
            while dq and dp[dq[-1]] <= dp[i]:
                dq.pop()
            # Add current index to deque
            dq.append(i)
        # The answer is the maximum value in the DP array
        return max(dp)

    # -------------------------------------------------------------------------
    # 13. Jump Game VI (LC 1696) — T2
    # You start at index 0. Each turn from index i you can jump to any index
    # in [i+1, i+k]. Score = sum of nums at visited indices. Maximise score.
    # Example: nums=[1,-1,-2,4,-7,3], k=2 → 7
    # Constraints: 1 <= n <= 1e5, -1e4 <= nums[i] <= 1e4, 1 <= k <= n
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def maxResult(self, nums: List[int], k: int) -> int:
        # Get length of array
        n = len(nums)
        # DP array to store maximum score to reach each index
        dp = [0] * n
        # Base case: starting score at index 0 is nums[0]
        dp[0] = nums[0]
        # Deque storing indices of DP values, keeping them in monotonic decreasing order
        dq = collections.deque([0])
        # Iterate from index 1 to n - 1
        for i in range(1, n):
            # Remove indices that are out of the jump range [i - k, i - 1]
            while dq and dq[0] < i - k:
                dq.popleft()
            # DP value is current number plus the maximum score from the best index in window
            dp[i] = nums[i] + dp[dq[0]]
            # Maintain decreasing order in the deque
            while dq and dp[dq[-1]] <= dp[i]:
                dq.pop()
            # Add current index to deque
            dq.append(i)
        # Return the score to reach the last index
        return dp[-1]

    # -------------------------------------------------------------------------
    # 14. Shortest Subarray with Sum at Least K (LC 862) — T3
    # Find the length of the shortest subarray with sum >= k. Return -1 if none.
    # Example: nums=[2,-1,2], k=3 → 3
    # Constraints: 1 <= n <= 5e4, -1e5 <= nums[i] <= 1e5, 1 <= k <= 1e9
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        # Get length of array
        n = len(nums)
        # Initialize prefix sum array of size n + 1
        prefix = [0] * (n + 1)
        # Build the prefix sum array
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]
        # Deque to store prefix indices, maintaining monotonic increasing prefix values
        dq = collections.deque()
        # Track minimum length found, initialized to infinity
        result = float('inf')
        # Iterate through prefix sum indices
        for j in range(n + 1):
            # If current prefix sum minus front prefix sum is at least k, update result
            while dq and prefix[j] - prefix[dq[0]] >= k:
                result = min(result, j - dq.popleft())
            # Maintain increasing order of prefix sum values in deque
            while dq and prefix[dq[-1]] >= prefix[j]:
                dq.pop()
            # Append current index to deque
            dq.append(j)
        # Return result if a valid subarray was found, otherwise -1
        return result if result != float('inf') else -1

    # -------------------------------------------------------------------------
    # 15. Remove Duplicate Letters (LC 316) — T2
    # Remove duplicate letters so each letter appears once; result must be the
    # smallest in lexicographic order among all valid results.
    # Example: s="cbacdcbc" → "acdb"
    # Constraints: 1 <= len(s) <= 1e4, s consists of lowercase English letters
    # Time: O(n), Space: O(1) [alphabet size 26]
    # -------------------------------------------------------------------------
    def removeDuplicateLetters(self, s: str) -> str:
        # Map each character to its last occurrence index in string s
        last = {c: i for i, c in enumerate(s)}
        # Stack to store the characters for the final result
        stack = []
        # Set to track characters currently present in the stack (for O(1) membership checks)
        in_stack = set()
        # Iterate through the string
        for i, c in enumerate(s):
            # If character is already in the stack, skip to avoid duplicates
            if c in in_stack:
                continue
            # While stack is not empty, stack top character is lexicographically greater than current,
            # and the stack top character appears again later in the string
            while stack and stack[-1] > c and last[stack[-1]] > i:
                # Remove the character from the set and pop it from stack
                in_stack.remove(stack.pop())
            # Push the current character onto the stack
            stack.append(c)
            # Add current character to the set
            in_stack.add(c)
        return "".join(stack)

    # -------------------------------------------------------------------------
    # 16. Remove K Digits (LC 402) — T2
    # Remove k digits from num (string) to make the smallest possible number.
    # Example: num="1432219", k=3 → "1219"
    # Constraints: 1 <= len(num) <= 1e5, 0 <= k <= len(num)
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def removeKdigits(self, num: str, k: int) -> str:
        # Stack to store the digits of the resulting number
        stack = []
        # Iterate through each digit in the number
        for digit in num:
            # While stack is not empty, we still have digits to remove (k > 0),
            # and the stack top digit is greater than the current digit
            while stack and k > 0 and stack[-1] > digit:
                # Pop from stack to ensure a smaller digit is at a higher place value
                stack.pop()
                # Decrement removal count
                k -= 1
            # Push current digit onto stack
            stack.append(digit)
        # If there are still digits to remove, slice them off from the end of the stack
        result = "".join(stack[:-k] if k else stack)
        # Strip leading zeros, and return "0" if the resulting string is empty
        return result.lstrip("0") or "0"

    # -------------------------------------------------------------------------
    # 17. 132 Pattern (LC 456) — T2
    # Return True if nums contains i<j<k with nums[i]<nums[k]<nums[j].
    # Example: nums=[3,1,4,2] → True (1,4,2)
    # Constraints: 1 <= n <= 2e5, -1e9 <= nums[i] <= 1e9
    # Time: O(n), Space: O(n)
    # -------------------------------------------------------------------------
    def find132pattern(self, nums: List[int]) -> bool:
        # Monotonically decreasing stack of values, representing potential nums[j] (the '3' in 132)
        stack = []
        # Best value for nums[k] (the '2' in 132), initialized to negative infinity
        third = float('-inf')
        # Scan from right to left
        for val in reversed(nums):
            # If we find an element smaller than third, we have found a valid nums[i] < nums[k] < nums[j] pattern
            if val < third:
                return True
            # Maintain decreasing stack order. Any popped element is smaller than the current val (which is the new '3')
            # and is a candidate for third (the '2')
            while stack and stack[-1] < val:
                third = stack.pop()
            # Push current value onto stack
            stack.append(val)
        return False

    # -------------------------------------------------------------------------
    # 18. Trapping Rain Water (LC 42) — T2
    # Given elevation map heights, compute total trapped water.
    # Example: height=[0,1,0,2,1,0,1,3,2,1,2,1] → 6
    # Constraints: 1 <= n <= 2e4, 0 <= height[i] <= 1e5
    # Time: O(n), Space: O(n)  [also doable O(1) with two pointers]
    # -------------------------------------------------------------------------
    def trap(self, height: List[int]) -> int:
        # Monotonically decreasing stack to store index of bars
        stack = []
        # Track total trapped water volume
        water = 0
        # Iterate through the height map
        for i, h in enumerate(height):
            # While stack is not empty and current height is greater than height at stack top index
            while stack and height[stack[-1]] < h:
                # Pop the bottom of the valley (the floor)
                bottom = stack.pop()
                # If stack becomes empty, there is no left wall to contain water; break
                if not stack:
                    break
                # The index of the left wall is the current stack top
                left = stack[-1]
                # Calculate width between left wall and current bar
                width = i - left - 1
                # Bounded height is min of left and right walls minus the floor height
                bounded_height = min(height[left], h) - height[bottom]
                # Add trapped water volume to total
                water += bounded_height * width
            # Push current index onto stack
            stack.append(i)
        return water

    # -------------------------------------------------------------------------
    # 19. Maximal Rectangle (LC 85) — T3
    # Given binary matrix, find the largest rectangle containing only 1s.
    # Example: matrix=[["1","0","1","0","0"],
    #                   ["1","0","1","1","1"],
    #                   ["1","1","1","1","1"],
    #                   ["1","0","0","1","0"]] → 6
    # Constraints: rows,cols <= 200
    # Time: O(rows * cols), Space: O(cols)
    # -------------------------------------------------------------------------
    def maximalRectangle(self, matrix: List[List[str]]) -> int:
        # If matrix is empty, return 0
        if not matrix or not matrix[0]:
            return 0
        # Number of columns
        cols = len(matrix[0])
        # Heights array representing histogram bar height for each column
        heights = [0] * cols
        # Track maximum area rectangle found
        max_area = 0
        # Iterate row by row
        for row in matrix:
            for j in range(cols):
                # Update histogram height: increment by 1 if '1', reset to 0 if '0'
                heights[j] = heights[j] + 1 if row[j] == '1' else 0
            # Calculate maximum rectangle area using the histogram values for current row
            max_area = max(max_area, self.largestRectangleArea(heights))
        return max_area

    # -------------------------------------------------------------------------
    # 20. Maximum Score of a Good Subarray (LC 2104) — T2
    # A "good subarray" contains index k. Score = min(nums[i..j]) * (j-i+1).
    # Maximise the score.
    # Example: nums=[1,4,3,7,4,5], k=3 → 15  (subarray [3,7,4,5], min=3, len=4)
    # Constraints: 1 <= n <= 1e5, 1 <= nums[i] <= 1e6, 0 <= k < n
    # Time: O(n), Space: O(1)
    # -------------------------------------------------------------------------
    def maximumScore(self, nums: List[int], k: int) -> int:
        # Get length of array
        n = len(nums)
        # Initialize left and right pointers at index k
        left, right = k, k
        # Current minimum value in the subarray nums[left..right]
        cur_min = nums[k]
        # Track maximum score found, starting with base score of size-1 subarray at k
        result = cur_min
        # Expand pointers outward until we cover the entire array
        while left > 0 or right < n - 1:
            if left == 0:
                # If left pointer reached start, must expand to the right
                right += 1
            elif right == n - 1:
                # If right pointer reached end, must expand to the left
                left -= 1
            elif nums[left - 1] >= nums[right + 1]:
                # Expand to the left if left-adjacent element is larger to keep minimum high
                left -= 1
            else:
                # Otherwise, expand to the right
                right += 1
            # Update the current minimum to include the newly added element
            cur_min = min(cur_min, nums[left], nums[right])
            # Update maximum score (minimum value times subarray length)
            result = max(result, cur_min * (right - left + 1))
        return result


# -----------------------------------------------------------------------------
# Supporting class for problem 9
# -----------------------------------------------------------------------------
class StockSpanner:
    """Online Stock Span (LC 901)."""
    def __init__(self):
        # stack of (price, span) pairs — monotonic decreasing by price
        self.stack = []

    def next(self, price: int) -> int:
        # Start span at 1 for the current day
        span = 1
        # While stack is not empty and the price at the top of the stack is less than or equal to current price
        while self.stack and self.stack[-1][0] <= price:
            # Pop the elements and accumulate their spans to skip those days
            span += self.stack.pop()[1]
        # Push current price and its accumulated span onto stack
        self.stack.append((price, span))
        return span


# =============================================================================
if __name__ == "__main__":
    sol = MonotonicSolutions()
    errors = []

    def check(label, got, expected):
        """Predicate helper used to validate a candidate state or answer."""
        # Compare got and expected results
        if got != expected:
            errors.append(f"FAIL {label}: got {got!r}, expected {expected!r}")
        else:
            print(f"  OK  {label}")

    print("=== Monotonic Stack / Deque — test suite ===\n")

    # 1. Daily Temperatures
    check("dailyTemperatures",
          sol.dailyTemperatures([73,74,75,71,69,72,76,73]),
          [1,1,4,2,1,1,0,0])

    # 2. Next Greater Element I
    check("nextGreaterElement",
          sol.nextGreaterElement([4,1,2], [1,3,4,2]),
          [-1,3,-1])

    # 3. Next Greater Element II
    check("nextGreaterElements",
          sol.nextGreaterElements([1,2,1]),
          [2,-1,2])

    # 4. Next Greater Element III
    check("nextGreaterElementIII n=12", sol.nextGreaterElementIII(12), 21)
    check("nextGreaterElementIII n=21", sol.nextGreaterElementIII(21), -1)
    check("nextGreaterElementIII n=230241", sol.nextGreaterElementIII(230241), 230412)

    # 5. Next Smaller Element
    check("nextSmallerElement",
          sol.nextSmallerElement([4,5,2,10,8]),
          [2,2,-1,4,-1])

    # 6. Largest Rectangle in Histogram
    check("largestRectangleArea [2,1,5,6,2,3]",
          sol.largestRectangleArea([2,1,5,6,2,3]),
          10)
    check("largestRectangleArea [2,4]",
          sol.largestRectangleArea([2,4]),
          4)

    # 7. Sum of Subarray Minimums
    check("sumSubarrayMins [3,1,2,4]",
          sol.sumSubarrayMins([3,1,2,4]),
          17)

    # 8. Sum of Subarray Ranges
    check("subArrayRanges [1,2,3]",
          sol.subArrayRanges([1,2,3]),
          4)
    check("subArrayRanges [1,3,3]",
          sol.subArrayRanges([1,3,3]),
          4)

    # 9. Stock Spanner
    sp = StockSpanner()
    spans = [sp.next(p) for p in [100,80,60,70,60,75,85]]
    check("StockSpanner", spans, [1,1,1,2,1,4,6])

    # 10. Maximum Width Ramp
    check("maxWidthRamp [6,0,8,2,1,5]",
          sol.maxWidthRamp([6,0,8,2,1,5]),
          4)
    check("maxWidthRamp [9,8,1,0,1,9,4,0,4,1]",
          sol.maxWidthRamp([9,8,1,0,1,9,4,0,4,1]),
          7)

    # 11. Sliding Window Maximum
    check("maxSlidingWindow k=3",
          sol.maxSlidingWindow([1,3,-1,-3,5,3,6,7], 3),
          [3,3,5,5,6,7])
    check("maxSlidingWindow k=1",
          sol.maxSlidingWindow([1], 1),
          [1])

    # 12. Constrained Subsequence Sum
    check("constrainedSubsetSum k=2",
          sol.constrainedSubsetSum([10,2,-10,5,20], 2),
          37)
    check("constrainedSubsetSum k=1 all neg",
          sol.constrainedSubsetSum([-1,-2,-3], 1),
          -1)

    # 13. Jump Game VI
    check("maxResult k=2",
          sol.maxResult([1,-1,-2,4,-7,3], 2),
          7)
    check("maxResult k=1",
          sol.maxResult([10,-5,-2,4,0,3], 3),
          17)

    # 14. Shortest Subarray with Sum >= K
    check("shortestSubarray [2,-1,2] k=3",
          sol.shortestSubarray([2,-1,2], 3),
          3)
    check("shortestSubarray [1] k=1",
          sol.shortestSubarray([1], 1),
          1)
    check("shortestSubarray [1,2] k=4",
          sol.shortestSubarray([1,2], 4),
          -1)

    # 15. Remove Duplicate Letters
    check("removeDuplicateLetters bcabc",
          sol.removeDuplicateLetters("bcabc"),
          "abc")
    check("removeDuplicateLetters cbacdcbc",
          sol.removeDuplicateLetters("cbacdcbc"),
          "acdb")

    # 16. Remove K Digits
    check("removeKdigits 1432219 k=3",
          sol.removeKdigits("1432219", 3),
          "1219")
    check("removeKdigits 10200 k=1",
          sol.removeKdigits("10200", 1),
          "200")
    check("removeKdigits 10 k=2",
          sol.removeKdigits("10", 2),
          "0")

    # 17. 132 Pattern
    check("find132pattern [3,1,4,2]", sol.find132pattern([3,1,4,2]), True)
    check("find132pattern [1,2,3,4]", sol.find132pattern([1,2,3,4]), False)
    check("find132pattern [3,5,0,3,4]", sol.find132pattern([3,5,0,3,4]), True)

    # 18. Trapping Rain Water
    check("trap [0,1,0,2,1,0,1,3,2,1,2,1]",
          sol.trap([0,1,0,2,1,0,1,3,2,1,2,1]),
          6)
    check("trap [4,2,0,3,2,5]",
          sol.trap([4,2,0,3,2,5]),
          9)

    # 19. Maximal Rectangle
    matrix = [
        ["1","0","1","0","0"],
        ["1","0","1","1","1"],
        ["1","1","1","1","1"],
        ["1","0","0","1","0"],
    ]
    check("maximalRectangle", sol.maximalRectangle(matrix), 6)

    # 20. Maximum Score of a Good Subarray
    check("maximumScore [1,4,3,7,4,5] k=3",
          sol.maximumScore([1,4,3,7,4,5], 3),
          15)
    check("maximumScore [5,5,4,5,4,1,1,1] k=0",
          sol.maximumScore([5,5,4,5,4,1,1,1], 0),
          20)

    print()
    if errors:
        for e in errors:
            print(e)
        raise SystemExit(1)
    else:
        print("All tests passed.")
