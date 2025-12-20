from typing import List

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        """
        Problem: Non-overlapping Intervals (Activity Selection)
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(1) (excluding sort)
        """
        if not intervals: return 0
        
        # Sort by end time
        intervals.sort(key=lambda x: x[1])
        
        end = intervals[0][1]
        count = 1 # Keep the first one
        
        for i in range(1, len(intervals)):
            if intervals[i][0] >= end:
                count += 1
                end = intervals[i][1]
        
        # We want to remove the ones that don't fit
        # So total - max_non_overlapping
        return len(intervals) - count

    def maxActivities(self, start: List[int], finish: List[int]) -> int:
        """
        Classic Activity Selection (Maximize count)
        """
        activities = sorted(zip(start, finish), key=lambda x: x[1])
        count = 1
        end = activities[0][1]
        
        for i in range(1, len(activities)):
            if activities[i][0] >= end:
                count += 1
                end = activities[i][1]
        return count
