class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def distribute_coins(root):
    """
    Problem: Move coins such that every node has exactly 1 coin. Min moves.
    
    Approach: DP on Trees
    - Post-order traversal.
    - Balance of a node = coins_in_subtree - nodes_in_subtree.
    - Excess/Deficit must move through the edge to parent.
    - Moves += abs(left_balance) + abs(right_balance).
    
    Time Complexity: O(N)
    Space Complexity: O(H)
    """
    moves = 0
    
    def dfs(node):
        nonlocal moves
        if not node:
            return 0
        
        left_bal = dfs(node.left)
        right_bal = dfs(node.right)
        
        moves += abs(left_bal) + abs(right_bal)
        
        # Current node balance = left + right + (node.val - 1 coin needed)
        return left_bal + right_bal + node.val - 1
        
    dfs(root)
    return moves

# Example Usage
if __name__ == "__main__":
    #   3
    #  / \
    # 0   0
    root = TreeNode(3)
    root.left = TreeNode(0)
    root.right = TreeNode(0)
    
    print(f"Min moves: {distribute_coins(root)}")
