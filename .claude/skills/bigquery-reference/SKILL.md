---
name: bigquery-reference
description: Quiqup BigQuery data warehouse reference — dataset overview, table grains, MCP tools, query best practices, canonical join keys, and key gotchas. Use before writing any BigQuery query to ensure correct table selection, join patterns, and data quality handling.
user-invocable: false
---

# BigQuery Execution Reference

Quick-reference for the Quiqup BigQuery data warehouse. For detailed column schemas, see `database-reference.md`. For validated SQL patterns, see `query-templates.md`.

## Quick Scan — All Tables & Views

### Datasets Overview

| Dataset | Purpose | When to Use |
|---------|---------|-------------|
| `quiqup.views.*` | Analytical views | **Start here** for most queries |
| `salesforce_current.*` | CRM data | Leads, accounts, opportunities, tasks |
| `ex_api_current.*` | Operational API | Orders, business accounts |
| `invoicer_current.*` | Invoicing | Invoices, line items, credit notes |
| `analytics_368564502.*` | GA4 raw events | Session/event-level drill-down |
| `google_ads_analytics.*` | Google Ads raw | Daily spend, campaign/ad group dimensions |
| `bi_reporting.*` | BI / Ops layer | Missions, couriers, sales funnel |

### Primary Reporting Layer (Start Here)

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `views.marketing_funnel_grandparent_monthly` | 1 row/month | **MAIN VIEW** — cohort LTV, ROI, break-even, paid/organic revenue |
| `views.quiqup_com_unique_visitors_monthly_2025_h2` | 1 row/month | Top-of-funnel: traffic -> leads -> spend (no cohort revenue) |
| `views.cac` | 1 row/account/week | Weekly CAC by marketing bucket |

### Definition & Mapping Tables (Source of Truth)

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `views.definition_paid_organic_channel` | 1 row/UTM source+medium | Paid vs Organic classification |
| `views.definition_lead_source` | 1 row/lead_source value | Lead source -> Inbound/Outbound/Old |
| `views.definition_utm_google_ads_mapping` | 1 row/UTM campaign | UTM -> Google Ads campaign + ad group |
| `views.definition_campaign_marketing_bucket` | 1 row/campaign name | Campaign -> region bucket (uae/ksa/marketplace) |
| `views.definition_high_intent_website_visitor` | 1 row/page event | High-intent page patterns (pricing, contact, demo) |
| `views.definition_traffic_channel` | 1 row/source+medium | UTM -> channel group (Paid Search, Paid Social, etc.) |

### Attribution & Revenue Views (Source of Truth)

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `views.grandparent_utm_attribution` | 1 row/grandparent | UTM attribution per GP (earliest-first, SSUP-aware) |
| `views.account_utm_attribution` | 1 row/SF account | UTM attribution per account (Lead->Opp->Account) |
| `views.account_lead_source_attribution` | 1 row/SF account | Lead source attribution per account (earliest-first) |
| `views.grandparent_lead_source_attribution` | 1 row/grandparent | Lead source attribution rolled up to GP (earliest-first) |
| `views.grandparent_revenue` | 1 row/grandparent | Deduplicated lifetime revenue per GP |
| `views.grandparent_account_created_date_and_first_order_delivered` | 1 row/grandparent | ALL GPs: acquisition date + activation date |
| `views.true_grandparent_account` | 1 row/account | Account -> grandparent hierarchy resolution |
| `views.google_ads_spend_monthly` | 1 row/month/campaign/adgroup | Pre-aggregated monthly spend |
| `views.opportunities_convert_minus_2months` | 1 row/opportunity | Opp→Account conversion. `is_converted` = all-time; `converted_by_reporting_month` = +2mo window. |
| `views.accounts_convert_minus_2months` | 1 row/account cohort | Account→Activation conversion (+2mo reporting offset) |

### Account & Traffic Views

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `views.master_account_data_daily` | 1 row/account/day | Account spine: lifecycle, UTM, activation, churn |
| `views.google_analytics_events` | 1 GA4 event | Flattened GA4 events (no manual event_params extraction) |
| `views.ga4_contact_form_submits` | 1 form submit event | Contact form submissions on quiqup.com |
| `views.ga4_traffic_classified_sessions_quiqup_com` | 1 session | Core paid/organic session classification |
| `views.salesforce_leads_monthly` | 1 row/month | Lead counts at various cleaning stages |

### Salesforce (CRM)

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `salesforce_current.accounts` | 1 SF account | Account data, `client_type_c`, UTM, activation signals |
| `salesforce_current.leads` | 1 SF lead | Lead data, `lead_source`, UTM, conversion FKs |
| `salesforce_current.opportunities` | 1 SF opportunity | Deal stage, classification, pricing model status |
| `salesforce_current.tasks` | 1 SF task | Email activities (filter `task_subtype = 'Email'`) |
| `salesforce_current.users` | 1 SF user | Owner/sender metadata |
| `salesforce_current.pricing_models` | 1 pricing model | Pricing definitions |

