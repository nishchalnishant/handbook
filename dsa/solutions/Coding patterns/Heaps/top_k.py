from typing import List
import heapq
from collections import Counter

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Problem: Kth Largest Element in an Array
        Pattern: Heap (Min Heap of size K) or QuickSelect
        """
        heap = []
        for n in nums:
            heapq.heappush(heap, n)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]

    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """
        Problem: Top K Frequent Elements
        Pattern: Header (or Bucket Sort for O(n))
        """
        count = Counter(nums)
        # heapq.nlargest(k, count.keys(), key=count.get)
        heap = []
        for num, freq in count.items():
            heapq.heappush(heap, (freq, num))
            if len(heap) > k:
                heapq.heappop(heap)
        return [pair[1] for pair in heap]
