from typing import List
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """
        Problem: Kth Largest Element in an Array
        Difficulty: Medium
        Time Complexity: O(n log k)
        Space Complexity: O(k)
        """
        heap = []
        for n in nums:
            heapq.heappush(heap, n)
            if len(heap) > k:
                heapq.heappop(heap)
        return heap[0]
