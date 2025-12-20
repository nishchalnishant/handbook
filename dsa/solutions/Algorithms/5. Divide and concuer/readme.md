# Divide and Conquer Overview ⚔️

Break problems into subproblems, solve them, and combine results.

## Concepts
- **Recurrence Relations**: T(n) = aT(n/b) + f(n).
- **Master Theorem**: Solving recurrences.

---

## Problems & Solutions

### Medium
1. **[Merge Sort](../2.%20Sorting/Medium/merge_sort.py)**
   - Classic D&C Sorting.
2. **[Maximum Subarray](Medium/max_subarray.py)**
   - O(n log n) D&C approach (vs O(n) Kadane).
3. **[Pow(x, n)](Medium/pow_x_n.py)**
   - Fast Exponentiation (Binary Exponentiation).
4. **[Majority Element](Medium/majority_element.py)**
   - D&C approach to find element appearing > n/2 times.

### Hard
1. **[Count Inversions](../2.%20Sorting/Hard/count_inversions.py)**
   - Using Merge Sort.
2. **[Closest Pair of Points](Hard/closest_pair.py)**
   - Find closest pair in O(n log n).

---

## Tips for Interviews
- **Master Theorem**: Know it to analyze complexity.
- **Overhead**: Recursion has overhead; small inputs might be better with iterative/brute-force.
