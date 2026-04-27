import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Set style for publication-quality figures
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'

# Load the data
df = pd.read_csv('results/experiment_results.csv')

# ============= FIGURE 1: Average Backtracks Comparison =============
fig1, ax1 = plt.subplots(figsize=(6, 4))

heuristics = ['sequential', 'random', 'mrv']
colors = ['#3498db', '#e74c3c', '#2ecc71']
x_pos = np.arange(len(heuristics))

means = [df[df['heuristic'] == h]['backtracks'].mean() for h in heuristics]
stds = [df[df['heuristic'] == h]['backtracks'].std() for h in heuristics]

bars = ax1.bar(x_pos, means, yerr=stds, color=colors, 
               capsize=5, alpha=0.8, edgecolor='black', linewidth=1.2)

ax1.set_xlabel('Heuristic', fontweight='bold')
ax1.set_ylabel('Average Number of Backtracks', fontweight='bold')
ax1.set_title('Comparison of Backtracking Performance\nAcross Three Heuristics (n=50)', 
              fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(['Sequential', 'Random', 'MRV'])
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Remove all spines except bottom and left
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Add value labels on bars
for i, (bar, mean) in enumerate(zip(bars, means)):
    height = bar.get_height()
    ax1.text(i, height,
             f'{mean:.1f}',
             ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('results/fig1_backtracks_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/fig1_backtracks_comparison.png")
plt.close()

# ============= FIGURE 2: Average Time Comparison =============
fig2, ax2 = plt.subplots(figsize=(6, 4))

means_time = [df[df['heuristic'] == h]['time_seconds'].mean() for h in heuristics]
stds_time = [df[df['heuristic'] == h]['time_seconds'].std() for h in heuristics]

bars = ax2.bar(x_pos, means_time, yerr=stds_time, color=colors,
               capsize=5, alpha=0.8, edgecolor='black', linewidth=1.2)

ax2.set_xlabel('Heuristic', fontweight='bold')
ax2.set_ylabel('Average Time (seconds)', fontweight='bold')
ax2.set_title('Comparison of Solving Time\nAcross Three Heuristics (n=50)', 
              fontweight='bold', pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(['Sequential', 'Random', 'MRV'])
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# Remove all spines except bottom and left
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Add value labels on bars
for i, (bar, mean) in enumerate(zip(bars, means_time)):
    height = bar.get_height()
    ax2.text(i, height,
             f'{mean:.4f}s',
             ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig('results/fig2_time_comparison.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/fig2_time_comparison.png")
plt.close()

# ============= FIGURE 3: Distribution Boxplot (LOG SCALE) =============
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(10, 4))

# Backtracks boxplot with LOG SCALE
data_backtracks = [df[df['heuristic'] == h]['backtracks'].values for h in heuristics]
bp1 = ax3a.boxplot(data_backtracks, tick_labels=['Sequential', 'Random', 'MRV'],
                    patch_artist=True, notch=True, showfliers=False)

for patch, color in zip(bp1['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax3a.set_ylabel('Number of Backtracks (log scale)', fontweight='bold')
ax3a.set_title('Distribution of Backtracks', fontweight='bold')
ax3a.set_yscale('log')
ax3a.grid(axis='y', alpha=0.3, linestyle='--', which='both')
ax3a.set_xlabel('Heuristic', fontweight='bold')

# Time boxplot with LOG SCALE
data_time = [df[df['heuristic'] == h]['time_seconds'].values for h in heuristics]
bp2 = ax3b.boxplot(data_time, tick_labels=['Sequential', 'Random', 'MRV'],
                    patch_artist=True, notch=True, showfliers=False)

for patch, color in zip(bp2['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax3b.set_ylabel('Time (seconds, log scale)', fontweight='bold')
ax3b.set_title('Distribution of Solving Time', fontweight='bold')
ax3b.set_yscale('log')
ax3b.grid(axis='y', alpha=0.3, linestyle='--', which='both')
ax3b.set_xlabel('Heuristic', fontweight='bold')

plt.tight_layout()
plt.savefig('results/fig3_distributions.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/fig3_distributions.png")
plt.close()

# ============= FIGURE 4: Per-Puzzle Performance =============
fig4, ax4 = plt.subplots(figsize=(8, 5))

for h, color in zip(heuristics, colors):
    data = df[df['heuristic'] == h].sort_values('puzzle_id')
    ax4.plot(data['puzzle_id'], data['backtracks'], 
             marker='o', label=h.capitalize(), color=color, 
             alpha=0.7, markersize=4)

ax4.set_xlabel('Puzzle ID', fontweight='bold')
ax4.set_ylabel('Number of Backtracks', fontweight='bold')
ax4.set_title('Backtracking Performance Across 50 Puzzles', fontweight='bold', pad=15)
ax4.legend(loc='upper right', framealpha=0.9)
ax4.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('results/fig4_per_puzzle.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/fig4_per_puzzle.png")
plt.close()

# ============= FIGURE 5: Summary Table Figure =============
fig5, ax5 = plt.subplots(figsize=(9, 3.5))
ax5.axis('tight')
ax5.axis('off')

# Create summary table
table_data = []
for h in heuristics:
    data = df[df['heuristic'] == h]
    table_data.append([
        h.capitalize(),
        f"{data['backtracks'].mean():.2f}",
        f"{data['backtracks'].std():.2f}",
        f"{data['time_seconds'].mean():.6f}",
        f"{data['time_seconds'].std():.6f}",
        f"{data['backtracks'].min():.0f}",
        f"{data['backtracks'].max():.0f}"
    ])

table = ax5.table(cellText=table_data,
                  colLabels=['Heuristic', 'Mean\nBacktracks', 'Std\nBacktracks', 
                            'Mean\nTime (s)', 'Std\nTime (s)', 'Min\nBacktracks', 'Max\nBacktracks'],
                  cellLoc='center',
                  loc='center',
                  colWidths=[0.14, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12])

table.auto_set_font_size(False)
table.set_fontsize(9)
table.scale(1, 2.5)

# Color the header
for i in range(7):
    table[(0, i)].set_facecolor('#3498db')
    table[(0, i)].set_text_props(weight='bold', color='white')

# Color rows
for i in range(1, 4):
    for j in range(7):
        table[(i, j)].set_facecolor(['#ecf0f1', '#d5dbdb', '#c0e6ba'][i-1])

plt.title('Summary Statistics: Backtracking Performance (n=50 puzzles)', 
          fontweight='bold', pad=20, fontsize=12)

plt.savefig('results/fig5_summary_table.png', dpi=300, bbox_inches='tight')
print("✓ Saved: results/fig5_summary_table.png")
plt.close()

print("\n" + "="*60)
print("All figures saved successfully!")
print("="*60)