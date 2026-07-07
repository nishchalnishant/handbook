"""
Heap / Priority Queue patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Python's `heapq` is a Min-Heap. For a Max-Heap, you must negate the values.\n- Pushing tuples: `heapq` will compare the first element, then the second. If the second element is an object that doesn't support comparison, it will crash.\n- Modifying elements inside the heap without re-heapifying.

Common Variants:
- Top K elements (maintain a heap of size K)\n- Merge K sorted lists\n- Two Heaps pattern (Find Median from Data Stream)

General Tips & Best Practices:
- To find K largest elements, use a Min-Heap of size K (O(N log K)).\n- To find K smallest elements, use a Max-Heap of size K.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

import heapq
from typing import List
from collections import Counter, defaultdict

class HeapSolutions:
    # -----------------------------------------------------------------------
    # 1. Kth Largest Element (LC 215) — T1
    # Given an integer array nums and an integer k, return the kth largest element in the array. Note that it is the kth largest element in the sorted order, not the kth distinct element.
    # Example: nums = [3,2,1,5,6,4], k = 2 → 5
    # Constraints: 1 <= k <= nums.length <= 10^5
    # Time: O(n log k), Space: O(k)
    # -----------------------------------------------------------------------
    def findKthLargest(self, nums: List[int], k: int) -> int:
        # Initialize a min-heap with the first k elements
        min_heap = nums[:k]
        heapq.heapify(min_heap)
        # Process the remaining elements
        for num in nums[k:]:
            # If the current element is larger than the minimum, replace it
            if num > min_heap[0]:
                heapq.heapreplace(min_heap, num)
        # The root is now the kth largest element
        return min_heap[0]

    # -----------------------------------------------------------------------
    # 2. K Closest Points to Origin (LC 973) — T1
    # Given an array of points where points[i] = [xi, yi] represents a point on the X-Y plane and an integer k, return the k closest points to the origin (0, 0). The distance between two points on the X-Y plane is the Euclidean distance (i.e., √(x1 - x2)^2 + (y1 You may return the answer in any order. The answer is guaranteed to be unique (except for the order that it is in).
    # Example: points = [[1,3],[-2,2]], k = 1 → [[-2,2]]
    # Constraints: 1 <= k <= points.length <= 10^4, 10^4 <= xi, yi <= 10^4
    # Time: O(n log k), Space: O(k)
    # -----------------------------------------------------------------------
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        # Max-heap represented by storing negated squared distances
        max_heap = []
        for x, y in points:
            # Squared Euclidean distance from the origin (negated for max-heap behavior)
            dist = -(x*x + y*y)
            # Push to heap if size is less than k
            if len(max_heap) < k:
                heapq.heappush(max_heap, (dist, x, y))
            # Otherwise, push-pop to keep only the k smallest distances
            else:
                heapq.heappushpop(max_heap, (dist, x, y))
        # Reconstruct coordinates from heap elements
        return [[x, y] for dist, x, y in max_heap]

    # -----------------------------------------------------------------------
    # 3. Top K Frequent Elements (LC 347) — T1
    # Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.
    # Example: nums = [1,1,1,2,2,3], k = 2 → [1,2]
    # Constraints: 1 <= nums.length <= 10^5, 10^4 <= nums[i] <= 10^4, k is in the range [1, the number of unique elements in the array], It is guaranteed that the answer is unique, Follow up: Your algorithm's time complexity must be better than O(n log n), where n is the array's, size
    # Time: O(n log k), Space: O(n)
    # -----------------------------------------------------------------------
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = Counter(nums)
        return heapq.nlargest(k, count.keys(), key=count.get)

    # -----------------------------------------------------------------------
    # 4. Find Median from Stream (LC 295) — T1
    # The median is the middle value in an ordered integer list. Implement the MedianFinder class to add integers to the data stream and return the median.
    # Time: O(log n) per addNum, O(1) per findMedian, Space: O(n)
    # -----------------------------------------------------------------------
    class MedianFinder:
        def __init__(self):
            self.lo = []  # max-heap
            self.hi = []  # min-heap

        def addNum(self, num: int) -> None:
            # Push negated number to max-heap (lo)
            heapq.heappush(self.lo, -num)
            # Rebalance to min-heap (hi)
            heapq.heappush(self.hi, -heapq.heappop(self.lo))

            # Maintain sizing constraint len(lo) >= len(hi)
            if len(self.lo) < len(self.hi):
                heapq.heappush(self.lo, -heapq.heappop(self.hi))

        def findMedian(self) -> float:
            # If total elements is odd, return root of lo
            if len(self.lo) > len(self.hi):
                return -self.lo[0]
            # If even, return average of both roots
            return (-self.lo[0] + self.hi[0]) / 2.0

    # -----------------------------------------------------------------------
    def leastInterval(self, tasks: List[str], n: int) -> int:
        # Count frequencies of each task
        counts = Counter(tasks)
        # Find maximum frequency of any task
        max_freq = max(counts.values())
        # Count how many tasks share the maximum frequency
        max_freq_tasks = sum(1 for v in counts.values() if v == max_freq)
        # Return maximum of total task count and the slots required by bottleneck tasks
        return max(len(tasks), (max_freq - 1) * (n + 1) + max_freq_tasks)

    # -----------------------------------------------------------------------
    # 6. Reorganize String (LC 767) — T1
    # Given a string s, rearrange the characters of s so that any two adjacent characters are not the same. Return any possible rearrangement of s or return "" if not possible.
    # Example: s = "aab" → "aba"
    # Constraints: 1 <= s.length <= 500, s consists of lowercase English letters
    # Time: O(n log k), Space: O(k)
    # -----------------------------------------------------------------------
    def reorganizeString(self, s: str) -> str:
        # Count character frequencies
        count = Counter(s)
        # Build max-heap of negated frequencies and characters
        max_heap = [(-freq, char) for char, freq in count.items()]
        heapq.heapify(max_heap)

        # Track the previously processed character to avoid adjacent duplicates
        prev_freq, prev_char = 0, ""
        res = []

        # Process characters from the heap
        while max_heap:
            freq, char = heapq.heappop(max_heap)
            res.append(char)

            # Re-enqueue the previous character if it still has occurrences left
            if prev_freq < 0:
                heapq.heappush(max_heap, (prev_freq, prev_char))

            # Update previous character state
            prev_freq = freq + 1
            prev_char = char

        res_str = "".join(res)
        # Return empty string if not all characters could be placed
        return res_str if len(res_str) == len(s) else ""

class KthLargest:
    # -----------------------------------------------------------------------
    # 7. Kth Largest in Stream (LC 703) — T1
    # Design a class to find the kth largest element in a stream.
    # Time: O(n log k) init, O(log k) per add, Space: O(k)
    # -----------------------------------------------------------------------
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.heap = nums
        heapq.heapify(self.heap)
        while len(self.heap) > k:
            heapq.heappop(self.heap)

    def add(self, val: int) -> int:
        """Design a class to find the kth largest element in a stream."""
        # Push to heap if we have less than k elements
        if len(self.heap) < self.k:
            heapq.heappush(self.heap, val)
        # Replace root if current value is larger than the kth largest element
        elif val > self.heap[0]:
            heapq.heapreplace(self.heap, val)
        # Return the root which is the current kth largest
        return self.heap[0]

class HeapSolutionsT2:
    # -----------------------------------------------------------------------
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        # Pair capital and profits, then sort by capital required
        projects = list(zip(capital, profits))
        projects.sort()
        max_heap = []
        i = 0
        # Select at most k projects
        for _ in range(k):
            # Push all affordable projects to the max-heap (negated profit)
            while i < len(projects) and projects[i][0] <= w:
                heapq.heappush(max_heap, -projects[i][1])
                i += 1
            # Break if no projects can be funded with current capital
            if not max_heap:
                break
            # Add profit of the most profitable affordable project to capital
            w += -heapq.heappop(max_heap)
        return w

    # -----------------------------------------------------------------------
    # 9. Find K Pairs with Smallest Sums (LC 373) — T1
    # You are given two integer arrays nums1 and nums2 sorted in non-decreasing order and an integer k. Define a pair (u, v) which consists of one element from the first array and one element from the second array. Return the k pairs (u1, v1), (u2, v2), ..., (uk, vk) with the smallest sums.
    # Example: nums1 = [1,7,11], nums2 = [2,4,6], k = 3 → [[1,2],[1,4],[1,6]]
    # Constraints: 1 <= nums1.length, nums2.length <= 10^5
    # Time: O(k log k), Space: O(k)
    # -----------------------------------------------------------------------
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        if not nums1 or not nums2: return []
        res = []
        heap = []
        # Seed the heap with the first column of each row up to min(k, len(nums1))
        for i in range(min(k, len(nums1))):
            heapq.heappush(heap, (nums1[i] + nums2[0], i, 0))

        # Extrude up to k pairs
        while heap and len(res) < k:
            val, i, j = heapq.heappop(heap)
            res.append([nums1[i], nums2[j]])
            # Advance column pointer in nums2 for row i and push next pair
            if j + 1 < len(nums2):
                heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
        return res

    # -----------------------------------------------------------------------
    # 10. Furthest Building (LC 1642) — T1
    # You are given an integer array heights representing the heights of buildings, some bricks, and some ladders. You start your journey from building 0 and move to the next building by possibly using bricks or ladders. If the current building's height is greater than or equal to the next building's height, you do not need a ladder or bricks. If the current building's height is less than the next building's height, you can either use one ladder or (h[i+1] - h[i]) bricks. Return the furthest building index (0-indexed) you can reach if you use the given ladders and bricks optimally.
    # Example: heights = [4,2,7,6,9,14,12], bricks = 5, ladders = 1 → 4
    # Constraints: 1 <= heights.length <= 10^5
    # Time: O(n log L) where L = ladders, Space: O(L)
    # -----------------------------------------------------------------------
    def furthestBuilding(self, heights: List[int], bricks: int, ladders: int) -> int:
        heap = []
        # Iterate through buildings
        for i in range(len(heights) - 1):
            diff = heights[i + 1] - heights[i]
            # Skip if moving flat or downhill
            if diff <= 0: continue

            # Push positive jump height to heap
            heapq.heappush(heap, diff)
            # If heap size exceeds ladders, substitute smallest jump with bricks
            if len(heap) > ladders:
                bricks -= heapq.heappop(heap)
            # If bricks are exhausted, return current index as furthest reach
            if bricks < 0:
                return i
        return len(heights) - 1

    # -----------------------------------------------------------------------
    # 13. Minimum Refueling Stops (LC 871) — T1
    # A car travels from a starting position to a destination which is target miles east of the starting position. There are gas stations along the way. The gas stations are represented as an array stations where stations[i] = [positioni, fueli] indicates that the ith gas station is positioni miles east of the starting position and has fueli liters of gas. Return the minimum number of refueling stops the car must make in order to reach its destination. If it cannot reach the destination, return -1.
    # Example: target = 1, startFuel = 1, stations = [] → 0
    # Constraints: 1 <= target, startFuel <= 10^9
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        import heapq

        # Max-heap to store the fuel available at stations we've passed
        max_heap = []

        # Current fuel tank
        tank = startFuel
        stops = 0
        prev_position = 0

        # Add a dummy station at the target
        stations.append([target, 0])

        for position, fuel in stations:
            # Distance to the next station
            distance = position - prev_position
            tank -= distance

            # If we run out of fuel before reaching the station
            while max_heap and tank < 0:
                # Refuel from the largest station we've passed
                tank += -heapq.heappop(max_heap)
                stops += 1

            # If we still don't have enough fuel, it's impossible
            if tank < 0:
                return -1

            # Add the current station's fuel to our options
            heapq.heappush(max_heap, -fuel)
            prev_position = position

        return stops

    # -----------------------------------------------------------------------
    # 11. Kth Smallest in Sorted Matrix (LC 378) — T1
    # Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix. Note that it is the kth smallest element in the sorted order, not the kth distinct element.
    # Example: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8 → 13
    # Constraints: n == matrix.length == matrix[i].length
    # Time: O(k log n), Space: O(n)
    # -----------------------------------------------------------------------
    def kthSmallestMatrix(self, matrix: List[List[int]], k: int) -> int:
        ROWS, COLS = len(matrix), len(matrix[0])
        minHeap = [] # val, r, c
        for r in range(min(k, ROWS)):
            minHeap.append((matrix[r][0], r, 0))
        heapq.heapify(minHeap)

        res = -1
        for i in range(k):
            res, r, c = heapq.heappop(minHeap)
            if c + 1 < COLS:
                heapq.heappush(minHeap, (matrix[r][c + 1], r, c + 1))
        return res

    # -----------------------------------------------------------------------
    # 12. Ugly Number II (LC 264) — T1
    # An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer n, return the nth ugly number.
    # Example: n = 10 → 12
    # Constraints: 1 <= n <= 1690
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def nthUglyNumber(self, n: int) -> int:
        # Initialize min-heap with the first ugly number (1)
        minHeap = [1]
        visited = set([1])
        factors = [2, 3, 5]
        curr = 1
        # Extract the minimum n times
        for i in range(n):
            curr = heapq.heappop(minHeap)
            # Push multiples to heap if they are not visited yet
            for f in factors:
                nxt = curr * f
                if nxt not in visited:
                    visited.add(nxt)
                    heapq.heappush(minHeap, nxt)
        return curr

    # -----------------------------------------------------------------------
    def minMeetingRooms(self, intervals: List[List[int]]) -> int:
        if not intervals: return 0
        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])
        min_heap = []
        # Store end time of the first meeting
        heapq.heappush(min_heap, intervals[0][1])

        # Process remaining meetings
        for i in intervals[1:]:
            # If room is free before next start, reclaim it
            if min_heap[0] <= i[0]:
                heapq.heappop(min_heap)
            # Push current end time to represent active room
            heapq.heappush(min_heap, i[1])
        return len(min_heap)

    # -----------------------------------------------------------------------
    def canAttendMeetings(self, intervals: List[List[int]]) -> bool:
        # Sort intervals by start time
        intervals.sort(key=lambda x: x[0])
        # Check adjacent intervals for overlaps
        for i in range(1, len(intervals)):
            if intervals[i][0] < intervals[i-1][1]:
                return False
        return True

    # -----------------------------------------------------------------------
    # 15. Single-Threaded CPU (LC 1882) — T2
    # You are given n​​​​​​ tasks labeled from 0 to n - 1 represented by a 2D integer array tasks, where tasks[i] = [enqueueTimei, processingTimei] means that the i^​​​​​​th​​​​ task will be available to process at enqueueTimei and will take processingTimei to finish processing. You have a single-threaded CPU that can process at most one task at a time and will act in the following way: processing time. If multiple tasks have the same shortest processing time, it will choose the task with the smallest index. Return the order in which the CPU will process the tasks.
    # Example: tasks = [[1,2],[2,4],[3,2],[4,1]] → [0,2,3,1]
    # Constraints: tasks.length == n, 1 <= n <= 10^5, 1 <= enqueueTimei, processingTimei <= 10^9
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def getOrder(self, tasks: List[List[int]]) -> List[int]:
        # Append original index to each task
        for i, t in enumerate(tasks):
            t.append(i)
        # Sort tasks by enqueue time
        tasks.sort(key=lambda x: x[0])
        res, minHeap = [], []
        i, time = 0, tasks[0][0]

        # Process tasks in CPU clock sequence
        while minHeap or i < len(tasks):
            # Push all tasks that have arrived up to current time
            while i < len(tasks) and time >= tasks[i][0]:
                heapq.heappush(minHeap, (tasks[i][1], tasks[i][2]))
                i += 1
            # If CPU is idle, jump time to next task arrival
            if not minHeap:
                time = tasks[i][0]
            # Execute shortest processing time task
            else:
                procTime, index = heapq.heappop(minHeap)
                time += procTime
                res.append(index)
        return res

    # -----------------------------------------------------------------------
    # 16. Last Stone Weight (LC 1046) — T2
    # You are given an array of integers stones where stones[i] is the weight of the i^th stone. We are playing a game with the stones. On each turn, we choose the heaviest two stones and smash them together. Suppose the heaviest two stones have weights x and y with x <= y. The result of this smash is: At the end of the game, there is at most one stone left. Return the weight of the last remaining stone. If there are no stones left, return 0.
    # Example: stones = [2,7,4,1,8,1] → 1
    # Constraints: 1 <= stones.length <= 30, 1 <= stones[i] <= 1000
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def lastStoneWeight(self, stones: List[int]) -> int:
        # Negate values to implement a max-heap in Python
        stones = [-s for s in stones]
        heapq.heapify(stones)
        # Smash the two largest stones until at most one remains
        while len(stones) > 1:
            first = heapq.heappop(stones)
            second = heapq.heappop(stones)
            # Push remaining weight if they are not identical
            if second > first:
                heapq.heappush(stones, first - second)
        stones.append(0)
        return abs(stones[0])


    # -----------------------------------------------------------------------
    # 20. Minimize Deviation in Array (LC 1675) — T3
    # Given an array nums of n positive integers, you can divide even elements by 2 or multiply odd elements by 2. Return the minimum possible deviation (max - min) after any number of operations.
    # Time: O(n log(max_val) * log n), Space: O(n)
    # -----------------------------------------------------------------------
    def minimumDeviation(self, nums: List[int]) -> int:
        pq = []
        min_val = float('inf')
        # Double odd numbers and seed min-heap with negated values (max-heap)
        for num in nums:
            if num % 2 == 1:
                num *= 2
            heapq.heappush(pq, -num)
            min_val = min(min_val, num)
        res = float('inf')
        # Shrink the maximum value until it becomes odd
        while True:
            max_val = -heapq.heappop(pq)
            res = min(res, max_val - min_val)
            # Stop if maximum is odd (cannot divide by 2)
            if max_val % 2 == 1:
                break
            max_val //= 2
            min_val = min(min_val, max_val)
            heapq.heappush(pq, -max_val)
        return res

class Twitter:
    # -----------------------------------------------------------------------
    # 17. Design Twitter (LC 355) — T2
    # Design a simplified version of Twitter where users can post tweets, follow/unfollow another user, and is able to see the 10 most recent tweets in the user's news feed. Implement the Twitter class: Each call to this function will be made with a unique tweetId. feed. Each item in the news feed must be posted by users who the user followed or by the user themself. Tweets must be ordered from most recent to least recent. with ID followeeId. user with ID followeeId.
    # Constraints: 1 <= userId, followerId, followeeId <= 500, 0 <= tweetId <= 10^4, All the tweets have unique IDs, At most 3 * 10^4 calls will be made to postTweet, getNewsFeed, follow, and unfollow, A user cannot follow himself
    # Time: O(n log n) getNewsFeed where n = followees, O(1) postTweet/follow/unfollow, Space: O(u*t)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.count = 0
        self.tweetMap = defaultdict(list)
        self.followMap = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        res = []
        minHeap = []

        # Add user to followMap to include self-tweets
        self.followMap[userId].add(userId)
        # Pull the most recent tweet of each followee and seed heap
        for followeeId in self.followMap[userId]:
            if followeeId in self.tweetMap:
                index = len(self.tweetMap[followeeId]) - 1
                count, tweetId = self.tweetMap[followeeId][index]
                minHeap.append([count, tweetId, followeeId, index - 1])
        heapq.heapify(minHeap)

        # Merge k-sorted streams to extract top 10 most recent tweets
        while minHeap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(minHeap)
            res.append(tweetId)
            # Push the next tweet from the popped followee's list
            if index >= 0:
                count, tweetId = self.tweetMap[followeeId][index]
                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])
        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)

class SlidingWindowMedian:
    # -----------------------------------------------------------------------
    # 19. Sliding Window Median — T2
    # The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle values. You are given an integer array nums and an integer k. There is a sliding window of size k which is moving from the very left of the array to the very right. You can only see the k numbers in the window. Each time the sliding window moves right by one position. Return the median array for each window in the original array. Answers within 10^-5 of the actual value will be accepted.
    # Example: nums = [1,3,-1,-3,5,3,6,7], k = 3 → [1.00000,-1.00000,-1.00000,3.00000,5.00000,6.00000]
    # Constraints: 1 <= k <= nums.length <= 10^5, 2^31 <= nums[i] <= 2^31 - 1
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def medianSlidingWindow(self, nums: List[int], k: int) -> List[float]:
        small, large = [], [] # small is max-heap, large is min-heap
        for i, x in enumerate(nums[:k]):
            heapq.heappush(small, (-x, i))
        for _ in range(k - (k // 2)):
            x, i = heapq.heappop(small)
            heapq.heappush(large, (-x, i))

        ans = [large[0][0] / 1.0 if k % 2 else (large[0][0] - small[0][0]) / 2.0]
        for i, x in enumerate(nums[k:]):
            if x >= large[0][0]:
                heapq.heappush(large, (x, i + k))
                if nums[i] <= large[0][0]:
                    y, j = heapq.heappop(large)
                    heapq.heappush(small, (-y, j))
            else:
                heapq.heappush(small, (-x, i + k))
                if nums[i] >= large[0][0]:
                    y, j = heapq.heappop(small)
                    heapq.heappush(large, (-y, j))

            while small and small[0][1] <= i: heapq.heappop(small)
            while large and large[0][1] <= i: heapq.heappop(large)

            ans.append(large[0][0] / 1.0 if k % 2 else (large[0][0] - small[0][0]) / 2.0)
        return ans

class HeapSolutionsL4:
    # -----------------------------------------------------------------------
    # 21. Median of Data Stream — two-heap running median (LC 295)
    # Time: O(log n) addNum, O(1) findMedian, Space: O(n)
    # -----------------------------------------------------------------------
    def __init__(self):
        self.lo = []  # max-heap (negated)
        self.hi = []  # min-heap

    def addNum(self, num: int) -> None:
        # Route the new number through max-heap (lo)
        heapq.heappush(self.lo, -num)
        # Push the maximum of lo to min-heap (hi)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))
        # Keep heaps balanced: lo size >= hi size
        if len(self.lo) < len(self.hi):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))

    def findMedian(self) -> float:
        # If odd number of elements, median is top of lo
        if len(self.lo) > len(self.hi):
            return -self.lo[0]
        # If even, median is average of both heap roots
        return (-self.lo[0] + self.hi[0]) / 2.0

    # -----------------------------------------------------------------------
    # 22. Smallest Range Covering Elements from K Lists (LC 632)
    # Time: O(n log k) where n = total elements, Space: O(k)
    # -----------------------------------------------------------------------
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = []
        cur_max = float('-inf')
        # Seed min-heap with the first element of each of the k lists
        for i, row in enumerate(nums):
            heapq.heappush(heap, (row[0], i, 0))
            cur_max = max(cur_max, row[0])

        best = [heap[0][0], cur_max]

        # Slide the window using the min-heap
        while True:
            val, i, j = heapq.heappop(heap)
            # Stop if any list is exhausted
            if j + 1 == len(nums[i]):
                break
            next_val = nums[i][j + 1]
            heapq.heappush(heap, (next_val, i, j + 1))
            cur_max = max(cur_max, next_val)
            # Update best range if current window is tighter
            if cur_max - heap[0][0] < best[1] - best[0]:
                best = [heap[0][0], cur_max]
        return best

    # -----------------------------------------------------------------------
    # 23. Maximum Performance of a Team (LC 1383)
    # Time: O(n log n + n log k), Space: O(k)
    # -----------------------------------------------------------------------
    def maxPerformance(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        """Maximum Performance of a Team (LC 1383): Sort engineers by efficiency descending."""
        engineers = sorted(zip(efficiency, speed), reverse=True)
        heap = []  # min-heap of speeds
        speed_sum = 0
        best = 0
        for eff, spd in engineers:
            heapq.heappush(heap, spd)
            speed_sum += spd
            if len(heap) > k:
                speed_sum -= heapq.heappop(heap)
            best = max(best, speed_sum * eff)
        return best % (10**9 + 7)

    # -----------------------------------------------------------------------
    # 24. K-th Smallest Prime Fraction (LC 786)
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def kthSmallestPrimeFraction(self, arr: List[int], k: int) -> List[int]:
        n = len(arr)
        heap = []
        # Seed heap with fractions having smallest numerator for each denominator
        for j in range(1, n):
            heapq.heappush(heap, (arr[0] / arr[j], 0, j))

        # Perform k-1 pop and push steps
        for _ in range(k - 1):
            val, i, j = heapq.heappop(heap)
            # Push next fraction with larger numerator if i + 1 < j
            if i + 1 < j:
                heapq.heappush(heap, (arr[i + 1] / arr[j], i + 1, j))

        val, i, j = heapq.heappop(heap)
        return [arr[i], arr[j]]

    # -----------------------------------------------------------------------
    # 25. Merge K Sorted Arrays (Array classic)
    # Time: O(N log k) where N = total elements, Space: O(k)
    # -----------------------------------------------------------------------
    def mergeKSortedArrays(self, arrays: List[List[int]]) -> List[int]:
        heap = []
        # Seed heap with first element of each non-empty array
        for ai, arr in enumerate(arrays):
            if arr:
                heapq.heappush(heap, (arr[0], ai, 0))

        result = []
        # Pop min and push successor from same array until heap is empty
        while heap:
            val, ai, ei = heapq.heappop(heap)
            result.append(val)
            if ei + 1 < len(arrays[ai]):
                heapq.heappush(heap, (arrays[ai][ei + 1], ai, ei + 1))
        return result

    # -----------------------------------------------------------------------
    # 26. Employee Free Time (LC 759)
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def employeeFreeTime(self, schedule: List[List[List[int]]]) -> List[List[int]]:
        intervals = [interval for employee in schedule for interval in employee]
        intervals.sort()
        free = []
        current_end = intervals[0][1]
        for start, end in intervals[1:]:
            if start > current_end:
                free.append([current_end, start])
            current_end = max(current_end, end)
        return free

    # -----------------------------------------------------------------------
    # 27. Jump Game VI — heap / monotonic-deque DP variant (LC 1696)
    # Time: O(n log k), Space: O(n)
    # -----------------------------------------------------------------------
    def maxResult(self, nums: List[int], k: int) -> int:
        """Jump Game VI (LC 1696): Define dp[i] as the maximum score reachable at index i."""
        n = len(nums)
        dp = [0] * n
        dp[0] = nums[0]
        heap = [(-dp[0], 0)]  # max-heap (negated)

        for i in range(1, n):
            # Evict entries outside the window [i-k, i-1]
            while heap[0][1] < i - k:
                heapq.heappop(heap)
            dp[i] = nums[i] + (-heap[0][0])
            heapq.heappush(heap, (-dp[i], i))

        return dp[n - 1]

    # -----------------------------------------------------------------------
    # 28. Ugly Number III — binary search + inclusion-exclusion LCM (LC 1201)
    # Time: O(log(max_val)), Space: O(1)
    # -----------------------------------------------------------------------
    def nthUglyNumberIII(self, n: int, a: int, b: int, c: int) -> int:
        """Ugly Number III (LC 1201): Use binary search on the answer range [1, 2e9]."""
        from math import gcd

        def lcm(x, y):
            # Compute least common multiple using GCD
            return x * y // gcd(x, y)

        # Compute pairwise and triple LCMs
        ab = lcm(a, b)
        bc = lcm(b, c)
        ac = lcm(a, c)
        abc = lcm(ab, c)

        def count(x):
            # Inclusion-exclusion formula for counting ugly numbers
            return (x // a + x // b + x // c
                    - x // ab - x // bc - x // ac
                    + x // abc)

        lo, hi = 1, 2 * 10**9
        # Binary search for the nth ugly number
        while lo < hi:
            mid = (lo + hi) // 2
            if count(mid) >= n:
                hi = mid
            else:
                lo = mid + 1
        return lo

    # -----------------------------------------------------------------------
    # 29. Process Tasks Using Servers — two-heap simulation (LC 1882)
    # Time: O((n + m) log m) where n = tasks, m = servers, Space: O(m)
    # -----------------------------------------------------------------------
    def assignTasks(self, servers: List[int], tasks: List[int]) -> List[int]:
        free = [(w, i) for i, w in enumerate(servers)]
        heapq.heapify(free)
        busy = []  # (free_at, weight, index)
        result = []
        for t, duration in enumerate(tasks):
            # Release servers that have finished
            while busy and busy[0][0] <= t:
                free_at, w, idx = heapq.heappop(busy)
                heapq.heappush(free, (w, idx))
            if not free:
                # Jump time to next release
                free_at, w, idx = heapq.heappop(busy)
                heapq.heappush(free, (w, idx))
                t = free_at
                # Release remaining servers at the same free_at time
                while busy and busy[0][0] <= t:
                    fa, ww, ii = heapq.heappop(busy)
                    heapq.heappush(free, (ww, ii))
            w, idx = heapq.heappop(free)
            heapq.heappush(busy, (t + duration, w, idx))
            result.append(idx)
        return result


if __name__ == "__main__":
    import heapq
    sol = HeapSolutions()
    sol2 = HeapSolutionsT2()

    # findKthLargest
    assert sol.findKthLargest([3, 2, 1, 5, 6, 4], 2) == 5
    assert sol.findKthLargest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4

    # kClosest
    res = sol.kClosest([[1, 3], [-2, 2]], 1)
    assert res == [[-2, 2]]
    res = sol.kClosest([[3, 3], [5, -1], [-2, 4]], 2)
    assert len(res) == 2

    # topKFrequent
    assert sorted(sol.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert sol.topKFrequent([1], 1) == [1]

    # leastInterval
    assert sol.leastInterval(["A","A","A","B","B","B"], 2) == 8
    assert sol.leastInterval(["A","A","A","B","B","B"], 0) == 6

    # reorganizeString
    r = sol.reorganizeString("aab")
    assert r == "aba"
    assert sol.reorganizeString("aaab") == ""

    # KthLargest
    kth = KthLargest(3, [4, 5, 8, 2])
    assert kth.add(3) == 4
    assert kth.add(5) == 5
    assert kth.add(10) == 5
    assert kth.add(9) == 8
    assert kth.add(4) == 8

    # findMaximizedCapital
    assert sol2.findMaximizedCapital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert sol2.findMaximizedCapital(3, 0, [1, 2, 3], [0, 1, 2]) == 6

    # kSmallestPairs
    res = sol2.kSmallestPairs([1, 7, 11], [2, 4, 6], 3)
    assert res == [[1, 2], [1, 4], [1, 6]]

    # furthestBuilding
    assert sol2.furthestBuilding([4, 2, 7, 6, 9, 14, 12], 5, 1) == 4
    assert sol2.furthestBuilding([14, 3, 19, 3], 17, 0) == 3

    # kthSmallestMatrix
    assert sol2.kthSmallestMatrix([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8) == 13
    assert sol2.kthSmallestMatrix([[-5]], 1) == -5

    # nthUglyNumber
    assert sol2.nthUglyNumber(10) == 12
    assert sol2.nthUglyNumber(1) == 1

    # getOrder (task scheduler)
    assert sol2.getOrder([[1, 2], [2, 4], [3, 2], [4, 1]]) == [0, 2, 3, 1]

    # lastStoneWeight
    assert sol2.lastStoneWeight([2, 7, 4, 1, 8, 1]) == 1
    assert sol2.lastStoneWeight([1]) == 1

    # SlidingWindowMedian
    swm = SlidingWindowMedian()
    assert swm.medianSlidingWindow([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]

    # minimumDeviation
    assert sol2.minimumDeviation([1, 2, 3, 4]) == 1
    assert sol2.minimumDeviation([4, 1, 5, 20, 3]) == 3

    # HeapSolutionsL4
    l4 = HeapSolutionsL4()

    # Median of Data Stream (two-heap running median)
    mf = HeapSolutionsL4()
    mf.addNum(1); mf.addNum(2)
    assert mf.findMedian() == 1.5
    mf.addNum(3)
    assert mf.findMedian() == 2.0

    # smallestRange
    assert l4.smallestRange([[4,10,15,24,26],[0,9,12,20],[5,18,22,30]]) == [20, 24]
    assert l4.smallestRange([[1,2,3],[1,2,3],[1,2,3]]) == [1, 1]

    # maxPerformance
    assert l4.maxPerformance(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 2) == 60
    assert l4.maxPerformance(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 3) == 68

    # kthSmallestPrimeFraction
    assert l4.kthSmallestPrimeFraction([1,2,3,5], 3) == [2, 5]
    assert l4.kthSmallestPrimeFraction([1,7], 1) == [1, 7]

    # mergeKSortedArrays
    assert l4.mergeKSortedArrays([[1,4,7],[2,5,8],[3,6,9]]) == [1,2,3,4,5,6,7,8,9]
    assert l4.mergeKSortedArrays([[1,3,5],[2,4,6],[]]) == [1,2,3,4,5,6]

    # employeeFreeTime
    assert l4.employeeFreeTime([[[1,3],[6,7]],[[2,4]],[[2,5],[9,12]]]) == [[5,6],[7,9]]
    assert l4.employeeFreeTime([[[1,3],[6,7]],[[2,4]]]) == [[4,6]]

    # maxResult (Jump Game VI)
    assert l4.maxResult([1,-1,-2,4,-7,3], 2) == 7
    assert l4.maxResult([10,-5,-2,4,0,3], 3) == 17

    # nthUglyNumberIII
    assert l4.nthUglyNumberIII(3, 2, 3, 5) == 4
    assert l4.nthUglyNumberIII(4, 2, 3, 4) == 6

    # assignTasks (Process Tasks Using Servers)
    assert l4.assignTasks([3,3,2], [1,2,3,2,1,2]) == [2,2,0,2,1,2]
    assert l4.assignTasks([5,1,4,3,2], [2,1,2,4,5,2,1]) == [1,4,1,4,1,3,2]

    print("All heap tests passed.")
