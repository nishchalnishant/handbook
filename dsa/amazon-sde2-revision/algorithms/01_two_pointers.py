"""
Two Pointers patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Using two pointers on an unsorted array when trying to find pairs (e.g., Two Sum on unsorted array requires Hash Map).\n- Infinite loops if pointers don't correctly move towards each other.\n- Skipping duplicates incorrectly in 3Sum/4Sum (must check `nums[i] == nums[i-1]`).

Common Variants:
- Opposite ends (e.g., Two Sum II, Container With Most Water)\n- Same direction fast/slow (e.g., Linked List cycle, Remove Duplicates)\n- Comparing two arrays (e.g., Intersection of Two Arrays)

General Tips & Best Practices:
- Always ensure the array is sorted if using the opposite-ends approach for sums.\n- For fast/slow pointers, draw out the step-by-step movement.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
from collections import Counter, deque

class TwoPointersSolutions:
    # -----------------------------------------------------------------------
    # 1. Two Sum II (Sorted Array) (LC 167) — T1
    # Given a 1-indexed array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Return the indices of the two numbers.
    # Example: numbers = [2,7,11,15], target = 9 → [1,2]
    # Constraints: 2 <= numbers.length <= 3 * 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        # l starts at beginning, r starts at end.
        l, r = 0, len(numbers) - 1
        while l < r:
            cur_sum = numbers[l] + numbers[r]
            # If current sum is too large, reduce the sum by moving right pointer left.
            if cur_sum > target:
                r -= 1
            # If current sum is too small, increase the sum by moving left pointer right.
            elif cur_sum < target:
                l += 1
            # Target found: return 1-based indices.
            else:
                return [l + 1, r + 1]
        return []

    # -----------------------------------------------------------------------
    # 2. 3Sum (LC 15) — T1
    # Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. Notice that the solution set must not contain duplicate triplets.
    # Example: nums = [-1,0,1,2,-1,-4] → [[-1,-1,2],[-1,0,1]]
    # Constraints: 3 <= nums.length <= 3000, 10^5 <= nums[i] <= 10^5
    # Time: O(n^2), Space: O(n)
    # -----------------------------------------------------------------------
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        # Sort array to allow duplicate skipping and two-pointer search.
        nums.sort()
        res = []
        for i in range(len(nums) - 2):
            # Skip duplicate elements for the first position to avoid duplicate triplets.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                s = nums[i] + nums[l] + nums[r]
                # If sum is negative, we need larger values; move left pointer right.
                if s < 0:
                    l += 1
                # If sum is positive, we need smaller values; move right pointer left.
                elif s > 0:
                    r -= 1
                # Triplet found.
                else:
                    res.append([nums[i], nums[l], nums[r]])
                    # Skip duplicate values for the second and third positions.
                    while l < r and nums[l] == nums[l + 1]: l += 1
                    while l < r and nums[r] == nums[r - 1]: r -= 1
                    # Advance both pointers after recording the triplet.
                    l += 1
                    r -= 1
        return res

    # -----------------------------------------------------------------------
    # 3. Container With Most Water (LC 11) — T1
    # You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the i^th line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container, such that the container contains the most water. Return the maximum amount of water a container can store. Notice that you may not slant the container.
    # Example: height = [1,8,6,2,5,4,8,3,7] → 49
    # Constraints: n == height.length, 2 <= n <= 10^5, 0 <= height[i] <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height) - 1
        max_area = 0
        while l < r:
            # Area is bounded by width (r - l) and the shorter height.
            area = (r - l) * min(height[l], height[r])
            max_area = max(max_area, area)
            # Move the pointer pointing to the shorter line to potentially find a taller boundary.
            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        return max_area

    # -----------------------------------------------------------------------
    # 5. Sort Colors (Dutch National Flag) (LC 75) — T1
    # Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue. We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.
    # Example: nums = [2,0,2,1,1,0] → [0,0,1,1,2,2]
    # Constraints: n == nums.length, 1 <= n <= 300
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def sortColors(self, nums: List[int]) -> None:
        # l tracks where 0 should go, r tracks where 2 should go.
        l, r = 0, len(nums) - 1
        i = 0
        while i <= r:
            # If current element is 0, swap with the left boundary l.
            if nums[i] == 0:
                nums[l], nums[i] = nums[i], nums[l]
                l += 1
                i += 1
            # If current element is 2, swap with the right boundary r. Do not increment i.
            elif nums[i] == 2:
                nums[i], nums[r] = nums[r], nums[i]
                r -= 1
            # If current element is 1, it's already in the correct relative position.
            else:
                i += 1

    # -----------------------------------------------------------------------
    # 6. Longest Substring Without Repeating Characters (LC 3) — T1
    # Given a string s, find the length of the longest substring without repeating characters.
    # Example: s = "abcabcbb" → 3
    # Constraints: 0 <= s.length <= 5 * 10^4
    # Time: O(n), Space: O(min(m, n)) where m is the alphabet size
    # -----------------------------------------------------------------------
    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = {}
        l = 0
        res = 0
        for r in range(len(s)):
            # If current character is already in window, shift left pointer to one past its last seen position.
            if s[r] in seen and seen[s[r]] >= l:
                l = seen[s[r]] + 1
            # Record/update the last seen index of s[r].
            seen[s[r]] = r
            # Update the maximum length found so far.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 9. Find All Anagrams in a String (LC 438) — T1
    # Given two strings s and p, return an array of all the start indices of p's anagrams in s. You may return the answer in any order.
    # Example: s = "cbaebabacd", p = "abc" → [0,6]
    # Constraints: 1 <= s.length, p.length <= 3 * 10^4, s and p consist of lowercase English letters
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s): return []
        p_count = Counter(p)
        # Pre-populate current window Counter with len(p)-1 elements.
        s_count = Counter(s[:len(p)-1])
        res = []
        l = 0
        # Iterate and slide the window.
        for r in range(len(p)-1, len(s)):
            # Add incoming character on the right.
            s_count[s[r]] += 1
            # If counters match, we found an anagram at index l.
            if s_count == p_count:
                res.append(l)
            # Remove outgoing character on the left.
            s_count[s[l]] -= 1
            # Delete zero-count key to keep s_count equal-comparable.
            if s_count[s[l]] == 0:
                del s_count[s[l]]
            l += 1
        return res

    # -----------------------------------------------------------------------
    # 10. Permutation in String (LC 567) — T1
    # Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise. In other words, return true if one of s1's permutations is the substring of s2.
    # Example: s1 = "ab", s2 = "eidbaooo" → true
    # Constraints: 1 <= s1.length, s2.length <= 10^4
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2): return False
        s1_count, s2_count = Counter(s1), Counter(s2[:len(s1)-1])
        l = 0
        # Iterate and slide the window of size len(s1).
        for r in range(len(s1)-1, len(s2)):
            # Add incoming character on the right.
            s2_count[s2[r]] += 1
            # If frequencies match, permutation exists.
            if s1_count == s2_count:
                return True
            # Remove outgoing character on the left.
            s2_count[s2[l]] -= 1
            # Delete zero-count key to keep s2_count equal-comparable.
            if s2_count[s2[l]] == 0:
                del s2_count[s2[l]]
            l += 1
        return False

class TwoPointersSolutionsT2:
    # -----------------------------------------------------------------------
    # 13. Longest Repeating Character Replacement (LC 424) — T2
    # You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times. Return the length of the longest substring containing the same letter you can get after performing the above operations.
    # Example: s = "ABAB", k = 2 → 4
    # Constraints: 1 <= s.length <= 10^5, 0 <= k <= s.length
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        res = 0
        l = 0
        maxf = 0
        for r in range(len(s)):
            # Update frequency of s[r].
            count[s[r]] = count.get(s[r], 0) + 1
            # Keep track of the maximum frequency of any single character in the window.
            maxf = max(maxf, count[s[r]])
            # If number of replacements needed exceeds k, shrink the window.
            while (r - l + 1) - maxf > k:
                count[s[l]] -= 1
                l += 1
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 15. Find the Duplicate Number (LC 287) — T2
    # Given an array of integers nums containing n + 1 integers where each integer is in the range [1, n] inclusive. There is only one repeated number in nums, return this repeated number. You must solve the problem without modifying the array nums and using only constant extra space.
    # Example: nums = [1,3,4,2,2] → 2
    # Constraints: 1 <= n <= 10^5, nums.length == n + 1, 1 <= nums[i] <= n, All the integers in nums appear only once except for precisely one integer which appears two or, more times, Follow up:, How can we prove that at least one duplicate number must exist in nums?, Can you solve the problem in linear runtime complexity?
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0, 0
        # Phase 1: Detect cycle and find a meeting point inside the cycle.
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2: Reset pointer slow2 to 0, advance both at same speed to find cycle entry.
        slow2 = 0
        while True:
            slow = nums[slow]
            slow2 = nums[slow2]
            if slow == slow2:
                return slow

    # -----------------------------------------------------------------------
    # 16. 4Sum (LC 18) — T2
    # Given an array nums of n integers, return an array of all the unique quadruplets [nums[a], nums[b], nums[c], nums[d]] such that: You may return the answer in any order.
    # Example: nums = [1,0,-1,0,-2,2], target = 0 → [[-2,-1,1,2],[-2,0,0,2],[-1,0,0,1]]
    # Constraints: 1 <= nums.length <= 200, 10^9 <= nums[i] <= 10^9, 10^9 <= target <= 10^9
    # Time: O(n^3), Space: O(n)
    # -----------------------------------------------------------------------
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        nums.sort()
        res = []
        n = len(nums)
        for i in range(n - 3):
            # Skip duplicates for the first element.
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            for j in range(i + 1, n - 2):
                # Skip duplicates for the second element.
                if j > i + 1 and nums[j] == nums[j - 1]:
                    continue

                left, right = j + 1, n - 1
                while left < right:
                    total = nums[i] + nums[j] + nums[left] + nums[right]
                    # If total is too small, move left pointer right.
                    if total < target:
                        left += 1
                    # If total is too large, move right pointer left.
                    elif total > target:
                        right -= 1
                    # Quadruplet found.
                    else:
                        res.append([nums[i], nums[j], nums[left], nums[right]])
                        left += 1
                        right -= 1
                        # Skip duplicate elements for left and right pointers.
                        while left < right and nums[left] == nums[left - 1]:
                            left += 1
                        while left < right and nums[right] == nums[right + 1]:
                            right -= 1
        return res

    # -----------------------------------------------------------------------
    # 17. Max Consecutive Ones III (LC 1004) — T2
    # Given a binary array nums and an integer k, return the maximum number of consecutive 1s in the array if you can flip at most k 0s.
    # Example: nums = [1,1,1,0,0,0,1,1,1,1,0], k = 2 → 6
    # Constraints: 1 <= nums.length <= 10^5, nums[i] is either 0 or 1, 0 <= k <= nums.length
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def longestOnes(self, nums: List[int], k: int) -> int:
        left = 0
        max_len = 0
        zero_count = 0

        for right in range(len(nums)):
            # Count the incoming element if it is a 0.
            if nums[right] == 0:
                zero_count += 1

            # If zeros in window exceed k, shrink window from left until a 0 is excluded.
            while zero_count > k:
                if nums[left] == 0:
                    zero_count -= 1
                left += 1

            # Update the longest consecutive 1s length.
            max_len = max(max_len, right - left + 1)

        return max_len

class TwoPointersSolutionsL4:
    # -----------------------------------------------------------------------
    # 18. Minimum Operations to Reduce X to Zero (LC 1658)
    # Remove numbers from either end so removed sum is x.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def minOperations(self, nums: List[int], x: int) -> int:
        """Remove numbers from either end so removed sum is x."""
        target = sum(nums) - x
        if target < 0:
            return -1
        left = 0
        window_sum = 0
        best = -1
        for right, value in enumerate(nums):
            window_sum += value
            while window_sum > target and left <= right:
                window_sum -= nums[left]
                left += 1
            if window_sum == target:
                best = max(best, right - left + 1)
        return -1 if best == -1 else len(nums) - best

    # -----------------------------------------------------------------------
    # 19. Count Number of Nice Subarrays (LC 1248)
    # Given integer array nums and integer k, return the number of nice subarrays — subarrays containing exactly k odd numbers.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        # Helper to find number of subarrays with at most limit odd numbers.
        def atMost(limit):
            odd_count = 0
            res = 0
            l = 0
            for r in range(len(nums)):
                # If current number is odd, increment count.
                odd_count += nums[r] % 2
                # If count exceeds limit, shrink window from left.
                while odd_count > limit:
                    odd_count -= nums[l] % 2
                    l += 1
                # Accumulate the number of subarrays ending at index r.
                res += r - l + 1
            return res
        return atMost(k) - atMost(k - 1)

    # -----------------------------------------------------------------------
    # 20. Frequency of the Most Frequent Element (LC 1838)
    # The frequency of an element is the number of times it occurs in an array. You are given an integer array nums and an integer k. In one operation, choose an index and increment nums[i] by 1. Return the maximum possible frequency of any element after at most k operations.
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxFrequency(self, nums: List[int], k: int) -> int:
        """Frequency of the Most Frequent Element (LC 1838): Sort the array."""
        nums.sort()
        l = 0
        window_sum = 0
        res = 1
        for r in range(len(nums)):
            window_sum += nums[r]
            # While the cost to equalize all elements in the window exceeds k, shrink window from left.
            while nums[r] * (r - l + 1) - window_sum > k:
                window_sum -= nums[l]
                l += 1
            # Update the maximum frequency.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 21. Longest Subarray of 1s After Deleting One Element (LC 1493)
    # Given a binary array nums, delete one element and return the length of the longest subarray containing only 1s.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def longestSubarray(self, nums: List[int]) -> int:
        l = 0
        zero_count = 0
        res = 0
        for r in range(len(nums)):
            # If element is 0, increment zero_count.
            if nums[r] == 0:
                zero_count += 1
            # If zeros exceed 1, shrink window from left.
            while zero_count > 1:
                if nums[l] == 0:
                    zero_count -= 1
                l += 1
            # Update the max length (excluding the deleted element).
            res = max(res, r - l)
        return res

    # -----------------------------------------------------------------------
    # 22. Longest Continuous Subarray With Absolute Diff <= Limit (LC 1438)
    # Given an integer array nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements is <= limit.
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def longestSubarrayWithLimit(self, nums: List[int], limit: int) -> int:
        max_dq = deque()  # decreasing, front is max index
        min_dq = deque()  # increasing, front is min index
        l = 0
        res = 0
        for r in range(len(nums)):
            # Maintain decreasing order in max_dq (store indices).
            while max_dq and nums[max_dq[-1]] <= nums[r]:
                max_dq.pop()
            # Maintain increasing order in min_dq (store indices).
            while min_dq and nums[min_dq[-1]] >= nums[r]:
                min_dq.pop()
            max_dq.append(r)
            min_dq.append(r)
            # If the difference between current max and min exceeds limit, shrink the window.
            while nums[max_dq[0]] - nums[min_dq[0]] > limit:
                # Remove index from deques if it is the outgoing left boundary index.
                if max_dq[0] == l:
                    max_dq.popleft()
                if min_dq[0] == l:
                    min_dq.popleft()
                l += 1
            # Update the longest subarray size.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 23. Number of Substrings Containing All Three Characters (LC 1358)
    # Given a string s consisting only of 'a', 'b', and 'c', return the number of substrings containing at least one occurrence of all these characters.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def numberOfSubstrings(self, s: str) -> int:
        count = {'a': 0, 'b': 0, 'c': 0}
        l = 0
        res = 0
        for r in range(len(s)):
            count[s[r]] += 1
            while count['a'] > 0 and count['b'] > 0 and count['c'] > 0:
                res += len(s) - r
                count[s[l]] -= 1
                l += 1
        return res

    # -----------------------------------------------------------------------
    # 24. Get Equal Substrings Within Budget (LC 1208)
    # You are given two strings s and t of the same length and an integer maxCost. Change s to t. The i-th character change costs |s[i] - t[i]|. Return the maximum length of a substring of s that can be changed to the same substring in t with a cost <= maxCost.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        l = 0
        window_cost = 0
        res = 0
        for r in range(len(s)):
            # Add transformation cost for s[r] -> t[r].
            window_cost += abs(ord(s[r]) - ord(t[r]))
            # If cost exceeds budget, shrink window from left.
            while window_cost > maxCost:
                window_cost -= abs(ord(s[l]) - ord(t[l]))
                l += 1
            # Update maximum length of substring transformation.
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 25. Max Consecutive Ones II (LC 487)
    # Given a binary array nums, return the maximum number of consecutive 1s if you can flip at most one 0. (Follow-up: if the data stream is infinite, how would you handle it?)
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        """Max Consecutive Ones II (LC 487): Use a sliding window allowing at most one 0."""
        l = 0
        zero_count = 0
        res = 0
        for r in range(len(nums)):
            # Increment zero count if current element is 0.
            if nums[r] == 0:
                zero_count += 1
            # Shrink window if zero count exceeds 1.
            while zero_count > 1:
                if nums[l] == 0:
                    zero_count -= 1
                l += 1
            res = max(res, r - l + 1)
        return res

    # -----------------------------------------------------------------------
    # 26. Grumpy Bookstore Owner (LC 1052)
    # There is a bookstore owner with customers[i] customers on minute i. The owner is grumpy on minutes marked grumpy[i] = 1 (those customers are unhappy). The owner can use a technique for minutes consecutive minutes to suppress grumpiness. Return the maximum number of satisfied customers.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def maxSatisfied(self, customers: List[int], grumpy: List[int], minutes: int) -> int:
        # Base satisfied customers (minutes bookstore owner is not grumpy).
        base = sum(c for c, g in zip(customers, grumpy) if g == 0)
        # Calculate additional satisfied customers in the first window of size minutes.
        window_gain = sum(customers[i] * grumpy[i] for i in range(minutes))
        max_gain = window_gain
        # Slide window of size minutes across the array.
        for r in range(minutes, len(customers)):
            # Add incoming minute to window gain.
            window_gain += customers[r] * grumpy[r]
            # Subtract outgoing minute from window gain.
            window_gain -= customers[r - minutes] * grumpy[r - minutes]
            # Record maximum gain from grumpy suppression.
            max_gain = max(max_gain, window_gain)
        return base + max_gain

    # -----------------------------------------------------------------------
    # 27. Minimum Swaps to Group All 1s Together II (LC 2134)
    # A swap exchanges the values at two distinct positions in a circular array. Return the minimum number of swaps required to group all the 1s together in the circular array nums.
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def minSwaps(self, nums: List[int]) -> int:
        """Minimum Swaps to Group All 1s Together II (LC 2134): Count total_ones = sum(nums)."""
        n = len(nums)
        total_ones = sum(nums)
        # If no ones exist, no swaps are needed.
        if total_ones == 0:
            return 0
        # Initialize the sliding window of size total_ones.
        window_ones = sum(nums[:total_ones])
        max_ones = window_ones
        # Slide window of size total_ones circularly.
        for r in range(total_ones, n + total_ones):
            # Add incoming circular element.
            window_ones += nums[r % n]
            # Subtract outgoing circular element.
            window_ones -= nums[(r - total_ones) % n]
            # Record maximum number of ones in any window.
            max_ones = max(max_ones, window_ones)
        # Swaps needed is the number of zeros in the window with the most ones.
        return total_ones - max_ones


if __name__ == "__main__":
    sol = TwoPointersSolutions()
    sol2 = TwoPointersSolutionsT2()

    # twoSum (sorted)
    assert sol.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert sol.twoSum([2, 3, 4], 6) == [1, 3]
    assert sol.twoSum([-1, 0], -1) == [1, 2]

    # threeSum
    assert sorted([sorted(t) for t in sol.threeSum([-1, 0, 1, 2, -1, -4])]) == [[-1, -1, 2], [-1, 0, 1]]
    assert sol.threeSum([0, 0, 0]) == [[0, 0, 0]]

    # maxArea
    assert sol.maxArea([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert sol.maxArea([1, 1]) == 1

    # sortColors (Dutch national flag)
    arr = [2, 0, 2, 1, 1, 0]
    sol.sortColors(arr)
    assert arr == [0, 0, 1, 1, 2, 2]

    # lengthOfLongestSubstring
    assert sol.lengthOfLongestSubstring("abcabcbb") == 3
    assert sol.lengthOfLongestSubstring("bbbbb") == 1
    assert sol.lengthOfLongestSubstring("pwwkew") == 3

    # findAnagrams
    assert sol.findAnagrams("cbaebabacd", "abc") == [0, 6]
    assert sol.findAnagrams("abab", "ab") == [0, 1, 2]

    # checkInclusion
    assert sol.checkInclusion("ab", "eidbaooo") == True
    assert sol.checkInclusion("ab", "eidboaoo") == False

    # characterReplacement
    assert sol2.characterReplacement("AABABBA", 1) == 4
    assert sol2.characterReplacement("ABAB", 2) == 4

    # findDuplicate (Floyd's cycle detection)
    assert sol2.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert sol2.findDuplicate([3, 1, 3, 4, 2]) == 3

    # fourSum
    assert sorted([sorted(q) for q in sol2.fourSum([1, 0, -1, 0, -2, 2], 0)]) == [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]
    assert sol2.fourSum([2, 2, 2, 2, 2], 8) == [[2, 2, 2, 2]]

    # longestOnes
    assert sol2.longestOnes([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2) == 6
    assert sol2.longestOnes([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3) == 10

    sol3 = TwoPointersSolutionsL4()

    # minOperations (LC 1658)
    assert sol3.minOperations([1, 1, 4, 2, 3], 5) == 2
    assert sol3.minOperations([5, 6, 7, 8, 9], 4) == -1
    assert sol3.minOperations([3, 2, 20, 1, 1, 3], 10) == 5
    assert sol3.minOperations([1, 1], 3) == -1

    # numberOfSubarrays (LC 1248)
    assert sol3.numberOfSubarrays([1, 1, 2, 1, 1], 3) == 2
    assert sol3.numberOfSubarrays([2, 4, 6], 1) == 0
    assert sol3.numberOfSubarrays([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2) == 16

    # maxFrequency (LC 1838)
    assert sol3.maxFrequency([1, 2, 4], 5) == 3
    assert sol3.maxFrequency([1, 4, 8, 13], 5) == 2
    assert sol3.maxFrequency([3, 9, 6], 2) == 1

    # longestSubarray (LC 1493)
    assert sol3.longestSubarray([1, 1, 0, 1]) == 3
    assert sol3.longestSubarray([0, 1, 1, 1, 0, 1, 1, 0, 1]) == 5
    assert sol3.longestSubarray([1, 1, 1]) == 2

    # longestSubarrayWithLimit (LC 1438)
    assert sol3.longestSubarrayWithLimit([8, 2, 4, 7], 4) == 2
    assert sol3.longestSubarrayWithLimit([10, 1, 2, 4, 7, 2], 5) == 4
    assert sol3.longestSubarrayWithLimit([4, 2, 2, 2, 4, 4, 2, 2], 0) == 3

    # numberOfSubstrings (LC 1358)
    assert sol3.numberOfSubstrings("abcabc") == 10
    assert sol3.numberOfSubstrings("aaacb") == 3
    assert sol3.numberOfSubstrings("abc") == 1

    # equalSubstring (LC 1208)
    assert sol3.equalSubstring("abcd", "bcdf", 3) == 3
    assert sol3.equalSubstring("abcd", "cdef", 3) == 1
    assert sol3.equalSubstring("abcd", "acde", 0) == 1

    # findMaxConsecutiveOnes (LC 487)
    assert sol3.findMaxConsecutiveOnes([1, 0, 1, 1, 0]) == 4
    assert sol3.findMaxConsecutiveOnes([1, 0, 1, 0, 1]) == 3
    assert sol3.findMaxConsecutiveOnes([1, 1, 1]) == 3

    # maxSatisfied (LC 1052)
    assert sol3.maxSatisfied([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3) == 16
    assert sol3.maxSatisfied([1], [0], 1) == 1

    # minSwaps (LC 2134)
    assert sol3.minSwaps([0, 1, 0, 1, 1, 0, 0]) == 1
    assert sol3.minSwaps([0, 1, 1, 1, 0, 0, 1, 1, 0]) == 2
    assert sol3.minSwaps([1, 1, 0, 0, 1]) == 0
    assert sol3.minSwaps([0, 0, 0]) == 0

    print("All two pointers tests passed.")
