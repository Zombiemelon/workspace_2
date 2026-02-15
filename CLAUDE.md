# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This workspace uses a **router pattern** with three layers: agents (long-running specialists), skills (reusable methodology references), and commands (user-invocable actions).

```
workspace_2/
├── CLAUDE.md                              ← ROUTER (this file)
│
├── .claude/
│   ├── agents/                            ← TASK AGENTS (subagent_type configs)
│   │   ├── bigquery-analyst.md            ← BigQuery data analysis specialist
│   │   └── outbound-taskforce_agent.md    ← Outbound pipeline tracker
│   │
│   ├── skills/                            ← METHODOLOGY REFERENCES (not user-invocable)
│   │   ├── bigquery-reference/            ← Dataset schemas, join keys, query gotchas
│   │   ├── funnel-methodology/            ← Funnel stages, cohort rules, retention defs
│   │   ├── analysis-playbooks/            ← Decomposition, pacing, contribution frameworks
│   │   ├── marketing-funnel-analysis/     ← Spend-to-revenue funnel methodology + template
│   │   ├── metabase-dashboard/            ← Metabase card/dashboard creation via MCP
│   │   ├── outbound-health-check/         ← Outbound targets, queries, RAG thresholds
│   │   ├── quiqup-health-checker/         ← Ops health checks, t-distribution anomaly detection
│   │   └── quiqup-ice-scorer/             ← Calibrated ICE scoring for product prioritization
│   │
│   └── commands/                          ← USER-INVOCABLE COMMANDS (slash commands)
│       ├── health-check.md                ← /health-check — Ops health checks (account velocity)
│       ├── outbound-health-check.md       ← /outbound-health-check — Outbound pipeline review
│       ├── funnel-report.md               ← /funnel-report — Marketing funnel performance
│       └── metabase-explore.md            ← /metabase-explore — Browse Metabase structure
│
├── quiqup-workspace/                      ← DOMAIN: Quiqup analytics
│   ├── CLAUDE.md                          ← Domain router
│   ├── agents/                            ← Domain sub-agents (bigquery, outbound, inbound)
│   │   └── _index.md                      ← Sub-agent directory
│   ├── knowledge_base/                    ← Data definitions, metric gotchas
│   └── projects/                          ← Active projects and OKRs
│
└── projects/                              ← Cross-domain project files
```

## How the Layers Connect

```
User runs /health-check (command)
  → Command reads quiqup-health-checker (skill) for methodology
  → Command calls mcp__salesforce__run_soql_query (MCP tool) for data
  → Command applies statistical logic from skill and presents report

User asks about outbound pipeline (query)
  → Router delegates to outbound-taskforce agent
  → Agent reads outbound-health-check (skill) for targets/thresholds
  → Agent queries BigQuery/Salesforce for live data
```

## Agent Selection Protocol

1. Check if a **command** matches (e.g., `/health-check`, `/funnel-report`)
2. Check `.claude/agents/` for a matching **task agent**
3. Check `./quiqup-workspace/agents/_index.md` for domain sub-agents
4. For Quiqup queries → delegate to `./quiqup-workspace/CLAUDE.md`

## Commands (User-Invocable)

| Command | Skill Reference | Purpose |
|---------|----------------|---------|
| `/health-check` | `quiqup-health-checker` | Ops health checks — account registration velocity with statistical anomaly detection |
| `/outbound-health-check` | `outbound-health-check` | Outbound pipeline review — opps, meetings, size mix, data quality |
| `/funnel-report` | `marketing-funnel-analysis` | Marketing funnel from spend to revenue with dimensional slicing |
| `/metabase-explore` | `metabase-dashboard` | Browse Metabase databases, collections, dashboards, cards |

## Task Agents

| Agent | subagent_type | Purpose |
|-------|--------------|---------|
| BigQuery Analyst | `bigquery-analyst` | Quiqup data warehouse queries, analytics, insights |
| Outbound Taskforce | `outbound-taskforce` | Outbound funnel metrics, SLA compliance, pipeline health |

## Skills (Methodology References)

| Skill | Path | Used By |
|-------|------|---------|
| BigQuery Reference | `.claude/skills/bigquery-reference/` | bigquery-analyst agent, funnel-report command |
| Funnel Methodology | `.claude/skills/funnel-methodology/` | funnel-report command |
| Analysis Playbooks | `.claude/skills/analysis-playbooks/` | Any analytical task |
| Marketing Funnel | `.claude/skills/marketing-funnel-analysis/` | /funnel-report command |
| Metabase Dashboard | `.claude/skills/metabase-dashboard/` | /metabase-explore command |
| Outbound Health Check | `.claude/skills/outbound-health-check/` | /outbound-health-check command |
| Quiqup Health Checker | `.claude/skills/quiqup-health-checker/` | /health-check command |
| ICE Scorer | `.claude/skills/quiqup-ice-scorer/` | Prioritization tasks (score, rank, compare initiatives) |

## External Tools (MCP)

| Tool | Purpose |
|------|---------|
| **BigQuery MCP** | Query Quiqup data warehouse |
| **Salesforce MCP** | CRM queries (accounts, leads, opps, tasks) |
| **Metabase MCP** | Dashboard and card management |
| **Coda MCP** | OKR tracking |
| **Notion MCP** | Strategic docs |

## BI Output Standards

- Executive summary first
- Confidence scores: High (>90%), Medium (70-90%), Low (<70%)
- Always cite data sources
- Use "Data shows" not "I think"

## Quick Reference

| Need | Location |
|------|----------|
| Run a command | `/health-check`, `/funnel-report`, etc. |
| Task agents | `.claude/agents/` |
| Skills (methodology) | `.claude/skills/` |
| Commands (user-invocable) | `.claude/commands/` |
| Quiqup domain | `./quiqup-workspace/CLAUDE.md` |
| Quiqup sub-agents | `./quiqup-workspace/agents/_index.md` |
| Data definitions | `./quiqup-workspace/knowledge_base/` |
| New skill | Create `.claude/skills/[name]/SKILL.md` |
| New command | Create `.claude/commands/[name].md` referencing a skill |
| New agent | Create `.claude/agents/[name].md` |
