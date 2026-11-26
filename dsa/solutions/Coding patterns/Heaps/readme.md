# Heaps (Priority Queue) ODEN

## Description
A Heap is a specialized tree-based data structure that satisfies the heap property. In a Min-Heap, the key at the root must be minimum among all keys present in the Binary Heap. (Max-Heap is the reverse). It is efficiently implemented as a Priority Queue.

## Strategies

### 1. Top 'K' Elements
- **Concept**: Use a Min-Heap of size K to keep track of the K largest elements. If a new element is larger than the root, replace root and heapify.
- **Use Case**: "Find the Kth largest...", "Top K frequent...".
- **Problems**:
    - Kth Largest Element in an Array
    - Top K Frequent Elements
    - Find K Pairs with Smallest Sums
    - K Closest Points to Origin
    - Sort Characters By Frequency

### 2. Merge 'K' Sorted Lists
- **Concept**: Push the first element of each list into a Min-Heap. Pop the smallest, and push the next element from exactly that list.
- **Problems**:
    - Merge k Sorted Lists

### 3. Two Heaps (Median Finder)
- **Concept**: Maintain a Max-Heap for the lower half of numbers and a Min-Heap for the upper half to find the median in O(1).
- **Problems**:
    - Find Median from Data Stream
    - Sliding Window Median

### 4. Greedy with Heap (Task Scheduling)
- **Concept**: Always process the most "expensive" or "frequent" task available to optimize cost/time.
- **Problems**:
    - Task Scheduler
    - Minimum Cost to Connect Sticks
    - Reorganize String
