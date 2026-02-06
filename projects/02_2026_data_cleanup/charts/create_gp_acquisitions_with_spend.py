import matplotlib.pyplot as plt
import numpy as np

# GP Data
quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025']
paid_gps = [401, 824, 633, 874, 1759, 1544, 862, 1233]
organic_gps = [800, 737, 550, 721, 1353, 1730, 2019, 1315]

# Marketing Spend Data (from BigQuery)
spend_aed = [40494, 65457, 46937, 57771, 55525, 61577, 70351, 90307]

# Calculate totals
totals = [p + o for p, o in zip(paid_gps, organic_gps)]

# CAC Data (calculated: Spend / GPs)
paid_cac = [101, 79, 74, 66, 32, 40, 82, 73]  # Spend / Paid GPs
blended_cac = [34, 42, 40, 36, 18, 19, 24, 35]  # Spend / Total GPs

# Create figure with white background - larger size for extra legend items
fig, ax1 = plt.subplots(figsize=(16, 8), facecolor='white')
ax1.set_facecolor('white')

# Bar positions and width
x = np.arange(len(quarters))
width = 0.6

# Colors
paid_color = '#E07A73'  # Coral
organic_color = '#3CB4AC'  # Teal
paid_cac_color = '#8B0000'  # Dark red/maroon
blended_cac_color = '#00008B'  # Dark blue

# Create stacked bar chart
bars_paid = ax1.bar(x, paid_gps, width, label='Paid GPs', color=paid_color, edgecolor='white', linewidth=0.5)
bars_organic = ax1.bar(x, organic_gps, width, bottom=paid_gps, label='Organic GPs', color=organic_color, edgecolor='white', linewidth=0.5)

# Add total labels on top of each bar
for i, total in enumerate(totals):
    ax1.text(i, total + 80, f'{total:,}', ha='center', va='bottom',
             fontsize=11, fontweight='bold', color='#333333')

# Configure left y-axis
ax1.set_ylabel('Number of GPs', fontsize=12, fontweight='bold')
ax1.set_ylim(0, max(totals) * 1.2)  # Add space for labels
ax1.set_xlabel('Quarter', fontsize=12)
ax1.set_xticks(x)
ax1.set_xticklabels(quarters, fontsize=11)

# Add gridlines for left axis
ax1.yaxis.grid(True, linestyle='-', alpha=0.3, color='gray', zorder=0)
ax1.set_axisbelow(True)

# Create secondary y-axis for marketing spend
ax2 = ax1.twinx()

# Plot marketing spend as a BLACK line with markers
line_spend = ax2.plot(x, spend_aed, color='black', linewidth=2.5, marker='o', markersize=8,
                      label='Marketing Spend (AED)', zorder=5)

# Add spend value labels on the line points
for i, spend in enumerate(spend_aed):
    ax2.text(i, spend + 3000, f'{spend:,.0f}', ha='center', va='bottom',
             fontsize=9, fontweight='bold', color='black')

# Configure right y-axis for spend
ax2.set_ylabel('Marketing Spend (AED)', fontsize=12, fontweight='bold')
ax2.set_ylim(0, max(spend_aed) * 1.35)  # More space for CAC labels

# Create third y-axis for CAC (offset to the right)
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 70))  # Offset the spine

# Plot CAC lines with dashed style
line_paid_cac = ax3.plot(x, paid_cac, color=paid_cac_color, linewidth=2.5, linestyle='--',
                          marker='o', markersize=8, label='Paid CAC (AED)', zorder=6)
line_blended_cac = ax3.plot(x, blended_cac, color=blended_cac_color, linewidth=2.5, linestyle='--',
                             marker='s', markersize=8, label='Blended CAC (AED)', zorder=6)

# Add CAC value labels on the line points
for i, cac in enumerate(paid_cac):
    ax3.text(i, cac + 5, f'{cac} AED', ha='center', va='bottom',
             fontsize=9, fontweight='bold', color=paid_cac_color)

for i, cac in enumerate(blended_cac):
    ax3.text(i, cac - 8, f'{cac} AED', ha='center', va='top',
             fontsize=9, fontweight='bold', color=blended_cac_color)

# Configure third y-axis for CAC
ax3.set_ylabel('CAC (AED)', fontsize=12, fontweight='bold', color='#333333')
ax3.set_ylim(0, max(paid_cac) * 1.4)  # Add space for labels
ax3.tick_params(axis='y', labelcolor='#333333')

# Add vertical dashed line between Q1 2025 and Q2 2025 (index 4.5)
ax1.axvline(x=4.5, color='#555555', linestyle='--', linewidth=2, zorder=3)
ax1.text(4.5, max(totals) * 1.15, 'SEO Started\n(May 2025)', ha='center', va='bottom', fontsize=10,
         color='#555555', fontweight='bold')

# Title
ax1.set_title('GP Acquisitions, Marketing Spend & CAC by Quarter (2024 - 2025)',
              fontsize=16, fontweight='bold', pad=20)

# Combined legend from all axes
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines3, labels3 = ax3.get_legend_handles_labels()
ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3,
           loc='upper left', framealpha=0.95, fontsize=10)

# Remove top spine for cleaner look
ax1.spines['top'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax3.spines['top'].set_visible(False)

# Tight layout
plt.tight_layout()

# Save
output_path = '/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_acquisitions_quarterly.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print(f"Chart saved to: {output_path}")
