# Execution Layer

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
| `views.account_lead_source_attribution` | 1 row/SF account | Lead source attribution per account (earliest-first across Lead→Opp→Account) |
| `views.grandparent_lead_source_attribution` | 1 row/grandparent | Lead source attribution rolled up to GP (earliest-first, via `true_grandparent_account`) |
| `views.grandparent_revenue` | 1 row/grandparent | Deduplicated lifetime revenue per GP |
| `views.grandparent_account_created_date_and_first_order_delivered` | 1 row/grandparent | ALL GPs: acquisition date + activation date |
| `views.true_grandparent_account` | 1 row/account | Account -> grandparent hierarchy resolution |
| `views.google_ads_spend_monthly` | 1 row/month/campaign/adgroup | Pre-aggregated monthly spend |
| `views.opportunities_convert_minus_2months` | 1 row/opportunity | Opp→Account conversion status (parent account created date). `converted_by_reporting_month` for 2mo-windowed dashboard; `is_converted` for all-time conversion (parent exists + not Deal Lost, no time window). `client_type_classification` uses `LEAST(child, grandparent)` created_date via `true_grandparent_account` join (updated 2026-02-10). |
| `views.accounts_convert_minus_2months` | 1 row/account cohort | Account→Activation conversion (delivered-order at grandparent level, +2mo reporting offset) |

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
| `ex_api_current.order_address_changes` | 1 address change | Order address modification events |

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

### Key Gotchas (Quick Scan)

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

### Formulas Quick Reference

| Metric | Formula |
|--------|---------|
| **Gross Margin** | `revenue x 0.25` |
| **ROI** | `(margin - spend) / spend x 100` |
| **CAC** | `spend / customers_acquired` |
| **Break-Even** | `spend / monthly_margin_rate` |
| **LTV:CAC** | `lifetime_margin_per_customer / CAC` (healthy = 3.0+) |

---

## Tools

**Required:** You MUST use the BigQuery MCP tools for all data retrieval:
- `mcp__BigQuery_Toolbox__execute_sql` — Run SQL queries against BigQuery
- `mcp__BigQuery_Toolbox__get_table_info` — Get schema/metadata for tables
- `mcp__BigQuery_Toolbox__get_dataset_info` — Get dataset information
- `mcp__BigQuery_Toolbox__list_table_ids` — List tables in a dataset
- `mcp__BigQuery_Toolbox__list_dataset_ids` — List available datasets
- `mcp__BigQuery_Toolbox__search_catalog` — Search for tables/views by name
- `mcp__BigQuery_Toolbox__ask_data_insights` — Get AI-assisted insights on data
- `mcp__BigQuery_Toolbox__analyze_contribution` — Analyze metric contributions
- `mcp__BigQuery_Toolbox__forecast` — Time-series forecasting

**Important:** Always use ToolSearch to load these tools before invoking them.

## Knowledge

**ALWAYS consult the Database Reference section below before writing queries.** It contains:
- Dataset and table definitions (grain, purpose, key columns)
- Canonical join relationships
- Data quality notes and gotchas
- Bridging notes for ID mismatches

**Key datasets:**
| Dataset | Purpose |
|---------|---------|
| `quiqup.views.*` | Analytical views — **start here for most queries** |
| ↳ `views.quiqup_com_unique_visitors_monthly_2025_h2` | Monthly marketing funnel (traffic, leads, spend) |
| ↳ `views.google_ads_spend_monthly` | Pre-aggregated spend by campaign/ad group |
| ↳ `views.definition_*` | Mapping tables (UTM→Google Ads, lead source, campaign bucket) |
| ↳ `views.master_account_data_daily` | Account spine with attribution + activation |
| ↳ `views.cac` | Weekly CAC by marketing bucket |
| `salesforce_current.*` | CRM data (leads, accounts, opportunities, tasks) |
| `ex_api_current.*` | Operational API data (orders, business_accounts) |
| `invoicer_current.*` | Invoicing data |
| `analytics_368564502.*` | GA4 raw events |
| `google_ads_analytics.*` | Google Ads metrics |
| `bi_reporting.*` | BI layer / ops reporting |

## Query Best Practices

1. **Always check the Database Reference section first** for:
   - Correct table/view names
   - Column definitions and data types
   - Known join keys
   - Data quality caveats

2. **Query safely:**
   - Use `LIMIT` during exploration
   - Filter on partition columns when available (`event_date`, `updated_at`)
   - Avoid `SELECT *` on large tables

3. **Common patterns:**
   - Lead source mapping: `JOIN views.definition_lead_source ON leads.lead_source = definition_lead_source.lead_source`
   - GP lead source attribution: `JOIN views.grandparent_lead_source_attribution ON gac.gac_grandparent_account_id = grandparent_lead_source_attribution.grandparent_account_id`
   - Account to Salesforce: `JOIN salesforce_current.accounts ON master_account_data_daily.account_id = accounts.id`
   - Orders to clients: `JOIN ex_api_current.business_accounts ON orders.business_partner_id = business_accounts.id`

## Query Explanation Template

After executing any query, provide this documentation:

**Query Logic:**
> [1-3 sentences explaining what the query calculates and the analytical approach]

**Fields Used:**
| Field | Table | Meaning |
|-------|-------|---------|
| `field_name` | `source_table` | Business definition of what this field represents |

**Why This Approach:**
> [Brief rationale for table selection, join strategy, or filtering logic]

## Marketing Spend Verification (REQUIRED)

**For ANY analysis involving marketing spend, leads attribution, or campaign performance:**

1. **Always verify totals against raw Google Ads data:**
```sql
-- Verification query: Compare aggregated views to raw source
SELECT
  'google_ads_spend_monthly' as source, SUM(spend_aed) as spend, SUM(clicks) as clicks
FROM views.google_ads_spend_monthly WHERE month = '[MONTH]'
UNION ALL
SELECT
  'CampaignBasicStats (raw)', ROUND(SUM(metrics_cost_micros)/1000000, 2), SUM(metrics_clicks)
FROM google_ads_analytics.ads_CampaignBasicStats_8350869641
WHERE segments_date >= '[MONTH_START]' AND segments_date < '[MONTH_END]'
```

2. **Currency is AED, not USD:** BigQuery `metrics_cost_micros` stores values in account currency (AED). The column `google_ads_spend_usd` in H2 view is mislabeled — it's actually AED.

3. **Performance Max and Demand Gen:** These campaign types don't have reliable ad group data. Use campaign-level stats from `CampaignBasicStats`.

4. **Clicks should always match:** If clicks don't match between views and raw data, investigate before proceeding.

5. **Report any discrepancies:** If totals don't match within 1%, flag it explicitly and investigate the cause.

---

# Database Reference

This is a query-free reference for the Quiqup BigQuery project data model: datasets, tables/views, row meaning ("grain"), key columns, and relationships.

## Global Context

- **Project:** `quiqup`
- **Region:** Many datasets are **EU** (notably `analytics_368564502` and `google_ads_analytics`).
- **Preferred Salesforce dataset:** `salesforce_current` (current snapshot).

---

## Dataset: `analytics_368564502` (GA4)

### View: `quiqup.views.google_analytics_events`
- **Row meaning (grain):** 1 GA4 event.
- **Purpose:** Flattened/cleaned GA4 events for analysis (avoids manual `event_params` extraction).
- **Key columns:**
  - `event_date` (DATE)
  - `event_name` (STRING)
  - `user_pseudo_id` (STRING)
  - `page_location` (STRING)
  - `page_title` (STRING)
  - `campaign_source`, `campaign_medium`, `campaign_name` (STRING)
- **Data coverage note:** Filters `event_date > '2025-02-04'`.

### Raw tables: `analytics_368564502.events_*`
- **Row meaning (grain):** 1 GA4 event (nested schema).
- **Notes:** Sharded by date; `event_params` is nested and requires extraction.
- **Data completeness note:** `business-ae-beta.quiqup.com` has no data since **May 29, 2025**.

---

## Dataset: `views` (Analytical Views)

### Table: `quiqup.views.master_account_data_daily`
- **Row meaning (grain):** 1 account/client snapshot row per day (enriched "account spine").
- **Purpose:** Account lifecycle + attribution + activation/churn signals.
- **Key columns:**
  - `external_id` (INT64): external client identifier (commonly used as "client id" in analysis).
  - `day_created_client` (DATE): client creation date.
  - `earliest_created_date` (DATE): preferred account creation date for cohorts.
  - `minimum_created_date` (TIMESTAMP): fallback creation timestamp (convert to DATE when needed).
  - `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` (STRING): attribution fields.
  - `total_orders` (INT64): total orders for the account scope represented by the row.
  - `first_orde_submitted_calculated` (TIMESTAMP): first submit timestamp.
  - `is_activated` (BOOL): activation status.
  - `account_id` (STRING): Salesforce account id (used to link to `salesforce_current.accounts`).
  - `pricing_model` (STRING): pricing model id (links to `salesforce_current.pricing_models.id`).
- **Data quality note:** `utm_term` may be URL-encoded (sometimes multiple times).

### View/Table: `quiqup.views.definition_lead_source`
- **Row meaning (grain):** 1 row per Salesforce `lead_source` value (definition mapping).
- **Purpose:** Canonical mapping of raw `lead_source` → standardized groups/flags.
- **Key columns:**
  - `lead_source` (STRING)
  - `source_group` (STRING): e.g., Inbound/Outbound/Old.
  - `is_website_source` (BOOL): website-originated lead sources.
  - `is_contact_form` (BOOL): contact-form lead sources (for GA4↔SF reconciliation).

### View/Table: `quiqup.views.definition_paid_organic_channel` ⭐ NEW
- **Row meaning (grain):** 1 row per UTM source/medium combination.
- **Purpose:** **Single source of truth** for paid vs organic channel classification.
- **Key columns:**
  - `utm_source` (STRING): UTM source value (or '*' for wildcard)
  - `utm_medium` (STRING): UTM medium value
  - `channel_type` (STRING): 'Paid' or 'Organic'
  - `channel_detail` (STRING): Specific channel name (e.g., 'Google Ads', 'Meta Ads', 'No Attribution')
  - `is_paid` (BOOL): TRUE for paid channels, FALSE for organic
- **Classification rule:** What is NOT explicitly PAID is ORGANIC (including missing UTM)
- **Paid channels:**
  - `utm_medium IN ('cpc', 'ppc', 'paid', 'paid_social', 'display', 'banner')`
  - Meta Ads: `utm_source IN ('fb', 'ig', 'facebook', 'instagram')` with paid mediums
- **Organic channels:** Internal (ldr, bdm), direct, email, referral, malformed UTM, NULL/missing
- **Usage:**
```sql
-- Join with priority: exact match > wildcard > default organic
SELECT
  COALESCE(exact.is_paid, wildcard.is_paid, FALSE) AS is_paid
FROM your_table t
LEFT JOIN views.definition_paid_organic_channel exact
  ON LOWER(t.utm_source) = LOWER(exact.utm_source)
  AND LOWER(t.utm_medium) = LOWER(exact.utm_medium)
  AND exact.utm_source != '*'
LEFT JOIN views.definition_paid_organic_channel wildcard
  ON wildcard.utm_source = '*'
  AND LOWER(t.utm_medium) = LOWER(wildcard.utm_medium)
```

