from typing import List

class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Problem: Rotate Image
        Pattern: Array/Matrix
        """
        if not matrix: return
        l, r = 0, len(matrix) - 1
        while l < r:
            for i in range(r - l):
                top, bottom = l, r
                # Save top left
                topLeft = matrix[top][l + i]
                # Move bottom left to top left
                matrix[top][l + i] = matrix[bottom - i][l]
                # Move bottom right to bottom left
                matrix[bottom - i][l] = matrix[bottom][r - i]
                # Move top right to bottom right
                matrix[bottom][r - i] = matrix[top + i][r]
                # Move top left to top right
                matrix[top + i][r] = topLeft
            l += 1
            r -= 1

    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        """
        Problem: Spiral Matrix
        Pattern: Array/Matrix
        """
        res = []
        left, right = 0, len(matrix[0])
        top, bottom = 0, len(matrix)
        
        while left < right and top < bottom:
            # get every i in the top row
            for i in range(left, right):
                res.append(matrix[top][i])
            top += 1
            # get every i in the right col
            for i in range(top, bottom):
                res.append(matrix[i][right - 1])
            right -= 1
            if not (left < right and top < bottom):
                break
            # get every i in the bottom row
            for i in range(right - 1, left - 1, -1):
                res.append(matrix[bottom - 1][i])
            bottom -= 1
            # get every i in the left col
            for i in range(bottom - 1, top - 1, -1):
                res.append(matrix[i][left])
            left += 1
        return res
