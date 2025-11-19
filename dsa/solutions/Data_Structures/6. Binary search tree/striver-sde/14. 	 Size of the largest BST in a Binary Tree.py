class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def largestBSTSubtree(self, root: TreeNode) -> int:
        def helper(node):
            if not node:
                return (True, 0, float('inf'), float('-inf'))  # isBST, size, minVal, maxVal
            
            left = helper(node.left)
            right = helper(node.right)
            
            if left[0] and right[0] and left[3] < node.val < right[2]:
                size = left[1] + right[1] + 1
                return (True, size, min(node.val, left[2]), max(node.val, right[3]))
            else:
                return (False, max(left[1], right[1]), 0, 0)
        
        return helper(root)[1]

# Example usage:
# root = TreeNode(10)
# root.left = TreeNode(5)
# root.right = TreeNode(15)
# root.left.left = TreeNode(1)
# root.left.right = TreeNode(8)
# root.right.right = TreeNode(7)

# sol = Solution()
# print(sol.largestBSTSubtree(root))  # Output: Size of the largest BST