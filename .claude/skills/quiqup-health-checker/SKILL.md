---
name: quiqup-health-checker
description: "Quiqup operational health checks — account registration velocity, statistical anomaly detection with t-distribution prediction intervals, and traffic-light alerting."
user-invocable: false
---

# Quiqup Ops Health Checker — Reference

Methodology and templates for operational health checks on Quiqup systems. Consumed by the `/health-check` command.

## Check Catalog

| # | Check | Data Source | Baseline | Status |
|---|-------|------------|----------|--------|
| 1 | Account Registration Velocity | Salesforce (SOQL) | 4-week same-weekday average | Active |

---

## Statistical Method: Prediction Interval (t-distribution)

All checks use the same anomaly detection framework. Given a small historical sample (n observations of the same metric at the same time window), we detect whether the current value is anomalously low.

### Formulae

Given n historical observations x1 ... xn:

```
Sample mean:        x̄ = Σxi / n
Sample std dev:     s = sqrt(Σ(xi - x̄)² / (n-1))
Coeff of variation: CV = s / x̄

Prediction interval lower bound:
  lower = x̄ - t(α, df=n-1) * s * sqrt(1 + 1/n)
```

### t Critical Values (one-sided lower)

| Confidence | df=3 (n=4) | df=7 (n=8) |
|-----------|-----------|-----------|
| 80% | 1.638 | 1.415 |
| 90% | 2.353 | 1.895 |
| 95% | 3.182 | 2.365 |

### Traffic-Light Assignment

```
IF x̄ < 3                         → LOW_SAMPLE (suppress alerting)
IF |current - x̄| < 2             → GREEN (absolute floor — noise protection)
IF CV > 0.5                       → append HIGH_VARIANCE warning

IF current >= 80% PI lower bound  → GREEN
IF current >= 95% PI lower bound  → AMBER
ELSE                              → RED

IF all historical values = 0      → NO_BASELINE (cannot compute)
```

### Worked Example

Historical same-weekday 3h counts: 12, 8, 15, 10
- x̄ = 11.25, s = 2.99, CV = 0.27
- 80% PI lower: 11.25 - 1.638 * 2.99 * 1.118 = 11.25 - 5.47 = 5.78
- 95% PI lower: 11.25 - 3.182 * 2.99 * 1.118 = 11.25 - 10.63 = 0.62

Current = 6 → above 5.78 → **GREEN**
Current = 4 → below 5.78, above 0.62 → **AMBER**
Current = 0 → below 0.62 → **RED**

---

## Check 1: Account Registration Velocity

### What It Measures

Number of Salesforce Accounts created in the **last 3 hours**, compared to the same 3-hour window on the **same day of the week** over the **previous 4 weeks**.

### Why It Matters

Account creation is a leading indicator of business activity. A sudden drop may signal:
- API/integration failures (website → Salesforce sync broken)
- Marketing channel outage
- Payment gateway issues blocking sign-ups
- Seasonal pattern (expected — check before escalating)

### SOQL Queries

**Query 1 — Current window (last 3 hours):**

```sql
SELECT COUNT() FROM Account WHERE CreatedDate >= {3h_ago_utc}
```

**Query 2 — Historical windows (single combined query):**

```sql
SELECT Id, CreatedDate FROM Account
WHERE (CreatedDate >= {w1_start} AND CreatedDate < {w1_end})
   OR (CreatedDate >= {w2_start} AND CreatedDate < {w2_end})
   OR (CreatedDate >= {w3_start} AND CreatedDate < {w3_end})
   OR (CreatedDate >= {w4_start} AND CreatedDate < {w4_end})
```

Where:
- `{3h_ago_utc}` = current UTC time minus 3 hours
- `{wN_start}` = same `3h_ago_utc` but N weeks earlier
- `{wN_end}` = same `now_utc` but N weeks earlier

**Datetime format:** `YYYY-MM-DDThh:mm:ssZ` (ISO 8601, SOQL-compatible)

### Datetime Computation (Bash)

```bash
# Get current UTC time components
NOW_UTC=$(date -u +%Y-%m-%dT%H:%M:%SZ)
THREE_H_AGO=$(date -u -v-3H +%Y-%m-%dT%H:%M:%SZ)  # macOS

# Historical same-weekday windows (N weeks back)
for N in 1 2 3 4; do
  DAYS=$((N * 7))
  W_START=$(date -u -v-${DAYS}d -v-3H +%Y-%m-%dT%H:%M:%SZ)  # macOS
  W_END=$(date -u -v-${DAYS}d +%Y-%m-%dT%H:%M:%SZ)           # macOS
done
```

### Counting Historical Results

The combined historical query returns individual records. Count per week by bucketing `CreatedDate` into the week it belongs to:
- Records where CreatedDate falls between w1_start and w1_end → w1_count
- Records where CreatedDate falls between w2_start and w2_end → w2_count
- etc.

### Edge Cases

| Case | Detection | Action |
|------|-----------|--------|
| Weekend/holiday | Weekday check | Low weekend volume is expected — still flag if below PI |
| Salesforce sync delay | Recent records may lag 5-15min | Note in report if <5min since window end |
| Time zone | All computation in UTC | Consistent regardless of user location |
| Very new account (< 4 weeks of data) | One or more historical weeks return 0 | Include zeros in calculation; note if n_nonzero < 3 |

---

## Report Template

```markdown
## Quiqup Ops Health Check — {date} {time} UTC

### 1. Account Registration Velocity [{STATUS}]

| Metric | Value |
|--------|-------|
| Accounts created (last 3h) | {current} |
| Baseline mean (4-wk avg) | {x_bar} |
| Baseline std dev | {s} |
| Change from mean | {change_pct}% |
| 80% PI lower bound | {pi80_lower} |
| 95% PI lower bound | {pi95_lower} |

**Historical breakdown:**
| Week | Date | Window | Count |
|------|------|--------|-------|
| W-1 | {w1_date} | {w1_start}–{w1_end} | {w1_count} |
| W-2 | {w2_date} | {w2_start}–{w2_end} | {w2_count} |
| W-3 | {w3_date} | {w3_start}–{w3_end} | {w3_count} |
| W-4 | {w4_date} | {w4_start}–{w4_end} | {w4_count} |

{warnings if any: HIGH_VARIANCE, LOW_SAMPLE, NO_BASELINE}

---

*Generated: {timestamp} | Data source: Salesforce SOQL | Method: t-distribution prediction interval (df=3)*
```

---

## Future Checks (Planned)

| # | Check | Data Source | Notes |
|---|-------|------------|-------|
| 2 | Order Volume Velocity | BigQuery | Same statistical method, different data source |
| 3 | Delivery Completion Rate | BigQuery | Ratio-based — may need proportion test |
| 4 | Support Ticket Spike | Salesforce Cases | Upward anomaly detection (invert PI logic) |
| 5 | Payment Failure Rate | BigQuery | Ratio-based |
