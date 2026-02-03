# Quiqup Sub-Agents Directory

## How This Works

The main Quiqup agent (`../CLAUDE.md`) can delegate tasks to these specialists. Each sub-agent has focused expertise and specific daily tasks.

---

## Available Sub-Agents

| Agent | File | Specialty | When to Use |
|-------|------|-----------|-------------|
| **Inbound Leads** | `inbound_leads_agent.md` | Lead monitoring, account creation, marketing spend | Daily lead checks, anomaly detection, marketing ROI questions |
| **Outbound Analytics** | `outbound_analytics_agent.md` | Outbound funnel, sales metrics, conversions | Outbound OKR tracking, sales pipeline analysis |
| **BigQuery Analyst** | `bigquery_analyst_agent.md` | BigQuery MCP queries, Quiqup data warehouse | Any query requiring live data from BigQuery |

---

## Sub-Agent Template

When creating a new sub-agent, use this structure:

```markdown
# Role
[One sentence: who is this agent and what do they oversee]

# Tools
[List of MCPs/tools this agent uses]

# Knowledge
[Link to relevant knowledge_base files]

# Daily Tasks
[Numbered list of recurring checks/tasks]

# Escalation
[When to escalate to main agent or user]
```

---

## Adding a New Sub-Agent

1. Create `./agents/[name]_agent.md` using the template above
2. Update this index file with the new agent
3. Update `../CLAUDE.md` workspace structure if needed

---

## Maintenance

| Date | Change |
|------|--------|
| 2026-01-27 | Created sub-agent directory |
