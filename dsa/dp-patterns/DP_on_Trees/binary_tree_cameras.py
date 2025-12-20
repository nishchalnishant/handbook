class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def min_camera_cover(root):
    """
    Problem: Minimize cameras to cover all nodes. Camera at node covers itself, parent, and children.
    
    Approach: DP on Trees (Greedy variation) / state-based DFS
    - States for a node:
        0: Has camera
        1: Covered by camera (but no camera here)
        2: Not covered (needs camera from parent)
    - Process from bottom-up (DFS).
    - If children need camera (state 2) -> Place camera here (state 0).
    - If children have camera (state 0) -> This node is covered (state 1).
    - If children are covered (state 1) -> This node is not covered (state 2).
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    ans = 0
    
    def dfs(node):
        nonlocal ans
        if not node:
            return 1 # Null nodes are considered covered
            
        left = dfs(node.left)
        right = dfs(node.right)
        
        if left == 2 or right == 2:
            ans += 1
            return 0 # Placed camera
            
        if left == 0 or right == 0:
            return 1 # Covered by child camera
            
        return 2 # Needs camera
        
    if dfs(root) == 2:
        ans += 1
        
    return ans

# Example Usage
if __name__ == "__main__":
    # 0
    #  \
    #   0
    #  / \
    # 0   0
    root = TreeNode(0)
    root.right = TreeNode(0)
    root.right.left = TreeNode(0)
    root.right.right = TreeNode(0)
    
    print(f"Min cameras: {min_camera_cover(root)}")
