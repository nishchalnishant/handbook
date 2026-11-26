class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        """Insert a node in the binary tree (level order)"""
        new_node = Node(data)
        if not self.root:
            self.root = new_node
            return
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if not current.left:
                current.left = new_node
                return
            else:
                queue.append(current.left)
            if not current.right:
                current.right = new_node
                return
            else:
                queue.append(current.right)

    def search(self, key):
        """Search for a node with given key in the binary tree"""
        if not self.root:
            return False
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current.data == key:
                return True
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)
        return False

    def delete(self, key):
        """Delete a node with the specified key (level order deletion)"""
        if not self.root:
            return
        if self.root.data == key and not self.root.left and not self.root.right:
            self.root = None
            return
        queue = [self.root]
        key_node = None
        last_node = None
        while queue:
            last_node = queue.pop(0)
            if last_node.data == key:
                key_node = last_node
            if last_node.left:
                queue.append(last_node.left)
            if last_node.right:
                queue.append(last_node.right)
        if key_node:
            key_node.data = last_node.data
            self._delete_deepest(last_node)

    def _delete_deepest(self, node_to_delete):
        """Helper function to delete the deepest node"""
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            if current is node_to_delete:
                current = None
                return
            if current.left:
                if current.left is node_to_delete:
                    current.left = None
                    return
                queue.append(current.left)
            if current.right:
                if current.right is node_to_delete:
                    current.right = None
                    return
                queue.append(current.right)

    def inorder_traversal(self, node):
        """In-order traversal (Left, Root, Right)"""
        if node:
            self.inorder_traversal(node.left)
            print(node.data, end=' ')
            self.inorder_traversal(node.right)

    def preorder_traversal(self, node):
        """Pre-order traversal (Root, Left, Right)"""
        if node:
            print(node.data, end=' ')
            self.preorder_traversal(node.left)
            self.preorder_traversal(node.right)

    def postorder_traversal(self, node):
        """Post-order traversal (Left, Right, Root)"""
        if node:
            self.postorder_traversal(node.left)
            self.postorder_traversal(node.right)
            print(node.data, end=' ')

    def level_order_traversal(self):
        """Level order traversal (Breadth-First)"""
        if not self.root:
            return
        queue = [self.root]
        while queue:
            current = queue.pop(0)
            print(current.data, end=' ')
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)

# Usage Example
bt = BinaryTree()
bt.insert(10)
bt.insert(20)
bt.insert(30)
bt.insert(40)
bt.insert(50)
bt.insert(60)

print("In-order Traversal:")
bt.inorder_traversal(bt.root)  # Output: 40 20 50 10 60 30
print("\nPre-order Traversal:")
bt.preorder_traversal(bt.root)  # Output: 10 20 40 50 30 60
print("\nPost-order Traversal:")
bt.postorder_traversal(bt.root)  # Output: 40 50 20 60 30 10
print("\nLevel-order Traversal:")
bt.level_order_traversal()  # Output: 10 20 30 40 50 60

# Search for a node
print("\n\nSearch for 50:", bt.search(50))  # Output: True
print("Search for 100:", bt.search(100))  # Output: False

# Delete a node
bt.delete(20)
print("Level-order Traversal after deleting 20:")
bt.level_order_traversal()  # Output may vary due to level order deletion