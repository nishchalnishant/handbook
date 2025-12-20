# Binary Search 🔢

## Description
Binary Search is an efficient algorithm for finding an item from a sorted list of items. It works by repeatedly dividing in half the portion of the list that could contain the item, until you've narrowed down the possible locations to just one. Time complexity is O(log n).

## Strategies

### 1. Standard Binary Search
- **Concept**: Classic implementation to find a target in a sorted array `nums`.
- **Use Case**: Simple lookups.
- **Problems**:
    - Binary Search
    - Search Insert Position
    - Peak Index in a Mountain Array

### 2. Binary Search on Answer
- **Concept**: Instead of searching an array, we search for the "Answer" within a range [min, max]. If value `x` is valid, we try a larger/smaller value to find the optimal boundary.
- **Use Case**: Problems asking for "Minimum capacity to...", "Kth smallest...", "Split array largest sum".
- **Problems**:
    - Capacity To Ship Packages Within D Days
    - Koko Eating Bananas
    - Split Array Largest Sum

### 3. Rotated Sorted Array
- **Concept**: The array is sorted but rotated at some pivot. One half is always sorted. Determine which half is sorted to decide where to search.
- **Problems**:
    - Search in Rotated Sorted Array
    - Find Minimum in Rotated Sorted Array
    - Find Peak Element

### 4. Find First/Last Occurrence
- **Concept**: Modify the binary search condition to find boundaries of a target value.
- **Problems**:
    - Find First and Last Position of Element in Sorted Array

### 5. Matrix Binary Search
- **Concept**: Treat a 2D matrix as a sorted 1D array or utilise row/column sorting properties.
- **Problems**:
    - Search a 2D Matrix

### 6. Advanced
- **Problems**:
    - Median of Two Sorted Arrays
