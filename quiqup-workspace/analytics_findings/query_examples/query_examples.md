# Query Example: Google Ads Ad Group ROI Analysis

**Created:** 2026-01-30
**Use Case:** Monthly ROI analysis by campaign and ad group for Google Ads

---

## Question

> "Show me monthly spend, acquisitions, revenue, margin, and ROI for each Google Ads campaign and ad group in 2025"

---

## Key Principles

### 1. Always Use Canonical Views for Mapping
Use `definition_utm_google_ads_mapping` for UTM → Google Ads mapping. **Never invent your own mapping logic.**

```sql
-- CORRECT: Use the canonical mapping view
LEFT JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
  ON ua.attributed_utm_campaign = gam.utm_campaign

-- WRONG: Don't hardcode mappings inline
CASE WHEN utm_campaign LIKE '%Dubai%' THEN 'Dubai' END  -- DON'T DO THIS
```

### 2. Reuse Logic from `marketing_funnel_grandparent_monthly`
This view is the source of truth for:
- **Revenue source:** `grandparent_revenue.total_revenue_aed`
- **Margin calculation:** Revenue × 0.25 (25%)
- **Attribution:** First-touch at grandparent level

### 3. Use `google_ads_ad_group_display` for Display Names
The mapping view has a special column that handles NULL ad groups:
- `google_ads_ad_group` — Original value (NULL for PMax, Demand Gen)
- `google_ads_ad_group_display` — COALESCE(ad_group, campaign) for display

---

## Common Errors to Avoid

### Error 1: Column Name Mismatches

```sql
-- WRONG: These column names don't exist
SELECT gac_grandparent_name  -- ❌ No such column
FROM grandparent_account_created_date_and_first_order_delivered

-- CORRECT: Check schema first, use actual column names
SELECT gac_grandparent_account_id  -- ✅ Actual column
FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered`
```

**Tip:** Always query `INFORMATION_SCHEMA.COLUMNS` to verify column names:
```sql
SELECT column_name, data_type
FROM `quiqup.views.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'grandparent_revenue'
```

### Error 2: Forgetting Campaign in Joins (Causes Duplicates)

Ad group names are NOT unique across campaigns. "Fulfillment" exists in:
- Generic Services - Dubai
- Generic Services - UAE
- KSA_Services

```sql
-- WRONG: Join only on ad_group (will cause duplicates/wrong matches)
ON am.ad_group = sd.ad_group

-- CORRECT: Join on BOTH campaign AND ad_group
ON am.campaign = sd.campaign AND am.ad_group = sd.ad_group
```

### Error 3: Not Handling NULL Ad Groups

Performance Max and Demand Gen campaigns have NULL ad_groups in spend data.

```sql
-- WRONG: Will lose PMax data
WHERE google_ads_ad_group IS NOT NULL

-- CORRECT: Use COALESCE to fall back to campaign name
COALESCE(google_ads_ad_group, google_ads_campaign) AS ad_group
```

### Error 4: Wrong ROI Formula

```sql
-- WRONG: Simple percentage (not accounting for margin)
(revenue - spend) / spend * 100  -- ❌ Uses revenue instead of margin

-- CORRECT: ROI based on margin (25% of revenue)
((revenue * 0.25) - spend) / spend * 100  -- ✅ Per marketing_funnel logic
```

---

## Full Query Example

