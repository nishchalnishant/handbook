"""
Trees & Binary Search Trees patterns and algorithms — Google L3/L4 interview prep.

Key Gotchas & Common Mistakes:
- Forgetting that a BST requires ALL left descendants to be less and ALL right descendants to be greater, not just immediate children.\n- Not handling skewed trees (worst-case O(N) time if unbalanced).\n- Losing the reference to the parent or root when modifying the tree.

Common Variants:
- DFS (Preorder, Inorder, Postorder)\n- BFS (Level Order Traversal)\n- Lowest Common Ancestor (LCA)\n- Tree construction from traversal arrays

General Tips & Best Practices:
- Inorder traversal of a BST gives a sorted array.\n- Many tree problems can be solved by answering: 'What does this node need from its children?' (Postorder).

Patterns covered in this module:
  - Reference implementations and key problem-solving strategies.
"""

from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Node:
    def __init__(self, val: int = 0, left: 'Node' = None, right: 'Node' = None, next: 'Node' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next

class TreeSolutions:
    # -----------------------------------------------------------------------
    # 1. Binary Tree Level Order Traversal (LC 102) — T1
    # Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).
    # Example: root = [3,9,20,null,null,15,7] → [[3],[9,20],[15,7]]
    # Constraints: The number of nodes in the tree is in the range [0, 2000], 1000 <= Node.val <= 1000
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root: return []
        res = []
        # Queue for BFS
        q = deque([root])
        while q:
            level = []
            # Snapshot queue size for current level
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                # Enqueue children only if they are not null
                if node.left: 
                    q.append(node.left)
                if node.right: 
                    q.append(node.right)
            res.append(level)
        return res

    # -----------------------------------------------------------------------
    # 2. Validate BST (LC 98) — T1
    # Given the root of a binary tree, determine if it is a valid binary search tree (BST).
    # Example: root = [2,1,3] → true
    # Constraints: The number of nodes in the tree is in the range [1, 10^4], 2^31 <= Node.val <= 2^31 - 1
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def valid(node, left_bound, right_bound):
            # Base case: empty tree is valid
            if not node: 
                return True
            # Verify current node value falls strictly within parent bounds
            if not (left_bound < node.val < right_bound):
                return False
            # Recurse left with updated upper bound and right with updated lower bound
            return (valid(node.left, left_bound, node.val) and
                    valid(node.right, node.val, right_bound))
        # Launch check with infinite boundaries
        return valid(root, float("-inf"), float("inf"))

    # -----------------------------------------------------------------------
    # 3. LCA of Binary Tree (LC 236) — T1
    # Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
    # Example: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1 → 3
    # Constraints: The number of nodes in the tree is in the range [2, 10^5]
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        # Base cases: found targets or hit null leaf
        if not root or root == p or root == q:
            return root
        # Check subtrees recursively
        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        # Split point: if both subtrees found a target, this is the LCA
        if left and right: 
            return root
        # Otherwise, bubble up the side that succeeded
        return left if left else right

    # -----------------------------------------------------------------------
    # 4. Binary Tree Max Path Sum (LC 124) — T1
    # A path in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. Return the maximum path sum of any non-empty path.
    # Example: root = [1,2,3] → 6
    # Constraints: The number of nodes in the tree is in the range [1, 3 * 10^4]
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        res = [root.val]

        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            if not node: return 0
            # Compute max path gain of left and right children, ignoring negative paths
            leftMax = max(dfs(node.left), 0)
            rightMax = max(dfs(node.right), 0)

            # Update global max sum using current node as splitting/turning point
            res[0] = max(res[0], node.val + leftMax + rightMax)
            # Return max single branch sum to parent
            return node.val + max(leftMax, rightMax)

        dfs(root)
        return res[0]

    # -----------------------------------------------------------------------
    # 5. Serialize / Deserialize Binary Tree (LC 297) — T1
    # Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.
    # Example: root = [1,2,3,null,null,4,5] → [1,2,3,null,null,4,5]
    # Constraints: The number of nodes in the tree is in the range [0, 10^4]
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def serialize(self, root: Optional[TreeNode]) -> str:
        res = []
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: append null marker
            if not node:
                res.append("N")
                return
            # Preorder step: append root value, then recurse left and right
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(res)

    # Time: O(n), Space: O(n)
    def deserialize(self, data: str) -> Optional[TreeNode]:
        # Split serialized string by delimiter
        vals = data.split(",")
        # Initialize index pointer
        self.i = 0
        def dfs():
            """Depth-first-search helper for the enclosing solution."""
            # Return None if null marker is encountered
            if vals[self.i] == "N":
                self.i += 1
                return None
            # Build node and recurse left and right
            node = TreeNode(int(vals[self.i]))
            self.i += 1
            node.left = dfs()
            node.right = dfs()
            return node
        # Launch pre-order deserialization
        return dfs()

    # -----------------------------------------------------------------------
    # 6. Diameter of Binary Tree (LC 543) — T1
    # Given the root of a binary tree, return the length of the diameter of the tree. The diameter of a binary tree is the length of the longest path between any two nodes in a tree. This path may or may not pass through the root. The length of a path between two nodes is represented by the number of edges between them.
    # Example: root = [1,2,3,4,5] → 3
    # Constraints: The number of nodes in the tree is in the range [1, 10^4], 100 <= Node.val <= 100
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        res = [0]
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            if not node: return 0
            # Get height of left and right subtrees
            left = dfs(node.left)
            right = dfs(node.right)
            # Update candidate path max
            res[0] = max(res[0], left + right)
            # Return edge height to parent
            return 1 + max(left, right)
        dfs(root)
        return res[0]

    # -----------------------------------------------------------------------
    # 7. Construct Tree from Pre+Inorder (LC 105) — T1
    # Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
    # Example: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7] → [3,9,20,null,null,15,7]
    # Constraints: 1 <= preorder.length <= 3000
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        # Map inorder values to indices for fast lookups
        inorder_idx = {v: i for i, v in enumerate(inorder)}
        self.pre_idx = 0

        def build(left, right):
            # Base case: empty subarray range
            if left > right: return None

            # Next element in preorder sequence is the current root
            root_val = preorder[self.pre_idx]
            self.pre_idx += 1
            root = TreeNode(root_val)

            # Find split index in inorder and build left/right subtrees
            idx = inorder_idx[root_val]
            root.left = build(left, idx - 1)
            root.right = build(idx + 1, right)
            return root

        return build(0, len(inorder) - 1)

    # -----------------------------------------------------------------------
    # 8. Construct Tree from Inorder + Postorder (LC 106) — L4
    # Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.
    # Example: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3] → [3,9,20,null,null,15,7]
    # Constraints: 1 <= inorder.length <= 3000, Postorder: last element is root. Mirror of preorder approach
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def buildTreePost(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        inorder_idx = {v: i for i, v in enumerate(inorder)}
        self.post_idx = len(postorder) - 1

        def build(left, right):
            if left > right:
                return None
            root_val = postorder[self.post_idx]
            self.post_idx -= 1
            root = TreeNode(root_val)
            idx = inorder_idx[root_val]
            root.right = build(idx + 1, right)   # right before left (postorder traversed right-to-left)
            root.left = build(left, idx - 1)
            return root

        return build(0, len(inorder) - 1)

class TreeSolutionsT2:
    # -----------------------------------------------------------------------
    # 8. Maximum Depth of Binary Tree (LC 104) — T2
    # Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
    # Example: root = [3,9,20,null,null,15,7] → 3
    # Constraints: The number of nodes in the tree is in the range [0, 10^4], 100 <= Node.val <= 100
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root: return 0
        return 1 + max(self.maxDepth(root.left), self.maxDepth(root.right))

    # -----------------------------------------------------------------------
    # 9. Invert Binary Tree (LC 226) — T2
    # Given the root of a binary tree, invert the tree, and return its root.
    # Example: root = [4,2,7,1,3,6,9] → [4,7,2,9,6,3,1]
    # Constraints: The number of nodes in the tree is in the range [0, 100], 100 <= Node.val <= 100
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root: return None
        # Swap children pointers in place
        root.left, root.right = root.right, root.left
        # Recurse on left and right children
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root

    # -----------------------------------------------------------------------
    # 10. Symmetric Tree (LC 101) — T2
    # Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).
    # Example: root = [1,2,2,3,4,4,3] → true
    # Constraints: The number of nodes in the tree is in the range [1, 1000], 100 <= Node.val <= 100, Follow up: Could you solve it both recursively and iteratively?
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root: return True
        def isMirror(t1, t2):
            # Base cases: both null is symmetric, one null is not
            if not t1 and not t2: return True
            if not t1 or not t2: return False
            # Check mirror children pairs
            return (t1.val == t2.val) and isMirror(t1.left, t2.right) and isMirror(t1.right, t2.left)
        return isMirror(root.left, root.right)

    # -----------------------------------------------------------------------
    # 11. LCA of BST (LC 235) — T2
    # Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.
    # Example: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8 → 6
    # Constraints: The number of nodes in the tree is in the range [2, 10^5]
    # Time: O(h), Space: O(1)
    # -----------------------------------------------------------------------
    def lowestCommonAncestorBST(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """LCA of BST (LC 235): Exploit the BST ordering property to navigate without recursion."""
        curr = root
        # Walk down tree using ordering rules
        while curr:
            # If both targets are in right subtree
            if p.val > curr.val and q.val > curr.val:
                curr = curr.right
            # If both targets are in left subtree
            elif p.val < curr.val and q.val < curr.val:
                curr = curr.left
            # Straddle found: this is the LCA
            else:
                return curr

    # -----------------------------------------------------------------------
    # 12. Kth Smallest in BST (LC 230) — T2
    # Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
    # Example: root = [3,1,4,null,2], k = 1 → 1
    # Constraints: The number of nodes in the tree is n, 1 <= k <= n <= 10^4
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        stack = []
        curr = root
        # Iterative in-order using explicit stack
        while stack or curr:
            # Go deep left
            while curr:
                stack.append(curr)
                curr = curr.left
            # Process node
            curr = stack.pop()
            k -= 1
            if k == 0:
                return curr.val
            # Advance to right child
            curr = curr.right

    # -----------------------------------------------------------------------
    # 13. House Robber III (LC 337) — T2
    # The thief has found himself a new place for his thievery again. There is only one entrance to this area, called root. Besides the root, each house has one and only one parent house. After a tour, the smart thief realized that all houses in this place form a binary tree. It will automatically contact the police if two directly-linked houses were broken into on the same night. Given the root of the binary tree, return the maximum amount of money the thief can rob without alerting the police.
    # Example: root = [3,2,3,null,3,null,1] → 7
    # Constraints: The number of nodes in the tree is in the range [1, 10^4], 0 <= Node.val <= 10^4
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def rob(self, root: Optional[TreeNode]) -> int:
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            if not node: return [0, 0] # [withRoot, withoutRoot]

            left = dfs(node.left)
            right = dfs(node.right)

            withRoot = node.val + left[1] + right[1]
            withoutRoot = max(left) + max(right)

            return [withRoot, withoutRoot]
        return max(dfs(root))

    # -----------------------------------------------------------------------
    # 14. Binary Tree Cameras (LC 968) — T2
    # You are given the root of a binary tree. We install cameras on the tree nodes where each camera at a node can monitor its parent, itself, and its immediate children. Return the minimum number of cameras needed to monitor all nodes of the tree.
    # Example: root = [0,0,null,0,0] → 1
    # Constraints: The number of nodes in the tree is in the range [1, 1000], Node.val == 0
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def minCameraCover(self, root: Optional[TreeNode]) -> int:
        res = [0]
        # 0 = strictly need camera, 1 = has camera, 2 = covered
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: null node is covered
            if not node: return 2

            # Recurse left and right
            left = dfs(node.left)
            right = dfs(node.right)

            # If either child is uncovered, place a camera here
            if left == 0 or right == 0:
                res[0] += 1
                return 1
            # If either child has a camera, this parent is covered
            if left == 1 or right == 1:
                return 2
            # Otherwise, this node needs coverage from its parent
            return 0

        if dfs(root) == 0:
            res[0] += 1
        return res[0]

    # -----------------------------------------------------------------------
    # 15. Recover BST (LC 99) — T2
    # You are given the root of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.
    # Example: root = [1,3,null,null,2] → [3,1,null,null,2]
    # Constraints: The number of nodes in the tree is in the range [2, 1000]
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def recoverTree(self, root: Optional[TreeNode]) -> None:
        first, second, prev = None, None, None

        def inorder(node):
            nonlocal first, second, prev
            if not node: return

            inorder(node.left)

            # Detect out-of-order BST elements
            if prev and prev.val > node.val:
                # First violation identifies first swapped node
                if not first:
                    first = prev
                # Second violation (or fallback of first) identifies second swapped node
                second = node
            prev = node

            inorder(node.right)

        inorder(root)
        # Swap values of the two mismatched nodes
        if first and second:
            first.val, second.val = second.val, first.val

    # -----------------------------------------------------------------------
    # 16. Vertical Order Traversal (LC 314) — T2
    # Given the root of a binary tree, calculate the vertical order traversal of the binary tree. For each node at position (row, col), its left and right children will be at positions (row + 1, col - 1) and (row + 1, col + 1). Sort by column, then row, then value.
    # Example: root = [3,9,20,null,null,15,7] → [[9],[3,15],[20],[7]]
    # Constraints: The number of nodes in the tree is in the range [1, 1000]
    # Time: O(n log n), Space: O(n)
    # -----------------------------------------------------------------------
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        from collections import defaultdict
        if not root: return []

        col_map = defaultdict(list)
        q = deque([(root, 0, 0)]) # node, row, col
        min_col, max_col = 0, 0

        while q:
            node, row, col = q.popleft()
            col_map[col].append((row, node.val))
            min_col = min(min_col, col)
            max_col = max(max_col, col)

            if node.left: q.append((node.left, row + 1, col - 1))
            if node.right: q.append((node.right, row + 1, col + 1))

        res = []
        for c in range(min_col, max_col + 1):
            col_map[c].sort()
            res.append([val for row, val in col_map[c]])
        return res

    # -----------------------------------------------------------------------
    # 17. Flatten Binary Tree to LL (LC 114) — T2
    # Given the root of a binary tree, flatten the tree into a "linked list". The "linked list" should use the same TreeNode class where the right child pointer points to the next node in the list and the left child pointer is always null. The "linked list" should be in the same order as a pre-order traversal of the binary tree.
    # Example: root = [1,2,5,3,4,null,6] → [1,null,2,null,3,null,4,null,5,null,6]
    # Constraints: The number of nodes in the tree is in the range [0, 2000]
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def flatten(self, root: Optional[TreeNode]) -> None:
        curr = root
        # Walk the tree rewiring pointers in place
        while curr:
            if curr.left:
                # Find predecessor of current node in left subtree
                runner = curr.left
                while runner.right:
                    runner = runner.right
                # Rewire right pointer of predecessor to current right subtree
                runner.right = curr.right
                # Move left subtree to the right
                curr.right = curr.left
                curr.left = None
            # Move to next node in list sequence
            curr = curr.right

    # -----------------------------------------------------------------------
    # 18. Path Sum III (LC 437) — T2
    # Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum. The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).
    # Example: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8 → 3
    # Constraints: The number of nodes in the tree is in the range [0, 1000], 10^9 <= Node.val <= 10^9, 1000 <= targetSum <= 1000
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:
        """Path Sum III (LC 437): Use a prefix-sum hash map combined with DFS."""
        from collections import defaultdict
        prefix_sum = defaultdict(int)
        prefix_sum[0] = 1

        def dfs(node, curr_sum):
            """Depth-first-search helper for the enclosing solution."""
            if not node: return 0

            # Accumulate running path sum
            curr_sum += node.val
            # Count matching sub-paths ending at current node
            count = prefix_sum[curr_sum - targetSum]

            # Update map, recurse and backtrack
            prefix_sum[curr_sum] += 1
            count += dfs(node.left, curr_sum)
            count += dfs(node.right, curr_sum)
            prefix_sum[curr_sum] -= 1

            return count
        return dfs(root, 0)

    # -----------------------------------------------------------------------
    # 19. Count Good Nodes in Binary Tree (LC 1448) — T2
    # Given a binary tree root, a node X in the tree is named good if in the path from root to X there are no nodes with a value greater than X. Return the number of good nodes in the binary tree.
    # Example: root = [3,1,4,3,null,1,5] → 4
    # Constraints: The number of nodes in the binary tree is in the range [1, 10^5], Each node's value is between [-10^4, 10^4]
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def goodNodes(self, root: TreeNode) -> int:
        def dfs(node, maxVal):
            """Depth-first-search helper for the enclosing solution."""
            if not node:
                return 0

            # Node is good if it is at least as large as maximum so far
            res = 1 if node.val >= maxVal else 0
            maxVal = max(maxVal, node.val)
            res += dfs(node.left, maxVal)
            res += dfs(node.right, maxVal)
            return res

        return dfs(root, root.val)

    # -----------------------------------------------------------------------
    # 20. All Nodes Distance K in Binary Tree (LC 863) — T2
    # Given the root of a binary tree, the value of a target node target, and an integer k, return an array of the values of all nodes that have a distance k from the target node. You can return the answer in any order.
    # Example: root = [3,5,1,6,2,0,8,null,null,7,4], target = 5, k = 2 → [7,4,1]
    # Constraints: The number of nodes in the tree is in the range [1, 500], 0 <= Node.val <= 500, All the values Node.val are unique, target is the value of one of the nodes in the tree, 0 <= k <= 1000
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def distanceK(self, root: TreeNode, target: TreeNode, k: int) -> List[int]:
        from collections import defaultdict, deque
        graph = defaultdict(list)

        def build_graph(node, parent):
            # Link child and parent bidirectionally
            if node and parent:
                graph[node.val].append(parent.val)
                graph[parent.val].append(node.val)
            if node.left:
                build_graph(node.left, node)
            if node.right:
                build_graph(node.right, node)

        # Build adjacency list representation of the tree
        build_graph(root, None)

        # Queue stores (value, distance_from_target)
        q = deque([(target.val, 0)])
        visited = {target.val}
        res = []

        # BFS out to distance k
        while q:
            node_val, dist = q.popleft()
            if dist == k:
                res.append(node_val)
            elif dist < k:
                for neighbor in graph[node_val]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        q.append((neighbor, dist + 1))
        return res

    # -----------------------------------------------------------------------
    # 21. Populating Next Right Pointers in Each Node (LC 116) — T2
    # You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition: struct Node { int val; Node *left; Node *right; Node *next; } Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL. Initially, all next pointers are set to NULL.
    # Example: root = [1,2,3,4,5,6,7] → [1,#,2,3,#,4,5,6,7,#]
    # Constraints: The number of nodes in the tree is in the range [0, 2^12 - 1], 1000 <= Node.val <= 1000, Follow-up:, You may only use constant extra space, The recursive approach is fine. You may assume implicit stack space does not count as extra space, for this problem
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def connect(self, root: 'Optional[Node]') -> 'Optional[Node]':
        if not root:
            return None

        curr = root
        nxt = root.left

        # Traverse levels from top to bottom
        while curr and nxt:
            # Connect left child to right child
            curr.left.next = curr.right
            # Connect right child to left child of next sibling
            if curr.next:
                curr.right.next = curr.next.left

            # Move to next sibling node
            curr = curr.next
            # Drop to the next level once current is finished
            if not curr:
                curr = nxt
                nxt = curr.left

        return root

    # -----------------------------------------------------------------------
    # 22. Binary Tree Right Side View (LC 199) — T1
    # Given the root of a binary tree, imagine yourself standing on the right side of it, return the values of the nodes you can see ordered from top to bottom.
    # Example: root = [1,2,3,null,5,null,4] → [1,3,4]
    # Constraints: The number of nodes in the tree is in the range [0, 100], 100 <= Node.val <= 100
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        res = []
        q = deque([root])

        # BFS level by level
        while q:
            rightSide = None
            qLen = len(q)

            # Process all nodes in current level
            for i in range(qLen):
                node = q.popleft()
                if node:
                    # Update to track the rightmost node processed so far
                    rightSide = node
                    if node.left: q.append(node.left)
                    if node.right: q.append(node.right)

            # Append value of rightmost node at this level
            if rightSide:
                res.append(rightSide.val)

        return res

    # -----------------------------------------------------------------------
    # 13. Lowest Common Ancestor of Deepest Leaves (LC 1123) — T2
    # Given the root of a binary tree, return the lowest common ancestor of its deepest leaves. Recall that: children is d + 1. every node in S is in the subtree with root A.
    # Example: root = [3,5,1,6,2,0,8,null,null,7,4] → [2,7,4]
    # Constraints: The number of nodes in the tree will be in the range [1, 1000], 0 <= Node.val <= 1000, The values of the nodes in the tree are unique, Note: This question is the same as 865: https://leetcode.com/problems/smallest-subtree-with-all-the-, deepest-nodes/
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def lcaDeepestLeaves(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            """Depth-first-search helper for the enclosing solution."""
            # Base case: null node has 0 depth and no LCA
            if not node:
                return 0, None
            l_depth, l_lca = dfs(node.left)
            r_depth, r_lca = dfs(node.right)

            # Left branch goes deeper
            if l_depth > r_depth:
                return l_depth + 1, l_lca
            # Right branch goes deeper
            elif r_depth > l_depth:
                return r_depth + 1, r_lca
            # Both sides have equal depth; this is the local LCA
            else:
                return l_depth + 1, node

        return dfs(root)[1]

class TreeSolutionsL4:
    # -----------------------------------------------------------------------
    # 1. Morris Inorder Traversal (LC 94)
    # O(1) space inorder traversal using threading
    # Time: O(n), Space: O(1)
    # -----------------------------------------------------------------------
    def morrisInorder(self, root: Optional[TreeNode]) -> List[int]:
        result = []
        curr = root
        while curr:
            if not curr.left:
                result.append(curr.val)
                curr = curr.right
            else:
                # find inorder predecessor
                runner = curr.left
                while runner.right and runner.right is not curr:
                    runner = runner.right
                if runner.right is None:
                    # first visit: set thread, go left
                    runner.right = curr
                    curr = curr.left
                else:
                    # second visit: remove thread, record value, go right
                    runner.right = None
                    result.append(curr.val)
                    curr = curr.right
        return result

    # -----------------------------------------------------------------------
    # 2. Boundary of Binary Tree (LC 545)
    # Left boundary + leaves + right boundary (anti-clockwise)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def boundaryOfBinaryTree(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []

        def is_leaf(node):
            return not node.left and not node.right

        def left_boundary(node):
            res = []
            # Traversal for left boundary
            while node:
                # Add value if it is not a leaf node
                if not is_leaf(node):
                    res.append(node.val)
                # Left child takes priority, fallback to right child
                if node.left:
                    node = node.left
                else:
                    node = node.right
            return res

        def right_boundary(node):
            res = []
            # Traversal for right boundary
            while node:
                # Add value if it is not a leaf node
                if not is_leaf(node):
                    res.append(node.val)
                # Right child takes priority, fallback to left child
                if node.right:
                    node = node.right
                else:
                    node = node.left
            # Anti-clockwise requirement: reverse right boundary
            return res[::-1]

        def leaves(node):
            if not node:
                return []
            # Base case: collect leaf values
            if is_leaf(node):
                return [node.val]
            # Recursively collect left and right leaves
            return leaves(node.left) + leaves(node.right)

        if is_leaf(root):
            return [root.val]

        return ([root.val]
                + left_boundary(root.left)
                + leaves(root.left) + leaves(root.right)
                + right_boundary(root.right))

    # -----------------------------------------------------------------------
    # 3. Find Leaves of Binary Tree (LC 366)
    # Group leaves by height (distance from the deepest leaf)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def findLeaves(self, root: Optional[TreeNode]) -> List[List[int]]:
        result: List[List[int]] = []

        def height(node) -> int:
            if not node:
                return -1
            # Compute height of subtrees bottom-up
            left_h = height(node.left)
            right_h = height(node.right)
            h = 1 + max(left_h, right_h)
            # Expand result buckets as height increases
            if h == len(result):
                result.append([])
            result[h].append(node.val)
            return h

        height(root)
        return result

    # -----------------------------------------------------------------------
    # 4. Maximum Width of Binary Tree (LC 662)
    # Level order with virtual position indices
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def widthOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        max_width = 0
        q: deque = deque([(root, 0)])
        while q:
            level_len = len(q)
            _, level_start = q[0]
            first = last = 0
            for i in range(level_len):
                node, idx = q.popleft()
                idx -= level_start  # normalise to prevent overflow
                if i == 0:
                    first = idx
                last = idx
                if node.left:
                    q.append((node.left, 2 * idx))
                if node.right:
                    q.append((node.right, 2 * idx + 1))
            max_width = max(max_width, last - first + 1)
        return max_width

    # -----------------------------------------------------------------------
    # 5. Check Completeness of Binary Tree (LC 958)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def isCompleteTree(self, root: Optional[TreeNode]) -> bool:
        """Check Completeness of Binary Tree (LC 958): Run BFS level by level."""
        if not root:
            return True
        q: deque = deque([root])
        found_null = False
        # BFS traversal
        while q:
            node = q.popleft()
            # If null node is encountered, set flag
            if node is None:
                found_null = True
            else:
                # If non-null is found after any null, it's not a complete tree
                if found_null:
                    return False
                q.append(node.left)
                q.append(node.right)
        return True

    # -----------------------------------------------------------------------
    # 6. Cousins in Binary Tree (LC 993)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def isCousins(self, root: Optional[TreeNode], x: int, y: int) -> bool:
        """Cousins in Binary Tree (LC 993): DFS the tree tracking each node's depth and parent."""
        info = {}  # val -> (depth, parent_val)

        def dfs(node, depth, parent_val):
            """Depth-first-search helper for the enclosing solution."""
            if not node:
                return
            # If target node is found, capture depth and parent value
            if node.val == x or node.val == y:
                info[node.val] = (depth, parent_val)
            # Recurse down left and right subtrees
            dfs(node.left, depth + 1, node.val)
            dfs(node.right, depth + 1, node.val)

        dfs(root, 0, None)
        if x not in info or y not in info:
            return False
        dx, px = info[x]
        dy, py = info[y]
        return dx == dy and px != py

    # -----------------------------------------------------------------------
    # 7. Step-By-Step Directions From a Binary Tree Node to Another (LC 2096)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        def find_path(node, target, path):
            if not node:
                return False
            # Return True when target is reached
            if node.val == target:
                return True
            # Backtracking path selection: try Left
            path.append('L')
            if find_path(node.left, target, path):
                return True
            path.pop()
            # Try Right
            path.append('R')
            if find_path(node.right, target, path):
                return True
            path.pop()
            return False

        # find LCA
        def lca(node):
            """Returns the lowest common ancestor for the requested nodes."""
            if not node:
                return None
            if node.val == startValue or node.val == destValue:
                return node
            left = lca(node.left)
            right = lca(node.right)
            # If targets are on different sides of current node, this is LCA
            if left and right:
                return node
            return left or right

        lca_node = lca(root)
        start_path: List[str] = []
        dest_path: List[str] = []
        find_path(lca_node, startValue, start_path)
        find_path(lca_node, destValue, dest_path)
        return 'U' * len(start_path) + ''.join(dest_path)

    # -----------------------------------------------------------------------
    # 8. Minimum Absolute Difference in BST (LC 530)
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def getMinimumDifference(self, root: Optional[TreeNode]) -> int:
        prev = None
        min_diff = float('inf')

        def inorder(node):
            nonlocal prev, min_diff
            if not node:
                return
            inorder(node.left)
            # Calculate difference between adjacent sorted values
            if prev is not None:
                min_diff = min(min_diff, node.val - prev)
            prev = node.val
            inorder(node.right)

        inorder(root)
        return min_diff

    # -----------------------------------------------------------------------
    # 9. Convert BST to Greater Tree (LC 538)
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def convertBST(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        acc = 0

        def reverse_inorder(node):
            nonlocal acc
            if not node:
                return
            # Right-first inorder traversal (visiting largest values first)
            reverse_inorder(node.right)
            # Accumulate values and overwrite node value
            acc += node.val
            node.val = acc
            reverse_inorder(node.left)

        reverse_inorder(root)
        return root

    # -----------------------------------------------------------------------
    # 10. Balance a Binary Search Tree (LC 1382)
    # Time: O(n), Space: O(n)
    # -----------------------------------------------------------------------
    def balanceBST(self, root: TreeNode) -> TreeNode:
        sorted_vals: List[int] = []

        def inorder(node):
            if not node:
                return
            inorder(node.left)
            # Gather elements in sorted ascending order
            sorted_vals.append(node.val)
            inorder(node.right)

        def build(left, right):
            if left > right:
                return None
            # Choose middle element as root to ensure height balance
            mid = (left + right) // 2
            node = TreeNode(sorted_vals[mid])
            node.left = build(left, mid - 1)
            node.right = build(mid + 1, right)
            return node

        inorder(root)
        return build(0, len(sorted_vals) - 1)

    # -----------------------------------------------------------------------
    # 11. Trim a Binary Search Tree (LC 669)
    # Time: O(n), Space: O(h)
    # -----------------------------------------------------------------------
    def trimBST(self, root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
        """Trim a Binary Search Tree (LC 669): Recursively trim the BST."""
        if not root:
            return None
        # If value is too small, discard left subtree and trim right subtree
        if root.val < low:
            return self.trimBST(root.right, low, high)
        # If value is too large, discard right subtree and trim left subtree
        if root.val > high:
            return self.trimBST(root.left, low, high)
        # Re-link trimmed left and right subtrees
        root.left = self.trimBST(root.left, low, high)
        root.right = self.trimBST(root.right, low, high)
        return root

    # -----------------------------------------------------------------------
    # 12. Delete Node in BST (LC 450)
    # Time: O(h), Space: O(h)
    # -----------------------------------------------------------------------
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
        """Delete Node in BST (LC 450): Search for the key using BST ordering."""
        if not root:
            return None
        if key < root.val:
            root.left = self.deleteNode(root.left, key)
        elif key > root.val:
            root.right = self.deleteNode(root.right, key)
        else:
            if not root.left:
                return root.right
            if not root.right:
                return root.left
            # find inorder successor (leftmost in right subtree)
            successor = root.right
            while successor.left:
                successor = successor.left
            root.val = successor.val
            root.right = self.deleteNode(root.right, successor.val)
        return root

    # -----------------------------------------------------------------------
    # 13. Insert into BST (LC 701)
    # Time: O(h), Space: O(h)
    # -----------------------------------------------------------------------
    def insertIntoBST(self, root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
        """Insert into BST (LC 701): Traverse the BST using standard BST search."""
        # Base case: create and insert new node
        if not root:
            return TreeNode(val)
        # Recurse left if value is smaller than current root
        if val < root.val:
            root.left = self.insertIntoBST(root.left, val)
        # Recurse right if value is larger
        else:
            root.right = self.insertIntoBST(root.right, val)
        return root


if __name__ == "__main__":
    def make_tree(vals):
        # BFS-style construction from list (None = missing node)
        """Builds tree for tests or examples."""
        if not vals:
            return None
        from collections import deque
        # Initialize root node
        root = TreeNode(vals[0])
        q = deque([root])
        i = 1
        # Reconstruct tree in BFS order
        while q and i < len(vals):
            node = q.popleft()
            # Reconstruct left child if present
            if i < len(vals) and vals[i] is not None:
                node.left = TreeNode(vals[i])
                q.append(node.left)
            i += 1
            # Reconstruct right child if present
            if i < len(vals) and vals[i] is not None:
                node.right = TreeNode(vals[i])
                q.append(node.right)
            i += 1
        return root

    sol = TreeSolutions()
    sol2 = TreeSolutionsT2()

    # levelOrder
    assert sol.levelOrder(make_tree([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert sol.levelOrder(None) == []

    # isValidBST
    assert sol.isValidBST(make_tree([2, 1, 3])) == True
    assert sol.isValidBST(make_tree([5, 1, 4, None, None, 3, 6])) == False

    # lowestCommonAncestor
    root = make_tree([3, 5, 1, 6, 2, 0, 8])
    p = root.left          # 5
    q_node = root.right    # 1
    assert sol.lowestCommonAncestor(root, p, q_node).val == 3

    # maxPathSum
    assert sol.maxPathSum(make_tree([1, 2, 3])) == 6
    assert sol.maxPathSum(make_tree([-10, 9, 20, None, None, 15, 7])) == 42

    # serialize / deserialize
    original = make_tree([1, 2, 3, None, None, 4, 5])
    data = sol.serialize(original)
    from collections import deque
    def tree_to_list(root):
        if not root: return []
        res, q = [], deque([root])
        # Reconstruct list via level-order
        while q:
            n = q.popleft()
            res.append(n.val if n else None)
            if n:
                q.append(n.left); q.append(n.right)
        # Strip trailing None values
        while res and res[-1] is None:
            res.pop()
        return res
    assert tree_to_list(sol.deserialize(data)) == tree_to_list(original)

    # diameterOfBinaryTree
    assert sol.diameterOfBinaryTree(make_tree([1, 2, 3, 4, 5])) == 3
    assert sol.diameterOfBinaryTree(make_tree([1, 2])) == 1

    # buildTree (preorder + inorder)
    assert tree_to_list(sol.buildTree([3, 9, 20, 15, 7], [9, 3, 15, 20, 7])) == [3, 9, 20, None, None, 15, 7]

    # maxDepth
    assert sol2.maxDepth(make_tree([3, 9, 20, None, None, 15, 7])) == 3
    assert sol2.maxDepth(None) == 0

    # invertTree
    assert tree_to_list(sol2.invertTree(make_tree([4, 2, 7, 1, 3, 6, 9]))) == [4, 7, 2, 9, 6, 3, 1]

    # isSymmetric
    assert sol2.isSymmetric(make_tree([1, 2, 2, 3, 4, 4, 3])) == True
    assert sol2.isSymmetric(make_tree([1, 2, 2, None, 3, None, 3])) == False

    # lowestCommonAncestorBST
    bst = make_tree([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5])
    assert sol2.lowestCommonAncestorBST(bst, TreeNode(2), TreeNode(8)).val == 6
    assert sol2.lowestCommonAncestorBST(bst, TreeNode(2), TreeNode(4)).val == 2

    # kthSmallest
    assert sol2.kthSmallest(make_tree([3, 1, 4, None, 2]), 1) == 1
    assert sol2.kthSmallest(make_tree([5, 3, 6, 2, 4, None, None, 1]), 3) == 3

    # rob (House Robber III)
    assert sol2.rob(make_tree([3, 2, 3, None, 3, None, 1])) == 7
    assert sol2.rob(make_tree([3, 4, 5, 1, 3, None, 1])) == 9

    # pathSum (path sum count)
    assert sol2.pathSum(make_tree([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]), 8) == 3

    # goodNodes
    assert sol2.goodNodes(make_tree([3, 1, 4, 3, None, 1, 5])) == 4

    # rightSideView
    assert sol2.rightSideView(make_tree([1, 2, 3, None, 5, None, 4])) == [1, 3, 4]
    assert sol2.rightSideView(None) == []

    # buildTreePost (inorder + postorder) — L4 variant
    tree = sol.buildTreePost([9, 3, 15, 20, 7], [9, 15, 7, 20, 3])
    assert tree_to_list(tree) == [3, 9, 20, None, None, 15, 7]  # same tree as preorder variant

    sol4 = TreeSolutionsL4()

    # morrisInorder
    assert sol4.morrisInorder(make_tree([4, 2, 6, 1, 3, 5, 7])) == [1, 2, 3, 4, 5, 6, 7]
    assert sol4.morrisInorder(make_tree([1])) == [1]
    assert sol4.morrisInorder(None) == []

    # boundaryOfBinaryTree
    assert sol4.boundaryOfBinaryTree(make_tree([1, None, 2, 3, 4])) == [1, 3, 4, 2]
    assert sol4.boundaryOfBinaryTree(make_tree([1])) == [1]

    # findLeaves
    assert sol4.findLeaves(make_tree([1, 2, 3, 4, 5])) == [[4, 5, 3], [2], [1]]

    # widthOfBinaryTree
    assert sol4.widthOfBinaryTree(make_tree([1, 3, 2, 5, 3, None, 9])) == 4
    assert sol4.widthOfBinaryTree(make_tree([1, 3, 2, 5, None, None, 9, 6, None, 7])) == 7
    assert sol4.widthOfBinaryTree(make_tree([1])) == 1

    # isCompleteTree
    assert sol4.isCompleteTree(make_tree([1, 2, 3, 4, 5, 6])) == True
    assert sol4.isCompleteTree(make_tree([1, 2, 3, 4, 5, None, 7])) == False

    # isCousins
    assert sol4.isCousins(make_tree([1, 2, 3, 4]), 4, 3) == False
    assert sol4.isCousins(make_tree([1, 2, 3, None, 4, None, 5]), 5, 4) == True
    assert sol4.isCousins(make_tree([1, 2, 3, None, 4]), 2, 3) == False

    # getDirections
    assert sol4.getDirections(make_tree([5, 1, 2, 3, None, 6, 4]), 3, 6) == "UURL"
    assert sol4.getDirections(make_tree([2, 1]), 2, 1) == "L"

    # getMinimumDifference
    assert sol4.getMinimumDifference(make_tree([4, 2, 6, 1, 3])) == 1
    assert sol4.getMinimumDifference(make_tree([1, 0, 48, None, None, 12, 49])) == 1

    # convertBST — use a simple tree: [3, 2, 4, 1]
    # inorder: 1, 2, 3, 4; suffix sums: 1->10, 2->9, 3->7, 4->4
    simple = make_tree([3, 2, 4, 1])
    sol4.convertBST(simple)
    assert simple.val == 7          # root 3 -> 3+4 = 7
    assert simple.left.val == 9     # node 2 -> 2+3+4 = 9
    assert simple.right.val == 4    # node 4 -> 4 (no greater values)

    # balanceBST — result should be a valid BST with same inorder
    unbalanced = make_tree([1, None, 2, None, None, None, 3, None, None, None, None, None, None, None, 4])
    # make a right-skewed tree manually
    skewed = TreeNode(1)
    skewed.right = TreeNode(2)
    skewed.right.right = TreeNode(3)
    skewed.right.right.right = TreeNode(4)
    balanced = sol4.balanceBST(skewed)
    assert sol4.morrisInorder(balanced) == [1, 2, 3, 4]
    # height should be 2 (balanced)
    def height_check(node):
        if not node: return 0
        return 1 + max(height_check(node.left), height_check(node.right))
    assert height_check(balanced) <= 3  # balanced BST of 4 nodes has height 2 or 3

    # trimBST
    assert tree_to_list(sol4.trimBST(make_tree([1, 0, 2]), 1, 2)) == [1, None, 2]
    assert tree_to_list(sol4.trimBST(make_tree([3, 0, 4, None, 2, None, None, None, None, 1]), 1, 3)) == [3, 2]

    # deleteNode
    result_del = sol4.deleteNode(make_tree([5, 3, 6, 2, 4, None, 7]), 3)
    assert sol4.morrisInorder(result_del) == [2, 4, 5, 6, 7]
    result_del2 = sol4.deleteNode(make_tree([5, 3, 6, 2, 4, None, 7]), 0)
    assert sol4.morrisInorder(result_del2) == [2, 3, 4, 5, 6, 7]

    # insertIntoBST
    inserted = sol4.insertIntoBST(make_tree([4, 2, 7, 1, 3]), 5)
    assert sol4.morrisInorder(inserted) == [1, 2, 3, 4, 5, 7]
    assert sol4.insertIntoBST(None, 5).val == 5

    print("All tree tests passed.")
