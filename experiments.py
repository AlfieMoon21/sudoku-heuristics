import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import csv
import random
from scipy import stats
from sudoku_solver import SudokuSolver, load_puzzles, string_to_board


def count_empty_cells(puzzle_str):
    return str(puzzle_str).count('0')


def run_experiments(num_puzzles=200):
    random.seed(42)

    print(f"Loading {num_puzzles} puzzles...")
    puzzles, solutions = load_puzzles('data/sudoku.csv', num_puzzles=num_puzzles)

    results = []
    heuristics = ['sequential', 'random', 'mrv']

    for idx, puzzle_str in enumerate(puzzles):
        print(f"\rPuzzle {idx + 1}/{num_puzzles}", end='', flush=True)
        empty_cells = count_empty_cells(puzzle_str)

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
                'solved': solved,
                'empty_cells': empty_cells,
            })

    print()
    df = pd.DataFrame(results)
    df.to_csv('results/experiment_results.csv', index=False)
    print("Results saved to results/experiment_results.csv")

    _print_summary(df, heuristics)
    _run_statistics(df)
    _generate_figures(df, num_puzzles)


def _print_summary(df, heuristics):
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    for heuristic in heuristics:
        h = df[df['heuristic'] == heuristic]
        print(f"\n{heuristic.upper()}:")
        print(f"  Mean Backtracks: {h['backtracks'].mean():.2f}  (σ={h['backtracks'].std():.2f})")
        print(f"  Median Backtracks: {h['backtracks'].median():.0f}")
        print(f"  Mean Time: {h['time_seconds'].mean():.6f}s")


def _run_statistics(df):
    print("\n" + "=" * 60)
    print("STATISTICAL TESTS (Mann-Whitney U, two-sided)")
    print("=" * 60)

    seq = df[df['heuristic'] == 'sequential']['backtracks']
    rnd = df[df['heuristic'] == 'random']['backtracks']
    mrv = df[df['heuristic'] == 'mrv']['backtracks']

    pairs = [
        ('Sequential vs Random', seq, rnd),
        ('Sequential vs MRV',    seq, mrv),
        ('Random vs MRV',        rnd, mrv),
    ]
    for label, a, b in pairs:
        u_stat, p_val = stats.mannwhitneyu(a, b, alternative='two-sided')
        sig = "***" if p_val < 0.001 else ("**" if p_val < 0.01 else ("*" if p_val < 0.05 else "ns"))
        print(f"  {label:30s}  U={u_stat:.0f}  p={p_val:.2e}  {sig}")


def _generate_figures(df, num_puzzles):
    heuristics = ['sequential', 'random', 'mrv']
    colours = {'sequential': '#4878CF', 'random': '#D65F5F', 'mrv': '#6ACC65'}

    # fig1 — mean backtracks bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    means = [df[df['heuristic'] == h]['backtracks'].mean() for h in heuristics]
    bars = ax.bar(heuristics, means, color=[colours[h] for h in heuristics])
    ax.bar_label(bars, fmt='%.1f', padding=3)
    ax.set_ylabel('Mean Backtracks')
    ax.set_title(f'Mean Backtracks per Heuristic (n={num_puzzles})')
    ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig('results/fig1_backtracks_comparison.png', dpi=150)
    plt.close()

    # fig2 — mean time bar chart
    fig, ax = plt.subplots(figsize=(6, 4))
    times = [df[df['heuristic'] == h]['time_seconds'].mean() for h in heuristics]
    bars = ax.bar(heuristics, times, color=[colours[h] for h in heuristics])
    ax.bar_label(bars, fmt='%.4f', padding=3)
    ax.set_ylabel('Mean Solve Time (s)')
    ax.set_title(f'Mean Solve Time per Heuristic (n={num_puzzles})')
    plt.tight_layout()
    plt.savefig('results/fig2_time_comparison.png', dpi=150)
    plt.close()

    # fig3 — backtrack distributions (sequential and random only; MRV all-zero)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, h in zip(axes, ['sequential', 'random']):
        data = df[df['heuristic'] == h]['backtracks']
        ax.hist(data, bins=30, color=colours[h], edgecolor='white')
        ax.set_title(f'{h.capitalize()} (mean={data.mean():.0f}, median={data.median():.0f})')
        ax.set_xlabel('Backtracks')
        ax.set_ylabel('Frequency')
    plt.suptitle(f'Backtrack Distributions (n={num_puzzles})')
    plt.tight_layout()
    plt.savefig('results/fig3_distributions.png', dpi=150)
    plt.close()

    # fig4 — per-puzzle backtracks line plot
    fig, ax = plt.subplots(figsize=(10, 4))
    for h in ['sequential', 'random']:
        subset = df[df['heuristic'] == h].sort_values('puzzle_id')
        ax.plot(subset['puzzle_id'], subset['backtracks'], alpha=0.7,
                label=h.capitalize(), color=colours[h])
    ax.set_xlabel('Puzzle Index')
    ax.set_ylabel('Backtracks')
    ax.set_title(f'Backtracks per Puzzle (n={num_puzzles})')
    ax.legend()
    plt.tight_layout()
    plt.savefig('results/fig4_per_puzzle.png', dpi=150)
    plt.close()

    # fig6 — difficulty correlation: empty cells vs sequential backtracks
    seq_df = df[df['heuristic'] == 'sequential'].copy()
    r, p = stats.pearsonr(seq_df['empty_cells'], seq_df['backtracks'])
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(seq_df['empty_cells'], seq_df['backtracks'],
               alpha=0.5, color=colours['sequential'], edgecolors='none', s=20)
    m, b = np.polyfit(seq_df['empty_cells'], seq_df['backtracks'], 1)
    xs = np.linspace(seq_df['empty_cells'].min(), seq_df['empty_cells'].max(), 100)
    ax.plot(xs, m * xs + b, color='black', linewidth=1.5, linestyle='--',
            label=f'r={r:.2f}, p={p:.2e}')
    ax.set_xlabel('Empty Cells (puzzle difficulty proxy)')
    ax.set_ylabel('Backtracks (Sequential)')
    ax.set_title('Puzzle Difficulty vs Sequential Backtracks')
    ax.legend()
    plt.tight_layout()
    plt.savefig('results/fig6_difficulty_correlation.png', dpi=150)
    plt.close()

    print(f"\nFigures saved to results/ (fig1–fig4, fig6)")
    print(f"Difficulty correlation: r={r:.3f}, p={p:.2e}")


if __name__ == "__main__":
    import sys
    num = 200
    if len(sys.argv) > 1:
        num = int(sys.argv[1])
    run_experiments(num_puzzles=num)
