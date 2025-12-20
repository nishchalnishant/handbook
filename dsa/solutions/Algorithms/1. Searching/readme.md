# Searching Overview 🔍

Searching algorithms retrieve elements from data structures. Efficiency depends on data organization (e.g., sorted vs. unsorted).

## Topics Covered

### 1. Linear Search
- **Unsorted Data**: Check each element sequentially. O(n).

### 2. Binary Search
- **Sorted Data**: Divide search space in half. O(log n).
- **Variants**: Lower Bound, Upper Bound, Answer Search.

### 3. Other Algorithms
- **Ternary Search**: For unimodal functions. O(log_3 n).
- **Exponential Search**: For unbounded arrays.
- **Interpolation Search**: For uniformly distributed data. O(log log n).

---

## Problems & Solutions

### Easy
1. **[Binary Search](Easy/binary_search.py)**
   - Standard implementation.
2. **[Linear Search](Easy/linear_search.py)**
   - Basic sequential search.
3. **[Sqrt(x)](Easy/sqrt_x.py)**
   - Compute square root using binary search.
4. **[First and Last Position](Easy/first_last_pos.py)**
   - Find start and end indices of target.

### Medium
1. **[Search in Rotated Sorted Array](Medium/search_rotated.py)**
   - Find target in rotated array.
2. **[Find Peak Element](Medium/find_peak.py)**
   - Find element greater than neighbors.
3. **[Single Element in Sorted Array](Medium/single_element.py)**
   - Find unique element (others appear twice).
4. **[Search in 2D Matrix](Medium/search_2d_matrix.py)**
   - Search in sorted matrix.

### Hard
1. **[Median of Two Sorted Arrays](Hard/median_sorted_arrays.py)**
   - Find median of merged arrays in O(log(m+n)).
2. **[Aggressive Cows](Hard/aggressive_cows.py)**
   - Allocate stalls to maximize minimum distance (Answer Search).

---

## Tips for Interviews
- **Sorted?**: Think **Binary Search**.
- **Infinite/Unbounded?**: Think **Exponential Search**.
- **Optimization?**: Think **Binary Search on Answer**.