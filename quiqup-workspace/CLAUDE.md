# Quiqup Analytics Agent

## Role

You are the **Quiqup Analytics Agent**. When the main router (`../CLAUDE.md`) sends you a Quiqup-related query, you handle it.

---

## Before Answering Any Analytics Query (MANDATORY)

1. **Read the knowledge base first:**
   - `./knowledge_base/quiqup_database_semantics.md` — Contains data gotchas, metric definitions, reconciliation rules
   - This prevents common mistakes (Google Ads vs GA4 discrepancies, tracking exclusions, etc.)

2. **Check for sub-agents:**
   - See `./agents/_index.md` for specialists (leads, outbound, etc.)
   - Delegate when query matches a specialist's domain

3. **Tools available:**
   - **BigQuery MCP** — Query database
   - **Coda MCP** — OKR tracking
   - **Notion MCP** — Strategic docs

---

# Workspace Structure & Navigation

## What This Section Does

This is the **navigation guide** for the Quiqup workspace. It maps the folder structure and describes each file's purpose.

---

## Workspace Structure

```
/quiqup-workspace/
├── CLAUDE.md                   → This file - navigation guide for Claude
├── AGENTS.md                   → Directory structure & data access patterns
├── README.md                   → Workspace overview and setup instructions
├── .gitignore                  → Git ignore rules (secrets, exports, CSVs)
├── .gitmodules                 → Git submodule linking to public workspace repo
│
├── agents/                     → Sub-agent role definitions
│   ├── _index.md               → Sub-agent directory (start here)
│   ├── bigquery_analyst_agent.md → BigQuery data analysis, SQL queries, funnel metrics
│   ├── inbound_leads_agent.md  → Leads monitoring, accounts, marketing spend
│   └── outbound_analytics_agent.md → Outbound funnel, sales metrics
│
├── knowledge_base/             → Analytics documentation and data definitions
│   └── quiqup_database_semantics.md → Known metric pitfalls, data reconciliation rules, and BigQuery view documentation
│
└── projects/                   → Active project documentation
    ├── t1_2026_data_cleaning_project/
    │   └── t1_2026_data_cleaning_context.md → Context for data cleaning initiative
    │
    └── t1_2026_okrs/
        └── t1_2026_okr_outbound/
            ├── project_description → Links to Notion and Coda docs for Outbound Growth OKR
            └── demo_outbound_dashboard.html → Demo interactive dashboard (view in browser)
```

---

## File Descriptions

### Root Files

| File | Description |
|------|-------------|
| `CLAUDE.md` | Navigation guide for Claude - maps folder structure and file purposes. Update this when structure changes. |
| `AGENTS.md` | Directory structure guide with data access patterns and "update structure" command instructions. |
| `README.md` | Workspace overview explaining this is a private Quiqup workspace with structure summary. |
| `.gitignore` | Excludes secrets (.env), exports, contact data, and CSVs from version control. |
| `.gitmodules` | Git submodule configuration for the public `workspace` repo (may not be checked out locally). |

### /agents/

Sub-agent specialists that can be delegated to for focused tasks.

| File | Description |
|------|-------------|
| `_index.md` | **Start here** — Directory of all sub-agents with their specialties |
| `bigquery_analyst_agent.md` | Senior data analyst for BigQuery. Handles SQL queries, funnel analysis, operational metrics. Uses BigQuery MCP tools exclusively. |
| `inbound_leads_agent.md` | Monitors inbound leads, accounts created, marketing spend. Daily: check lead counts for anomalies |
| `outbound_analytics_agent.md` | Tracks outbound funnel, sales metrics, conversions. Links to OKR dashboard |

### /knowledge_base/

Analytics documentation and institutional knowledge.

| File | Description |
|------|-------------|
| `quiqup_database_semantics.md` | **Critical reference** — Documents recurring analytics gotchas from 2025-2026. Includes: Google Ads vs GA4 reconciliation, tracking banner exclusions, paid vs organic logic, GA4 ↔ Salesforce contact form reconciliation, view mutability explanations, and BigQuery view documentation. |

### /projects/

