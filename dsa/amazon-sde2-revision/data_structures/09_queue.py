"""
Queue patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Using a list for a queue in Python (`pop(0)` is O(N)). Always use `collections.deque`.\n- Assuming queue size won't grow exponentially in BFS without visited checks.\n- Popping from an empty queue.

Common Variants:
- Breadth-First Search (BFS) level-order traversal\n- Shortest path in unweighted graphs\n- Monotonic Queue for Sliding Window Maximum

General Tips & Best Practices:
- To process level-by-level in BFS, loop `for _ in range(len(q)):`.\n- Remember to mark nodes as visited *when enqueueing*, not when dequeueing, to avoid duplicates.

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from collections import deque
from typing import List, Tuple

class QueueSolutions:
    # -----------------------------------------------------------------------
    # 2. Rotten Oranges (LC 994) — T1
    # You are given an m x n grid where each cell can have one of three values: 0 representing an empty cell, 1 representing a fresh orange, or 2 representing a rotten orange. Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten. Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
    # Example: grid = [[2,1,1],[1,1,0],[0,1,1]] → 4
    # Constraints: m == grid.length, n == grid[i].length, 1 <= m, n <= 10
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def orangesRotting(self, grid: List[List[int]]) -> int:
        q = deque()
        fresh = 0
        rows, cols = len(grid), len(grid[0])

        # Scan the grid to count fresh oranges and enqueue initially rotten ones
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    fresh += 1
                elif grid[r][c] == 2:
                    q.append((r, c))

        # If there are no fresh oranges, no time is needed
        if fresh == 0: return 0

        minutes = 0
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]

        # Process BFS level by level to simulate time step in minutes
        while q and fresh > 0:
            minutes += 1
            for _ in range(len(q)):
                r, c = q.popleft()
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    # If neighbor is fresh, rot it and enqueue it
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 2
                        fresh -= 1
                        q.append((nr, nc))

        return minutes if fresh == 0 else -1

    # -----------------------------------------------------------------------
    # 3. 01 Matrix (LC 542) — T1
    # Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell. The distance between two cells sharing a common edge is 1.
    # Example: mat = [[0,0,0],[0,1,0],[0,0,0]] → [[0,0,0],[0,1,0],[0,0,0]]
    # Constraints: m == mat.length, n == mat[i].length, 1 <= m, n <= 10^4, 1 <= m * n <= 10^4, mat[i][j] is either 0 or 1, There is at least one 0 in mat, Note: This question is the same as 1765: https://leetcode.com/problems/map-of-highest-peak/
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        rows, cols = len(mat), len(mat[0])
        q = deque()

        # Enqueue all 0-cells and mark non-0 cells as unvisited (-1)
        for r in range(rows):
            for c in range(cols):
                if mat[r][c] == 0:
                    q.append((r, c))
                else:
                    mat[r][c] = -1 # marked as unvisited

        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        # Multi-source BFS to calculate distance to the nearest 0
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # If neighbor is unvisited, compute its distance and enqueue
                if 0 <= nr < rows and 0 <= nc < cols and mat[nr][nc] == -1:
                    mat[nr][nc] = mat[r][c] + 1
                    q.append((nr, nc))

        return mat

    # -----------------------------------------------------------------------
    # 4. Walls and Gates (LC 286) — T1
    # You are given an m x n grid rooms initialized with these three possible values: -1 (A wall or an obstacle), 0 (A gate), INF (Infinity means an empty room). Fill each empty room with the distance to its nearest gate. If it is impossible to reach a gate, it should be filled with INF.
    # Example: rooms = [[2147483647,-1,0,2147483647],[2147483647,2147483647,2147483647,-1],[2147483647,-1,2147483647,-1],[0,-1,2147483647,2147483647]] → [[3,-1,0,1],[2,2,1,-1],[1,-1,2,-1],[0,-1,3,4]]
    # Constraints: m == rooms.length, n == rooms[i].length, 1 <= m, n <= 250
    # Time: O(m*n), Space: O(m*n)
    # -----------------------------------------------------------------------
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        if not rooms: return
        rows, cols = len(rooms), len(rooms[0])
        q = deque()

        # Gather all gates as the initial sources of the BFS
        for r in range(rows):
            for c in range(cols):
                if rooms[r][c] == 0:
                    q.append((r, c))

        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        # Traverse in multi-source BFS order to fill distances
        while q:
            r, c = q.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # Update empty room distance and enqueue if unvisited
                if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == 2147483647:
                    rooms[nr][nc] = rooms[r][c] + 1
                    q.append((nr, nc))

    # -----------------------------------------------------------------------
    # 5. Shortest Path in Binary Matrix (LC 1091) — T1
    # Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. If there is no clear path, return -1. A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right cell (i.e., (n - 1, n - 1)) such that: they share an edge or a corner). The length of a clear path is the number of visited cells of this path.
    # Example: grid = [[0,1],[1,0]] → 2
    # Constraints: n == grid.length, n == grid[i].length, 1 <= n <= 100, grid[i][j] is 0 or 1
    # Time: O(n^2), Space: O(n^2)
    # -----------------------------------------------------------------------
    def shortestPathBinaryMatrix(self, grid: List[List[int]]) -> int:
        # Check start and end constraints
        if grid[0][0] != 0 or grid[-1][-1] != 0: return -1
        rows, cols = len(grid), len(grid[0])
        q = deque([(0, 0, 1)])
        grid[0][0] = 1 # mark visited

        dirs = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
        # 8-directional BFS traversal
        while q:
            r, c, dist = q.popleft()
            # If target reached, return path length
            if r == rows - 1 and c == cols - 1:
                return dist
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                # If neighbor is unvisited, mark visited and enqueue with updated distance
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, dist + 1))
        return -1

    # -----------------------------------------------------------------------
    # 7. Open the Lock (LC 752) — T1
    # You have a lock in front of you with 4 circular wheels. Each wheel has 10 slots: '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'. The wheels can rotate freely and wrap around: for example we can turn '9' to be '0', or '0' to be '9'. Each move consists of turning one wheel one slot. The lock initially starts at '0000', a string representing the state of the 4 wheels. You are given a list of deadends dead ends, meaning if the lock displays any of these codes, the wheels of the lock will stop turning and you will be unable to open it. Given a target representing the value of the wheels that will unlock the lock, return the minimum total number of turns required to open the lock, or -1 if it is impossible.
    # Example: deadends = ["0201","0101","0102","1212","2002"], target = "0202" → 6
    # Constraints: 1 <= deadends.length <= 500, deadends[i].length == 4, target.length == 4, target will not be in the list deadends, target and deadends[i] consist of digits only
    # Time: O(10^4 * 4), Space: O(10^4)
    # -----------------------------------------------------------------------
    def openLock(self, deadends: List[str], target: str) -> int:
        # Store deadends in a set for O(1) lookups
        dead = set(deadends)
        if "0000" in dead: return -1

        q = deque([("0000", 0)])
        visited = set(["0000"])

        # BFS over the state space
        while q:
            state, moves = q.popleft()
            if state == target: return moves

            # Rotate each of the 4 wheels in both directions
            for i in range(4):
                digit = int(state[i])
                for d in [-1, 1]:
                    new_digit = (digit + d) % 10
                    next_state = state[:i] + str(new_digit) + state[i+1:]
                    # Enqueue only valid, unvisited configurations
                    if next_state not in visited and next_state not in dead:
                        visited.add(next_state)
                        q.append((next_state, moves + 1))
        return -1

    # -----------------------------------------------------------------------
    # 8. Minimum Knight Moves (LC 1197) — T1
    # In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0]. A knight has 8 possible moves it can make, as illustrated below. Each move is two squares in a cardinal direction, then one square in an orthogonal direction. Return the minimum number of steps needed to move the knight to the square [x, y]. It is guaranteed the answer exists.
    # Example: x = 2, y = 1 → 1
    # Constraints: 300 <= x, y <= 300
    # Time: O(max(|x|, |y|)^2), Space: O(max(|x|, |y|)^2)
    # -----------------------------------------------------------------------
    def minKnightMoves(self, x: int, y: int) -> int:
        # Use quadrant symmetry
        x, y = abs(x), abs(y)
        q = deque([(0, 0, 0)])
        visited = set([(0, 0)])
        dirs = [(1,2), (2,1), (2,-1), (1,-2), (-1,-2), (-2,-1), (-2,1), (-1,2)]

        # BFS on grid coordinates
        while q:
            cx, cy, moves = q.popleft()
            if cx == x and cy == y: return moves

            for dx, dy in dirs:
                nx, ny = cx + dx, cy + dy
                # keep slightly out of quadrant to allow minimal backsteps
                if nx >= -2 and ny >= -2 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    q.append((nx, ny, moves + 1))
        return -1

class MyCircularQueue:
    # -----------------------------------------------------------------------
    # 1. Design Circular Queue (LC 622) — T2
    # Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer". One of the benefits of the circular queue is that we can make use of the spaces in front of the queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if there is a space in front of the queue. But using the circular queue, we can use the space to store new values. Implement the MyCircularQueue class: operation is successful. successful. You must solve the problem without using the built-in queue data structure in your programming language.
    # Constraints: 1 <= k <= 1000, 0 <= value <= 1000, At most 3000 calls will be made to enQueue, deQueue, Front, Rear, isEmpty, and isFull
    # Time: O(1) per operation, Space: O(k)
    # -----------------------------------------------------------------------
    def __init__(self, k: int):
        self.q = [0] * k
        self.k = k
        self.front = 0
        self.size = 0

    # Time: O(1), Space: O(1)
    def enQueue(self, value: int) -> bool:
        # If queue is full, cannot enqueue
        if self.isFull(): return False
        # Calculate rear index using modular arithmetic
        rear = (self.front + self.size) % self.k
        self.q[rear] = value
        self.size += 1
        return True

    # Time: O(1), Space: O(1)
    def deQueue(self) -> bool:
        # If queue is empty, cannot dequeue
        if self.isEmpty(): return False
        # Move the front pointer forward circularly
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    # Time: O(1), Space: O(1)
    def Front(self) -> int:
        if self.isEmpty(): return -1
        return self.q[self.front]

    # Time: O(1), Space: O(1)
    def Rear(self) -> int:
        if self.isEmpty(): return -1
        return self.q[(self.front + self.size - 1) % self.k]

    # Time: O(1), Space: O(1)
    def isEmpty(self) -> bool:
        """Returns whether is empty holds for the provided input."""
        return self.size == 0

    # Time: O(1), Space: O(1)
    def isFull(self) -> bool:
        """Returns whether is full holds for the provided input."""
        return self.size == self.k

class MovingAverage:
    # -----------------------------------------------------------------------
    # 4. Jump Game III (LC 1306) — T2
    # Given an array of non-negative integers arr, you are initially positioned at start index of the array. When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index with value 0. Notice that you can not jump outside of the array at any time.
    # Example: arr = [4,2,3,0,3,1,2], start = 5 → true
    # Constraints: 1 <= arr.length <= 5 * 10^4, 0 <= arr[i] < arr.length, 0 <= start < arr.length
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def canReach(self, arr: List[int], start: int) -> bool:
        q = deque([start])
        visited = set([start])

        # Traverse reachable indexes in BFS order
        while q:
            node = q.popleft()
            # If target value 0 is reached
            if arr[node] == 0:
                return True

            # Jump forward and backward from current index
            for neighbor in (node + arr[node], node - arr[node]):
                if 0 <= neighbor < len(arr) and neighbor not in visited:
                    visited.add(neighbor)
                    q.append(neighbor)
        return False

    # -----------------------------------------------------------------------
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        from collections import deque
        n = len(nums)
        # Compute prefix sums array
        prefix = [0] * (n + 1)
        for i in range(n):
            prefix[i + 1] = prefix[i] + nums[i]

        res = n + 1
        # Monotonically increasing queue of prefix sum indices
        q = deque()

        for i in range(n + 1):
            # Check if current prefix minus front prefix is at least k
            while q and prefix[i] - prefix[q[0]] >= k:
                res = min(res, i - q.popleft())
            # Maintain increasing prefix sums order in the deque
            while q and prefix[i] <= prefix[q[-1]]:
                q.pop()
            q.append(i)

        return res if res <= n else -1

    # -----------------------------------------------------------------------
    def constrainedSubsetSum(self, nums: List[int], k: int) -> int:
        from collections import deque
        # Monotonically decreasing queue storing (max_subsequence_sum, index)
        q = deque()
        res = nums[0]

        for i, num in enumerate(nums):
            # Remove indices out of current k step range
            if q and i - q[0][1] > k:
                q.popleft()

            # Choose either start fresh or extend maximum from queue
            cur_max = max(num, num + (q[0][0] if q else 0))
            res = max(res, cur_max)

            # Keep queue monotonic by popping smaller values
            while q and q[-1][0] <= cur_max:
                q.pop()

            # Only positive values can help build future maximum sums
            if cur_max > 0:
                q.append((cur_max, i))

        return res

    # -----------------------------------------------------------------------
    # 7. As Far from Land as Possible (LC 1162) — T2
    # Given an n x n grid containing only values 0 and 1, where 0 represents water and 1 represents land, find a water cell such that its distance to the nearest land cell is maximized, and return the distance. If no land or water exists in the grid, return -1. The distance used in this problem is the Manhattan distance: the distance between two cells (x0, y0) and (x1, y1) is |x0 - x1| + |y0 - y1|.
    # Example: grid = [[1,0,1],[0,0,0],[1,0,1]] → 2
    # Constraints: n == grid.length, n == grid[i].length, 1 <= n <= 100, grid[i][j] is 0 or 1
    # Time: O(n^2), Space: O(n^2)
    # -----------------------------------------------------------------------
    def maxDistance(self, grid: List[List[int]]) -> int:
        from collections import deque
        n = len(grid)
        q = deque()

        # Seed all land cells in the queue
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    q.append((r, c, 0))

        # Check edge case: all land or all water
        if not q or len(q) == n * n:
            return -1

        res = 0
        # Multi-source BFS traversal to find max distance
        while q:
            r, c, dist = q.popleft()
            res = max(res, dist)
            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Enqueue unvisited water neighbor
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc, dist + 1))

        return res

if __name__ == "__main__":
    sol = QueueSolutions()

    # orangesRotting
    assert sol.orangesRotting([[2,1,1],[1,1,0],[0,1,1]]) == 4
    assert sol.orangesRotting([[2,1,1],[0,1,1],[1,0,1]]) == -1
    assert sol.orangesRotting([[0,2]]) == 0

    # updateMatrix (0/1 BFS distance)
    assert sol.updateMatrix([[0,0,0],[0,1,0],[0,0,0]]) == [[0,0,0],[0,1,0],[0,0,0]]
    assert sol.updateMatrix([[0,0,0],[0,1,0],[1,1,1]]) == [[0,0,0],[0,1,0],[1,2,1]]

    # shortestPathBinaryMatrix
    assert sol.shortestPathBinaryMatrix([[0,1],[1,0]]) == 2
    assert sol.shortestPathBinaryMatrix([[0,0,0],[1,1,0],[1,1,0]]) == 4
    assert sol.shortestPathBinaryMatrix([[1,0]]) == -1  # blocked start

    # openLock
    assert sol.openLock(["0201","0101","0102","1212","2002"], "0202") == 6
    assert sol.openLock(["8888"], "0009") == 1
    assert sol.openLock(["0000"], "8888") == -1

    # MyCircularQueue
    cq = MyCircularQueue(3)
    assert cq.enQueue(1) == True
    assert cq.enQueue(2) == True
    assert cq.enQueue(3) == True
    assert cq.enQueue(4) == False  # full
    assert cq.Rear() == 3
    assert cq.isFull() == True
    assert cq.deQueue() == True
    assert cq.enQueue(4) == True
    assert cq.Rear() == 4

    # canReach (Jump Game III)
    mv = MovingAverage()
    assert mv.canReach([4,2,3,0,3,1,2], 5) == True
    assert mv.canReach([4,2,3,0,3,1,2], 0) == True
    assert mv.canReach([3,0,2,1,2], 2) == False

    print("All queue tests passed.")
