from typing import List
from collections import Counter, deque
import heapq

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """
        Problem: Task Scheduler
        Difficulty: Medium
        Time Complexity: O(m) where m is number of tasks
        Space Complexity: O(1)
        """
        count = Counter(tasks)
        maxHeap = [-cnt for cnt in count.values()]
        heapq.heapify(maxHeap)
        
        time = 0
        q = deque() # pairs of [-cnt, idleTime]
        
        while maxHeap or q:
            time += 1
            if maxHeap:
                cnt = 1 + heapq.heappop(maxHeap)
                if cnt:
                    q.append([cnt, time + n])
            
            if q and q[0][1] == time:
                heapq.heappush(maxHeap, q.popleft()[0])
        return time
