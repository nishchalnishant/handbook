from typing import Optional, List
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        Problem: Binary Tree Level Order Traversal
        Pattern: BFS (Queue)
        """
        if not root: return []
        res = []
        q = deque([root])
        
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
            res.append(level)
        return res

    def minDepth(self, root: Optional[TreeNode]) -> int:
        """
        Problem: Minimum Depth of Binary Tree
        Pattern: BFS (Optimal for min depth as it stops at first leaf)
        """
        if not root: return 0
        q = deque([(root, 1)])
        while q:
            node, depth = q.popleft()
            if not node.left and not node.right:
                return depth
            if node.left: q.append((node.left, depth + 1))
            if node.right: q.append((node.right, depth + 1))
        return 0

    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        """
        Problem: Binary Tree Right Side View
        Pattern: BFS (Take last element of each level)
        """
        if not root: return []
        res = []
        q = deque([root])
        
        while q:
            level_len = len(q)
            for i in range(level_len):
                node = q.popleft()
                # If it's the last node in the current level, add to result
                if i == level_len - 1:
                    res.append(node.val)
                if node.left: q.append(node.left)
                if node.right: q.append(node.right)
        return res

    def maxDepth(self, root: Optional[TreeNode]) -> int:
        """
        Problem: Maximum Depth of Binary Tree
        Pattern: BFS or DFS
        """
        if not root: return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))
