# Code Documentation

## Overview

This document explains how the Sudoku solver code works, breaking down each component and algorithm.

## File Structure

### sudoku_solver.py
Main implementation file containing:
- Data loading functions
- Board display functions
- Sudoku validation logic
- Backtracking solver with three heuristics

### experiments.py
Experiment runner that:
- Tests all three heuristics on multiple puzzles
- Records performance metrics
- Saves results to CSV
- Prints summary statistics

---

## How It Works - Step by Step

### 1. Loading Puzzles

**Function: `load_puzzles(filename, num_puzzles=100)`**

Takes the CSV file and extracts puzzle strings.
```python
puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=10)
```

**Input:** CSV file with columns `quizzes` and `solutions`  
**Output:** Two lists of 81-character strings

Example string: `"004300209005009001070060043..."`
- Each character is a digit 0-9
- 0 means empty cell
- 81 characters total (9×9 grid)

---

### 2. Converting Data Format

**Function: `string_to_board(s)`**

Converts the 81-character string into a 9×9 grid (list of lists).

**Example:**
```
Input:  "004300209005009001..."
Output: [[0,0,4,3,0,0,2,0,9],
         [0,0,5,0,0,9,0,0,1],
         ...]
```

**How it works:**
- Loop through 9 rows
- For each row, take 9 characters from the string
- Convert each character to an integer
- Build a 2D list

**Function: `board_to_string(board)`**

Does the reverse - converts 9×9 grid back to 81-character string.

---

### 3. Displaying the Board

**Function: `print_board(board)`**

Makes the board readable with grid lines.

**Output looks like:**
```
0 0 4  | 3 0 0  | 2 0 9
0 0 5  | 0 0 9  | 0 0 1
0 7 0  | 0 6 0  | 0 4 3
- - - - - - - - - - - -
...
```

**How it works:**
- Loop through all 81 cells
- Add horizontal line every 3 rows (`i % 3 == 0`)
- Add vertical separator every 3 columns (`j % 3 == 0`)
- Print the number at each position

---

### 4. Sudoku Validation

**Function: `is_valid(board, row, col, num)`**

Checks if placing a number at a position follows Sudoku rules.

**The three rules checked:**

**Rule 1: Row Check**
```python
if num in board[row]:
    return False
```
Checks if the number already exists anywhere in that row.

**Rule 2: Column Check**
```python
if num in [board[i][col] for i in range(9)]:
    return False
```
Checks if the number already exists anywhere in that column.

**Rule 3: 3×3 Box Check**
```python
box_row, box_col = 3 * (row // 3), 3 * (col // 3)
```

This math finds which 3×3 box the cell belongs to:
- `row // 3` gives 0, 1, or 2 (which vertical box)
- Multiply by 3 to get starting row (0, 3, or 6)
- Same for columns

Then checks all 9 cells in that box.

**Example:**
- Cell at row=5, col=7
- Box row: `3 * (5 // 3) = 3 * 1 = 3`
- Box col: `3 * (7 // 3) = 3 * 2 = 6`
- Check box from (3,6) to (5,8)

---

**Function: `get_possible_values(board, row, col)`**

Returns list of all valid numbers (1-9) that can go in a cell.

**How it works:**
- If cell is already filled (not 0), return empty list
- Try each number 1-9
- Use `is_valid()` to check if it's allowed
- Return list of valid numbers

**Example:**
```python
possible = get_possible_values(board, 0, 0)
# might return [1, 6, 8] - only these are valid for that cell
```

---

### 5. The Backtracking Algorithm

**Class: `SudokuSolver`**

This is the heart of the program. It uses **backtracking** to solve puzzles.

#### What is Backtracking?

Think of it like exploring a maze:
1. Try a path
2. If you hit a dead end, go back and try a different path
3. Keep trying until you find the exit

For Sudoku:
1. Pick an empty cell
2. Try placing numbers 1-9
3. For each valid number, try to solve the rest of the puzzle
4. If you get stuck, undo that number and try the next one
5. Keep going until puzzle is solved

#### Initialization
```python
solver = SudokuSolver(heuristic='mrv')
```

