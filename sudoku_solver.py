import pandas as pd
import time
import random


def load_puzzles(filename, num_puzzles=100):
    """Load sudoku puzzles from CSV"""
    df = pd.read_csv(filename)
    puzzles = []
    solutions = []
    
    for i in range(min(num_puzzles, len(df))):
        puzzle = df.iloc[i]['quizzes']
        solution = df.iloc[i]['solutions']
        puzzles.append(puzzle)
        solutions.append(solution)
    
    return puzzles, solutions

def string_to_board(s):
    """Convert 81-char string to 9x9 grid"""
    board = []
    for i in range(9):
        row = [int(s[i*9 + j]) for j in range(9)]
        board.append(row)
    return board

def board_to_string(board):
    """Convert 9x9 grid back to string"""
    return ''.join(str(board[i][j]) for i in range(9) for j in range(9))


def print_board(board):
    """Pretty print the sudoku board"""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


def is_valid(board, row, col, num):
    """Check if placing num at (row, col) is valid"""
    # Check row
    if num in board[row]:
        return False
    
    # Check column
    if num in [board[i][col] for i in range(9)]:
        return False
    
    # Check 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            if board[i][j] == num:
                return False
    
    return True

def get_possible_values(board, row, col):
    """Get all valid numbers for a cell"""
    if board[row][col] != 0:
        return []
    
    possible = []
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            possible.append(num)
    return possible


class SudokuSolver:
    def __init__(self, heuristic='sequential'):
        self.heuristic = heuristic
        self.backtracks = 0
        
    def solve(self, board):
        """Main solving function"""
        self.backtracks = 0
        result = self._solve_recursive(board)
        return result
    
    def _solve_recursive(self, board):
        """Recursive backtracking"""
        # Find empty cell using chosen heuristic
        cell = self._find_empty_cell(board)
        
        if cell is None:
            return True  # Solved!
        
        row, col = cell
        
        # Try each number 1-9
        for num in range(1, 10):
            if is_valid(board, row, col, num):
                board[row][col] = num
                
                if self._solve_recursive(board):
                    return True
                
                # Backtrack
                board[row][col] = 0
                self.backtracks += 1
        
        return False
    
    def _find_empty_cell(self, board):
        """Find next empty cell based on heuristic"""
        
        if self.heuristic == 'sequential':
            # Row by row, left to right
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        return (i, j)
        
        elif self.heuristic == 'random':
            # Random empty cell
            empty_cells = [(i, j) for i in range(9) for j in range(9) if board[i][j] == 0]
            if empty_cells:
                return random.choice(empty_cells)
        
        elif self.heuristic == 'mrv':
            # Minimum Remaining Values - cell with fewest possibilities
            min_options = 10
            best_cell = None
            
            for i in range(9):
                for j in range(9):
                    if board[i][j] == 0:
                        options = len(get_possible_values(board, i, j))
                        if options < min_options:
                            min_options = options
                            best_cell = (i, j)
            
            return best_cell
        
        return None  # No empty cells


if __name__ == "__main__":
    # Load one puzzle
    puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=1)
    
    print("Testing all three heuristics on the same puzzle:\n")
    print("="*60)
    
    for heuristic in ['sequential', 'random', 'mrv']:
        board = string_to_board(puzzles[0])  # Reset board each time
        
        solver = SudokuSolver(heuristic=heuristic)
        start = time.time()
        solved = solver.solve(board)
        elapsed = time.time() - start
        
        print(f"\n{heuristic.upper()} Heuristic:")
        print(f"  Time: {elapsed:.6f}s")
        print(f"  Backtracks: {solver.backtracks}")
        print(f"  Solved: {solved}")
    
    print("\n" + "="*60)