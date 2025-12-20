# Heap (Priority Queue) Overview

A Heap is a specialized tree-based data structure (usually a complete binary tree) that satisfies the heap property.

## Topics Covered

### 1. Types
- **Max-Heap**: Parent >= Children. Root is Max.
- **Min-Heap**: Parent <= Children. Root is Min.

### 2. Operations
- **Push (Insert)**: Add to end, bubble up. O(log n).
- **Pop (Extract)**: Remove root, move last to root, bubble down. O(log n).
- **Peek**: See root. O(1).
- **Heapify**: Build heap from array. O(n).

---

## Problems & Solutions

### Medium
1. **[Kth Largest Element in an Array](Medium/kth_largest.py)**
   - Find kth largest value (Min-Heap of size k).
2. **[Top K Frequent Elements](Medium/top_k_frequent.py)**
   - Find k most frequent items.
3. **[K Closest Points to Origin](Medium/k_closest.py)**
   - Find points closest to (0,0).
4. **[Task Scheduler](Medium/task_scheduler.py)**
   - Schedule tasks with cooldowns (Max-Heap).

### Hard
1. **[Merge k Sorted Lists](Hard/merge_k_lists.py)**
   - Merge k sorted lists (Min-Heap).
2. **[Find Median from Data Stream](Hard/find_median.py)**
   - Maintain median using two heaps (Min & Max).

---

## Tips for Interviews
- **Top K**: Use a Heap. Min-Heap for Kth Largest, Max-Heap for Kth Smallest.
- **Merge**: Use Min-Heap to efficient merge multiple sorted streams.
- **Python**: `heapq` implements a **Min-Heap**. For Max-Heap, insert elements inverted (`-val`).