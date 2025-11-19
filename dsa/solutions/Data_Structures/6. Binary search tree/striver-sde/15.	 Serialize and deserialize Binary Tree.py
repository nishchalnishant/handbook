class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string."""
        def helper(node):
            if not node:
                result.append("None")
                return
            result.append(str(node.val))
            helper(node.left)
            helper(node.right)
        
        result = []
        helper(root)
        return ",".join(result)

    def deserialize(self, data):
        """Decodes your encoded data to tree."""
        def helper():
            val = next(values)
            if val == "None":
                return None
            node = TreeNode(int(val))
            node.left = helper()
            node.right = helper()
            return node
        
        values = iter(data.split(","))
        return helper()

# Example usage:
# codec = Codec()
# tree = codec.deserialize("1,2,None,None,3,4,None,None,5,None,None")
# serialized = codec.serialize(tree)
# print(serialized)