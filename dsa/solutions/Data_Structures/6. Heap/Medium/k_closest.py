from typing import List
import heapq

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        """
        Problem: K Closest Points to Origin
        Difficulty: Medium
        Time Complexity: O(n log k)
        Space Complexity: O(k)
        """
        # Max heap of size k (store negative distance)
        maxHeap = []
        
        for x, y in points:
            dist = -(x**2 + y**2)
            heapq.heappush(maxHeap, (dist, x, y))
            if len(maxHeap) > k:
                heapq.heappop(maxHeap)
        
        return [[x, y] for (dist, x, y) in maxHeap]
