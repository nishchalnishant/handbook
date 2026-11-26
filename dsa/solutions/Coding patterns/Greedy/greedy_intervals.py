from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        Problem: Non-overlapping Intervals
        Pattern: Greedy (Sort by end time)
        """
        intervals.sort(key=lambda x: x[1])
        res = 0
        end = float("-inf")
        
        for s, e in intervals:
            if s >= end:
                end = e
            else:
                res += 1
        return res

    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Problem: Merge Intervals
        Pattern: Greedy (Sort by start time)
        """
        intervals.sort(key=lambda x: x[0])
        res = [intervals[0]]
        
        for start, end in intervals[1:]:
            lastEnd = res[-1][1]
            if start <= lastEnd:
                res[-1][1] = max(lastEnd, end)
            else:
                res.append([start, end])
        return res
