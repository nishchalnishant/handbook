# Definition for a Node.
class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

class Solution:
    def cloneGraph(self, node: 'Node') -> 'Node':
        if not node:
            return None
        
        # A dictionary to store the mapping from original node to its clone
        cloned_nodes = {}

        # Helper function to perform DFS and clone the graph
        def dfs(current_node):
            if current_node in cloned_nodes:
                return cloned_nodes[current_node]
            
            # Clone the current node
            clone = Node(current_node.val)
            cloned_nodes[current_node] = clone
            
            # Recursively clone all the neighbors
            for neighbor in current_node.neighbors:
                clone.neighbors.append(dfs(neighbor))
            
            return clone
        
        # Start cloning from the given node
        return dfs(node)

# Explanation:
# 1. We use a dictionary `cloned_nodes` to map each original node to its clone.
# 2. The `dfs` function is used to traverse the graph and clone nodes recursively.
# 3. If a node is already cloned (exists in `cloned_nodes`), we return the clone directly.
# 4. Otherwise, we create a new clone, add it to the dictionary, and recursively clone its neighbors.
# 5. The function returns the clone of the input node.

# Example usage:
# You can create a graph using the Node class and test the cloneGraph function.