# Sudoku Heuristic Comparison Study
**COMP213 - Artificial Intelligence & Machine Learning**

A comparative analysis of three cell selection heuristics for backtracking-based Sudoku solving.

## Project Overview

This project investigates how different heuristics affect the performance of a backtracking algorithm when solving Sudoku puzzles. Three heuristics are compared:

1. **Sequential** - Selects empty cells left-to-right, top-to-bottom
2. **Random** - Randomly selects an empty cell
3. **MRV (Minimum Remaining Values)** - Selects the most constrained cell (fewest possible values)

## Quick Start

### Prerequisites
- Python 3.8+
- pandas
- numpy
- matplotlib

### Installation
```bash
# Clone the repository
git clone https://github.com/AlfieMoon21/sudoku-heuristics.git
cd sudoku-heuristics

# Install dependencies (Arch Linux)
sudo pacman -S python-pandas python-numpy python-matplotlib

# Or using pip
python3 -m pip install pandas numpy matplotlib
```

### Dataset Setup

1. Download the Sudoku dataset from [Kaggle](https://www.kaggle.com/datasets/bryanpark/sudoku)
2. Extract and place `sudoku.csv` in the `data/` directory
3. The CSV should have columns: `quizzes` and `solutions`

### Usage
```bash
# Test the solver with one puzzle
python3 sudoku_solver.py

# Run full experiment (50 puzzles by default)
python3 experiments.py

# Run experiment with custom number of puzzles
python3 experiments.py 100
```

## Project Structure
```
sudoku-heuristics/
├── sudoku_solver.py      # Main solver implementation
├── experiments.py        # Experiment runner
├── data/
│   └── sudoku.csv       # Puzzle dataset (not in repo)
├── results/
│   └── experiment_results.csv  # Experimental results
├── requirements.txt
└── README.md
```

## Implementation Details

### Backtracking Algorithm

The solver uses recursive backtracking:
1. Find an empty cell (using selected heuristic)
2. Try values 1-9
3. For each valid value, recursively solve the remaining puzzle
4. If no value works, backtrack and try different value
5. Continue until puzzle is solved or all possibilities exhausted

### Heuristics Explained

**Sequential Heuristic**
- Simple left-to-right, top-to-bottom scan
- No lookahead or optimization
- Baseline for comparison

**Random Heuristic**
- Selects empty cells randomly
- Tests whether order matters
- Expected to perform poorly

**MRV Heuristic**
- Selects cell with fewest possible valid values
- Implements "fail-fast" strategy
- Most constrained variable ordering
- Expected to minimize backtracks

## Results Summary

Preliminary results from 50 puzzles:

| Heuristic  | Avg Time (s) | Avg Backtracks | Total Time (s) |
|------------|--------------|----------------|----------------|
| Sequential | 0.000417     | 99.18          | 0.0208         |
| Random     | 0.151        | 30,147         | 7.55           |
| MRV        | 0.00395      | 0              | 0.1975         |

**Key Findings:**
- MRV solved all 50 puzzles without backtracking
- Random heuristic was ~360x slower than Sequential
- MRV is ~10x slower than Sequential but never backtracks

## Metrics Collected

For each puzzle and heuristic:
- **Time** - Execution time in seconds
- **Backtracks** - Number of times algorithm had to undo a choice
- **Success** - Whether puzzle was solved

## Running Experiments
```bash
# Small test (10 puzzles, ~20 seconds)
python3 experiments.py 10

# Medium test (50 puzzles, ~2 minutes)
python3 experiments.py 50

# Large test (100 puzzles, ~5 minutes)
python3 experiments.py 100
```

Results are saved to `results/experiment_results.csv`

## Code Documentation

All functions include docstrings explaining:
- Purpose and behavior
- Parameters and return values
- Usage examples where relevant

See inline documentation in `sudoku_solver.py` for details.

## Academic Context

This work explores constraint satisfaction problems (CSPs) and heuristic search algorithms, specifically:
- Backtracking search
- Variable ordering heuristics
- Most constrained variable (MCV) / MRV heuristic
- Combinatorial optimization

## References

Key papers and resources:
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
- [Additional references to be added during literature review]

## Future Work

- Test on puzzles of varying difficulty
- Implement additional heuristics (e.g., degree heuristic, least constraining value)
- Compare with constraint propagation techniques
- Analyze computational complexity

## Author

[Your Name]  
COMP213 - Artificial Intelligence & Machine Learning  
[Your University]  
February 2026

## License

This project is for academic purposes.