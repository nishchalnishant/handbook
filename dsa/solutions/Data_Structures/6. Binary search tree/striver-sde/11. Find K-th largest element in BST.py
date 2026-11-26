class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthLargest(self, root: TreeNode, k: int) -> int:
        # Helper function for reverse in-order traversal
        def reverse_inorder_traversal(node):
            nonlocal k, result
            if not node or k == 0:
                return
            
            # Traverse the right subtree first
            reverse_inorder_traversal(node.right)
            
            # Decrement k and check if this is the k-th largest
            k -= 1
            if k == 0:
                result = node.val
                return
            
            # Traverse the left subtree
            reverse_inorder_traversal(node.left)
        
        result = None
        reverse_inorder_traversal(root)
        return result

# Example usage:
# Constructing a sample BST
#         5
#        / \
#       3   7
#      / \   \
#     2   4   8

root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(7)
root.left.left = TreeNode(2)
root.left.right = TreeNode(4)
root.right.right = TreeNode(8)

solution = Solution()
k = 3
print(f"The {k}-th largest element in the BST is: {solution.kthLargest(root, k)}")