from typing import List
import math

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        """
        Problem: Max Points on a Line
        Difficulty: Hard
        Time Complexity: O(n^2)
        Space Complexity: O(n)
        """
        if len(points) <= 2: return len(points)
        
        res = 0
        for i in range(len(points)):
            slopes = {}
            for j in range(i + 1, len(points)):
                x1, y1 = points[i]
                x2, y2 = points[j]
                
                if x1 == x2:
                    m = float('inf')
                else:
                    m = (y2 - y1) / (x2 - x1)
                
                slopes[m] = slopes.get(m, 0) + 1
            
            if slopes:
                res = max(res, max(slopes.values()) + 1) # +1 for the point itself
            else:
                res = max(res, 1) # Only the point itself exists or duplicates
                
        return res
