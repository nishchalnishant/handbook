def solve_sudoku(board):
    """
    Problem: Solve Sudoku using Bitmasking for optimization.
    
    Approach: Backtracking + Bitmask
    - Use arrays of integers rows[9], cols[9], boxes[3][3] to store used numbers.
    - If number 5 is used, set 5th bit (1<<5).
    - To check if k is available: not ((rows[i] >> k) & 1).
    - To set k: rows[i] |= (1 << k).
    - To unset k (backtrack): rows[i] &= ~(1 << k).
    
    Time Complexity: O(9^M) where M is number of empty cells (but very fast due to bitwise ops).
    Space Complexity: O(1) (fixed size auxiliary arrays)
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [[0] * 3 for _ in range(3)]
    
    empty_cells = []
    
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                val = int(board[i][j])
                shift = 1 << val
                rows[i] |= shift
                cols[j] |= shift
                boxes[i//3][j//3] |= shift
            else:
                empty_cells.append((i, j))
                
    def backtrack(idx):
        if idx == len(empty_cells):
            return True
            
        r, c = empty_cells[idx]
        b_r, b_c = r // 3, c // 3
        
        # Available candidates: Invert occupied mask, mask with 1-9 (bits 1..9)
        # occupied = rows[r] | cols[c] | boxes[b_r][b_c]
        # free = ~occupied & 0x3FE (binary 1111111110)
        
        occupied = rows[r] | cols[c] | boxes[b_r][b_c]
        
        for num in range(1, 10):
            shift = 1 << num
            if not (occupied & shift):
                rows[r] |= shift
                cols[c] |= shift
                boxes[b_r][b_c] |= shift
                board[r][c] = str(num)
                
                if backtrack(idx + 1):
                    return True
                    
                rows[r] &= ~shift
                cols[c] &= ~shift
                boxes[b_r][b_c] &= ~shift
                board[r][c] = '.'
                
        return False

    backtrack(0)

# Example Usage
if __name__ == "__main__":
    board = [["5","3",".",".","7",".",".",".","."],
             ["6",".",".","1","9","5",".",".","."],
             [".","9","8",".",".",".",".","6","."],
             ["8",".",".",".","6",".",".",".","3"],
             ["4",".",".","8",".","3",".",".","1"],
             ["7",".",".",".","2",".",".",".","6"],
             [".","6",".",".",".",".","2","8","."],
             [".",".",".","4","1","9",".",".","5"],
             [".",".",".",".","8",".",".","7","9"]]
    solve_sudoku(board)
    print("Solved Sudoku:")
    for row in board:
        print(row)
