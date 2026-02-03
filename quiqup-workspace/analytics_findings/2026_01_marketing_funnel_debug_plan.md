# Debug Plan: marketing_funnel_grandparent_monthly View

**Date:** 2026-01-29
**Status:** In Progress

---

## Issues Identified

### Issue 1: `monthly_revenue_aed` Definition

**Current behavior:** Revenue invoiced in that month (by `invoice.end_date`)

**Expected behavior:** Revenue from grandparents **acquired** in that month (cohort revenue)

**Problem:** Current logic sums ALL revenue invoiced in a month regardless of when the grandparent was acquired. This doesn't answer "How much revenue did the July cohort generate?"

**Debug steps:**
1. Query the current view logic
2. Trace how `monthly_revenue_aed` is calculated
3. Redesign to link revenue to acquisition cohort

**Fix approach:**
```
NEW LOGIC:
For each month M:
  - Find all grandparents where acquisition_date is in month M
  - Sum their TOTAL lifetime revenue (not just revenue in month M)
  - This gives "LTV of cohort acquired in month M"
```

---

### Issue 2: `grandparent_activation_rate_pct` = 282.4% for July 2025

**Current behavior:** `grandparents_activated / grandparents_acquired * 100`

**Problem:** These two metrics are INDEPENDENT:
- `grandparents_acquired` = GPs where acquisition_date is in July (74)
- `grandparents_activated` = GPs where first_order_delivered is in July (209)

The 209 activated includes GPs acquired in Jan, Feb, Mar... who happened to place their first order in July.

**Debug steps:**
1. Verify the activated count includes all historical acquisitions
2. Confirm the mismatch between numerator and denominator cohorts

**Fix approach:**
```
NEW LOGIC:
activation_rate = (GPs acquired in month M who have activated by now) / (GPs acquired in month M)

NOT: (GPs who activated in month M) / (GPs acquired in month M)
```

---

### Issue 3: `unique_campaigns_acquired` Unclear

**Current behavior:** `COUNT(DISTINCT attributed_utm_campaign)` for GPs acquired in that month

**Problem:** Definition is unclear. Does it add analytical value?

**Debug steps:**
1. Verify the calculation
2. Determine if this metric is useful

**Fix approach:**
- Either remove or rename to `distinct_utm_campaigns_in_cohort`
- Add clarifying comment

---

## Debug Queries

### Query 1: Verify July 2025 activation rate issue

```sql
-- Check what's being counted
SELECT
  '2025-07' as month,

  -- GPs acquired in July
  (SELECT COUNT(DISTINCT grandparent_account_id)
   FROM views.grandparent_utm_attribution
   WHERE acquisition_date >= '2025-07-01' AND acquisition_date < '2025-08-01') as acquired_in_july,

  -- GPs who activated (first order) in July (regardless of acquisition date)
  (SELECT COUNT(DISTINCT gac_grandparent_account_id)
   FROM views.grandparent_account_created_date_and_first_order_delivered
   WHERE gac_grandparent_first_order_delivered >= '2025-07-01'
     AND gac_grandparent_first_order_delivered < '2025-08-01'
     AND gac_grandparent_first_order_delivered < '2030-01-01') as activated_in_july,

  -- GPs acquired in July who have EVER activated
  (SELECT COUNT(DISTINCT gpa.grandparent_account_id)
   FROM views.grandparent_utm_attribution gpa
   JOIN views.grandparent_account_created_date_and_first_order_delivered gac
     ON gac.gac_grandparent_account_id = gpa.grandparent_account_id
   WHERE gpa.acquisition_date >= '2025-07-01' AND gpa.acquisition_date < '2025-08-01'
     AND gac.gac_grandparent_first_order_delivered < '2030-01-01') as july_cohort_ever_activated
```

### Query 2: Verify revenue attribution

```sql
-- Check what monthly_revenue_aed currently measures
SELECT
  DATE_TRUNC(i.end_date, MONTH) as invoice_month,
  COUNT(DISTINCT i.id) as invoices,
  SUM(i.total_amount) as revenue
FROM (
  SELECT DISTINCT
    tg.grandparent_account_id,
    CASE WHEN ia.invoice_to_parent THEN ia.parent_account_id ELSE ia.account_id END AS eff_account
  FROM views.true_grandparent_account tg
  JOIN invoicer_current.accounts ia ON ia.salesforce_id = tg.business_account_id
) u
JOIN invoicer_current.invoices i
  ON i.account_id = u.eff_account
  AND i.record_deleted = FALSE AND i.deleted_at IS NULL AND i.state = 'paid'
WHERE i.end_date >= '2025-07-01' AND i.end_date < '2025-08-01'
GROUP BY 1
```

### Query 3: What revenue SHOULD be (cohort-based)

