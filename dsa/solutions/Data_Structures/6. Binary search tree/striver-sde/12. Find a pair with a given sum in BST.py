class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_pair_with_sum(root, target):
    def inorder_traversal(node, elements):
        if not node:
            return
        inorder_traversal(node.left, elements)
        elements.append(node.val)
        inorder_traversal(node.right, elements)

    elements = []
    inorder_traversal(root, elements)

    left, right = 0, len(elements) - 1
    while left < right:
        current_sum = elements[left] + elements[right]
        if current_sum == target:
            return (elements[left], elements[right])
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return None

# Example usage:
# Constructing a sample BST
root = TreeNode(5)
root.left = TreeNode(3)
root.right = TreeNode(7)
root.left.left = TreeNode(2)
root.left.right = TreeNode(4)
root.right.left = TreeNode(6)
root.right.right = TreeNode(8)

target = 9
result = find_pair_with_sum(root, target)
if result:
    print(f"Pair found: {result}")
else:
    print("No pair found.")