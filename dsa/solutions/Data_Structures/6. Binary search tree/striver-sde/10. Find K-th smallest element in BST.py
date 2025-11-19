class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthSmallest(self, root: TreeNode, k: int) -> int:
        # In-order traversal of BST gives sorted order of elements
        def in_order_traversal(node):
            if not node:
                return []
            return in_order_traversal(node.left) + [node.val] + in_order_traversal(node.right)
        
        # Perform in-order traversal and get the k-th smallest element
        sorted_elements = in_order_traversal(root)
        return sorted_elements[k - 1]

# Example usage:
# Constructing a BST
#        3
#       / \
#      1   4
#       \
#        2
root = TreeNode(3)
root.left = TreeNode(1)
root.left.right = TreeNode(2)
root.right = TreeNode(4)

solution = Solution()
k = 2
print(f"The {k}-th smallest element in the BST is: {solution.kthSmallest(root, k)}")