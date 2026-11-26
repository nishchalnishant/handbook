from typing import List
import math

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """
        Problem: Koko Eating Bananas
        Pattern: Binary Search on Answer
        """
        l, r = 1, max(piles)
        res = r
        
        while l <= r:
            k = (l + r) // 2
            hours = 0
            for p in piles:
                hours += math.ceil(p / k)
            
            if hours <= h:
                res = min(res, k)
                r = k - 1
            else:
                l = k + 1
        return res

    def shipWithinDays(self, weights: List[int], days: int) -> int:
        """
        Problem: Capacity To Ship Packages Within D Days
        Pattern: Binary Search on Answer
        """
        l, r = max(weights), sum(weights)
        res = r
        
        while l <= r:
            cap = (l + r) // 2
            if self.canShip(cap, weights, days):
                res = min(res, cap)
                r = cap - 1
            else:
                l = cap + 1
        return res
    
    def canShip(self, cap, weights, days):
        ships = 1
        currCap = 0
        for w in weights:
            if currCap + w > cap:
                ships += 1
                currCap = 0
            currCap += w
        return ships <= days
