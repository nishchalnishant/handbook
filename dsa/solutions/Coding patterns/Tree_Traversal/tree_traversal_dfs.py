from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        Problem: Invert Binary Tree
        Pattern: DFS
        """
        if not root: return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root

    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        """
        Problem: Diameter of Binary Tree
        Pattern: DFS (Postorder - max depth from left + max depth from right)
        """
        self.res = 0
        
        def depth(node):
            if not node: return 0
            left = depth(node.left)
            right = depth(node.right)
            self.res = max(self.res, left + right)
            return 1 + max(left, right)
            
        depth(root)
        return self.res

    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        Problem: Path Sum
        Pattern: DFS
        """
        if not root: return False
        if not root.left and not root.right:
            return root.val == targetSum
        return self.hasPathSum(root.left, targetSum - root.val) or \
               self.hasPathSum(root.right, targetSum - root.val)

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        """
        Problem: Subtree of Another Tree
        Pattern: DFS (Compare identical trees)
        """
        if not subRoot: return True
        if not root: return False
        
        if self.isSameTree(root, subRoot):
            return True
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
    
    def isSameTree(self, p, q):
        if not p and not q: return True
        if not p or not q or p.val != q.val: return False
        return self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
