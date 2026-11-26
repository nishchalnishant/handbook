from typing import List

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """
        Problem: Daily Temperatures
        Pattern: Monotonic Stack (Decreasing stack to find next greater)
        """
        res = [0] * len(temperatures)
        stack = [] # pair: [weather, index]
        
        for i, t in enumerate(temperatures):
            while stack and t > stack[-1][0]:
                stackT, stackInd = stack.pop()
                res[stackInd] = i - stackInd
            stack.append([t, i])
        return res

    def largestRectangleArea(self, heights: List[int]) -> int:
        """
        Problem: Largest Rectangle in Histogram
        Pattern: Monotonic Stack (Increasing stack)
        """
        maxArea = 0
        stack = [] # pair: (index, height)
        
        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                index, height = stack.pop()
                maxArea = max(maxArea, height * (i - index))
                start = index
            stack.append((start, h))
            
        for i, h in stack:
            maxArea = max(maxArea, h * (len(heights) - i))
            
        return maxArea
