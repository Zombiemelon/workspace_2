"""
August 2025 Invoice Reconciliation
Compares Xero CSV (Finance source) vs BigQuery invoicer_current.invoices
"""

import pandas as pd
import json
import re
from pathlib import Path

# Paths
CSV_PATH = "/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/exports/august_revenue.csv"
BQ_EXPORT_PATH = "/Users/svetoslavdimitrov/.claude/projects/-Users-svetoslavdimitrov-Documents-workspace-2/6ed6638b-ca20-4cb9-b7db-f87622254a07/tool-results/mcp-BigQuery_Toolbox-execute_sql-1769886327787.txt"
OUTPUT_DIR = "/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/exports"

print("=" * 60)
print("AUGUST 2025 INVOICE RECONCILIATION")
print("=" * 60)

# ============================================================
# 1. LOAD CSV DATA (Xero - Finance Source of Truth)
# ============================================================
print("\n[1] Loading CSV data...")

df_csv = pd.read_csv(CSV_PATH, skiprows=1)  # Skip the header row with "Raw Data Xero"
print(f"    Raw CSV rows: {len(df_csv):,}")

# Identify the invoice reference column and amount column
# Based on earlier inspection: 'Reference' has invoice numbers, 'Credit (AED)' has amounts
df_csv.columns = df_csv.columns.str.strip()

# Find the correct column names
print(f"    Columns: {list(df_csv.columns[:10])}...")  # First 10 columns

# The Reference column contains invoice numbers like "INV-108077"
# Credit (AED) contains the amounts

def clean_amount(val):
    """Convert string amounts with commas to float"""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    # Remove commas and convert
    cleaned = str(val).replace(',', '').strip()
    try:
        return float(cleaned)
    except:
        return 0.0

df_csv['amount_clean'] = df_csv['Credit (AED)'].apply(clean_amount)

# Aggregate by invoice number (Reference column)
csv_by_invoice = df_csv.groupby('Reference').agg({
    'amount_clean': 'sum'
}).reset_index()
csv_by_invoice.columns = ['invoice_number', 'csv_amount']
csv_by_invoice['csv_amount'] = csv_by_invoice['csv_amount'].round(2)

print(f"    Unique invoices in CSV: {len(csv_by_invoice):,}")
print(f"    Total CSV amount: AED {csv_by_invoice['csv_amount'].sum():,.2f}")

# Validate invoice number format
csv_invoice_pattern = csv_by_invoice['invoice_number'].str.match(r'^INV-\d+$', na=False)
print(f"    Invoices matching INV-XXXXX pattern: {csv_invoice_pattern.sum():,} / {len(csv_by_invoice):,}")

# ============================================================
# 2. LOAD BIGQUERY DATA
# ============================================================
print("\n[2] Loading BigQuery data...")

with open(BQ_EXPORT_PATH, 'r') as f:
    bq_raw = json.load(f)

# Parse the JSON result - format is [{"type": "text", "text": "JSON_STRING"}, ...]
# Each element has a nested JSON string in the 'text' field
bq_records = []
for item in bq_raw:
    if isinstance(item, dict) and 'text' in item:
        try:
            record = json.loads(item['text'])
            bq_records.append(record)
        except json.JSONDecodeError:
            pass

df_bq = pd.DataFrame(bq_records)
print(f"    BigQuery rows: {len(df_bq):,}")
print(f"    Columns: {list(df_bq.columns)}")

# Use net_amount (total_amount - tax) for comparison since CSV excludes VAT
df_bq['bq_amount'] = df_bq['net_amount'].astype(float).round(2)

print(f"    Unique invoices in BigQuery: {df_bq['invoice_number'].nunique():,}")
print(f"    Total BigQuery net amount: AED {df_bq['bq_amount'].sum():,.2f}")

# Validate invoice number format in BigQuery
bq_invoice_pattern = df_bq['invoice_number'].str.match(r'^INV-\d+$', na=False)
print(f"    Invoices matching INV-XXXXX pattern: {bq_invoice_pattern.sum():,} / {len(df_bq):,}")

# ============================================================
# 3. RECONCILIATION - FULL OUTER JOIN
# ============================================================
print("\n[3] Performing reconciliation...")

# Prepare BigQuery data (select relevant columns)
bq_for_join = df_bq[['invoice_number', 'bq_amount', 'state', 'start_date', 'end_date']].copy()