```sql
-- =============================================================================
-- GOOGLE ADS AD GROUP ROI ANALYSIS (2025)
-- =============================================================================
-- Sources:
--   - definition_utm_google_ads_mapping: UTM → Google Ads mapping (canonical)
--   - grandparent_account_created_date_and_first_order_delivered: Acquisition dates
--   - grandparent_utm_attribution: First-touch attribution
--   - grandparent_revenue: Lifetime revenue per grandparent
--   - google_ads_spend_monthly: Monthly spend by campaign/ad group
--
-- Logic follows: marketing_funnel_grandparent_monthly
--   - Margin = Revenue × 25%
--   - ROI = (Margin - Spend) / Spend × 100
-- =============================================================================

WITH grandparent_with_google_ads AS (
  -- Step 1: Join grandparents → UTM attribution → Google Ads mapping
  SELECT
    gac.gac_grandparent_account_id AS grandparent_account_id,
    DATE_TRUNC(DATE(gac.gac_minimum_created_date), MONTH) AS cohort_month,
    gam.google_ads_campaign,
    gam.google_ads_ad_group_display AS ad_group  -- Use display name (handles NULLs)
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  LEFT JOIN `quiqup.views.grandparent_utm_attribution` ua
    ON gac.gac_grandparent_account_id = ua.grandparent_account_id
  LEFT JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
    ON ua.attributed_utm_campaign = gam.utm_campaign
  WHERE gam.google_ads_campaign IS NOT NULL  -- Only Google Ads attributed
    AND DATE(gac.gac_minimum_created_date) >= '2025-01-01'
    AND DATE(gac.gac_minimum_created_date) < '2026-01-01'
),

grandparent_revenue AS (
  -- Step 2: Get lifetime revenue per grandparent
  SELECT grandparent_account_id, total_revenue_aed
  FROM `quiqup.views.grandparent_revenue`
),

acquisition_metrics AS (
  -- Step 3: Aggregate acquisitions and revenue by month/campaign/ad_group
  SELECT
    gga.cohort_month AS month,
    gga.google_ads_campaign AS campaign,
    gga.ad_group,
    COUNT(DISTINCT gga.grandparent_account_id) AS grandparents_acquired,
    ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)), 0) AS revenue_aed,
    ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)) * 0.25, 0) AS margin_aed  -- 25% margin
  FROM grandparent_with_google_ads gga
  LEFT JOIN grandparent_revenue gpr
    ON gga.grandparent_account_id = gpr.grandparent_account_id
  GROUP BY 1, 2, 3
),

spend_data AS (
  -- Step 4: Get monthly spend by campaign/ad_group
  -- NOTE: COALESCE handles NULL ad_groups (PMax, Demand Gen)
  SELECT
    month,
    google_ads_campaign AS campaign,
    COALESCE(google_ads_ad_group, google_ads_campaign) AS ad_group,
    ROUND(spend_aed, 2) AS spend_aed
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE month >= '2025-01-01' AND month < '2026-01-01'
)

-- Step 5: FULL OUTER JOIN to capture both acquisitions and spend
-- (Some months have spend but no acquisitions, and vice versa)
SELECT
  FORMAT_DATE('%Y-%m', COALESCE(am.month, sd.month)) AS month,
  COALESCE(am.campaign, sd.campaign) AS campaign,
  COALESCE(am.ad_group, sd.ad_group) AS ad_group,
  COALESCE(sd.spend_aed, 0) AS spend_aed,
  COALESCE(am.grandparents_acquired, 0) AS gps_acquired,
  COALESCE(am.revenue_aed, 0) AS revenue_aed,
  COALESCE(am.margin_aed, 0) AS margin_aed,
  -- ROI = (margin - spend) / spend × 100 (per marketing_funnel logic)
  ROUND(
    CASE
      WHEN COALESCE(sd.spend_aed, 0) > 0
      THEN ((COALESCE(am.margin_aed, 0) - COALESCE(sd.spend_aed, 0)) / sd.spend_aed) * 100
      ELSE NULL  -- Cannot calculate ROI without spend
    END, 1
  ) AS roi_pct
FROM acquisition_metrics am
FULL OUTER JOIN spend_data sd
  ON am.month = sd.month
  AND am.campaign = sd.campaign  -- IMPORTANT: Join on campaign too!
  AND am.ad_group = sd.ad_group
ORDER BY month, campaign, ad_group
```

---

## Understanding the Output

### Example Row
```
| month   | campaign                | ad_group           | spend_aed | gps_acquired | revenue_aed | margin_aed | roi_pct |
|---------|-------------------------|--------------------|-----------|--------------|-------------|------------|---------|
| 2025-09 | Generic Services - Dubai| Fulfillment        | 1,606.43  | 12           | 18,427      | 4,607      | 186.8   |
```

**Interpretation:**
- In Sep 2025, the Dubai Fulfillment ad group spent 1,606 AED
- Acquired 12 grandparents that month
- Those 12 grandparents generated 18,427 AED lifetime revenue
- At 25% margin = 4,607 AED margin
- ROI = (4,607 - 1,606) / 1,606 × 100 = **+186.8%** ✅

### Gotcha: GPs with 0 Revenue

If you see GPs acquired with 0 revenue, this is **NOT a data bug**:
- These are accounts that were acquired but **never activated** (never placed an order)
- Even 11-month-old cohorts may have 0% activation in some ad groups
- This indicates a **lead quality problem**, not a data problem

---

## Related Views

| View | Purpose |
|------|---------|
| `definition_utm_google_ads_mapping` | Canonical UTM → Google Ads mapping |
| `grandparent_account_created_date_and_first_order_delivered` | Acquisition dates |
| `grandparent_utm_attribution` | First-touch UTM attribution |
| `grandparent_revenue` | Lifetime revenue per grandparent |
| `google_ads_spend_monthly` | Monthly spend by campaign/ad group |
| `marketing_funnel_grandparent_monthly` | Full funnel metrics (reference for logic) |

---

# Query Example: Ad Group Performance with Activation Metrics