### View: `quiqup.views.ga4_contact_form_submits`
- **Row meaning (grain):** 1 GA4 "contact form submit" event (canonicalized).
- **Purpose:** Standardized contact-form submission events on `www.quiqup.com` contact-related pages.
- **Key columns:**
  - `event_date` (DATE)
  - `event_datetime` (TIMESTAMP)
  - `user_pseudo_id` (STRING)
  - `ga_session_id` (INT64/STRING depending on view implementation)
  - `event_name` (STRING)
  - `page_location` (STRING)
  - `path` (STRING)
  - `is_tracking_page` (BOOL)
- **Event family semantics:** Multiple event names can represent a submit; treat all as "submission" and dedupe within a short time window per user when counting submissions.

### View: `quiqup.views.quiqup_com_unique_visitors_monthly_2025_h2`
- **Row meaning (grain):** 1 row per month.
- **Purpose:** Monthly funnel spine for `https://www.quiqup.com`: traffic → GA4 submits → Salesforce lead creation + marketing spend.
- **Key columns:**
  - `month` (DATE)
  - `unique_visitors` (INT64)
  - `high_intent_visitors` (INT64)
  - `paid_unique_visitors`, `organic_unique_visitors` (INT64): paid/organic split
  - `google_ads_paid_unique_visitors` (INT64): subset of paid visitors from Google Ads specifically
  - `google_ads_paid_sessions` (INT64): session count from Google Ads (use for clicks comparison)
  - `ga4_website_leads` (INT64): distinct submitters (GA4 `user_pseudo_id`)
  - `sf_contact_form_website_source_leads_deduped` (INT64): recommended Salesforce funnel metric
  - **Spend columns (embedded):**
    - `google_ads_spend_aed` (FLOAT64): monthly Google Ads spend (currency: AED)
    - `google_ads_clicks` (INT64): monthly clicks
    - `google_ads_impressions` (INT64): monthly impressions
    - `cost_per_lead_aed` (FLOAT64): `spend / sf_leads`
    - `cost_per_click_aed` (FLOAT64): `spend / clicks`
- **Important exclusion:** Internal tracking banner experiment traffic (`utm_source=trackingpage` + `utm_medium=banner`) is excluded from all metrics.
- **Drill-down:** For granular data, join to `salesforce_current.leads` by month or use campaign-level stats directly.

**⚠️ Paid vs Organic Classification (GA4 Traffic):**

The view uses session-level classification, then aggregates to user level:

| Classification | Logic | Notes |
|----------------|-------|-------|
| **Paid session** | Has `gclid` OR `wbraid` OR `gbraid` OR channel_group starts with 'Paid' OR `utm_medium` IN ('cpc', 'ppc', 'paid', 'paid_social', 'display', 'banner') | Any paid signal counts |
| **Google Ads session** | Has `gclid`/`wbraid`/`gbraid` OR (`utm_source='google'` AND `utm_medium='cpc'`) | Subset of paid |
| **Organic session** | NOT a paid session | Default if no paid signals |

**User-level aggregation:** A user is counted as `paid_unique_visitor` if they had **ANY** paid session in the month (uses MAX). This means a user who visits once via paid and once via organic is counted as paid only.

**Click IDs explained:**
- `gclid` — Google Click ID (standard Google Ads tracking)
- `wbraid` — Web attribution for iOS (privacy-preserving, post-iOS 14.5)
- `gbraid` — App attribution for iOS (cross-app tracking)

**Underlying views dependency tree:**
```
quiqup_com_unique_visitors_monthly_2025_h2
├── ga4_unique_visitors_monthly ← ga4_pageviews_quiqup_com_base
├── ga4_high_intent_visitors_monthly ← definition_high_intent_website_visitor
├── ga4_channel_monthly_quiqup_com ← ga4_user_month_channel_quiqup_com
│   └── ga4_traffic_classified_sessions_quiqup_com  ← [PAID/ORGANIC LOGIC HERE]
│       ├── ga4_landing_utm_extracted_quiqup_com ← ga4_landing_sessions_quiqup_com
│       └── definition_traffic_channel (mapping table)
├── ga4_google_ads_paid_sessions_monthly_quiqup_com ← ga4_traffic_classified_sessions_quiqup_com
├── ga4_contact_form_submitters_monthly_quiqup_com ← ga4_contact_form_submits
├── salesforce_leads_monthly ← salesforce_contact_form_leads_clean
└── [embedded CTE] monthly_spend ← ads_CampaignBasicStats_8350869641
```

**Drill-down queries from H2:**
```sql
-- Monthly funnel (aggregated)
SELECT * FROM views.quiqup_com_unique_visitors_monthly_2025_h2
WHERE month = '2025-12-01'

-- Drill to leads for that month
SELECT l.id, l.created_date, l.utm_campaign_c, l.utm_source_c, l.lead_source
FROM salesforce_current.leads l
JOIN views.definition_lead_source dls ON l.lead_source = dls.lead_source
WHERE DATE_TRUNC(DATE(l.created_date), MONTH) = '2025-12-01'
  AND dls.is_contact_form = TRUE

-- Drill to campaign spend breakdown
SELECT camp.campaign_name, COALESCE(bucket.marketing_bucket, 'other') as bucket,
  SUM(stats.metrics_cost_micros) / 1000000 as spend_usd
FROM google_ads_analytics.ads_CampaignBasicStats_8350869641 stats
JOIN google_ads_analytics.ads_Campaign_8350869641 camp
  ON stats.campaign_id = camp.campaign_id AND camp._DATA_DATE = camp._LATEST_DATE
LEFT JOIN views.definition_campaign_marketing_bucket bucket ON camp.campaign_name = bucket.campaign_name
WHERE DATE_TRUNC(stats.segments_date, MONTH) = '2025-12-01'
GROUP BY 1, 2
```

### View: `quiqup.views.marketing_funnel_grandparent_monthly`

---

## 🎯 THIS IS THE SINGLE SOURCE OF TRUTH FOR MARKETING PERFORMANCE

**Use this view for ALL marketing ROI, cohort, and acquisition analysis.** Do not query underlying tables directly unless you need drill-down beyond what this view provides.

---

- **Row meaning (grain):** 1 row per month (H2 2025: July–December).
- **Purpose:** **Main table for marketing expense analysis.** Extends H2 with cohort-based grandparent metrics — acquisitions, activation, and lifetime revenue attributed to each monthly cohort.

### Column Reference with Calculation Logic

#### Traffic & Leads Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `month` | DATE | First day of month | Direct from H2 view |
| `unique_visitors` | INT64 | COUNT DISTINCT GA4 `user_pseudo_id` on quiqup.com | `views.quiqup_com_unique_visitors_monthly_2025_h2` |
| `high_intent_visitors` | INT64 | Visitors who viewed pricing, contact, or demo pages | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `definition_high_intent_website_visitor` |
| `paid_unique_visitors` | INT64 | Users with ANY paid session (gclid/wbraid/gbraid OR paid utm_medium) | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ga4_traffic_classified_sessions_quiqup_com` |
| `organic_unique_visitors` | INT64 | Users with NO paid sessions | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ga4_traffic_classified_sessions_quiqup_com` |
| `ga4_website_leads` | INT64 | COUNT DISTINCT `user_pseudo_id` who submitted contact form (GA4 event) | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ga4_contact_form_submits` |
| `sf_contact_form_website_source_leads_deduped` | INT64 | Salesforce leads from website, valid email/phone, deduplicated | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `salesforce_leads_monthly` |

#### Spend Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `google_ads_spend_aed` | FLOAT64 | SUM(`metrics_cost_micros` / 1000000) for the month | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ads_CampaignBasicStats_8350869641` |
| `google_ads_clicks` | INT64 | SUM(`metrics_clicks`) for the month | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ads_CampaignBasicStats_8350869641` |
| `google_ads_impressions` | INT64 | SUM(`metrics_impressions`) for the month | `views.quiqup_com_unique_visitors_monthly_2025_h2` ← `ads_CampaignBasicStats_8350869641` |

#### Grandparent Acquisition Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `grandparents_acquired` | INT64 | COUNT DISTINCT grandparents created in month M (**ALL**, with or without UTM) | `views.grandparent_account_created_date_and_first_order_delivered` |
| `gp_with_attribution` | INT64 | COUNT DISTINCT grandparents with non-NULL UTM attribution | `views.grandparent_utm_attribution` |
| `attribution_coverage_pct` | FLOAT64 | `gp_with_attribution / grandparents_acquired × 100` | Calculated |
| `gp_acquired_paid` | INT64 | COUNT DISTINCT grandparents where UTM matches PAID channel. **Calculation:** Joins `grandparent_utm_attribution` to `definition_paid_organic_channel` on `utm_source` + `utm_medium`, takes those with `is_paid = TRUE` | **`views.definition_paid_organic_channel`** (source of truth for paid/organic) |
| `gp_acquired_organic` | INT64 | `grandparents_acquired - gp_acquired_paid`. Includes unattributed GPs (NULL UTM = organic) | Calculated from `grandparents_acquired` minus `gp_acquired_paid` |
| `gp_acquired_from_google` | INT64 | COUNT DISTINCT grandparents where `attributed_utm_source = 'google'` | `views.grandparent_utm_attribution` |
| `distinct_campaigns_in_cohort` | INT64 | COUNT DISTINCT `attributed_utm_campaign` for cohort month | `views.grandparent_utm_attribution` |

#### Activation Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `cohort_ever_activated` | INT64 | COUNT grandparents from cohort with `first_delivered_order_date IS NOT NULL` | `views.grandparent_account_created_date_and_first_order_delivered` |
| `cohort_activation_rate_pct` | FLOAT64 | `cohort_ever_activated / grandparents_acquired × 100` | Calculated |

#### Revenue Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `cohort_lifetime_revenue_aed` | FLOAT64 | SUM of `total_revenue_aed` for ALL grandparents in cohort. **Invoice-to-parent deduplicated.** | **`views.grandparent_revenue`** (source of truth for revenue) |
| `cohort_lifetime_revenue_paid_aed` | FLOAT64 | SUM of revenue for grandparents with `is_paid = TRUE` channel | `views.grandparent_revenue` + `views.definition_paid_organic_channel` |
| `cohort_lifetime_revenue_organic_aed` | FLOAT64 | SUM of revenue for grandparents with organic/unattributed channel | `views.grandparent_revenue` + `views.definition_paid_organic_channel` |
| `revenue_paid_pct` | FLOAT64 | `cohort_lifetime_revenue_paid_aed / cohort_lifetime_revenue_aed × 100` | Calculated |
| `revenue_organic_pct` | FLOAT64 | `cohort_lifetime_revenue_organic_aed / cohort_lifetime_revenue_aed × 100` | Calculated |
| `cohort_total_orders` | INT64 | COUNT of delivered orders from cohort grandparents | `views.grandparent_account_created_date_and_first_order_delivered` |

#### Margin Columns (Revenue × 0.25)
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `cohort_margin_aed` | FLOAT64 | `cohort_lifetime_revenue_aed × 0.25` | Calculated (25% gross margin) |
| `cohort_margin_paid_aed` | FLOAT64 | `cohort_lifetime_revenue_paid_aed × 0.25` | Calculated |
| `cohort_margin_organic_aed` | FLOAT64 | `cohort_lifetime_revenue_organic_aed × 0.25` | Calculated |

#### Unit Economics Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `cost_per_gp_acquired` | FLOAT64 | `google_ads_spend_aed / grandparents_acquired` | Calculated |
| `cost_per_gp_acquired_paid` | FLOAT64 | `google_ads_spend_aed / gp_acquired_paid` | Calculated |
| `ltv_per_gp_acquired` | FLOAT64 | `cohort_lifetime_revenue_aed / grandparents_acquired` | Calculated |
| `ltv_per_gp_acquired_paid` | FLOAT64 | `cohort_lifetime_revenue_paid_aed / gp_acquired_paid` | Calculated |
| `ltv_per_gp_acquired_organic` | FLOAT64 | `cohort_lifetime_revenue_organic_aed / gp_acquired_organic` | Calculated |
| `ltv_margin_per_gp_acquired` | FLOAT64 | `cohort_margin_aed / grandparents_acquired` — **Use this for profitability** | Calculated |
| `ltv_margin_per_gp_acquired_paid` | FLOAT64 | `cohort_margin_paid_aed / gp_acquired_paid` | Calculated |
| `ltv_margin_per_gp_acquired_organic` | FLOAT64 | `cohort_margin_organic_aed / gp_acquired_organic` | Calculated |
| `cohort_roi` | FLOAT64 | `(cohort_margin_aed - google_ads_spend_aed) / google_ads_spend_aed` | Calculated |
| `cohort_roi_paid` | FLOAT64 | `(cohort_margin_paid_aed - google_ads_spend_aed) / google_ads_spend_aed` | Calculated |

#### Break-Even Analysis Columns
| Column | Type | Calculation | Source Table |
|--------|------|-------------|--------------|
| `cohort_age_months` | INT64 | Months since cohort month (minimum 1) | Calculated from current date |
| `monthly_margin_paid_aed` | FLOAT64 | `cohort_margin_paid_aed / cohort_age_months` — Monthly run-rate | Calculated |
| `monthly_margin_total_aed` | FLOAT64 | `cohort_margin_aed / cohort_age_months` | Calculated |
| `breakeven_months_paid` | FLOAT64 | `google_ads_spend_aed / monthly_margin_paid_aed` — Months to recover ad spend from paid margin | Calculated |
| `breakeven_months_paid_with_agency` | FLOAT64 | `(google_ads_spend_aed + 3600) / monthly_margin_paid_aed` — Includes 3,600 AED agency fee | Calculated |
| `breakeven_months_total` | FLOAT64 | `google_ads_spend_aed / monthly_margin_total_aed` | Calculated |
| `breakeven_months_total_with_agency` | FLOAT64 | `(google_ads_spend_aed + 3600) / monthly_margin_total_aed` | Calculated |

### Critical Semantics
- **Cohort-based:** Revenue and activation are measured for the cohort acquired in month M, not total business metrics for month M
- **ALL grandparents included:** Counts ALL grandparents from `grandparent_account_created_date_and_first_order_delivered`, not just those with UTM attribution
- **Paid/Organic classification:** Uses `views.definition_paid_organic_channel` as source of truth. Rule: **What is NOT paid = Organic** (including unattributed)
- **Invoice-to-parent deduplication:** Revenue is deduplicated at the grandparent level to avoid counting the same invoice multiple times when children invoice to parent

### Dependency Tree
```
marketing_funnel_grandparent_monthly
├── views.quiqup_com_unique_visitors_monthly_2025_h2 (traffic, leads, spend)
├── views.grandparent_account_created_date_and_first_order_delivered (ALL grandparents, activation)
├── views.grandparent_utm_attribution (UTM attribution for ~50% of grandparents)
├── views.definition_paid_organic_channel (paid vs organic classification) ⭐ SOURCE OF TRUTH
└── views.grandparent_revenue (deduplicated lifetime revenue) ⭐ SOURCE OF TRUTH
```

### Break-Even Interpretation
| Value | Meaning |
|-------|---------|
| **< cohort_age_months** | Already broken even (profitable) |
| **= cohort_age_months** | Breaking even exactly now |
| **> cohort_age_months** | Not yet broken even (still recovering investment) |
| **Very high (50+)** | Unlikely to break even at current run-rate |

**Agency fee note:** 3,600 AED/month is the standard agency management fee. Include it for true cost analysis.

### Usage
```sql
-- Monthly cohort performance with break-even analysis
SELECT
  month,
  grandparents_acquired,
  gp_acquired_paid,
  gp_acquired_organic,

  -- Revenue & Margin
  cohort_lifetime_revenue_aed,
  cohort_margin_aed,
  cohort_margin_paid_aed,
  cohort_margin_organic_aed,

  -- Margin-based LTV (key profitability metric)
  ltv_margin_per_gp_acquired,
  ltv_margin_per_gp_acquired_paid,
  ltv_margin_per_gp_acquired_organic,

  google_ads_spend_aed,
  cohort_roi,

  -- Break-even analysis
  cohort_age_months,
  breakeven_months_paid,
  breakeven_months_paid_with_agency,
  breakeven_months_total,
  breakeven_months_total_with_agency
