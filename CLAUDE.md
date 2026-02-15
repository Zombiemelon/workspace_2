# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Before Answering Any Analytics Query (MANDATORY)

1. **Read the knowledge base first:**
   - `./quiqup-workspace/knowledge_base/quiqup_database_semantics.md` — Data gotchas, metric definitions, reconciliation rules
   - This prevents common mistakes (Google Ads vs GA4 discrepancies, tracking exclusions, etc.)

2. **Check for matching commands/agents** before doing ad-hoc work (see Agent Selection Protocol below)

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
│   ├── agents/                            ← Agent role definitions (outbound, etc.)
│   ├── knowledge_base/                    ← Data definitions, metric gotchas
│   ├── analytics_findings/                ← Completed analyses and reports
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
3. Check `./quiqup-workspace/agents/` for domain-specific agent role definitions
4. For any analytics query → read `./quiqup-workspace/knowledge_base/` first

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
| **Sequential Thinking** | Enhanced multi-step reasoning and complex analysis |
| **Context7** | Access to up-to-date documentation and framework patterns |
| **Magic (21st.dev)** | Advanced UI component generation and design system integration |
| **Playwright** | Cross-browser testing and E2E automation capabilities |
| **Filesystem** | Direct filesystem operations on the workspace directory |
| **Puppeteer** | Headless browser automation and web scraping |

> **Note:** Sequential Thinking, Context7, Magic, Filesystem, and Puppeteer are configured at user scope (`~/.claude/.mcp.json`). They enhance agent capabilities but are not required for basic analytics functionality.

## BI Output Standards

- Executive summary first
- Confidence scores: High (>90%), Medium (70-90%), Low (<70%)
- Always cite data sources
- Use "Data shows" not "I think"

## Document Format Standards (MANDATORY)

All documents must include YAML front matter:

```yaml
---
title: "Document Title"
date: YYYY-MM-DD
author: Claude | [Name]
description: "Brief summary of what this file contains and its purpose"
---
```

Optional fields: `category` (analysis/decision/playbook/data), `status` (draft/final), `tags`, `data_period`, `statistical_methods`

Naming convention: `YYYY-MM-DD_[category]_[short-description].md`

## Quick Reference

| Need | Location |
|------|----------|
| Run a command | `/health-check`, `/funnel-report`, etc. |
| Task agents | `.claude/agents/` |
| Skills (methodology) | `.claude/skills/` |
| Commands (user-invocable) | `.claude/commands/` |
| Agent role definitions | `./quiqup-workspace/agents/` |
| Data definitions & gotchas | `./quiqup-workspace/knowledge_base/` |
| Analytics findings | `./quiqup-workspace/analytics_findings/` |
| Projects & OKRs | `./quiqup-workspace/projects/` |
| New skill | Create `.claude/skills/[name]/SKILL.md` |
| New command | Create `.claude/commands/[name].md` referencing a skill |
| New agent | Create `.claude/agents/[name].md` |
