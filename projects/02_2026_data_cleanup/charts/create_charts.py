import matplotlib.pyplot as plt
import numpy as np

# Set clean, professional style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# =============================================================================
# CHART 1: GP Acquisitions by Channel (Jan 2024 - Dec 2025) - Stacked Area
# =============================================================================

months_gp = [
    'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'May 2024', 'Jun 2024',
    'Jul 2024', 'Aug 2024', 'Sep 2024', 'Oct 2024', 'Nov 2024', 'Dec 2024',
    'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'May 2025', 'Jun 2025',
    'Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025'
]

paid_gps = [1, 157, 243, 285, 288, 251, 238, 183, 212, 306, 263, 305,
            221, 634, 904, 644, 549, 351, 73, 359, 430, 372, 432, 429]

organic_gps = [210, 280, 310, 242, 312, 183, 189, 171, 190, 232, 270, 219,
               285, 577, 491, 485, 559, 686, 943, 552, 524, 483, 362, 470]

fig1, ax1 = plt.subplots(figsize=(14, 7))

x = np.arange(len(months_gp))

# Create stacked area chart
ax1.fill_between(x, 0, paid_gps, alpha=0.8, color='coral', label='Paid GPs')
ax1.fill_between(x, paid_gps, np.array(paid_gps) + np.array(organic_gps),
                  alpha=0.8, color='teal', label='Organic GPs')

# Add vertical dashed line at May 2025 (index 16)
may_2025_idx = months_gp.index('May 2025')
ax1.axvline(x=may_2025_idx, color='darkblue', linestyle='--', linewidth=2, alpha=0.7)
ax1.text(may_2025_idx + 0.2, max(np.array(paid_gps) + np.array(organic_gps)) * 0.9,
         'SEO Started', fontsize=10, color='darkblue', fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(months_gp, rotation=45, ha='right')
ax1.set_xlabel('Month')
ax1.set_ylabel('Number of Grandparents')
ax1.set_title('Grandparent Acquisitions by Channel (Jan 2024 - Dec 2025)', fontweight='bold', pad=15)
ax1.legend(loc='upper left')
ax1.set_xlim(0, len(months_gp) - 1)
ax1.set_ylim(0, None)

plt.tight_layout()
plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_acquisitions_by_channel.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("Chart 1 saved: gp_acquisitions_by_channel.png")

# =============================================================================
# CHART 2: Website Visitors & Spend (H2 2025) - Stacked Bar + Line
# =============================================================================

months_h2 = ['Jul 2025', 'Aug 2025', 'Sep 2025', 'Oct 2025', 'Nov 2025', 'Dec 2025']
paid_visitors = [6661, 6515, 7082, 8220, 7540, 7345]
organic_visitors = [6762, 7272, 7316, 8499, 8833, 8344]
spend_aed = [18772, 19733, 31846, 29519, 28202, 32586]

fig2, ax2 = plt.subplots(figsize=(12, 7))

x2 = np.arange(len(months_h2))
width = 0.6

# Stacked bar chart
bars_paid = ax2.bar(x2, paid_visitors, width, color='indianred', label='Paid Visitors', alpha=0.85)
bars_organic = ax2.bar(x2, organic_visitors, width, bottom=paid_visitors,
                        color='seagreen', label='Organic Visitors', alpha=0.85)

ax2.set_xlabel('Month')
ax2.set_ylabel('Number of Visitors')
ax2.set_xticks(x2)
ax2.set_xticklabels(months_h2, rotation=45, ha='right')

# Secondary y-axis for spend
ax2_right = ax2.twinx()
ax2_right.plot(x2, spend_aed, color='royalblue', linestyle='--', linewidth=2.5,
               marker='o', markersize=8, label='Spend (AED)')
ax2_right.set_ylabel('Spend (AED)', color='royalblue')
ax2_right.tick_params(axis='y', labelcolor='royalblue')

# Add spend values on the line
for i, val in enumerate(spend_aed):
    ax2_right.annotate(f'{val:,}', (x2[i], val), textcoords="offset points",
                       xytext=(0, 10), ha='center', fontsize=9, color='royalblue')

ax2.set_title('Website Visitors & Marketing Spend (H2 2025)', fontweight='bold', pad=15)

# Combine legends
lines1, labels1 = ax2.get_legend_handles_labels()
lines2, labels2 = ax2_right.get_legend_handles_labels()
ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.tight_layout()
plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/visitors_spend_h2_2025.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("Chart 2 saved: visitors_spend_h2_2025.png")

# =============================================================================
# CHART 3: Visitor Channel Split - 100% Stacked Bar (H2 2025)
# =============================================================================

fig3, ax3 = plt.subplots(figsize=(12, 7))

# Calculate percentages
total_visitors = [p + o for p, o in zip(paid_visitors, organic_visitors)]
paid_pct = [p / t * 100 for p, t in zip(paid_visitors, total_visitors)]
organic_pct = [o / t * 100 for o, t in zip(organic_visitors, total_visitors)]

x3 = np.arange(len(months_h2))
width = 0.6

# 100% stacked bar chart
bars_paid_pct = ax3.bar(x3, paid_pct, width, color='indianred', label='Paid Visitors', alpha=0.85)
bars_organic_pct = ax3.bar(x3, organic_pct, width, bottom=paid_pct,
                            color='seagreen', label='Organic Visitors', alpha=0.85)

# Add percentage labels on each segment
for i in range(len(months_h2)):
    # Paid percentage label (center of paid bar)
    ax3.text(x3[i], paid_pct[i] / 2, f'{paid_pct[i]:.1f}%',
             ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    # Organic percentage label (center of organic bar)
    ax3.text(x3[i], paid_pct[i] + organic_pct[i] / 2, f'{organic_pct[i]:.1f}%',
             ha='center', va='center', fontsize=10, fontweight='bold', color='white')

ax3.set_xlabel('Month')
ax3.set_ylabel('Percentage (%)')
ax3.set_xticks(x3)
ax3.set_xticklabels(months_h2, rotation=45, ha='right')
ax3.set_ylim(0, 100)

# Add horizontal gridlines at 25%, 50%, 75%
ax3.set_yticks([0, 25, 50, 75, 100])
ax3.yaxis.grid(True, linestyle='-', alpha=0.7)
ax3.set_axisbelow(True)

ax3.set_title('Visitor Channel Split (H2 2025)', fontweight='bold', pad=15)
ax3.legend(loc='upper right')

plt.tight_layout()
plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/visitor_channel_split_100pct.png',
            dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()

print("Chart 3 saved: visitor_channel_split_100pct.png")

print("\nAll charts created successfully!")
