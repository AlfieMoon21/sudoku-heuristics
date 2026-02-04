# Usage Guide

## Basic Usage

### Running a Single Test
```python
from sudoku_solver import SudokuSolver, load_puzzles, string_to_board

# Load one puzzle
puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=1)
board = string_to_board(puzzles[0])

# Solve with MRV heuristic
solver = SudokuSolver(heuristic='mrv')
solved = solver.solve(board)

print(f"Solved: {solved}")
print(f"Backtracks: {solver.backtracks}")
```

### Comparing Heuristics
```python
heuristics = ['sequential', 'random', 'mrv']

for h in heuristics:
    board = string_to_board(puzzles[0])  # Reset board
    solver = SudokuSolver(heuristic=h)
    
    start = time.time()
    solver.solve(board)
    elapsed = time.time() - start
    
    print(f"{h}: {elapsed:.4f}s, {solver.backtracks} backtracks")
```

## Command Line Options
```bash
# Run solver test
python3 sudoku_solver.py

# Run experiments with default settings (50 puzzles)
python3 experiments.py

# Specify number of puzzles
python3 experiments.py 25

# Using make (if Makefile is set up)
make test
make experiment
```

## Understanding Output

### Solver Output
```
SEQUENTIAL Heuristic:
  Time: 0.000514s
  Backtracks: 135
  Solved: True
```

- **Time**: How long it took to solve (seconds)
- **Backtracks**: How many times the algorithm had to undo a choice
- **Solved**: Whether a solution was found

### Experiment Output

Results are saved to `results/experiment_results.csv`:
```csv
puzzle_id,heuristic,time_seconds,backtracks,solved
0,sequential,0.000498,135,True
0,random,0.059560,11362,True
0,mrv,0.003546,0,True
```

## Troubleshooting

### "FileNotFoundError: data/sudoku.csv"
- Make sure you've downloaded the dataset
- Place it in the `data/` directory

### "ModuleNotFoundError: No module named 'pandas'"
```bash
# Arch Linux
sudo pacman -S python-pandas python-numpy python-matplotlib

# Or pip
python3 -m pip install pandas numpy matplotlib
```

### Results directory not found
```bash
mkdir -p results
```