FROM views.marketing_funnel_grandparent_monthly
ORDER BY month

-- Campaign ROI analysis (drill down)
SELECT
  gua.attributed_utm_campaign,
  COUNT(DISTINCT gua.grandparent_account_id) AS gp_acquired,
  ROUND(SUM(gpr.total_revenue_aed), 0) AS lifetime_revenue,
  ROUND(SUM(gpr.total_revenue_aed) * 0.25, 0) AS lifetime_margin
FROM views.grandparent_utm_attribution gua
LEFT JOIN views.grandparent_revenue gpr
  ON gpr.grandparent_account_id = gua.grandparent_account_id
WHERE gua.acquisition_date >= '2025-07-01'
GROUP BY 1
ORDER BY 3 DESC
```

### Advanced: Campaign Break-Even with First 3 Months Margin

**Use case:** Compare campaigns across cohorts with different maturity (older cohorts had more time to generate revenue). Using first 3 months margin provides fair cross-cohort comparison.

**Formula:** `Break-Even Months = Spend ÷ (First 3 Months Revenue × 25% ÷ 3)`

**Key patterns:**
1. **Campaign deduplication:** Campaigns get renamed over time but keep same `campaign_id`. Use `ARRAY_AGG` to pick one name per campaign_id.
2. **Grandparent-to-accounts mapping:** Use `master_account_data_daily` where `grandparent_account_id` = GP, not Salesforce parent hierarchy.
3. **Activation filter:** Exclude `2030-01-01` placeholder dates (view uses this for non-activated).
4. **Invoice join:** Join through `invoicer_current.accounts` which has both `id` (STRING = SF ID) and `account_id` (INT64 = invoicer ID).

```sql
-- Campaign Break-Even Analysis (First 3 Months Margin)
-- Compares ROI across campaigns with different maturity

WITH campaign_latest_name AS (
  -- Dedupe campaigns: pick one name per campaign_id (longest name for full descriptor)
  SELECT
    campaign_id,
    ARRAY_AGG(campaign_name ORDER BY LENGTH(campaign_name) DESC LIMIT 1)[OFFSET(0)] AS campaign_name
  FROM `quiqup.google_ads_analytics.ads_Campaign_8350869641`
  GROUP BY campaign_id
),

gp_acquisition AS (
  SELECT
    gac.gac_grandparent_account_id AS gp_id,
    DATE_TRUNC(DATE(gac.gac_minimum_created_date), MONTH) AS cohort,
    CASE
      WHEN gac.gac_minimum_created_date < '2025-07-01' THEN 'H1 2025'
      ELSE 'H2 2025'
    END AS period,
    gam.google_ads_campaign AS campaign,
    gac.gac_grandparent_first_order_delivered AS activation_date
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  JOIN `quiqup.views.grandparent_utm_attribution` ua
    ON gac.gac_grandparent_account_id = ua.grandparent_account_id
  JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
    ON ua.attributed_utm_campaign = gam.utm_campaign
  WHERE gam.google_ads_campaign IS NOT NULL
    AND gac.gac_minimum_created_date >= '2025-01-01'
    AND gac.gac_minimum_created_date < '2026-01-01'
),

-- Filter to activated GPs only (exclude 2030-01-01 placeholder)
activated_gps AS (
  SELECT *
  FROM gp_acquisition
  WHERE activation_date IS NOT NULL
    AND DATE(activation_date) < '2026-01-01'
),

-- Get all account_ids under each grandparent (critical: use master_account_data_daily)
gp_accounts AS (
  SELECT DISTINCT
    grandparent_account_id AS gp_id,
    account_id
  FROM `quiqup.views.master_account_data_daily`
  WHERE grandparent_account_id IN (SELECT gp_id FROM activated_gps)
),

-- Calculate first 3 months revenue for each activated GP
first_3mo_revenue AS (
  SELECT
    ag.gp_id,
    ag.period,
    ag.campaign,
    SUM(i.total_amount - COALESCE(i.tax_amount, 0)) AS revenue_3mo
  FROM activated_gps ag
  JOIN gp_accounts ga ON ag.gp_id = ga.gp_id
  -- Join through invoicer accounts to bridge STRING SF ID → INT64 invoicer ID
  JOIN `quiqup.invoicer_current.accounts` ia
    ON ga.account_id = ia.id
    AND ia.record_deleted = FALSE
  JOIN `quiqup.invoicer_current.invoices` i
    ON ia.account_id = i.account_id
  WHERE i.record_deleted = FALSE
    AND i.state IN ('paid', 'overdue')
    AND i.start_date >= DATE(ag.activation_date)
    AND i.start_date < DATE_ADD(DATE(ag.activation_date), INTERVAL 3 MONTH)
  GROUP BY 1, 2, 3
),

-- Get spend by campaign for each period (uses campaign_id deduplication)
spend_by_campaign AS (
  SELECT
    cln.campaign_name AS campaign,
    CASE
      WHEN s.segments_date < '2025-07-01' THEN 'H1 2025'
      ELSE 'H2 2025'
    END AS period,
    SUM(s.metrics_cost_micros) / 1000000 AS spend_aed
  FROM `quiqup.google_ads_analytics.ads_CampaignBasicStats_8350869641` s
  JOIN campaign_latest_name cln ON s.campaign_id = cln.campaign_id
  WHERE s.segments_date >= '2025-01-01' AND s.segments_date < '2026-01-01'
  GROUP BY 1, 2
),

campaign_metrics AS (
  SELECT
    ag.period,
    ag.campaign,
    COUNT(DISTINCT ag.gp_id) AS activated_gps,
    SUM(COALESCE(r.revenue_3mo, 0)) AS total_revenue_3mo
  FROM activated_gps ag
  LEFT JOIN first_3mo_revenue r
    ON ag.gp_id = r.gp_id
    AND ag.period = r.period
    AND ag.campaign = r.campaign
  GROUP BY 1, 2
)

-- Final output with break-even calculation
SELECT
  cm.period,
  cm.campaign,
  cm.activated_gps AS gps,
  ROUND(s.spend_aed) AS spend,
  ROUND(cm.total_revenue_3mo * 0.25 / 3) AS monthly_margin,
  CASE
    WHEN cm.total_revenue_3mo * 0.25 / 3 > 0
    THEN ROUND(s.spend_aed / (cm.total_revenue_3mo * 0.25 / 3), 1)
    ELSE NULL
  END AS break_even_months
FROM campaign_metrics cm
JOIN spend_by_campaign s
  ON cm.campaign = s.campaign
  AND cm.period = s.period
