# Sudoku Heuristics Comparison
**COMP213 - Artificial Intelligence & Machine Learning**

Comparing three cell selection heuristics for backtracking-based Sudoku solving.

## Quick Start

### Setup
```bash
# Install dependencies (Arch Linux)
sudo pacman -S python-pandas python-numpy python-matplotlib

# Download dataset from Kaggle
# https://www.kaggle.com/datasets/bryanpark/sudoku
# Place as: data/sudoku.csv
```

### Run
```bash
# Test solver
python3 sudoku_solver.py

# Run experiments
python3 experiments.py
```

## Heuristics Tested

1. **Sequential** - Left-to-right, top-to-bottom
2. **Random** - Random cell selection  
3. **MRV** - Minimum Remaining Values (most constrained cell first)

## Results (50 puzzles)

| Heuristic  | Avg Backtracks | Avg Time  |
|------------|----------------|-----------|
| Sequential | 99             | 0.0004s   |
| Random     | 30,147         | 0.15s     |
| MRV        | **0**          | 0.004s    |

**MRV solved all puzzles without backtracking!**

## Documentation

- **[CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md)** - Detailed code explanation
- **[USAGE.md](USAGE.md)** - Usage examples (optional)

## Dataset

Download from: [Kaggle Sudoku Dataset](https://www.kaggle.com/datasets/bryanpark/sudoku)  
Required format: CSV with `quizzes` and `solutions` columns

## Author

Alfie Jenkins - February 2026