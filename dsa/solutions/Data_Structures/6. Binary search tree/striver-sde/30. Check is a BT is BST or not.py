class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isBST(node, lower=float('-inf'), upper=float('inf')):
    if not node:
        return True
    if not (lower < node.val < upper):
        return False
    return isBST(node.left, lower, node.val) and isBST(node.right, node.val, upper)

# Example usage:
if __name__ == "__main__":
    # Constructing a binary tree
    root = TreeNode(2)
    root.left = TreeNode(1)
    root.right = TreeNode(3)

    # Check if the binary tree is a BST
    if isBST(root):
        print("The binary tree is a BST.")
    else:
        print("The binary tree is not a BST.")