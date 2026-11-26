"""
Hard Recursion Problems
-----------------------
This file contains solutions to 10 advanced recursion and backtracking problems.
"""

# 1. N-Queens
# Place n queens on an n x n chessboard such that no two queens attack each other
def solve_n_queens(n):
    res = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    
    def is_safe(row, col):
        for i in range(row):
            if board[i][col] == 'Q': return False
        for i, j in zip(range(row-1, -1, -1), range(col-1, -1, -1)):
            if board[i][j] == 'Q': return False
        for i, j in zip(range(row-1, -1, -1), range(col+1, n)):
            if board[i][j] == 'Q': return False
        return True

    def backtrack(row):
        if row == n:
            res.append(["".join(r) for r in board])
            return
        for col in range(n):
            if is_safe(row, col):
                board[row][col] = 'Q'
                backtrack(row + 1)
                board[row][col] = '.'
    
    backtrack(0)
    return res

# 2. Sudoku Solver
# Solve a given Sudoku board
def solve_sudoku(board):
    def is_valid(r, c, val):
        for i in range(9):
            if board[r][i] == val or board[i][c] == val: return False
        start_r, start_c = 3 * (r // 3), 3 * (c // 3)
        for i in range(3):
            for j in range(3):
                if board[start_r + i][start_c + j] == val: return False
        return True

    def backtrack():
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    for val in map(str, range(1, 10)):
                        if is_valid(i, j, val):
                            board[i][j] = val
                            if backtrack(): return True
                            board[i][j] = '.'
                    return False
        return True
    
    backtrack()
    return board

# 3. Word Search II (Core logic: Find one word)
def exist(board, word):
    rows, cols = len(board), len(board[0])
    def backtrack(r, c, index):
        if index == len(word): return True
        if r < 0 or c < 0 or r >= rows or c >= cols or board[r][c] != word[index]:
            return False
        temp, board[r][c] = board[r][c], '#'
        res = any(backtrack(r+dr, c+dc, index+1) for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)])
        board[r][c] = temp
        return res
    
    for r in range(rows):
        for c in range(cols):
            if backtrack(r, c, 0): return True
    return False

# 4. Palindromic Partitioning
# Partition a string into all possible palindromes
def partition(s):
    res = []
    def backtrack(start, path):
        if start == len(s):
            res.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if sub == sub[::-1]:
                path.append(sub)
                backtrack(end, path)
                path.pop()
    backtrack(0, [])
    return res

# 5. Wildcard Matching
# Implement wildcard pattern matching with '?' and '*'
def is_wildcard_match(s, p):
    memo = {}
    def backtrack(i, j):
        if (i, j) in memo: return memo[(i, j)]
        if j == len(p): return i == len(s)
        
        match = i < len(s) and (p[j] == s[i] or p[j] == '?')
        if p[j] == '*':
            res = backtrack(i, j + 1) or (i < len(s) and backtrack(i + 1, j))
        else:
            res = match and backtrack(i + 1, j + 1)
        
        memo[(i, j)] = res
        return res
    return backtrack(0, 0)

# 6. Regular Expression Matching
def is_regex_match(s, p):
    memo = {}
    def backtrack(i, j):
        if (i, j) in memo: return memo[(i, j)]
        if j == len(p): return i == len(s)
        
        match = i < len(s) and (p[j] == s[i] or p[j] == '.')
        if j + 1 < len(p) and p[j+1] == '*':
            res = backtrack(i, j + 2) or (match and backtrack(i + 1, j))
        else:
            res = match and backtrack(i + 1, j + 1)
        
        memo[(i, j)] = res
        return res
    return backtrack(0, 0)

# 7. Flatten a Nested List
def flatten(nested):
    res = []
    def backtrack(curr):
        for item in curr:
            if isinstance(item, list):
                backtrack(item)
            else:
                res.append(item)
    backtrack(nested)
    return res

# 8. K-th Permutation Sequence
import math
def get_permutation(n, k):
    nums = list(range(1, n + 1))
    def backtrack(n, k, nums):
        if n == 0: return ""
        fact = math.factorial(n - 1)
        idx = (k - 1) // fact
        val = nums.pop(idx)
        return str(val) + backtrack(n - 1, (k - 1) % fact + 1, nums)
    return backtrack(n, k, nums)

# 9. Rat in a Maze
def find_paths(maze):
    n = len(maze)
    res = []
    def backtrack(r, c, path):
        if r == n - 1 and c == n - 1:
            res.append(path)
            return
        maze[r][c] = 0 # Mark visited
        for dr, dc, move in [(1,0,'D'),(0,-1,'L'),(0,1,'R'),(-1,0,'U')]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and maze[nr][nc] == 1:
                backtrack(nr, nc, path + move)
        maze[r][c] = 1 # Unmark
    
    if maze[0][0] == 1: backtrack(0, 0, "")
    return res

# 10. M-Coloring Problem
def graph_coloring(adj, m, n):
    colors = [0] * n
    def is_safe(v, c):
        for neighbor in adj[v]:
            if colors[neighbor] == c: return False
        return True
    
    def backtrack(v):
        if v == n: return True
        for c in range(1, m + 1):
            if is_safe(v, c):
                colors[v] = c
                if backtrack(v + 1): return True
                colors[v] = 0
        return False
    
    return backtrack(0)

if __name__ == "__main__":
    print(f"N-Queens (4): Found {len(solve_n_queens(4))} solutions.")
    print(f"Palindrome Partitioning 'aab': {partition('aab')}")
    print(f"Wildcard Match 'aa' with '*': {is_wildcard_match('aa', '*')}")
    print(f"Regex Match 'aa' with 'a*': {is_regex_match('aa', 'a*')}")
    print(f"Flatten [1,[2,3],[[4]]]: {flatten([1,[2,3],[[4]]])}")
    print(f"3rd permutation of n=3: {get_permutation(3, 3)}") # Expect '213'
    maze = [[1, 0, 0, 0], [1, 1, 0, 1], [1, 1, 0, 0], [0, 1, 1, 1]]
    print(f"Rat in maze: {find_paths(maze)}")
