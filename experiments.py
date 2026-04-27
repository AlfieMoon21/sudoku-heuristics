import pandas as pd
import time
import csv
from sudoku_solver import SudokuSolver, load_puzzles, string_to_board

def run_experiments(num_puzzles=50):
    """Run experiments comparing all three heuristics"""
    
    print(f"Loading {num_puzzles} puzzles...")
    puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=num_puzzles)
    
    results = []
    heuristics = ['sequential', 'random', 'mrv']
    
    for idx, puzzle_str in enumerate(puzzles):
        print(f"\nPuzzle {idx + 1}/{num_puzzles}")
        
        for heuristic in heuristics:
            board = string_to_board(puzzle_str)
            
            solver = SudokuSolver(heuristic=heuristic)
            start = time.time()
            solved = solver.solve(board)
            elapsed = time.time() - start
            
            results.append({
                'puzzle_id': idx,
                'heuristic': heuristic,
                'time_seconds': elapsed,
                'backtracks': solver.backtracks,
                'solved': solved
            })
            
            print(f"  {heuristic:12} - Time: {elapsed:.6f}s, Backtracks: {solver.backtracks}")
    
    # Save results to CSV
    df = pd.DataFrame(results)
    df.to_csv('results/experiment_results.csv', index=False)
    print(f"\n✅ Results saved to results/experiment_results.csv")
    
    # Print summary statistics
    print("\n" + "="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    
    for heuristic in heuristics:
        heur_data = df[df['heuristic'] == heuristic]
        avg_time = heur_data['time_seconds'].mean()
        avg_backtracks = heur_data['backtracks'].mean()
        
        print(f"\n{heuristic.upper()}:")
        print(f"  Average Time: {avg_time:.6f}s")
        print(f"  Average Backtracks: {avg_backtracks:.2f}")
        print(f"  Total Time: {heur_data['time_seconds'].sum():.4f}s")

if __name__ == "__main__":
    import sys
    
    # Allow command line argument for number of puzzles
    num = 50
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    
    run_experiments(num_puzzles=num)