WHERE cm.activated_gps >= 3  -- Exclude tiny sample sizes
ORDER BY cm.period, break_even_months NULLS LAST
```

**Field glossary:**
| Field | Source | Meaning |
|-------|--------|---------|
| `gac_grandparent_account_id` | `grandparent_account_created_date_and_first_order_delivered` | Unique business (GP = top-level account) |
| `gac_minimum_created_date` | Same | Acquisition date (first account created under GP) |
| `gac_grandparent_first_order_delivered` | Same | Activation date (first delivered order) |
| `attributed_utm_campaign` | `grandparent_utm_attribution` | UTM campaign that acquired this GP |
| `google_ads_campaign` | `definition_utm_google_ads_mapping` | Canonical Google Ads campaign name |
| `campaign_id` | `ads_Campaign_8350869641` | Stable campaign identifier (names change) |
| `metrics_cost_micros` | `ads_CampaignBasicStats` | Spend in micros (÷1M = AED) |
| `total_amount - tax_amount` | `invoicer_current.invoices` | Net revenue (excl VAT) |

---

### View: `quiqup.views.cac`
- **Row meaning (grain):** 1 row per account × week.
- **Purpose:** Weekly CAC = Google Ads spend ÷ activated clients (with a paid-only variant).
- **Key columns:**
  - `id` (STRING): Salesforce account ID
  - `created_week` (DATE): week (Monday) derived from `master_account_data_daily.earliest_created_date`
  - `account_lead_source_grouped_marketing` (STRING): marketing bucket (uae/ksa/marketplace/other)
  - `CAC`: spend ÷ activated clients (includes cohorts without paid UTMs)
  - `CAC_paid`: spend ÷ activated clients where paid attribution matches Google Ads
- **Interpretation note:** Activation is lagged; very recent cohorts can look inflated until activation "catches up".
- **Uses:** `views.definition_campaign_marketing_bucket` for campaign → bucket mapping.

### View: `quiqup.views.definition_campaign_marketing_bucket`
- **Row meaning (grain):** 1 row per Google Ads campaign name.
- **Purpose:** Canonical mapping of campaign_name → marketing bucket (uae/ksa/marketplace/other).
- **Key columns:**
  - `campaign_name` (STRING): Google Ads campaign name
  - `marketing_bucket` (STRING): uae, ksa, marketplace
- **Coverage:** 35 campaigns (31 uae, 3 ksa, 1 marketplace); unmapped campaigns default to "other".
- **Pattern-based inclusions:** Campaigns matching `GL_QQP_GA_SEM%` or `GL_QQP_GA_MAX%` are auto-included as "uae".
- **Usage:**
```sql
SELECT camp.campaign_name, COALESCE(bucket.marketing_bucket, 'other') as bucket
FROM google_ads_analytics.ads_Campaign_8350869641 camp
LEFT JOIN views.definition_campaign_marketing_bucket bucket
  ON camp.campaign_name = bucket.campaign_name
WHERE camp._DATA_DATE = camp._LATEST_DATE
```

### View: `quiqup.views.definition_utm_google_ads_mapping`
- **Row meaning (grain):** 1 row per UTM campaign value (definition mapping).
- **Purpose:** Maps Salesforce UTM campaigns to Google Ads campaign/ad group for spend attribution.
- **Key columns:**
  - `utm_campaign` (STRING): UTM value found in Salesforce (primary key)
  - `google_ads_campaign` (STRING): Matching Google Ads campaign name
  - `google_ads_ad_group` (STRING): Matching ad group (NULL for PMax/campaign-level)
  - `marketing_bucket` (STRING): uae, ksa, marketplace
  - `campaign_type` (STRING): search, pmax, demandgen, meta, internal, content, direct
- **Coverage:** 48 UTM patterns mapped (36 Google Ads, 5 Meta, 7 other).
- **Usage:**
```sql
-- Join leads to mapping
SELECT l.id, l.utm_campaign_c, m.google_ads_campaign, m.google_ads_ad_group
FROM salesforce_current.leads l
LEFT JOIN views.definition_utm_google_ads_mapping m
  ON l.utm_campaign_c = m.utm_campaign

-- Filter to Google Ads only
WHERE m.campaign_type IN ('search', 'pmax', 'demandgen')
```

### View: `quiqup.views.account_utm_attribution`
- **Row meaning (grain):** 1 row per Salesforce account with attributed UTM data.
- **Purpose:** Earliest-first UTM attribution across Lead → Opportunity → Account hierarchy.
- **Total coverage:** 11,695 accounts attributed (31% of all accounts).
- **Key columns:**
  - `account_id` (STRING): Salesforce account ID (join key)
  - `attributed_from_object` (STRING): Source object type — `account`, `lead`, or `opportunity`
  - `attributed_from_id` (STRING): ID of the source object
  - `attributed_object_created_date` (TIMESTAMP): When the attributed object was created
  - `attributed_utm_campaign` (STRING): UTM campaign value
  - `attributed_utm_source` (STRING): UTM source value
  - `attributed_utm_medium` (STRING): UTM medium value
  - `attributed_utm_content` (STRING): UTM content value
  - `attributed_utm_term` (STRING): UTM term value
- **Attribution breakdown:**
  | Source | Accounts | Unique Campaigns |
  |--------|----------|------------------|
  | Account | 10,946 | 65 |
  | Lead | 739 | 57 |
  | Opportunity | 10 | 5 |
- **Logic:**
  1. Collects UTM data from accounts, opportunities, and converted leads
  2. For leads: uses `COALESCE(utm_*, pi_utm_*)` (Pardot fallback)
  3. Ranks by `created_date` ascending
  4. Returns the earliest object with UTM data per account
- **Usage:**
```sql
-- Join attribution to accounts
SELECT
  a.id,
  a.name,
  attr.attributed_utm_campaign,
  attr.attributed_from_object
FROM salesforce_current.accounts a
LEFT JOIN views.account_utm_attribution attr
  ON a.id = attr.account_id
WHERE a.is_deleted = FALSE

-- Campaign performance with attribution source
SELECT
  attr.attributed_utm_campaign,
  attr.attributed_from_object,
  COUNT(DISTINCT a.id) AS accounts
FROM salesforce_current.accounts a
JOIN views.account_utm_attribution attr ON a.id = attr.account_id
GROUP BY 1, 2
ORDER BY 3 DESC
```
- **Documentation:** See `knowledge_base/utm_attribution_logic.md` for full SQL and edge cases.

### View: `quiqup.views.grandparent_utm_attribution`
- **Row meaning (grain):** 1 row per grandparent account with attributed UTM data.
- **Purpose:** Earliest-first UTM attribution rolled up to grandparent level. Used for cohort-based marketing analysis where 1 grandparent = 1 acquisition.
- **Key columns:**
  - `grandparent_account_id` (STRING): Salesforce ID of the grandparent account (join key)
  - `grandparent_account_name` (STRING): Name of the grandparent
  - `acquisition_date` (DATE): Earliest created_date across all accounts in the grandparent hierarchy
  - `attributed_utm_campaign`, `attributed_utm_source`, `attributed_utm_medium` (STRING): UTM values from earliest attribution
  - `attributed_from_object` (STRING): Source type — `account`, `lead`, or `opportunity`
  - `attributed_from_id` (STRING): ID of the source object
- **Critical semantics:**
  - **SSUP Exception:** Self-signup accounts (parent `0010800003I4PcsAAF` with 21,563 children) are treated as their own grandparents
  - Uses `views.true_grandparent_account` to handle hierarchy correctly
  - Attribution is inherited from child accounts via `views.account_utm_attribution`
- **🚨 CRITICAL GOTCHA: This view ONLY contains ACTIVATED grandparents!**
  - All grandparents in this view have `gac_grandparent_first_order_delivered IS NOT NULL`
  - **DO NOT use this view to calculate activation rates** — you will always get 100%
  - For activation rate analysis, use `account_utm_attribution` + `salesforce_current.accounts` as source, then LEFT JOIN to `grandparent_account_created_date_and_first_order_delivered` to determine activation status
  - Example correct pattern:
  ```sql
  -- CORRECT: Get ALL accounts, then check activation
  SELECT
    a.id AS account_id,
    gac.gac_grandparent_account_id IS NOT NULL AS is_activated
  FROM salesforce_current.accounts a
  JOIN views.account_utm_attribution ua ON a.id = ua.account_id
  LEFT JOIN views.grandparent_account_created_date_and_first_order_delivered gac
    ON a.id = gac.gac_grandparent_account_id
  WHERE ua.attributed_utm_medium = 'cpc'

  -- WRONG: This will show 100% activation (only activated GPs are in the view)
  SELECT gua.grandparent_account_id, gac.gac_grandparent_first_order_delivered IS NOT NULL AS is_activated
  FROM views.grandparent_utm_attribution gua
  LEFT JOIN views.grandparent_account_created_date_and_first_order_delivered gac
    ON gua.grandparent_account_id = gac.gac_grandparent_account_id
  ```
- **⚠️ Paid channel identification:**
  - **Google Ads paid traffic:** `attributed_utm_medium = 'cpc'`
  - **Organic Google traffic:** `attributed_utm_medium IN ('organic', '(none)')` with `attributed_utm_source = 'google'`
  - Always filter by `attributed_utm_medium = 'cpc'` when calculating ROI for paid campaigns
- **Usage:**
```sql
-- Cohort analysis by acquisition month (ALL traffic)
SELECT
  DATE_TRUNC(acquisition_date, MONTH) AS cohort_month,
  attributed_utm_campaign,
  COUNT(DISTINCT grandparent_account_id) AS grandparents_acquired
FROM views.grandparent_utm_attribution
WHERE acquisition_date >= '2025-07-01'
GROUP BY 1, 2
ORDER BY 1, 3 DESC

-- PAID ONLY cohort analysis (Google Ads)
SELECT
  DATE_TRUNC(acquisition_date, MONTH) AS cohort_month,
  attributed_utm_campaign,
  COUNT(DISTINCT grandparent_account_id) AS grandparents_acquired
FROM views.grandparent_utm_attribution
WHERE acquisition_date >= '2025-07-01'
  AND attributed_utm_medium = 'cpc'  -- PAID ONLY
GROUP BY 1, 2
ORDER BY 1, 3 DESC
```

### View: `quiqup.views.grandparent_revenue`
- **Row meaning (grain):** 1 row per grandparent account with deduplicated lifetime revenue.
- **Purpose:** Aggregates invoice revenue at grandparent level, avoiding double-counting when children invoice to parent.
- **Key columns:**
  - `grandparent_account_id` (STRING): Salesforce ID of the grandparent (join key)
  - `total_revenue_aed` (FLOAT64): Total recognized revenue (excludes void/cancelled/draft invoices)
  - `total_invoices` (INT64): Count of distinct invoices
- **Critical semantics:**
  - **Invoice-to-parent deduplication:** When `invoice_to_parent = TRUE`, invoices go to parent_account_id. This view deduplicates by `effective_invoicing_account` before summing.
  - Without deduplication, revenue can be inflated ~19x for hierarchical accounts
  - Revenue filter: `state NOT IN ('void', 'cancelled', 'draft')` and `record_deleted = FALSE`
- **Usage:**
```sql
-- Join with attribution for campaign LTV
SELECT
  gua.attributed_utm_campaign,
  COUNT(DISTINCT gua.grandparent_account_id) AS gp_count,
  ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)), 0) AS lifetime_revenue_aed
FROM views.grandparent_utm_attribution gua
LEFT JOIN views.grandparent_revenue gpr
  ON gpr.grandparent_account_id = gua.grandparent_account_id