### Invoicer

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `invoicer_current.accounts` | 1 invoicing account | Hierarchy + `invoice_to_parent` flag |
| `invoicer_current.invoices` | 1 invoice | Billing: amount, state, start/end dates |
| `invoicer_current.invoice_lines` | 1 line item | Order-level charges on invoices |
| `invoicer_current.credit_notes` | 1 credit note | Refunds (typically COD) |
| `invoicer_current.forecast_invoice_lines` | 1 forecast line | Not-yet-invoiced expected charges |

### Operational API

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `ex_api_current.orders` | 1 order (current state) | Order data; use `order_state_changes` for history |
| `ex_api_current.business_accounts` | 1 business account | Client entities in ops system |
| `ex_api_current.order_state_changes` | 1 state transition | Historical order state transitions |

### Google Ads Raw

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `google_ads_analytics.ads_CampaignBasicStats_8350869641` | 1 row/campaign/day | Daily spend, clicks, impressions, conversions |
| `google_ads_analytics.ads_Campaign_8350869641` | 1 campaign/day (snapshot) | Campaign definitions. **MUST filter `_DATA_DATE = _LATEST_DATE`** |
| `google_ads_analytics.ads_AdGroup_8350869641` | 1 ad group/day (snapshot) | Ad group definitions. **MUST filter `_DATA_DATE = _LATEST_DATE`** |

### BI Reporting

| Table | Grain | What It Defines |
|-------|-------|-----------------|
| `bi_reporting.sales_funnel` | 1 funnel entity | Combined Leads + Opps + Accounts |
| `bi_reporting.missions` | 1 mission | Delivery missions |
| `bi_reporting.internal_orders` | 1 mission-order link | Mission <-> order relationship |
| `bi_reporting.client_orders` | 1 order (BI layer) | Order with `state_updated_at` for delivery timing |
| `bi_reporting.couriers` | 1 courier | Courier profiles |

### When to Query Raw Tables Instead of Views

1. **Drill-down beyond monthly granularity** → `salesforce_current.leads`, `google_ads_analytics.*`
2. **Individual lead/account details** → `salesforce_current.leads`, `salesforce_current.accounts`
3. **Raw invoice line items** → `invoicer_current.invoice_lines`
4. **Verification/reconciliation** → Cross-check views against raw tables

## Key Gotchas

| Gotcha | Impact |
|--------|--------|
| `grandparent_utm_attribution` only has **activated** GPs | Activation rate = always 100% if used alone |
| Without `invoice_to_parent` dedup, revenue inflates **~19x** | Always use CASE WHEN join on invoicer |
| `client_type_c IS NULL` = B2B, `'Individual'` = B2C | Must filter for B2B analysis |
| Google Ads dimension tables need `_DATA_DATE = _LATEST_DATE` | Without filter -> cartesian products |
| `start_date` for Finance/Xero reconciliation, NOT `end_date` | Wrong date = ~205K AED discrepancy |
| Currency is **AED** not USD | `google_ads_spend_usd` column is mislabeled — it's AED |
| "Not paid" = Organic (including NULL/missing UTM) | Organic is the catch-all bucket |
| SSUP accounts (parent `0010800003I4PcsAAF`) = own grandparent | 21,563 self-signup children treated individually |
| `gac_grandparent_first_order_delivered = 2030-01-01` | Placeholder for non-activated accounts |
| Paid definition differs: GA4 (broad) vs Attribution (`cpc` only) | Use GA4 for traffic, `cpc` for ROI |

## Formulas Quick Reference

| Metric | Formula |
|--------|---------|
| **Gross Margin** | `revenue x 0.25` |
| **ROI** | `(margin - spend) / spend x 100` |
| **CAC** | `spend / customers_acquired` |
| **Break-Even** | `spend / monthly_margin_rate` |
| **LTV:CAC** | `lifetime_margin_per_customer / CAC` (healthy = 3.0+) |

## Tools

**Required:** Use BigQuery MCP tools for all data retrieval:
- `mcp__BigQuery_Toolbox__execute_sql` — Run SQL queries
- `mcp__BigQuery_Toolbox__get_table_info` — Get schema/metadata
- `mcp__BigQuery_Toolbox__get_dataset_info` — Get dataset information
- `mcp__BigQuery_Toolbox__list_table_ids` — List tables in a dataset
- `mcp__BigQuery_Toolbox__list_dataset_ids` — List available datasets
- `mcp__BigQuery_Toolbox__search_catalog` — Search for tables/views by name
- `mcp__BigQuery_Toolbox__ask_data_insights` — AI-assisted insights
- `mcp__BigQuery_Toolbox__analyze_contribution` — Metric contributions
- `mcp__BigQuery_Toolbox__forecast` — Time-series forecasting

