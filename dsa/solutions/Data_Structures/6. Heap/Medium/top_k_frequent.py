from typing import List
from collections import Counter
import heapq

class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Problem: Top K Frequent Elements
        Difficulty: Medium
        Time Complexity: O(n log k)
        Space Complexity: O(n)
        """
        count = Counter(nums)
        heap = []
        
        for num, freq in count.items():
            heapq.heappush(heap, (freq, num))
            if len(heap) > k:
                heapq.heappop(heap)
                
        return [pair[1] for pair in heap]
