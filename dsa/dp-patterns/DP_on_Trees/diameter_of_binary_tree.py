class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def diameter_of_binary_tree(root):
    """
    Problem: Length of longest path between any two nodes in a tree.
    
    Approach: DP on Trees (Post-order traversal)
    - At each node, we need:
        1. Max depth of left subtree.
        2. Max depth of right subtree.
    - Diameter passing through this node = left_depth + right_depth.
    - Update global max diameter.
    - Return max_depth (1 + max(left, right)) to parent.
    
    Time Complexity: O(N)
    Space Complexity: O(H) (Recursion stack)
    """
    max_diameter = 0
    
    def depth(node):
        nonlocal max_diameter
        if not node:
            return 0
        
        left_d = depth(node.left)
        right_d = depth(node.right)
        
        # Diameter through current node
        max_diameter = max(max_diameter, left_d + right_d)
        
        # Return depth to parent
        return 1 + max(left_d, right_d)
        
    depth(root)
    return max_diameter

# Example Usage
if __name__ == "__main__":
    #   1
    #  / \
    # 2   3
    # | \
    # 4  5
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print(f"Diameter: {diameter_of_binary_tree(root)}")
