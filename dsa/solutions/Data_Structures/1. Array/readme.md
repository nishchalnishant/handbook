# Arrays Overview 📊

Arrays are one of the most fundamental data structures, serving as a crucial building block for many algorithms. This section covers everything from basic operations to advanced techniques like searching, sorting, and dynamic arrays.

## Topics Covered

### 1. Introduction to Arrays
- **Definition**: A collection of elements stored in contiguous memory locations, allowing random access via index.
- **Key Concepts**:
    - Fixed vs. Dynamic size.
    - Index-based access (0-indexed).
    - Cache efficiency due to memory layout.
- **Complexity**:
    - Access: O(1)
    - Search: O(n) (Linear), O(log n) (Binary, if sorted)
    - Insertion/Deletion: O(n) (shifting required)

### 2. Common Techniques
- **Two Pointers**: For finding pairs, reversing, or merging.
- **Sliding Window**: For subarray problems (sums, counts).
- **Kadane’s Algorithm**: For maximum subarray sum (O(n)).
- **Prefix Sum**: For efficient range sum queries.
- **Sorting**: Simplifies many problems (e.g., 2Sum, 3Sum).

---

## Problems & Solutions

### Easy
1. **[Two Sum](Easy/two_sum.py)**
   - Find two numbers that add up to a target.
2. **[Maximum Subarray](Easy/maximum_subarray.py)**
   - Find the contiguous subarray with the largest sum (Kadane’s Algorithm).
3. **[Move Zeroes](Easy/move_zeroes.py)**
   - Move all 0s to the end while maintaining relative order of non-zero elements.

### Medium
1. **[Product of Array Except Self](Medium/product_of_array_except_self.py)**
   - Return an array where each valid `i` is the product of all elements except `nums[i]`.
2. **[Subarray Sum Equals K](Medium/subarray_sum_equals_k.py)**
   - Find total number of continuous subarrays whose sum equals `k`.
3. **[Merge Intervals](Medium/merge_intervals.py)**
   - Merge all overlapping intervals.
4. **[Find Minimum in Rotated Sorted Array](Medium/find_min_rotated.py)**
   - Find the minimum element in an array sorted then pivoted.

### Hard
1. **[Sliding Window Maximum](Hard/sliding_window_maximum.py)**
   - Find the max in each window of size `k` (Deque approach).

---

## Tips for Interviews
- **Edge Cases**: Empty array, single element, duplicates, all negative numbers.
- **In-Place**: Look for opportunities to swap elements or use the array itself for state storage to achieve O(1) space.
- **Sorting**: Check if sorting the array first (O(n log n)) simplifies the problem significantly compared to O(n^2).
