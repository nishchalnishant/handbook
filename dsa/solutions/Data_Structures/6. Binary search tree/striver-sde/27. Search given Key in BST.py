class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def searchBST(root, key):
    # Base case: root is None or key is present at root
    if root is None or root.val == key:
        return root

    # Key is greater than root's value
    if key > root.val:
        return searchBST(root.right, key)

    # Key is smaller than root's value
    return searchBST(root.left, key)

# Helper function to insert a new node in BST
def insertIntoBST(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insertIntoBST(root.left, val)
    else:
        root.right = insertIntoBST(root.right, val)
    return root

# Example usage
if __name__ == "__main__":
    # Create a sample BST
    root = None
    values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
    for value in values:
        root = insertIntoBST(root, value)

    # Search for a key in the BST
    key = 6
    result = searchBST(root, key)
    if result:
        print(f"Key {key} found in BST.")
    else:
        print(f"Key {key} not found in BST.")