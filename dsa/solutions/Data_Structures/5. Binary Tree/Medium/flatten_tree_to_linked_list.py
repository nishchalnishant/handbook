from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Problem: Flatten Binary Tree to Linked List
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        curr = root
        while curr:
            if curr.left:
                prev = curr.left
                while prev.right:
                    prev = prev.right
                    
                prev.right = curr.right
                curr.right = curr.left
                curr.left = None
            curr = curr.right
