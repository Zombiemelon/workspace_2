#!/usr/bin/env python3
"""
Create GP acquisition charts using BUSINESS ACCOUNTS ONLY data.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# Monthly Data (Jan 2024 - Dec 2025)
monthly_data = {
    'month': ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06',
              '2024-07', '2024-08', '2024-09', '2024-10', '2024-11', '2024-12',
              '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06',
              '2025-07', '2025-08', '2025-09', '2025-10', '2025-11', '2025-12'],
    'total_gps': [211, 430, 543, 521, 599, 434, 427, 354, 402, 538, 533, 524,
                  482, 474, 539, 482, 525, 467, 465, 412, 431, 456, 406, 414],
    'paid_gps': [1, 156, 243, 285, 288, 251, 238, 183, 212, 306, 263, 305,
                 214, 204, 308, 242, 198, 122, 30, 146, 179, 167, 220, 171],
    'organic_gps': [210, 274, 300, 236, 311, 183, 189, 171, 190, 232, 270, 219,
                    268, 270, 231, 240, 327, 345, 435, 266, 252, 289, 186, 243]
}

# Quarterly Data
quarterly_data = {
    'quarter': ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025', 'Q2 2025', 'Q3 2025', 'Q4 2025'],
    'paid_gps': [400, 824, 633, 874, 726, 562, 355, 558],
    'organic_gps': [784, 730, 550, 721, 769, 912, 953, 718],
    'total': [1184, 1554, 1183, 1595, 1495, 1474, 1308, 1276],
    'spend': [40494, 65457, 46937, 57771, 55525, 61577, 70351, 90307],
    'paid_cac': [101, 79, 74, 66, 76, 110, 198, 162],
    'blended_cac': [34, 42, 40, 36, 37, 42, 54, 71]
}

# Colors
CORAL = '#E07A73'
TEAL = '#3CB4AC'
MAROON = '#8B0000'
DARK_BLUE = '#00008B'
BLACK = '#000000'

# Chart 1: GP Acquisitions Quarterly with Spend and CAC
def create_quarterly_acquisitions_chart():
    fig, ax1 = plt.subplots(figsize=(16, 8))

    quarters = quarterly_data['quarter']
    paid = quarterly_data['paid_gps']
    organic = quarterly_data['organic_gps']
    totals = quarterly_data['total']
    spend = quarterly_data['spend']
    paid_cac = quarterly_data['paid_cac']
    blended_cac = quarterly_data['blended_cac']

    x = np.arange(len(quarters))
    width = 0.6

    # Stacked bars
    bars1 = ax1.bar(x, paid, width, label='Paid GPs', color=CORAL)
    bars2 = ax1.bar(x, organic, width, bottom=paid, label='Organic GPs', color=TEAL)

    # Add total labels on top of bars
    for i, (p, o, t) in enumerate(zip(paid, organic, totals)):
        ax1.text(i, t + 30, f'{t:,}', ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax1.set_ylabel('GP Acquisitions', fontsize=12)
    ax1.set_xlabel('Quarter', fontsize=12)
    ax1.set_xticks(x)
    ax1.set_xticklabels(quarters, fontsize=10)
    ax1.set_ylim(0, max(totals) * 1.15)

    # Secondary axis for spend
    ax2 = ax1.twinx()
    spend_line = ax2.plot(x, spend, color=BLACK, marker='o', linewidth=2, label='Marketing Spend (AED)')
    ax2.set_ylabel('Marketing Spend (AED)', fontsize=12)
    ax2.set_ylim(0, max(spend) * 1.3)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v/1000:.0f}K'))

    # Third axis for CAC
    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 70))
    paid_cac_line = ax3.plot(x, paid_cac, color=MAROON, linestyle='--', marker='s', linewidth=2, label='Paid CAC')
    blended_cac_line = ax3.plot(x, blended_cac, color=DARK_BLUE, linestyle='--', marker='^', linewidth=2, label='Blended CAC')
    ax3.set_ylabel('CAC (AED)', fontsize=12)
    ax3.set_ylim(0, max(paid_cac) * 1.3)

    # Add CAC value labels
    for i, (pc, bc) in enumerate(zip(paid_cac, blended_cac)):
        ax3.annotate(f'{pc} AED', (i, pc), textcoords="offset points", xytext=(0, 8),
                     ha='center', fontsize=8, color=MAROON)
        ax3.annotate(f'{bc} AED', (i, bc), textcoords="offset points", xytext=(0, -12),
                     ha='center', fontsize=8, color=DARK_BLUE)

    # SEO Started marker - between Q1 2025 (index 4) and Q2 2025 (index 5)
    seo_x = 4.5
    ax1.axvline(x=seo_x, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax1.text(seo_x, max(totals) * 1.08, 'SEO Started\n(May 2025)', ha='center', va='bottom',
             fontsize=9, style='italic', color='gray')

    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax1.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper left', fontsize=10)

    plt.title('GP Acquisitions, Marketing Spend & CAC by Quarter (2024-2025) — Business Accounts Only',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_acquisitions_quarterly.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: gp_acquisitions_quarterly.png")

# Chart 2: GP Channel Split 100% (Monthly)
def create_monthly_channel_split_chart():
    fig, ax = plt.subplots(figsize=(14, 7))

    months = monthly_data['month']
    paid = np.array(monthly_data['paid_gps'])
    organic = np.array(monthly_data['organic_gps'])
    total = paid + organic

    paid_pct = (paid / total) * 100
    organic_pct = (organic / total) * 100

    x = np.arange(len(months))
    width = 0.8

    bars1 = ax.bar(x, paid_pct, width, label='Paid %', color=CORAL)
    bars2 = ax.bar(x, organic_pct, width, bottom=paid_pct, label='Organic %', color=TEAL)

    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels([m[2:] for m in months], fontsize=8, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())

    # SEO Started marker at May 2025 (index 16)
    seo_x = 16
    ax.axvline(x=seo_x, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(seo_x, 102, 'SEO Started\n(May 2025)', ha='center', va='bottom',
            fontsize=9, style='italic', color='gray')

    ax.legend(loc='upper right', fontsize=10)
    plt.title('GP Channel Split by Month (2024-2025) — Business Accounts Only',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_channel_split_100pct.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: gp_channel_split_100pct.png")

# Chart 3: GP Channel Split 100% (Quarterly)
def create_quarterly_channel_split_chart():
    fig, ax = plt.subplots(figsize=(12, 6))

    quarters = quarterly_data['quarter']
    paid = np.array(quarterly_data['paid_gps'])
    organic = np.array(quarterly_data['organic_gps'])
    total = paid + organic

    paid_pct = (paid / total) * 100
    organic_pct = (organic / total) * 100

    x = np.arange(len(quarters))
    width = 0.6

    bars1 = ax.bar(x, paid_pct, width, label='Paid %', color=CORAL)
    bars2 = ax.bar(x, organic_pct, width, bottom=paid_pct, label='Organic %', color=TEAL)

    # Add percentage labels on bars
    for i, (pp, op) in enumerate(zip(paid_pct, organic_pct)):
        ax.text(i, pp / 2, f'{pp:.0f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')
        ax.text(i, pp + op / 2, f'{op:.0f}%', ha='center', va='center', fontsize=9, color='white', fontweight='bold')

    ax.set_ylabel('Percentage (%)', fontsize=12)
    ax.set_xlabel('Quarter', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(quarters, fontsize=10)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())

    # SEO Started marker between Q1 2025 (index 4) and Q2 2025 (index 5)
    seo_x = 4.5
    ax.axvline(x=seo_x, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(seo_x, 102, 'SEO Started\n(May 2025)', ha='center', va='bottom',
            fontsize=9, style='italic', color='gray')

    ax.legend(loc='upper right', fontsize=10)
    plt.title('GP Channel Split by Quarter (2024-2025) — Business Accounts Only',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_channel_split_quarterly.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: gp_channel_split_quarterly.png")

# Chart 4: GP Acquisitions by Channel (Stacked Area)
def create_channel_area_chart():
    fig, ax = plt.subplots(figsize=(14, 7))

    months = monthly_data['month']
    paid = monthly_data['paid_gps']
    organic = monthly_data['organic_gps']

    x = np.arange(len(months))

    ax.fill_between(x, 0, paid, label='Paid GPs', color=CORAL, alpha=0.8)
    ax.fill_between(x, paid, np.array(paid) + np.array(organic), label='Organic GPs', color=TEAL, alpha=0.8)

    ax.set_ylabel('GP Acquisitions', fontsize=12)
    ax.set_xlabel('Month', fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels([m[2:] for m in months], fontsize=8, rotation=45, ha='right')
    ax.set_xlim(0, len(months) - 1)

    # SEO Started marker at May 2025 (index 16)
    seo_x = 16
    ax.axvline(x=seo_x, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
    ax.text(seo_x, max(np.array(paid) + np.array(organic)) * 0.95, 'SEO Started', ha='center', va='top',
            fontsize=9, style='italic', color='gray', rotation=90)

    ax.legend(loc='upper left', fontsize=10)
    plt.title('GP Acquisitions by Channel (2024-2025) — Business Accounts Only',
              fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/analytics_findings/charts/gp_acquisitions_by_channel.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Created: gp_acquisitions_by_channel.png")

if __name__ == '__main__':
    create_quarterly_acquisitions_chart()
    create_monthly_channel_split_chart()
    create_quarterly_channel_split_chart()
    create_channel_area_chart()
    print("\nAll charts created successfully!")
