---
name: outbound-health-check
description: "Outbound Taskforce health check methodology — plan targets, query templates, report structure, and traffic-light thresholds. Referenced by the /outbound-health-check command."
user-invocable: false
---

# Outbound Taskforce Health Check — Reference

Methodology and templates for the recurring outbound operations health check. This skill is consumed by the `/outbound-health-check` command.

## Plan Targets (Term 1, Jan-Apr 2026)

Source: `projects/outbound_taskforce/outbound_taskforce_project_context.md`

### Volume Targets

| Metric | Monthly Target | Weekly Target |
|--------|---------------|---------------|
| Outbound opportunities created | 20 | 5 |
| Outbound meetings (org-wide) | 60 | 15 |
| Meetings per BDM | 15 | ~4 |
| Meeting-to-opp ratio | 3:1 | — |

### Size Mix Targets (Monthly Outbound Opps)

| Segment | Target |
|---------|--------|
| Large | 4 |
| Medium | 3 |
| Small | 5 |
| Micro | 8 |
| **Total** | **20** |

### Conversion Assumptions

| Stage | Target Rate |
|-------|------------|
| Opp -> Signed (Micro) | 36% |
| Opp -> Signed (Large/Medium/Small) | 17% |
| Signed -> Activated | 75% |

### Revenue Ambition

| Metric | Value |
|--------|-------|
| 2026 target new acquisition revenue | ~5.6M AED/year |
| Target revenue per BDM | ~1.4M AED |
| Active BDMs assumed | 4 |
| Target activations/year | ~244 new clients |

## Data Model

### Outbound Classification

An opportunity or lead is "outbound" when its `lead_source` value appears in `quiqup.views.definition_lead_source` with `source_group = 'Outbound'`.

```sql
-- Canonical outbound filter (use as CTE in all queries)
WITH outbound_lead_sources AS (
  SELECT DISTINCT lead_source
  FROM `quiqup.views.definition_lead_source`
  WHERE source_group = 'Outbound'
)
```

### Key Tables

| Table | Use |
|-------|-----|
| `salesforce_current.opportunities` | Opp counts, size mix, conversion |
| `salesforce_current.leads` | Lead volume, status, classification, contact details |
| `salesforce_current.tasks` | Meeting logging (subject='meeting', status='Completed') |
| `salesforce_current.users` | BDM name resolution (tasks.owner_id -> users.id) |
| `views.definition_lead_source` | Outbound classification |
| `views.opportunities_convert_minus_2months` | Conversion rates |

### Meeting Detection

Meetings are logged as Tasks in Salesforce, NOT Events. A meeting is outbound if:
- Path A: `tasks.what_id -> opportunities.id` where opp has outbound lead_source
- Path B: `tasks.who_id -> leads.id` where lead has outbound lead_source (only if task not linked to an opp)

Full SQL: see `projects/outbound_taskforce/level1_executive_dashboard.sql` Card 1.

## Traffic-Light Thresholds

Use these to assign RAG status to each metric:

### Opportunity Volume (prorated pace)

| Status | Condition |
|--------|-----------|
| GREEN | >= 90% of prorated monthly target |
| AMBER | 70-89% of prorated monthly target |
| RED | < 70% of prorated monthly target |

### Meeting Volume (prorated pace)

| Status | Condition |
|--------|-----------|
| GREEN | >= 90% of prorated target |
| AMBER | 70-89% of prorated target |
| RED | < 70% of prorated target |
| GREY | Data unreliable (< 50% of BDMs logging meetings) |

### Size Mix (monthly)

| Status | Condition |
|--------|-----------|
| GREEN | Within +/- 25% of segment target |
| AMBER | 25-50% deviation from target |
| RED | > 50% deviation from target |

### Data Quality (unclassified leads)

| Status | Condition |
|--------|-----------|
| GREEN | < 15% unclassified |
| AMBER | 15-30% unclassified |
| RED | > 30% unclassified |

### Meeting Logging Compliance

| Status | Condition |
|--------|-----------|
| GREEN | All active BDMs logged >= 1 meeting in last 7 days |
| AMBER | 1-2 BDMs with zero meetings logged |
| RED | > 2 BDMs with zero meetings logged |

## Report Template