GROUP BY 1
ORDER BY 3 DESC
```

### View: `quiqup.views.account_lead_source_attribution`
- **Row meaning (grain):** 1 row per Salesforce account with attributed lead source.
- **Purpose:** Earliest-first lead source attribution per account. Mirrors `account_utm_attribution` logic but for the `lead_source` / `account_source` field instead of UTM parameters.
- **Key columns:**
  - `account_id` (STRING): Salesforce account ID (join key)
  - `attributed_from_object` (STRING): Source type — `account`, `lead`, or `opportunity`
  - `attributed_from_id` (STRING): ID of the source object
  - `attributed_object_created_date` (TIMESTAMP): When the attributed object was created
  - `attributed_lead_source` (STRING): The lead source value (e.g., "Inbound: Contact form", "Outbound: Own research")
- **Attribution logic:**
  - Collects `account_source` (accounts), `lead_source` (opportunities), `lead_source` (converted leads)
  - Picks the **earliest created** object — same earliest-first pattern as UTM attribution
  - Lead sources only from converted leads (`converted_account_id IS NOT NULL`)
- **Coverage:** 27,299 accounts (71.6%) — significantly better than UTM attribution (31%)
- **Attribution breakdown:**
  | Source Object | Accounts | Distinct Sources |
  |--------------|----------|------------------|
  | Account | 22,175 | 25 |
  | Lead | 4,541 | 51 |
  | Opportunity | 583 | 29 |
- **Usage:**
```sql
-- Join to definition for source_group
SELECT
  alsa.attributed_lead_source,
  dls.source_group,
  COUNT(*) AS accounts
FROM views.account_lead_source_attribution alsa
LEFT JOIN views.definition_lead_source dls
  ON alsa.attributed_lead_source = dls.lead_source
GROUP BY 1, 2
ORDER BY 3 DESC
```

### View: `quiqup.views.grandparent_lead_source_attribution`
- **Row meaning (grain):** 1 row per grandparent account with attributed lead source.
- **Purpose:** Earliest-first lead source attribution rolled up to grandparent level via `true_grandparent_account`. Mirrors `grandparent_utm_attribution` but for lead source. Pre-joins `definition_lead_source` for convenience.
- **Key columns:**
  - `grandparent_account_id` (STRING): Salesforce ID of the grandparent (join key)
  - `grandparent_account_name` (STRING): Name of the grandparent
  - `acquisition_date` (DATE): Date of the earliest attributed object in the GP hierarchy
  - `attributed_lead_source` (STRING): The lead source value
  - `attributed_from_object` (STRING): Source type — `account`, `lead`, or `opportunity`
  - `attributed_from_id` (STRING): ID of the source object
  - `source_group` (STRING): Pre-joined from `definition_lead_source` — Inbound/Outbound/Old
  - `is_website_source` (BOOL): Pre-joined flag
  - `is_contact_form` (BOOL): Pre-joined flag
- **Coverage:** 23,992 grandparents — 2.1x better than UTM GP attribution (11,206)
- **GP breakdown by source_group:**
  | Source Group | GPs |
  |-------------|-----|
  | Inbound | 23,210 |
  | Outbound | 730 |
  | Old | 35 |
- **Critical semantics:**
  - Hierarchy resolved via `views.true_grandparent_account` (same SSUP handling)
  - Unlike `grandparent_utm_attribution`, this view includes **all GPs with any lead source** (not limited to activated only)
  - `source_group` is pre-joined — no need to separately join `definition_lead_source`
- **Usage:**
```sql
-- Grandparent revenue by source_group (Inbound vs Outbound)
SELECT
  gls.source_group,
  COUNT(DISTINCT gls.grandparent_account_id) AS gp_count,
  ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)), 0) AS lifetime_revenue
FROM views.grandparent_lead_source_attribution gls
LEFT JOIN views.grandparent_revenue gpr
  ON gls.grandparent_account_id = gpr.grandparent_account_id
GROUP BY 1
ORDER BY 3 DESC

-- Cohort analysis by acquisition month and source_group
SELECT
  DATE_TRUNC(gls.acquisition_date, MONTH) AS cohort_month,
  gls.source_group,
  COUNT(DISTINCT gls.grandparent_account_id) AS gps_acquired
FROM views.grandparent_lead_source_attribution gls
WHERE gls.acquisition_date >= '2025-07-01'
GROUP BY 1, 2
ORDER BY 1, 3 DESC
```

### View: `quiqup.views.google_ads_spend_monthly`
- **Row meaning (grain):** 1 row per month × campaign × ad group.
- **Purpose:** Pre-aggregated monthly Google Ads spend for easy joins with Salesforce data.
- **Key columns:**
  - `month` (DATE): First day of month
  - `google_ads_campaign` (STRING): Campaign name
  - `google_ads_ad_group` (STRING): Ad group name (NULL for Performance Max)
  - `clicks` (INT64): Monthly clicks
  - `impressions` (INT64): Monthly impressions
  - `spend_aed` (FLOAT64): Monthly spend in AED
  - `conversions` (FLOAT64): Monthly conversions
- **Includes:** Both ad group level (search/demandgen) and campaign level (Performance Max).
- **Usage:**
```sql
-- Get monthly spend by campaign
SELECT month, google_ads_campaign, SUM(spend_aed) as spend
FROM views.google_ads_spend_monthly
GROUP BY 1, 2

-- Join with leads via UTM mapping
SELECT
  l.id, l.created_date, m.google_ads_campaign, s.spend_aed
FROM salesforce_current.leads l
LEFT JOIN views.definition_utm_google_ads_mapping m
  ON l.utm_campaign_c = m.utm_campaign
LEFT JOIN views.google_ads_spend_monthly s
  ON m.google_ads_campaign = s.google_ads_campaign
  AND (m.google_ads_ad_group = s.google_ads_ad_group
       OR (m.google_ads_ad_group IS NULL AND s.google_ads_ad_group IS NULL))
  AND DATE_TRUNC(DATE(l.created_date), MONTH) = s.month
WHERE m.campaign_type IN ('search', 'pmax', 'demandgen')
```

### View: `quiqup.views.ga4_traffic_classified_sessions_quiqup_com`
- **Row meaning (grain):** 1 row per session (user_pseudo_id × ga_session_id × month).
- **Purpose:** **Core traffic classification view** — classifies each session as paid/organic and Google Ads/non-Google Ads.
- **Key columns:**
  - `month` (DATE): Month of the session
  - `user_pseudo_id` (STRING): GA4 user ID
  - `ga_session_id` (STRING): GA4 session ID
  - `has_click_id` (BOOL): TRUE if session has gclid, wbraid, or gbraid
  - `is_paid_session` (BOOL): TRUE if paid traffic (see classification logic above)
  - `is_google_ads_session` (BOOL): TRUE if Google Ads specifically
- **Exclusions:** Tracking banner experiment sessions are filtered out.
- **Usage:**
```sql
-- Get paid vs organic session counts by month
SELECT month,
  COUNTIF(is_paid_session) AS paid_sessions,
  COUNTIF(NOT is_paid_session) AS organic_sessions
FROM views.ga4_traffic_classified_sessions_quiqup_com
GROUP BY 1
```

### Table: `quiqup.views.definition_traffic_channel`
- **Row meaning (grain):** 1 row per source/medium combination.
- **Purpose:** Maps UTM source/medium to channel groups for traffic classification.
- **Key columns:**
  - `source_key` (STRING): UTM source value (lowercase)
  - `medium_key` (STRING): UTM medium value (lowercase)
  - `channel_group` (STRING): Classification — 'Paid Search', 'Paid Social', 'Email', 'Referral', 'Content', etc.
  - `owner` (STRING): Team responsible (usually 'Marketing')
- **Channel groups that indicate paid:** Any `channel_group` starting with 'Paid' (e.g., 'Paid Search', 'Paid Social')
- **Special value:** `channel_group = 'Exclude - Internal Banner Experiment'` for `trackingpage/banner` traffic

### Other notable views (light semantics)
- `quiqup.views.definition_high_intent_website_visitor`
  - **Row meaning:** 1 qualifying page view / event.
  - **Key columns:** `event_date`, `event_datetime`, `user_pseudo_id`, `page_location`, `path`, `high_intent_reason`.
  - **Purpose:** Single source of truth for "high-intent visitor" classification.
- `quiqup.views.salesforce_leads_monthly`
  - **Row meaning:** 1 row per month with lead counts at various cleaning stages.
  - **Key columns:**
    - `sf_contact_form_leads_raw`: Raw count from Salesforce
    - `sf_contact_form_website_source_leads_raw`: Website-source leads (raw)
    - `sf_contact_form_leads_valid`: Leads with valid email or phone
    - `sf_contact_form_website_source_leads_deduped`: **Recommended metric** — valid + deduplicated
  - **Deduplication logic:** Uses `dedupe_key` to merge duplicates (same email/phone).
- `quiqup.views.ga4_excluded_users_tracking_banner_monthly`
  - **Row meaning:** 1 row per user_pseudo_id × month who should be excluded.
  - **Purpose:** Users who came via tracking banner experiment (`utm_source=trackingpage` + `utm_medium=banner`) — excluded from all funnel metrics.
- `quiqup.views.opportunities_convert_minus_2months`
  - **Row meaning:** 1 opportunity cohort row with a +2 month reporting offset.
  - **Purpose:** "Opportunity → Account conversion within 2 months" (uses parent account created date).
  - **Key columns:** `converted_by_reporting_month` (2-month windowed, for dashboard), `is_converted` (all-time: parent exists + not Deal Lost, no time window), `conversion_date` (actual parent creation date).
- `quiqup.views.accounts_convert_minus_2months`
  - **Row meaning:** 1 account cohort row with conversion measured via delivered-order activation at grandparent level.

---

## Dataset: `ex_api_current` (Operational API Data)

### Table: `ex_api_current.orders`
- **Row meaning (grain):** 1 order (current-state snapshot).
- **Key columns:**
  - `client_order_id` (STRING): stable external order id.
  - `business_partner_id` (STRING): links to `ex_api_current.business_accounts.id`.
  - `state` (STRING): **current** order state only.
  - `inserted_at` (TIMESTAMP): order creation timestamp.
  - `updated_at` (TIMESTAMP): commonly used as a partition field.
  - `record_deleted` (BOOL): soft delete flag.
- **Important:** Use `order_state_changes` for historical state transitions; `orders.state` is not historical.

### Table: `ex_api_current.business_accounts`
- **Row meaning (grain):** 1 business account / client entity in operational system.
- **Key columns:** `id` (STRING), `name` (STRING), `billing_country` (STRING), `record_deleted` (BOOL).
- **Relationship:** `orders.business_partner_id = business_accounts.id`.
- **Bridge field (cohorts):** `business_accounts.external_id` (STRING) can be used to bridge to `views.master_account_data_daily.external_id` (INT64, cast to STRING).

### Table: `ex_api_current.order_state_changes`
- **Row meaning (grain):** 1 state transition record per order event.
- **Key columns:** `client_order_id`, `internal_order_id`, `state`, `on_hold_reason`, `inserted_at`, `occurred_at`.
- **Relationship:** join to `orders` via `client_order_id`.
- **Semantics:** Use this table to determine whether/when an order was in a given state during a period.

### Table: `ex_api_current.order_address_changes`
- **Row meaning (grain):** 1 address change event for an order.
- **Key columns:** `client_order_id`, address fields, `occurred_at`, `author`.
- **Relationship:** joins to `order_state_changes` and `orders` via `client_order_id`.

---

## Dataset: `invoicer_current` (Invoicing)

### Table: `invoicer_current.accounts` (27K rows)
- **Row meaning (grain):** 1 invoicing account record.
- **Key columns:**
  - `id` (STRING): Salesforce ID format (e.g., "0010800002ppRMpAAM")
  - `account_id` (INTEGER): Internal numeric ID — **use this for joins to invoices**
  - `salesforce_id` (STRING): Salesforce account ID
  - `account_name` (STRING): Account display name
  - **Hierarchy fields:**
    - `parent_account_id` (INTEGER): Numeric ID of parent account
    - `parent_account_name` (STRING)
    - `parent_salesforce_id` (STRING): Salesforce ID of parent
    - `grandparent_account_name` (STRING)
    - `grandparent_salesforce_id` (STRING): Salesforce ID of grandparent
  - `invoice_to_parent` (BOOLEAN): **CRITICAL** — if TRUE, invoices go to parent
  - `net_balance` (FLOAT): Current account balance
  - `payment_terms` (INTEGER): Payment terms in days

### Table: `invoicer_current.invoices` (120K rows)
- **Row meaning (grain):** 1 invoice record.
- **Partitioned by:** `updated_at` (MONTH)
- **Key columns:**
  - `id` (INTEGER): Invoice ID — **use for joins to invoice_lines**
  - `account_id` (INTEGER): Links to `accounts.account_id` (NOT the string ID!)
  - `invoice_number` (STRING): e.g., "INV-121268"
  - `start_date`, `end_date` (DATE): Billing period
  - `total_amount` (FLOAT): Invoice total in currency
  - `balance` (FLOAT): Remaining balance (0 if paid)
  - `state` (STRING): e.g., "paid", "void", "draft"
  - `currency` (STRING): Lowercase, e.g., "aed"
  - `tax_amount` (FLOAT): VAT amount
  - `created_at` (TIMESTAMP): Invoice creation date
  - `deleted_at` (TIMESTAMP): Soft delete timestamp
  - `record_deleted` (BOOLEAN): Soft delete flag

### Table: `invoicer_current.invoice_lines` (13M rows)
- **Row meaning (grain):** 1 line item on an invoice.
- **Partitioned by:** `updated_at` (MONTH)
- **Key columns:**
  - `id` (INTEGER): Line item ID
  - `invoice_id` (INTEGER): Links to `invoices.id`
  - `order_id` (INTEGER): Links to order that generated this charge
  - `description` (STRING): Service/product description
  - `quantity` (FLOAT): Units
  - `type` (STRING): Line item type
  - `amount` (FLOAT): Line total (excl. tax)
  - `tax_amount` (FLOAT): Tax for this line

### Table: `invoicer_current.credit_notes` (49K rows)
- **Row meaning (grain):** 1 credit note (money returned to client).
- **Partitioned by:** `created_at` (MONTH)
- **Key columns:**
  - `id` (INTEGER): Credit note ID
  - `account_id` (INTEGER): Links to `accounts.account_id`
  - `invoice_id` (INTEGER): Links to `invoices.id` (if applied to specific invoice)
  - `creditnote_number` (STRING): e.g., "CN-12345"
  - `amount` (FLOAT): Credit amount
  - `state` (STRING): Credit note status
  - `date` (DATE): Credit note date
- **Use case:** Typically for Cash on Delivery (COD) refunds.

### Table: `invoicer_current.forecast_invoice_lines` (13M rows)
- **Row meaning (grain):** 1 forecasted line item (not yet invoiced).
- **Partitioned by:** `created_at` (MONTH)
- **Key columns:**
  - `id` (INTEGER): Forecast line ID
  - `order_id` (INTEGER): Links to order
  - `description` (STRING): Service description
  - `quantity` (FLOAT): Units
  - `type` (STRING): Line item type
  - `amount` (FLOAT): Expected amount
  - `tax_amount` (FLOAT): Expected tax
- **Note:** No `invoice_id` — these become invoice_lines when invoice is issued.

### Invoice-to-Parent Join Pattern

**⚠️ CRITICAL: When querying invoices for a specific account, you MUST check `invoice_to_parent`**

```sql
-- CORRECT: Get invoices for an account, handling invoice_to_parent
SELECT i.*
FROM invoicer_current.accounts a
JOIN invoicer_current.invoices i
  ON i.account_id = CASE
       WHEN a.invoice_to_parent = TRUE THEN a.parent_account_id
       ELSE a.account_id
     END
