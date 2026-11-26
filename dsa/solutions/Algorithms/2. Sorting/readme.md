# Sorting Overview

Sorting arranges elements in specific order (ascending/descending).

## Topics Covered

### 1. Basic Sorts (O(n^2))
- **Bubble Sort**: Repeated swaps.
- **Insertion Sort**: Build sorted array one by one.
- **Selection Sort**: Pick minimum and place at sorted position.

### 2. Efficient Sorts (O(n log n))
- **Merge Sort**: Divide and Conquer (Stable).
- **Quick Sort**: Partitioning (Unstable, In-place).
- **Heap Sort**: Binary Heap (Unstable, In-place).

### 3. Linear Sorts (O(n))
- **Counting Sort**, **Radix Sort**, **Bucket Sort**.

---

## Problems & Solutions

### Easy
1. **[Bubble Sort](Easy/bubble_sort.py)**
   - Basic implementation.
2. **[Insertion Sort](Easy/insertion_sort.py)**
   - Efficient for small/nearly sorted data.
3. **[Selection Sort](Easy/selection_sort.py)**
   - Minimize swaps.

### Medium
1. **[Merge Sort](Medium/merge_sort.py)**
   - Stable divide and conquer.
2. **[Quick Sort](Medium/quick_sort.py)**
   - Fast average case.
3. **[Heap Sort](Medium/heap_sort.py)**
   - Space efficient O(n log n).
4. **[Kth Largest Element](Medium/kth_largest.py)**
   - Using Quick Select (or Heap).
5. **[Sort Colors](Medium/sort_colors.py)**
   - Dutch National Flag problem (0s, 1s, 2s).

### Hard
1. **[Count Inversions](Hard/count_inversions.py)**
   - Using Merge Sort.
2. **[Maximum Gap](Hard/maximum_gap.py)**
   - Linear time sort (Radix/Bucket) required.

---

## Tips for Interviews
- **Stability**: Merge Sort is stable. Quick Sort is not.
- **In-Place**: Quick Sort, Heap Sort.
- **Worst Case**: Quick Sort is O(n^2) (avoid with random pivot). Merge/Heap are O(n log n).
