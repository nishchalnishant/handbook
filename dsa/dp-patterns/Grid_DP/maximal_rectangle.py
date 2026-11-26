def maximal_rectangle(matrix):
    """
    Problem: Find largest rectangle containing only 1s.
    
    Approach: Grid DP + Histogram logic
    - Treat each row as base of a histogram.
    - Compute heights for each column at current row (if 1, height++, else 0).
    - Solve "Largest Rectangle in Histogram" problem for each row.
    
    Time Complexity: O(M*N)
    Space Complexity: O(N)
    """
    if not matrix: return 0
    m, n = len(matrix), len(matrix[0])
    heights = [0] * n
    max_area = 0
    
    def largest_rectangle_area(h):
        stack = [-1]
        max_a = 0
        h.append(0) # Sentinel
        for i, height in enumerate(h):
            while stack[-1] != -1 and h[stack[-1]] >= height:
                curr_h = h[stack.pop()]
                curr_w = i - stack[-1] - 1
                max_a = max(max_a, curr_h * curr_w)
            stack.append(i)
        h.pop()
        return max_a
        
    for i in range(m):
        for j in range(n):
            if matrix[i][j] == '1':
                heights[j] += 1
            else:
                heights[j] = 0
        max_area = max(max_area, largest_rectangle_area(heights))
        
    return max_area

# Example Usage
if __name__ == "__main__":
    matrix = [["1","0","1","0","0"],
              ["1","0","1","1","1"],
              ["1","1","1","1","1"],
              ["1","0","0","1","0"]]
    print(f"Maximal Rectangle Area: {maximal_rectangle(matrix)}")
