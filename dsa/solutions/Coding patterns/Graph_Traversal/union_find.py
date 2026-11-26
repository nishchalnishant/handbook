from typing import List

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [1] * (n + 1)
        
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x]) # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)
        if rootX != rootY:
            if self.rank[rootX] > self.rank[rootY]:
                self.parent[rootY] = rootX
                self.rank[rootX] += self.rank[rootY]
            else:
                self.parent[rootX] = rootY
                self.rank[rootY] += self.rank[rootX]
            return True
        return False

class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        """
        Problem: Redundant Connection
        Pattern: Union Find (Cycle Detection)
        """
        dsu = DSU(len(edges))
        for u, v in edges:
            if not dsu.union(u, v):
                return [u, v]
        return []

    def makeConnected(self, n: int, connections: List[List[int]]) -> int:
        """
        Problem: Number of Operations to Make Network Connected
        Pattern: Union Find
        """
        if len(connections) < n - 1: return -1
        dsu = DSU(n)
        components = n
        
        for u, v in connections:
            # We assume 0-indexed nodes for this problem, adjusting DSU slightly or passing mapped nodes
            # DSU above is 1-indexed ready, but works for 0-indexed if we ignore index n
            if dsu.find(u) != dsu.find(v):
                dsu.union(u, v)
                components -= 1
                
        return components - 1
