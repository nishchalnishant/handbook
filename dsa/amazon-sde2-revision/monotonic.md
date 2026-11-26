# Monotonic Stack — Amazon SDE-2 Reference

One template. Two flavors. Everything else is a variation.

---

summary 

these are the monotonic stack points 
- iterate from right to left 
- chek if the stack is empty
- if yes just push the current element in the stack
- if not check if the top most element is less than the current one, if yes just push the element to it if no pop till we find an element less than current element

modify this to get different variations

Next Smaller to Right: Iterate right-to-left, pop if stack[-1] >= current
Next Greater to Right: Iterate right-to-left, pop if stack[-1] <= current
Next Smaller to Left: Iterate left-to-right, pop if stack[-1] >= current
Next Greater to Left: Iterate left-to-right, pop if stack[-1] <= current


----

## The Core Template

```python
stack = []          # stores indices (almost always indices, not values)
for i, x in enumerate(arr):
    while stack and CONDITION:
        j = stack.pop()
        # j just found its answer — record it here
    stack.append(i)
```

---

## Flavor 1 — Monotonic Increasing Stack

Stack values go **small → large** bottom to top.
Pop when current element is **smaller** than top → finds **next/prev smaller**.

```python
stack = []
for i, x in enumerate(arr):
    while stack and arr[stack[-1]] >= x:   # pop anything >= x
        j = stack.pop()
        # arr[j]'s next smaller = x (index i)
        # arr[j]'s prev smaller = arr[stack[-1]] if stack else none
    stack.append(i)
```

**Next smaller element:**
```python
def next_smaller(arr):
    # res stores the index of the next smaller element. 
    # Init to -1: assume no smaller element unless we find one.
    res = [-1] * len(arr)
    
    # stack stores indices of elements for which we HAVEN'T YET FOUND a smaller element.
    stack = []
    
    for i, x in enumerate(arr):
        # Is current value 'x' smaller than the value of the index sitting on top of the stack?
        # If yes, 'x' is officially the "Next Smaller Element" for the guy on top!
        while stack and arr[stack[-1]] > x:
            # Remove the top index from the stack because we found its answer.
            popped_index = stack.pop()
            
            # Record our discovery: The next smaller element for 'popped_index' is located at index 'i'.
            res[popped_index] = i
            
        # Push current index 'i' onto the stack because we don't know ITS next smaller element yet.
        stack.append(i)
        
    return res
# [3,1,2,4] → [1,-1,-1,-1]  (index of next smaller)
```

**Previous smaller element:**
```python
def prev_smaller(arr):
    res = [-1] * len(arr)
    stack = []
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] >= x:
            stack.pop()
        res[i] = stack[-1] if stack else -1   # top = prev smaller index
        stack.append(i)
    return res
# [3,1,2,4] → [-1,-1,1,2]  (index of prev smaller)
```

---

## Flavor 2 — Monotonic Decreasing Stack

Stack values go **large → small** bottom to top.
Pop when current element is **larger** than top → finds **next/prev greater**.

```python
stack = []
for i, x in enumerate(arr):
    while stack and arr[stack[-1]] <= x:   # pop anything <= x
        j = stack.pop()
        # arr[j]'s next greater = x (index i)
        # arr[j]'s prev greater = arr[stack[-1]] if stack else none
    stack.append(i)
```

**Next greater element:**
```python
def next_greater(arr):
    res = [-1] * len(arr)
    stack = []
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] < x:
            res[stack.pop()] = i
        stack.append(i)
    return res
# [2,1,3,4] → [2,2,3,-1]  (index of next greater)
```

**Previous greater element:**
```python
def prev_greater(arr):
    res = [-1] * len(arr)
    stack = []
    for i, x in enumerate(arr):
        while stack and arr[stack[-1]] <= x:
            stack.pop()
        res[i] = stack[-1] if stack else -1
        stack.append(i)
    return res
```

---

## The `>` vs `>=` Rule

| Condition in `while` | Stack type | Finds |
|----------------------|------------|-------|
| `arr[top] >= x` | increasing | next **strictly smaller** |
| `arr[top] > x`  | increasing | next **smaller or equal** |
| `arr[top] <= x` | decreasing | next **strictly greater** |
| `arr[top] < x`  | decreasing | next **greater or equal** |

For most interview problems, use strict (`>` / `<`) — handles duplicates cleanly.

---

## Problem Patterns

### Daily Temperatures (LC 739) — next greater, return distance not index

```python
def daily_temperatures(temps):
    res = [0] * len(temps)
    stack = []                          # decreasing stack
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j             # distance, not index
        stack.append(i)
    return res
```

---

### Largest Rectangle in Histogram (LC 84) — prev + next smaller, area = h × width

```python
def largest_rectangle(heights):
    heights = [0] + heights + [0]      # sentinel 0s to flush stack at the end
    stack = [0]                        # increasing stack, stores indices
    res = 0
    for i in range(1, len(heights)):
        while heights[stack[-1]] > heights[i]:
            h = heights[stack.pop()]
            w = i - stack[-1] - 1      # width between prev smaller and current
            res = max(res, h * w)
        stack.append(i)
    return res
```

---

### Trapping Rain Water (LC 42) — decreasing stack, water fills between bars

```python
def trap(height):
    stack = []                         # decreasing stack
    water = 0
    for i, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            bottom = height[stack.pop()]
            if not stack:
                break
            width = i - stack[-1] - 1
            water += (min(height[stack[-1]], h) - bottom) * width
        stack.append(i)
    return water
```

---

### Sum of Subarray Minimums (LC 907) — contribution counting

Each element contributes as minimum for subarrays where it is the smallest.
Use prev smaller (left boundary) + next smaller (right boundary).

```python
def sum_subarray_mins(arr):
    MOD = 10**9 + 7
    n = len(arr)
    left = [0] * n    # number of subarrays where arr[i] is min on the left
    right = [0] * n

    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] >= arr[i]:
            stack.pop()
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] > arr[i]:   # strict > to avoid double count
            stack.pop()
        right[i] = stack[-1] - i if stack else n - i
        stack.append(i)

    return sum(arr[i] * left[i] * right[i] for i in range(n)) % MOD
```

---

### Next Greater Element II — circular array (LC 503)

Iterate twice to simulate wraparound. Use `i % n` for index.

```python
def next_greater_ii(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        while stack and nums[stack[-1]] < nums[i % n]:
            res[stack.pop()] = nums[i % n]
        if i < n:
            stack.append(i)
    return res
```

---

## What Stays the Same Across All Problems

1. Stack stores **indices**, not values — you need both position and value
2. Pop inside the `while` loop = "this element just found its answer"
3. After the loop, anything left in the stack has no next greater/smaller (answer = -1 or n)
4. Sentinel values (`[0] + arr + [0]`) flush the stack without extra post-loop handling

---

## Complexity

| | Time | Space |
|-|------|-------|
| Every element pushed once, popped once | O(N) | O(N) stack |