**Parameters:**
- `heuristic`: Which strategy to use ('sequential', 'random', or 'mrv')

**Attributes:**
- `self.heuristic`: Stores which strategy
- `self.backtracks`: Counter for how many times we backtrack

---

#### Main Solve Function

**Function: `solve(board)`**
```python
solved = solver.solve(board)
```

**What it does:**
- Resets the backtrack counter to 0
- Calls the recursive solving function
- Returns `True` if solved, `False` if impossible

**Important:** This modifies the board directly (in-place).

---

#### Recursive Solving

**Function: `_solve_recursive(board)`**

This is where the magic happens. Here's the algorithm step-by-step:

**Step 1: Find an empty cell**
```python
cell = self._find_empty_cell(board)
```
Uses the chosen heuristic to pick which empty cell to fill next.

**Step 2: Check if done**
```python
if cell is None:
    return True  # No empty cells = solved!
```

**Step 3: Try each number 1-9**
```python
row, col = cell

for num in range(1, 10):
    if is_valid(board, row, col, num):
        board[row][col] = num  # Place the number
```

**Step 4: Recursively solve the rest**
```python
        if self._solve_recursive(board):
            return True  # Success! This path works
```

**Step 5: Backtrack if it didn't work**
```python
        # If we reach here, that number didn't lead to a solution
        board[row][col] = 0  # Undo (backtrack)
        self.backtracks += 1
```

**Step 6: Return failure if no number worked**
```python
return False  # None of 1-9 worked, need to backtrack further
```

---

### 6. The Three Heuristics

**Function: `_find_empty_cell(board)`**

This chooses WHICH empty cell to fill next. Different strategies can make the algorithm much faster or slower.

---

#### Heuristic 1: Sequential
```python
if self.heuristic == 'sequential':
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
```

**Strategy:** Just scan left-to-right, top-to-bottom.

**Pros:**
- Simple
- Fast to find next cell
- Predictable

**Cons:**
- Might pick cells with many possibilities
- Can waste time exploring wrong paths

**Performance:** Medium (baseline)

---

#### Heuristic 2: Random
```python
elif self.heuristic == 'random':
    empty_cells = [(i, j) for i in range(9) 
                   for j in range(9) if board[i][j] == 0]
    if empty_cells:
        return random.choice(empty_cells)
```

**Strategy:** Pick any empty cell randomly.

**How it works:**
- Build list of all empty cells
- Use `random.choice()` to pick one

**Pros:**
- Shows that cell order matters
- Good for testing

**Cons:**
- Very inefficient
- Might pick "easy" cells with many options
- Explores many unnecessary paths

**Performance:** WORST (very slow, many backtracks)

---

#### Heuristic 3: MRV (Minimum Remaining Values)
```python
elif self.heuristic == 'mrv':
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
```

**Strategy:** Pick the cell with the FEWEST possible values (most constrained).

**Why this works:**
- If a cell only has 1 option, we MUST use that number
- If a cell has 2 options, we'll quickly find out if we're wrong
- Fails fast when on wrong path
- Reduces search space dramatically

**How it works:**
- Check every empty cell
- Count how many valid numbers each one can have
- Pick the one with the smallest count

**Pros:**
- Much smarter than sequential
- Minimizes backtracks
- Often solves without ANY backtracking

**Cons:**
- Slower per iteration (has to check all cells)
- More computation to pick next cell

**Performance:** BEST (fewest backtracks, often 0!)

---

## Performance Comparison

From our experiments on 50 puzzles:

| Heuristic  | Avg Backtracks | Avg Time  | How it works |
|------------|----------------|-----------|--------------|
| Sequential | ~100           | 0.0004s   | First empty cell |
| Random     | ~30,000        | 0.15s     | Random empty cell |
| MRV        | **0**          | 0.004s    | Most constrained cell |

**Key insight:** MRV never backtracked on any puzzle! It always picked the right path.

---

## Example: How MRV Finds the Best Cell

Imagine this partial board:
```
Cell A: Can be [1, 2, 3, 4, 5] - 5 options
Cell B: Can be [7, 9] - 2 options
Cell C: Can be [3] - 1 option
```

