"""
Number of Islands was asked in BOTH round 1 and round 2.
Know all three solutions cold, plus the follow-ups below.

Complexities: all core solutions are O(m*n) time; DFS/BFS O(m*n) space worst
case (recursion/queue), union-find O(m*n) space with near-O(1) amortized ops.
"""

from collections import deque


# ---------------------------------------------------------------------------
# 1) Classic: DFS
# ---------------------------------------------------------------------------
def num_islands_dfs(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def sink(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"  # mark visited in-place (mention: mutates input; use a
        # visited set if the grid must be preserved)
        sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                sink(r, c)
    return count


# ---------------------------------------------------------------------------
# 2) BFS (say: avoids recursion-depth issues on huge grids)
# ---------------------------------------------------------------------------
def num_islands_bfs(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            count += 1
            grid[r][c] = "0"
            q = deque([(r, c)])
            while q:
                cr, cc = q.popleft()
                for nr, nc in ((cr+1,cc), (cr-1,cc), (cr,cc+1), (cr,cc-1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1":
                        grid[nr][nc] = "0"
                        q.append((nr, nc))
    return count


# ---------------------------------------------------------------------------
# 3) Union-Find (needed for the streaming follow-up)
# ---------------------------------------------------------------------------
class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = 0  # incremented externally when a land cell is added

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        self.components -= 1


def num_islands_union_find(grid: list[list[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    dsu = DSU(rows * cols)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != "1":
                continue
            dsu.components += 1
            idx = r * cols + c
            if r > 0 and grid[r-1][c] == "1":
                dsu.union(idx, idx - cols)
            if c > 0 and grid[r][c-1] == "1":
                dsu.union(idx, idx - 1)
    return dsu.components


# ---------------------------------------------------------------------------
# 4) THE PRODUCTION TWIST: "the grid doesn't fit in memory"
# Process row by row keeping only the previous row's component labels.
# This is the follow-up most likely from a systems-minded interviewer.
# ---------------------------------------------------------------------------
def num_islands_streaming(row_iter) -> int:
    """
    row_iter yields one row (list of '0'/'1') at a time.
    Keep DSU labels only for the previous row; islands that no longer touch
    the frontier are 'closed' and counted.
    Sketch (interview level): maintain per-cell component ids for prev row;
    for each new row, union with the cell above and the cell to the left;
    count components that disappear from the frontier.
    """
    prev_labels: list[int] = []
    next_id = 0
    parent: dict[int, int] = {}
    closed = 0

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for row in row_iter:
        cur: list[int] = []
        for c, val in enumerate(row):
            if val != "1":
                cur.append(-1)
                continue
            label = -1
            if c > 0 and cur[c-1] != -1:          # left neighbor
                label = cur[c-1]
            if prev_labels and prev_labels[c] != -1:  # up neighbor
                if label == -1:
                    label = prev_labels[c]
                else:
                    union(label, prev_labels[c])
            if label == -1:
                label = next_id
                parent[label] = label
                next_id += 1
            cur.append(label)
        # roots alive on the new frontier
        frontier = {find(l) for l in cur if l != -1}
        prev_roots = {find(l) for l in prev_labels if l != -1}
        closed += len(prev_roots - frontier)
        prev_labels = cur

    closed += len({find(l) for l in prev_labels if l != -1})
    return closed


# ---------------------------------------------------------------------------
# 5) Cousins to be fluent in (one-liners of the idea):
#   - Max Area of Island: same DFS, return size, track max.
#   - Rotting Oranges: multi-source BFS, answer = number of BFS levels.
#   - Surrounded Regions: DFS from BORDER 'O's first, flip the rest.
#   - Distinct Islands: record shape as normalized path signature, count set size.
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    g = [
        ["1","1","0","0","0"],
        ["1","1","0","0","0"],
        ["0","0","1","0","0"],
        ["0","0","0","1","1"],
    ]
    import copy
    assert num_islands_dfs(copy.deepcopy(g)) == 3
    assert num_islands_bfs(copy.deepcopy(g)) == 3
    assert num_islands_union_find(copy.deepcopy(g)) == 3
    assert num_islands_streaming(iter(copy.deepcopy(g))) == 3
    print("all variants OK")
