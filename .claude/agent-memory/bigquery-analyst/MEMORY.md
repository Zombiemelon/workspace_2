# BigQuery Analyst Agent Memory

## Definitions (READ FIRST)

All business definitions live in [definitions.md](definitions.md). Every definition maps to a specific BigQuery view/table. Never hardcode classification logic — always JOIN to the definition view.

Key definitions quick-reference:
- **Paid vs Organic** -> `views.definition_paid_organic_channel` (NOT paid = Organic)
- **Inbound vs Outbound** -> `views.definition_lead_source` (source_group)
- **Opp Conversion** -> `views.opportunities_convert_minus_2months` (parent account existence)
- **New vs Existing Client** -> `client_type_classification` on opp view (LEAST of child/GP created_date)
- **Net Revenue** -> `invoicer_current.invoices` (start_date, paid/overdue, total - tax)
- **Grandparent Resolution** -> `views.true_grandparent_account`
- **Activation** -> first_delivered_order_date IS NOT NULL (2030-01-01 = placeholder)

## Topic Files

| File | Contents |
|------|----------|
| [definitions.md](definitions.md) | All business definitions with source views, rules, join patterns |
| [schema-patterns.md](schema-patterns.md) | Account hierarchy, SSUP, join gotchas, currency, date fields |
| [opp-conversion-notes.md](opp-conversion-notes.md) | View logic, dashboard filter mismatch, validation counts |
| [revenue-benchmarks.md](revenue-benchmarks.md) | 2025 totals, concentration, fulfilment segment, cross-checks |
| [data-quality.md](data-quality.md) | NULL rates, SF ID resolution, GA4 gaps, file offsets |

## Critical Reminders

- SSUP catch-all: exclude from top-client rankings (`NOT LIKE '%SSUP%'`)
- `stage_name` is mutable — opp conversion snapshots drift over time
- `grandparent_utm_attribution` only has activated GPs — activation rate from it alone = always 100%
- Without invoice-to-parent dedup, revenue inflates ~19x
- Dashboard "Inbound Leads" filter != `definition_lead_source.source_group` (undercounts by ~88 opps)
- Google Ads dimension tables: MUST filter `_DATA_DATE = _LATEST_DATE`
