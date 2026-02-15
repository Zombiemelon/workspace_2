---
name: marketing-funnel-analysis
description: "Marketing funnel performance analysis from spend to revenue. Covers monthly overview, multi-dimensional slicing (paid/organic, channel, client size, region, campaign, lead source), and drill-down to individual clients. Use when analyzing marketing funnel performance, spend efficiency, conversion rates by stage, campaign ROI, acquisition cohort economics, or channel contribution. Also use when the user says 'funnel report', 'marketing performance', 'spend to revenue', 'CAC analysis', or 'cohort ROI'."
user-invocable: false
---

# Marketing Funnel Analysis

## Purpose & Scope

End-to-end marketing funnel analysis from Google Ads spend to invoiced revenue. Produces standardized reports with MoM comparison, anomaly detection, and actionable recommendations.

**In scope:** Website traffic, leads, GP acquisition, activation, revenue, unit economics (CAC, LTV, ROI, break-even), paid/organic split, channel attribution.

**Out of scope:** Outbound-specific pipeline analysis (use `outbound-health-check` skill). Individual campaign optimization (use `bigquery-reference` + ad group queries directly). Retention/churn analysis (use `funnel-methodology` skill retention section).

## Data Foundation

### Primary View

`views.marketing_funnel_grandparent_monthly` is the **single source of truth** for monthly marketing performance. It pre-aggregates traffic, leads, spend, GP acquisition, activation, revenue, margin, and unit economics into 1 row/month.

**Use this view for the monthly overview.** Only query raw tables when slicing by a dimension the view doesn't support.

### Funnel Stage Map

| # | Stage | Data Source | Key Column | Grain |
|---|-------|-------------|------------|-------|
| 1 | Marketing Spend | `views.marketing_funnel_grandparent_monthly` | `google_ads_spend_aed` | Monthly |
| 2 | Website Traffic | Same view | `unique_visitors` | Monthly |
| 3 | High-Intent Visitors | Same view | `high_intent_visitors` | Monthly |
| 4 | Website Leads (SF deduped) | Same view | `sf_contact_form_website_source_leads_deduped` | Monthly |
| 5 | Grandparents Acquired | Same view | `grandparents_acquired` | Monthly (cohort) |
| 6 | Paid GP Acquired | Same view | `gp_acquired_paid` | Monthly (cohort) |
| 7 | Organic GP Acquired | Same view | `gp_acquired_organic` | Monthly (cohort) |
| 8 | Activated (First Order) | Same view | `cohort_ever_activated` | Monthly (cohort) |
| 9 | Cohort Revenue | Same view | `cohort_lifetime_revenue_aed` | Monthly (cohort, cumulative) |
| 10 | Unit Economics | Same view | `cost_per_gp_acquired`, `ltv_per_gp_acquired`, `cohort_roi`, `breakeven_months_paid` | Monthly (cohort) |

For dimensional slicing beyond the view, rebuild from raw tables:

| Dimension | Raw Source | Join Pattern |
|-----------|-----------|-------------|
| **Paid/Organic** | `views.grandparent_utm_attribution` + `views.definition_paid_organic_channel` | Priority join: exact source+medium > wildcard medium > default organic |
| **Channel** | `views.definition_traffic_channel` | Join on source+medium from attribution |
| **Campaign** | `views.definition_utm_google_ads_mapping` | Join on `attributed_utm_campaign` |
| **Client Size** | `salesforce_current.opportunities` via `views.opportunities_convert_minus_2months` | Join on grandparent_account_id, group by `client_classification_c` |
| **Lead Source** | `views.grandparent_lead_source_attribution` | Join on grandparent_account_id, group by `source_group` |
| **Region** | `views.definition_campaign_marketing_bucket` | Join on campaign_name, group by `marketing_bucket` |
| **New/Existing** | `views.opportunities_convert_minus_2months` | Filter by `client_type_classification` = 'N' or 'E' |

See `references/dimension-guide.md` for full join patterns and gotchas (Phase 2).

### Known Data Quality Flags

| Issue | Months Affected | Impact |
|-------|-----------------|--------|
| UTM tracking outage | Jul 2025 | GP acquisition/attribution undercounted |
| GA4 tracking outage | Oct-Nov 2025 | Website visitors and leads undercounted |
| Attribution coverage | All months | Only ~31% of accounts have UTM data; ~50% of GPs |
| Cohort maturity | Last 3 months | ROI and break-even unreliable — cohorts need 6+ months to mature |
| Currency | All | Google Ads `spend_usd` column is actually AED (mislabeled) |
| SSUP accounts | All | Self-signup parent `0010800003I4PcsAAF` — 21,563 children treated individually |

**Always disclose** which flags affect the current analysis period.

## Analysis Workflow

Follow this decision tree for every funnel analysis request:

### Step 1: DETERMINE SCOPE

