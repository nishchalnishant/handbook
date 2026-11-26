"""
Sorting patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Using quicksort in interviews without knowing how to avoid worst-case O(n^2) (use randomized pivot).\n- Modifying the array while iterating over it.\n- Custom comparators in Python 3 require `functools.cmp_to_key`.

Common Variants:
- Merge sort (good for linked lists or counting inversions)\n- Quick select (finding kth element in O(n) average time)\n- Cyclic sort (when numbers are 1 to N)

General Tips & Best Practices:
- Python's `list.sort()` is Timsort, which is stable and O(n log n).\n- If numbers are small and bounded, consider Counting Sort or Bucket Sort.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

import random
import math
from typing import List

class SortingSolutions:
    # -----------------------------------------------------------------------
    # 1. Sort Colors (Dutch National Flag) (LC 75) — T1
    # Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue. We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.
    # Example: nums = [2,0,2,1,1,0] → [0,0,1,1,2,2]
    # Constraints: n == nums.length, 1 <= n <= 300
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def sortColors(self, nums: List[int]) -> None:
        # l is the boundary for 0s, r is the boundary for 2s.
        l, r = 0, len(nums) - 1
        # i is the current element index.
        i = 0
        # Iterate until the current pointer crosses the right boundary.
        while i <= r:
            # If current element is 0, swap with left boundary and advance both pointers.
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l]
                l += 1
                i += 1
            # If current element is 2, swap with right boundary and decrement right pointer (do not advance i).
            elif nums[i] == 2:
                nums[i], nums[r] = nums[r], nums[i]
                r -= 1
            # If current element is 1, it's already in the correct place, just advance i.
            else:
                i += 1

    # -----------------------------------------------------------------------
    # 2. Kth Largest Element in Array (LC 215) — T1
    # Given an integer array nums and an integer k, return the kth largest element in the array. Note that it is the kth largest element in the sorted order, not the kth distinct element.
    # Example: nums = [3,2,1,5,6,4], k = 2 → 5
    # Constraints: 1 <= k <= nums.length <= 10^5, we can create a heap of length k and then insert in that heap, that would take O(nlog(k))
    # Time: O(n) avg, Space: O(n)
    # -----------------------------------------------------------------------
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Convert kth largest index to equivalent 0-indexed position from left.
        k = len(nums) - k
        def quickSelect(l, r):
            # Choose the rightmost element as pivot, and set partition index p to l.
            pivot, p = nums[r], l
            # Move all elements smaller than or equal to pivot to the left of p.
            for i in range(l, r):
                if nums[i] <= pivot:
                    nums[p], nums[i] = nums[i], nums[p]
                    p += 1
            # Swap pivot to its correct sorted position p.
            nums[p], nums[r] = nums[r], nums[p]
            # Recursively select in the left partition if pivot index is greater than target.
            if p > k: return quickSelect(l, p - 1)
            # Recursively select in the right partition if pivot index is smaller than target.
            elif p < k: return quickSelect(p + 1, r)
            # Target element found at partition index.
            else: return nums[p]
        return quickSelect(0, len(nums) - 1)

    # -----------------------------------------------------------------------
    # 3. Largest Number (LC 179) — T2
    # Given a list of non-negative integers nums, arrange them such that they form the largest number and return it. Since the result may be very large, so you need to return a string instead of an integer.
    # Example: nums = [10,2] → "210"
    # Constraints: 1 <= nums.length <= 100, 0 <= nums[i] <= 10^9, Instead of asking "Is A greater than B?", we ask: "Does putting A before B make a larger combined string than putting B before A?"
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def largestNumber(self, nums: List[int]) -> str:
        from functools import cmp_to_key
        # Convert each number to its string representation.
        for i, n in enumerate(nums):
            nums[i] = str(n)

        # Custom comparison logic: order pairs by which concatenation is lexicographically larger.
        def compare(n1, n2):
            """Comparator helper used to order candidate values."""
            if n1 + n2 > n2 + n1: return -1
            else: return 1

        # Sort values using the custom key.
        nums = sorted(nums, key=cmp_to_key(compare))
        # Concatenate sorted strings and convert to int then str to remove leading zeros.
        return str(int("".join(nums)))


    # -----------------------------------------------------------------------
    # 5. Maximum Gap (LC 164) — T2
    # Given an integer array nums, return the maximum difference between two successive elements in its sorted form. If the array contains less than two elements, return 0. You must write an algorithm that runs in linear time and uses linear extra space.
    # Example: nums = [3,6,9,1] → 3
    # Constraints: 1 <= nums.length <= 10^5, 0 <= nums[i] <= 10^9
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def maximumGap(self, nums: List[int]) -> int:
        # If array has less than two elements, the gap is 0.
        if len(nums) < 2: return 0
        mi, ma = min(nums), max(nums)
        # If min equals max, all elements are identical, gap is 0.
        if mi == ma: return 0

        n = len(nums)
        # Compute the minimum possible maximum gap based on Pigeonhole Principle.
        gap = math.ceil((ma - mi) / (n - 1))
        min_bucket = [float("inf")] * n
        max_bucket = [float("-inf")] * n

        # Distribute numbers into buckets.
        for num in nums:
            b = (num - mi) // gap
            min_bucket[b] = min(min_bucket[b], num)
            max_bucket[b] = max(max_bucket[b], num)

        res = 0
        prev_max = min_bucket[0]
        # Calculate gaps between adjacent non-empty buckets.
        for i in range(1, n):
            # Skip empty buckets.
            if min_bucket[i] == float("inf"):
                continue
            # Gap is the difference between current bucket's minimum and previous bucket's maximum.
            res = max(res, min_bucket[i] - prev_max)
            prev_max = max_bucket[i]
        return res

    # -----------------------------------------------------------------------
    # 6. H-Index (T2) — Sort descending, find largest i where citations[i] >= i+1
    # Given an array of integers citations where citations[i] is the number of citations a researcher received for their ith paper, return the researcher's h-index.
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def hIndex(self, citations: List[int]) -> int:
        # Sort citations in descending order.
        citations.sort(reverse=True)
        h = 0
        # Check papers from most to least cited.
        for i, c in enumerate(citations):
            # If the current paper has at least i + 1 citations, update h-index.
            if c >= i + 1:
                h = i + 1
            # Otherwise, stop early.
            else:
                break
        return h

    # -----------------------------------------------------------------------
    # 7. 3Sum Closest (T2) — Sort + converging two pointers, track min abs diff
    # Given an integer array nums of length n and an integer target, find three integers in nums such that the sum is closest to target. Return the sum of the three integers.
    # Example: nums = [-1,2,1,-4], target = 1 → 2
    # Constraints: 3 <= nums.length <= 500
    # Time: O(n^2), Space: O(1)
    # -----------------------------------------------------------------------
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        # Sort the array to enable two pointers.
        nums.sort()
        # Initialize the closest sum with the first three elements.
        res = sum(nums[:3])
        # Fix the first element.
        for i in range(len(nums) - 2):
            l, r = i + 1, len(nums) - 1
            # Move two pointers towards each other.
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                # Update closest sum if current sum is closer to target.
                if abs(s - target) < abs(res - target):
                    res = s
                # Adjust pointers based on current sum.
                if s < target:
                    l += 1
                elif s > target:
                    r -= 1
                # If exact target sum is found, return immediately.
                else:
                    return res
        return res

    # -----------------------------------------------------------------------
    # 8. Merge Sort (Sort classic) — T2
    # Given an array of integers nums, sort the array in ascending order and return it. You must solve the problem without using any built-in functions in O(nlog(n)) time complexity and with the smallest space complexity possible.
    # Example: nums = [5,2,3,1] → [1,2,3,5]
    # Constraints: 1 <= nums.length <= 5 * 10^4
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def mergeSort(self, nums: List[int]) -> List[int]:
        # Base case: array of length 0 or 1 is already sorted.
        if len(nums) <= 1:
            return nums

        # Split the array at the midpoint.
        mid = len(nums) // 2
        # Recursively sort left and right halves.
        left = self.mergeSort(nums[:mid])
        right = self.mergeSort(nums[mid:])

        # Merge the sorted halves back together.
        return self.merge(left, right)

    def merge(self, left: List[int], right: List[int]) -> List[int]:
        res = []
        i = j = 0

        # Linear scan using two pointers to merge sorted halves.
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                j += 1

        # Append any remaining elements.
        res.extend(left[i:])
        res.extend(right[j:])
        return res

    # -----------------------------------------------------------------------
    # 9. Quick Sort (Sort classic) — T2
    # Given an array of integers nums, sort the array in ascending order using the Quick Sort algorithm.
    # Example: nums = [5,2,3,1] → [1,2,3,5]
    # Constraints: 1 <= nums.length <= 5 * 10^4
    # Time: O(n log n) avg, Space: O(log n)
    # -----------------------------------------------------------------------
    def quickSort(self, nums: List[int]) -> List[int]:
        # Recursive quicksort implementation.
        def sort(low, high):
            """Sorts the current range or collection for the enclosing algorithm."""
            if low < high:
                # Partition the subarray and get the pivot index.
                pivot_idx = partition(low, high)
                # Recursively sort left and right partitions.
                sort(low, pivot_idx - 1)
                sort(pivot_idx + 1, high)

        # Lomuto partition scheme: uses rightmost element as pivot.
        def partition(low, high):
            """Partitions the current range around a pivot or boundary condition."""
            pivot = nums[high]
            # i tracks the boundary of elements smaller than pivot.
            i = low - 1

            for j in range(low, high):
                # If current element is smaller than pivot, move it to left side.
                if nums[j] < pivot:
                    i += 1
                    nums[i], nums[j] = nums[j], nums[i]

            # Place pivot in its final correct sorted position.
            nums[i + 1], nums[high] = nums[high], nums[i + 1]
            return i + 1

        sort(0, len(nums) - 1)
        return nums

    # -----------------------------------------------------------------------
    # 12. Pancake Sorting (LC 969) — T2
    # Given an array of integers arr, sort the array by performing a series of pancake flips. In one pancake flip we do the following steps: For example, if arr = [3,2,1,4] and we performed a pancake flip choosing k = 3, we reverse the sub- array [3,2,1], so arr = [1,2,3,4] after the pancake flip at k = 3. Return an array of the k-values corresponding to a sequence of pancake flips that sort arr. Any valid answer that sorts the array within 10 * arr.length flips will be judged as correct.
    # Example: arr = [3,2,4,1] → [4,2,4,3]
    # Constraints: 1 <= arr.length <= 100, 1 <= arr[i] <= arr.length, All integers in arr are unique (i.e. arr is a permutation of the integers from 1 to arr.length)
    # Time: O(n^2), Space: O(n)
    # -----------------------------------------------------------------------
    def pancakeSort(self, arr: List[int]) -> List[int]:
        res = []
        # Iterate from the largest target value (len(arr)) down to 2 (1 is implicitly in place at the end).
        for x in range(len(arr), 1, -1):
            # Find the current 0-based index of value x in the array.
            i = arr.index(x)
            # Record the flip lengths: (i + 1) to flip target to index 0, and x to flip it to its correct sorted position.
            res.extend([i + 1, x])
            # Reconstruct the array to simulate the two flips:
            # 1. Flip at (i + 1) reverses the first i + 1 elements, putting x at index 0.
            # 2. Flip at x reverses the first x elements, putting x at its final sorted position at index x - 1.
            # arr[:i:-1] takes the suffix after index i and reverses it, which combined with arr[:i] simulates the net action of both flips.
            arr = arr[:i:-1] + arr[:i]
        return res

    # -----------------------------------------------------------------------
    # 13. Sort Transformed Array (LC 360) — T2
    # Given a sorted integer array nums and three integers a, b and c, apply a quadratic function of the form f(x) = ax^2 + bx + c to each element nums[i] in the array, and return the array in a sorted order.
    # Example: nums = [-4,-2,2,4], a = 1, b = 3, c = 5 → [3,9,15,33]
    # Constraints: 1 <= nums.length <= 200
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def sortTransformedArray(self, nums: List[int], a: int, b: int, c: int) -> List[int]:
        # Pre-allocate output list of the same length.
        res = [0] * len(nums)
        # Two pointers pointing to the boundaries of the sorted input nums.
        l, r = 0, len(nums) - 1
        # Set the write index and direction based on the sign of a (parabola opening direction).
        idx = len(nums) - 1 if a >= 0 else 0
        while l <= r:
            # Apply f(x) = a*x^2 + b*x + c to elements at both pointers.
            l_val, r_val = a*nums[l]*nums[l] + b*nums[l] + c, a*nums[r]*nums[r] + b*nums[r] + c
            if a >= 0:
                # If a >= 0, largest values are at the extremes, so we fill from right to left.
                if l_val >= r_val:
                    res[idx] = l_val
                    l += 1
                else:
                    res[idx] = r_val
                    r -= 1
                # Move write index leftwards.
                idx -= 1
            else:
                # If a < 0, smallest values are at the extremes, so we fill from left to right.
                if l_val <= r_val:
                    res[idx] = l_val
                    l += 1
                else:
                    res[idx] = r_val
                    r -= 1
                # Move write index rightwards.
                idx += 1
        return res

    # -----------------------------------------------------------------------
    # 15. Sort Characters By Frequency (LC 451) — T2
    # Given a string s, sort it in decreasing order based on the frequency of the characters. The frequency of a character is the number of times it appears in the string. Return the sorted string. If there are multiple answers, return any of them.
    # Example: s = "tree" → "eert"
    # Constraints: 1 <= s.length <= 5 * 10^5, s consists of uppercase and lowercase English letters and digits
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def frequencySort(self, s: str) -> str:
        from collections import Counter
        # Count frequency of each character.
        count = Counter(s)
        # Create buckets where the index represents frequency (0 to len(s)).
        buckets = [[] for _ in range(len(s) + 1)]
        for char, freq in count.items():
            # Group characters by their frequency count.
            buckets[freq].append(char)

        res = []
        # Iterate from the highest frequency bucket down to 1.
        for i in range(len(buckets) - 1, 0, -1):
            # Append each character repeated by its frequency to build the sorted runs.
            for char in buckets[i]:
                res.append(char * i)
        # Concatenate and return the sorted string.
        return "".join(res)

    # -----------------------------------------------------------------------
    # 16. Custom Sort String (LC 791) — T2
    # You are given two strings order and s. All the characters of order are unique and were sorted in some custom order previously. Permute the characters of s so that they match the order that order was sorted. More specifically, if a character x occurs before a character y in order, then x should occur before y in the permuted string. Return any permutation of s that satisfies this property.
    # Example: order = "cba", s = "abcd" → "cbad"
    # Constraints: 1 <= order.length <= 26, 1 <= s.length <= 200, order and s consist of lowercase English letters, All the characters of order are unique
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def customSortString(self, order: str, s: str) -> str:
        from collections import Counter
        # Count frequency of each character in the input string s.
        count = Counter(s)
        res = []
        # Append characters according to order and delete processed keys.
        for char in order:
            if char in count:
                res.append(char * count[char])
                del count[char]
        # Append the remaining characters that were not in order (in any order).
        for char, freq in count.items():
            res.append(char * freq)
        # Form and return the custom-sorted string.
        return "".join(res)

    # -----------------------------------------------------------------------
    # 17. Queue Reconstruction by Height (LC 406) — T2
    # You are given an array of people, people, which are the attributes of some people in a queue (not necessarily in order). Each people[i] = [hi, ki] represents the i^th person of height hi with exactly ki other people in front who have a height greater than or equal to hi. Reconstruct and return the queue that is represented by the input array people. The returned queue should be formatted as an array queue, where queue[j] = [hj, kj] is the attributes of the j^th person in the queue (queue[0] is the person at the front of the queue).
    # Example: people = [[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]] → [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]
    # Constraints: 1 <= people.length <= 2000, 0 <= hi <= 10^6, 0 <= ki < people.length, It is guaranteed that the queue can be reconstructed
    # Time: O(n^2), Space: O(n)
    # -----------------------------------------------------------------------
    def reconstructQueue(self, people: List[List[int]]) -> List[List[int]]:
        # Sort by height descending, and then by k ascending.
        people.sort(key=lambda x: (-x[0], x[1]))
        res = []
        # Insert each person at index p[1] (k) in the result list.
        # Since taller elements are placed first, the insert position matches the exact number of taller/equal people in front.
        for p in people:
            res.insert(p[1], p)
        return res

    # -----------------------------------------------------------------------
    # 18. Wiggle Sort II — nth element + three-way partition (LC 324)
    # Given an integer array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]...
    # Example: nums = [1,5,1,1,6,4] → [1,6,1,5,1,4]
    # Time: O(n) avg, Space: O(1)
    # -----------------------------------------------------------------------
    def wiggleSort(self, nums: List[int]) -> None:
        n = len(nums)
        # Find median via sorted copy (acceptable for interview; O(n log n))
        mid = (n - 1) // 2
        median = sorted(nums)[mid]

        # Index-mapped DNF three-way partition mapping virtual index i to target array positions.
        A = lambda i: nums[(1 + 2 * i) % (n | 1)]

        # Setter helper for mapped indices.
        def set_A(i, val):
            nums[(1 + 2 * i) % (n | 1)] = val

        # Three-way partition pointers: lo writes elements > median, hi writes elements < median.
        lo, cur, hi = 0, 0, n - 1
        while cur <= hi:
            val = A(cur)
            if val > median:
                # Swap elements at lo and cur in mapped index space, advance both pointers.
                tmp = A(lo)
                set_A(lo, val)
                set_A(cur, tmp)
                lo += 1
                cur += 1
            elif val < median:
                # Swap elements at hi and cur in mapped index space, decrement high write pointer.
                tmp = A(hi)
                set_A(hi, val)
                set_A(cur, tmp)
                hi -= 1
            else:
                # Element is equal to median, keep it in the middle partition and advance.
                cur += 1

    # -----------------------------------------------------------------------
    # 19. Sort an Array — heap sort implementation (LC 912)
    # Given an array of integers nums, sort the array in ascending order and return it. Must solve without built-in sort functions, O(n log n) time.
    # Example: nums = [5,2,3,1] → [1,2,3,5]
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def sortArray(self, nums: List[int]) -> List[int]:
        def heapify(arr, size, root):
            """Restores the heap property for the current subtree."""
            largest = root
            left = 2 * root + 1
            right = 2 * root + 2
            # Check if left child exists and is greater than current largest.
            if left < size and arr[left] > arr[largest]:
                largest = left
            # Check if right child exists and is greater than current largest.
            if right < size and arr[right] > arr[largest]:
                largest = right
            # If the largest is not the root, swap and recursively heapify the affected sub-tree.
            if largest != root:
                arr[root], arr[largest] = arr[largest], arr[root]
                heapify(arr, size, largest)

        n = len(nums)
        # Build a max-heap in-place from the bottom up (starting from the last non-leaf node).
        for i in range(n // 2 - 1, -1, -1):
            heapify(nums, n, i)
        # One by one extract elements from the heap.
        for i in range(n - 1, 0, -1):
            # Swap the root (maximum element) with the last element of the unsorted heap.
            nums[0], nums[i] = nums[i], nums[0]
            # Call heapify on the reduced heap to restore the max-heap property.
            heapify(nums, i, 0)
        return nums

    # -----------------------------------------------------------------------
    # 24. Smallest Value After Replacing With Sum of Prime Factors (LC 2507)
    # Given a positive integer n, continuously replace n with the sum of its prime factors (with repetition) until n does not change. Return the smallest value n will take on.
    # Example: n = 15 → 5  (15 -> 3+5=8 -> 2+2+2=6 -> 2+3=5 -> 5, stable)
    # Time: O(sqrt(n) * iterations), Space: O(1)
    # -----------------------------------------------------------------------
    def smallestValue(self, n: int) -> int:
        # Helper to compute the sum of prime factors with multiplicity.
        def prime_factor_sum(x):
            s = 0
            i = 2
            # Trial division up to square root of x.
            while i * i <= x:
                # Add i to sum as long as it divides x.
                while x % i == 0:
                    s += i
                    x //= i
                i += 1
            # If the remaining x is greater than 1, then it must be prime.
            if x > 1:
                s += x
            return s

        # Repeat the replacement until a stable fixed point is reached.
        while True:
            nxt = prime_factor_sum(n)
            if nxt == n:
                return n
            n = nxt

    # -----------------------------------------------------------------------
    # 27. Maximum Number of Events That Can Be Attended (LC 1353) — greedy + heap Given an array of events where events[i] = [startDay, endDay], attend at most one event per day. Return the maximum number of events you can attend.
    # Example: events = [[1,2],[2,3],[3,4]] → 3
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def maxEvents(self, events: List[List[int]]) -> int:
        import heapq
        # Sort events by their start days.
        events.sort()
        heap = []  # min-heap of end days
        i = 0
        n = len(events)
        attended = 0
        # Initialize the current day to the start day of the first event.
        day = events[0][0]

        while i < n or heap:
            # Push all events starting on or before the current day onto the min-heap.
            while i < n and events[i][0] <= day:
                heapq.heappush(heap, events[i][1])
                i += 1
            # Discard any events from the heap that have already ended before the current day.
            while heap and heap[0] < day:
                heapq.heappop(heap)
            # Attend the available event with the earliest end day.
            if heap:
                heapq.heappop(heap)
                attended += 1
                day += 1
            # If no events are currently available, jump to the next event's start day.
            elif i < n:
                day = events[i][0]

        return attended

if __name__ == "__main__":
    sol = SortingSolutions()

    # sortColors
    arr = [2, 0, 2, 1, 1, 0]
    sol.sortColors(arr)
    assert arr == [0, 0, 1, 1, 2, 2]

    # findKthLargest (quickselect)
    assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert sol.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # largestNumber
    assert sol.largestNumber([10, 2]) == "210"
    assert sol.largestNumber([3, 30, 34, 5, 9]) == "9534330"
    assert sol.largestNumber([0, 0]) == "0"

    # hIndex
    assert sol.hIndex([3, 0, 6, 1, 5]) == 3
    assert sol.hIndex([1, 3, 1]) == 1

    # threeSumClosest
    assert sol.threeSumClosest([-1, 2, 1, -4], 1) == 2
    assert sol.threeSumClosest([0, 0, 0], 1) == 0

    # mergeSort
    assert sol.mergeSort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    assert sol.mergeSort([]) == []

    # quickSort
    assert sol.quickSort([3, 6, 8, 10, 1, 2, 1]) == [1, 1, 2, 3, 6, 8, 10]

    # frequencySort
    assert sol.frequencySort("tree") in ["eert", "eetr"]
    assert sol.frequencySort("cccaaa") in ["cccaaa", "aaaccc"]

    # customSortString
    assert sol.customSortString("cba", "abcd") == "cbad"

    # reconstructQueue
    res = sol.reconstructQueue([[7,0],[4,4],[7,1],[5,0],[6,1],[5,2]])
    assert res == [[5,0],[7,0],[5,2],[6,1],[4,4],[7,1]]

    # wiggleSort (LC 324)
    arr = [1, 5, 1, 1, 6, 4]
    sol.wiggleSort(arr)
    for k in range(1, len(arr)):
        if k % 2 == 1:
            assert arr[k - 1] < arr[k], f"wiggleSort failed at index {k}: {arr}"
        else:
            assert arr[k - 1] > arr[k], f"wiggleSort failed at index {k}: {arr}"
    arr2 = [1, 3, 2, 2, 3, 1]
    sol.wiggleSort(arr2)
    for k in range(1, len(arr2)):
        if k % 2 == 1:
            assert arr2[k - 1] < arr2[k], f"wiggleSort failed at index {k}: {arr2}"
        else:
            assert arr2[k - 1] > arr2[k], f"wiggleSort failed at index {k}: {arr2}"

    # findKthLargest already tested above (quickselect)

    # sortArray (heap sort, LC 912)
    assert sol.sortArray([5, 2, 3, 1]) == [1, 2, 3, 5]
    assert sol.sortArray([5, 1, 1, 2, 0, 0]) == [0, 0, 1, 1, 2, 5]

    # smallestValue (LC 2507)
    assert sol.smallestValue(15) == 5
    assert sol.smallestValue(4) == 4
    assert sol.smallestValue(7) == 7

    # maxEvents (LC 1353)
    assert sol.maxEvents([[1,2],[2,3],[3,4]]) == 3
    assert sol.maxEvents([[1,2],[2,3],[3,4],[1,2]]) == 4
    assert sol.maxEvents([[1,4],[4,4],[2,2],[3,4],[1,1]]) == 4

    print("All sorting tests passed.")