WHERE a.salesforce_id = '001P4000006ruBuIAI'
  AND i.record_deleted = FALSE
  AND i.deleted_at IS NULL
ORDER BY i.end_date DESC

-- WRONG: Directly joining on account_id ignores invoice_to_parent
SELECT i.*
FROM invoicer_current.accounts a
JOIN invoicer_current.invoices i ON i.account_id = a.account_id  -- WRONG!
WHERE a.salesforce_id = '001P4000006ruBuIAI'
```

### Canonical Join Keys

| From | To | Join Key |
|------|----|----|
| `invoicer_current.accounts` | `invoicer_current.invoices` | `accounts.account_id = invoices.account_id` (or `parent_account_id` if `invoice_to_parent = TRUE`) |
| `invoicer_current.invoices` | `invoicer_current.invoice_lines` | `invoices.id = invoice_lines.invoice_id` |
| `invoicer_current.accounts` | `salesforce_current.accounts` | `accounts.salesforce_id = sf_accounts.id` |
| `invoicer_current.invoices` | `views.master_account_data_daily` | `invoices.account_id = master.external_id` |

### Data Quality Notes

1. **Currency:** All invoices are in AED (lowercase "aed" in data)
2. **Soft deletes:** Always filter `record_deleted = FALSE AND deleted_at IS NULL`
3. **State values:** Common states are "paid", "void", "draft", "sent"
4. **Balance = 0:** Indicates fully paid invoice
5. **Revenue definitions:**
   - **Recognized revenue (default):** `state NOT IN ('void', 'cancelled', 'draft')` — includes paid + sent invoices
   - **Cash collected:** `state = 'paid'` — only fully paid invoices
   - **Exclude:** `void` (reversed), `cancelled` (never issued), `draft` (not finalized)
6. **Margin & ROI calculations:**
   - **Gross margin:** `margin = revenue × 0.25` (25% margin rate)
   - **ROI formula:** `ROI = (margin - spend) / spend × 100`
   - Example: Revenue 100K AED → Margin 25K AED; Spend 10K AED → ROI = (25K - 10K) / 10K × 100 = 150%

7. **⚠️ CRITICAL: Date Filtering for Monthly Revenue (Xero/Finance Reconciliation)**

   When querying monthly revenue that needs to match Finance/Xero reports, **use `start_date` NOT `end_date`**:

   | Date Field | Meaning | When to Use |
   |------------|---------|-------------|
   | `start_date` | Billing period START (e.g., Aug 1) | **Finance reconciliation** — matches Xero invoice date |
   | `end_date` | Billing period END (e.g., Sep 1) | Revenue recognition timing |

   **Example: August 2025 invoices for Finance reconciliation**
   ```sql
   -- ✅ CORRECT: Matches Finance/Xero (filters by billing period start)
   SELECT SUM(total_amount - COALESCE(tax_amount, 0)) as net_revenue
   FROM invoicer_current.invoices
   WHERE start_date >= '2025-08-01' AND start_date < '2025-09-01'
     AND state IN ('paid', 'overdue')
     AND record_deleted = FALSE

   -- ❌ WRONG: Will include July billing period invoices (end_date = Aug 1)
   --          and exclude August billing period invoices (end_date = Sep 1)
   SELECT SUM(total_amount - COALESCE(tax_amount, 0)) as net_revenue
   FROM invoicer_current.invoices
   WHERE end_date >= '2025-08-01' AND end_date < '2025-09-01'
   ```

   **Root cause:** Finance exports from Xero are based on invoice issue date (which aligns with `start_date`), while BigQuery `end_date` represents when the billing period ends.

   **Discovered:** January 2026 — reconciling August 2025 revenue showed AED 205K discrepancy until date filter was corrected.

---

## Dataset: `salesforce_current` (CRM)

### Table: `salesforce_current.accounts`
- **Row meaning (grain):** 1 Salesforce account.
- **Key columns:**
  - `id` (STRING)
  - `name` (STRING)
  - `created_date` (TIMESTAMP)
  - `client_type_c` (STRING/NULL): **NULL indicates business** (filter `client_type_c IS NULL` for business accounts).
  - `account_source` (STRING): e.g., "Inbound: Self-signup", "Inbound: Contact form".
  - Attribution fields: `utm_campaign_c`, `UTM_Source_c`, `UTM_Medium_c`
  - Activation/onboarding signals: `external_id_c`, `first_order_delivered_c`, `last_order_delivered_c`, `activated_timestamp_c`, `login_sent_c`, `signup_whats_app_sent_c`
  - Pricing model: `Pricing_Model_c`

**⚠️ CRITICAL: B2B Analysis Must Filter for Business Accounts**

The `accounts` table contains BOTH business (B2B) and individual (B2C) accounts. For any B2B funnel or marketing analysis, you **MUST** filter:

```sql
WHERE client_type_c IS NULL  -- Business accounts only
  AND is_deleted = FALSE
```

**`client_type_c` values:**
| Value | Meaning | 2025 Count |
|-------|---------|------------|
| `NULL` | **Business (B2B)** | ~5,400 |
| `Individual` | B2C / Personal users | ~6,300 |
| `Business` | Legacy (rare) | ~5 |
| `Personal` | Legacy (rare) | ~2 |

**Example — Self-signup accounts (CORRECT):**
```sql
-- Business self-signup accounts only
SELECT COUNT(*)
FROM salesforce_current.accounts
WHERE account_source = 'Inbound: Self-signup'
  AND client_type_c IS NULL  -- ⚠️ REQUIRED for B2B
  AND is_deleted = FALSE
  AND EXTRACT(YEAR FROM created_date) = 2025
-- Returns: ~5,400 (not ~11,600 which includes Individual)
```

### Table: `salesforce_current.leads`
- **Row meaning (grain):** 1 Salesforce lead record.
- **Key columns:**
  - `id` (STRING)
  - `created_date` (TIMESTAMP)
  - `lead_source` (STRING): map to `views.definition_lead_source.lead_source`.
  - `email`, `phone` (STRING): often used for de-duplication and linking.
  - **UTM attribution fields (for spend attribution):**
    - `utm_campaign_c`, `utm_source_c`, `utm_medium_c`, `utm_content_c`, `utm_term_c` (STRING)
    - `pi_utm_campaign_c`, `pi_utm_source_c`, `pi_utm_medium_c` (STRING): Pardot UTM fields
  - Volume expectation fields (STRING): `numberof_daily_deliveries_c`, `expected_deliveries_per_day_c`, `expected_monthly_volume_pardot_c`
  - Disqualification field: `reason_for_disqualification_c` (STRING)
  - **Conversion FK:** `converted_opportunity_id` (STRING): links directly to `salesforce_current.opportunities.id` when converted.

**Lead-level spend attribution:**
```sql
-- Link lead to Google Ads campaign via UTM
SELECT
  l.id as lead_id,
  l.utm_campaign_c,
  l.created_date,
  camp.campaign_name,
  ag.ad_group_name
FROM salesforce_current.leads l
LEFT JOIN google_ads_analytics.ads_Campaign_8350869641 camp
  ON camp._DATA_DATE = camp._LATEST_DATE
LEFT JOIN google_ads_analytics.ads_AdGroup_8350869641 ag
  ON ag.campaign_id = camp.campaign_id AND ag._DATA_DATE = ag._LATEST_DATE
