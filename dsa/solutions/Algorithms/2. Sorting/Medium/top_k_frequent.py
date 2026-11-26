from typing import List
import heapq
from collections import Counter

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Problem: Top K Frequent Elements
        Difficulty: Medium
        Time Complexity: O(k log n)
        Space Complexity: O(n)
        """
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)
