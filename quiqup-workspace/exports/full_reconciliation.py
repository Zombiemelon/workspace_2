"""
Full 2025 Invoice Reconciliation (Jan-Aug)
Compares Xero CSV (Finance source) vs BigQuery invoicer_current.invoices
Outputs:
1. missing_in_bigquery.csv - Invoices in CSV but not in BigQuery
2. missing_in_csv.csv - Invoices in BigQuery but not in CSV
3. value_discrepancies.csv - Invoices with amount differences
"""

import pandas as pd
import json
from pathlib import Path
from datetime import datetime

# Paths
CSV_PATH = "/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/exports/2022_monthly revenue.csv"
BQ_EXPORT_PATH = "/Users/svetoslavdimitrov/.claude/projects/-Users-svetoslavdimitrov-Documents-workspace-2/c826e7e4-cd1b-4288-859b-da56e918f347/tool-results/mcp-BigQuery_Toolbox-execute_sql-1769890319630.txt"
OUTPUT_DIR = "/Users/svetoslavdimitrov/Documents/workspace_2/quiqup-workspace/exports"

print("=" * 70)
print("FULL 2025 INVOICE RECONCILIATION (JAN-AUG)")
print("=" * 70)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================
# 1. LOAD CSV DATA (Xero - Finance Source of Truth)
# ============================================================
print("\n[1] Loading CSV data (Xero)...")

df_csv = pd.read_csv(CSV_PATH, skiprows=1)  # Skip the header row with "Raw Data Xero"
print(f"    Raw CSV rows: {len(df_csv):,}")

# Clean column names
df_csv.columns = df_csv.columns.str.strip()

def clean_amount(val):
    """Convert string amounts with commas to float"""
    if pd.isna(val):
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    cleaned = str(val).replace(',', '').strip()
    try:
        return float(cleaned)
    except:
        return 0.0

df_csv['amount_clean'] = df_csv['Credit (AED)'].apply(clean_amount)

# Extract month from Date column
df_csv['Date'] = pd.to_datetime(df_csv['Date'], format='%d %b %Y', errors='coerce')
df_csv['month'] = df_csv['Date'].dt.month
df_csv['month_name'] = df_csv['Date'].dt.strftime('%b')

# Filter to Jan-Aug 2025 only (months 1-8)
df_csv = df_csv[df_csv['month'].between(1, 8)]
print(f"    CSV rows (Jan-Aug 2025): {len(df_csv):,}")

# Aggregate by invoice number
csv_by_invoice = df_csv.groupby('Reference').agg({
    'amount_clean': 'sum',
    'month': 'first',
    'month_name': 'first',
    'Description': 'first'
}).reset_index()
csv_by_invoice.columns = ['invoice_number', 'csv_amount', 'month', 'month_name', 'description']
csv_by_invoice['csv_amount'] = csv_by_invoice['csv_amount'].round(2)

print(f"    Unique invoices in CSV: {len(csv_by_invoice):,}")
print(f"    Total CSV amount: AED {csv_by_invoice['csv_amount'].sum():,.2f}")

# Show by month
csv_monthly = csv_by_invoice.groupby(['month', 'month_name']).agg({
    'invoice_number': 'count',
    'csv_amount': 'sum'
}).reset_index()
print("\n    Monthly breakdown (CSV):")
for _, row in csv_monthly.iterrows():
    print(f"      {row['month_name']}: {row['invoice_number']:,} invoices, AED {row['csv_amount']:,.2f}")

# ============================================================
# 2. LOAD BIGQUERY DATA
# ============================================================
print("\n[2] Loading BigQuery data...")

with open(BQ_EXPORT_PATH, 'r') as f:
    bq_raw = json.load(f)

# Parse the JSON result - format is [{"type": "text", "text": "JSON_STRING"}, ...]
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

# Convert net_amount to float
df_bq['bq_amount'] = df_bq['net_amount'].astype(float).round(2)

# Extract month from start_date
df_bq['start_date'] = pd.to_datetime(df_bq['start_date'])
df_bq['month'] = df_bq['start_date'].dt.month
df_bq['month_name'] = df_bq['start_date'].dt.strftime('%b')

print(f"    Unique invoices in BigQuery: {df_bq['invoice_number'].nunique():,}")
print(f"    Total BigQuery net amount: AED {df_bq['bq_amount'].sum():,.2f}")

# Show by month
bq_monthly = df_bq.groupby(['month', 'month_name']).agg({
    'invoice_number': 'count',
    'bq_amount': 'sum'
}).reset_index()
print("\n    Monthly breakdown (BigQuery):")
for _, row in bq_monthly.iterrows():
    print(f"      {row['month_name']}: {row['invoice_number']:,} invoices, AED {row['bq_amount']:,.2f}")

# ============================================================
# 3. RECONCILIATION - FULL OUTER JOIN
# ============================================================
print("\n[3] Performing reconciliation...")

# Prepare BigQuery data
bq_for_join = df_bq[['invoice_number', 'bq_amount', 'state', 'start_date', 'month', 'month_name']].copy()
bq_for_join.columns = ['invoice_number', 'bq_amount', 'state', 'start_date', 'bq_month', 'bq_month_name']

# Full outer join
reconciled = pd.merge(
    csv_by_invoice,
    bq_for_join,
    on='invoice_number',
    how='outer',
    indicator=True
)

# ============================================================
# 4. CREATE OUTPUT FILES
# ============================================================
print("\n[4] Creating output files...")

