class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findLCA(root, p, q):
    if not root:
        return None

    # If both p and q are smaller than root, LCA lies in the left subtree
    if p.val < root.val and q.val < root.val:
        return findLCA(root.left, p, q)

    # If both p and q are greater than root, LCA lies in the right subtree
    if p.val > root.val and q.val > root.val:
        return findLCA(root.right, p, q)

    # If one of p or q is on one side and the other is on the other side, root is the LCA
    return root

# Example usage:
# Constructing a sample BST
#         6
#        / \
#       2   8
#      / \ / \
#     0  4 7  9
#       / \
#      3   5

root = TreeNode(6)
root.left = TreeNode(2)
root.right = TreeNode(8)
root.left.left = TreeNode(0)
root.left.right = TreeNode(4)
root.right.left = TreeNode(7)
root.right.right = TreeNode(9)
root.left.right.left = TreeNode(3)
root.left.right.right = TreeNode(5)

p = root.left  # Node with value 2
q = root.right  # Node with value 8

lca = findLCA(root, p, q)
print(f"LCA of {p.val} and {q.val} is {lca.val}")