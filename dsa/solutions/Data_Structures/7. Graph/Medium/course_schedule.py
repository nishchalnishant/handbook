from typing import List

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        """
        Problem: Course Schedule
        Difficulty: Medium
        Time Complexity: O(V + E)
        Space Complexity: O(V + E)
        """
        preMap = { i:[] for i in range(numCourses) }
        for crs, pre in prerequisites:
            preMap[crs].append(pre)
            
        # 0: unvisited, 1: visiting, 2: visited
        visitSet = set()
        
        def dfs(crs):
            if crs in visitSet:
                return False
            if preMap[crs] == []:
                return True
            
            visitSet.add(crs)
            for pre in preMap[crs]:
                if not dfs(pre): return False
            visitSet.remove(crs)
            preMap[crs] = []
            return True
        
        for crs in range(numCourses):
            if not dfs(crs): return False
        return True
