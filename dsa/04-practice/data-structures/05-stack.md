---
tags: [coding, data-structures, stack]
topic: stack
difficulty: mixed
---
# Stack Problems

## What this covers

> [!abstract] In this file
> **Covers:** Worked stack problems: monotonic stack (next greater, histogram, contribution counting), parentheses, expression evaluation, stack design.
> **You'll be able to:** Recognise and code monotonic-stack problems in one pass.
> **Prereqs:** Stack lecture · **Pair with:** [Stack lecture](../../02-data-structures/05-stack.md) · **Time:** 3 h
> **Tiers:** ⚡ T1 must master · 🎯 T2 build fluency · 💤 T3 skip at L3 ([details](../../00-start-here/01-roadmap.md#tier-legend))

**Sections:** [Stack Interview Checklist](#stack-interview-checklist) · [Monotonic Stack — Next Greater/Smaller](#monotonic-stack--next-greatersmaller) · [Monotonic Stack — Arrays and Sequences](#monotonic-stack--arrays-and-sequences) · [Monotonic Stack — Histogram / Rectangle](#monotonic-stack--histogram--rectangle) · [Valid Parentheses / Nesting](#valid-parentheses--nesting) · [Stack Design](#stack-design) · [Queue from Stacks](#queue-from-stacks) · [Expression Evaluation](#expression-evaluation) · [Simulation / Other](#simulation--other) · [Parentheses — Score and Repair](#parentheses--score-and-repair)

> [!abstract]- Problem index (34)
> **Monotonic Stack — Next Greater/Smaller:** [Next Greater Element I](#next-greater-element-i--t2) · [Next Greater Element II](#next-greater-element-ii--t2) · [Daily Temperatures](#daily-temperatures--t2) · [Online Stock Span](#monotonic-stack--next-greatersmaller) · [Sum of Subarray Minimums](#monotonic-stack--next-greatersmaller)  
> **Monotonic Stack — Arrays and Sequences:** [Car Fleet (LC 853)](#car-fleet-lc-853--t2) · [Maximum Width Ramp (LC 962)](#monotonic-stack--arrays-and-sequences) · [Number of Visible People in a Queue (LC 1944)](#monotonic-stack--arrays-and-sequences) · [Flatten Binary Tree to Linked List (LC 114 — iterative)](#flatten-binary-tree-to-linked-list-lc-114--iterative--t2) · [Path Sum II (LC 113 — iterative DFS)](#path-sum-ii-lc-113--iterative-dfs--t2) · [132 Pattern (LC 456)](#monotonic-stack--arrays-and-sequences) · [Buildings With an Ocean View (LC 1762)](#monotonic-stack--arrays-and-sequences)  
> **Monotonic Stack — Histogram / Rectangle:** [Largest Rectangle in Histogram](#largest-rectangle-in-histogram--t2) · [Maximal Rectangle](#maximal-rectangle--t2) · [Trapping Rain Water (stack approach)](#trapping-rain-water-stack-approach--t1)  
> **Valid Parentheses / Nesting:** [Valid Parentheses](#valid-parentheses--t2) · [Valid Parenthesis String (LC 678)](#valid-parenthesis-string-lc-678--t2) · [Remove All Adjacent Duplicates in String](#valid-parentheses--nesting) · [Remove K Digits](#remove-k-digits--t2)  
> **Stack Design:** [Min Stack](#min-stack--t2) · [Maximum Frequency Stack](#stack-design)  
> **Queue from Stacks:** [Implement Queue using Stacks](#queue-from-stacks) · [Validate Stack Sequences](#queue-from-stacks)  
> **Expression Evaluation:** [Evaluate Reverse Polish Notation](#evaluate-reverse-polish-notation--t2) · [Basic Calculator I](#expression-evaluation) · [Basic Calculator II](#expression-evaluation) · [Basic Calculator III](#expression-evaluation)  
> **Simulation / Other:** [Exclusive Time of Functions](#simulation--other) · [Simplify Path](#simulation--other) · [Baseball Game](#simulation--other) · [Asteroid Collision](#asteroid-collision--t2)  
> **Parentheses — Score and Repair:** [Score of Parentheses (LC 856)](#parentheses--score-and-repair) · [Minimum Add to Make Parentheses Valid (LC 921)](#parentheses--score-and-repair) · [Check if Word is Valid After Substitutions (LC 1003)](#parentheses--score-and-repair)  

> [!tip] If you only have 20 minutes
> **Do these first:** [Daily Temperatures](#daily-temperatures--t2) · [Next Greater Element II](#next-greater-element-ii--t2) · [Largest Rectangle in Histogram](#largest-rectangle-in-histogram--t2) · [Trapping Rain Water (stack approach)](#trapping-rain-water-stack-approach--t1) · [Valid Parentheses](#valid-parentheses--t2) · [Min Stack](#min-stack--t2) · [Evaluate Reverse Polish Notation](#evaluate-reverse-polish-notation--t2) · [Asteroid Collision](#asteroid-collision--t2)
> **Template:** Monotonic stack of *indices*: `while st and a[st[-1]] < a[i]: j = st.pop(); ans[j] = i - j` — pop = "`i` is the answer for `j`".
> **Template:** Histogram: on pop, width = `i - st[-1] - 1` (or `i` if stack empty); append a sentinel `0` to flush.
> **Gotchas:** Store indices, not values · strict vs non-strict compare decides duplicate handling · circular arrays → loop `2n` with `i % n` · empty-stack check before `st[-1]`.

---

## Stack Interview Checklist

> [!info] When to reach for a stack
> - The problem asks for the next/previous greater or smaller item.
> - The input has nested structure: parentheses, scopes, encoded strings, call logs.
> - You need to undo the most recent unresolved action: duplicates cancel, collisions, path backtracking.
> - You want to keep a monotonic property while scanning once from left to right.
> - A brute-force solution repeatedly rescans past elements and feels quadratic.

> [!tip] Edge cases to sanity-check
> - Empty input, single element, and all-equal values.
> - Strict vs non-strict comparisons (`<` vs `<=`) when duplicates exist.
> - Sentinel values or end-of-array flushing.
> - Whether the answer is an index, a value, or a distance.

---

## Monotonic Stack — Next Greater/Smaller

---

### Next Greater Element I `🎯 T2`

> [!example] Problem
> The next greater element of some element x in an array is the first greater element that is to the right of x in the same array.
> You are given two distinct 0-indexed integer arrays nums1 and nums2, where nums1 is a subset of nums2.
> For each 0 <= i < nums1.length, find the index j such that nums1[i] == nums2[j] and determine the next greater element of nums2[j] in nums2. If there is no next greater element, then the answer for this query is -1.
> Return an array ans of length nums1.length such that ans[i] is the next greater element as described above.
> 
> **Example 1:**
> ```
> Input: nums1 = [4,1,2], nums2 = [1,3,4,2]
> Output: [-1,3,-1]
> Explanation: The next greater element for each value of nums1 is as follows:
> - 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
> - 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
> - 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
> ```
> 
> **Example 2:**
> ```
> Input: nums1 = [2,4], nums2 = [1,2,3,4]
> Output: [3,-1]
> Explanation: The next greater element for each value of nums1 is as follows:
> - 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
> - 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.
> ```
> 
> **Constraints:**
> - 1 <= nums1.length <= nums2.length <= 1000
> - 0 <= nums1[i], nums2[i] <= 10^4
> - All integers in nums1 and nums2 are unique.
> - All the integers of nums1 also appear in nums2.

> [!info] Approach
> We need the next greater element for many values, so we preprocess `nums2` with a monotonic stack to avoid repeated scans. Scan `nums2` once with a decreasing stack. When a larger value arrives, it resolves all smaller values on the stack. Store a map `value -> next greater value` and then answer each query from `nums1` in O(1).

> [!note]- Python Solution
> ```python
> def next_greater_element(nums1, nums2):
>     stack = []
>     nxt = {}
>     for x in nums2:
>         while stack and stack[-1] < x:
>             nxt[stack.pop()] = x
>         stack.append(x)
>     return [nxt.get(x, -1) for x in nums1]
> ```

> [!success] Complexity
> O(n) time, O(n) space.

> [!tip] Alternatives
> The same monotonic stack pattern generalizes to next greater/smaller element variants and stock-span style problems.

---

### Next Greater Element II `🎯 T2`

> [!example] Problem
> Given a circular integer array nums (i.e., the next element of nums[nums.length - 1] is nums[0]), return the next greater number for every element in nums.
> The next greater number of a number x is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return -1 for this number.
> 
> **Example 1:**
> ```
> Input: nums = [1,2,1]
> Output: [2,-1,2]
> Explanation: The first 1's next greater number is 2; 
> The number 2 can't find next greater number. 
> The second 1's next greater number needs to search circularly, which is also 2.
> ```
> 
> **Example 2:**
> ```
> Input: nums = [1,2,3,4,3]
> Output: [2,3,4,-1,4]
> ```
> 
> **Constraints:**
> - 1 <= nums.length <= 10^4
> - -10^9 <= nums[i] <= 10^9

> [!info] Approach
> Circular array means element `0` might be the next greater for element `n-1`. Simulate by doubling the array conceptually. Same decreasing monotonic stack. Iterate `0..2n-1` with `i % n` for index. Only push on the first pass (`i < n`) to avoid duplicate results. Initialize `result = [-1] * n`. Iterate `2n` times. Use `i % n` to access elements. Only push `i % n` when `i < n`.

> [!note]- Python Solution
> ```python
> def next_greater_elements(nums):
>     n = len(nums)
>     result = [-1] * n
>     stack = []
>     for i in range(2 * n):
>         while stack and nums[stack[-1]] < nums[i % n]:
>             result[stack.pop()] = nums[i % n]
>         if i < n:
>             stack.append(i)
>     return result
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Brute force O(n²) with modular wrapping. No fundamentally better approach.

---

### Daily Temperatures `🎯 T2`

> [!example] Problem
> Given an array of integers temperatures represents the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature. If there is no future day for which this is possible, keep answer[i] == 0 instead.
> 
> **Example 1:**
> ```
> Input: temperatures = [73,74,75,71,69,72,76,73]
> Output: [1,1,4,2,1,1,0,0]
> ```
> 
> **Example 2:**
> ```
> Input: temperatures = [30,40,50,60]
> Output: [1,1,1,0]
> ```
> 
> **Example 3:**
> ```
> Input: temperatures = [30,60,90]
> Output: [1,1,0]
> ```
> 
> **Constraints:**
> - 1 <= temperatures.length <= 10^5
> - 30 <= temperatures[i] <= 100

> [!tip] Recognize · Gotcha
> **Signal:** "Days until warmer" · **Gotcha:** Store **indices**, not values — need distance computation.

> [!failure] Tempting wrong approach
> Scanning forward from each day — O(n²). Keep a monotonic decreasing stack of indices; each pop resolves one answer.

> [!info] Approach
> Brute force checks every future day for each index — O(n²). We need to resolve each index exactly once. Monotonic decreasing stack of indices. When a warmer temperature arrives, all cooler pending indices on the stack have found their answer. Push index `i` onto the stack. When `temps[i] > temps[stack[-1]]`, pop and record `result[popped] = i - popped`. Stack holds indices of temperatures that haven't yet seen a warmer day.

> [!note]- Python Solution
> ```python
> def daily_temperatures(temperatures):
>     result = [0] * len(temperatures)
>     stack = []  # indices, decreasing temperature order
>     for i, t in enumerate(temperatures):
>         while stack and temperatures[stack[-1]] < t:
>             j = stack.pop()
>             result[j] = i - j
>         stack.append(i)
>     return result
> ```

> [!success] Complexity
> Time O(n) — each index pushed and popped at most once; Space O(n).

> [!tip] Alternatives
> Brute force O(n²). Sparse table for range-minimum queries — overkill here.

**Also try:**

- **Online Stock Span** — Naively scan backwards each day — O(n) per call, O(n²) total
- **Sum of Subarray Minimums** — Enumerate all subarrays — O(n²) or O(n³)

---

## Monotonic Stack — Arrays and Sequences

---

### Car Fleet (LC 853) `🎯 T2`

> [!example] Problem
> There are n cars at given miles away from the starting mile 0, traveling to reach the mile target.
> You are given two integer arrays position and speed, both of length n, where position[i] is the starting mile of the ith car and speed[i] is the speed of the ith car in miles per hour.
> A car cannot pass another car, but it can catch up and then travel next to it at the speed of the slower car.
> A car fleet is a car or cars driving next to each other. The speed of the car fleet is the minimum speed of any car in the fleet.
> If a car catches up to a car fleet at the mile target, it will still be considered as part of the car fleet.
> Return the number of car fleets that will arrive at the destination.
> 
> **Example 1:**
> ```
> Input: target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]
> Output: 3
> Explanation:
> ```
> 
> **Example 2:**
> ```
> Input: target = 10, position = [3], speed = [3]
> Output: 1
> Explanation:
> ```
> 
> **Example 3:**
> ```
> Input: target = 100, position = [0,2,4], speed = [4,2,1]
> Output: 1
> Explanation:
> ```
> 
> **Constraints:**
> - n == position.length == speed.length
> - 1 <= n <= 10^5
> - 0 < target <= 10^6
> - 0 <= position[i] < target
> - All the values of position are unique.
> - 0 < speed[i] <= 10^6

> [!info] Approach
> Cars closer to the target are ahead. A car behind can only join the fleet ahead if it arrives no later. A stack of arrival times tracks fleets. Sort by position descending (closest to target first). Compute each car's arrival time `(target - pos) / speed`. A car merges into the fleet ahead if its time ≤ the current stack top (it catches up). Otherwise it starts a new fleet. Iterate sorted arrival times. Push if `> stack[-1]` (or stack empty). Stack size = number of fleets.

> [!note]- Python Solution
> ```python
> def car_fleet(target, position, speed):
>     pairs = sorted(zip(position, speed), reverse=True)
>     stack = []
>     for pos, spd in pairs:
>         time = (target - pos) / spd
>         if not stack or time > stack[-1]:
>             stack.append(time)
>         # else: merges into the fleet ahead (smaller or equal time)
>     return len(stack)
> ```

> [!success] Complexity
> Time O(n log n) for sort; Space O(n).

> [!tip] Alternatives
> After sorting, a single pass with a counter (no explicit stack) works: increment count whenever a car's time exceeds the current fleet's time.

---

### Flatten Binary Tree to Linked List (LC 114 — iterative) `🎯 T2`

> [!example] Problem
> Same problem as [Flatten Binary Tree to Linked List](08-tree.md#flatten-binary-tree-to-linked-list--t2) — this section covers the alternative approach only.

> [!info] Approach
> Recursive flatten risks call-stack overflow on skewed trees. Iterative with an explicit stack gives O(h) space. Preorder traversal with a stack. Process root, push right child then left child (so left is processed first). After visiting each node, redirect its `right` to the next preorder node, set `left = None`. Push root. While stack: pop node, if node.right exists push it, if node.left exists push it. Set `node.right = stack[-1] if stack else None`, `node.left = None`.

> [!note]- Python Solution
> ```python
> class TreeNode:
>     def __init__(self, val=0, left=None, right=None):
>         self.val = val
>         self.left = left
>         self.right = right
> >
> def flatten(root):
>     if not root:
>         return
>     stack = [root]
>     while stack:
>         node = stack.pop()
>         if node.right:
>             stack.append(node.right)
>         if node.left:
>             stack.append(node.left)
>         node.right = stack[-1] if stack else None
>         node.left = None
> ```

> [!success] Complexity
> Time O(n); Space O(h) where h = tree height.

> [!tip] Alternatives
> Morris traversal — O(n) time O(1) space (no stack), but modifies tree temporarily and is harder to reason about. The "find predecessor" approach in O(n) with constant space is also canonical.

---

### Path Sum II (LC 113 — iterative DFS) `🎯 T2`

> [!example] Problem
> Same problem as [Path Sum II](08-tree.md#path-sum-ii--t2) — this section covers the alternative approach only.

> [!info] Approach
> Recursive DFS is natural but risks stack overflow. An iterative DFS with an explicit stack carrying path state mirrors the recursion exactly. Stack of `(node, remaining_sum, path)` tuples. When a leaf is reached with `remaining == 0`, record the path. Push `(root, target, [])`. On each pop: if leaf and remaining == 0, add copy of path to results. Push right child, then left child (left processed first) with updated remaining and path.

> [!note]- Python Solution
> ```python
> def path_sum(root, target_sum):
>     if not root:
>         return []
>     results = []
>     stack = [(root, target_sum, [])]
>     while stack:
>         node, remaining, path = stack.pop()
>         path = path + [node.val]
>         remaining -= node.val
>         if not node.left and not node.right:
>             if remaining == 0:
>                 results.append(path)
>         else:
>             if node.right:
>                 stack.append((node.right, remaining, path))
>             if node.left:
>                 stack.append((node.left, remaining, path))
>     return results
> ```

> [!success] Complexity
> Time O(n); Space O(n) for stack and path copies (worst case skewed tree).

> [!tip] Alternatives
> Recursive DFS with backtracking — cleaner code, but O(h) call stack. For a balanced tree that's O(log n); for skewed trees risk overflow.

**Also try:**

- **Maximum Width Ramp (LC 962)** — We want the leftmost possible `i` and rightmost possible `j`
- **Number of Visible People in a Queue (LC 1944)** — A taller person blocks all shorter ones behind them
- **132 Pattern (LC 456)** — Brute force is O(n³)
- **Buildings With an Ocean View (LC 1762)** — A building has an ocean view iff it is taller than all buildings to its right

---

## Monotonic Stack — Histogram / Rectangle

---

### Largest Rectangle in Histogram `🎯 T2`

> [!example] Problem
> Given an array of integers heights representing the histogram's bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.
> 
> **Example 1:**
> ```
> Input: heights = [2,1,5,6,2,3]
> Output: 10
> Explanation: The above is a histogram where width of each bar is 1.
> The largest rectangle is shown in the red area, which has an area = 10 units.
> ```
> 
> **Example 2:**
> ```
> Input: heights = [2,4]
> Output: 4
> ```
> 
> **Constraints:**
> - 1 <= heights.length <= 10^5
> - 0 <= heights[i] <= 10^4

> [!tip] Recognize · Gotcha
> **Signal:** Monotonic stack · **Gotcha:** **Sentinel 0** at end to flush stack; **width** formula when stack empty.

> [!failure] Tempting wrong approach
> Expanding left/right from every bar — O(n²). Use a monotonic increasing stack; on pop, width = `i - stack[-1] - 1` (or `i` if the stack is empty).

> [!info] Approach
> For each bar as the height of the rectangle, the width extends left and right until a shorter bar is hit. Finding those boundaries naively is O(n) each. Monotonic increasing stack of indices. When a bar shorter than the stack top arrives, the top bar's right boundary has been found — compute area. Append sentinel `0` to flush the stack. On pop, `height = heights[popped]`. Width = `i - stack[-1] - 1` if stack is non-empty, else `i` (the bar is the global minimum so far).

> [!note]- Python Solution
> ```python
> def largest_rectangle_area(heights):
>     stack = []  # increasing stack of indices
>     best = 0
>     for i, h in enumerate(heights + [0]):  # sentinel 0 flushes stack
>         while stack and heights[stack[-1]] > h:
>             height = heights[stack.pop()]
>             width = i if not stack else i - stack[-1] - 1
>             best = max(best, height * width)
>         stack.append(i)
>     return best
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Divide and conquer O(n log n) average — find minimum bar, recurse on left and right. Brute force O(n²).

---

### Maximal Rectangle `🎯 T2`

> [!example] Problem
> Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.
> 
> **Example 1:**
> ```
> Input: matrix = [["1","0","1","0","0"],["1","0","1","1","1"],["1","1","1","1","1"],["1","0","0","1","0"]]
> Output: 6
> Explanation: The maximal rectangle is shown in the above picture.
> ```
> 
> **Example 2:**
> ```
> Input: matrix = [["0"]]
> Output: 0
> ```
> 
> **Example 3:**
> ```
> Input: matrix = [["1"]]
> Output: 1
> ```
> 
> **Constraints:**
> - rows == matrix.length
> - cols == matrix[i].length
> - 1 <= row, cols <= 200
> - matrix[i][j] is '0' or '1'.

> [!info] Approach
> Reduce to Largest Rectangle in Histogram. Each row defines a histogram where `heights[j]` = consecutive '1's above and including `matrix[row][j]`. Maintain a `heights` array. For each row, update heights (reset to 0 on '0', increment on '1'). Apply the histogram algorithm per row. `heights[j] = heights[j] + 1 if matrix[row][j] == '1' else 0`. Run `largest_rectangle_area(heights)` for each row.

> [!note]- Python Solution
> ```python
> def maximal_rectangle(matrix):
>     if not matrix or not matrix[0]:
>         return 0
>     cols = len(matrix[0])
>     heights = [0] * cols
>     best = 0
>     for row in matrix:
>         for j in range(cols):
>             heights[j] = heights[j] + 1 if row[j] == '1' else 0
>         best = max(best, largest_rectangle_area(heights))
>     return best
> >
> def largest_rectangle_area(heights):
>     stack = []
>     best = 0
>     for i, h in enumerate(heights + [0]):
>         while stack and heights[stack[-1]] > h:
>             height = heights[stack.pop()]
>             width = i if not stack else i - stack[-1] - 1
>             best = max(best, height * width)
>         stack.append(i)
>     return best
> ```

> [!success] Complexity
> Time O(rows * cols); Space O(cols).

> [!tip] Alternatives
> DP with `left[j]`, `right[j]`, `height[j]` arrays — O(rows * cols), same complexity without the stack. Useful to know for follow-up.

---

### Trapping Rain Water (stack approach) `⚡ T1`

> [!example] Problem
> Same problem as [Trapping Rain Water (LC 42)](../algorithms/02-two-pointers.md#trapping-rain-water-lc-42--t1) — this section covers the alternative approach only.

> [!info] Approach
> Water fills valleys. Each valley is bounded by taller bars on both sides. The stack lets us process valleys as they form. Monotonic decreasing stack. When a taller bar arrives, the top of the stack is a valley bottom. Water height = `min(left_bar, current_bar) - valley_bottom_height`. Width = distance between left and current bar minus 1. Push indices onto a decreasing stack. On pop (taller bar arrived), compute bounded water above the popped bar.

> [!note]- Python Solution
> ```python
> def trap(height):
>     stack = []
>     water = 0
>     for i, h in enumerate(height):
>         while stack and height[stack[-1]] < h:
>             bottom = stack.pop()
>             if not stack:
>                 break
>             left = stack[-1]
>             bounded_height = min(height[left], h) - height[bottom]
>             water += bounded_height * (i - left - 1)
>         stack.append(i)
>     return water
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Two-pointer O(n) time O(1) space — `left_max` and `right_max` pointers. Simpler to code in practice; stack version better for explaining the "why".

---

## Valid Parentheses / Nesting

---

### Valid Parentheses `🎯 T2`

> [!example] Problem
> Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
> An input string is valid if
> 
> **Example 1:**
> ```
> Input: s = "()"
> Output: true
> ```
> 
> **Example 2:**
> ```
> Input: s = "()[]{}"
> Output: true
> ```
> 
> **Example 3:**
> ```
> Input: s = "(]"
> Output: false
> ```
> 
> **Example 4:**
> ```
> Input: s = "([])"
> Output: true
> ```
> 
> **Example 5:**
> ```
> Input: s = "([)]"
> Output: false
> ```
> 
> **Constraints:**
> - 1 <= s.length <= 10^4
> - s consists of parentheses only '()[]{}'.

> [!tip] Recognize · Gotcha
> **Signal:** Stack matching · **Gotcha:** **Order** matters; **only one type** of bracket in simpler variants.

> [!info] Approach
> LIFO — the most recently opened bracket must be the next closed. Push opening brackets. On each closing bracket, pop the stack and verify it matches. Map `')' → '('`, etc. If stack is empty when closing bracket arrives, or top doesn't match, return `False`. Valid iff stack is empty at end.

> [!note]- Python Solution
> ```python
> def is_valid(s):
>     stack = []
>     pairs = {')': '(', ']': '[', '}': '{'}
>     for ch in s:
>         if ch in '([{':
>             stack.append(ch)
>         elif not stack or stack[-1] != pairs[ch]:
>             return False
>         else:
>             stack.pop()
>     return not stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Counter approach fails — `([)]` has equal counts but is invalid. Stack is necessary for order.

---

### Valid Parenthesis String (LC 678) `🎯 T2`

> [!example] Problem
> String `s` contains only `(`, `)`, and `*`, where `*` can act as `(`, `)`, or an empty string. Return true if `s` can be made valid.
>
> **Example:**
> ```
> Input: s = "(*))"   → true   (* acts as "(")
> Input: s = "(*("    → false
> ```

> [!info] Approach
> Track the **range** of possible open-bracket counts instead of one exact count. `lo` = open count if every `*` is `)`/empty; `hi` = open count if every `*` is `(`. On `(`: both +1. On `)`: both −1. On `*`: `lo -= 1`, `hi += 1`. If `hi < 0` at any point, too many `)` even with all `*` as `(` → false. Clamp `lo` at 0 (a `*` need not be `)` when there's nothing to close). Valid iff `lo == 0` at the end — some assignment closes everything exactly.

> [!note]- Python Solution
> ```python
> def check_valid_string(s):
>     lo = hi = 0
>     for c in s:
>         if c == '(':
>             lo += 1; hi += 1
>         elif c == ')':
>             lo -= 1; hi -= 1
>         else:  # '*'
>             lo -= 1; hi += 1
>         if hi < 0:
>             return False
>         lo = max(lo, 0)
>     return lo == 0
> ```

> [!success] Complexity
> O(n) time, O(1) space.

> [!tip] Alternatives
> Two-stack solution (indices of `(` and `*`, match `)` greedily, then pair leftover `(` with later `*`) — O(n) space, easier to reinvent under pressure. Greedy range-tracking is the interview-impressive one; know both.

---

### Remove K Digits `🎯 T2`

> [!example] Problem
> Given string num representing a non-negative integer num, and an integer k, return the smallest possible integer after removing k digits from num.
> 
> **Example 1:**
> ```
> Input: num = "1432219", k = 3
> Output: "1219"
> Explanation: Remove the three digits 4, 3, and 2 to form the new number 1219 which is the smallest.
> ```
> 
> **Example 2:**
> ```
> Input: num = "10200", k = 1
> Output: "200"
> Explanation: Remove the leading 1 and the number is 200. Note that the output must not contain leading zeroes.
> ```
> 
> **Example 3:**
> ```
> Input: num = "10", k = 2
> Output: "0"
> Explanation: Remove all the digits from the number and it is left with nothing which is 0.
> ```
> 
> **Constraints:**
> - 1 <= k <= num.length <= 10^5
> - num consists of only digits.
> - num does not have any leading zeros except for the zero itself.

> [!info] Approach
> Greedy — to minimize, remove a digit when the next digit is smaller (it would be more beneficial at that position). Monotonic increasing stack. Pop the top when it's larger than the current digit and `k > 0`. Build the stack left to right. Pop larger elements while `k > 0`. If `k` still > 0 after the loop, trim last `k` digits from the stack (which is already sorted ascending). Strip leading zeros.

> [!note]- Python Solution
> ```python
> def remove_k_digits(num, k):
>     stack = []
>     for d in num:
>         while k > 0 and stack and stack[-1] > d:
>             stack.pop()
>             k -= 1
>         stack.append(d)
>     # If k > 0, remove from the end (stack is already non-decreasing)
>     stack = stack[:-k] if k else stack
>     result = ''.join(stack).lstrip('0')
>     return result or '0'
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No fundamentally better approach. The greedy monotonic stack is O(n) optimal.

**Also try:**

- **Remove All Adjacent Duplicates in String** — Removing one pair can create new adjacent duplicates — process must cascade

---

## Stack Design

---

### Min Stack `🎯 T2`

> [!example] Problem
> Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.
> Implement the MinStack class:
> You must implement a solution with O(1) time complexity for each function.
> 
> **Example 1:**
> ```
> Input
> ["MinStack","push","push","push","getMin","pop","top","getMin"]
> [[],[-2],[0],[-3],[],[],[],[]]
> 
> Output
> [null,null,null,null,-3,null,0,-2]
> 
> Explanation
> MinStack minStack = new MinStack();
> minStack.push(-2);
> minStack.push(0);
> minStack.push(-3);
> minStack.getMin(); // return -3
> minStack.pop();
> minStack.top();    // return 0
> minStack.getMin(); // return -2
> ```
> 
> **Constraints:**
> - -2^{31} <= val <= 2^{31} - 1
> - Methods pop, top and getMin operations will always be called on non-empty stacks.
> - At most 3 * 10^4 calls will be made to push, pop, top, and getMin.

> [!info] Approach
> A regular stack loses track of the minimum after pops. We need the minimum at every stack depth. Parallel `min_stack` where `min_stack[i]` = minimum of all elements in `stack[0..i]`. Both stacks stay synchronized. On push, `min_stack` pushes `min(val, min_stack[-1])`. On pop, both stacks pop. `get_min` returns `min_stack[-1]`.

> [!note]- Python Solution
> ```python
> class MinStack:
>     def __init__(self):
>         self._stack: list[int] = []
>         self._min_stack: list[int] = []
> >
>     def push(self, val):
>         self._stack.append(val)
>         current_min = val if not self._min_stack else min(val, self._min_stack[-1])
>         self._min_stack.append(current_min)
> >
>     def pop(self):
>         self._stack.pop()
>         self._min_stack.pop()
> >
>     def top(self):
>         return self._stack[-1]
> >
>     def get_min(self):
>         return self._min_stack[-1]
> ```

> [!success] Complexity
> Time O(1) all ops; Space O(n).

> [!tip] Alternatives
> Store `(val, current_min)` tuples in a single stack — same complexity, single structure. Saves one stack at the cost of slightly less readable code.

**Also try:**

- **Maximum Frequency Stack** — Standard stack gives LIFO; we want frequency-priority with LIFO for ties

---

## Queue from Stacks

**Also try:**

- **Implement Queue using Stacks** — Stack is LIFO; reversing the stack gives FIFO order
- **Validate Stack Sequences** — Simulate the push sequence and greedily pop when the top matches the next expected pop

---

## Expression Evaluation

---

### Evaluate Reverse Polish Notation `🎯 T2`

> [!example] Problem
> You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.
> Evaluate the expression. Return an integer that represents the value of the expression.
> Note that
> 
> **Example 1:**
> ```
> Input: tokens = ["2","1","+","3","*"]
> Output: 9
> Explanation: ((2 + 1) * 3) = 9
> ```
> 
> **Example 2:**
> ```
> Input: tokens = ["4","13","5","/","+"]
> Output: 6
> Explanation: (4 + (13 / 5)) = 6
> ```
> 
> **Example 3:**
> ```
> Input: tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
> Output: 22
> Explanation: ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
> = ((10 * (6 / (12 * -11))) + 17) + 5
> = ((10 * (6 / -132)) + 17) + 5
> = ((10 * 0) + 17) + 5
> = (0 + 17) + 5
> = 17 + 5
> = 22
> ```
> 
> **Constraints:**
> - 1 <= tokens.length <= 10^4
> - tokens[i] is either an operator: "+", "-", "*", or "/", or an integer in the range [-200, 200].

> [!info] Approach
> RPN eliminates parentheses — operators apply to the two most recently seen operands. LIFO matches this. Operand stack. Push numbers. On operator, pop two operands, apply, push result. Pop `b` then `a` (order matters for `-` and `/`). Apply operator. Push result. Division truncates toward zero: `int(a / b)` not `a // b` (handles negatives).

> [!note]- Python Solution
> ```python
> def eval_rpn(tokens):
>     stack = []
>     ops = {'+', '-', '*', '/'}
>     for token in tokens:
>         if token in ops:
>             b, a = stack.pop(), stack.pop()
>             if token == '+': stack.append(a + b)
>             elif token == '-': stack.append(a - b)
>             elif token == '*': stack.append(a * b)
>             else: stack.append(int(a / b))  # truncate toward zero
>         else:
>             stack.append(int(token))
>     return stack[0]
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> Recursive evaluation — same complexity but harder to implement iteratively for deeply nested expressions.

**Also try:**

- **Basic Calculator I** — Parentheses introduce nested scope
- **Basic Calculator II** — `*` and `/` have higher precedence than `+` and `-`
- **Basic Calculator III** — Combination of I (parentheses) and II (precedence)

---

## Simulation / Other

---

### Asteroid Collision `🎯 T2`

> [!example] Problem
> We are given an array asteroids of integers representing asteroids in a row. The indices of the asteriod in the array represent their relative position in space.
> For each asteroid, the absolute value represents its size, and the sign represents its direction (positive meaning right, negative meaning left). Each asteroid moves at the same speed.
> Find out the state of the asteroids after all collisions. If two asteroids meet, the smaller one will explode. If both are the same size, both will explode. Two asteroids moving in the same direction will never meet.
> 
> **Example 1:**
> ```
> Input: asteroids = [5,10,-5]
> Output: [5,10]
> Explanation: The 10 and -5 collide resulting in 10. The 5 and 10 never collide.
> ```
> 
> **Example 2:**
> ```
> Input: asteroids = [8,-8]
> Output: []
> Explanation: The 8 and -8 collide exploding each other.
> ```
> 
> **Example 3:**
> ```
> Input: asteroids = [10,2,-5]
> Output: [10]
> Explanation: The 2 and -5 collide resulting in -5. The 10 and -5 collide resulting in 10.
> ```
> 
> **Constraints:**
> - 2 <= asteroids.length <= 10^4
> - -1000 <= asteroids[i] <= 1000
> - asteroids[i] != 0

> [!info] Approach
> Collisions only happen between a positive (right-moving) on the stack and a new negative (left-moving). Stack of survivors. Maintain a stack of surviving asteroids. A collision only occurs when `stack[-1] > 0 and asteroid < 0`. While collision conditions hold: if top is smaller, pop (top destroyed, current continues); if equal, pop and break (both destroyed); if top is larger, break (current destroyed, don't append). Use `while...else` to append only if current survived.

> [!note]- Python Solution
> ```python
> def asteroid_collision(asteroids):
>     stack = []
>     for ast in asteroids:
>         survived = True
>         while stack and stack[-1] > 0 and ast < 0:
>             if stack[-1] < abs(ast):
>                 stack.pop()
>             elif stack[-1] == abs(ast):
>                 stack.pop()
>                 survived = False
>                 break
>             else:
>                 survived = False
>                 break
>         if survived:
>             stack.append(ast)
>     return stack
> ```

> [!success] Complexity
> Time O(n); Space O(n).

> [!tip] Alternatives
> No fundamentally different approach — stack simulation is inherent to sequential collision resolution.

**Also try:**

- **Exclusive Time of Functions** — Functions nest (call stack semantics)
- **Simplify Path** — `..` means go up one directory — pop from the path
- **Baseball Game** — All operations reference the top of the score history — LIFO structure

---

## Parentheses — Score and Repair

**Also try:**

- **Score of Parentheses (LC 856)** — Depth determines the multiplier — each level of nesting doubles the score of inner `()`
- **Minimum Add to Make Parentheses Valid (LC 921)** — An unmatched `)` cannot be fixed by future characters — it needs an immediate `(` inserted to its left
- **Check if Word is Valid After Substitutions (LC 1003)** — Every `c` must be preceded by `ab` immediately below it — a nesting structure

---

## See Also

[[queue]] | [[dynamic-programming]] | [[monotonic-techniques]]
