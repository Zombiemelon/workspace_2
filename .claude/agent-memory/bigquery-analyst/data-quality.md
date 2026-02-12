# Data Quality Notes

Known data quality issues, NULL rates, and resolution patterns.

## Grandparent SF ID Resolution

- Some grandparent Salesforce IDs don't resolve in `salesforce_current.accounts`
- Example: Al Bayader showed raw SF ID instead of account name
- Workaround: Always use LEFT JOIN (not INNER) and display COALESCE(sf_name, raw_id)

## UTM Attribution Coverage

- ~69% of accounts have no UTM attribution (NULL)
- `views.grandparent_utm_attribution` only contains **activated** GPs
- Using this view alone gives activation_rate = 100% (survivorship bias)
- For true acquisition counts, use `views.grandparent_account_created_date_and_first_order_delivered`

## Invoice Data

- `tax_amount` can be NULL — always use `COALESCE(tax_amount, 0)` in net revenue formula
- Currency stored as lowercase "aed" in data
- `record_deleted = FALSE` filter is critical — soft-deleted invoices exist

## Salesforce Opportunities

- `stage_name` is mutable — historical snapshot comparisons will drift
- All `type` values are NULL (no useful type classification on the opp itself)
- Only 1 `record_type_id` exists — no need to filter by record type
- No deleted opps in 2025-2026 range (but always filter `is_deleted = FALSE`)

## GA4 Data Gaps

- `business-ae-beta.quiqup.com` — no data since May 29, 2025
- `utm_term` may be URL-encoded (sometimes multiple times)
- Internal tracking banner traffic should be excluded from analysis

## Execution Reference File

The full schema documentation is in `bigquery_execution_reference.md` (1,846 lines).
- For invoicer schemas: read from offset 977+
- For views schemas: read from offset 245+
- For Google Ads schemas: read from offset 1400+