**Created:** 2026-01-30
**Updated:** 2026-01-30 (Fixed activation rate bug)
**Use Case:** Campaign optimization - identify successful vs failed ad groups with full funnel metrics

---

## Question

> "Show me ad group performance for a specific campaign with spend, leads, accounts, activation rate, margin, and break-even analysis"

---

## Key Principles

### 1. 🚨 CRITICAL: Use Correct Source for Activation Rates

**BUG:** `grandparent_utm_attribution` only contains ACTIVATED grandparents. Using it will always show 100% activation.

**FIX:** Use `account_utm_attribution` + `salesforce_current.accounts` as the source, then LEFT JOIN to `grandparent_account_created_date_and_first_order_delivered` to determine activation.

```sql
-- ❌ WRONG: Will show 100% activation (only activated accounts in this view)
FROM `quiqup.views.grandparent_utm_attribution` gua
LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  ON gua.grandparent_account_id = gac.gac_grandparent_account_id

-- ✅ CORRECT: Gets ALL accounts, then checks activation status
FROM `quiqup.salesforce_current.accounts` a
JOIN `quiqup.views.account_utm_attribution` ua ON a.id = ua.account_id
LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  ON a.id = gac.gac_grandparent_account_id
```

### 2. Activation = First Delivered Order
Check activation with: `gac.gac_grandparent_account_id IS NOT NULL`

### 3. Break-Even Formula
```
Break-Even Months = Spend ÷ Monthly Rate
Monthly Rate = Margin ÷ Avg Cohort Age (months)
```

### 4. Filter by Cohort Period for Mature Analysis
```sql
-- H1 2025 cohorts (7-12 months mature by Jan 2026)
WHERE DATE(a.created_date) >= '2025-01-01' AND DATE(a.created_date) < '2025-07-01'
```

---

## Full Query Example

