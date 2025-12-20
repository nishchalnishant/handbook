# Two Pointers Overview 👉👈

Two pointers pattern involves using two pointers to iterate through a data structure (usually an array or string) to solve problems efficiently, often reducing O(n^2) to O(n).

## Concepts
- **Opposite Direction**: One from start, one from end (e.g., Palindrome, Two Sum Sorted).
- **Same Direction**: Fast and Slow pointers (e.g., Cycle Detection, Remove Duplicates).

---

## Problems & Solutions

### Easy
1. **[Two Sum II - Input Array Is Sorted](Easy/two_sum_sorted.py)**
   - Find two numbers that add up to target.
2. **[Valid Palindrome](../8.%20String/Easy/valid_palindrome.py)**
   - Check if string is palindrome.
3. **[Remove Duplicates](Easy/remove_duplicates.py)**
   - Remove duplicates from sorted array.

### Medium
1. **[Container With Most Water](Medium/container_most_water.py)**
   - Maximize area between two lines.
2. **[3Sum](Medium/3sum.py)**
   - Find triplets summing to zero.

### Hard
1. **[Trapping Rain Water](Hard/trapping_rain_water.py)**
   - Two pointer approach (O(1) space).

---

## Tips for Interviews
- **Sorted Input**: Hints at Two Pointers or Binary Search.
- **In-Place**: Often used to satisfy O(1) space constraints.
