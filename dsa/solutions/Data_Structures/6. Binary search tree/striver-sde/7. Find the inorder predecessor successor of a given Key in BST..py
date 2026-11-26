class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def findPredecessorSuccessor(root, key):
    predecessor = None
    successor = None

    # Find the key in the BST
    current = root
    while current:
        if key < current.key:
            successor = current
            current = current.left
        elif key > current.key:
            predecessor = current
            current = current.right
        else:
            # Key found, find predecessor and successor
            # Predecessor is the rightmost node in the left subtree
            if current.left:
                temp = current.left
                while temp.right:
                    temp = temp.right
                predecessor = temp

            # Successor is the leftmost node in the right subtree
            if current.right:
                temp = current.right
                while temp.left:
                    temp = temp.left
                successor = temp
            break

    return (predecessor.key if predecessor else None, successor.key if successor else None)

# Helper function to insert a node in BST
def insert(root, key):
    if root is None:
        return TreeNode(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root

# Example usage
if __name__ == "__main__":
    root = None
    keys = [50, 30, 70, 20, 40, 60, 80]
    for key in keys:
        root = insert(root, key)

    key = 65
    predecessor, successor = findPredecessorSuccessor(root, key)
    print(f"Inorder Predecessor of {key}: {predecessor}")
    print(f"Inorder Successor of {key}: {successor}")