```sql
-- Revenue from July 2025 acquisition cohort
SELECT
  'July 2025 Cohort' as cohort,
  COUNT(DISTINCT gpa.grandparent_account_id) as gps_acquired,
  COUNT(DISTINCT gpr.grandparent_account_id) as gps_with_revenue,
  SUM(COALESCE(gpr.total_revenue_aed, 0)) as cohort_lifetime_revenue
FROM views.grandparent_utm_attribution gpa
LEFT JOIN views.grandparent_revenue gpr ON gpr.grandparent_account_id = gpa.grandparent_account_id
WHERE gpa.acquisition_date >= '2025-07-01' AND gpa.acquisition_date < '2025-08-01'
```

---

## Proposed Fix: Redesigned View

```sql
CREATE OR REPLACE VIEW `quiqup.views.marketing_funnel_grandparent_monthly` AS

WITH h2_base AS (
  SELECT * FROM views.quiqup_com_unique_visitors_monthly_2025_h2
),

-- COHORT: Grandparents acquired in each month
cohort_acquired AS (
  SELECT
    DATE_TRUNC(acquisition_date, MONTH) AS cohort_month,
    grandparent_account_id,
    attributed_utm_campaign
  FROM views.grandparent_utm_attribution
),

-- COHORT METRICS: Aggregated per cohort month
cohort_metrics AS (
  SELECT
    ca.cohort_month AS month,
    COUNT(DISTINCT ca.grandparent_account_id) AS grandparents_acquired,
    COUNT(DISTINCT CASE WHEN ca.attributed_utm_source = 'google' THEN ca.grandparent_account_id END) AS gp_acquired_google,
    COUNT(DISTINCT ca.attributed_utm_campaign) AS distinct_campaigns,

    -- Activation: cohort members who have activated (ever)
    COUNT(DISTINCT CASE
      WHEN gac.gac_grandparent_first_order_delivered < '2030-01-01'
      THEN ca.grandparent_account_id
    END) AS cohort_activated,

    -- Revenue: lifetime revenue of this cohort
    SUM(COALESCE(gpr.total_revenue_aed, 0)) AS cohort_lifetime_revenue_aed

  FROM cohort_acquired ca
  LEFT JOIN views.grandparent_account_created_date_and_first_order_delivered gac
    ON gac.gac_grandparent_account_id = ca.grandparent_account_id
  LEFT JOIN views.grandparent_revenue gpr
    ON gpr.grandparent_account_id = ca.grandparent_account_id
  GROUP BY 1
)

SELECT
  h2.month,

  -- Original H2 metrics
  h2.unique_visitors,
  h2.high_intent_visitors,
  h2.sf_contact_form_website_source_leads_deduped AS sf_leads,
  h2.google_ads_spend_aed,
  h2.google_ads_clicks,

  -- Cohort acquisition
  COALESCE(cm.grandparents_acquired, 0) AS grandparents_acquired,
  COALESCE(cm.gp_acquired_google, 0) AS gp_acquired_google,
  COALESCE(cm.distinct_campaigns, 0) AS distinct_campaigns_in_cohort,

  -- Cohort activation (how many of THIS month's acquired GPs activated)
  COALESCE(cm.cohort_activated, 0) AS cohort_activated,
  ROUND(cm.cohort_activated * 100.0 / NULLIF(cm.grandparents_acquired, 0), 1) AS cohort_activation_rate_pct,

  -- Cohort revenue (lifetime revenue of THIS month's acquired GPs)
  COALESCE(cm.cohort_lifetime_revenue_aed, 0) AS cohort_lifetime_revenue_aed,

  -- Unit economics
  ROUND(h2.google_ads_spend_aed / NULLIF(cm.grandparents_acquired, 0), 2) AS cost_per_gp_acquired,
  ROUND(cm.cohort_lifetime_revenue_aed / NULLIF(h2.google_ads_spend_aed, 0), 2) AS cohort_roi

FROM h2_base h2
LEFT JOIN cohort_metrics cm ON cm.month = h2.month
ORDER BY h2.month DESC
```

---

## Key Changes in Redesign

| Metric | Old | New |
|--------|-----|-----|
| `monthly_revenue_aed` | Revenue invoiced in month | `cohort_lifetime_revenue_aed` = Lifetime revenue of GPs acquired in month |
| `grandparents_activated` | GPs who activated in month | `cohort_activated` = GPs acquired in month who have ever activated |
| `grandparent_activation_rate_pct` | activated_in_month / acquired_in_month (WRONG) | cohort_activated / grandparents_acquired (CORRECT) |
| `unique_campaigns_acquired` | Unclear | `distinct_campaigns_in_cohort` = Distinct UTM campaigns for that cohort |

---

## Execution Plan

1. [ ] Run debug queries to verify issues
2. [ ] Confirm the expected logic with user
3. [ ] Update the view with cohort-based calculations
4. [ ] Verify the fix with July 2025 data
5. [ ] Update documentation

---

*Debug plan created by BigQuery Analyst Agent*