WHERE l.utm_campaign_c = CONCAT(
  REPLACE(REPLACE(camp.campaign_name, ' - ', '_'), ' ', '-'),
  '_',
  REPLACE(ag.ad_group_name, ' ', '-')
)
```

### Table: `salesforce_current.opportunities`
- **Row meaning (grain):** 1 Salesforce opportunity.
- **Key columns:** `id`, `account_id`, `name`, `created_date`, `stage_name`, `is_deleted`, `is_won`, `is_closed`.
- **Diagnostics fields (examples):** `pricing_model_status_c`, `client_classification_c`, `reason_for_closed_lost_c`, `opportunity_was_lost_due_to_pricing_c`, `onboarding_status_c`, `kyc_complete_c`, `deal_done_timestamp_c`.
- **Lead relationship:** `salesforce_current.leads.converted_opportunity_id = opportunities.id`.

### Table: `salesforce_current.tasks` (Email activities)
- **Row meaning (grain):** 1 Salesforce task record (including email activity).
- **Email filter:** `task_subtype = 'Email'`.
- **Key columns:** `id`, `created_date`, `task_subtype`, `what_id`, `who_id`, `description`, `created_by_id`.
- **Relationships:**
  - `tasks.what_id` can reference `opportunities.id` (join when analyzing email sequences on opportunities).
  - `tasks.who_id` references the person entity (Lead/Contact).
  - Email body and headers often live in `tasks.description` as plain text.

### Table: `salesforce_current.users`
- **Row meaning (grain):** 1 Salesforce user.
- **Relationship:** join to `opportunities.owner_id` or `tasks.created_by_id` for owner/sender metadata.

### Table: `salesforce_current.pricing_models`
- **Row meaning (grain):** 1 pricing model definition.
- **Primary key:** `id` (matches `views.master_account_data_daily.pricing_model`).
- **Key columns:**
  - `name` / `name_c` (STRING): human-friendly name (prefer `name_c` when present).
  - Pricing fields stored as STRING (examples): `next_day_from_emirates_c`, `next_day_other_emirates_c`, `same_day_from_emirates_c`, `same_day_other_emirates_c`.

---

## Dataset: `bi_reporting` (BI Layer / Ops Reporting)

### View/Table: `bi_reporting.sales_funnel`
- **Row meaning (grain):** 1 sales funnel entity row (combined Leads + Opportunities + Accounts).
- **Key columns:** `client_name`, `account_id`, `lead_id`, `opportunity_id`, `client_classification`, `isactive`.

### Table: `bi_reporting.missions`
- **Row meaning (grain):** 1 mission.
- **Key columns:** `id`, `mission_date_utc`, `last_attempted_by_courier_id`.

### Table: `bi_reporting.internal_orders`
- **Row meaning (grain):** link between missions and orders.
- **Key columns:** `mission_id`, `client_order_id`, `state`, `type` (filter to delivery orders when relevant).

### Table: `bi_reporting.client_orders`
- **Row meaning (grain):** 1 order record in BI layer.
- **Key columns:** `id`, `state_updated_at` (delivery timestamp analysis).

### Table: `bi_reporting.couriers`
- **Row meaning (grain):** 1 courier.
- **Key columns:** `id`, `email`, `firstname`, `lastname`.

---

## Dataset: `google_ads_analytics` (Google Ads Raw Transfer)

### Table: `google_ads_analytics.ads_CampaignStats_8350869641`
- **Row meaning (grain):** 1 campaign metric record per date (and other dimensions, depending on connector schema).
- **Key columns (common):**
  - `metrics_cost_micros` (INT64): divide by 1,000,000 to get spend in currency units.
  - `metrics_clicks` (INT64)
  - `metrics_impressions` (INT64)
  - `metrics_conversions` (FLOAT64/NUMERIC depending on schema)

### Other common tables
- `ads_AccountStats_8350869641` (account-level aggregation)
- `ads_AdGroupStats_8350869641` (ad group level)
- `ads_BudgetStats_8350869641` (budget utilization)

### Table: `google_ads_analytics.ads_Campaign_8350869641`
- **Row meaning (grain):** 1 campaign definition **per day** (historical snapshots).
- **Key columns:** `campaign_id` (INT64), `campaign_name` (STRING), `campaign_status` (STRING), `campaign_start_date` (DATE), `_DATA_DATE` (DATE), `_LATEST_DATE` (DATE).
- **⚠️ CRITICAL: Dimension table deduplication required!**
  - This table contains historical snapshots (22K+ rows for 39 campaigns).
  - **Always filter:** `WHERE _DATA_DATE = _LATEST_DATE` to get current snapshot.
  - Failure to filter causes cartesian products and inflated metrics.

### Table: `google_ads_analytics.ads_AdGroup_8350869641`
- **Row meaning (grain):** 1 ad group definition **per day** (historical snapshots).
- **Key columns:** `ad_group_id` (INT64), `campaign_id` (INT64), `ad_group_name` (STRING), `ad_group_status` (STRING), `_DATA_DATE` (DATE), `_LATEST_DATE` (DATE).
- **⚠️ CRITICAL: Dimension table deduplication required!**
  - This table contains historical snapshots (407K+ rows for 630 ad groups).
  - **Always filter:** `WHERE _DATA_DATE = _LATEST_DATE` to get current snapshot.

**Correct dimension join pattern:**
```sql
-- CORRECT: Filter to latest snapshot
SELECT campaign_id, campaign_name
FROM google_ads_analytics.ads_Campaign_8350869641
WHERE _DATA_DATE = _LATEST_DATE

-- WRONG: No filter = cartesian product
SELECT campaign_id, campaign_name
FROM google_ads_analytics.ads_Campaign_8350869641  -- Missing filter!
```

### UTM Campaign ↔ Google Ads Mapping

**Pattern:** UTM campaigns in `master_account_data_daily.utm_campaign` are constructed from Google Ads campaign + ad group names.

**Join formula:**
```sql
-- Transform Google Ads to match UTM format
CONCAT(
  REPLACE(REPLACE(campaign_name, ' - ', '_'), ' ', '-'),
  '_',
  REPLACE(ad_group_name, ' ', '-')
) = utm_campaign
```

**Example mappings:**
| UTM Campaign | Google Ads Campaign | Ad Group |
|--------------|---------------------|----------|
| `Generic-Services_Dubai_Fulfillment` | Generic Services - Dubai | Fulfillment |
| `Generic-Services_Ecommerce` | Generic Services | Ecommerce |
| `Generic-Services_UAE_International-Delivery` | Generic Services - UAE | International delivery |

**Full join query pattern:**
```sql
SELECT
  m.utm_campaign,
  m.external_id,
  c.campaign_name,
  ag.ad_group_name,
  s.metrics_cost_micros / 1000000 as spend_aed,
  s.metrics_clicks,
  s.metrics_conversions
FROM `quiqup.views.master_account_data_daily` m
JOIN `quiqup.google_ads_analytics.ads_Campaign_8350869641` c
JOIN `quiqup.google_ads_analytics.ads_AdGroup_8350869641` ag
  ON c.campaign_id = ag.campaign_id
JOIN `quiqup.google_ads_analytics.ads_AdGroupStats_8350869641` s
  ON ag.ad_group_id = s.ad_group_id
WHERE m.utm_campaign = CONCAT(
  REPLACE(REPLACE(c.campaign_name, ' - ', '_'), ' ', '-'),
  '_',
  REPLACE(ag.ad_group_name, ' ', '-')
)
```

**Caveats:**
- 2 UTM values don't match: `Generic-Services_Dubai-Abu-Dhabi` and `Generic-Services_Dubai_Dubai-Abu-Dhabi` (ad group named "Courier from Dubai to Abu Dhabi")
- UTM campaigns without location suffix (e.g., `Generic-Services_Ecommerce`) may match multiple Google Ads campaigns—aggregate or filter by campaign
- Auto-tagging is enabled (`customer_auto_tagging_enabled = true`), so GCLID is primary tracking method

---

## Canonical Relationships (Join Keys)

- **Operational orders → operational clients:** `ex_api_current.orders.business_partner_id = ex_api_current.business_accounts.id`
- **Order history:** `ex_api_current.order_state_changes.client_order_id = ex_api_current.orders.client_order_id`
- **Order address history:** `ex_api_current.order_address_changes.client_order_id = ex_api_current.orders.client_order_id`
- **Invoices → clients (client-level):** `invoicer_current.invoices.account_id = views.master_account_data_daily.external_id`
- **Master account → Salesforce account:** `views.master_account_data_daily.account_id = salesforce_current.accounts.id`
- **Master account → pricing model:** `views.master_account_data_daily.pricing_model = salesforce_current.pricing_models.id`
- **Lead source normalization:** `salesforce_current.leads.lead_source = views.definition_lead_source.lead_source`
- **Account lead source attribution:** `views.account_lead_source_attribution.account_id = salesforce_current.accounts.id`
- **GP lead source attribution:** `views.grandparent_lead_source_attribution.grandparent_account_id = views.grandparent_account_created_date_and_first_order_delivered.gac_grandparent_account_id`
- **Lead → opportunity conversion:** `salesforce_current.leads.converted_opportunity_id = salesforce_current.opportunities.id`
- **Email tasks → opportunities:** `salesforce_current.tasks.what_id = salesforce_current.opportunities.id` (when `what_id` refers to opportunities)
- **Opportunity/user ownership metadata:** `salesforce_current.opportunities.owner_id = salesforce_current.users.id`

## Bridging Notes (When IDs Don't Match Directly)

- **Cohorting master accounts → operational orders:**
  - `views.master_account_data_daily.external_id` is INT64, while `ex_api_current.business_accounts.external_id` is STRING.
  - Bridge chain (conceptually): master external id ↔ business_accounts external id ↔ orders business_partner_id.

- **UTM campaign → Google Ads spend:**
  - `master_account_data_daily.utm_campaign` uses format `Generic-Services_[Location]_[AdGroup]`
  - Google Ads uses separate `campaign_name` and `ad_group_name` fields
  - Join key: `utm_campaign = CONCAT(REPLACE(REPLACE(campaign_name, ' - ', '_'), ' ', '-'), '_', REPLACE(ad_group_name, ' ', '-'))`
  - See "UTM Campaign ↔ Google Ads Mapping" section above for full pattern.

---

## Ad Group ROI Analysis Pattern

**Complete query for calculating monthly ROI by Google Ads ad group:**

```sql
-- Step 1: Get grandparents acquired via PAID Google Ads, mapped to ad groups
WITH grandparent_cohort AS (
  SELECT
    gua.grandparent_account_id,
    DATE_TRUNC(gua.acquisition_date, MONTH) AS cohort_month,
    gua.attributed_utm_campaign,
    m.google_ads_campaign,
    m.google_ads_ad_group
  FROM `quiqup.views.grandparent_utm_attribution` gua
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON gua.attributed_utm_campaign = m.utm_campaign
  WHERE EXTRACT(YEAR FROM gua.acquisition_date) = 2025
    AND gua.attributed_utm_medium = 'cpc'  -- ⚠️ CRITICAL: Paid only
    AND m.campaign_type IN ('search', 'pmax', 'demandgen')  -- Google Ads only
),

-- Step 2: Aggregate by ad group with lifetime revenue
cohort_revenue AS (
  SELECT
    gc.cohort_month,
    gc.google_ads_campaign,
    gc.google_ads_ad_group,
    COUNT(DISTINCT gc.grandparent_account_id) AS grandparents_acquired,
    ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)), 0) AS lifetime_revenue_aed
  FROM grandparent_cohort gc
  LEFT JOIN `quiqup.views.grandparent_revenue` gpr
    ON gpr.grandparent_account_id = gc.grandparent_account_id
  GROUP BY 1, 2, 3
),

-- Step 3: Get monthly spend by ad group
ad_group_spend AS (
  SELECT
    month,
    google_ads_campaign,
    google_ads_ad_group,
    SUM(spend_aed) AS spend_aed
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE EXTRACT(YEAR FROM month) = 2025
  GROUP BY 1, 2, 3
)

