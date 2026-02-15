---
name: metabase-dashboard
description: "Build and manage Metabase dashboards via MCP — card creation, display types, visualization settings, dashboard layout, parameters, and wiring. Use when creating or updating Metabase cards and dashboards."
user-invocable: false
---

# Metabase Dashboard Builder Reference

Patterns and recipes for building Metabase dashboards via the MCP API. Covers card creation, display types, visualization tuning, dashboard layout, and parameter wiring.

## Quick Reference — MCP Tools

| Tool | Purpose |
|------|---------|
| `mcp__metabase__create_card` | Create a new question/card |
| `mcp__metabase__update_card` | Change display, viz settings, SQL |
| `mcp__metabase__get_card` | Read card config |
| `mcp__metabase__execute_card` | Run card and get results |
| `mcp__metabase__delete_card` | Archive/delete a card |
| `mcp__metabase__create_dashboard` | Create new dashboard |
| `mcp__metabase__update_dashboard` | Update dashboard params, layout |
| `mcp__metabase__get_dashboard` | Read full dashboard config |
| `mcp__metabase__get_dashboard_cards` | List cards on a dashboard |
| `mcp__metabase__add_card_to_dashboard` | Place a card on a dashboard |
| `mcp__metabase__update_dashboard_cards` | Bulk-update card positions/sizes |
| `mcp__metabase__remove_card_from_dashboard` | Remove a card from dashboard |

**Important:** Always use `ToolSearch` to load these tools before invoking them.

## Environment

- **Metabase URL:** `https://metabase.dev.quiq.ly`
- **Database ID:** 2 (Reporting — BigQuery `quiqup` project)
- **Dashboard link pattern:** `https://metabase.dev.quiq.ly/dashboard/{id}`
- **Card link pattern:** `https://metabase.dev.quiq.ly/question/{id}`

## Creating Cards

### Native SQL Card (basic)

```json
{
  "name": "Card Name",
  "display": "scalar",
  "database_id": 2,
  "collection_id": null,
  "dataset_query": {
    "type": "native",
    "native": {
      "query": "SELECT COUNT(*) AS metric_name FROM ...",
      "template-tags": {}
    },
    "database": 2
  },
  "visualization_settings": {}
}
```

### With Template Tag (Metabase Variable)

Add a `template-tags` block and use `{{variable_name}}` in SQL:

```json
"template-tags": {
  "days_lookback": {
    "id": "unique-uuid-here",
    "name": "days_lookback",
    "display-name": "Days Lookback",
    "type": "number",
    "default": "7"
  }
}
```

In SQL: `WHERE date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {{days_lookback}} DAY)`

**Note:** After creation, the tag type in Metabase UI should say "Number" with default "7".

## Display Types

| Display | Best For | Key Settings |
|---------|----------|-------------|
| `scalar` | Single KPI number | `column_title`, `number_style`, `suffix` |
| `progress` | Goal tracking (X / target) | `progress.goal`, `progress.color` |
| `table` | Multi-column data | `table.columns`, `column_settings` |
| `row` | Horizontal bar chart | `graph.dimensions`, `graph.metrics`, `stackable.stack_type` |
| `bar` | Vertical bar chart | Same as `row` |
| `line` | Time series | `graph.dimensions` (date), `graph.metrics` |
| `pie` | Share/distribution | `pie.dimension`, `pie.metric` |
| `gauge` | Range indicator | `gauge.segments` |
| `map` | Geographic data | `map.type`, `map.latitude_column` |

### Scalar Card

```json
{
  "display": "scalar",
  "visualization_settings": {
    "column_settings": {
      "[\"name\",\"column_alias\"]": {
        "column_title": "Display Name",
        "number_style": "decimal",
        "suffix": "%"
      }
    }
  }
}
```

**Column settings key format:** `[\"name\",\"<sql_alias>\"]` — must match the SQL column alias exactly.

### Progress Bar Card

```json
{
  "display": "progress",
  "visualization_settings": {
    "progress.goal": 20,
    "progress.color": "#84BB4C"
  }
}
```

- SQL must return a **single numeric value** (e.g., `SELECT COUNT(*) AS opps_this_month`)
- Color: `#84BB4C` (green), `#F9D45C` (amber), `#EF8C8C` (red)

### Stacked Bar Chart (Row)

```json
{
  "display": "row",
  "visualization_settings": {
    "graph.dimensions": ["bdm_name"],
    "graph.metrics": ["meetings", "opps_created"],
    "stackable.stack_type": "stacked"
  }
}
```

- `graph.dimensions`: the categorical axis (usually names/labels)
- `graph.metrics`: the numeric values to plot (multiple = stacked/grouped)
- `stackable.stack_type`: `"stacked"` or `"normalized"` or `null` (grouped)

### Table with Column Customization

