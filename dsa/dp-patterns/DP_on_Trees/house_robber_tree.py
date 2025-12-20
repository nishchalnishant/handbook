class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob_tree(root):
    """
    Problem: Leetcode 337. House Robber III.
    Cannot rob two directly-linked nodes.
    
    Approach: DP on Trees
    - Returns pair (rob_root, not_rob_root)
    - rob_root = val + not_rob_left + not_rob_right
    - not_rob_root = max(rob_left, not_rob_left) + max(rob_right, not_rob_right)
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    def dfs(node):
        if not node: return (0, 0)
        
        left = dfs(node.left)
        right = dfs(node.right)
        
        # If we rob this node
        rob = node.val + left[1] + right[1]
        
        # If we don't rob this node
        not_rob = max(left) + max(right)
        
        return (rob, not_rob)
        
    return max(dfs(root))

# Example Usage
if __name__ == "__main__":
    #   3
    #  / \
    # 2   3
    #  \   \
    #   3   1
    root = TreeNode(3)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.right = TreeNode(3)
    root.right.right = TreeNode(1)
    
    print(f"Max robbed from tree: {rob_tree(root)}")
