# Sliding Window 🪟

## Description
The Sliding Window pattern is used to find a subarray or substring that satisfies a specific condition, optimizing the time complexity by maintaining a window of elements. Instead of recomputing the entire window, you "slide" it by adding a new element and removing the old one.

## Strategies

### 1. Fixed Size Window
- **Concept**: The window size `k` is constant. You slide the window one element at a time, calculating the metric (sum, average, max) for each step.
- **Use Case**: Calculating metrics over all subarrays of size `k`.
- **Problems**:
    - Max Sum Subarray of Size K
    - Permutation in String
    - Find All Anagrams in a String

### 2. Variable Size Window
- **Concept**: The window expands by moving the right pointer. If the window condition is violated (e.g., sum > target), the left pointer shrinks the window until the condition is valid again.
- **Use Case**: Finding the longest/shortest subarray satisfying a condition.
- **Problems**:
    - Longest Substring Without Repeating Characters
    - Minimum Window Substring
    - Longest Repeating Character Replacement
    - Minimum Size Subarray Sum
    - Fruit Into Baskets
    - Longest Substring with At Most K Distinct Characters
    - Subarrays with K Different Integers

### 3. Monotonic Queue Window
- **Concept**: Use a Deque (Double-ended queue) to maintain elements in increasing or decreasing order within the window window to allow O(1) access to max/min.
- **Use Case**: Finding maximum or minimum in a sliding window efficiently.
- **Problems**:
    - Sliding Window Maximum