```json
{
  "display": "table",
  "visualization_settings": {
    "table.columns": [
      {"name": "col1", "enabled": true},
      {"name": "col2", "enabled": true},
      {"name": "hidden_col", "enabled": false}
    ],
    "column_settings": {
      "[\"name\",\"col1\"]": { "column_title": "Display Name" },
      "[\"name\",\"col2\"]": { "column_title": "Percentage", "suffix": "%" }
    }
  }
}
```

## Dashboard Layout

### Grid System

- Dashboard is **24 columns wide** (Metabase v0.44+)
- Cards are positioned by `(col, row, size_x, size_y)`
- `col`: 0-23 (left to right)
- `row`: 0+ (top to bottom, auto-extends)
- Common widths: 6 (quarter), 8 (third), 12 (half), 24 (full)

### Adding a Card to Dashboard

```json
// mcp__metabase__add_card_to_dashboard
{
  "dashboard_id": 518,
  "card_id": 3988,
  "row": 0,
  "col": 0,
  "size_x": 4,
  "size_y": 3
}
```

Returns a `dashcard_id` — needed for parameter wiring and removal.

### Typical Layout Patterns

**KPI Row (4 cards):**
```
| Scalar (5w) | Scalar (5w) | Progress (9w) | Scalar (5w) |
```
Row 0, cols 0/5/10/19, height 3

**Full-width chart below:**
```
| Chart (24w, 5h) |
```
Row 3, col 0

### Removing a Card

Use `mcp__metabase__remove_card_from_dashboard` with the `dashcard_id` (NOT the card_id).

### Repositioning Cards

Use `mcp__metabase__update_dashboard_cards` with a `cards` array containing `id` (dashcard_id), `row`, `col`, `size_x`, `size_y` for each card.

## Dashboard Parameters (Filters)

### Adding a Parameter

Update the dashboard's `parameters` array:

```json
// mcp__metabase__update_dashboard
{
  "dashboard_id": 518,
  "parameters": [
    {
      "id": "days_lookback",
      "name": "Days Lookback",
      "slug": "days_lookback",
      "type": "number/=",
      "default": 7
    }
  ]
}
```

### Wiring Parameters to Cards

Each dashcard needs `parameter_mappings` to connect the dashboard filter to its template tag:

```json
// mcp__metabase__update_dashboard_cards
{
  "dashboard_id": 518,
  "cards": [
    {
      "id": 3095,  // dashcard_id
      "parameter_mappings": [
        {
          "parameter_id": "days_lookback",
          "card_id": 3988,
          "target": ["variable", ["template-tag", "days_lookback"]]
        }
      ]
    }
  ]
}
```

**Key:** `parameter_id` matches the dashboard parameter's `id`, and `target` points to the card's `template-tag` name.

**Cards without the variable** (e.g., month-based cards) should NOT have parameter_mappings for that parameter.

## Workflow Checklist

1. **Create card** with `create_card` (get `card_id`)
2. **Test card** with `execute_card` to verify data
3. **Add to dashboard** with `add_card_to_dashboard` (get `dashcard_id`)
4. **Wire parameters** with `update_dashboard_cards` if card uses template tags
5. **Tune visuals** with `update_card` to adjust display type and viz settings
6. **Adjust layout** with `update_dashboard_cards` for position/size

## STRICT RULES

- **NEVER delete or archive cards, dashboards, or remove cards from dashboards without the user's explicit permission.** This includes `delete_card`, `remove_card_from_dashboard`, and setting `archived: true`. Always ask first.

## Gotchas

| Issue | Solution |
|-------|----------|
| Column settings key must exactly match SQL alias | Use `[\"name\",\"my_alias\"]` format |
| `execute_card` needs card ID, not dashcard ID | Card ID from `create_card` response |
| Progress bar needs single-value query | `SELECT COUNT(*) AS x` not multi-column |
| Template tag `default` must be a string | `"default": "7"` not `"default": 7` |
| `remove_card_from_dashboard` uses dashcard_id | Get from `get_dashboard_cards` or `add_card_to_dashboard` response |
| Updating dashboard params overwrites existing | Always include ALL existing params in the array |
| Parameter wiring preserves other dashcard fields | Include `row`, `col`, `size_x`, `size_y` when updating cards |

## Outbound Taskforce Dashboard (518)

Reference implementation. See `projects/outbound_taskforce/metric_status.md` for current card inventory.

| Card | ID | Dashcard | Display | Position |
|------|----|----------|---------|----------|
| Outbound Meetings | 3988 | 3095 | scalar | (0,0) 5x3 |
| Outbound Opps Created | 3989 | 3096 | scalar | (5,0) 5x3 |
| Opps This Month (progress) | 3992 | 3099 | progress | (10,0) 9x3 |
| Pace to Target % | 3993 | 3100 | scalar | (19,0) 5x3 |
| BDM Leaderboard | 3991 | 3098 | row (stacked) | (0,3) 24x5 |

Dashboard parameter: `days_lookback` (number, default 7) wired to cards 3988, 3989, 3991.
