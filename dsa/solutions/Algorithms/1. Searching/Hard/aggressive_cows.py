from typing import List

class Solution:
    def aggressiveCows(self, stalls: List[int], k: int) -> int:
        """
        Problem: Aggressive Cows
        Difficulty: Hard (Binary Search on Answer)
        Time Complexity: O(n log n)
        Space Complexity: O(1) (excluding sort)
        """
        stalls.sort()
        
        def canPlace(dist):
            cows = 1
            last = stalls[0]
            for i in range(1, len(stalls)):
                if stalls[i] - last >= dist:
                    cows += 1
                    last = stalls[i]
                    if cows >= k:
                        return True
            return False
            
        l, r = 1, stalls[-1] - stalls[0]
        res = 0
        while l <= r:
            mid = (l + r) // 2
            if canPlace(mid):
                res = mid
                l = mid + 1
            else:
                r = mid - 1
        return res
