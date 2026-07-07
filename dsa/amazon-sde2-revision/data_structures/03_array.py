"""
Arrays patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Modifying an array while iterating over it.\n- Out of bounds errors (always check `0 <= i < len(arr)`).\n- Assuming the array is sorted when it isn't.

Common Variants:
- Prefix Sums (Range Sum Queries)\n- Two Pointers / Sliding Window\n- In-place modifications (O(1) space)\n- Kadane's Algorithm (Maximum Subarray)

General Tips & Best Practices:
- If O(1) space is required, think about using the array itself as a hash map (e.g., negating values).\n- For subarray sums, almost always think Prefix Sums.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
from collections import deque

class ArraySolutions:
    # -----------------------------------------------------------------------
    # 1. Two Sum (LC 1) — T1
    # Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice. You can return the answer in any order.
    # Example: nums = [2,7,11,15], target = 9 → [0,1]
    # Constraints: 2 <= nums.length <= 10^4, 10^9 <= nums[i] <= 10^9, 10^9 <= target <= 10^9, Only one valid answer exists, Follow-up: Can you come up with an algorithm that is less than O(n^2) time complexity?
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Map to store number to its index.
        seen = {}
        # Iterate over the numbers with their indices.
        for i, num in enumerate(nums):
            # Check if complement exists in seen map.
            if target - num in seen:
                # Return the indices of the complement and current element.
                return [seen[target - num], i]
            # Record current number and its index.
            seen[num] = i
        # Return empty list if no pair is found.
        return []

    # -----------------------------------------------------------------------
    # 2. Best Time to Buy and Sell Stock (LC 121) — T1
    # You are given an array prices where prices[i] is the price of a given stock on the i^th day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
    # Example: prices = [7,1,5,3,6,4] → 5
    # Constraints: 1 <= prices.length <= 10^5, 0 <= prices[i] <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxProfit(self, prices: List[int]) -> int:
        # Track the lowest price seen so far.
        min_price = float('inf')
        # Track the maximum profit we can get.
        max_profit = 0
        # Iterate over all prices day by day.
        for price in prices:
            # Update running minimum price.
            min_price = min(min_price, price)
            # Update running maximum profit if selling today is better.
            max_profit = max(max_profit, price - min_price)
        return max_profit

    # -----------------------------------------------------------------------
    # 3. Maximum Subarray (LC 53) — T1
    # Given an integer array nums, find the subarray with the largest sum, and return its sum.
    # Example: nums = [-2,1,-3,4,-1,2,1,-5,4] → 6
    # Constraints: 1 <= nums.length <= 10^5, 10^4 <= nums[i] <= 10^4, Follow up: If you have figured out the O(n) solution, try coding another solution using the divide, and conquer approach, which is more subtle
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxSubArray(self, nums: List[int]) -> int:
        # Initialize global maximum sum to negative infinity.
        max_sum = float('-inf')
        # Track the current subarray sum.
        current_sum = 0
        # Iterate through each number in the array.
        for num in nums:
            # Decide to restart subarray at current element or extend.
            current_sum = max(num, current_sum + num)
            # Update global max sum.
            max_sum = max(max_sum, current_sum)
        return max_sum

    # Divide and Conquer approach for Maximum Subarray
    # Time: O(n log n), Space: O(log n)
    def maxSubArrayDivideAndConquer(self, nums: List[int]) -> int:
        def find_max_crossing_subarray(left, mid, right):
            # Best suffix sum ending exactly at mid.
            left_sum = float('-inf')
            current_sum = 0
            for i in range(mid, left - 1, -1):
                current_sum += nums[i]
                left_sum = max(left_sum, current_sum)
            
            # Best prefix sum starting exactly at mid + 1.
            right_sum = float('-inf')
            current_sum = 0
            for i in range(mid + 1, right + 1):
                current_sum += nums[i]
                right_sum = max(right_sum, current_sum)
                    
            return left_sum + right_sum

        def find_max_subarray(left, right):
            # Base case: only one element in range.
            if left == right:
                return nums[left]
                
            # Find the midpoint of the current range.
            mid = (left + right) // 2
            
            # Recursively find the max subarray sum in left, right, and crossing segments.
            left_max = find_max_subarray(left, mid)
            right_max = find_max_subarray(mid + 1, right)
            cross_max = find_max_crossing_subarray(left, mid, right)
            
            # Return the maximum of all three candidate values.
            return max(left_max, right_max, cross_max)
            
        return find_max_subarray(0, len(nums) - 1)

    # -----------------------------------------------------------------------
    # 4. Product of Array Except Self (LC 238) — T1
    # Given an integer array nums, return an array answer such that answer[i] is equal to the product of all the elements of nums except nums[i]. The product of any prefix or suffix of nums is guaranteed to fit in a 32-bit integer. You must write an algorithm that runs in O(n) time and without using the division operation.
    # Example: nums = [1,2,3,4] → [24,12,8,6]
    # Constraints: 2 <= nums.length <= 10^5, 30 <= nums[i] <= 30, The input is generated such that answer[i] is guaranteed to fit in a 32-bit integer, Follow up: Can you solve the problem in O(1) extra space complexity? (The output array does not, count as extra space for space complexity analysis.)
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        # Initialize result array with 1s.
        res = [1] * n
        # Prefix product tracks product of all elements to the left of i.
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        # Suffix product tracks product of all elements to the right of i.
        suffix = 1
        for i in range(n - 1, -1, -1):
            # Combine prefix and suffix products.
            res[i] *= suffix
            suffix *= nums[i]
        return res

    # -----------------------------------------------------------------------
    # 5. Contains Duplicate (LC 217) — T1
    # Given an integer array nums, return true if any value appears at least twice in the array, and return false if every element is distinct.
    # Example: nums = [1,2,3,1] → true
    # Constraints: 1 <= nums.length <= 10^5, 10^9 <= nums[i] <= 10^9
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def containsDuplicate(self, nums: List[int]) -> bool:
        return len(set(nums)) != len(nums)

    # -----------------------------------------------------------------------
    # 6. Trapping Rain Water (LC 42) — T1
    # Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.
    # Example: height = [0,1,0,2,1,0,1,3,2,1,2,1] → 6
    # Constraints: n == height.length, 1 <= n <= 2 * 10^4, 0 <= height[i] <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def trap(self, height: List[int]) -> int:
        # Guard against empty height array.
        if not height: return 0
        # Initialize left and right pointers.
        l, r = 0, len(height) - 1
        # Track the maximum heights from left and right sides.
        l_max, r_max = height[l], height[r]
        res = 0

        # Loop until left and right pointers meet.
        while l < r:
            # Symmetrically advance pointers from the side with lower max height.
            if l_max < r_max:
                l += 1
                l_max = max(l_max, height[l])
                res += l_max - height[l]
            else:
                r -= 1
                r_max = max(r_max, height[r])
                res += r_max - height[r]
        return res

    # -----------------------------------------------------------------------
    # 7. Sliding Window Maximum (LC 239) — T1
    # You are given an array of integers nums, there is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position. Return the max sliding window.
    # Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 → [3,3,5,5,6,7]
    # Constraints: 1 <= nums.length <= 10^5, 10^4 <= nums[i] <= 10^4, 1 <= k <= nums.length
    # Time: O(n), Space: O(k)
    # -----------------------------------------------------------------------
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        res = []
        q = deque()  # stores indices
        for i, num in enumerate(nums):
            while q and q[0] < i - k + 1:
                q.popleft()
            while q and nums[q[-1]] < num:
                q.pop()
            q.append(i)
            if i >= k - 1:
                res.append(nums[q[0]])
        return res

    # -----------------------------------------------------------------------
    # 8. Subarray Sum Equals K (LC 560) — T1
    # Given an array of integers nums and an integer k, return the total number of subarrays whose sum equals to k. A subarray is a contiguous non-empty sequence of elements within an array.
    # Example: nums = [1,1,1], k = 2 → 2
    # Constraints: 1 <= nums.length <= 2 * 10^4, 1000 <= nums[i] <= 1000, 10^7 <= k <= 10^7
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        curr_sum = 0
        prefix_sums = {0: 1}            # storing the prefix sum in the hash table used for cases when the array has negative numbers 
        for num in nums:
            curr_sum += num
            if curr_sum - k in prefix_sums:
                count += prefix_sums[curr_sum - k]
            prefix_sums[curr_sum] = prefix_sums.get(curr_sum, 0) + 1
        return count

    # -----------------------------------------------------------------------
    # 9. Merge Intervals — T1
    # Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
    # Example: intervals = [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
    # Constraints: 1 <= intervals.length <= 10^4, intervals[i].length == 2, 0 <= starti <= endi <= 10^4
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # Sort intervals by start time.
        intervals.sort(key=lambda x: x[0])
        # Seed result with the first interval.
        res = [intervals[0]]
        # Process remaining intervals sequentially.
        for start, end in intervals[1:]:
            last_end = res[-1][1]
            # If current interval overlaps with the last added interval, merge them.
            if start <= last_end:
                res[-1][1] = max(last_end, end)
            # Otherwise, append it as a new distinct interval.
            else:
                res.append([start, end])
        return res

    # -----------------------------------------------------------------------
    # 10. 3Sum (LC 15) — T1
    # Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. Notice that the solution set must not contain duplicate triplets.
    # Example: nums = [-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]
    # Constraints: 3 <= nums.length <= 3000, 10^5 <= nums[i] <= 10^5
    # Time: O(n^2), Space: O(n)
    # -----------------------------------------------------------------------
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Sort input array to easily skip duplicates and use two pointers.
        nums.sort()
        res = []
        # Fix one element and find pairs sum to its negation.
        for i in range(len(nums) - 2):
            # Skip duplicates of the first element.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            # Move pointers toward each other to find target sums.
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                if s < 0:
                    l += 1
                elif s > 0:
                    r -= 1
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    # Skip duplicate values for left and right pointers.
                    while l < r and nums[l] == nums[l + 1]: l += 1
                    while l < r and nums[r] == nums[r - 1]: r -= 1
                    l += 1
                    r -= 1
        return res

    # -----------------------------------------------------------------------
    # 11. Container With Most Water (LC 11) — T1
    # You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the i^th line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store. Notice that you may not slant the container.
    # Example: height = [1,8,6,2,5,4,8,3,7] → 49
    # Constraints: n == height.length, 2 <= n <= 10^5, 0 <= height[i] <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxArea(self, height: List[int]) -> int:
        # Left and right boundaries pointers.
        l, r = 0, len(height) - 1
        max_area = 0
        # Contract boundaries inwards while updating max area.
        while l < r:
            # Calculate water trapped in the current container boundaries.
            area = (r - l) * min(height[l], height[r])
            max_area = max(max_area, area)
            # Move the pointer pointing to the shorter vertical bar.
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_area

class ArraySolutionsT2:
    # -----------------------------------------------------------------------
    # 1. Maximum Product Subarray (LC 152) — T2
    # Given an integer array nums, find a subarray that has the largest product, and return the product. The test cases are generated so that the answer will fit in a 32-bit integer. Note that the product of an array with a single element is the value of that element.
    # Example: nums = [2,3,-2,4] → 6
    # Constraints: 1 <= nums.length <= 2 * 10^4, 10 <= nums[i] <= 10, The product of any subarray of nums is guaranteed to fit in a 32-bit integer
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxProduct(self, nums: List[int]) -> int:
        # Initialize result with the maximum single element.
        res = max(nums)
        # Running minimum and maximum products ending at current position.
        curMin, curMax = 1, 1

        for n in nums:
            # Zero resets the running window boundaries.
            if n == 0:
                curMin, curMax = 1, 1
                continue
            # Keep previous curMax to calculate new curMin correctly.
            tmp = curMax * n
            # Update running max and min products.
            curMax = max(n * curMax, n * curMin, n)
            curMin = min(tmp, n * curMin, n)
            # Track overall maximum subarray product.
            res = max(res, curMax)
        return res

    # -----------------------------------------------------------------------
    # 2. Find Minimum in Rotated Sorted Array — T2
    # Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become: Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]]. Given the sorted rotated array nums of unique elements, return the minimum element of this array. You must write an algorithm that runs in O(log n) time.
    # Example: nums = [3,4,5,1,2] → 1
    # Constraints: n == nums.length, 1 <= n <= 5000, 5000 <= nums[i] <= 5000, All the integers of nums are unique, nums is sorted and rotated between 1 and n times
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def findMin(self, nums: List[int]) -> int:
        # Track running minimum, starting with the first element.
        res = nums[0]
        # Pointers for binary search.
        l, r = 0, len(nums) - 1

        while l <= r:
            # If current segment is already sorted, the minimum is nums[l].
            if nums[l] < nums[r]:
                res = min(res, nums[l])
                break

            # Find mid element.
            m = (l + r) // 2
            res = min(res, nums[m])
            # If mid is greater or equal to left element, left side is sorted.
            if nums[m] >= nums[l]:
                l = m + 1
            else:
                r = m - 1
        return res

    # -----------------------------------------------------------------------
    # 3. Search in Rotated Sorted Array (LC 33) — T2
    # There is an integer array nums sorted in ascending order (with distinct values). Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2]. Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums. You must write an algorithm with O(log n) runtime complexity.
    # Example: nums = [4,5,6,7,0,1,2], target = 0 → 4
    # Constraints: 1 <= nums.length <= 5000, 10^4 <= nums[i] <= 10^4, All values of nums are unique, nums is an ascending array that is possibly rotated, 10^4 <= target <= 10^4
    # Time: O(log n), Space: O(1)
    # -----------------------------------------------------------------------
    def search(self, nums: List[int], target: int) -> int:
        l, r = 0, len(nums) - 1

        while l <= r:
            mid = (l + r) // 2
            if target == nums[mid]:
                return mid

            # Left sorted portion
            if nums[l] <= nums[mid]:
                if target > nums[mid] or target < nums[l]:
                    l = mid + 1
                else:
                    r = mid - 1
            # Right sorted portion
            else:
                if target < nums[mid] or target > nums[r]:
                    r = mid - 1
                else:
                    l = mid + 1
        return -1

    # -----------------------------------------------------------------------
    # 4. Jump Game (LC 55) — T2
    # You are given an integer array nums. You are initially positioned at the array's first index, and each element in the array represents your maximum jump length at that position. Return true if you can reach the last index, or false otherwise.
    # Example: nums = [2,3,1,1,4] → true
    # Constraints: 1 <= nums.length <= 10^4, 0 <= nums[i] <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def canJump(self, nums: List[int]) -> bool:
        # Start with the last index as the initial goal.
        goal = len(nums) - 1
        # Work backward from the end of the array to index 0.
        for i in range(len(nums) - 1, -1, -1):
            # If current index can jump to or beyond the goal, update the goal.
            if i + nums[i] >= goal:
                goal = i
        # If goal is shifted all the way to 0, index 0 can reach the end.
        return goal == 0

    # -----------------------------------------------------------------------
    # 5. Next Permutation — T2
    # A permutation of an array of integers is an arrangement of its members into a sequence or linear order. [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1]. The next permutation of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the next permutation of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order). lexicographical larger rearrangement. Given an array of integers nums, find the next permutation of nums. The replacement must be in place and use only constant extra memory.
    # Example: nums = [1,2,3] → [1,3,2]
    # Constraints: 1 <= nums.length <= 100, 0 <= nums[i] <= 100
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def nextPermutation(self, nums: List[int]) -> None:
        N = len(nums)
        pivot = 0
        # Find the first element from the right that is smaller than its next element
        for i in range(N - 1, 0, -1):
            if nums[i - 1] < nums[i]:
                pivot = i
                break

        if pivot == 0:
            nums.reverse()
            return

        swap = N - 1
        while nums[pivot - 1] >= nums[swap]:
            swap -= 1

        # Swap and reverse the suffix
        nums[swap], nums[pivot - 1] = nums[pivot - 1], nums[swap]
        nums[pivot:] = reversed(nums[pivot:])

    # -----------------------------------------------------------------------
    # 6. Rotate Array — T2
    # Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.
    # Example: nums = [1,2,3,4,5,6,7], k = 3 → [5,6,7,1,2,3,4]
    # Constraints: 1 <= nums.length <= 10^5, 2^31 <= nums[i] <= 2^31 - 1, 0 <= k <= 10^5, Follow up:, Try to come up with as many solutions as you can. There are at least three different ways to solve, this problem, Could you do it in-place with O(1) extra space?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def rotate(self, nums: List[int], k: int) -> None:
        # Reduce k modulo length to prevent out-of-bounds on k > N.
        k = k % len(nums)

        def reverse(l, r):
            # Swap symmetric elements to reverse segment in-place.
            while l < r:
                nums[l], nums[r] = nums[r], nums[l]
                l, r = l + 1, r - 1

        # Step 1: Reverse entire array.
        reverse(0, len(nums) - 1)
        # Step 2: Reverse first k elements.
        reverse(0, k - 1)
        # Step 3: Reverse remaining N-k elements.
        reverse(k, len(nums) - 1)

    # -----------------------------------------------------------------------
    # 7. Majority Element (LC 169) — T2
    # Given an array nums of size n, return the majority element. The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.
    # Example: nums = [3,2,3] → 3
    # Constraints: n == nums.length, 1 <= n <= 5 * 10^4, 10^9 <= nums[i] <= 10^9, The input is generated such that a majority element will exist in the array, Follow-up: Could you solve the problem in linear time and in O(1) space?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def majorityElement(self, nums: List[int]) -> int:
        # Candidates and votes counter.
        res, count = 0, 0
        # Single pass Boyer-Moore Voting algorithm.
        for n in nums:
            # If current count is zero, pick the current element as candidate.
            if count == 0:
                res = n
            # Cancel out candidates on mismatches.
            count += (1 if n == res else -1)
        return res

    # -----------------------------------------------------------------------
    # 8. Set Matrix Zeroes — T2
    # Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's. You must do it in place.
    # Example: matrix = [[1,1,1],[1,0,1],[1,1,1]] → [[1,0,1],[0,0,0],[1,0,1]]
    # Constraints: m == matrix.length, n == matrix[0].length, 1 <= m, n <= 200, 2^31 <= matrix[i][j] <= 2^31 - 1, Follow up:, A straightforward solution using O(mn) space is probably a bad idea, A simple improvement uses O(m + n) space, but still not the best solution, Could you devise a constant space solution?
    # Time: O(m*n), Space: O(1)
    # -----------------------------------------------------------------------
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """Set Matrix Zeroes: Use the matrix's own first row and first column as O(1) space ledgers."""
        ROWS, COLS = len(matrix), len(matrix[0])
        rowZero = False

        # First pass: use first row/col as marker arrays.
        for r in range(ROWS):
            for c in range(COLS):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0
                    # For r==0, use separate rowZero flag since (0,0) is shared.
                    if r > 0:
                        matrix[r][0] = 0
                    else:
                        rowZero = True

        # Second pass: zero out cells based on markers.
        for r in range(1, ROWS):
            for c in range(1, COLS):
                if matrix[0][c] == 0 or matrix[r][0] == 0:
                    matrix[r][c] = 0

        # Zero out first column if ledger cell says so.
        if matrix[0][0] == 0:
            for r in range(ROWS):
                matrix[r][0] = 0

        # Zero out first row if flag is set.
        if rowZero:
            for c in range(COLS):
                matrix[0][c] = 0

    # -----------------------------------------------------------------------
    # 9. Spiral Matrix (LC 54) — T2
    # Given an m x n matrix, return all elements of the matrix in spiral order.
    # Example: matrix = [[1,2,3],[4,5,6],[7,8,9]] → [1,2,3,6,9,8,7,4,5]
    # Constraints: m == matrix.length, n == matrix[i].length, 1 <= m, n <= 10, 100 <= matrix[i][j] <= 100
    # Time: O(m*n), Space: O(1)
    # -----------------------------------------------------------------------
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        res = []
        # Setup boundaries for peeling layers.
        left, right = 0, len(matrix[0])
        top, bottom = 0, len(matrix)

        while left < right and top < bottom:
            # Traverse top row left-to-right.
            for i in range(left, right):
                res.append(matrix[top][i])
            top += 1

            # Traverse right column top-to-bottom.
            for i in range(top, bottom):
                res.append(matrix[i][right - 1])
            right -= 1

            # Check for termination before reversing direction.
            if not (left < right and top < bottom):
                break

            # Traverse bottom row right-to-left.
            for i in range(right - 1, left - 1, -1):
                res.append(matrix[bottom - 1][i])
            bottom -= 1

            # Traverse left column bottom-to-top.
            for i in range(bottom - 1, top - 1, -1):
                res.append(matrix[i][left])
            left += 1

        return res