**Sequential:** Would pick Cell A (first one found)  
**Random:** Might pick any of them  
**MRV:** Picks Cell C (only 1 option - must be 3!)

If Cell B is picked:
- Try 7 → might work or might not
- Try 9 → might work or might not

If Cell C is picked:
- Must be 3 → guaranteed right!

---

## The experiments.py File

### What It Does

Runs all three heuristics on multiple puzzles and records:
- Time taken
- Number of backtracks
- Whether it solved successfully

### Main Function: `run_experiments(num_puzzles=50)`

**Process:**

1. **Load puzzles**
```python
   puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=50)
```

2. **For each puzzle, test all three heuristics**
```python
   for idx, puzzle_str in enumerate(puzzles):
       for heuristic in ['sequential', 'random', 'mrv']:
```

3. **Reset the board for each test**
```python
   board = string_to_board(puzzle_str)
```
   Important: Each heuristic gets a fresh copy!

4. **Time the solving**
```python
   start = time.time()
   solved = solver.solve(board)
   elapsed = time.time() - start
```

5. **Record the results**
```python
   results.append({
       'puzzle_id': idx,
       'heuristic': heuristic,
       'time_seconds': elapsed,
       'backtracks': solver.backtracks,
       'solved': solved
   })
```

6. **Save to CSV**
```python
   df = pd.DataFrame(results)
   df.to_csv('results/experiment_results.csv', index=False)
```

7. **Print summary statistics**
   - Average time per heuristic
   - Average backtracks per heuristic
   - Total time per heuristic

---

## Data Flow Diagram
```
CSV File (sudoku.csv)
    ↓
load_puzzles() → List of 81-char strings
    ↓
string_to_board() → 9×9 grid (2D list)
    ↓
SudokuSolver.solve() → Backtracking algorithm
    ↓
    ├→ _find_empty_cell() → Pick next cell (heuristic)
    ├→ is_valid() → Check if number is valid
    ├→ _solve_recursive() → Try numbers 1-9, recurse
    └→ Backtrack if stuck
    ↓
Solved board (modified in-place)
    ↓
Results (time, backtracks) → Save to CSV
```

---

## Key Concepts Explained

### Recursion

The algorithm calls itself:
```python
def _solve_recursive(board):
    # ...
    if self._solve_recursive(board):  # Calls itself!
        return True
```

Each call tries to solve one cell, then recursively solves the rest.

### Backtracking

When a path doesn't work:
```python
board[row][col] = 0  # Undo our choice
self.backtracks += 1  # Count it
```

Go back and try a different number.

### In-Place Modification

The board is modified directly:
```python
board[row][col] = num  # Changes the original board
```

Not creating new copies - faster but need to reset for each test.

### Heuristic

A strategy or "rule of thumb" for making decisions.

In our case: How to choose which cell to fill next.

---

## Common Questions

**Q: Why does MRV have 0 backtracks?**  
A: It's so smart at picking cells that it never makes a wrong choice. By always filling the most constrained cell, it fails fast if on wrong path and finds the right path quickly.

**Q: Why is Random so slow?**  
A: It might pick cells with many options (like 7 possible numbers), then waste time trying all of them when other cells only have 1-2 options.

**Q: Does Sequential always work?**  
A: Yes! All three heuristics will eventually solve any solvable puzzle. They just take different amounts of time and backtracks.

**Q: Why is MRV slower per puzzle than Sequential?**  
A: MRV has to check all empty cells and count their options to find the best one. Sequential just picks the first. But MRV's smarter choices mean it backtracks way less, so it's still better overall for harder puzzles.

---

## Summary

1. **Load** puzzles from CSV
2. **Convert** to 9×9 grid
3. **Solve** using backtracking:
   - Pick empty cell (using heuristic)
   - Try numbers 1-9
   - Recurse
   - Backtrack if stuck
4. **Record** performance metrics
5. **Compare** heuristics

The experiment shows that **how you choose cells matters a lot** - MRV is clearly the best strategy!