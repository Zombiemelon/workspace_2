---
name: funnel-report
description: "Generate a marketing funnel performance report -- monthly overview from spend to revenue with optional dimensional slicing and client drill-down."
---

# Marketing Funnel Report

Generate a structured marketing funnel performance report using live BigQuery data. Covers the full pipeline: Google Ads spend, website traffic, leads, GP acquisition, activation, revenue, and unit economics.

## Before You Start

1. Read the skill reference: `.claude/skills/marketing-funnel-analysis/SKILL.md`
2. Read the report template: `.claude/skills/marketing-funnel-analysis/references/report-template.md`
3. Read the BigQuery reference: `.claude/skills/bigquery-reference/SKILL.md` (for view schemas and gotchas)

## What To Do

### Step 1: Determine Scope

Parse the user's request and any arguments to determine:

- **Period:** Default = last 6 complete months. Override with `--period`.
- **Dimension:** None (overview) or a specific slice. Override with `--by`.
- **Depth:** Overview only, or include client drill-down. Override with `--drill`.
- **Format:** Full report or executive summary only. Override with `--quick`.

If the period is ambiguous, state your assumption: *"Showing Jul 2025 - Dec 2025 (last 6 complete months). Adjust?"*

### Step 2: Pull Monthly Overview Data

Use the `bigquery-analyst` agent (Task tool with `subagent_type: "bigquery-analyst"`) to query the data.

**Primary query:**
```sql
SELECT *
FROM `quiqup.views.marketing_funnel_grandparent_monthly`
WHERE month >= '{START_DATE}'
ORDER BY month
```

This single view contains: spend, visitors, high-intent visitors, leads, GP acquisition (total/paid/organic), activation, revenue (total/paid/organic), margin, unit economics (CAC, LTV, ROI, break-even).

**Cross-check:** Verify `grandparents_acquired x ltv_per_gp_acquired ≈ cohort_lifetime_revenue_aed`. Flag if >5% discrepancy.

### Step 3: Calculate MoM Changes

For every metric in the Monthly Funnel Table:
1. Calculate MoM % change: `(current - prior) / prior * 100`
2. Apply RAG thresholds from the skill reference (Anomaly Thresholds section)
3. Flag metrics that breach AMBER or RED thresholds

### Step 4: Dimensional Slicing (if --by specified)

**IMPORTANT:** The `marketing_funnel_grandparent_monthly` view is pre-aggregated to 1 row/month. It CANNOT be sliced by dimension. For dimensional analysis, you must query the underlying tables.

**Base approach for all dimensions:**
1. Start from `views.grandparent_account_created_date_and_first_order_delivered` (all GPs)
2. LEFT JOIN the dimension's definition view (see SKILL.md Funnel Stage Map)
3. LEFT JOIN `views.grandparent_revenue` for revenue
4. GROUP BY month + dimension column
5. Calculate per-segment: GP count, activation rate, revenue, ROI

Consult `references/dimension-guide.md` for the specific JOIN pattern (Phase 2 — if this file doesn't exist yet, construct the query following the patterns in `bigquery-reference` skill).

After getting dimensional data, apply the **Contribution Analysis** playbook from `analysis-playbooks` skill:
- Rank segments by size
- Calculate cumulative %
- Flag concentration risk (top segment > 50% or #1 account > 15%)

### Step 5: Client Drill-Down (if --drill specified)

From the dimensional query, add individual GP fields:
- `grandparent_account_name`, `acquisition_date`, `first_delivered_order_date`
- `total_revenue_aed`, attribution fields (UTM source, campaign)
- ORDER BY revenue DESC, LIMIT 20

### Step 6: Assemble Report

Use the report template from `references/report-template.md`:

1. **Executive Summary** — 12 headline metrics with RAG status + 1-2 sentence headline
2. **Monthly Funnel Table** — All months with stage-to-stage rates
3. **Unit Economics** — CAC, LTV, ROI, break-even per cohort
4. **Dimension Breakdown** — Only if `--by` was specified
5. **Top Clients** — Only if `--drill` was specified
6. **Data Quality Notes** — Flag known issues from SKILL.md
7. **Recommended Actions** — 2-3 specific, data-backed items

### Step 7: Present

- **Always** present the Executive Summary inline to the user
- If `--quick` was specified, stop after the Executive Summary
- For full reports, present inline if compact enough, or save to file:
  `projects/marketing_funnel/reports/funnel_report_YYYY-MM-DD.md`

## Arguments

| Argument | Description | Default | Example |
|----------|-------------|---------|---------|
| `--period <range>` | Time period to analyze | Last 6 complete months | `--period 2025-h2`, `--period last-3`, `--period jan-2026` |
| `--by <dimension>` | Slice by dimension | No slicing (totals only) | `--by paid-organic`, `--by channel`, `--by size`, `--by region`, `--by campaign`, `--by source` |
| `--drill` | Include top-20 client drill-down | Off | `--drill` |
| `--quick` | Executive summary only (12 metrics + RAG) | Full report | `--quick` |
| `--compare <period>` | Side-by-side with another period | No comparison | `--compare 2025-h1` |
| `--cohort <month>` | Single cohort lifetime trajectory | All cohorts | `--cohort 2025-09` |

**Combining arguments:** Arguments can be combined. Example: `/funnel-report --period 2025-h2 --by paid-organic --quick` produces a quick executive summary of H2 2025 split by paid/organic.

**Phase 2 arguments** (`--by` dimensions) require the `references/dimension-guide.md` file. If it doesn't exist yet, construct queries using patterns from the `bigquery-reference` skill.

**Phase 3 arguments** (`--drill`, `--cohort`) require the `references/sql-templates.md` file. If it doesn't exist yet, construct queries using the drill-down approach described in the SKILL.md.
