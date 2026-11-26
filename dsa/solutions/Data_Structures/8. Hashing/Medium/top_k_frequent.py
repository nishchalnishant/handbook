from typing import List
from collections import Counter
import heapq

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Problem: Top K Frequent Elements
        Difficulty: Medium
        Time Complexity: O(n) using Bucket Sort
        Space Complexity: O(n)
        """
        count = Counter(nums)
        freq = [[] for i in range(len(nums) + 1)]
        
        for n, c in count.items():
            freq[c].append(n)
            
        res = []
        for i in range(len(freq) - 1, 0, -1):
            for n in freq[i]:
                res.append(n)
                if len(res) == k:
                    return res
        return res
