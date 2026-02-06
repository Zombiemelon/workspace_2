import matplotlib.pyplot as plt
import numpy as np

# Data
quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
paid_gps = [401, 824, 633, 874, 1759, 1544, 862, 1233]
organic_gps = [800, 737, 550, 721, 1353, 1730, 2019, 1315]

# Calculate totals and percentages
totals = [p + o for p, o in zip(paid_gps, organic_gps)]
paid_pct = [p / t * 100 for p, t in zip(paid_gps, totals)]
organic_pct = [o / t * 100 for o, t in zip(organic_gps, totals)]

# Create figure with white background
fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
ax.set_facecolor('white')

# Bar positions and width
x = np.arange(len(quarters))
width = 0.65  # Wider bars for 8 quarters

# Colors
paid_color = '#E57373'  # Coral/red
organic_color = '#4DB6AC'  # Teal/green

# Create 100% stacked bars
bars_paid = ax.bar(x, paid_pct, width, label='Paid', color=paid_color, edgecolor='white', linewidth=0.5)
bars_organic = ax.bar(x, organic_pct, width, bottom=paid_pct, label='Organic', color=organic_color, edgecolor='white', linewidth=0.5)

# Add percentage labels on each segment
for i, (p_pct, o_pct) in enumerate(zip(paid_pct, organic_pct)):
    # Paid label (positioned in middle of paid segment)
    ax.text(i, p_pct / 2, f'{p_pct:.0f}%', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    # Organic label (positioned in middle of organic segment)
    ax.text(i, p_pct + o_pct / 2, f'{o_pct:.0f}%', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')

# Add vertical dashed line between Q1 2025 and Q2 2025 (between index 4 and 5)
# Position it at 4.5 (middle between Q1 2025 and Q2 2025)
ax.axvline(x=4.5, color='#555555', linestyle='--', linewidth=1.5, zorder=5)
ax.text(4.5, 105, 'SEO Started\n(May 2025)', ha='center', va='bottom', fontsize=9,
        color='#555555', fontweight='bold')

# Add horizontal reference line at 50%
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.7, zorder=1)

# Horizontal gridlines at 25%, 50%, 75%
ax.yaxis.set_major_locator(plt.MultipleLocator(25))
ax.yaxis.grid(True, linestyle='-', alpha=0.3, color='gray', zorder=0)
ax.set_axisbelow(True)

# Set axis properties
ax.set_xlim(-0.5, len(quarters) - 0.5)
ax.set_ylim(0, 115)  # Extra space for annotation
ax.set_xticks(x)
ax.set_xticklabels(quarters, fontsize=10)
ax.set_ylabel('Percentage (%)', fontsize=11)
ax.set_xlabel('Quarter', fontsize=11)

# Title
ax.set_title('GP Channel Split by Quarter (2024 - 2025)', fontsize=14, fontweight='bold', pad=15)

# Legend
ax.legend(loc='upper right', framealpha=0.9, fontsize=10)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout
plt.tight_layout()

# Save
output_path = '/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_channel_split_quarterly.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print(f"Chart saved to: {output_path}")
