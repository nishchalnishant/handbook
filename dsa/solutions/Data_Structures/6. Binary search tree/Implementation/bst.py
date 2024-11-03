class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Insert a new node with the specified data into the BST."""
        if not self.root:
            self.root = Node(data)
        else:
            self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        """Helper method to insert a new node recursively."""
        if data < node.data:
            if node.left is None:
                node.left = Node(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = Node(data)
            else:
                self._insert_recursive(node.right, data)
        # Duplicate values are not added in this BST implementation

    def search(self, key):
        """Search for a node with the given key in the BST."""
        return self._search_recursive(self.root, key)

    def _search_recursive(self, node, key):
        """Helper method to search for a node recursively."""
        if node is None or node.data == key:
            return node is not None
        if key < node.data:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, key):
        """Delete a node with the specified key."""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        """Helper method to delete a node recursively."""
        if not node:
            return node
        if key < node.data:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.data:
            node.right = self._delete_recursive(node.right, key)
        else:
            # Node with only one child or no child
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            # Node with two children: Get the inorder successor (smallest in the right subtree)
            temp = self._find_min(node.right)
            node.data = temp.data
            node.right = self._delete_recursive(node.right, temp.data)
        return node

    def _find_min(self, node):
        """Find the node with the minimum value in the subtree."""
        current = node
        while current.left is not None:
            current = current.left
        return current

    def inorder_traversal(self):
        """In-order traversal (Left, Root, Right)"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self):
        """Pre-order traversal (Root, Left, Right)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self):
        """Post-order traversal (Left, Right, Root)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.data)

# Usage Example
bst = BinarySearchTree()
bst.insert(50)
bst.insert(30)
bst.insert(70)
bst.insert(20)
bst.insert(40)
bst.insert(60)
bst.insert(80)

print("In-order Traversal:", bst.inorder_traversal())  # Output: [20, 30, 40, 50, 60, 70, 80]
print("Pre-order Traversal:", bst.preorder_traversal())  # Output: [50, 30, 20, 40, 70, 60, 80]
print("Post-order Traversal:", bst.postorder_traversal())  # Output: [20, 40, 30, 60, 80, 70, 50]

# Search for a node
print("Search for 40:", bst.search(40))  # Output: True
print("Search for 100:", bst.search(100))  # Output: False

# Delete a node
bst.delete(30)
print("In-order Traversal after deleting 30:", bst.inorder_traversal())  # Output: [20, 40, 50, 60, 70, 80]