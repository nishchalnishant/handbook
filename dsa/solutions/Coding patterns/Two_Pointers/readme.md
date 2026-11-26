# Two Pointers 🎯

## Description
The Two Pointers pattern involves using two pointers to iterate through an array or list, often used to find pairs or elements that meet specific criteria. This technique is particularly useful for sorted arrays or lists where you need to find pairs that satisfy a specific condition, or when you need to reverse/modify parts of the structure in-place.

## Strategies

### 1. Converging Pointers (Sorted Array Target Sum)
- **Concept**: One pointer starts at the beginning/left and the other at the end/right. They move towards each other based on a condition (usually sum comparison).
- **Use Case**: Finding pairs/triplets in sorted arrays that sum to a target.
- **Problems**:
    - Container With Most Water
    - 3Sum
    - 3Sum Closest
    - 4Sum
    - Two Sum II - Input Array Is Sorted
    - Boats to Save People
    - Squares of a Sorted Array
    - 3Sum Smaller
    - Sort Colors

### 2. Fast & Slow Pointers (Cycle Detection)
- **Concept**: The "Tortoise and Hare" algorithm. One pointer moves one step at a time (slow), the other moves two steps (fast). If they meet, there is a cycle.
- **Use Case**: Cycle detection in linked lists or array-based sequences.
- **Problems**:
    - Linked List Cycle
    - Happy Number
    - Find the Duplicate Number

### 3. Fixed Separation
- **Concept**: Maintain a fixed distance between pointers (e.g., `k` steps apart) to find an element relative to the end of the list.
- **Use Case**: Finding the Nth node from the end.
- **Problems**:
    - Remove Nth Node From End of List

### 4. In-place Array Modification
- **Concept**: Use one pointer to iterate (read) and another to track the position for the next valid element (write).
- **Use Case**: Removing duplicates or specific elements without extra space.
- **Problems**:
    - Remove Duplicates from Sorted Array
    - Move Zeroes
    - Rotate Array

### 5. Expanding From Center
- **Concept**: Start from a center index (or between two indices) and expand outwards while characters match.
- **Use Case**: Palindrome search.
- **Problems**:
    - Longest Palindromic Substring
    - Valid Palindrome II
