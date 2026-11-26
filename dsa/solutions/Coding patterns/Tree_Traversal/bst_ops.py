from typing import Optional

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        """
        Problem: Validate Binary Search Tree
        Pattern: DFS (Inorder or Range Check)
        """
        def validate(node, low=-float('inf'), high=float('inf')):
            if not node: return True
            if node.val <= low or node.val >= high:
                return False
            return validate(node.left, low, node.val) and validate(node.right, node.val, high)
        return validate(root)

    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """
        Problem: Lowest Common Ancestor of a Binary Search Tree
        Pattern: BST Property (Walk down)
        """
        curr = root
        while curr:
            if p.val < curr.val and q.val < curr.val:
                curr = curr.left
            elif p.val > curr.val and q.val > curr.val:
                curr = curr.right
            else:
                return curr
        return None