class ArraySolutionsL4:
    # -----------------------------------------------------------------------
    # 1. Subarray Product Less Than K (LC 713)
    # Given an array of positive integers nums and a positive integer k, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.
    # Example: nums = [10,5,2,6], k = 100 → 8
    # Constraints: 1 <= nums.length <= 3 * 10^4, 1 <= nums[i] <= 1000, 0 <= k <= 10^6
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        # If k <= 1, no positive product can be less than k.
        if k <= 1:
            return 0
        count = 0
        product = 1
        l = 0
        # Expand right boundary.
        for r in range(len(nums)):
            product *= nums[r]
            # Shrink left boundary while product >= k.
            while product >= k:
                product //= nums[l]
                l += 1
            # Number of valid subarrays ending at r is (r - l + 1).
            count += r - l + 1
        return count

    # -----------------------------------------------------------------------
    # 2. Maximum Sum Circular Subarray (LC 918)
    # Given a circular integer array nums of length n, return the maximum possible sum of a non-empty subarray of nums. A circular array means the end of the array connects to the beginning. Formally, the next element of nums[i] is nums[(i + 1) % n] and the previous element of nums[i] is nums[(i - 1 + n) % n].
    # Example: nums = [1,-2,3,-2] → 3
    # Constraints: n == nums.length, 1 <= n <= 3 * 10^4, 3 * 10^4 <= nums[i] <= 3 * 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        # Precompute total sum of elements.
        total_sum = sum(nums)
        # Running and global max/min subarray sums.
        max_sum = cur_max = nums[0]
        min_sum = cur_min = nums[0]
        # Single pass to run both max-sum and min-sum Kadane.
        for num in nums[1:]:
            cur_max = max(num, cur_max + num)
            max_sum = max(max_sum, cur_max)
            cur_min = min(num, cur_min + num)
            min_sum = min(min_sum, cur_min)
        # Symmetrically choose between non-wrapping and wrapping max sums.
        if max_sum > 0:
            return max(max_sum, total_sum - min_sum)
        return max_sum

    # -----------------------------------------------------------------------
    # 3. Shortest Unsorted Continuous Subarray (LC 581)
    # Given an integer array nums, you need to find one continuous subarray such that if you only sort this subarray in non-decreasing order, then the whole array will be sorted in non-decreasing order. Return the length of the shortest such subarray.
    # Example: nums = [2,6,4,8,10,9,15] → 5
    # Constraints: 1 <= nums.length <= 10^4, 10^5 <= nums[i] <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findUnsortedSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        l, r = -1, -2
        # Scan from left to find the first slope drop index.
        for i in range(n - 1):
            if nums[i] > nums[i + 1]:
                l = i
                break
        # If no slope drop, array is already sorted.
        if l == -1:
            return 0
        # Scan from right to find the first slope rise index.
        for i in range(n - 1, 0, -1):
            if nums[i] < nums[i - 1]:
                r = i
                break
        # Find minimum and maximum elements in the unsorted middle.
        dirty_min = min(nums[l:r + 1])
        dirty_max = max(nums[l:r + 1])
        # Expand left boundary if predecessor exceeds dirty minimum.
        while l > 0 and nums[l - 1] > dirty_min:
            l -= 1
        # Expand right boundary if successor is smaller than dirty maximum.
        while r < n - 1 and nums[r + 1] < dirty_max:
            r += 1
        return r - l + 1

    # -----------------------------------------------------------------------
    # 4. Find All Numbers Disappeared in an Array (LC 448)
    # Given an array nums of n integers where nums[i] is in the range [1, n], return an array of all the integers in the range [1, n] that do not appear in nums.
    # Example: nums = [4,3,2,7,8,2,3,1] → [5,6]
    # Constraints: n == nums.length, 1 <= n <= 10^5, 1 <= nums[i] <= n
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        # Mark visited indices by negating elements.
        for num in nums:
            idx = abs(num) - 1
            if nums[idx] > 0:
                nums[idx] = -nums[idx]
        # Any positive element indicates a missing number at index + 1.
        return [i + 1 for i in range(len(nums)) if nums[i] > 0]

    # -----------------------------------------------------------------------
    # 5. First Missing Positive (LC 41)
    # Given an unsorted integer array nums, return the smallest missing positive integer. You must implement an algorithm that runs in O(n) time and uses O(1) auxiliary space.
    # Example: nums = [1,2,0] → 3
    # Constraints: 1 <= nums.length <= 10^5, 2^31 <= nums[i] <= 2^31 - 1
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # Step 1: Clean out negative numbers, zeros, and out-of-range elements.
        for i in range(n):
            if nums[i] <= 0 or nums[i] > n:
                nums[i] = n + 1
        # Step 2: Use in-place negation as a presence bitmap.
        for i in range(n):
            v = abs(nums[i])
            if 1 <= v <= n and nums[v - 1] > 0:
                nums[v - 1] = -nums[v - 1]
        # Step 3: Scan from index 0 to find the first positive cell.
        for i in range(n):
            if nums[i] > 0:
                return i + 1
        return n + 1

    # -----------------------------------------------------------------------
    # 6. Maximum Points You Can Obtain from Cards (LC 1423)
    # There are several cards arranged in a row. In one step you can take one card from the beginning or end of the row. You want to take exactly k cards. Return the maximum score of points you can obtain.
    # Example: cardPoints = [1,2,3,4,5,6,1], k = 3 → 12
    # Constraints: 1 <= cardPoints.length <= 10^5, 1 <= cardPoints[i] <= 10^4, 1 <= k <= cardPoints.length
    # Time: O(k), Space: O(1)
    # -----------------------------------------------------------------------
    def maxScore(self, cardPoints: List[int], k: int) -> int:
        n = len(cardPoints)
        total = sum(cardPoints)
        window_size = n - k
        # If picking all cards, return the sum of all elements.
        if window_size == 0:
            return total
        # Sum of the first unselected sliding window.
        window = sum(cardPoints[:window_size])
        min_window = window
        # Slide the window rightward.
        for i in range(window_size, n):
            window += cardPoints[i] - cardPoints[i - window_size]
            min_window = min(min_window, window)
        # Maximum score is total minus the minimum unselected window.
        return total - min_window

    # -----------------------------------------------------------------------
    # 7. Minimum Size Subarray Sum (LC 209)
    # Given an array of positive integers nums and a positive integer target, return the minimal length of a contiguous subarray of which the sum is greater than or equal to target. If there is no such subarray, return 0.
    # Example: target = 7, nums = [2,3,1,2,4,3] → 2
    # Constraints: 1 <= target <= 10^9, 1 <= nums.length <= 10^5, 1 <= nums[i] <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        curr_sum = 0
        min_len = float('inf')
        # Iterate right pointer.
        for r in range(len(nums)):
            curr_sum += nums[r]
            # Shrink window from left as long as range sum meets target.
            while curr_sum >= target:
                min_len = min(min_len, r - l + 1)
                curr_sum -= nums[l]
                l += 1
        # Return 0 if no valid subarray sum was found.
        return 0 if min_len == float('inf') else min_len

    # -----------------------------------------------------------------------
    # 8. Longest Mountain in Array (LC 845)
    # You may recall that an array arr is a mountain array if and only if arr.length >= 3 and there exists an index i (0-indexed) with 0 < i < arr.length - 1 such that arr[0] < arr[1] < ... < arr[i] > arr[i + 1] > ... > arr[arr.length - 1]. Given an integer array arr, return the length of the longest mountain. If there is no mountain, return 0.
    # Example: arr = [2,1,4,7,3,2,5] → 5
    # Constraints: 1 <= arr.length <= 10^4, 0 <= arr[i] <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def longestMountain(self, arr: List[int]) -> int:
        n = len(arr)
        res = 0
        # Scan internal elements.
        for i in range(1, n - 1):
            # Check if current element is a mountain peak.
            if arr[i - 1] < arr[i] > arr[i + 1]:
                left, right = i, i
                # Expand left slope downwards.
                while left > 0 and arr[left - 1] < arr[left]:
                    left -= 1
                # Expand right slope downwards.
                while right < n - 1 and arr[right + 1] < arr[right]:
                    right += 1
                # Track the longest mountain.
                res = max(res, right - left + 1)
        return res

    # -----------------------------------------------------------------------
    # 9. Fruit Into Baskets (LC 904)
    # You are visiting a farm that has a single row of fruit trees arranged from left to right. The trees are represented by an integer array fruits where fruits[i] is the type of fruit the i-th tree produces. You want to collect as much fruit as possible, but with only 2 baskets you can only pick from at most 2 distinct types of fruit. Given the array fruits, return the maximum number of fruits you can pick.
    # Example: fruits = [1,2,1] → 3
    # Constraints: 1 <= fruits.length <= 10^5, 0 <= fruits[i] <= fruits.length
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def totalFruit(self, fruits: List[int]) -> int:
        from collections import defaultdict
        # Count frequency of fruit types in window.
        basket: dict = defaultdict(int)
        l = 0
        res = 0
        # Iterate right pointer.
        for r in range(len(fruits)):
            basket[fruits[r]] += 1
            # Shrink window from left if distinct types exceed 2.
            while len(basket) > 2:
                basket[fruits[l]] -= 1
                # Remove the key entirely if frequency drops to 0.
                if not basket[fruits[l]]:
                    del basket[fruits[l]]
                l += 1
            # Update max fruits collected in valid window.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 10. Replace Elements with Greatest Element on Right Side (LC 1299)
    # Given an array arr, replace every element in that array with the greatest element among the elements to its right, and replace the last element with -1. After doing so, return the array.
    # Example: arr = [17,18,5,4,6,1] → [18,6,6,6,1,-1]
    # Constraints: 1 <= arr.length <= 10^4, 1 <= arr[i] <= 10^5
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def replaceElements(self, arr: List[int]) -> List[int]:
        # Sentinel value for the last element.
        cur_max = -1
        # Traverse right-to-left.
        for i in range(len(arr) - 1, -1, -1):
            # Save new running max before overwriting element.
            new_max = max(cur_max, arr[i])
            arr[i] = cur_max
            cur_max = new_max
        return arr

    # -----------------------------------------------------------------------
    # 11. Range Sum Query — Immutable (LC 303)
    # Given an integer array nums, handle multiple queries of the following type: Calculate the sum of the elements of nums between indices left and right inclusive where left <= right. Implement the NumArray class: and right inclusive.
    # Example: ["NumArray", "sumRange", "sumRange", "sumRange"] → [null, 1, -1, -3]
    # Constraints: 1 <= nums.length <= 10^4, 10^5 <= nums[i] <= 10^5, 0 <= left <= right < nums.length, At most 10^4 calls will be made to sumRange
    # Time: O(1) per query, O(n) build, Space: O(n)
    # -----------------------------------------------------------------------
    def __init_range_sum__(self, nums: List[int]) -> None:
        n = len(nums)
        self._prefix = [0] * (n + 1)
        for i in range(n):
            self._prefix[i + 1] = self._prefix[i] + nums[i]

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix[right + 1] - self._prefix[left]

    # -----------------------------------------------------------------------
    # 12. Range Sum Query 2D — Immutable (LC 304)
    # Given a 2D matrix matrix, handle multiple queries of the following type: Calculate the sum of the elements of matrix inside the rectangle defined by its upper left corner (row1, col1) and lower right corner (row2, col2).
    # Example: ["NumMatrix", "sumRegion", "sumRegion", "sumRegion"] → [null, 8, 11, 12]
    # Constraints: m == matrix.length, n == matrix[i].length, 1 <= m, n <= 200, 10^4 <= matrix[i][j] <= 10^4, 0 <= row1 <= row2 < m, 0 <= col1 <= col2 < n, At most 10^4 calls will be made to sumRegion
    # Time: O(1) per query, O(m*n) build, Space: O(m*n)
    # -----------------------------------------------------------------------
    def __init_range_sum_2d__(self, matrix: List[List[int]]) -> None:
        m, n = len(matrix), len(matrix[0])
        self._P = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                self._P[i][j] = (matrix[i-1][j-1]
                                 + self._P[i-1][j]
                                 + self._P[i][j-1]
                                 - self._P[i-1][j-1])

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        # Use 2D prefix sum inclusion-exclusion formula to query region sum in O(1).
        return (self._P[row2+1][col2+1]
                - self._P[row1][col2+1]
                - self._P[row2+1][col1]
                + self._P[row1][col1])


