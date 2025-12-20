from typing import List

class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        """
        Problem: Maximum Gap
        Difficulty: Hard
        Time Complexity: O(n) (Bucket Sort/Pigeonhole Principle)
        Space Complexity: O(n)
        """
        if len(nums) < 2:
            return 0
        
        minVal, maxVal = min(nums), max(nums)
        if minVal == maxVal:
            return 0
            
        n = len(nums)
        bucketSize = max(1, (maxVal - minVal) // (n - 1))
        bucketCount = (maxVal - minVal) // bucketSize + 1
        
        buckets = [[float("inf"), float("-inf")] for _ in range(bucketCount)]
        
        for n in nums:
            idx = (n - minVal) // bucketSize
            buckets[idx][0] = min(buckets[idx][0], n)
            buckets[idx][1] = max(buckets[idx][1], n)
            
        prevMax = minVal
        maxGap = 0
        
        for i in range(bucketCount):
            if buckets[i][0] == float("inf"):
                continue # Empty bucket
            
            maxGap = max(maxGap, buckets[i][0] - prevMax)
            prevMax = buckets[i][1]
            
        return maxGap
