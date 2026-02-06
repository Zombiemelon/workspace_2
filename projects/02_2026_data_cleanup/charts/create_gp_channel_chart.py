import matplotlib.pyplot as plt
import numpy as np

# Data
months = [
    'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024',
    'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024',
    'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025',
    'Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025'
]

paid_gps = [1, 157, 243, 285, 288, 251, 238, 183, 212, 306, 263, 305,
            221, 634, 904, 644, 549, 351, 73, 359, 430, 372, 432, 429]

organic_gps = [210, 280, 310, 242, 312, 183, 189, 171, 190, 232, 270, 219,
               285, 577, 491, 485, 559, 686, 943, 552, 524, 483, 362, 470]

# Calculate totals and percentages
totals = [p + o for p, o in zip(paid_gps, organic_gps)]
paid_pct = [p / t * 100 for p, t in zip(paid_gps, totals)]
organic_pct = [o / t * 100 for o, t in zip(organic_gps, totals)]

# Create figure with white background
plt.style.use('default')
fig, ax = plt.subplots(figsize=(14, 6), facecolor='white')
ax.set_facecolor('white')

# X positions
x = np.arange(len(months))
width = 0.7

# Create 100% stacked bars
bars_paid = ax.bar(x, paid_pct, width, label='Paid GPs', color='#E57373')  # coral/red
bars_organic = ax.bar(x, organic_pct, width, bottom=paid_pct, label='Organic GPs', color='#26A69A')  # teal/green

# Add percentage labels on each segment
for i, (p_pct, o_pct) in enumerate(zip(paid_pct, organic_pct)):
    # Paid label (bottom segment)
    if p_pct >= 5:  # Only show label if segment is big enough
        ax.text(i, p_pct / 2, f'{p_pct:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='bold', color='white')

    # Organic label (top segment)
    if o_pct >= 5:  # Only show label if segment is big enough
        ax.text(i, p_pct + o_pct / 2, f'{o_pct:.0f}%', ha='center', va='center',
                fontsize=7, fontweight='bold', color='white')

# Add vertical dashed line at May 2025 (index 16)
may_2025_idx = months.index('May 2025')
ax.axvline(x=may_2025_idx - 0.5, color='#333333', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(may_2025_idx - 0.5, 105, 'SEO Started', ha='center', va='bottom',
        fontsize=9, fontweight='bold', color='#333333')

# Add horizontal reference line at 50%
ax.axhline(y=50, color='gray', linestyle='--', linewidth=1, alpha=0.7)

# Add horizontal gridlines at 25%, 50%, 75%
ax.yaxis.grid(True, linestyle='-', alpha=0.3, color='gray')
ax.set_axisbelow(True)
ax.set_yticks([0, 25, 50, 75, 100])

# Configure axes
ax.set_xlabel('Month', fontsize=11, fontweight='bold')
ax.set_ylabel('Percentage', fontsize=11, fontweight='bold')
ax.set_title('GP Channel Split (Jan 2024 - Dec 2025)', fontsize=14, fontweight='bold', pad=20)

# X-axis configuration
ax.set_xticks(x)
ax.set_xticklabels(months, rotation=45, ha='right', fontsize=8)

# Y-axis configuration
ax.set_ylim(0, 110)  # Extra space for annotation
ax.set_yticklabels(['0%', '25%', '50%', '75%', '100%'])

# Legend
ax.legend(loc='upper right', framealpha=0.9, fontsize=10)

# Remove top and right spines for cleaner look
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Tight layout
plt.tight_layout()

# Save the chart
output_path = '/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_channel_split_100pct.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print(f"Chart saved to: {output_path}")