```sql
-- =============================================================================
-- AD GROUP PERFORMANCE WITH ACTIVATION METRICS (CORRECTED)
-- =============================================================================
-- Use Case: Campaign optimization analysis
-- Metrics: Spend, Leads, Accounts, Activated, Activation %, Margin, Monthly Rate, ROI, Break-Even
--
-- 🚨 KEY FIX: Uses account_utm_attribution + salesforce accounts (not grandparent_utm_attribution)
--    to correctly calculate activation rates (grandparent_utm_attribution only has activated accounts)
--
-- Sources:
--   - salesforce_current.accounts: ALL accounts (activated and not)
--   - account_utm_attribution: UTM attribution at account level
--   - definition_utm_google_ads_mapping: UTM → Google Ads mapping
--   - grandparent_account_created_date_and_first_order_delivered: Activation status (LEFT JOIN)
--   - grandparent_revenue: Lifetime revenue per grandparent
--   - google_ads_spend_monthly: Monthly spend by campaign/ad group
--   - salesforce_current.leads: Lead counts
-- =============================================================================

WITH campaign_ad_groups AS (
  -- Get all ad groups for the target campaign
  SELECT DISTINCT
    google_ads_campaign,
    google_ads_ad_group
  FROM `quiqup.views.definition_utm_google_ads_mapping`
  WHERE google_ads_campaign = 'Generic Services - Dubai'  -- Change campaign here
    AND google_ads_ad_group IS NOT NULL
),

spend_data AS (
  -- Aggregate spend by ad group for the period
  SELECT
    google_ads_ad_group,
    SUM(spend_aed) AS spend_aed
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE google_ads_campaign = 'Generic Services - Dubai'
    AND month >= '2025-01-01' AND month < '2025-07-01'  -- H1 2025
  GROUP BY 1
),

leads_data AS (
  -- Count leads by ad group via UTM mapping
  SELECT
    m.google_ads_ad_group,
    COUNT(DISTINCT l.id) AS leads_created
  FROM `quiqup.salesforce_current.leads` l
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON l.utm_campaign_c = m.utm_campaign
  WHERE m.google_ads_campaign = 'Generic Services - Dubai'
    AND l.is_deleted = FALSE
    AND DATE(l.created_date) >= '2025-01-01' AND DATE(l.created_date) < '2025-07-01'
  GROUP BY 1
),

-- 🚨 FIXED: Use account_utm_attribution + salesforce accounts to get ALL accounts
account_data AS (
  SELECT
    m.google_ads_ad_group,
    a.id AS account_id,
    DATE(a.created_date) AS created_date,
    -- Check if activated by joining to the activated view
    gac.gac_grandparent_account_id IS NOT NULL AS is_activated
  FROM `quiqup.salesforce_current.accounts` a
  JOIN `quiqup.views.account_utm_attribution` ua
    ON a.id = ua.account_id
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON ua.attributed_utm_campaign = m.utm_campaign
  LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
    ON a.id = gac.gac_grandparent_account_id
  WHERE m.google_ads_campaign = 'Generic Services - Dubai'
    AND ua.attributed_utm_medium = 'cpc'  -- Paid traffic only
    AND DATE(a.created_date) >= '2025-01-01' AND DATE(a.created_date) < '2025-07-01'
    AND a.is_deleted = FALSE
),

account_agg AS (
  -- Aggregate account metrics
  SELECT
    google_ads_ad_group,
    COUNT(DISTINCT account_id) AS account_count,
    COUNT(DISTINCT CASE WHEN is_activated THEN account_id END) AS accounts_activated,
    AVG(DATE_DIFF(CURRENT_DATE(), created_date, DAY) / 30.44) AS avg_months
  FROM account_data
  GROUP BY 1
),

-- Revenue only for activated accounts
revenue_data AS (
  SELECT
    m.google_ads_ad_group,
    ROUND(SUM(COALESCE(gpr.total_revenue_aed, 0)), 0) AS lifetime_revenue_aed
  FROM `quiqup.salesforce_current.accounts` a
  JOIN `quiqup.views.account_utm_attribution` ua
    ON a.id = ua.account_id
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON ua.attributed_utm_campaign = m.utm_campaign
  JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
    ON a.id = gac.gac_grandparent_account_id  -- Only activated accounts have revenue
  LEFT JOIN `quiqup.views.grandparent_revenue` gpr
    ON gac.gac_grandparent_account_id = gpr.grandparent_account_id
  WHERE m.google_ads_campaign = 'Generic Services - Dubai'
    AND ua.attributed_utm_medium = 'cpc'
    AND DATE(a.created_date) >= '2025-01-01' AND DATE(a.created_date) < '2025-07-01'
    AND a.is_deleted = FALSE
  GROUP BY 1
)

-- Final output with all metrics
SELECT
  cag.google_ads_ad_group AS ad_group,
  ROUND(COALESCE(s.spend_aed, 0), 0) AS spend_aed,
  COALESCE(l.leads_created, 0) AS leads,
  COALESCE(acc.account_count, 0) AS accounts,
  COALESCE(acc.accounts_activated, 0) AS activated,
  ROUND(SAFE_DIVIDE(acc.accounts_activated, acc.account_count) * 100, 1) AS activation_pct,
  ROUND(COALESCE(acc.avg_months, 0), 1) AS avg_months,
  ROUND(COALESCE(r.lifetime_revenue_aed, 0) * 0.25, 0) AS margin_aed,
  -- Monthly rate = margin / avg_months
  CASE
    WHEN COALESCE(acc.avg_months, 0) > 0
    THEN ROUND(COALESCE(r.lifetime_revenue_aed, 0) * 0.25 / acc.avg_months, 0)
    ELSE 0
  END AS monthly_rate,
  -- ROI % = (margin - spend) / spend * 100
  CASE
    WHEN COALESCE(s.spend_aed, 0) > 0
    THEN ROUND(((COALESCE(r.lifetime_revenue_aed, 0) * 0.25) - s.spend_aed) / s.spend_aed * 100, 1)
    ELSE NULL
  END AS roi_pct,
  -- Break-even = spend / monthly_rate
  CASE
    WHEN COALESCE(r.lifetime_revenue_aed, 0) * 0.25 / NULLIF(acc.avg_months, 0) > 0
    THEN ROUND(s.spend_aed / (r.lifetime_revenue_aed * 0.25 / acc.avg_months), 0)
    ELSE NULL
  END AS break_even_months
FROM campaign_ad_groups cag
LEFT JOIN spend_data s ON s.google_ads_ad_group = cag.google_ads_ad_group
LEFT JOIN leads_data l ON l.google_ads_ad_group = cag.google_ads_ad_group
LEFT JOIN account_agg acc ON acc.google_ads_ad_group = cag.google_ads_ad_group
LEFT JOIN revenue_data r ON r.google_ads_ad_group = cag.google_ads_ad_group
ORDER BY s.spend_aed DESC NULLS LAST
```

---

## Understanding the Output

### Example Row
```
| ad_group    | spend_aed | leads | accounts | activated | activation_pct | avg_months | margin_aed | monthly_rate | roi_pct | break_even_months |
|-------------|-----------|-------|----------|-----------|----------------|------------|------------|--------------|---------|-------------------|
| Fulfillment | 1,835     | 25    | 18       | 16        | 88.9           | 10.2       | 12         | 1            | -99.4   | 1,622             |
```

**Interpretation:**
- H1 2025 Fulfillment ad group spent 1,835 AED
- Generated 25 leads → 18 accounts (72% lead-to-account conversion)
- 16 of 18 accounts activated (**88.9% activation rate**)
- But only 12 AED margin after 10.2 months = **0.75 AED/account**
- At 1 AED/month rate, break-even would take 1,622 months
- **Diagnosis:** Both activation (88.9%) and revenue per account (near zero) need improvement