Before querying, confirm:
- **Period:** What months? Default: last 6 complete months + current MTD
- **Granularity:** Monthly overview (default), dimensional slice, or client drill-down?
- **Dimension:** If slicing, which dimension? (paid/organic, channel, size, region, campaign, source)
- **Client type:** All opportunities, or new clients only (`client_type_classification = 'N'`)? Default: ask if unclear.

If any of these are ambiguous, propose your assumption: *"I'll show the last 6 months, total funnel (all clients), paid vs organic split. Correct?"*

### Step 2: MONTHLY OVERVIEW

**Query:** `SELECT * FROM views.marketing_funnel_grandparent_monthly WHERE month >= '{START_DATE}' ORDER BY month`

**Process:**
1. Calculate MoM % change for every metric
2. Apply RAG thresholds (see below) to flag anomalies
3. Format into the Monthly Funnel Table (see report template)
4. Calculate period averages for trend context

**Cross-check:** Verify `grandparents_acquired` x `ltv_per_gp_acquired` approximately equals `cohort_lifetime_revenue_aed`. If >5% discrepancy, investigate before presenting.

### Step 3: DIMENSIONAL SLICING (when requested)

Consult `references/dimension-guide.md` for the specific dimension's join pattern and SQL template (Phase 2).

**General approach:**
1. Start from `views.grandparent_account_created_date_and_first_order_delivered` (all GPs, not just attributed)
2. LEFT JOIN the dimension's definition view
3. LEFT JOIN `views.grandparent_revenue` for revenue
4. GROUP BY month + dimension column
5. Calculate same metrics as monthly overview, per segment
6. Apply Contribution Analysis playbook from `analysis-playbooks` skill

**Flag concentration risk:** If top segment > 50% of total, or #1 account > 15% of segment revenue, call it out.

### Step 4: CLIENT DRILL-DOWN (when requested)

From any dimensional slice, drill to individual grandparent accounts:
1. Remove the GROUP BY
2. Add: `grandparent_account_name`, `acquisition_date`, `first_delivered_order_date`, `total_revenue_aed`, attribution fields
3. ORDER BY `total_revenue_aed` DESC
4. LIMIT 20 (unless user requests more)

Present as a ranked table with: rank, GP name, acquired date, channel, first order date, revenue, status (active/churned).

## Anomaly Thresholds

Apply RAG (Red/Amber/Green) status to headline metrics:

| Metric | GREEN | AMBER | RED |
|--------|-------|-------|-----|
| GP Acquisition MoM | Within +/- 20% | 20-40% swing | >40% swing |
| Activation Rate | >60% | 40-60% | <40% |
| ROI (6+ month cohort) | >1.0 | 0.5-1.0 | <0.5 |
| Attribution Coverage | >40% | 25-40% | <25% |
| Spend MoM Change | Within +/- 30% | 30-50% swing | >50% swing |
| CAC MoM Change | Within +/- 25% | 25-50% swing | >50% swing |
| Break-Even (paid, 6+ month) | <12 months | 12-24 months | >24 months or negative margin |

**Cohort maturity caveat:** Do NOT apply ROI or break-even thresholds to cohorts younger than 6 months. Instead, note: *"Cohort too young for reliable ROI assessment."*

## Output Format

Use the full template from `references/report-template.md`. The key sections:

```
# Marketing Funnel Report -- {PERIOD}

## Executive Summary
(7-12 metrics with RAG status, 1-2 sentence headline)

## Monthly Funnel Table
(Stage-by-stage: spend, traffic, leads, GPs, activation, revenue, ROI — with MoM%)

## Unit Economics by Cohort
(CAC, LTV, margin, ROI, break-even per cohort month)

## [Dimension] Breakdown (if --by specified)
(Segment table + concentration analysis)

## Data Quality Notes
(Which flags affect this report)

## Recommended Actions
(2-3 specific items with rationale)
```

**Executive Summary is mandatory.** Even for deep-dive requests, always lead with the summary.

## Composability

This skill works alongside existing skills — reference, don't duplicate:

| Skill | What it provides to this analysis |
|-------|----------------------------------|
| `funnel-methodology` | Stage definitions, conversion windows (use +2mo dashboard vs all-time), cohort rules, retention definitions |
| `analysis-playbooks` | Decomposition (when a metric changes), Pacing (are we on track?), Contribution (what's driving growth?), ROI (is spend worth it?) |
| `bigquery-reference` | Table schemas, canonical join keys, MCP tool names, spend verification query, view gotchas |

When a funnel question naturally leads to "why did this change?" or "are we on track?", chain to the relevant playbook from `analysis-playbooks`.

## Reference Files

| File | Purpose | Phase |
|------|---------|-------|
| `references/report-template.md` | Full markdown report template with all sections | 1 |
| `references/dimension-guide.md` | Dimension definitions, join patterns, SQL templates, coverage warnings | 2 |
| `references/sql-templates.md` | Parameterized SQL for dimensional slicing and drill-down | 2 |
