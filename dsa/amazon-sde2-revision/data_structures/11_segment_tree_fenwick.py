"""
Segment Tree and Fenwick Tree (Binary Indexed Tree) — Google L4 interview prep.

Not covered elsewhere in this repo. These come up in "design a data structure
that supports range query + point/range update" problems — a step up in
difficulty from a plain prefix-sum array, which only handles static arrays.

Segment Tree: O(log n) point update, O(log n) range query, supports any
associative operation (sum, min, max, gcd...). Build O(n), space O(4n).

Fenwick Tree (BIT): O(log n) point update, O(log n) prefix-sum query.
Simpler and faster in practice than a segment tree, but limited to
invertible operations (sum, xor) since queries are prefix-only.

Key Gotchas:
- Segment tree array size: use 4*n to be safe (recursive/array-based version).
- Fenwick tree is 1-indexed internally; range_sum(l, r) = prefix(r) - prefix(l-1).
- Fenwick can't directly do range-min/max (no inverse operation) — use a
  segment tree for those.
"""

from typing import List


class SegmentTree:
    """Array-based segment tree supporting point update + range sum query."""

    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.tree = [0] * (4 * self.n)
        if self.n:
            self._build(nums, 0, 0, self.n - 1)

    def _build(self, nums, node, start, end):
        if start == end:
            self.tree[node] = nums[start]
            return
        mid = (start + end) // 2
        self._build(nums, 2 * node + 1, start, mid)
        self._build(nums, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def update(self, index: int, value: int) -> None:
        self._update(0, 0, self.n - 1, index, value)

    def _update(self, node, start, end, index, value):
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node + 1, start, mid, index, value)
        else:
            self._update(2 * node + 2, mid + 1, end, index, value)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]

    def query(self, left: int, right: int) -> int:
        """Inclusive range sum over [left, right]."""
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node, start, end, left, right):
        if right < start or end < left:
            return 0  # no overlap
        if left <= start and end <= right:
            return self.tree[node]  # total overlap
        mid = (start + end) // 2
        return (self._query(2 * node + 1, start, mid, left, right) +
                self._query(2 * node + 2, mid + 1, end, left, right))


class FenwickTree:
    """1-indexed Binary Indexed Tree supporting point update + prefix sum."""

    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def update(self, index: int, delta: int) -> None:
        """Add `delta` to the element at 0-indexed `index`."""
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)  # move to next responsible node

    def prefix_sum(self, index: int) -> int:
        """Sum of elements in [0, index], 0-indexed inclusive."""
        i = index + 1
        total = 0
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)  # move to parent
        return total

    def range_sum(self, left: int, right: int) -> int:
        """Sum of elements in [left, right], 0-indexed inclusive."""
        if left == 0:
            return self.prefix_sum(right)
        return self.prefix_sum(right) - self.prefix_sum(left - 1)


class NumArray:
    """LC 307 — Range Sum Query - Mutable, backed by a Fenwick tree."""

    def __init__(self, nums: List[int]):
        self.nums = nums[:]
        self.fenwick = FenwickTree(len(nums))
        for i, v in enumerate(nums):
            self.fenwick.update(i, v)

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self.fenwick.update(index, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self.fenwick.range_sum(left, right)


if __name__ == "__main__":
    # Segment tree: sum range query + point update
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    assert st.query(1, 3) == 15  # 3+5+7
    st.update(1, 10)  # nums -> [1,10,5,7,9,11]
    assert st.query(1, 3) == 22  # 10+5+7

    # Fenwick tree: prefix sum + range sum
    fw = FenwickTree(6)
    for i, v in enumerate([1, 3, 5, 7, 9, 11]):
        fw.update(i, v)
    assert fw.prefix_sum(2) == 9  # 1+3+5
    assert fw.range_sum(1, 3) == 15  # 3+5+7
    fw.update(1, 7)  # add 7 -> index1 becomes 10
    assert fw.range_sum(1, 3) == 22

    # NumArray (LC 307)
    na = NumArray([1, 3, 5])
    assert na.sumRange(0, 2) == 9
    na.update(1, 2)
    assert na.sumRange(0, 2) == 8

    print("All segment tree / Fenwick tree tests passed.")
