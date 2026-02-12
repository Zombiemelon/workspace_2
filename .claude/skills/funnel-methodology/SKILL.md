---
name: funnel-methodology
description: Quiqup B2B funnel stage definitions, cohort construction rules, conversion windows, retention/churn definitions, and standard queries. Use when analyzing lead-to-customer funnels, cohort performance, or retention metrics.
user-invocable: false
---

# Funnel & Cohort Methodology

Canonical definitions for measuring the Quiqup B2B acquisition and retention funnel. Every stage, transition, and cohort rule below maps to a specific data source.

## Funnel Stages

The Quiqup B2B funnel has 6 stages. Each stage is defined by a specific field/event in the data, not by subjective judgment.

| Stage | Definition | Data Source | Key Field |
|-------|-----------|-------------|-----------|
| **1. Lead** | Salesforce lead record created | `salesforce_current.leads` | `created_date` |
| **2. Qualified Lead** | Lead with `is_converted = TRUE` or has matching opportunity | `salesforce_current.leads` | `is_converted`, `converted_opportunity_id` |
| **3. Opportunity** | Salesforce opportunity created (linked to account) | `salesforce_current.opportunities` | `created_date`, `account_id` |
| **4. Won (Deal Done)** | Opportunity stage = 'Deal Done' | `salesforce_current.opportunities` | `stage_name = 'Deal Done'` |
| **5. Signed (Parent Created)** | Parent account created in SF hierarchy = contract signed | `views.opportunities_convert_minus_2months` | `is_converted = TRUE` |
| **6. Activated** | First delivered order at grandparent level | `views.grandparent_account_created_date_and_first_order_delivered` | `first_delivered_order_date IS NOT NULL` (exclude `2030-01-01` placeholder) |

### Stage Transition Rules

| Transition | What triggers it | Measurement |
|-----------|-----------------|-------------|
| Lead -> Qualified | Lead converts in Salesforce (creates contact + optionally opp) | `leads.is_converted = TRUE` |
| Qualified -> Opportunity | Opportunity record created linked to the account | `opportunities.created_date` |
| Opportunity -> Won | Stage changes to 'Deal Done' | `opportunities.stage_name = 'Deal Done'` |
| Won -> Signed | Parent account created within reporting window | `is_converted = TRUE` on opp view |
| Signed -> Activated | First order delivered | `first_delivered_order_date NOT IN (NULL, '2030-01-01')` |

### Accounts That Skip Stages

Some accounts enter the funnel without a lead (e.g., self-signup, direct referral). Handle these by:
- Counting them in the stage where they first appear (usually Opportunity or Activated)
- Flagging them separately: *"N accounts entered at Opportunity stage with no prior lead"*
- For funnel conversion rate calculations, only use accounts that entered at the top of the funnel being measured

### Deal Lost Handling

- `stage_name = 'Deal Lost'` removes an opportunity from the "converted" count
- A Deal Lost opp is **not deleted** — it remains in the data with `is_deleted = FALSE`
- `stage_name` is mutable — a lost deal can be reopened. Snapshot comparisons will drift.
- For funnel analysis: count Deal Lost as "exited at Opportunity stage" unless the user asks otherwise

## Conversion Windows

| Metric | Window | Source |
|--------|--------|--------|
| Opp -> Signed (dashboard) | +2 months from `opp_created_month` | `views.opportunities_convert_minus_2months.converted_by_reporting_month` |
| Opp -> Signed (all-time) | No window — if parent exists and not Deal Lost, it's converted | `views.opportunities_convert_minus_2months.is_converted` |
| Signed -> Activated | No standard window — measure as time-to-first-order | `first_delivered_order_date - account_created_date` |
| Lead -> Opp | Recommended: 90 days | Manual calculation: `opp.created_date - lead.created_date` |

### Dashboard vs All-Time Conversion

The +2 month window (`converted_by_reporting_month`) is used on the dashboard to give each cohort a consistent evaluation period. For business analysis, **prefer `is_converted`** (all-time) unless the user specifically asks about dashboard-aligned rates.

**Always state which conversion definition you're using.**

## Cohort Construction

### Primary Cohort Dimension: Opportunity Created Month

The default cohort grouping for Quiqup is by **opportunity created month** (`opp_created_month`). This is the standard used in:
- The conversion rate dashboard
- Monthly performance reviews
- The `opportunities_convert_minus_2months` view

### Alternative Cohort Dimensions

