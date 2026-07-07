"""
Sliding Window patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Shrinking the window too early or too late (while loop condition is crucial).\n- Forgetting to update the optimal answer (max/min length) either inside or outside the shrink loop.\n- Handling negative numbers in subarray sums (standard sliding window fails, need prefix sums).

Common Variants:
- Fixed length window (e.g., Maximum Average Subarray)\n- Variable length window (e.g., Longest Substring Without Repeating Characters)\n- At most K distinct elements

General Tips & Best Practices:
- Use a frequency map or counter to track window state.\n- The pattern is always: Expand right, update state, while invalid: shrink left, update state.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from collections import Counter, defaultdict
from typing import List

from sortedcontainers import SortedList


class SlidingWindowSolutions:

    # -----------------------------------------------------------------------
    # 1. Minimum Window Substring (LC 76) — T3
    # find smallest window in s containing all chars of t
    # Time: O(|s| + |t|)
    # -----------------------------------------------------------------------
    def min_window(self, s: str, t: str) -> str:
        """Pattern: VARIABLE window."""
        if not t or not s:
            return ""
        need = Counter(t)
        required = len(need)
        formed = 0
        window = {}
        l = 0
        best = (float("inf"), 0, 0)  # (length, left, right)
        for r, ch in enumerate(s):
            # Add current character to window frequency map.
            window[ch] = window.get(ch, 0) + 1
            # If current character frequency matches the target frequency in need, increment formed count.
            if ch in need and window[ch] == need[ch]:
                formed += 1
            # Shrink window from left as long as all required character frequencies are satisfied.
            while formed == required:
                # Update best window if current window is smaller.
                if r - l + 1 < best[0]:
                    best = (r - l + 1, l, r)
                lch = s[l]
                # Remove left character from window frequency.
                window[lch] -= 1
                # If window count of left character falls below target frequency, decrement formed count.
                if lch in need and window[lch] < need[lch]:
                    formed -= 1
                l += 1
        return "" if best[0] == float("inf") else s[best[1]: best[2] + 1]

    # -----------------------------------------------------------------------
    # 2. Longest Substring Without Repeating Characters (LC 3) — T2
    # no duplicate chars in window
    # Time: O(n)
    # -----------------------------------------------------------------------
    def length_of_longest_substring(self, s: str) -> int:
        """Pattern: VARIABLE window."""
        seen = set()
        l = best = 0
        for r, ch in enumerate(s):
            # If current character is a duplicate, shrink window from left until duplicate is removed.
            while ch in seen:
                seen.remove(s[l])
                l += 1
            seen.add(ch)
            best = max(best, r - l + 1)
        return best

    # -----------------------------------------------------------------------
    # 3. Longest Repeating Character Replacement (LC 424) — T3
    # can replace at most k chars; maximize window with one dominant char
    # Time: O(n)
    # -----------------------------------------------------------------------
    def character_replacement(self, s: str, k: int) -> int:
        """Pattern: VARIABLE window."""
        count = defaultdict(int)
        max_freq = l = best = 0
        for r, ch in enumerate(s):
            # Record frequency of character ch.
            count[ch] += 1
            # Maintain the maximum frequency of any character in the current window.
            max_freq = max(max_freq, count[ch])
            # If operations needed (window_size - max_freq) exceeds k, shrink window from left.
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1
                l += 1
            best = max(best, r - l + 1)
        return best

    # -----------------------------------------------------------------------
    # 4. Permutation in String (LC 567) — T2
    # does s2 contain a permutation of s1?
    # Time: O(|s1| + |s2|)
    # -----------------------------------------------------------------------
    def check_inclusion(self, s1: str, s2: str) -> bool:
        """Pattern: FIXED window of size len(s1)."""
        if len(s1) > len(s2):
            return False
        need = Counter(s1)
        # Initialize window Counter with the first len(s1) elements.
        window = Counter(s2[: len(s1)])
        # Check if initial window matches s1.
        if window == need:
            return True
        # Slide window across s2.
        for r in range(len(s1), len(s2)):
            rc, lc = s2[r], s2[r - len(s1)]
            # Add incoming character rc, remove outgoing character lc.
            window[rc] += 1
            window[lc] -= 1
            # Clean up zero-count key to keep window directly comparable.
            if window[lc] == 0:
                del window[lc]
            if window == need:
                return True
        return False

    # -----------------------------------------------------------------------
    # 5. Find All Anagrams in a String (LC 438) — T2
    # return start indices of all anagram windows
    # Time: O(|s| + |p|)
    # -----------------------------------------------------------------------
    def find_anagrams(self, s: str, p: str) -> List[int]:
        """Pattern: FIXED window of size len(p)."""
        k = len(p)
        need = Counter(p)
        # Initialize window Counter with first k elements.
        window = Counter(s[:k])
        res = [0] if window == need else []
        # Slide window across s.
        for r in range(k, len(s)):
            rc, lc = s[r], s[r - k]
            # Add incoming character rc, remove outgoing character lc.
            window[rc] += 1
            window[lc] -= 1
            # Clean up zero-count key.
            if window[lc] == 0:
                del window[lc]
            # If counters match, record window start index.
            if window == need:
                res.append(r - k + 1)
        return res

    # -----------------------------------------------------------------------
    # 6. Maximum Sum Subarray of Size K (T1) — T1
    # fixed-size window sum
    # Time: O(n)
    # -----------------------------------------------------------------------
    def max_sum_subarray_k(self, nums: List[int], k: int) -> int:
        """Pattern: FIXED window of size k."""
        # Sum of the first window.
        window_sum = sum(nums[:k])
        best = window_sum
        # Slide window of size k across nums.
        for r in range(k, len(nums)):
            # Add incoming element, subtract outgoing element.
            window_sum += nums[r] - nums[r - k]
            best = max(best, window_sum)
        return best

    # -----------------------------------------------------------------------
    # 7. Count of Anagrams (LC 567 variant)
    # count of all anagram occurrences of p in s (not just existence)
    # Time: O(|s| + |p|)
    # -----------------------------------------------------------------------
    def count_anagrams(self, s: str, p: str) -> int:
        """Pattern: FIXED window of size len(p)."""
        k = len(p)
        if k > len(s):
            return 0
        need = Counter(p)
        # Initialize window Counter with first k elements.
        window = Counter(s[:k])
        count = 1 if window == need else 0
        # Slide window across s.
        for r in range(k, len(s)):
            rc, lc = s[r], s[r - k]
            # Add incoming character rc, remove outgoing character lc.
            window[rc] += 1
            window[lc] -= 1
            # Clean up zero-count key.
            if window[lc] == 0:
                del window[lc]
            if window == need:
                count += 1
        return count

    # -----------------------------------------------------------------------
    # 8. Minimum Size Subarray Sum (LC 209) — T2
    # smallest contiguous subarray with sum >= target
    # Time: O(n)
    # -----------------------------------------------------------------------
    def min_sub_array_len(self, target: int, nums: List[int]) -> int:
        """Pattern: VARIABLE window."""
        l = window_sum = 0
        best = float("inf")
        for r in range(len(nums)):
            window_sum += nums[r]
            # Shrink window from left while current sum is at least target.
            while window_sum >= target:
                best = min(best, r - l + 1)
                window_sum -= nums[l]
                l += 1
        return 0 if best == float("inf") else best

    # -----------------------------------------------------------------------
    # 9. Subarray Product Less Than K (LC 713) — T2
    # count contiguous subarrays with product strictly < k
    # Time: O(n)
    # -----------------------------------------------------------------------
    def num_subarray_product_less_than_k(self, nums: List[int], k: int) -> int:
        """Pattern: VARIABLE window."""
        if k <= 1:
            return 0
        prod = l = count = 0
        prod = 1
        for r in range(len(nums)):
            prod *= nums[r]
            # Shrink window from left while product is at least k.
            while prod >= k:
                prod //= nums[l]
                l += 1
            # Add the number of valid subarrays ending at index r.
            count += r - l + 1
        return count

    # -----------------------------------------------------------------------
    # 10. Longest Subarray with Sum <= K (T2) — general template
    # works for non-negative integers
    # Time: O(n)
    # -----------------------------------------------------------------------
    def longest_subarray_sum_at_most_k(self, nums: List[int], k: int) -> int:
        """Pattern: VARIABLE window."""
        l = window_sum = best = 0
        for r in range(len(nums)):
            window_sum += nums[r]
            # Shrink window from left if sum exceeds k.
            while window_sum > k and l <= r:
                window_sum -= nums[l]
                l += 1
            best = max(best, r - l + 1)
        return best

    # -----------------------------------------------------------------------
    # 11. Maximum Consecutive Ones III (LC 1004) — T2
    # flip at most k zeros; find longest 1-run
    # Time: O(n)
    # -----------------------------------------------------------------------
    def longest_ones(self, nums: List[int], k: int) -> int:
        """Pattern: VARIABLE window."""
        zeros = l = best = 0
        for r in range(len(nums)):
            # If current element is 0, increment zeros count.
            if nums[r] == 0:
                zeros += 1
            # If zeros exceed limit k, shrink window from left.
            while zeros > k:
                if nums[l] == 0:
                    zeros -= 1
                l += 1
            # Update the longest window found.
            best = max(best, r - l + 1)
        return best

    # -----------------------------------------------------------------------
    # 12. Fruit Into Baskets (LC 904) — T2
    # at most 2 distinct values in window; max window length
    # Time: O(n)
    # -----------------------------------------------------------------------
    def total_fruit(self, fruits: List[int]) -> int:
        """Pattern: VARIABLE window, at-most-2-distinct constraint."""
        basket: dict = {}
        l = best = 0
        for r in range(len(fruits)):
            # Add current fruit type to basket.
            basket[fruits[r]] = basket.get(fruits[r], 0) + 1
            # If basket contains more than 2 distinct fruit types, shrink window from left.
            while len(basket) > 2:
                lf = fruits[l]
                basket[lf] -= 1
                if basket[lf] == 0:
                    del basket[lf]
                l += 1
            # Update maximum fruits we can collect.
            best = max(best, r - l + 1)
        return best

    # -----------------------------------------------------------------------
    # 13. Subarrays with K Different Integers (LC 992) — T3
    # count subarrays with exactly k distinct values
    # Time: O(n)
    # -----------------------------------------------------------------------
    def subarrays_with_k_distinct(self, nums: List[int], k: int) -> int:
        def at_most(k: int) -> int:
            """Pattern: VARIABLE window, exact-K trick."""
            count: dict = {}
            l = res = 0
            for r in range(len(nums)):
                # Increment count for current element.
                count[nums[r]] = count.get(nums[r], 0) + 1
                # Shrink window if distinct elements exceed k.
                while len(count) > k:
                    lv = nums[l]
                    count[lv] -= 1
                    if count[lv] == 0:
                        del count[lv]
                    l += 1
                # Add all valid subarrays ending at index r.
                res += r - l + 1
            return res

        return at_most(k) - at_most(k - 1)

    # -----------------------------------------------------------------------
    # 14. Minimum Operations to Reduce X to Zero (LC 1658) — T3
    # remove elements from either end summing to x; min removals
    # Time: O(n)
    # -----------------------------------------------------------------------
    def min_operations(self, nums: List[int], x: int) -> int:
        """Pattern: VARIABLE window (complement)."""
        target = sum(nums) - x
        if target < 0:
            return -1
        if target == 0:
            return len(nums)
        l = window_sum = 0
        best = -1
        for r in range(len(nums)):
            window_sum += nums[r]
            # Shrink window from left if window sum exceeds target.
            while window_sum > target and l <= r:
                window_sum -= nums[l]
                l += 1
            # If window sum matches target, record maximum window size.
            if window_sum == target:
                best = max(best, r - l + 1)
        return -1 if best == -1 else len(nums) - best

    # -----------------------------------------------------------------------
    # 15. Maximum Erasure Value (LC 1698) — T2
    # max sum subarray with all unique elements
    # Time: O(n)
    # -----------------------------------------------------------------------
    def maximum_unique_subarray(self, nums: List[int]) -> int:
        """Pattern: VARIABLE window, uniqueness constraint via set."""
        seen = set()
        l = window_sum = best = 0
        for r in range(len(nums)):
            # If current element is duplicate, shrink window from left until uniqueness is restored.
            while nums[r] in seen:
                seen.remove(nums[l])
                window_sum -= nums[l]
                l += 1
            seen.add(nums[r])
            window_sum += nums[r]
            best = max(best, window_sum)
        return best

    # -----------------------------------------------------------------------
    # 16. Longest Turbulent Subarray (LC 978) — T2
    # alternating comparison signs (>, <, >, < ...)
    # Time: O(n)
    # -----------------------------------------------------------------------
    def max_turbulence_size(self, arr: List[int]) -> int:
        """Pattern: VARIABLE window."""
        if len(arr) == 1:
            return 1
        l = best = 1
        prev = 0  # -1 for <, 0 for =, 1 for >
        for r in range(1, len(arr)):
            # Determine sign of current comparison.
            cur = (arr[r] > arr[r - 1]) - (arr[r] < arr[r - 1])  # sign
            # If turbulence is broken (same direction or flat segment).
            if cur == 0 or cur == prev:
                # Reset left pointer depending on whether it was a flat segment.
                if cur != 0:
                    l = r - 1
                else:
                    l = r
            best = max(best, r - l + 1)
            prev = cur
        return best

    # -----------------------------------------------------------------------
    # 17. Number of Substrings Containing All Three Characters (LC 1358) — T2
    # count substrings with at least one a, b, c
    # Time: O(n)
    # -----------------------------------------------------------------------
    def number_of_substrings(self, s: str) -> int:
        """Pattern: VARIABLE window (count from right)."""
        last = {"a": -1, "b": -1, "c": -1}
        count = 0
        for r, ch in enumerate(s):
            # Update last seen index of the character.
            last[ch] = r
            # Add all valid starting positions (from index 0 up to min_last).
            count += 1 + min(last.values())
        return count

    # -----------------------------------------------------------------------
    # 18. Replace the Substring for Balanced String (LC 1234) — T3
    # string with Q,W,E,R; replace min chars so each appears n/4 times
    # Time: O(n)
    # -----------------------------------------------------------------------
    def balanced_string(self, s: str) -> int:
        """Pattern: VARIABLE window (find minimum window to replace)."""
        n = len(s)
        k = n // 4
        count = Counter(s)
        # If already balanced
        if all(count[c] == k for c in "QWER"):
            return 0
        res = n
        l = 0
        for r in range(n):
            # Decrement outside count as s[r] goes inside the window.
            count[s[r]] -= 1  # remove from outside (inside window)
            # Shrink window from left as long as characters outside window satisfy quota.
            while l <= r and all(count[c] <= k for c in "QWER"):
                res = min(res, r - l + 1)
                # Increment outside count as s[l] exits window.
                count[s[l]] += 1  # add back to outside
                l += 1
        return res

    # -----------------------------------------------------------------------
    # 19. Maximum Consecutive Ones III — fixed window form (LC 1004 variant) — T2
    # same as #11 but shown as FIXED-style monotonic shrink
    # Time: O(n)
    # -----------------------------------------------------------------------
    def longest_ones_fixed_style(self, nums: List[int], k: int) -> int:
        """Pattern: FIXED-style variable window (monotonic shrink — window never"""
        zeros = l = 0
        for r in range(len(nums)):
            # Increment zero count.
            if nums[r] == 0:
                zeros += 1
            # If zeros exceed limit, slide left boundary forward.
            if zeros > k:
                if nums[l] == 0:
                    zeros -= 1
                l += 1
        # Window size len(nums) - l is the max size reached.
        return len(nums) - l

    # -----------------------------------------------------------------------
    # 20. Sliding Window Median (LC 480) — T3
    # median of every window of size k
    # Time: O(n log k)
    # -----------------------------------------------------------------------
    def median_sliding_window(self, nums: List[int], k: int) -> List[float]:
        """Pattern: FIXED window of size k."""
        window: SortedList = SortedList()
        res: List[float] = []
        for i, n in enumerate(nums):
            # Add incoming element.
            window.add(n)
            # Remove element falling out of window.
            if len(window) > k:
                window.remove(nums[i - k])
            # If window is complete, calculate median.
            if len(window) == k:
                # Odd size window: middle element.
                if k & 1:
                    res.append(float(window[k // 2]))
                # Even size window: average of two middle elements.
                else:
                    res.append((window[k // 2 - 1] + window[k // 2]) / 2.0)
        return res


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sol = SlidingWindowSolutions()
    failures = []

    def check(name, got, expected):
        """Predicate helper used to validate a candidate state or answer."""
        if got != expected:
            failures.append(f"FAIL {name}: got {got!r}, expected {expected!r}")

    # 1. min_window
    check("min_window basic", sol.min_window("ADOBECODEBANC", "ABC"), "BANC")
    check("min_window single", sol.min_window("a", "a"), "a")
    check("min_window impossible", sol.min_window("a", "aa"), "")

    # 2. length_of_longest_substring
    check("longest_no_repeat abcabcbb", sol.length_of_longest_substring("abcabcbb"), 3)
    check("longest_no_repeat bbbbb", sol.length_of_longest_substring("bbbbb"), 1)
    check("longest_no_repeat pwwkew", sol.length_of_longest_substring("pwwkew"), 3)

    # 3. character_replacement
    check("char_replacement ABAB 2", sol.character_replacement("ABAB", 2), 4)
    check("char_replacement AABABBA 1", sol.character_replacement("AABABBA", 1), 4)

    # 4. check_inclusion
    check("check_inclusion ab s1=ab s2=eidbaooo", sol.check_inclusion("ab", "eidbaooo"), True)
    check("check_inclusion ab s1=ab s2=eidboaoo", sol.check_inclusion("ab", "eidboaoo"), False)

    # 5. find_anagrams
    check("find_anagrams cbaebabacd abc", sol.find_anagrams("cbaebabacd", "abc"), [0, 6])
    check("find_anagrams abab ab", sol.find_anagrams("abab", "ab"), [0, 1, 2])

    # 6. max_sum_subarray_k
    check("max_sum_k basic", sol.max_sum_subarray_k([2, 1, 5, 1, 3, 2], 3), 9)

    # 7. count_anagrams
    check("count_anagrams", sol.count_anagrams("cbaebabacd", "abc"), 2)

    # 8. min_sub_array_len
    check("min_subarray_sum 7 [2,3,1,2,4,3]", sol.min_sub_array_len(7, [2, 3, 1, 2, 4, 3]), 2)
    check("min_subarray_sum no solution", sol.min_sub_array_len(100, [1, 2, 3]), 0)

    # 9. num_subarray_product_less_than_k
    check("product<k [10,5,2,6] k=100", sol.num_subarray_product_less_than_k([10, 5, 2, 6], 100), 8)

    # 10. longest_subarray_sum_at_most_k
    check("longest_sum<=k", sol.longest_subarray_sum_at_most_k([1, 2, 3, 4], 5), 2)

    # 11. longest_ones
    check("longest_ones [1,1,1,0,0,0,1,1,1,1,0] k=2",
          sol.longest_ones([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), 6)

    # 12. total_fruit
    check("total_fruit [1,2,1]", sol.total_fruit([1, 2, 1]), 3)
    check("total_fruit [0,1,2,2]", sol.total_fruit([0, 1, 2, 2]), 3)
    check("total_fruit [1,2,3,2,2]", sol.total_fruit([1, 2, 3, 2, 2]), 4)

    # 13. subarrays_with_k_distinct
    check("k_distinct [1,2,1,2,3] k=2", sol.subarrays_with_k_distinct([1, 2, 1, 2, 3], 2), 7)
    check("k_distinct [1,2,1,3,4] k=3", sol.subarrays_with_k_distinct([1, 2, 1, 3, 4], 3), 3)

    # 14. min_operations
    check("min_ops [1,1,4,2,3] x=5", sol.min_operations([1, 1, 4, 2, 3], 5), 2)
    check("min_ops [5,6,7,8,9] x=4", sol.min_operations([5, 6, 7, 8, 9], 4), -1)
    check("min_ops [3,2,20,1,1,3] x=10", sol.min_operations([3, 2, 20, 1, 1, 3], 10), 5)

    # 15. maximum_unique_subarray
    check("max_erasure [4,2,4,5,6]", sol.maximum_unique_subarray([4, 2, 4, 5, 6]), 17)
    check("max_erasure [5,2,1,2,5,2,1,2,5]", sol.maximum_unique_subarray([5, 2, 1, 2, 5, 2, 1, 2, 5]), 8)

    # 16. max_turbulence_size
    check("turbulent [9,4,2,10,7,8,8,1,9]", sol.max_turbulence_size([9, 4, 2, 10, 7, 8, 8, 1, 9]), 5)
    check("turbulent [4,8,12,16]", sol.max_turbulence_size([4, 8, 12, 16]), 2)
    check("turbulent [100]", sol.max_turbulence_size([100]), 1)

    # 17. number_of_substrings
    check("substrings_abc abcabc", sol.number_of_substrings("abcabc"), 10)
    check("substrings_abc aaacb", sol.number_of_substrings("aaacb"), 3)

    # 18. balanced_string
    check("balanced QWER", sol.balanced_string("QWER"), 0)
    check("balanced QQWE", sol.balanced_string("QQWE"), 1)
    check("balanced QQQW", sol.balanced_string("QQQW"), 2)
    check("balanced QQQQ", sol.balanced_string("QQQQ"), 3)

    # 19. longest_ones_fixed_style (same answers as #11)
    check("longest_ones_fixed [1,1,1,0,0,0,1,1,1,1,0] k=2",
          sol.longest_ones_fixed_style([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), 6)

    # 20. sliding window median
    check("median [1,3,-1,-3,5,3,6,7] k=3",
          sol.median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3),
          [1.0, -1.0, -1.0, 3.0, 5.0, 6.0])
    check("median [1,2] k=1",
          sol.median_sliding_window([1, 2], 1),
          [1.0, 2.0])

    if failures:
        for f in failures:
            print(f)
        raise SystemExit(1)
    else:
        print("ALL TESTS PASSED")