# Full outer join
reconciled = pd.merge(
    csv_by_invoice,
    bq_for_join,
    on='invoice_number',
    how='outer',
    indicator=True
)

# Categorize discrepancies
def categorize(row):
    if row['_merge'] == 'left_only':
        return 'IN_CSV_NOT_IN_BQ'
    elif row['_merge'] == 'right_only':
        return 'IN_BQ_NOT_IN_CSV'
    else:
        # Both sources have the invoice - check amounts
        diff = abs(row['csv_amount'] - row['bq_amount'])
        if diff < 0.01:  # Within 1 fils tolerance
            return 'MATCHED'
        else:
            return 'AMOUNT_MISMATCH'

reconciled['category'] = reconciled.apply(categorize, axis=1)
reconciled['amount_diff'] = (reconciled['csv_amount'].fillna(0) - reconciled['bq_amount'].fillna(0)).round(2)

# ============================================================
# 4. SUMMARY OF DISCREPANCIES
# ============================================================
print("\n" + "=" * 60)
print("RECONCILIATION SUMMARY")
print("=" * 60)

summary = reconciled.groupby('category').agg({
    'invoice_number': 'count',
    'csv_amount': 'sum',
    'bq_amount': 'sum',
    'amount_diff': 'sum'
}).round(2)
summary.columns = ['invoice_count', 'csv_total', 'bq_total', 'difference']

print("\n" + summary.to_string())

print("\n" + "-" * 60)
print("TOTALS")
print("-" * 60)
print(f"Total invoices in CSV:      {len(csv_by_invoice):,}")
print(f"Total invoices in BigQuery: {len(df_bq):,}")
print(f"Total CSV amount:           AED {csv_by_invoice['csv_amount'].sum():,.2f}")
print(f"Total BigQuery amount:      AED {df_bq['bq_amount'].sum():,.2f}")
print(f"Overall difference:         AED {csv_by_invoice['csv_amount'].sum() - df_bq['bq_amount'].sum():,.2f}")

# ============================================================
# 5. DETAILED BREAKDOWN BY CATEGORY
# ============================================================

print("\n" + "=" * 60)
print("DETAILED BREAKDOWN")
print("=" * 60)

# A) Invoices in CSV but not in BigQuery
csv_only = reconciled[reconciled['category'] == 'IN_CSV_NOT_IN_BQ']
print(f"\n[A] IN CSV, NOT IN BIGQUERY: {len(csv_only)} invoices, AED {csv_only['csv_amount'].sum():,.2f}")
if len(csv_only) > 0:
    print("    Sample invoices:")
    print(csv_only[['invoice_number', 'csv_amount']].head(10).to_string(index=False))

# B) Invoices in BigQuery but not in CSV
bq_only = reconciled[reconciled['category'] == 'IN_BQ_NOT_IN_CSV']
print(f"\n[B] IN BIGQUERY, NOT IN CSV: {len(bq_only)} invoices, AED {bq_only['bq_amount'].sum():,.2f}")
if len(bq_only) > 0:
    print("    Sample invoices:")
    print(bq_only[['invoice_number', 'bq_amount', 'state']].head(10).to_string(index=False))

# C) Amount mismatches
mismatches = reconciled[reconciled['category'] == 'AMOUNT_MISMATCH'].copy()
mismatches['abs_diff'] = mismatches['amount_diff'].abs()
mismatches = mismatches.sort_values('abs_diff', ascending=False)
print(f"\n[C] AMOUNT MISMATCHES: {len(mismatches)} invoices, net difference AED {mismatches['amount_diff'].sum():,.2f}")
if len(mismatches) > 0:
    print("    Top 10 by absolute difference:")
    print(mismatches[['invoice_number', 'csv_amount', 'bq_amount', 'amount_diff']].head(10).to_string(index=False))

# D) Matched
matched = reconciled[reconciled['category'] == 'MATCHED']
print(f"\n[D] MATCHED: {len(matched)} invoices, AED {matched['csv_amount'].sum():,.2f}")

# ============================================================
# 6. EXPORT DETAILED RESULTS
# ============================================================
output_path = f"{OUTPUT_DIR}/august_reconciliation_results.csv"
reconciled.to_csv(output_path, index=False)
print(f"\n[6] Detailed results exported to: {output_path}")

print("\n" + "=" * 60)
print("RECONCILIATION COMPLETE")
print("=" * 60)
