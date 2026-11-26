from typing import List, Optional
import collections

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Problem: Vertical Order Traversal of a Binary Tree
        Difficulty: Hard
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        nodes = []
        q = collections.deque([(root, 0, 0)]) # node, row, col
        
        while q:
            node, r, c = q.popleft()
            if node:
                nodes.append((c, r, node.val))
                q.append((node.left, r + 1, c - 1))
                q.append((node.right, r + 1, c + 1))
                
        nodes.sort()
        
        res = collections.defaultdict(list)
        for c, r, val in nodes:
            res[c].append(val)
            
        return [res[x] for x in sorted(res.keys())]
