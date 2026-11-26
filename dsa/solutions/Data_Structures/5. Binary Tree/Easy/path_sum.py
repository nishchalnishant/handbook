from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        Problem: Path Sum
        Difficulty: Easy
        Time Complexity: O(n)
        Space Complexity: O(h)
        """
        if not root:
            return False
            
        if not root.left and not root.right:
            return targetSum == root.val
            
        return (self.hasPathSum(root.left, targetSum - root.val) or 
                self.hasPathSum(root.right, targetSum - root.val))
