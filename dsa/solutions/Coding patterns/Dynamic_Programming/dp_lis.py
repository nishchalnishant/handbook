from typing import List
import bisect

class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """
        Problem: Longest Increasing Subsequence
        Pattern: DP with Binary Search (O(n log n))
        """
        sub = []
        for x in nums:
            if len(sub) == 0 or sub[-1] < x:
                sub.append(x)
            else:
                idx = bisect.bisect_left(sub, x)
                sub[idx] = x
        return len(sub)

    def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
        """
        Problem: Russian Doll Envelopes
        Pattern: LIS (Sort logic important)
        """
        # Sort by width ascending, then height descending to handle same width
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        heights = [h for w, h in envelopes]
        return self.lengthOfLIS(heights)
