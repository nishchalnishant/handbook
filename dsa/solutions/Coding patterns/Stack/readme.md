# Stack & Monotonic Stack 🥞

## Description
A Stack is a LIFO (Last In First Out) data structure. It's crucial for parsing, expression evaluation, and problems involving matching or "history".

## Strategies

### 1. Valid Parentheses
- **Concept**: Use a stack to track open brackets. Pop when a matching close bracket is found.
- **Problems**:
    - Valid Parentheses
    - Longest Valid Parentheses
    - Simplify Path
    - Decode String
    - Asteroid Collision

### 2. Monotonic Stack
- **Concept**: Maintain elements in the stack such that they are always increasing (or decreasing). This helps find the "Next Greater Element" or "Previous Smaller Element" in O(n).
- **Problems**:
    - Next Greater Element I / II
    - Daily Temperatures
    - Largest Rectangle in Histogram
    - Sum of Subarray Minimums

### 3. Expression Evaluation
- **Concept**: Use stack to handle precedence and nesting in math expressions.
- **Problems**:
    - Basic Calculator II
    - Evaluate Reverse Polish Notation

### 4. Min Stack
- **Concept**: Design a stack that supports `getMin()` in O(1) time (often by using an auxiliary stack).
- **Problems**:
    - Min Stack
