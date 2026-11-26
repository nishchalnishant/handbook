class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def bstFromPreorder(preorder):
    def constructBST(preorder, bound):
        nonlocal index
        if index == len(preorder) or preorder[index] > bound:
            return None

        root_val = preorder[index]
        index += 1
        root = TreeNode(root_val)
        root.left = constructBST(preorder, root_val)
        root.right = constructBST(preorder, bound)
        return root

    index = 0
    return constructBST(preorder, float('inf'))

# Helper function to print the tree (inorder traversal)
def printInorder(root):
    if root:
        printInorder(root.left)
        print(root.val, end=" ")
        printInorder(root.right)

# Example usage
preorder = [8, 5, 1, 7, 10, 12]
root = bstFromPreorder(preorder)
print("Inorder Traversal of Constructed BST:")
printInorder(root)