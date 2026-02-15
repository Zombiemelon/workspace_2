---
name: outbound-health-check
description: "Run the weekly Outbound Taskforce health check — pull live data, compare against plan targets, flag problems, and produce an actionable status report."
---

# Outbound Taskforce Health Check

Run a structured operational health check on the Outbound Taskforce. Compare live Salesforce/BigQuery data against the plan targets and flag deviations, blockers, and data quality issues.

## Before You Start

1. Read the skill reference: `.claude/skills/outbound-health-check/SKILL.md`
2. Read the project context: `projects/outbound_taskforce/outbound_taskforce_project_context.md`
3. Read the current TODO: `projects/outbound_taskforce/TODO.md`
4. Read the metric status: `projects/outbound_taskforce/metric_status.md`
5. Read the most recent health check report in `projects/outbound_taskforce/health_checks/` for comparison

## What To Do

Use the `outbound-taskforce` subagent (Task tool with `subagent_type: "outbound-taskforce"`) to pull live data. Give it the specific queries listed in the skill reference.

Then produce the health check report using the exact template from the skill reference.

### Data Collection (delegate to outbound-taskforce agent)

Launch the outbound-taskforce agent with this prompt:

> Pull the following outbound taskforce metrics for the health check. Use `views.definition_lead_source` with `source_group = 'Outbound'` for all outbound classification. All queries should filter `is_deleted = FALSE`.
>
> 1. **Opportunities this month**: Count outbound opps created since 1st of current month. Also calculate prorated pace vs 20/month target.
> 2. **Opportunities by month**: Monthly outbound opp counts for 2026 YTD.
> 3. **Meetings this month and by week**: Outbound meetings (tasks where subject='meeting', status='Completed') linked to outbound opps or leads. Break down by week.
> 4. **Size mix**: Outbound opps by `client_classification_c` (Large/Medium/Small/Micro/NULL) for current month and YTD.
> 5. **BDM leaderboard**: Per-BDM meetings + opps for last 7 days and MTD.
> 6. **Lead volume and status**: Count of outbound leads created in 2026, by status (Open, Contacted, Disqualified, etc.) and by month.
> 7. **Unclassified leads**: Count of outbound leads where `client_classification_c IS NULL`, by owner.
> 8. **Conversion rates**: From `views.opportunities_convert_minus_2months`, outbound opp→signed conversion rate by month.
> 9. **Queue leads**: Count of outbound leads with owner = 'Salesforce Queue' or similar, unassigned.
> 10. **Disqualification reasons**: Top reasons from `reason_for_disqualification_c` for disqualified outbound leads this month.

### Report Assembly

After receiving data, produce the report using the template in the skill reference. Compare every metric against:
- **Plan targets** (from project context)
- **Previous health check** (from `projects/outbound_taskforce/health_checks/`)

### Report Output

Save the report to: `projects/outbound_taskforce/health_checks/health_check_YYYY-MM-DD.md`

Present the executive summary to the user inline.

## Arguments

- `--quick` — Skip detailed breakdowns, just show the 5 headline metrics and traffic-light status
- `--bdm <name>` — Focus on a single BDM's performance
- `--compare` — Side-by-side with the previous health check, highlighting changes
