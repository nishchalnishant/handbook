from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        """
        Problem: Merge Intervals
        Difficulty: Medium
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        intervals.sort(key=lambda i: i[0])
        output = [intervals[0]]
        
        for start, end in intervals[1:]:
            lastEnd = output[-1][1]
            
            if start <= lastEnd:
                output[-1][1] = max(lastEnd, end)
            else:
                output.append([start, end])
        return output

# Test
if __name__ == "__main__":
    sol = Solution()
    print(sol.merge([[1,3],[2,6],[8,10],[15,18]])) # [[1,6],[8,10],[15,18]]