### Interpreting Break-Even Values

| Break-Even | Status | Action |
|------------|--------|--------|
| ≤ 12 months | ✅ Profitable | Scale up |
| 12-18 months | ⚠️ Near break-even | Monitor |
| 18-24 months | ⚠️ Marginal | Optimize or reduce |
| > 24 months | ❌ Unprofitable | Pause or restructure |
| NULL | ❌ No revenue | Pause immediately |

---

# Query Example: Cohort Comparison for Performance Investigation

**Created:** 2026-01-30
**Updated:** 2026-01-30 (Fixed activation rate bug)
**Use Case:** Investigate why ad group performance changed over time

---

## Question

> "Why did Fulfillment and Courier Service performance collapse in H1 2025?"

---

## Full Query Example

```sql
-- =============================================================================
-- COHORT COMPARISON: INVESTIGATE PERFORMANCE CHANGES (CORRECTED)
-- =============================================================================
-- Use Case: Compare ad group performance across time periods
-- Key metric: Revenue per account (reveals quality changes vs volume changes)
--
-- 🚨 KEY FIX: Uses account_utm_attribution + salesforce accounts (not grandparent_utm_attribution)
--    to correctly calculate activation rates
-- =============================================================================

WITH account_cohort_data AS (
  SELECT
    m.google_ads_ad_group,
    a.id AS account_id,
    DATE(a.created_date) AS created_date,
    -- Define cohort periods
    CASE
      WHEN DATE(a.created_date) >= '2024-01-01' AND DATE(a.created_date) < '2024-07-01' THEN 'H1 2024'
      WHEN DATE(a.created_date) >= '2024-07-01' AND DATE(a.created_date) < '2025-01-01' THEN 'H2 2024'
      WHEN DATE(a.created_date) >= '2025-01-01' AND DATE(a.created_date) < '2025-07-01' THEN 'H1 2025'
      WHEN DATE(a.created_date) >= '2025-07-01' AND DATE(a.created_date) < '2026-01-01' THEN 'H2 2025'
    END AS cohort_period,
    gac.gac_grandparent_account_id IS NOT NULL AS is_activated,
    COALESCE(gpr.total_revenue_aed, 0) AS revenue_aed
  FROM `quiqup.salesforce_current.accounts` a
  JOIN `quiqup.views.account_utm_attribution` ua
    ON a.id = ua.account_id
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON ua.attributed_utm_campaign = m.utm_campaign
  LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
    ON a.id = gac.gac_grandparent_account_id
  LEFT JOIN `quiqup.views.grandparent_revenue` gpr
    ON a.id = gpr.grandparent_account_id
  WHERE m.google_ads_campaign = 'Generic Services - Dubai'
    AND m.google_ads_ad_group IN ('Fulfillment', 'Courier Service')  -- Target ad groups
    AND ua.attributed_utm_medium = 'cpc'
    AND DATE(a.created_date) >= '2024-01-01'
    AND a.is_deleted = FALSE
),

spend_by_period AS (
  SELECT
    google_ads_ad_group,
    CASE
      WHEN month >= '2024-01-01' AND month < '2024-07-01' THEN 'H1 2024'
      WHEN month >= '2024-07-01' AND month < '2025-01-01' THEN 'H2 2024'
      WHEN month >= '2025-01-01' AND month < '2025-07-01' THEN 'H1 2025'
      WHEN month >= '2025-07-01' AND month < '2026-01-01' THEN 'H2 2025'
    END AS cohort_period,
    SUM(spend_aed) AS spend_aed
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE google_ads_campaign = 'Generic Services - Dubai'
    AND google_ads_ad_group IN ('Fulfillment', 'Courier Service')
    AND month >= '2024-01-01'
  GROUP BY 1, 2
)

SELECT
  a.google_ads_ad_group AS ad_group,
  a.cohort_period,
  ROUND(COALESCE(s.spend_aed, 0), 0) AS spend_aed,
  COUNT(DISTINCT a.account_id) AS accounts,
  COUNT(DISTINCT CASE WHEN a.is_activated THEN a.account_id END) AS activated,
  ROUND(SAFE_DIVIDE(
    COUNT(DISTINCT CASE WHEN a.is_activated THEN a.account_id END),
    COUNT(DISTINCT a.account_id)
  ) * 100, 1) AS activation_pct,
  ROUND(SUM(a.revenue_aed), 0) AS revenue_aed,
  ROUND(SUM(a.revenue_aed) * 0.25, 0) AS margin_aed,
  -- KEY METRIC: Revenue per account (quality indicator)
  ROUND(SAFE_DIVIDE(SUM(a.revenue_aed), COUNT(DISTINCT a.account_id)), 0) AS revenue_per_acct
FROM account_cohort_data a
LEFT JOIN spend_by_period s
  ON a.google_ads_ad_group = s.google_ads_ad_group
  AND a.cohort_period = s.cohort_period
WHERE a.cohort_period IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY a.google_ads_ad_group, a.cohort_period
```

