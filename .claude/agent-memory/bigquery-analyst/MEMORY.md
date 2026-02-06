# BigQuery Analyst Agent Memory

## Key Schema Patterns

### invoicer_current.invoices - Revenue Queries
- **Source of truth** for revenue: `invoicer_current.invoices`
- **Date filter**: Use `start_date` (not `end_date`) for Finance reconciliation
- **States**: `paid`, `overdue` for recognized revenue
- **Net revenue**: `total_amount - COALESCE(tax_amount, 0)`
- **Soft delete filter**: `record_deleted = FALSE`
- **Currency**: All AED (lowercase "aed" in data)

### Account Hierarchy (invoicer_current.accounts)
- Accounts have grandparent > parent > child hierarchy
- `invoice_to_parent` flag routes invoices to parent account
- Invoice `account_id` already reflects routing (joins directly)
- For business group rollup: use `COALESCE(grandparent_account_name, parent_account_name, account_name)`
- For SF name resolution: join `accounts.salesforce_id` to `salesforce_current.accounts.id`
- Some `account_name` values are raw Salesforce IDs -- always LEFT JOIN to SF accounts for display names

### SSUP Catch-All
- "SSUP Grandparent account" is a catch-all for self-signup accounts (~2,700 sub-accounts)
- Represents ~8.5% of 2025 revenue; must be excluded from "top client" rankings
- Filter: `WHERE group_name NOT LIKE '%SSUP%'`

## 2025 Revenue Benchmarks
- Total net revenue (2025, paid+overdue): AED 45,993,284 (n=28,801 invoices, 3,807 billing accounts)
- Top 15 business groups = 49.7% of total revenue
- #1 client: M.H. Alshaya Group = 12.7% of total

## Salesforce Service Offering Field
- Field: `salesforce_current.accounts.Service_Offering_c` (STRING)
- Values: Last Mile (22,819), NULL (9,381), On-demand (3,775), 4 Hours (997), Sameday (518), Fulfillment (517), Fulfillment + Last Mile (41)
- For fulfilment client analysis: filter `Service_Offering_c IN ('Fulfillment', 'Fulfillment + Last Mile')`
- 2025 fulfilment revenue: AED 11,167,340 (n=1,663 invoices) = 24.3% of total company revenue
- Top client: La Purete Group (AED 2.71M), top 15 = 83.3% of fulfilment revenue (highly concentrated)

## Data Quality Notes
- See `bigquery_execution_reference.md` for full schema docs (file is large, read in chunks: offset 977+ for invoicer)
- Grandparent SF IDs sometimes don't resolve in salesforce_current.accounts (e.g., Al Bayader showed raw SF ID)