# --- FILE 1: Missing in BigQuery (in CSV but not in BQ) ---
missing_in_bq = reconciled[reconciled['_merge'] == 'left_only'].copy()
missing_in_bq = missing_in_bq[['invoice_number', 'csv_amount', 'month_name', 'description']]
missing_in_bq.columns = ['invoice_number', 'csv_amount_aed', 'month', 'description']
missing_in_bq = missing_in_bq.sort_values(['month', 'invoice_number'])

output_path_1 = f"{OUTPUT_DIR}/missing_in_bigquery.csv"
missing_in_bq.to_csv(output_path_1, index=False)
print(f"\n    [A] MISSING IN BIGQUERY: {len(missing_in_bq)} invoices")
print(f"        Total amount: AED {missing_in_bq['csv_amount_aed'].sum():,.2f}")
print(f"        Saved to: {output_path_1}")

# Show breakdown by month
if len(missing_in_bq) > 0:
    print("        By month:")
    for month in missing_in_bq['month'].unique():
        month_data = missing_in_bq[missing_in_bq['month'] == month]
        print(f"          {month}: {len(month_data)} invoices, AED {month_data['csv_amount_aed'].sum():,.2f}")

# --- FILE 2: Missing in CSV (in BQ but not in CSV) ---
missing_in_csv = reconciled[reconciled['_merge'] == 'right_only'].copy()
missing_in_csv = missing_in_csv[['invoice_number', 'bq_amount', 'bq_month_name', 'state', 'start_date']]
missing_in_csv.columns = ['invoice_number', 'bigquery_amount_aed', 'month', 'state', 'start_date']
missing_in_csv = missing_in_csv.sort_values(['month', 'invoice_number'])

output_path_2 = f"{OUTPUT_DIR}/missing_in_csv.csv"
missing_in_csv.to_csv(output_path_2, index=False)
print(f"\n    [B] MISSING IN CSV: {len(missing_in_csv)} invoices")
print(f"        Total amount: AED {missing_in_csv['bigquery_amount_aed'].sum():,.2f}")
print(f"        Saved to: {output_path_2}")

# Show breakdown by month
if len(missing_in_csv) > 0:
    print("        By month:")
    for month in missing_in_csv['month'].unique():
        month_data = missing_in_csv[missing_in_csv['month'] == month]
        print(f"          {month}: {len(month_data)} invoices, AED {month_data['bigquery_amount_aed'].sum():,.2f}")

# --- FILE 3: Value Discrepancies ---
matched = reconciled[reconciled['_merge'] == 'both'].copy()
matched['difference_aed'] = (matched['bq_amount'] - matched['csv_amount']).round(2)
matched['abs_difference'] = matched['difference_aed'].abs()

# Filter to only those with differences > 0.01 AED (1 fils tolerance)
discrepancies = matched[matched['abs_difference'] > 0.01].copy()
discrepancies = discrepancies[['invoice_number', 'bq_amount', 'csv_amount', 'difference_aed', 'month_name', 'state']]
discrepancies.columns = ['invoice_number', 'bigquery_amount_aed', 'csv_amount_aed', 'difference_aed', 'month', 'state']
discrepancies = discrepancies.sort_values('abs_difference' if 'abs_difference' in discrepancies.columns else 'difference_aed', ascending=False, key=abs)

output_path_3 = f"{OUTPUT_DIR}/value_discrepancies.csv"
discrepancies.to_csv(output_path_3, index=False)
print(f"\n    [C] VALUE DISCREPANCIES: {len(discrepancies)} invoices")
print(f"        Net difference: AED {discrepancies['difference_aed'].sum():,.2f}")
print(f"        Saved to: {output_path_3}")

# Show top 10 largest discrepancies
if len(discrepancies) > 0:
    print("        Top 10 largest discrepancies:")
    top_10 = discrepancies.head(10)
    for _, row in top_10.iterrows():
        print(f"          {row['invoice_number']}: BQ={row['bigquery_amount_aed']:,.2f}, CSV={row['csv_amount_aed']:,.2f}, Diff={row['difference_aed']:+,.2f}")

# ============================================================
# 5. SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("RECONCILIATION SUMMARY")
print("=" * 70)

total_csv_invoices = len(csv_by_invoice)
total_bq_invoices = len(df_bq)
matched_exactly = len(matched) - len(discrepancies)

print(f"\nTotal invoices in CSV (Xero):     {total_csv_invoices:,}")
print(f"Total invoices in BigQuery:       {total_bq_invoices:,}")
print(f"\nMatched exactly:                  {matched_exactly:,} ({matched_exactly/total_csv_invoices*100:.1f}%)")
print(f"Value discrepancies:              {len(discrepancies):,}")
print(f"Missing in BigQuery:              {len(missing_in_bq):,}")
print(f"Missing in CSV:                   {len(missing_in_csv):,}")

print(f"\nTotal CSV amount:                 AED {csv_by_invoice['csv_amount'].sum():,.2f}")
print(f"Total BigQuery amount:            AED {df_bq['bq_amount'].sum():,.2f}")
print(f"Overall difference:               AED {df_bq['bq_amount'].sum() - csv_by_invoice['csv_amount'].sum():+,.2f}")

print("\n" + "=" * 70)
print("OUTPUT FILES CREATED:")
print("=" * 70)
print(f"1. {output_path_1}")
print(f"2. {output_path_2}")
print(f"3. {output_path_3}")

print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 70)
