# Binary Tree Overview

A specialized tree where each node has at most two children (left and right).

## Topics Covered

### 1. Types of Binary Trees
- **Binary Search Tree (BST)**: Left < Root < Right.
- **Complete/Full/Perfect**: Structure properties important for Heap and array representation.
- **Balanced (AVL/Red-Black)**: Height-balanced for O(log n) operations.

### 2. Traversals
- **DFS**:
    - **Preorder**: Root -> Left -> Right.
    - **Inorder**: Left -> Root -> Right (Sorted in BST).
    - **Postorder**: Left -> Right -> Root.
- **BFS**: Level Order (using Queue).

---

## Problems & Solutions

### Easy
1. **[Max Depth of Binary Tree](Easy/max_depth.py)**
   - Find the height (Recursive/Iterative DFS).
2. **[Invert Binary Tree](Easy/invert_tree.py)**
   - Swap left and right children.
3. **[Same Tree](Easy/same_tree.py)**
   - Check if two trees are structurally identical.
4. **[Symmetric Tree](Easy/symmetric_tree.py)**
   - Check if tree is a mirror of itself.
5. **[Subtree of Another Tree](Easy/subtree.py)**
   - Check if one tree is subtree of another.

### Medium
1. **[Binary Tree Level Order Traversal](Medium/level_order.py)**
   - Traverse level by level (BFS).
2. **[Validate Binary Search Tree](Medium/validate_bst.py)**
   - Ensure every node follows BST property.
3. **[Kth Smallest Element in a BST](Medium/kth_smallest.py)**
   - Find kth smallest value (Inorder traversal).
4. **[Construct Tree from Preorder and Inorder](Medium/construct_tree.py)**
   - Rebuild unique tree from traversals.
5. **[Lowest Common Ancestor of BST](Medium/lca_bst.py)**
   - Find LCA in O(h) or O(log n).

### Hard
1. **[Serialize and Deserialize Binary Tree](Hard/serialize_deserialize.py)**
   - Convert tree to string and back.
2. **[Binary Tree Maximum Path Sum](Hard/max_path_sum.py)**
   - Maximum path sum between any two nodes.

---

## Tips for Interviews
- **Recursive vs Iterative**: Be comfortable converting recursion to stack-based iteration.
- **Traversals**: Know which traversal solves what (e.g., Inorder for BST sorted list, Postorder for deletion).
- **BST Property**: Always leverage O(log n) search/insert in BST.
