from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        Problem: Validate Binary Search Tree
        Difficulty: Medium
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        def valid(node, left, right):
            if not node:
                return True
            if not (left < node.val < right):
                return False
                
            return (valid(node.left, left, node.val) and 
                    valid(node.right, node.val, right))
            
        return valid(root, float("-inf"), float("inf"))
