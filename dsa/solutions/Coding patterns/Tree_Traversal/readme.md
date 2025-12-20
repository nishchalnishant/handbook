# Tree Traversal 🌳

## Description
Tree traversal refers to the process of visiting (checking and/or updating) each node in a tree data structure, exactly once. Such traversals are classified by the order in which the nodes are visited.

## Strategies

### 1. Breadth-First Search (Level Order)
- **Concept**: Use a **Queue** to traverse the tree level by level. Visited nodes are expanded to their children before moving deeper.
- **Use Case**: Finding the shortest path in unweighted trees, level-by-level printing.
- **Problems**:
    - Binary Tree Level Order Traversal
    - Minimum Depth of Binary Tree
    - Binary Tree Right Side View
    - Maximum Depth of Binary Tree

### 2. Depth-First Search (Recursive/Stack)
- **Concept**: Visit children of a node before visiting siblings. Can be done recursively or using a **Stack**.
- **Variants**:
    - **Preorder** (Root -> Left -> Right)
    - **Inorder** (Left -> Root -> Right): Sorted order for BSTs.
    - **Postorder** (Left -> Right -> Root): Deleting nodes, bottom-up calculations.
- **Problems**:
    - Validate Binary Search Tree (Inorder)
    - Path Sum
    - Diameter of Binary Tree
    - Invert Binary Tree
    - Subtree of Another Tree
    - Construct Binary Tree from Preorder and Inorder Traversal

### 3. Lowest Common Ancestor (LCA)
- **Concept**: Finding the deepest node that is a parent of both target nodes.
- **Use Case**: Finding common lineage.
- **Problems**:
    - Lowest Common Ancestor of a Binary Tree
    - Lowest Common Ancestor of a Binary Search Tree

### 4. Serialization
- **Concept**: Converting a tree into a string (or array) and vice versa for storage or transmission.
- **Problems**:
    - Serialize and Deserialize Binary Tree