-- Step 4: Join and calculate ROI
SELECT
  cr.cohort_month,
  cr.google_ads_campaign,
  cr.google_ads_ad_group,
  cr.grandparents_acquired,
  cr.lifetime_revenue_aed,
  ROUND(cr.lifetime_revenue_aed * 0.25, 0) AS margin_aed,  -- 25% margin
  COALESCE(s.spend_aed, 0) AS spend_aed,
  CASE
    WHEN COALESCE(s.spend_aed, 0) > 0
    THEN ROUND(((cr.lifetime_revenue_aed * 0.25) - s.spend_aed) / s.spend_aed * 100, 1)
    ELSE NULL
  END AS roi_pct
FROM cohort_revenue cr
LEFT JOIN ad_group_spend s
  ON cr.cohort_month = s.month
  AND cr.google_ads_campaign = s.google_ads_campaign
  AND (cr.google_ads_ad_group = s.google_ads_ad_group
       OR (cr.google_ads_ad_group IS NULL AND s.google_ads_ad_group IS NULL))
ORDER BY cr.cohort_month, cr.google_ads_campaign, cr.google_ads_ad_group
```

**Key points:**
- **Paid filter:** Always use `attributed_utm_medium = 'cpc'` to identify paid Google Ads traffic
- **Campaign types:** Filter to `campaign_type IN ('search', 'pmax', 'demandgen')` for Google Ads only
- **Revenue:** Uses `grandparent_revenue` for deduplicated lifetime revenue (not period revenue)
- **ROI formula:** `ROI = (margin - spend) / spend × 100` where `margin = revenue × 0.25`
- **Ad group nulls:** Performance Max campaigns have NULL ad groups — handle with `OR (... IS NULL AND ... IS NULL)`

---

## Opportunity → Conversion → Cohort Revenue Query (REFERENCE)

This is the validated end-to-end query that answers: **"For opportunities created in a given period, how many converted and how much revenue did their cohorts generate?"**

Filters to new clients only (`client_type_classification = 'N'`). Add `owner_full_name_c` grouping for per-owner attribution.

**Join chain:** Opportunity → `true_grandparent_account` (on `business_account_id`) → all child accounts under GP → `invoicer_current.accounts` (on `salesforce_id`) → `invoicer_current.invoices` (handling `invoice_to_parent`)

**Key design decisions:**
- Each GP is deduplicated to its **earliest** converted opportunity's cohort month (prevents cross-month double-counting)
- When `invoice_to_parent = TRUE`, uses `parent_account_id` as the effective invoicer ID
- Revenue is period-specific (filtered by invoice `start_date`), NOT lifetime

```sql
-- Cohort Revenue by Opportunity Owner (New Clients Only)
-- Validated 2026-02-10: Total = AED 2,539,552 across 83 GPs, 516 new-client opps
-- Adjust date filters for different periods

WITH cohort_gps AS (
  -- Deduplicate each GP to its earliest converted new-client opp
  -- owner_full_name_c comes from the earliest opp via ARRAY_AGG
  SELECT
    tga.grandparent_account_id,
    MIN(DATE_TRUNC(v.opp_created_date, MONTH)) AS cohort_month,
    ARRAY_AGG(v.owner_full_name_c ORDER BY v.opp_created_date ASC LIMIT 1)[OFFSET(0)] AS owner_name
  FROM `quiqup.views.opportunities_convert_minus_2months` v
  JOIN `quiqup.views.true_grandparent_account` tga
    ON v.account_id = tga.business_account_id
  WHERE v.is_deleted = FALSE
    AND v.opp_created_date >= '2025-01-01'
    AND v.opp_created_date < '2026-01-01'
    AND v.is_converted = TRUE
    AND v.client_type_classification = 'N'
  GROUP BY tga.grandparent_account_id
),

gp_effective_accounts AS (
  -- Map each GP's child accounts to their invoicer IDs
  -- Handles invoice_to_parent: when TRUE, use parent_account_id
  SELECT DISTINCT
    cg.cohort_month,
    cg.grandparent_account_id,
    cg.owner_name,
    CASE
      WHEN ia.invoice_to_parent = TRUE THEN ia.parent_account_id
      ELSE ia.account_id
    END AS effective_invoicer_id
  FROM cohort_gps cg
  JOIN `quiqup.views.true_grandparent_account` tga
    ON cg.grandparent_account_id = tga.grandparent_account_id
  JOIN `quiqup.invoicer_current.accounts` ia
    ON ia.salesforce_id = tga.business_account_id
  WHERE ia.record_deleted = FALSE
),

gp_2025_revenue AS (
  -- Sum net revenue (total_amount - tax_amount) for the target period
  SELECT
    gea.cohort_month,
    gea.grandparent_account_id,
    gea.owner_name,
    ROUND(SUM(i.total_amount - COALESCE(i.tax_amount, 0)), 0) AS revenue
  FROM gp_effective_accounts gea
  JOIN `quiqup.invoicer_current.invoices` i
    ON i.account_id = gea.effective_invoicer_id
  WHERE i.state IN ('paid', 'overdue')
    AND i.record_deleted = FALSE
    AND i.deleted_at IS NULL
    AND i.start_date >= '2025-01-01'       -- Same period as opp filter
    AND i.start_date < '2026-01-01'
  GROUP BY gea.cohort_month, gea.grandparent_account_id, gea.owner_name
),

opp_counts AS (
  -- Opp-level counts per month per owner (NOT deduplicated to GP)
  SELECT
    DATE_TRUNC(opp_created_date, MONTH) AS opp_created_month,
    owner_full_name_c AS owner_name,
    COUNT(*) AS total_opps,
    COUNTIF(is_converted = TRUE) AS converted
  FROM `quiqup.views.opportunities_convert_minus_2months`
  WHERE is_deleted = FALSE
    AND opp_created_date >= '2025-01-01'
    AND opp_created_date < '2026-01-01'
    AND client_type_classification = 'N'
  GROUP BY opp_created_month, owner_name
)

SELECT
  oc.opp_created_month,
  oc.owner_name,
  oc.total_opps,
  oc.converted,
  COALESCE(r.revenue, 0) AS revenue_aed
FROM opp_counts oc
LEFT JOIN (
  SELECT cohort_month, owner_name, ROUND(SUM(revenue), 0) AS revenue
  FROM gp_2025_revenue
  GROUP BY cohort_month, owner_name
) r ON oc.opp_created_month = r.cohort_month AND oc.owner_name = r.owner_name
ORDER BY oc.opp_created_month, revenue_aed DESC
```

**To remove owner grouping** (simple monthly cohort): Remove `owner_name` / `owner_full_name_c` from all CTEs and the final SELECT, and remove the `owner_name` join condition in the final LEFT JOIN.

**To include existing clients**: Remove `AND client_type_classification = 'N'` from `cohort_gps` and `opp_counts`. WARNING: This inflated 2025 revenue from 2.5M to 14.2M AED (82% difference) due to existing large accounts.

**Revenue attribution caveat:** Winner-take-all — if Owner A brought the first converted opp for a GP, ALL GP revenue goes to Owner A even if Owner B later brought another opp under the same GP.

---

## Standard Financial Calculations (REFERENCE)

### Break-Even Month Calculation

**Formula:**
```
Break-Even Month = Spend ÷ Monthly Margin Rate
```

**What it means:** At what month (from acquisition) does cumulative margin equal spend?

**Correct SQL pattern:**
```sql
-- Monthly margin rate = Total Margin / Avg Months Elapsed
monthly_margin_rate = margin_aed / avg_months_elapsed

-- Break-even month = when cumulative margin equals spend
break_even_month = CASE
  WHEN spend_aed = 0 THEN 0                           -- No spend = always profitable
  WHEN monthly_margin_rate <= 0 THEN NULL             -- No margin = never breaks even
  ELSE ROUND(spend_aed / monthly_margin_rate, 1)      -- Simple division
END
```

**Validation checklist:**
| Check | Expected |
|-------|----------|
| If margin > spend | Break-even < current month (ALREADY profitable) |
| If margin < spend | Break-even > current month (NOT YET profitable) |
| If monthly rate = 0 | Break-even = NULL/Never |
| If spend = 0 | Break-even = 0 (pure profit) |

**Example calculations (ALWAYS show these):**
| Campaign | Spend | Margin | Monthly Rate | Break-Even | Calculation |
|----------|-------|--------|--------------|------------|-------------|
| Campaign A | 8,083 | 32,036 | 3,290 | **2.5 mo** | 8,083 ÷ 3,290 = 2.5 ✅ Already profitable |
| Campaign B | 39,549 | 31,841 | 3,362 | **11.8 mo** | 39,549 ÷ 3,362 = 11.8 |
| Campaign C | 40,894 | 10,125 | 1,072 | **38.2 mo** | 40,894 ÷ 1,072 = 38.2 |

### ROI Calculation

**Formula:**
```
ROI % = ((Margin - Spend) / Spend) × 100
```

**Interpretation:**
- ROI > 0%: Profitable (margin exceeds spend)
- ROI = 0%: Break-even (margin equals spend)
- ROI < 0%: Unprofitable (spend exceeds margin)
- ROI = -100%: Total loss (zero margin)

### CAC (Customer Acquisition Cost)

**Formula:**
```
CAC = Spend / Customers Acquired
```

**Note:** Always specify what "customer" means (lead, account, grandparent, activated GP).

### LTV:CAC Ratio

**Formula:**
```
LTV:CAC = Lifetime Margin per Customer / CAC
```

**Benchmarks:**
- < 1.0: Losing money on every customer
- 1.0-3.0: Marginal/break-even
- 3.0+: Healthy unit economics

### Payback Period

**Formula:**
```
Payback Period (months) = CAC / Monthly Margin per Customer
```

**Note:** This is equivalent to break-even month at the unit level.

---

## Statistical Methods (Quick Reference)

### Method Selection
| Question | Method |
|----------|--------|
| "Does X cause Y?" / "How much more likely?" | Relative Risk + Chi-Square |
| "Is the difference significant?" | Chi-Square (categorical) or t-test (continuous) |

### Key Thresholds
| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Relative Risk** | ≥2.0 | Strong effect ("2x more likely") |
| | 1.5-2.0 | Moderate |
| | <1.2 | Negligible |
| **Chi-Square (df=1)** | ≥10.83 | p<0.001 ✓✓✓ |
| | ≥6.63 | p<0.01 ✓✓ |
| | ≥3.84 | p<0.05 ✓ |

### SQL: 2x2 Contingency Table
```sql
WITH contingency AS (
  SELECT
    SUM(CASE WHEN exposed AND outcome THEN 1 ELSE 0 END) AS a,
    SUM(CASE WHEN exposed AND NOT outcome THEN 1 ELSE 0 END) AS b,
    SUM(CASE WHEN NOT exposed AND outcome THEN 1 ELSE 0 END) AS c,
    SUM(CASE WHEN NOT exposed AND NOT outcome THEN 1 ELSE 0 END) AS d,
    COUNT(*) AS n
  FROM base_data
)
SELECT
  ROUND((a/(a+b)) / NULLIF(c/(c+d), 0), 2) AS relative_risk,
  ROUND(n * POW(a*d - b*c, 2) / NULLIF((a+b)*(c+d)*(a+c)*(b+d), 0), 2) AS chi_square
FROM contingency
```

---

**Maintenance:** If you discover a new reusable query pattern or table combination, prompt the user: *"This pattern could be useful for future queries. Want me to add it to the Use Cases section?"*
