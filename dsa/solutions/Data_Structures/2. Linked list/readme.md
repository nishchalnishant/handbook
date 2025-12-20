# Linked Lists Overview

A Linked List is a linear data structure where elements (nodes) are not stored in contiguous memory locations but are linked using pointers. This allows for dynamic memory allocation and efficient insertion/deletion.

## Topics Covered

### 1. Introduction
- **Structure**: Each node contains `Data` and a `Pointer` to the next node.
- **Types**:
    - **Singly**: Unidirectional (Head -> Tail -> NULL).
    - **Doubly**: Bidirectional (Prev <-> Next).
    - **Circular**: Last node connects back to the first.

### 2. Common Techniques
- **Fast & Slow Pointers (Tortoise and Hare)**: Detect cycles, find middle, remove nth from end.
- **Dummy Node**: Simplifies edge cases at the head (e.g., merging, removing).
- **Reversal**: Iterative or recursive pointer manipulation.

---

## Problems & Solutions

### Easy
1. **[Reverse Linked List](Easy/reverse_list.py)**
   - Reverse a singly linked list.
2. **[Middle of the Linked List](Easy/middle_node.py)**
   - Find the middle node (Fast & Slow pointers).
3. **[Detect Cycle](Easy/detect_cycle.py)**
   - Determine if the list has a cycle.
4. **[Remove Duplicates from Sorted List](Easy/remove_duplicates.py)**
   - Delete duplicates such that each element appears only once.
5. **[Merge Two Sorted Lists](Easy/merge_sorted_lists.py)**
   - Merge two sorted lists into one sorted list.
6. **[Palindrome Linked List](Easy/palindrome_linked_list.py)**
   - Check if the list is a palindrome (O(n) time, O(1) space).

### Medium
1. **[Add Two Numbers](Medium/add_two_numbers.py)**
   - Add two numbers represented by linked lists.
2. **[Remove Nth Node From End](Medium/remove_nth_node.py)**
   - Remove the nth node from the end of the list.
3. **[Intersection of Two Lists](Medium/intersection_node.py)**
   - Find the node where two lists intersect.
4. **[Sort List](Medium/sort_list.py)**
   - Sort a linked list in O(n log n) time (Merge Sort).

### Hard
1. **[Merge k Sorted Lists](Hard/merge_k_lists.py)**
   - Merge k sorted linked lists (Heap approach).
2. **[Reverse Nodes in k-Group](Hard/reverse_k_group.py)**
   - Reverse nodes of the list k at a time.

---

## Tips for Interviews
- **Visualizing**: Always draw pointers to understand how they change during insertion/deletion.
- **Two Pointers**: Extremely powerful for tracking different positions (middle, end, cycle) simultaneously.
- **Edge Cases**:
  - Empty list or single node.
  - Cycle detection (infinite loops).
  - Updating the `head` pointer.
