---
name: health-check
description: "Run Quiqup operational health checks — account registration velocity with statistical anomaly detection. Compares live Salesforce data against historical baselines and flags significant drops."
---

# Quiqup Ops Health Check

Run operational health checks on Quiqup systems. Compares live metrics against historical baselines using prediction intervals (t-distribution) and flags anomalies with traffic-light status.

## Before You Start

1. Read the skill reference: `.claude/skills/quiqup-health-checker/SKILL.md`

## What To Do

### Step 1: Compute Datetime Ranges

Run this Bash command to get all required datetime ranges (macOS `date` syntax):

```bash
echo "=== CURRENT WINDOW ==="
echo "NOW_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "THREE_H_AGO=$(date -u -v-3H +%Y-%m-%dT%H:%M:%SZ)"

echo "=== HISTORICAL WINDOWS (same weekday, weeks 1-4) ==="
for N in 1 2 3 4; do
  DAYS=$((N * 7))
  echo "W${N}_START=$(date -u -v-${DAYS}d -v-3H +%Y-%m-%dT%H:%M:%SZ)"
  echo "W${N}_END=$(date -u -v-${DAYS}d +%Y-%m-%dT%H:%M:%SZ)"
  echo "W${N}_DATE=$(date -u -v-${DAYS}d +%Y-%m-%d)"
done
```

Parse the output to extract all datetime values.

### Step 2: Query Current Window

Use `mcp__salesforce__run_soql_query` to count accounts created in the last 3 hours:

```sql
SELECT COUNT() FROM Account WHERE CreatedDate >= {THREE_H_AGO}
```

Store the result as `current_count`.

### Step 3: Query Historical Windows

Use `mcp__salesforce__run_soql_query` with a combined query for all 4 historical windows:

```sql
SELECT Id, CreatedDate FROM Account
WHERE (CreatedDate >= {W1_START} AND CreatedDate < {W1_END})
   OR (CreatedDate >= {W2_START} AND CreatedDate < {W2_END})
   OR (CreatedDate >= {W3_START} AND CreatedDate < {W3_END})
   OR (CreatedDate >= {W4_START} AND CreatedDate < {W4_END})
```

From the results, count records per week by checking which date range each `CreatedDate` falls into:
- w1_count, w2_count, w3_count, w4_count

### Step 4: Compute Statistics

Calculate using the formulae from the skill reference:

```
x̄ = (w1 + w2 + w3 + w4) / 4
s = sqrt(((w1-x̄)² + (w2-x̄)² + (w3-x̄)² + (w4-x̄)²) / 3)
CV = s / x̄

pi80_lower = x̄ - 1.638 * s * sqrt(1.25)
pi95_lower = x̄ - 3.182 * s * sqrt(1.25)

change_pct = (current - x̄) / x̄ * 100
```

### Step 5: Apply Traffic-Light Logic

Follow the decision tree from the skill reference:

1. If x̄ < 3 → `LOW_SAMPLE` (suppress alerting, report as informational)
2. If |current - x̄| < 2 → `GREEN` (absolute floor)
3. If CV > 0.5 → append `HIGH_VARIANCE` warning
4. If current >= pi80_lower → `GREEN`
5. If current >= pi95_lower → `AMBER`
6. Else → `RED`
7. If all historical = 0 → `NO_BASELINE`

### Step 6: Present Report

Present the report inline using the template from the skill reference. Include:

- Traffic-light status (GREEN/AMBER/RED) prominently
- Current count vs baseline mean
- Statistical detail (std dev, PI bounds, change %)
- Historical breakdown table (each week's count and date)
- Any warnings (HIGH_VARIANCE, LOW_SAMPLE, etc.)
- Interpretation: what the status means operationally

**If RED or AMBER**: Add a "Recommended Actions" section suggesting:
- Check Salesforce integration/API health
- Check website/signup flow
- Compare with other metrics (orders, leads) to determine if isolated
- Escalate if corroborated by other drops

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--check <name>` | Run a specific check only | All checks |
| `--verbose` | Include full statistical workings | Summary only |
| `--window <hours>` | Override the 3-hour window | 3 |
