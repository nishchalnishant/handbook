class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findCeil(root: TreeNode, key: int) -> int:
    ceil = -1
    while root:
        if root.val == key:
            return root.val
        if root.val < key:
            root = root.right
        else:
            ceil = root.val
            root = root.left
    return ceil

# Example usage:
# Constructing the BST
#         8
#       /   \
#      4     12
#     / \   /  \
#    2   6 10  14

root = TreeNode(8)
root.left = TreeNode(4)
root.right = TreeNode(12)
root.left.left = TreeNode(2)
root.left.right = TreeNode(6)
root.right.left = TreeNode(10)
root.right.right = TreeNode(14)

key = 5
print(f"The ceil of {key} in the BST is: {findCeil(root, key)}")