---

## Understanding the Output

### Example: Detecting Quality Collapse (Corrected Data)

```
| ad_group        | cohort_period | spend_aed | accounts | activated | activation_pct | revenue_per_acct |
|-----------------|---------------|-----------|----------|-----------|----------------|------------------|
| Courier Service | H2 2024       | 1,916     | 22       | 22        | 100.0          | 653              |
| Courier Service | H1 2025       | 1,935     | 58       | 57        | 98.3           | 15               |
| Fulfillment     | H2 2024       | 921       | 9        | 9         | 100.0          | 500              |
| Fulfillment     | H1 2025       | 1,835     | 18       | 16        | 88.9           | 3                |
| Fulfillment     | H2 2025       | 7,117     | 61       | 52        | 85.2           | 7                |
```

**Diagnosis:**
- Account volume increased (Courier Service: 22 → 58, Fulfillment: 9 → 18 → 61) ✅
- Activation rates are high but declining slightly (Fulfillment: 100% → 88.9% → 85.2%) ⚠️
- **Revenue per account collapsed dramatically** (Courier: 653 → 15 AED, Fulfillment: 500 → 3 AED) ❌

**Primary issue: Customer value/quality, not activation.**

### Common Patterns

| Pattern | Symptom | Likely Cause |
|---------|---------|--------------|
| Activation drop | activation_pct decreases | Lead quality issue, wrong audience |
| Revenue/account drop | revenue_per_acct decreases, activation stable | Smaller customers, pricing issue, churn |
| Volume drop | accounts decreases, revenue_per_acct stable | Budget cut, competition, seasonality |
| Recovery | metrics improve in later period | Targeting fix, product improvement |

---

# Query Example: Organic vs Paid Correlation Analysis

**Created:** 2026-01-30
**Use Case:** Determine if organic revenue depends on paid marketing spend

---

## Question

> "Is the 74% organic revenue real, or a side effect of paid marketing (brand awareness)?"

---

## Analysis 1: Spend-Organic Correlation (30-month time series)

```sql
-- =============================================================================
-- ORGANIC VS PAID CORRELATION ANALYSIS
-- =============================================================================
-- Tests whether cutting paid spend affects organic account creation
-- Time period: July 2023 - December 2025 (30 months)
-- =============================================================================

WITH monthly_data AS (
  SELECT
    DATE_TRUNC(DATE(g.gac_minimum_created_date), MONTH) AS month,
    SUM(CASE WHEN COALESCE(poc.is_paid, FALSE) THEN 1 ELSE 0 END) AS gp_acquired_paid,
    SUM(CASE WHEN COALESCE(poc.is_paid, FALSE) = FALSE THEN 1 ELSE 0 END) AS gp_acquired_organic,
    COUNT(DISTINCT g.gac_grandparent_account_id) AS total_gps
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` g
  LEFT JOIN `quiqup.views.grandparent_utm_attribution` gua
    ON g.gac_grandparent_account_id = gua.grandparent_account_id
  LEFT JOIN `quiqup.views.definition_paid_organic_channel` poc
    ON LOWER(gua.attributed_utm_source) = LOWER(poc.utm_source)
    AND LOWER(gua.attributed_utm_medium) = LOWER(poc.utm_medium)
  WHERE DATE(g.gac_minimum_created_date) >= '2023-07-01'
    AND DATE(g.gac_minimum_created_date) < '2026-01-01'
  GROUP BY 1
),
monthly_spend AS (
  SELECT
    DATE_TRUNC(month, MONTH) AS month,
    SUM(spend_aed) AS google_ads_spend_aed
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE month >= '2023-07-01' AND month < '2026-01-01'
  GROUP BY 1
),
combined AS (
  SELECT
    md.month,
    COALESCE(ms.google_ads_spend_aed, 0) AS spend,
    md.gp_acquired_paid AS paid_gps,
    md.gp_acquired_organic AS organic_gps
  FROM monthly_data md
  LEFT JOIN monthly_spend ms ON md.month = ms.month
)
SELECT
  -- Correlation coefficients
  ROUND(CORR(spend, organic_gps), 3) AS corr_spend_vs_organic,
  ROUND(CORR(spend, paid_gps), 3) AS corr_spend_vs_paid,
  ROUND(CORR(paid_gps, organic_gps), 3) AS corr_paid_vs_organic,
  COUNT(*) AS months_analyzed,
  ROUND(AVG(spend), 0) AS avg_spend,
  ROUND(AVG(paid_gps), 0) AS avg_paid_gps,
  ROUND(AVG(organic_gps), 0) AS avg_organic_gps
