from typing import List
from collections import deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Problem: Course Schedule
        Pattern: Topological Sort (Kahn's Algorithm - BFS)
        """
        adj = {i: [] for i in range(numCourses)}
        indegree = {i: 0 for i in range(numCourses)}
        
        for crs, pre in prerequisites:
            adj[pre].append(crs)
            indegree[crs] += 1
            
        q = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                q.append(i)
                
        finish = 0
        while q:
            node = q.popleft()
            finish += 1
            for neighbor in adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    q.append(neighbor)
                    
        return finish == numCourses

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        """
        Problem: Course Schedule II
        Pattern: Topological Sort
        """
        adj = {i: [] for i in range(numCourses)}
        indegree = {i: 0 for i in range(numCourses)}
        
        for crs, pre in prerequisites:
            adj[pre].append(crs)
            indegree[crs] += 1
            
        q = deque()
        for i in range(numCourses):
            if indegree[i] == 0:
                q.append(i)
                
        output = []
        while q:
            node = q.popleft()
            output.append(node)
            for neighbor in adj[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    q.append(neighbor)
                    
        return output if len(output) == numCourses else []
