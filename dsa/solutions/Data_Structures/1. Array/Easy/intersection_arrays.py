from typing import List
from collections import Counter

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        Problem: Intersection of Two Arrays II
        Difficulty: Easy
        Time Complexity: O(n + m)
        Space Complexity: O(min(n, m))
        """
        if len(nums1) > len(nums2):
            return self.intersect(nums2, nums1)
            
        cnt = Counter(nums1)
        res = []
        for x in nums2:
            if cnt[x] > 0:
                res.append(x)
                cnt[x] -= 1
        return res
