# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

This workspace uses a **router pattern** for AI agent orchestration:

```
workspace_2/
├── CLAUDE.md                    ← ROUTER (this file - selects agents)
├── workspace/agents/            ← REUSABLE AGENTS
│   ├── _index.md                ← Agent directory (check first)
│   └── data_analyst_agent.md    ← B2B analytics specialist
└── quiqup-workspace/            ← DOMAIN: Quiqup analytics
    ├── CLAUDE.md                ← Domain router
    ├── agents/                  ← Domain sub-agents (bigquery, outbound, inbound)
    ├── knowledge_base/          ← Data definitions, metric gotchas
    └── projects/                ← Active projects and OKRs
```

## Agent Selection Protocol

1. **Read `./workspace/agents/_index.md`** for available agents
2. Match query to most specific agent
3. Read and follow that agent's instructions
4. For Quiqup queries → delegate to `./quiqup-workspace/CLAUDE.md`

## Domain Routing

| Domain | Path | Triggers |
|--------|------|----------|
| **Quiqup** | `./quiqup-workspace/` | Leads, analytics, OKRs, BigQuery, Salesforce |

## External Tools (MCP)

| Tool | Purpose |
|------|---------|
| **BigQuery MCP** | Query Quiqup data warehouse |
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
| Agent list | `./workspace/agents/_index.md` |
| Quiqup domain | `./quiqup-workspace/CLAUDE.md` |
| Data definitions | `./quiqup-workspace/knowledge_base/` |
| New agent | Create `./workspace/agents/[name]_agent.md` and update index |
| New domain | Create `./[domain]-workspace/CLAUDE.md` |