FROM combined
```

**Interpretation:**
- `corr_spend_vs_organic` < 0.5 = weak correlation → organic is independent
- `corr_spend_vs_organic` > 0.7 = strong correlation → organic may depend on paid

---

## Analysis 1b: Lag Correlation (Does spend today → organic later?)

```sql
-- =============================================================================
-- LAG CORRELATION: Does spend in month N affect organic in N+1, N+2, N+3?
-- =============================================================================

WITH monthly_data AS (
  SELECT
    DATE_TRUNC(DATE(g.gac_minimum_created_date), MONTH) AS month,
    SUM(CASE WHEN COALESCE(poc.is_paid, FALSE) THEN 1 ELSE 0 END) AS gp_acquired_paid,
    SUM(CASE WHEN COALESCE(poc.is_paid, FALSE) = FALSE THEN 1 ELSE 0 END) AS gp_acquired_organic
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` g
  LEFT JOIN `quiqup.views.grandparent_utm_attribution` gua
    ON g.gac_grandparent_account_id = gua.grandparent_account_id
  LEFT JOIN `quiqup.views.definition_paid_organic_channel` poc
    ON LOWER(gua.attributed_utm_source) = LOWER(poc.utm_source)
    AND LOWER(gua.attributed_utm_medium) = LOWER(poc.utm_medium)
  WHERE DATE(g.gac_minimum_created_date) >= '2023-07-01'
    AND DATE(g.gac_minimum_created_date) < '2026-01-01'
  GROUP BY 1
),
monthly_spend AS (
  SELECT
    DATE_TRUNC(month, MONTH) AS month,
    SUM(spend_aed) AS spend
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE month >= '2023-07-01' AND month < '2026-01-01'
  GROUP BY 1
),
combined AS (
  SELECT
    md.month,
    COALESCE(ms.spend, 0) AS spend,
    md.gp_acquired_organic AS organic_gps,
    LAG(COALESCE(ms.spend, 0), 1) OVER (ORDER BY md.month) AS spend_lag1,
    LAG(COALESCE(ms.spend, 0), 2) OVER (ORDER BY md.month) AS spend_lag2,
    LAG(COALESCE(ms.spend, 0), 3) OVER (ORDER BY md.month) AS spend_lag3
  FROM monthly_data md
  LEFT JOIN monthly_spend ms ON md.month = ms.month
)
SELECT 'Same month' AS lag_period, ROUND(CORR(spend, organic_gps), 3) AS correlation FROM combined
UNION ALL
SELECT '1 month lag', ROUND(CORR(spend_lag1, organic_gps), 3) FROM combined WHERE spend_lag1 IS NOT NULL
UNION ALL
SELECT '2 month lag', ROUND(CORR(spend_lag2, organic_gps), 3) FROM combined WHERE spend_lag2 IS NOT NULL
UNION ALL
SELECT '3 month lag', ROUND(CORR(spend_lag3, organic_gps), 3) FROM combined WHERE spend_lag3 IS NOT NULL
```

**Interpretation:**
- If lag correlations are < 0.3 = no delayed brand awareness effect
- If lag correlations increase with lag = possible awareness buildup

---

## Analysis 2: Activation Rate & Revenue by Channel

```sql
-- =============================================================================
-- ACTIVATION RATE & REVENUE BY CHANNEL
-- =============================================================================
-- Compares paid vs organic account quality and revenue generation
-- =============================================================================

WITH all_accounts AS (
  SELECT
    a.id AS account_id,
    DATE(a.created_date) AS account_created_date,
    DATE_TRUNC(DATE(a.created_date), MONTH) AS acquisition_month,
    COALESCE(a.utm_source_c, attr.attributed_utm_source, '(direct)') AS utm_source,
    COALESCE(a.utm_medium_c, attr.attributed_utm_medium, '(none)') AS utm_medium
  FROM `quiqup.salesforce_current.accounts` a
  LEFT JOIN `quiqup.views.account_utm_attribution` attr
    ON a.id = attr.account_id
  WHERE a.is_deleted = FALSE
    AND DATE(a.created_date) >= '2025-07-01'
    AND DATE(a.created_date) < '2026-01-01'
),
with_channel AS (
  SELECT
    aa.*,
    COALESCE(poc.is_paid, FALSE) AS is_paid
  FROM all_accounts aa
  LEFT JOIN `quiqup.views.definition_paid_organic_channel` poc
    ON LOWER(aa.utm_source) = LOWER(poc.utm_source)
    AND LOWER(aa.utm_medium) = LOWER(poc.utm_medium)
),
with_activation AS (
  SELECT
    wc.*,
    CASE WHEN gp.gac_grandparent_account_id IS NOT NULL THEN 1 ELSE 0 END AS is_activated,
    gr.total_revenue_aed
  FROM with_channel wc
  LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gp
    ON wc.account_id = gp.gac_grandparent_account_id
  LEFT JOIN `quiqup.views.grandparent_revenue` gr
    ON wc.account_id = gr.grandparent_account_id
)
SELECT
  acquisition_month,
  CASE WHEN is_paid THEN 'Paid' ELSE 'Organic' END AS channel,
  COUNT(DISTINCT account_id) AS total_accounts,
  SUM(is_activated) AS activated_count,
  ROUND(100.0 * SUM(is_activated) / NULLIF(COUNT(DISTINCT account_id), 0), 1) AS activation_rate_pct,
  ROUND(SUM(COALESCE(total_revenue_aed, 0)), 0) AS total_revenue_aed
FROM with_activation
GROUP BY acquisition_month, is_paid
ORDER BY acquisition_month, is_paid DESC
```

---

## Analysis 3: Revenue Concentration (Pareto)

```sql
-- =============================================================================
-- REVENUE CONCENTRATION (PARETO ANALYSIS)
-- =============================================================================
-- Determines if organic revenue is concentrated in few "whale" accounts
-- =============================================================================

WITH account_revenue AS (
  SELECT
    gr.grandparent_account_id,
    gr.total_revenue_aed,
    COALESCE(poc.is_paid, FALSE) AS is_paid,
    COALESCE(poc.channel_type, 'Organic') AS channel_type
  FROM `quiqup.views.grandparent_revenue` gr
  LEFT JOIN `quiqup.views.grandparent_utm_attribution` gua
    ON gr.grandparent_account_id = gua.grandparent_account_id
  LEFT JOIN `quiqup.views.definition_paid_organic_channel` poc
    ON LOWER(gua.attributed_utm_source) = LOWER(poc.utm_source)
    AND LOWER(gua.attributed_utm_medium) = LOWER(poc.utm_medium)
  LEFT JOIN `quiqup.views.grandparent_account_created_date_and_first_order_delivered` g
    ON gr.grandparent_account_id = g.gac_grandparent_account_id
  WHERE DATE(g.gac_minimum_created_date) >= '2025-01-01'
    AND gr.total_revenue_aed > 0
),
channel_totals AS (
  SELECT
    channel_type,
    SUM(total_revenue_aed) AS total_channel_revenue,
    COUNT(DISTINCT grandparent_account_id) AS total_accounts
  FROM account_revenue
  GROUP BY channel_type
),
ranked_accounts AS (
  SELECT
    ar.channel_type,
    ar.grandparent_account_id,
    ar.total_revenue_aed,
    ct.total_channel_revenue,
    ct.total_accounts,
    ROW_NUMBER() OVER (PARTITION BY ar.channel_type ORDER BY ar.total_revenue_aed DESC) AS rank_in_channel,
    SUM(ar.total_revenue_aed) OVER (
      PARTITION BY ar.channel_type
      ORDER BY ar.total_revenue_aed DESC
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS cumulative_revenue
  FROM account_revenue ar
  JOIN channel_totals ct ON ar.channel_type = ct.channel_type
)
SELECT
  channel_type,
  total_accounts,
  ROUND(total_channel_revenue, 0) AS total_revenue_aed,
  MAX(CASE WHEN cumulative_revenue >= total_channel_revenue * 0.5 THEN NULL ELSE rank_in_channel END) + 1 AS accounts_for_50pct,
  MAX(CASE WHEN cumulative_revenue >= total_channel_revenue * 0.75 THEN NULL ELSE rank_in_channel END) + 1 AS accounts_for_75pct,
  MAX(CASE WHEN cumulative_revenue >= total_channel_revenue * 0.90 THEN NULL ELSE rank_in_channel END) + 1 AS accounts_for_90pct,
  MAX(CASE WHEN rank_in_channel = 1 THEN total_revenue_aed ELSE NULL END) AS top_1_account_revenue,
  ROUND(100.0 * MAX(CASE WHEN rank_in_channel = 1 THEN total_revenue_aed ELSE NULL END) / total_channel_revenue, 1) AS top_1_pct_of_channel
FROM ranked_accounts
GROUP BY channel_type, total_accounts, total_channel_revenue
ORDER BY total_revenue_aed DESC
```

**Interpretation:**
- If `accounts_for_75pct` < 5 = highly concentrated (whale risk)
- If `accounts_for_75pct` > 30 = well distributed (healthy)
- Compare organic vs paid distribution to assess quality
