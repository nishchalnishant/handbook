class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def max_path_sum(root):
    """
    Problem: Find max path sum. Path can start/end anywhere.
    
    Approach: DP on Trees
    - Similar to Diameter, but values can be negative.
    - max_gain(node) = node.val + max(left_gain, right_gain, 0)
        - We compare with 0 because we can choose NOT to include a negative sum path.
    - Path sum through node = node.val + max(left, 0) + max(right, 0).
    - Update global max path sum.
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    max_sum = float('-inf')
    
    def max_gain(node):
        nonlocal max_sum
        if not node:
            return 0
            
        left_gain = max(max_gain(node.left), 0)
        right_gain = max(max_gain(node.right), 0)
        
        # Current path sum including split at this node
        price_new_path = node.val + left_gain + right_gain
        max_sum = max(max_sum, price_new_path)
        
        # Return max gain contributing to parent path
        return node.val + max(left_gain, right_gain)
        
    max_gain(root)
    return max_sum

# Example Usage
if __name__ == "__main__":
    #   -10
    #   /  \
    #  9   20
    #     /  \
    #    15   7
    root = TreeNode(-10)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    print(f"Max Path Sum: {max_path_sum(root)}")
