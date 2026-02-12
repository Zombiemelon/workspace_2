---
name: metabase-explore
description: "Explore Metabase structure — list databases, collections, dashboards, and cards. Use when you need to understand what already exists before building new reports."
---

# Metabase Explorer

Catalog the structure of the Quiqup Metabase instance at `https://metabase.dev.quiq.ly`.

## What To Do

When invoked, systematically explore Metabase and produce a structured summary of what exists.

### Step 1: List Databases
Use `mcp__metabase__list_databases` to get all connected data sources.

### Step 2: List Collections (non-personal)
Use `mcp__metabase__list_collections` and filter to **non-personal collections only** (skip "X's Personal Collection" entries). Organize hierarchically by parent/child relationships using the `location` field.

### Step 3: List Dashboards
Use `mcp__metabase__list_dashboards` to get all dashboards. For each, note:
- Dashboard ID, name, collection
- Number of cards
- Last edited date

### Step 4: List Cards in Key Collections
For the most relevant collections (Sales, Growth, KPIs, Operations, Product), use `mcp__metabase__list_cards` to catalog existing questions/cards.

### Step 5: Produce Summary
Output a structured report with:

```
## Metabase Structure Summary

### Databases
| ID | Name | Engine |
|----|------|--------|

### Collections (non-personal)
| ID | Name | Parent | # Dashboards | # Cards |
|----|------|--------|-------------|---------|

### Key Dashboards
| ID | Name | Collection | Cards | Link |
|----|------|-----------|-------|------|
(Link format: https://metabase.dev.quiq.ly/dashboard/{id})

### Key Cards/Questions
| ID | Name | Type | Database | Collection |
|----|------|------|----------|-----------|
```

## Arguments

- `--collection <name>` — Focus on a specific collection instead of exploring everything
- `--dashboard <id>` — Deep-dive into a specific dashboard's cards and structure
- `--cards-only` — Skip databases/collections, just list cards

## Tips

- The output can be large. Use `--collection Sales` to scope down.
- Dashboard links follow the pattern: `https://metabase.dev.quiq.ly/dashboard/{id}`
- Card links follow the pattern: `https://metabase.dev.quiq.ly/question/{id}`