if __name__ == "__main__":

    sol = ArraySolutions()
    sol2 = ArraySolutionsT2()

    # 1. Two Sum
    assert sol.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert sol.twoSum([3, 2, 4], 6) == [1, 2]
    assert sol.twoSum([3, 3], 6) == [0, 1]                  # duplicate values

    # 2. Best Time to Buy and Sell Stock
    assert sol.maxProfit([7, 1, 5, 3, 6, 4]) == 5
    assert sol.maxProfit([7, 6, 4, 3, 1]) == 0              # no profit possible

    # 3. Maximum Subarray
    assert sol.maxSubArray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert sol.maxSubArray([1]) == 1
    assert sol.maxSubArray([-1]) == -1                       # all negative

    # 4. Product of Array Except Self
    assert sol.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert sol.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert sol.productExceptSelf([0, 0]) == [0, 0]           # two zeros

    # 5. Contains Duplicate
    assert sol.containsDuplicate([1, 2, 3, 1]) == True
    assert sol.containsDuplicate([1, 2, 3, 4]) == False

    # 6. Trapping Rain Water
    assert sol.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert sol.trap([4, 2, 0, 3, 2, 5]) == 9
    assert sol.trap([3, 0, 0, 2, 0, 4]) == 10               # multiple valleys

    # 7. Sliding Window Maximum
    assert sol.maxSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [3, 3, 5, 5, 6, 7]
    assert sol.maxSlidingWindow([1], 1) == [1]               # single element

    # 8. Subarray Sum Equals K
    assert sol.subarraySum([1, 1, 1], 2) == 2
    assert sol.subarraySum([1, 2, 3], 3) == 2
    assert sol.subarraySum([-1, -1, 1], 0) == 1              # negative numbers

    # 9. 3Sum
    assert sorted([sorted(t) for t in sol.threeSum([-1, 0, 1, 2, -1, -4])]) == [[-1, -1, 2], [-1, 0, 1]]
    assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]
    assert sol.threeSum([1, 2, -2, -1]) == []                # no solution

    # 10. Container With Most Water
    assert sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert sol.maxArea([1, 1]) == 1

    # 11. Maximum Product Subarray
    assert sol2.maxProduct([2, 3, -2, 4]) == 6
    assert sol2.maxProduct([-2, 0, -1]) == 0
    assert sol2.maxProduct([-2, 3, -4]) == 24                # two negatives

    # 12. Find Min in Rotated Sorted Array
    assert sol2.findMin([3, 4, 5, 1, 2]) == 1
    assert sol2.findMin([4, 5, 6, 7, 0, 1, 2]) == 0
    assert sol2.findMin([11, 13, 15, 17]) == 11              # not rotated

    # 13. Search in Rotated Sorted Array
    assert sol2.search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert sol2.search([4, 5, 6, 7, 0, 1, 2], 3) == -1
    assert sol2.search([1], 0) == -1

    # 14. Jump Game
    assert sol2.canJump([2, 3, 1, 1, 4]) == True
    assert sol2.canJump([3, 2, 1, 0, 4]) == False
    assert sol2.canJump([0]) == True                         # single element

    # 15. Majority Element
    assert sol2.majorityElement([3, 2, 3]) == 3
    assert sol2.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2

    # 16. Spiral Matrix
    assert sol2.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 2, 3, 6, 9, 8, 7, 4, 5]
    assert sol2.spiralOrder([[1, 2], [3, 4]]) == [1, 2, 4, 3]

    print("All array tests passed.")