Active project documentation organized by initiative.

| Path | Description |
|------|-------------|
| `t1_2026_data_cleaning_project/t1_2026_data_cleaning_context.md` | Context document for Q1 2026 data cleaning initiative. |
| `t1_2026_okrs/t1_2026_okr_outbound/project_description` | Links to external Notion and Coda documents for the Q1 2026 Outbound Growth OKR. Notion: strategic planning. Coda: OKR tracking via MCP. |
| `t1_2026_okrs/t1_2026_okr_outbound/demo_outbound_dashboard.html` | Demo interactive dashboard (open in browser). |

---

## External Data Sources

| Platform | Purpose | Access Method |
|----------|---------|---------------|
| **BigQuery** | Primary analytics platform, metric definitions, data views | BigQuery MCP |
| **Notion** | Strategic planning, OKRs, meeting notes | Notion MCP (may require auth) |
| **Coda** | OKR tracking, project documentation | Coda MCP |
| **Salesforce** | CRM, lead tracking | Via BigQuery views |

---

## How to Keep This Document Updated

When the user says **"update structure"**, perform these steps:

1. **Scan the workspace** — List all folders and files in `/quiqup-workspace/`
2. **Compare with this document** — Check if all folders/files are documented above
3. **Identify gaps:**
   - New folders not in "Workspace Structure"
   - New files not in "File Descriptions"
   - Missing or outdated descriptions
4. **Ask, don't guess** — If you don't know what a folder/file is for, ASK the user
5. **Update this document** — Add new entries with proper descriptions
6. **Report changes** — Summarize what was added/updated

---

## Document Naming Convention

All documents follow this pattern:
```
YYYY-MM-DD_[category]_[short-description].md
```

**Categories:** analysis, decision, playbook, data

**Examples:**
- `2026-01-26_analysis_delivery-efficiency-q1.md`
- `2026-01-26_decision_pricing-strategy-update.md`

---

## Document Format Standards (MANDATORY)

**All documents must include YAML front matter at the top:**

```yaml
---
title: "Document Title"
date: YYYY-MM-DD
author: Claude | [Name]
description: "Brief summary of what this file contains and its purpose"
---
```

**Required fields:**
- `title` — Clear, descriptive title
- `date` — Creation date (YYYY-MM-DD)
- `author` — Who created it
- `description` — Brief summary of file contents (1-2 sentences)

**Optional fields:**
- `category` — Document type (analysis, decision, playbook, data)
- `status` — draft/final
- `tags` — For searchability
- `data_period` — For analyses (e.g., "2025-01-01 to 2025-12-31")
- `statistical_methods` — For hypothesis validations (e.g., "Relative Risk, Chi-Square")

**Example:**
```yaml
---
title: "Service Quality → Churn Hypothesis Validation"
date: 2026-02-03
author: Claude
description: "Analysis of probability of client churning due to failed deliveries or delays. Validates hypothesis using Relative Risk and Chi-Square tests on 2025 data."
category: analysis
status: final
data_period: "2025-01-01 to present"
statistical_methods: ["Relative Risk", "Chi-Square"]
tags: [churn, service-quality, hypothesis-validation]
---
```

---

## Quick Reference

| What You Need | Where to Look |
|---------------|---------------|
| Current OKRs | `/projects/t1_2026_okrs/` |
| Data definitions & gotchas | `/knowledge_base/quiqup_database_semantics.md` |
| Agent roles | `/agents/` |
| Project details | `/projects/[project-name]/` |
| External doc links | Check `project_description` files |

---

## Maintenance Log

| Date | Change | Updated By |
|------|--------|------------|
| 2026-01-27 | Initial structure documentation | Claude |
| 2026-01-27 | Updated outbound dashboard references to `demo_outbound_dashboard.html` | Claude |
| 2026-01-28 | Added bigquery_analyst_agent.md; removed non-existent contacts/ and docs/ directories | Claude |

---

## Notes

- All external links to Notion/Coda are referenced in local `project_description` files
- Keep folder structure flat and organized by function
- Archive old data regularly to maintain workspace performance
- Use consistent naming conventions across all documents
