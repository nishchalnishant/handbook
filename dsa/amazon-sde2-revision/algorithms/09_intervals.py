"""
Intervals patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Not sorting the intervals first! Almost all interval problems require sorting by start time (or end time).\n- Merging logic: `interval[0] <= prev[1]` vs `<` (ask if adjacent intervals [1,2] and [2,3] merge).\n- Modifying the list while iterating.

Common Variants:
- Merge Intervals\n- Insert Interval\n- Meeting Rooms (I and II - requiring min-heap)\n- Non-overlapping intervals

General Tips & Best Practices:
- Sort by start time for merging.\n- Sort by end time for finding maximum non-overlapping intervals.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import List
import heapq
from sortedcontainers import SortedList

class IntervalSolutions:
    # -----------------------------------------------------------------------
    # 1. Merge Intervals (LC 56) — T1
    # Given an array of intervals where intervals[i] = [starti, endi], merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.
    # Example: intervals = [[1,3],[2,6],[8,10],[15,18]] → [[1,6],[8,10],[15,18]]
    # Constraints: 1 <= intervals.length <= 10^4, intervals[i].length == 2, 0 <= starti <= endi <= 10^4
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if not intervals: return []
        # Sort intervals by their start times.
        intervals.sort(key=lambda x: x[0])
        # Initialize result list with the first interval.
        res = [intervals[0]]
        for start, end in intervals[1:]:
            last_end = res[-1][1]
            # If current interval overlaps with the last merged one, merge them.
            if start <= last_end:
                res[-1][1] = max(last_end, end)
            else:
                # Otherwise, it's disjoint; start a new interval.
                res.append([start, end])
        return res

    # -----------------------------------------------------------------------
    # 2. Insert Interval (LC 57) — T1
    # You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the i^th interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval. Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary). Return intervals after the insertion. Note that you don't need to modify intervals in-place. You can make a new array and return it.
    # Example: intervals = [[1,3],[6,9]], newInterval = [2,5] → [[1,5],[6,9]]
    # Constraints: 0 <= intervals.length <= 10^4, intervals[i].length == 2, 0 <= starti <= endi <= 10^5, intervals is sorted by starti in ascending order, newInterval.length == 2, 0 <= start <= end <= 10^5
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        """Insert Interval (LC 57): Traverse the already-sorted, non-overlapping interval list once."""
        res = []
        for i in range(len(intervals)):
            # If newInterval ends before the current interval starts, we can
            # insert newInterval and append the remaining intervals.
            if newInterval[1] < intervals[i][0]:
                res.append(newInterval)
                return res + intervals[i:]
            # If newInterval starts after the current interval ends, the current
            # interval is non-overlapping and comes before newInterval.
            elif newInterval[0] > intervals[i][1]:
                res.append(intervals[i])
            else:
                # Overlap detected: merge by updating the bounds of newInterval.
                newInterval = [min(newInterval[0], intervals[i][0]), max(newInterval[1], intervals[i][1])]
        # Append the merged newInterval if it hasn't been returned yet.
        res.append(newInterval)
        return res

    # -----------------------------------------------------------------------
    # 3. Non-overlapping Intervals (LC 435) — T2
    # Given an array of intervals intervals where intervals[i] = [starti, endi], return the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping. Note that intervals which only touch at a point are non-overlapping. For example, [1, 2] and [2, 3] are non-overlapping.
    # Example: intervals = [[1,2],[2,3],[3,4],[1,3]] → 1
    # Constraints: 1 <= intervals.length <= 10^5, intervals[i].length == 2, 5 * 10^4 <= starti < endi <= 5 * 10^4
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        # Sort intervals by end times to greedily keep earliest ending intervals.
        intervals.sort(key=lambda x: x[1])
        res = 0
        prevEnd = intervals[0][1]
        for start, end in intervals[1:]:
            # If the current interval starts after or at the previous end, keep it.
            if start >= prevEnd:
                prevEnd = end
            else:
                # Overlap found: increment the count of removals.
                res += 1
        return res

    # -----------------------------------------------------------------------
    # 5. Meeting Rooms II (LC 253) — T2
    # Given an array of meeting time intervals where intervals[i] = [starti, endi], determine if a person could attend all meetings.
    # Example: intervals = [[0,30],[5,10],[15,20]] → false
    # Constraints: 0 <= intervals.length <= 10^4
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        # Sort meetings by start times.
        intervals.sort(key=lambda x: x[0])
        min_heap = []
        for i in intervals:
            # If the room with earliest end time is free, reuse it.
            if min_heap and min_heap[0] <= i[0]:
                heapq.heappop(min_heap)
            # Push the end time of the current meeting onto the heap.
            heapq.heappush(min_heap, i[1])
        # The size of the heap represents the total rooms needed simultaneously.
        return len(min_heap)

    # -----------------------------------------------------------------------
    # 6. Minimum Arrows to Burst Balloons (LC 452) — T2
    # There are some spherical balloons taped onto a flat wall that represents the XY-plane. The balloons are represented as a 2D integer array points where points[i] = [xstart, xend]. Balloons are burst if an arrow is shot at x, where xstart <= x <= xend. Return the minimum number of arrows that must be shot to burst all balloons.
    # Example: points = [[10,16],[2,8],[1,6],[7,12]] → 2
    # Constraints: 1 <= points.length <= 10^5
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def findMinArrowShots(self, points: List[List[int]]) -> int:
        if not points: return 0
        # Sort balloons by their right (end) boundary.
        points.sort(key=lambda x: x[1])
        arrows = 1
        curr_end = points[0][1]
        for start, end in points:
            # If the current balloon starts after the end of the last shot arrow range,
            # we must shoot a new arrow.
            if start > curr_end:
                arrows += 1
                curr_end = end
        return arrows

    # -----------------------------------------------------------------------
    # 7. Interval List Intersections (LC 986) — L4
    # You are given two lists of closed intervals, firstList and secondList, where firstList[i] = [starti, endi] and secondList[j] = [startj, endj]. Each list of intervals is pairwise disjoint and in sorted order. Return the intersection of these two interval lists.
    # Example: firstList = [[0,2],[5,10],[13,23],[24,25]], secondList = [[1,5],[8,12],[15,24],[25,26]] → [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
    # Constraints: 0 <= firstList.length, secondList.length <= 1000, Two sorted interval lists A and B; return all intersecting intervals, Key: always advance the pointer whose interval ends first
    # Time: O(m + n), Space: O(m + n)
    # -----------------------------------------------------------------------
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        """Interval List Intersections (LC 986): Use two pointers, one for each sorted list."""
        res = []
        i = j = 0
        # Two-pointer traversal through both lists of disjoint intervals.
        while i < len(firstList) and j < len(secondList):
            # Compute the boundary overlap.
            lo = max(firstList[i][0], secondList[j][0])
            hi = min(firstList[i][1], secondList[j][1])
            # If overlap exists, record it.
            if lo <= hi:
                res.append([lo, hi])
            # Advance pointer of the interval ending first.
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1
        return res

    # -----------------------------------------------------------------------
    # 9. My Calendar I — sorted list / BST for interval conflict detection (LC 729)
    # Implement a MyCalendarI class to store events. When a new event is booked, check if it conflicts with any existing event. Two events conflict if they overlap (not just touch). Return True if the event can be booked.
    # Time: O(log n) per booking, Space: O(n)
    # -----------------------------------------------------------------------
    def myCalendarIBook(self, calendar: SortedList, start: int, end: int) -> bool:
        # Locate the insertion point of the new event in the sorted calendar.
        idx = calendar.bisect_left((start, end))
        # Check if the predecessor event conflicts with the new event.
        if idx > 0:
            ps, pe = calendar[idx - 1]
            if ps < end and start < pe:
                return False
        # Check if the successor event conflicts with the new event.
        if idx < len(calendar):
            ns, ne = calendar[idx]
            if ns < end and start < ne:
                return False
        # No conflict found: append the new event to the calendar and return True.
        calendar.add((start, end))
        return True

    # -----------------------------------------------------------------------
    # 10. My Calendar II — double-booking detection (LC 731)
    # Implement a MyCalendarII class. A booking is accepted if it causes no triple-booking. Return True if the event can be booked without a triple.
    # Time: O(n) per booking, Space: O(n)
    # -----------------------------------------------------------------------
    def myCalendarIIBook(self, calendar: list, overlaps: list, start: int, end: int) -> bool:
        # Check if the new event conflicts with any existing double-booked regions.
        for os, oe in overlaps:
            if start < oe and os < end:
                return False
        # Record any new double-booked overlaps created by adding this event.
        for s, e in calendar:
            lo, hi = max(s, start), min(e, end)
            if lo < hi:
                overlaps.append((lo, hi))
        # Accept the event and add it to the calendar.
        calendar.append((start, end))
        return True

    # -----------------------------------------------------------------------
    # 13. Count of Smaller Numbers After Self — interval tree approach
    # NOTE: This is an alternative to the BIT/merge-sort approach; in interviews the BIT approach is more common but interval trees are conceptually related. Given integer array nums, return counts[i] = number of smaller elements to the right of nums[i]. Space: O(n)
    # Time: O(n log n) average with BST, O(n^2) worst case; BIT is preferred
    # -----------------------------------------------------------------------
    def countSmaller(self, nums: List[int]) -> List[int]:
        # Coordinate-compress the numbers by sorting unique elements.
        ranked = sorted(set(nums))
        # Map each unique value to its 1-based rank position.
        rank = {v: i + 1 for i, v in enumerate(ranked)}
        n = len(ranked)
        bit = [0] * (n + 1)

        def update(i: int) -> None:
            # Add 1 to index i and all its covering ancestors in the BIT.
            # Traverse BIT upward to add count
            while i <= n:
                bit[i] += 1
                i += i & (-i)

        def query(i: int) -> int:
            s = 0
            # Accumulate prefix sums by traversing down to 0 in the BIT.
            while i > 0:
                s += bit[i]
                i -= i & (-i)
            return s

        res = []
        # Traverse right to left to count smaller elements.
        for val in reversed(nums):
            r = rank[val]
            # Query number of elements strictly smaller than current value.
            res.append(query(r - 1))
            # Insert the current value rank into the BIT.
            update(r)
        # Reverse the result to match the original index ordering.
        return res[::-1]

    # -----------------------------------------------------------------------
    # 15. Remove Covered Intervals (LC 1288)
    # Given a list of intervals, remove all intervals that are covered by another interval. Return the number of remaining intervals. An interval [a,b] is covered by [c,d] if c <= a and b <= d.
    # Time: O(n log n), Space: O(1)
    # -----------------------------------------------------------------------
    def removeCoveredIntervals(self, intervals: List[List[int]]) -> int:
        # Sort by start ascending, then by end descending when starts are equal.
        intervals.sort(key=lambda x: (x[0], -x[1]))
        count = 0
        max_end = 0
        for start, end in intervals:
            # If current interval ends after the maximum end seen so far,
            # it is not covered by any prior interval.
            if end > max_end:
                count += 1
                max_end = end
        return count

    # -----------------------------------------------------------------------
    # 16. Divide Intervals Into Minimum Number of Groups — sweep line (LC 2406)
    # Partition intervals into the minimum number of groups such that no two intervals in the same group overlap. Return the minimum number of groups.
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def minGroups(self, intervals: List[List[int]]) -> int:
        # Extract starts and ends independently and sort them.
        starts = sorted(s for s, e in intervals)
        ends = sorted(e for s, e in intervals)
        groups = 0
        j = 0
        # Sweep through starts using two-pointer style comparison.
        for i in range(len(starts)):
            # If current start is <= earliest ending active interval,
            # we need a new group.
            if starts[i] <= ends[j]:
                groups += 1
            else:
                # Otherwise, reuse the group of the interval that ended.
                j += 1
        return groups

if __name__ == "__main__":
    import heapq
    sol = IntervalSolutions()

    # merge
    assert sol.merge([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]]
    assert sol.merge([[1,4],[4,5]]) == [[1,5]]

    # insert
    assert sol.insert([[1,3],[6,9]], [2,5]) == [[1,5],[6,9]]
    assert sol.insert([[1,2],[3,5],[6,7],[8,10],[12,16]], [4,8]) == [[1,2],[3,10],[12,16]]

    # eraseOverlapIntervals
    assert sol.eraseOverlapIntervals([[1,2],[2,3],[3,4],[1,3]]) == 1
    assert sol.eraseOverlapIntervals([[1,2],[1,2],[1,2]]) == 2

    # minMeetingRooms
    assert sol.minMeetingRooms([[0,30],[5,10],[15,20]]) == 2
    assert sol.minMeetingRooms([[7,10],[2,4]]) == 1

    # findMinArrowShots
    assert sol.findMinArrowShots([[10,16],[2,8],[1,6],[7,12]]) == 2
    assert sol.findMinArrowShots([[1,2],[3,4],[5,6],[7,8]]) == 4

    # intervalIntersection (L4 — two sorted lists)
    A = [[0,2],[5,10],[13,23],[24,25]]
    B = [[1,5],[8,12],[15,24],[25,26]]
    assert sol.intervalIntersection(A, B) == [[1,2],[5,5],[8,10],[15,23],[24,24],[25,25]]
    assert sol.intervalIntersection([], [[1,3]]) == []

    # myCalendarIBook (LC 729)
    cal1 = SortedList()
    assert sol.myCalendarIBook(cal1, 10, 20) == True
    assert sol.myCalendarIBook(cal1, 15, 25) == False
    assert sol.myCalendarIBook(cal1, 20, 30) == True

    # myCalendarIIBook (LC 731)
    cal2, overlaps2 = [], []
    assert sol.myCalendarIIBook(cal2, overlaps2, 10, 20) == True
    assert sol.myCalendarIIBook(cal2, overlaps2, 50, 60) == True
    assert sol.myCalendarIIBook(cal2, overlaps2, 10, 40) == True
    assert sol.myCalendarIIBook(cal2, overlaps2, 5, 15) == False
    assert sol.myCalendarIIBook(cal2, overlaps2, 5, 10) == True
    assert sol.myCalendarIIBook(cal2, overlaps2, 25, 55) == True

    # countSmaller (BIT / interval tree alt)
    assert sol.countSmaller([5, 2, 6, 1]) == [2, 1, 1, 0]
    assert sol.countSmaller([-1]) == [0]
    assert sol.countSmaller([-1, -1]) == [0, 0]

    # removeCoveredIntervals (LC 1288)
    assert sol.removeCoveredIntervals([[1,4],[3,6],[2,8]]) == 2
    assert sol.removeCoveredIntervals([[1,4],[2,3]]) == 1

    # minGroups (LC 2406)
    assert sol.minGroups([[5,10],[6,8],[1,5],[2,3],[1,10]]) == 3
    assert sol.minGroups([[1,3],[5,6],[8,10],[11,13]]) == 1

    print("All interval tests passed.")
