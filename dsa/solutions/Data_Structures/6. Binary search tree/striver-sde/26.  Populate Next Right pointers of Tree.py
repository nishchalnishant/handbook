class Node:
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

def connect(root):
    if not root:
        return None

    # Start with the root node
    current_level = [root]

    while current_level:
        next_level = []
        for i in range(len(current_level)):
            node = current_level[i]
            # Connect the current node to the next node in the level
            if i + 1 < len(current_level):
                node.next = current_level[i + 1]
            else:
                node.next = None

            # Add children to the next level
            if node.left:
                next_level.append(node.left)
            if node.right:
                next_level.append(node.right)

        # Move to the next level
        current_level = next_level

    return root

# Helper function to print the next pointers for each level
def print_next_pointers(root):
    while root:
        current = root
        while current:
            print(current.val, end=" -> ")
            current = current.next
        print("None")
        root = root.left

# Example usage
if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)

    connect(root)
    print_next_pointers(root)