| Dimension | When to use | Source |
|-----------|-------------|--------|
| Opp created month | Default for conversion analysis | `opp_created_month` |
| Account created month | For acquisition volume trends | `salesforce_current.accounts.created_date` |
| First order month | For activation/revenue cohorts | `first_delivered_order_date` |
| Campaign cohort | For marketing ROI | `grandparent_utm_attribution.attributed_utm_campaign` |
| Lead source cohort | For channel analysis | `grandparent_lead_source_attribution.source_group` |

### Cohort Revenue Attribution

When attributing revenue to a cohort:
1. **Always clarify New vs Existing** — `client_type_classification = 'N'` for new business only
2. **Use grandparent-level revenue** — `views.grandparent_revenue` for deduplicated lifetime revenue
3. **Time-bound the revenue** — Specify "revenue in first 3/6/12 months" or "lifetime to date"
4. **Watch for pre-existing revenue** — Existing clients (`'E'`) have revenue history that pre-dates the opportunity. Including it inflates cohort ROI.

## Retention & Churn Definitions

### Revenue Retention (B2B Context)

For Quiqup's B2B model, retention is measured at the **grandparent account level** using invoice activity.

| Metric | Definition | Measurement |
|--------|-----------|-------------|
| **Active** | Grandparent has at least 1 paid/overdue invoice with `start_date` in the measurement month | `invoicer_current.invoices` grouped by GP |
| **Churned** | Previously active GP with no invoices for 3+ consecutive months | Gap analysis on monthly invoice presence |
| **Reactivated** | Churned GP that resumes invoicing | Invoice appears after 3+ month gap |
| **Net Revenue Retention (NRR)** | `(Revenue from same GPs in period 2) / (Revenue from those GPs in period 1) x 100` | Compare same-GP cohort across periods |
| **Gross Revenue Retention (GRR)** | NRR but capping per-GP growth at 100% (no upsell credit) | Same as NRR but `MIN(period2_revenue, period1_revenue)` |

### Churn Analysis Steps

1. Build a monthly GP activity flag: active/inactive per month
2. Identify first inactive month after last active month
3. Mark as churned if inactive for 3+ consecutive months
4. Calculate churn rate: `churned_GPs / active_GPs_in_prior_month`
5. Segment by account size, service offering, lead source to find patterns

### Important Caveats

- **Seasonal clients** may look like churn but are actually seasonal pauses. Check Service_Offering_c and historical pattern before labeling as churned.
- **Invoice timing** can cause false churn signals — a client billed quarterly will show 2 "inactive" months between invoices. Use a 3-month window minimum.
- **SSUP accounts** (`NOT LIKE '%SSUP%'`) should be analyzed separately — their churn pattern differs from managed accounts.

## Standard Queries

### Full Funnel Counts (Monthly)

```sql
-- Lead counts by month
SELECT DATE_TRUNC(DATE(created_date), MONTH) AS month, COUNT(*) AS leads
FROM salesforce_current.leads
WHERE is_deleted = FALSE
GROUP BY 1

-- Opportunity counts by month (validated against dashboard)
SELECT DATE_TRUNC(DATE(created_date), MONTH) AS month, COUNT(*) AS opps
FROM salesforce_current.opportunities
WHERE is_deleted = FALSE
GROUP BY 1

-- Conversion by opp cohort (all-time)
SELECT
  opp_created_month,
  COUNT(*) AS total_opps,
  COUNTIF(is_converted) AS converted,
  ROUND(COUNTIF(is_converted) / COUNT(*) * 100, 1) AS conversion_rate
FROM views.opportunities_convert_minus_2months
WHERE is_deleted = FALSE
GROUP BY 1
ORDER BY 1
```

### Cohort Revenue (New Clients Only)

```sql
SELECT
  o.opp_created_month,
  COUNT(DISTINCT o.grandparent_account_id) AS gp_count,
  SUM(gr.total_revenue) AS cohort_revenue
FROM views.opportunities_convert_minus_2months o
JOIN views.grandparent_revenue gr
  ON o.grandparent_account_id = gr.grandparent_account_id
WHERE o.is_deleted = FALSE
  AND o.client_type_classification = 'N'
  AND o.is_converted = TRUE
GROUP BY 1
ORDER BY 1
```

### Monthly GP Activity (for Retention)

```sql
SELECT
  gp.grandparent_account_id,
  DATE_TRUNC(i.start_date, MONTH) AS activity_month,
  SUM(i.total_amount - COALESCE(i.tax_amount, 0)) AS net_revenue
FROM invoicer_current.invoices i
JOIN invoicer_current.accounts ia ON i.account_id = ia.id
JOIN views.true_grandparent_account gp ON ia.salesforce_id = gp.account_id
WHERE i.state IN ('paid', 'overdue')
  AND i.record_deleted = FALSE
GROUP BY 1, 2
```
