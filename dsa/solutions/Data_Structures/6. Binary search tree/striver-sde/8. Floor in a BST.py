class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def floor_in_bst(root, key):
    floor = None
    while root:
        if root.val == key:
            return root.val
        elif root.val < key:
            floor = root.val
            root = root.right
        else:
            root = root.left
    return floor

# Helper function to insert a node in BST
def insert_into_bst(root, val):
    if not root:
        return TreeNode(val)
    if val < root.val:
        root.left = insert_into_bst(root.left, val)
    else:
        root.right = insert_into_bst(root.right, val)
    return root

# Example usage
if __name__ == "__main__":
    root = None
    values = [8, 4, 12, 2, 6, 10, 14]
    for val in values:
        root = insert_into_bst(root, val)
    
    key = 5
    print(f"The floor of {key} in the BST is: {floor_in_bst(root, key)}")