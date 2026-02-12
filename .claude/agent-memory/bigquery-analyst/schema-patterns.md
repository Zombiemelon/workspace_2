# Schema Patterns & Join Gotchas

Discovered patterns from working with the Quiqup data warehouse. These are things that tripped up queries or required non-obvious approaches.

## Account Hierarchy (invoicer_current.accounts)

- Accounts follow grandparent > parent > child hierarchy
- `invoice_to_parent` flag routes invoices to parent account
- Invoice `account_id` already reflects routing — joins directly, no manual routing needed
- For business group rollup: `COALESCE(grandparent_account_name, parent_account_name, account_name)`
- For SF name resolution: join `accounts.salesforce_id` to `salesforce_current.accounts.id`
- Some `account_name` values are raw Salesforce IDs — always LEFT JOIN to SF accounts for display names

## SSUP Catch-All

- "SSUP Grandparent account" (parent SF ID: `0010800003I4PcsAAF`) is a catch-all for self-signup accounts
- ~2,700 sub-accounts, 21,563 children treated individually (each is its own grandparent)
- Represents ~8.5% of 2025 revenue
- MUST exclude from "top client" rankings: `WHERE group_name NOT LIKE '%SSUP%'`

## Salesforce Service Offering Field

- Field: `salesforce_current.accounts.Service_Offering_c` (STRING)
- Distribution: Last Mile (22,819), NULL (9,381), On-demand (3,775), 4 Hours (997), Sameday (518), Fulfillment (517), Fulfillment + Last Mile (41)
- For fulfilment client analysis: `Service_Offering_c IN ('Fulfillment', 'Fulfillment + Last Mile')`

## B2B vs B2C Filter

- `client_type_c IS NULL` = B2B
- `client_type_c = 'Individual'` = B2C
- Must filter for B2B when doing business analysis

## Google Ads Dimension Tables

- Campaign and AdGroup tables are daily snapshots
- **MUST filter `_DATA_DATE = _LATEST_DATE`** or you get cartesian products
- Performance Max and Demand Gen campaigns don't have reliable ad group data — use campaign-level

## Currency

- All amounts are AED, not USD
- `google_ads_spend_usd` column in H2 view is mislabeled — it's actually AED
- `metrics_cost_micros` stores values in account currency (AED), divide by 1,000,000

## Date Field Gotchas

- Revenue: use `start_date` (Finance/billing period), NOT `end_date` — wrong date = ~205K AED discrepancy
- Opportunities: column is `created_date` (not `created_at`)
- Non-activated accounts: `first_delivered_order_date = 2030-01-01` is a placeholder, not a real date

## Invoice-to-Parent Deduplication

- Without dedup, revenue inflates **~19x**
- Always use the CASE WHEN join pattern on invoicer accounts
- `views.grandparent_revenue` handles this automatically — prefer it over manual joins

## GA4 Data

- `business-ae-beta.quiqup.com` has no data since May 29, 2025
- `views.google_analytics_events` filters `event_date > '2025-02-04'`
- Contact form: multiple event names can represent a submit — dedupe within short time window per user
- Internal tracking banner traffic (`utm_source=trackingpage` + `utm_medium=banner`) is excluded from all metrics in H2 view

## Key Join Patterns

```
Lead source mapping:     leads.lead_source = definition_lead_source.lead_source
GP lead source:          gac.gac_grandparent_account_id = grandparent_lead_source_attribution.grandparent_account_id
Account to SF:           master_account_data_daily.account_id = salesforce_current.accounts.id
Orders to clients:       orders.business_partner_id = business_accounts.id
UTM to Google Ads:       grandparent_utm_attribution.attributed_utm_campaign = definition_utm_google_ads_mapping.utm_campaign
```
