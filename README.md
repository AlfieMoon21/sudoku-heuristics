# Sudoku Heuristics Comparison
**COMP213 - Artificial Intelligence & Machine Learning**

Comparing three cell selection heuristics for backtracking-based Sudoku solving.

## Quick Start

### Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download dataset from Kaggle
# https://www.kaggle.com/datasets/bryanpark/sudoku
# Place as: data/sudoku.csv
```

### Run
```bash
# Test solver on one puzzle
python3 sudoku_solver.py

# Run full experiments (200 puzzles, generates all figures and stats)
python3 experiments.py

# Run with custom puzzle count
python3 experiments.py 100
```

## Heuristics Tested

1. **Sequential** - Left-to-right, top-to-bottom
2. **Random** - Random cell selection
3. **MRV** - Minimum Remaining Values (most constrained cell first)

## Results (200 puzzles)

| Heuristic  | Mean BT | Median BT | Mean Time |
|------------|---------|-----------|-----------|
| Sequential | 95.70   | 60        | 0.000421s |
| Random     | 33,216  | 14,517    | 0.185786s |
| MRV        | **0**   | **0**     | 0.004142s |

All pairwise differences significant at p < 0.001 (Mann-Whitney U test).

**MRV solved all 200 puzzles without backtracking.**

## Output Files

- `results/experiment_results.csv` — raw per-puzzle results
- `results/fig1_backtracks_comparison.png` — mean backtracks bar chart
- `results/fig2_time_comparison.png` — mean time bar chart
- `results/fig3_distributions.png` — backtrack distributions
- `results/fig4_per_puzzle.png` — per-puzzle backtrack line plot
- `results/fig6_difficulty_correlation.png` — empty cells vs sequential backtracks

## Documentation

- **[CODE_DOCUMENTATION.md](CODE_DOCUMENTATION.md)** - Detailed code explanation
- **[USAGE.md](USAGE.md)** - Usage examples

## Dataset

Download from: [Kaggle Sudoku Dataset](https://www.kaggle.com/datasets/bryanpark/sudoku)
Required format: CSV with `quizzes` and `solutions` columns

## Author

Alfie Jenkins - February 2026
