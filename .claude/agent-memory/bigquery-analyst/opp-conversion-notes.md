# Opportunity Conversion View Notes

Detailed notes on `views.opportunities_convert_minus_2months` behavior discovered through analysis.

## View Join Chain

```
salesforce_current.opportunities
  -> salesforce_current.accounts (child, on opp.account_id = acc.id)
  -> salesforce_current.accounts (parent, on acc.parent_id = parent.id)
  -> views.true_grandparent_account (on acc.id)
  -> salesforce_current.accounts (grandparent)
```

## Key Computed Columns

| Column | Type | Logic |
|--------|------|-------|
| `opp_created_month` | DATE | Month-truncated `opp.created_date` |
| `conversion_month` | DATE | `opp_created_month + 2 months` (reporting offset, NOT actual conversion) |
| `raw_conversion_month` | DATE | `DATE_TRUNC(parent.created_date, MONTH)` (actual conversion month) |
| `is_converted` | BOOL | Parent exists AND stage != 'Deal Lost' (all-time, no window) |
| `converted_by_reporting_month` | BOOL | Parent exists + created before end of reporting window + not Deal Lost |
| `client_type_classification` | STRING | `LEAST(child, grandparent)` created_date comparison (updated 2026-02-10) |

## +2 Month Reporting Offset

- Opps created in **May** appear in the **July** bar on the dashboard
- They have until **end of July** to convert (parent account created before Aug 1)
- Each cohort gets a consistent 2-month window

## Stage Mutability Warning

`stage_name` is mutable — opps can change stage retroactively. This means:
- Conversion rates drift vs historical snapshots
- Only 1 record_type_id exists; all `type` values are NULL
- No deleted opps in 2025-2026 range

## Stage Distribution (May 2025 - Feb 2026, inbound)

- Deal Lost: 255
- Deal Done: 77
- Pipeline stages: 29
- Total rows (is_deleted=FALSE): 6,731 (as of 2026-02-10)

## Dashboard Filter Mismatch (discovered 2026-02-10)

The dashboard "Inbound Leads" filter uses a **CUSTOM list of 48 lead_source values**, NOT the `definition_lead_source.source_group` mapping. Key discrepancies:

- 36 of 48 values in the dashboard filter have zero opps in the date range (legacy/international values)
- Lead sources in `definition_lead_source` Inbound but MISSING from dashboard filter:
  - `Inbound: Self-signup` — 37 opps
  - `Existing Client` — 27 opps
  - `Inbound : Leadership referral` — 24 opps

**Impact:** Dashboard undercounts inbound opportunities by ~88 opps in the May 2025-Jan 2026 window.

## Validation: Expected Monthly Opportunity Counts

Source: Dashboard "Monthly Opportunities" chart (x-axis = `opp_created_month`)

| Month | Expected Count |
|-------|---------------|
| May 2025 | 58 |
| Jun 2025 | 70 |
| Jul 2025 | 78 |
| Aug 2025 | 51 |
| Sep 2025 | 80 |
| Oct 2025 | 57 |
| Nov 2025 | 57 |
| Dec 2025 | 57 |
| Jan 2026 | 79 |

*Validated 2026-02-09. These numbers may drift as stage_name is mutable.*

**Validation query:**
```sql
SELECT DATE_TRUNC(DATE(created_date), MONTH) AS created_month, COUNT(*) AS total
FROM salesforce_current.opportunities
WHERE is_deleted = FALSE
  AND DATE(created_date) >= '2025-05-01' AND DATE(created_date) < '2026-02-01'
GROUP BY 1 ORDER BY 1
```

**Cross-check:** The view's `opp_created_month` with `is_deleted = FALSE` must produce identical counts.

**Key notes:**
- Dashboard "Monthly Opportunities" uses `opp_created_month`, NOT `conversion_month`
- The conversion rate chart uses `conversion_month` (= opp_created_month + 2 months)
- Filter: `is_deleted = FALSE` only — no stage or client_type filter
