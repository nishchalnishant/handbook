"""
Binary Search patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Off-by-one errors: using `lo <= hi` but failing to do `lo = mid + 1` or `hi = mid - 1`.\n- Integer overflow on `mid = (lo + hi) // 2` (structurally good to know `lo + (hi - lo) // 2`).\n- Searching on the answer space: forgetting to check if the function is truly monotonic.

Common Variants:
- Standard element lookup in sorted array\n- Find first/last occurrence (lower_bound, upper_bound)\n- Search in rotated sorted array\n- Search on an implicit answer space (e.g., Koko eating bananas)

General Tips & Best Practices:
- Always test the case where the array has 1 or 2 elements.\n- Clearly define your search space (inclusive vs. exclusive bounds) and stick to one template.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
import math

class BinarySearchSolutions:
    # -----------------------------------------------------------------------
    # 1. Binary Search (LC 704) — T1
    # Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1. You must write an algorithm with O(log n) runtime complexity.
    # Example: nums = [-1,0,3,5,9,12], target = 9 → 4
    # Constraints: 1 <= nums.length <= 10^4, 10^4 < nums[i], target < 10^4, All the integers in nums are unique, nums is sorted in ascending order
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def search(self, nums: List[int], target: int) -> int:
        # Initialize left and right pointers covering the entire array.
        l, r = 0, len(nums) - 1
        while l <= r:
            # Find the midpoint of the current search interval.
            m = (l + r) // 2
            # If target is larger than mid element, search the right half.
            if nums[m] < target:
                l = m + 1
            # If target is smaller than mid element, search the left half.
            elif nums[m] > target:
                r = m - 1
            # Target found, return its index.
            else:
                return m
        # Target not found in the array.
        return -1

    # -----------------------------------------------------------------------
    # 2. Search in Rotated Sorted Array (LC 33) — T1
    # There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2]. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums. You must write an algorithm with O(log n) runtime complexity.
    # Example: nums = [4,5,6,7,0,1,2], target = 0 → 4
    # Constraints: 1 <= nums.length <= 5000, 10^4 <= nums[i] <= 10^4, All values of nums are unique, nums is an ascending array that is possibly rotated, 10^4 <= target <= 10^4
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def searchRotated(self, nums: List[int], target: int) -> int:
        # Initialize pointers at the array boundaries.
        l, r = 0, len(nums) - 1
        while l <= r:
            m = (l + r) // 2
            # Early return if target is at the midpoint.
            if nums[m] == target:
                return m
            # If left half is sorted.
            if nums[l] <= nums[m]:
                # If target is outside the sorted left half, search the right half.
                if target > nums[m] or target < nums[l]:
                    l = m + 1
                # Otherwise, target is in the sorted left half, search left.
                else:
                    r = m - 1
            # Otherwise, right half is sorted.
            else:
                # If target is outside the sorted right half, search the left half.
                if target < nums[m] or target > nums[r]:
                    r = m - 1
                # Otherwise, target is in the sorted right half, search right.
                else:
                    l = m + 1
        # Target not found.
        return -1

    # -----------------------------------------------------------------------
    # 3. Find Minimum in Rotated Sorted Array (LC 153) — T1
    # Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become: Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]]. Given the sorted rotated array nums of unique elements, return the minimum element of this array. You must write an algorithm that runs in O(log n) time.
    # Example: nums = [3,4,5,1,2] → 1
    # Constraints: n == nums.length, 1 <= n <= 5000, 5000 <= nums[i] <= 5000, All the integers of nums are unique, nums is sorted and rotated between 1 and n times
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def findMin(self, nums: List[int]) -> int:
        # Initialize the result with the first element as a candidate.
        res = nums[0]
        l, r = 0, len(nums) - 1
        while l <= r:
            # If the current subarray is already sorted, the first element is the min.
            if nums[l] < nums[r]:
                res = min(res, nums[l])
                break
            m = (l + r) // 2
            # Update the candidate minimum with the midpoint.
            res = min(res, nums[m])
            # If left half is sorted, the minimum/pivot must lie in the right half.
            if nums[m] >= nums[l]:
                l = m + 1
            # Otherwise, right half is sorted, the minimum is in the left half.
            else:
                r = m - 1
        return res

    # -----------------------------------------------------------------------
    # 4. Koko Eating Bananas (LC 875) — T1
    # Koko loves to eat bananas. There are n piles of bananas, the i^th pile has piles[i] bananas. The guards have gone and will come back in h hours. Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour. Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return. Return the minimum integer k such that she can eat all the bananas within h hours.
    # Example: piles = [3,6,7,11], h = 8 → 4
    # Constraints: 1 <= piles.length <= 10^4, piles.length <= h <= 10^9, 1 <= piles[i] <= 10^9
    # Time: O(n log m), Space: O(1)
    # -----------------------------------------------------------------------
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        # l is the minimum speed (1 banana/hr), r is the maximum possible speed.
        l, r = 1, max(piles)
        res = r
        while l <= r:
            k = (l + r) // 2
            # Compute total hours Koko takes to eat all piles at speed k.
            hours = sum(math.ceil(p / k) for p in piles)
            # If Koko can finish within h, try to find a smaller speed.
            if hours <= h:
                res = min(res, k)
                r = k - 1
            # Otherwise, speed is too slow; increase it.
            else:
                l = k + 1
        return res

    # -----------------------------------------------------------------------
    # 5. Search a 2D Matrix (LC 74) — T1
    # You are given an m x n integer matrix matrix with the following two properties: Given an integer target, return true if target is in matrix or false otherwise. You must write a solution in O(log(m * n)) time complexity.
    # Example: matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3 → true
    # Constraints: m == matrix.length, n == matrix[i].length, 1 <= m, n <= 100, 10^4 <= matrix[i][j], target <= 10^4
    # Time: O(log(m * n)), Space: O(1)
    # -----------------------------------------------------------------------
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        if not matrix: return False
        ROWS, COLS = len(matrix), len(matrix[0])
        # l and r bound the flattened matrix indices.
        l, r = 0, ROWS * COLS - 1
        while l <= r:
            m = (l + r) // 2
            # Map 1D index m to 2D row and column.
            row, col = m // COLS, m % COLS
            # If value is smaller than target, search the right portion.
            if matrix[row][col] < target:
                l = m + 1
            # If value is larger than target, search the left portion.
            elif matrix[row][col] > target:
                r = m - 1
            # Target found.
            else:
                return True
        return False

    # -----------------------------------------------------------------------
    # 5. Median of Two Sorted Arrays (LC 4) — T3
    # Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
    # Time: O(log(min(m,n))), Space: O(1)
    # -----------------------------------------------------------------------
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        # Ensure A is the smaller array to bound the binary search range.
        if len(A) > len(B):
            A, B = B, A
        
        total = len(A) + len(B)
        half = total // 2
        
        # Binary search range on partition index of array A.
        l, r = 0, len(A) - 1
        while True:
            # i is the partition index of array A.
            i = (l + r) // 2
            # j is the partition index of array B, computed so that the left partition size is constant.
            j = half - i - 2
            
            # Boundary values for left and right partitions of A and B.
            aLeft = A[i] if i >= 0 else float('-inf')
            aRight = A[i + 1] if (i + 1) < len(A) else float('inf')
            bLeft = B[j] if j >= 0 else float('-inf')
            bRight = B[j + 1] if (j + 1) < len(B) else float('inf')
            
            # Check if partitions are correctly placed.
            if aLeft <= bRight and bLeft <= aRight:
                # If total length is odd, the median is the minimum of the right partition.
                if total % 2:
                    return float(min(aRight, bRight))
                # If total length is even, median is average of max of lefts and min of rights.
                return (max(aLeft, bLeft) + min(aRight, bRight)) / 2
            elif aLeft > bRight:
                # Left side of partition A is too large; reduce the partition size in A.
                r = i - 1
            else:
                # Right side of partition A is too small; increase the partition size in A.
                l = i + 1

class BinarySearchSolutionsT2:
    # -----------------------------------------------------------------------
    # 6. Capacity to Ship Packages Within D Days (LC 1011) — T2
    # A conveyor belt has packages that must be shipped from one port to another within days days. The i^th package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship. Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.
    # Example: weights = [1,2,3,4,5,6,7,8,9,10], days = 5 → 15
    # Constraints: 1 <= days <= weights.length <= 5 * 10^4, 1 <= weights[i] <= 500
    # Time: O(n log s), Space: O(1)
    # -----------------------------------------------------------------------
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # Lower bound is max weight (we must carry it), upper bound is total sum.
        l, r = max(weights), sum(weights)
        res = r
        while l <= r:
            cap = (l + r) // 2
            # Simulate shipping with current capacity: count ships required.
            ships, currCap = 1, cap
            for w in weights:
                # If adding weight w exceeds capacity, start a new shipping day.
                if currCap - w < 0:
                    ships += 1
                    currCap = cap
                currCap -= w
            # If current capacity can ship within allowed days, try smaller capacity.
            if ships <= days:
                res = min(res, cap)
                r = cap - 1
            # Otherwise, capacity is too small; increase it.
            else:
                l = cap + 1
        return res

    # -----------------------------------------------------------------------
    # 7. Find Minimum in Rotated Sorted Array II (LC 154) — T2
    # Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,4,4,5,6,7] might become: Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]]. Given the sorted rotated array nums that may contain duplicates, return the minimum element of this array. You must decrease the overall operation steps as much as possible.
    # Example: nums = [1,3,5] → 1
    # Constraints: n == nums.length, 1 <= n <= 5000, 5000 <= nums[i] <= 5000, nums is sorted and rotated between 1 and n times, Follow up: This problem is similar to Find Minimum in Rotated Sorted Array, but nums may contain, duplicates. Would this affect the runtime complexity? How and why?
    # Time: O(n) worst case, O(log n) average, Space: O(1)
    # -----------------------------------------------------------------------
    def findMinII(self, nums: List[int]) -> int:
        # Initialize boundaries covering the array indices.
        l, r = 0, len(nums) - 1
        while l < r:
            m = l + (r - l) // 2
            # If mid element is greater than right boundary, min lies in the right side.
            if nums[m] > nums[r]:
                l = m + 1
            # If mid element is less than right boundary, min is at or to the left of mid.
            elif nums[m] < nums[r]:
                r = m
            # If mid element equals right boundary, we cannot determine; shrink right pointer.
            else:
                r -= 1
        return nums[l]

    # -----------------------------------------------------------------------
    # 8. Search in Rotated Sorted Array II (LC 81) — T2
    # There is an integer array nums sorted in non-decreasing order (not necessarily with distinct values). Before being passed to your function, nums is rotated at an unknown pivot index k (0 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,4,4,5,6,6,7] might be rotated at pivot index 5 and become [4,5,6,6,7,0,1,2,4,4]. Given the array nums after the rotation and an integer target, return true if target is in nums, or false if it is not in nums. You must decrease the overall operation steps as much as possible.
    # Example: nums = [2,5,6,0,0,1,2], target = 0 → true
    # Constraints: 1 <= nums.length <= 5000, 10^4 <= nums[i] <= 10^4, nums is guaranteed to be rotated at some pivot, 10^4 <= target <= 10^4, Follow up: This problem is similar to Search in Rotated Sorted Array, but nums may contain, duplicates. Would this affect the runtime complexity? How and why?
    # Time: O(n) worst case, O(log n) average, Space: O(1)
    # -----------------------------------------------------------------------
    def searchII(self, nums: List[int], target: int) -> bool:
        # Initialize boundaries covering the array indices.
        l, r = 0, len(nums) - 1
        while l <= r:
            m = l + (r - l) // 2
            # Target found.
            if nums[m] == target:
                return True
            # Case when boundary elements equal midpoint: cannot decide which half is sorted.
            if nums[l] == nums[m] == nums[r]:
                l += 1
                r -= 1
            # Left side is sorted.
            elif nums[l] <= nums[m]:
                # If target is within the sorted left half, search left.
                if nums[l] <= target < nums[m]:
                    r = m - 1
                # Otherwise, search right.
                else:
                    l = m + 1
            # Right side is sorted.
            else:
                # If target is within the sorted right half, search right.
                if nums[m] < target <= nums[r]:
                    l = m + 1
                # Otherwise, search left.
                else:
                    r = m - 1
        return False

    # -----------------------------------------------------------------------
    # 9. Time Based Key-Value Store (LC 981) — T2
    # Design a time-based key-value data structure that can store multiple values for the same key at different time stamps and retrieve the key's value at a certain timestamp. Implement the TimeMap class: given time timestamp. timestamp_prev <= timestamp. If there are multiple such values, it returns the value associated with the largest timestamp_prev. If there are no values, it returns "".
    # Constraints: 1 <= key.length, value.length <= 100, key and value consist of lowercase English letters and digits, 1 <= timestamp <= 10^7, All the timestamps timestamp of set are strictly increasing, At most 2 * 10^5 calls will be made to set and get
    # Time: O(log n) per get, O(1) per set, Space: O(n)
    # -----------------------------------------------------------------------
    class TimeMap:
        def __init__(self):
            import collections
            self.store = collections.defaultdict(list)

        def set(self, key: str, value: str, timestamp: int) -> None:
            self.store[key].append([value, timestamp])

        def get(self, key: str, timestamp: int) -> str:
            res = ""
            # Retrieve the list of (value, timestamp) pairs for the given key.
            values = self.store.get(key, [])
            l, r = 0, len(values) - 1
            while l <= r:
                m = (l + r) // 2
                # If stored timestamp is <= requested, record value and search for larger.
                if values[m][1] <= timestamp:
                    res = values[m][0]
                    l = m + 1
                # Otherwise, timestamp is too large, search left.
                else:
                    r = m - 1
            return res

    # -----------------------------------------------------------------------
    # 13. Sqrt(x) (LC 69) — T2
    # Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well. You must not use any built-in exponent function or operator.
    # Example: x = 4 → 2
    # Constraints: 0 <= x <= 2^31 - 1
    # Time: O(log x), Space: O(1)
    # -----------------------------------------------------------------------
    def mySqrt(self, x: int) -> int:
        if x == 0:
            return 0

        left, right = 1, x
        res = 0

        while left <= right:
            mid = left + (right - left) // 2

            # If mid squared exceeds x, target square root must be smaller.
            if mid * mid > x:
                right = mid - 1
            # If mid squared is less than x, record mid as candidate and try larger.
            elif mid * mid < x:
                left = mid + 1
                res = mid
            # Perfect square found.
            else:
                return mid

        return res

class BinarySearchSolutionsL4:
    # -----------------------------------------------------------------------
    # 1. Find Peak Element (LC 162)
    # A peak element is one that is strictly greater than its neighbors. Given nums, find a peak and return its index. O(log n) required.
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def findPeakElement(self, nums: List[int]) -> int:
        l, r = 0, len(nums) - 1
        while l < r:
            m = l + (r - l) // 2
            # If next element is larger, we are on an upward slope; peak must be on the right.
            if nums[m] < nums[m + 1]:
                l = m + 1
            # Otherwise, we are on a downward slope; peak is at mid or to its left.
            else:
                r = m
        return l

    # -----------------------------------------------------------------------
    # 2. Find First and Last Position of Element in Sorted Array (LC 34)
    # Return [first_index, last_index] of target in sorted nums, or [-1,-1].
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        def find_boundary(find_first: bool) -> int:
            l, r, res = 0, len(nums) - 1, -1
            while l <= r:
                m = (l + r) // 2
                # If mid element is smaller, search the right half.
                if nums[m] < target:
                    l = m + 1
                # If mid element is larger, search the left half.
                elif nums[m] > target:
                    r = m - 1
                # Target found.
                else:
                    res = m
                    # If looking for first occurrence, continue searching left.
                    if find_first:
                        r = m - 1
                    # If looking for last occurrence, continue searching right.
                    else:
                        l = m + 1
            return res

        return [find_boundary(True), find_boundary(False)]

    # -----------------------------------------------------------------------
    # 3. Search a 2D Matrix II (LC 240)
    # Matrix rows sorted left-to-right, columns top-to-bottom. Find target.
    # Time: O(m + n), Space: O(1)
    # -----------------------------------------------------------------------
    def searchMatrixII(self, matrix: List[List[int]], target: int) -> bool:
        """Search a 2D Matrix II (LC 240): Start at the top-right corner."""
        if not matrix or not matrix[0]:
            return False
        rows, cols = len(matrix), len(matrix[0])
        row, col = 0, cols - 1
        while row < rows and col >= 0:
            val = matrix[row][col]
            # Target found.
            if val == target:
                return True
            # If current value exceeds target, target cannot be in this column; move left.
            elif val > target:
                col -= 1
            # If current value is less than target, target cannot be in this row; move down.
            else:
                row += 1
        return False

    # -----------------------------------------------------------------------
    # 4. Kth Smallest Element in a Sorted Matrix (LC 378)
    # n x n matrix, rows and cols sorted. Return the kth smallest element.
    # Time: O(n log(max-min)), Space: O(1)
    # -----------------------------------------------------------------------
    def kthSmallest(self, matrix: List[List[int]], k: int) -> int:
        n = len(matrix)

        # Helper to count elements less than or equal to mid in sorted matrix.
        def count_le(mid: int) -> int:
            row, col = 0, n - 1
            cnt = 0
            # Staircase search starting from top-right corner.
            while row < n and col >= 0:
                # If element <= mid, then all elements to its left in the row are also <= mid.
                if matrix[row][col] <= mid:
                    cnt += col + 1
                    row += 1  # Move to the next row.
                else:
                    col -= 1  # Move left to find smaller values.
            return cnt

        # Binary search range on values.
        l, r = matrix[0][0], matrix[n - 1][n - 1]
        while l < r:
            mid = l + (r - l) // 2
            # If there are at least k elements <= mid, the kth element is <= mid.
            if count_le(mid) >= k:
                r = mid
            # Otherwise, the kth element is strictly larger than mid.
            else:
                l = mid + 1
        return l

    # -----------------------------------------------------------------------
    # 5. Find K Closest Elements (LC 658)
    # Return the k closest integers to x in sorted array arr.
    # Time: O(log(n-k) + k), Space: O(1) excluding output
    # -----------------------------------------------------------------------
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        """Return the k closest integers to x in sorted array arr."""
        # Binary search for the starting index of the window.
        l, r = 0, len(arr) - k
        while l < r:
            m = l + (r - l) // 2
            # Compare distance to x for elements at indices m and m+k.
            # If element at m is farther, window must shift right.
            if x - arr[m] > arr[m + k] - x:
                l = m + 1
            # Otherwise, window must shift left or stay.
            else:
                r = m
        return arr[l:l + k]


    # -----------------------------------------------------------------------
    # 7. Count of Smaller Numbers After Self (LC 315)
    # For each nums[i], count elements to its right that are smaller.
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def countSmaller(self, nums: List[int]) -> List[int]:
        from bisect import bisect_left, insort
        sorted_list: List[int] = []
        result: List[int] = []
        # Traverse right-to-left.
        for num in reversed(nums):
            # The rank of num in our sorted list of elements seen so far
            # is exactly the count of elements smaller than num to its right.
            result.append(bisect_left(sorted_list, num))
            # Insert the current element to keep our seen list sorted.
            insort(sorted_list, num)
        # Reverse the collected result to restore original left-to-right order.
        return result[::-1]

    # -----------------------------------------------------------------------
    # 8. Split Array Largest Sum (LC 410)
    # Split nums into m non-empty subarrays to minimize the largest subarray sum.
    # Time: O(n log(sum)), Space: O(1)
    # -----------------------------------------------------------------------
    def splitArray(self, nums: List[int], m: int) -> int:
        # Greedy feasibility check: can we partition nums with max subarray sum <= max_sum?
        def feasible(max_sum: int) -> bool:
            """Predicate helper used by binary search on the answer."""
            splits, curr = 1, 0
            for n in nums:
                # If current subarray sum exceeds max_sum, start a new subarray split.
                if curr + n > max_sum:
                    splits += 1
                    curr = 0
                curr += n
            # Return True if the number of splits required doesn't exceed m.
            return splits <= m

        l, r = max(nums), sum(nums)
        while l < r:
            mid = l + (r - l) // 2
            # If mid is feasible, try to find a smaller maximum sum.
            if feasible(mid):
                r = mid
            # Otherwise, mid is too small; we need a larger limit.
            else:
                l = mid + 1
        return l

    # -----------------------------------------------------------------------
    # 9. Maximum Side Length of a Square with Sum <= Threshold (LC 1292)
    # Return the max side length of a square submatrix with sum <= threshold.
    # Time: O(m * n * log(min(m,n))), Space: O(m * n)
    # -----------------------------------------------------------------------
    def maxSideLength(self, mat: List[List[int]], threshold: int) -> int:
        rows, cols = len(mat), len(mat[0])
        # Compute 2D prefix sums to enable O(1) square sum queries.
        prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for i in range(1, rows + 1):
            for j in range(1, cols + 1):
                prefix[i][j] = (mat[i-1][j-1] + prefix[i-1][j]
                                + prefix[i][j-1] - prefix[i-1][j-1])

        # Helper to check if a square of side k exists with sum <= threshold.
        def has_square(k: int) -> bool:
            for i in range(k, rows + 1):
                for j in range(k, cols + 1):
                    # Query 2D range sum in O(1) using prefix matrix.
                    s = (prefix[i][j] - prefix[i-k][j]
                         - prefix[i][j-k] + prefix[i-k][j-k])
                    if s <= threshold:
                        return True
            return False

        # Binary search on the side length of the square.
        l, r, res = 1, min(rows, cols), 0
        while l <= r:
            mid = l + (r - l) // 2
            # If a square of side mid is valid, record candidate and try larger.
            if has_square(mid):
                res = mid
                l = mid + 1
            # Otherwise, side length is too large; search smaller.
            else:
                r = mid - 1
        return res



if __name__ == "__main__":
    sol = BinarySearchSolutions()
    sol2 = BinarySearchSolutionsT2()

    # search
    assert sol.search([-1, 0, 3, 5, 9, 12], 9) == 4
    assert sol.search([-1, 0, 3, 5, 9, 12], 2) == -1

    # searchMatrix
    assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3) == True
    assert sol.searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13) == False

    # minEatingSpeed
    assert sol.minEatingSpeed([3, 6, 7, 11], 8) == 4
    assert sol.minEatingSpeed([30, 11, 23, 4, 20], 5) == 30

    # findMin (rotated)
    assert sol.findMin([3, 4, 5, 1, 2]) == 1
    assert sol.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert sol.findMin([11, 13, 15, 17]) == 11

    # searchRotated
    assert sol.searchRotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert sol.searchRotated([4, 5, 6, 7, 0, 1, 2], 3) == -1

    # findMedianSortedArrays
    assert sol.findMedianSortedArrays([1, 3], [2]) == 2.0
    assert sol.findMedianSortedArrays([1, 2], [3, 4]) == 2.5

    # shipWithinDays
    assert sol2.shipWithinDays([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5) == 15
    assert sol2.shipWithinDays([3, 2, 2, 4, 1, 4], 3) == 6

    # searchWithDuplicates (LC 81)
    assert sol2.searchII([2, 5, 6, 0, 0, 1, 2], 0) == True
    assert sol2.searchII([2, 5, 6, 0, 0, 1, 2], 3) == False
    assert sol2.searchII([1, 1, 1, 1, 1, 1, 2], 2) == True

    # TimeMap
    tm = sol2.TimeMap()
    tm.set("foo", "bar", 1)
    assert tm.get("foo", 1) == "bar"
    assert tm.get("foo", 3) == "bar"
    tm.set("foo", "bar2", 4)
    assert tm.get("foo", 4) == "bar2"
    assert tm.get("foo", 5) == "bar2"

    # mySqrt
    assert sol2.mySqrt(4) == 2
    assert sol2.mySqrt(8) == 2
    assert sol2.mySqrt(0) == 0

    sol4 = BinarySearchSolutionsL4()

    # findPeakElement (LC 162)
    assert sol4.findPeakElement([1, 2, 3, 1]) == 2
    assert sol4.findPeakElement([1, 2, 1, 3, 5, 6, 4]) in (1, 5)
    assert sol4.findPeakElement([1]) == 0

    # searchRange (LC 34)
    assert sol4.searchRange([5, 7, 7, 8, 8, 10], 8) == [3, 4]
    assert sol4.searchRange([5, 7, 7, 8, 8, 10], 6) == [-1, -1]
    assert sol4.searchRange([], 0) == [-1, -1]

    # searchMatrixII (LC 240)
    assert sol4.searchMatrixII(
        [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19],
         [3, 6, 9, 16, 22], [10, 13, 14, 17, 24],
         [18, 21, 23, 26, 30]], 5) == True
    assert sol4.searchMatrixII(
        [[1, 4, 7, 11, 15], [2, 5, 8, 12, 19],
         [3, 6, 9, 16, 22], [10, 13, 14, 17, 24],
         [18, 21, 23, 26, 30]], 20) == False

    # kthSmallest (LC 378)
    assert sol4.kthSmallest([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
    assert sol4.kthSmallest([[1, 2], [1, 3]], 2) == 1

    # findClosestElements (LC 658)
    assert sol4.findClosestElements([1, 2, 3, 4, 5], 4, 3) == [1, 2, 3, 4]
    assert sol4.findClosestElements([1, 2, 3, 4, 5], 4, -1) == [1, 2, 3, 4]

    # countSmaller (LC 315)
    assert sol4.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert sol4.countSmaller([-1]) == [0]
    assert sol4.countSmaller([-1, -1]) == [0, 0]

    # splitArray (LC 410)
    assert sol4.splitArray([7, 2, 5, 10, 8], 2) == 18
    assert sol4.splitArray([1, 2, 3, 4, 5], 2) == 9

    # maxSideLength (LC 1292)
    assert sol4.maxSideLength([[1, 1, 3, 2, 4, 3, 2],
                                [1, 1, 3, 2, 4, 3, 2],
                                [1, 1, 3, 2, 4, 3, 2]], 4) == 2
    assert sol4.maxSideLength([[2, 2], [2, 2]], 4) == 1

    print("All binary search tests passed.")
