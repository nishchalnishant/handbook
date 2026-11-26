from typing import Optional
from collections import deque

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        """Encodes a tree to a single string."""
        if not root: return "[]"
        res = []
        q = deque([root])
        while q:
            node = q.popleft()
            if node:
                res.append(str(node.val))
                q.append(node.left)
                q.append(node.right)
            else:
                res.append("null")
        return "[" + ",".join(res) + "]"

    def deserialize(self, data: str) -> Optional[TreeNode]:
        """Decodes your encoded data to tree."""
        if data == "[]": return None
        vals = data[1:-1].split(",")
        root = TreeNode(int(vals[0]))
        q = deque([root])
        i = 1
        while q:
            node = q.popleft()
            if vals[i] != "null":
                node.left = TreeNode(int(vals[i]))
                q.append(node.left)
            i += 1
            if vals[i] != "null":
                node.right = TreeNode(int(vals[i]))
                q.append(node.right)
            i += 1
        return root
