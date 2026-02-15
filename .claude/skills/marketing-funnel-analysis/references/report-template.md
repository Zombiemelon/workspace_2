# Marketing Funnel Report Template

Use this template for all `/funnel-report` outputs. Replace `{PLACEHOLDERS}` with actual values.

---

# Marketing Funnel Report -- {PERIOD}

## Executive Summary

| Metric | Current | Prior | MoM % | Status |
|--------|---------|-------|-------|--------|
| Google Ads Spend (AED) | {val} | {val} | {%} | {RAG} |
| Unique Visitors | {val} | {val} | {%} | |
| High-Intent Visitors | {val} | {val} | {%} | |
| SF Leads (deduped) | {val} | {val} | {%} | |
| GPs Acquired | {val} | {val} | {%} | {RAG} |
| - Paid | {val} | {val} | {%} | |
| - Organic | {val} | {val} | {%} | |
| Activation Rate | {%} | {%} | {pp} | {RAG} |
| Cohort Lifetime Revenue (AED) | {val} | {val} | {%} | |
| CAC - All (AED) | {val} | {val} | {%} | {RAG} |
| ROI (all) | {val} | {val} | {pp} | {RAG} |
| Break-Even Months (paid) | {val} | {val} | {delta} | {RAG} |

**Headline:** {1-2 sentence summary of the most important finding. Quantified, with business implication.}

**Attribution Note:** {X}% of GPs in this period have UTM attribution. Unattributed GPs are classified as organic by default.

---

## Monthly Funnel Table

| Month | Spend (AED) | Visitors | HI Visitors | SF Leads | GPs Acquired | Paid | Organic | Activated | Act. Rate | Revenue (AED) | ROI |
|-------|------------|----------|-------------|----------|-------------|------|---------|-----------|-----------|---------------|-----|
| {M1} | | | | | | | | | | | |
| {M2} | | | | | | | | | | | |
| {M3} | | | | | | | | | | | |
| {M4} | | | | | | | | | | | |
| {M5} | | | | | | | | | | | |
| {M6} | | | | | | | | | | | |
| **Avg** | | | | | | | | | | | |

### Stage-to-Stage Conversion Rates

| Transition | Rate | Trend | Note |
|-----------|------|-------|------|
| Visitor -> HI Visitor | {%} | {up/down/flat} | |
| HI Visitor -> SF Lead | {%} | {up/down/flat} | |
| Spend -> GP Acquired (CAC) | {AED} | {up/down/flat} | Lower = better |
| GP Acquired -> Activated | {%} | {up/down/flat} | |

---

## Unit Economics by Cohort

| Cohort Month | GPs | CAC All (AED) | CAC Paid (AED) | LTV/GP (AED) | Margin/GP (AED) | ROI | ROI (paid) | Break-Even Mo | Cohort Age |
|-------------|-----|--------------|----------------|-------------|----------------|-----|------------|--------------|------------|
| {M1} | | | | | | | | | |
| {M2} | | | | | | | | | |
| {M3} | | | | | | | | | |
| {M4} | | | | | | | | | |
| {M5} | | | | | | | | | |
| {M6} | | | | | | | | | |

**Margin assumption:** Revenue x 25% gross margin.
**Agency fee:** 3,600 AED/month (included in `breakeven_months_paid_with_agency` column if available).
**Cohort maturity warning:** Cohorts younger than 6 months have unreliable ROI and break-even figures.

---

## {DIMENSION_NAME} Breakdown

*This section appears when `--by {dimension}` is specified.*

| {Dimension} | GPs Acquired | % of Total | Revenue (AED) | ROI | Activation Rate | vs Prior Period |
|-------------|-------------|-----------|---------------|-----|----------------|----------------|
| {Segment 1} | | | | | | |
| {Segment 2} | | | | | | |
| {Segment 3} | | | | | | |
| **Total** | | **100%** | | | | |

### Concentration Analysis

- **Top segment:** {name} at {X}% of total GPs acquired
- **Revenue concentration:** Top 3 segments account for {X}% of cohort revenue
- **Risk level:** {Low / Moderate / High}
- **Notable shifts:** {Which segments gained or lost share vs prior period}

---

## Top Clients

*This section appears when `--drill` is specified.*

| # | GP Name | Acquired | Channel | First Order | Revenue (AED) | Orders | Status |
|---|---------|----------|---------|-------------|---------------|--------|--------|
| 1 | | | | | | | |
| 2 | | | | | | | |
| ... | | | | | | | |
| 20 | | | | | | | |

**Status:** Active = invoice in last 3 months. At-risk = no invoice 2-3 months. Churned = no invoice 3+ months.

---

## Data Quality Notes

| Flag | Impact | Months Affected | Severity |
|------|--------|-----------------|----------|
| UTM tracking outage | GP attribution undercounted | Jul 2025 | Medium |
| GA4 tracking outage | Visitor and lead counts undercounted | Oct-Nov 2025 | High |
| Attribution coverage | Only {X}% of GPs have UTM data | All months | Medium |
| Cohort maturity | ROI/break-even unreliable for recent cohorts | Last 3 months | Low |

**NULL handling:** Missing UTM = Organic. Missing client_classification = in totals, excluded from size segments. Missing first_delivered_order_date or 2030-01-01 = not activated.

---

## Recommended Actions

| # | Action | Rationale | Priority |
|---|--------|-----------|----------|
| 1 | {Specific action} | {Data-backed reasoning} | {High/Medium/Low} |
| 2 | {Specific action} | {Data-backed reasoning} | {High/Medium/Low} |
| 3 | {Specific action} | {Data-backed reasoning} | {High/Medium/Low} |

---

*Generated: {DATE} | Source: views.marketing_funnel_grandparent_monthly*
*Skill: marketing-funnel-analysis v1.0 | Confidence: {High/Medium/Low} -- {reason}*
