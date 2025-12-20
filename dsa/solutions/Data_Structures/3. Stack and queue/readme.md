# Stack & Queue Overview 📚

Stacks and Queues are fundamental linear data structures. Stack follows **LIFO** (Last In First Out) and Queue follows **FIFO** (First In First Out).

## Topics Covered

### 1. Stack (LIFO)
- **Operations**: Push, Pop, Peek (all O(1)).
- **Applications**:
    - Expression Evaluation (Postfix/Prefix).
    - Backtracking (DFS).
    - Undo mechanisms.
    - Valid Parentheses.

### 2. Queue (FIFO)
- **Operations**: Enqueue, Dequeue (O(1) with deque).
- **Applications**:
    - BFS (Level Order Traversal).
    - Task Scheduling.
    - Sliding Window (Deque).

### 3. Monotonic Stack
- **Concept**: Maintain elements in increasing/decreasing order.
- **Use Case**: Next Greater Element, Daily Temperatures, Largest Rectangle in Histogram.

### 4. Priority Queue (Heap)
- **Concept**: Elements processed by priority.
- **Use Case**: Dijkstra, Top K elements.

---

## Problems & Solutions

### Easy
1. **[Valid Parentheses](Easy/valid_parentheses.py)**
   - Check if brackets are balanced `()[]{}`.
2. **[Implement Queue using Stacks](Easy/implement_queue_using_stacks.py)**
   - Implement FIFO queue using two stacks.
3. **[Implement Stack using Queues](Easy/implement_stack_using_queues.py)**
   - Implement LIFO stack using queues.
4. **[Min Stack](Easy/min_stack.py)**
   - Stack with O(1) `getMin()`.

### Medium
1. **[Evaluate Reverse Polish Notation](Medium/evaluate_rpn.py)**
   - Evaluate postfix arithmetic expressions.
2. **[Daily Temperatures](Medium/daily_temperatures.py)**
   - Find days until warmer temperature (Monotonic Stack).
3. **[Generate Parentheses](Medium/generate_parentheses.py)**
   - Generate all valid combinations of `n` pairs of parentheses.
4. **[Decode String](Medium/decode_string.py)**
   - Decode strings like `3[a]2[bc]` -> `aaabcbc`.

### Hard
1. **[Largest Rectangle in Histogram](Hard/largest_rectangle_histogram.py)**
   - Find largest area in histogram (Monotonic Stack).
2. **[Trapping Rain Water](Hard/trapping_rain_water.py)**
   - Compute how much water can be trapped (Two Pointers / Stack).
3. **[Sliding Window Maximum](Hard/sliding_window_maximum.py)**
   - Find max in sliding window (Deque).

---

## Tips for Interviews
- **Stack for Matching**: Any problem involving matching pairs (brackets, tags) usually needs a stack.
- **Monotonic Stack**: If looking for "Next Greater/Smaller" element, think Monotonic Stack.
- **BFS = Queue**: Almost all BFS implementations use a queue.