**Important:** Always use ToolSearch to load these tools before invoking them.

## Query Best Practices

1. **Check the Quick Scan above** for correct table names, grains, and gotchas.
2. **Query safely:** `LIMIT` during exploration. Filter on partition columns. Avoid `SELECT *`.
3. **Common join patterns:**
   - Lead source: `JOIN views.definition_lead_source ON leads.lead_source = definition_lead_source.lead_source`
   - GP lead source: `JOIN views.grandparent_lead_source_attribution ON gac.gac_grandparent_account_id = gls.grandparent_account_id`
   - Account to SF: `JOIN salesforce_current.accounts ON master.account_id = accounts.id`
   - Orders to clients: `JOIN ex_api_current.business_accounts ON orders.business_partner_id = business_accounts.id`

### Query Explanation Template

After executing any query, provide:
- **Query Logic:** 1-3 sentences explaining what the query calculates
- **Fields Used:** Table of field | table | business meaning
- **Why This Approach:** Brief rationale for table selection, join strategy, or filtering

## Marketing Spend Verification (REQUIRED)

**For ANY analysis involving marketing spend:**

1. **Verify totals against raw Google Ads data:**
```sql
SELECT 'google_ads_spend_monthly' as source, SUM(spend_aed) as spend, SUM(clicks) as clicks
FROM views.google_ads_spend_monthly WHERE month = '[MONTH]'
UNION ALL
SELECT 'CampaignBasicStats (raw)', ROUND(SUM(metrics_cost_micros)/1000000, 2), SUM(metrics_clicks)
FROM google_ads_analytics.ads_CampaignBasicStats_8350869641
WHERE segments_date >= '[MONTH_START]' AND segments_date < '[MONTH_END]'
```
2. **Currency is AED, not USD.** The `google_ads_spend_usd` column is mislabeled.
3. **Performance Max / Demand Gen:** No reliable ad group data. Use campaign-level stats.
4. **Clicks must match.** Investigate discrepancies before proceeding.
5. **Report discrepancies >1%** explicitly.

## Canonical Join Keys

| From | To | Join Key |
|------|----|----|
| `invoicer.accounts` | `invoicer.invoices` | `accounts.account_id = invoices.account_id` (or `parent_account_id` if `invoice_to_parent`) |
| `invoicer.invoices` | `invoice_lines` | `invoices.id = invoice_lines.invoice_id` |
| `invoicer.accounts` | `sf.accounts` | `accounts.salesforce_id = sf_accounts.id` |
| `master_account_data_daily` | `sf.accounts` | `master.account_id = accounts.id` |
| `sf.leads` | `definition_lead_source` | `leads.lead_source = definition_lead_source.lead_source` |
| `sf.leads` | `sf.opportunities` | `leads.converted_opportunity_id = opportunities.id` |
| `sf.tasks` | `sf.opportunities` | `tasks.what_id = opportunities.id` |
| `orders` | `business_accounts` | `orders.business_partner_id = business_accounts.id` |
| `gp_lead_source_attribution` | `gp_created_date` | `gls.grandparent_account_id = gac.gac_grandparent_account_id` |

### Bridging Notes

- **master_account → orders:** `master.external_id` (INT64) vs `business_accounts.external_id` (STRING). Cast to bridge.
- **UTM → Google Ads:** Use `views.definition_utm_google_ads_mapping` or construct: `CONCAT(REPLACE(REPLACE(campaign_name, ' - ', '_'), ' ', '-'), '_', REPLACE(ad_group_name, ' ', '-'))`

## Critical View Semantics

### `marketing_funnel_grandparent_monthly`
- **Cohort-based:** Revenue/activation for cohort acquired in month M, not total business in month M
- **ALL GPs included:** Not just those with UTM attribution
- **Paid/Organic:** Uses `definition_paid_organic_channel`. NOT paid = Organic (including unattributed)
- **Invoice-to-parent dedup:** Revenue deduplicated at GP level
- **Break-even:** `< cohort_age_months` = profitable; `> cohort_age_months` = not yet; 50+ = unlikely
- **Agency fee:** 3,600 AED/month standard. Include for true cost analysis.

### `grandparent_utm_attribution`
- **ONLY activated GPs.** DO NOT use for activation rates (always = 100%).
- For activation analysis: start from `salesforce_current.accounts` + `account_utm_attribution`, LEFT JOIN to `grandparent_account_created_date_and_first_order_delivered`.

## Supporting Files

- **`database-reference.md`** — Full column schemas for every dataset. Read when you need column-level detail.
- **`query-templates.md`** — Validated SQL patterns: Ad Group ROI, Opp Conversion Cohort Revenue, Campaign Break-Even, Financial Calculations, Statistical Methods.
