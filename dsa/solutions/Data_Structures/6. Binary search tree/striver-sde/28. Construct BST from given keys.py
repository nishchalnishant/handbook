class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return TreeNode(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def construct_bst(self, keys):
        for key in keys:
            self.root = self.insert(self.root, key)

    def inorder_traversal(self, root):
        if root is not None:
            self.inorder_traversal(root.left)
            print(root.key, end=" ")
            self.inorder_traversal(root.right)

# Example usage
if __name__ == "__main__":
    keys = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    bst = BST()
    bst.construct_bst(keys)
    print("Inorder Traversal of BST:")
    bst.inorder_traversal(bst.root)