```markdown
# Outbound Taskforce — Health Check (YYYY-MM-DD)

## Executive Summary

| Metric | Status | Value | Target | Note |
|--------|--------|-------|--------|------|
| Opp Volume (MTD) | [RAG] | X/20 (Y% prorated pace) | 20/mo | |
| Meeting Volume (MTD) | [RAG] | X logged | 60/mo | |
| Size Mix | [RAG] | L:X M:X S:X Mi:X | L:4 M:3 S:5 Mi:8 | |
| Data Quality | [RAG] | X% unclassified | <15% | |
| Meeting Logging | [RAG] | X/Y BDMs logging | All BDMs | |

**Headline:** [1-2 sentence summary of the most important finding]

---

## 1. Opportunity Volume

### Monthly Trend

| Month | Target | Actual | % of Target |
|-------|--------|--------|-------------|
| Jan 2026 | 20 | X | X% |
| Feb 2026 (prorated) | X | X | X% |

### Weekly Breakdown (Current Month)

| Week | Opps Created | Cumulative |
|------|-------------|------------|
| W1 (1-7) | X | X |
| W2 (8-14) | X | X |
| ... | | |

---

## 2. Meeting Volume

### Monthly Trend

| Month | Target | Logged | Gap | Note |
|-------|--------|--------|-----|------|
| Jan | 60 | X | X | |
| Feb (prorated) | X | X | X | |

### BDM Logging Compliance

| BDM | Meetings Logged (Last 7d) | Meetings Logged (MTD) | Opps (MTD) | Logging? |
|-----|--------------------------|----------------------|------------|----------|

---

## 3. Size Mix

### Current Month

| Segment | Target | Actual | Deviation | Status |
|---------|--------|--------|-----------|--------|
| Large | 4 | X | X% | [RAG] |
| Medium | 3 | X | X% | [RAG] |
| Small | 5 | X | X% | [RAG] |
| Micro | 8 | X | X% | [RAG] |
| Unclassified | 0 | X | — | [flag if >0] |

### YTD Cumulative

[Same table structure for all months combined]

---

## 4. Conversion Pipeline

### Opp -> Signed (by cohort month, all-time)

| Cohort Month | Total Opps | Converted | Rate | Target Rate |
|-------------|-----------|-----------|------|-------------|

### Notes on Activation

[State whether Signed->Activated is measurable yet. If not, explain the blocker.]

---

## 5. Lead Pipeline

### Volume by Month

| Month | Leads Created | Disqualified | Contacted | In Conversation | Open |
|-------|-------------|-------------|-----------|----------------|------|

### Disqualification Analysis (Current Month)

| Reason | Count | % of Disqualified |
|--------|-------|-------------------|

---

## 6. Data Quality & Blockers

### Unclassified Leads

| BDM | Unclassified | Total | % Unclassified | Change vs Last Check |
|-----|-------------|-------|----------------|---------------------|

### Open Blockers

| Issue | Owner | Impact | Priority | Status vs Last Check |
|-------|-------|--------|----------|---------------------|

---

## 7. Recommended Actions

| # | Action | Owner | Priority | Rationale |
|---|--------|-------|----------|-----------|

---

## 8. Changes Since Last Health Check

| Metric | Last Check (DATE) | This Check | Direction |
|--------|-------------------|------------|-----------|

---

*Generated: YYYY-MM-DD | Data source: Quiqup BigQuery + Salesforce | Dashboard: https://metabase.dev.quiq.ly/dashboard/518*
```

## Comparison Logic

When a previous health check exists, calculate deltas:
- **Opp volume**: month-over-month trend
- **Unclassified leads**: absolute change (should be decreasing)
- **Blocker status**: resolved / still open / new
- **Meeting logging**: improving or degrading
- **Size mix**: convergence toward or divergence from targets

## Files

| File | Purpose |
|------|---------|
| `projects/outbound_taskforce/outbound_taskforce_project_context.md` | Plan targets and funnel math |
| `projects/outbound_taskforce/TODO.md` | Open action items |
| `projects/outbound_taskforce/metric_status.md` | Dashboard card status |
| `projects/outbound_taskforce/unclassified_leads_2026.md` | Lead-level unclassified list |
| `projects/outbound_taskforce/dashboard_plan.md` | Dashboard architecture |
| `projects/outbound_taskforce/level1_executive_dashboard.sql` | Validated SQL for Level 1 |
| `projects/outbound_taskforce/level3_bdm_weekly.sql` | SQL for BDM weekly view |
| `projects/outbound_taskforce/health_checks/` | Historical health check reports |
