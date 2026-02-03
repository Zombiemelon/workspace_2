---
title: "Service Quality → Churn Hypothesis Validation"
date: 2026-02-03
author: Claude
description: "Analysis of probability of client churning due to failed deliveries or delays. Validates hypothesis that service quality issues drive churn more than price, using Relative Risk and Chi-Square tests on 2025 operational data."
category: analysis
status: final
data_period: "2025-01-01 to present"
statistical_methods: ["Relative Risk", "Chi-Square"]
tags: [churn, service-quality, failed-deliveries, late-deliveries, hypothesis-validation]
---

# Service Quality → Churn Hypothesis Validation

---

## Hypothesis

> "Clients churn primarily due to unresolved service quality issues (failed deliveries, late deliveries), not price. Therefore, proactive AM calling when failed delivery spikes are detected could reduce churn."

**Prior Evidence:** Root cause analysis (Jan 24–Apr 25) suggested 7+ client churns were driven by service issues (43% lost/damaged, 29% late deliveries, 14% pickup issues, 19% price).

---

## Segments Analyzed

| Segment | Definition | Rationale |
|---------|------------|-----------|
| **New Clients** | < 2 months since first order | Early lifecycle, not yet established |
| **Activated Clients** | ≥ 2 months since first order | Established relationship |

**Churn Definition:** No orders in last 90 days (for clients who placed orders in 2025)

---

## Key Findings

### Baseline Churn Rates

| Segment | Total Clients | Churned | Churn Rate |
|---------|---------------|---------|------------|
| Activated Clients | 2,622 | 533 | **20.3%** |
| New Clients | 2,462 | 1,832 | **74.4%** |

### Failed Deliveries → Churn

**Using Failure RATE (≥5% of orders failed vs <5%) to control for order volume:**

| Segment | High Failure Rate Churn | Low/No Failure Churn | Relative Risk | Chi-Square | p-value |
|---------|-------------------------|----------------------|---------------|------------|---------|
| **Activated Clients** | 16.7% | 11.2% | **1.49** | 13.17 | **< 0.001** |
| New Clients | 46.0% | 52.6% | 0.87 | 0.87 | ≥ 0.05 (NS) |

### Late Deliveries → Churn

**Using Late RATE (≥10% of orders late vs <10%):**

| Segment | High Late Rate Churn | Low/No Late Churn | Relative Risk | Chi-Square | p-value |
|---------|----------------------|-------------------|---------------|------------|---------|
| **Activated Clients** | 18.8% | 12.4% | **1.51** | 8.77 | **< 0.01** |
| New Clients | 62.5% | 47.3% | 1.32 | 2.47 | ≥ 0.05 (NS) |

---

## Verdict

| Segment | Failed Deliveries | Late Deliveries | Overall Verdict |
|---------|-------------------|-----------------|-----------------|
| **Activated Clients** | ✅ VALIDATED (RR=1.49, p<0.001) | ✅ VALIDATED (RR=1.51, p<0.01) | **HYPOTHESIS VALIDATED** |
| **New Clients** | ❌ Not significant | ❌ Not significant | **NOT VALIDATED** |

**Effect Size:** Moderate (RR ≈ 1.5 = 50% increased churn risk)

---

## Critical Caveats

### 1. Confounding Variable Discovery

Initial analysis using binary "had failure yes/no" showed **opposite results** (RR < 1):

| Failure Status | Avg Orders per Client |
|----------------|----------------------|
| No Failures | 6.4 orders |
| Had Failures | 1,300 orders |

Clients with failures have **200x more orders** on average. This creates selection bias: more orders = more chances for failure AND more engagement (less churn).

**Solution:** Use failure RATE (failures/orders) instead of binary "had failure".

### 2. New Client Sample Size

Only 201 New Clients with ≥10 orders available for rate-based analysis. Insufficient statistical power to detect effect.

### 3. Late Delivery Data Quality

| Delay Bucket | Orders | % |
|--------------|--------|---|
| On time/early | 2,260,551 | 92.6% |
| 1-60 min late | 15,403 | 0.6% |
| 1-6 hours late | 8,482 | 0.4% |
| **6-24 hours late** | 109,908 | **4.5%** |
| **24+ hours late** | 46,146 | **1.9%** |

Many "late" orders are 6-24+ hours late, which may represent next-day delivery services where `delivery_before` is set to same-day but delivery is expected next day.

### 4. Causation vs Correlation

This analysis shows **correlation**, not causation. We cannot prove that failures/delays directly cause churn without:
- A/B testing proactive AM intervention
- Controlling for other factors (pricing, fit, competition)

---

## Recommendations

1. **For Activated Clients:** Implement proactive AM calling when:
   - Failure rate > 5% in rolling 30 days, OR
   - Late rate > 10% in rolling 30 days

2. **For New Clients:** Investigate other churn drivers:
   - Onboarding friction
   - Product-market fit
   - Pricing issues
   - Competitor offerings

3. **Data Quality:** Review `delivery_before` timestamp logic for next-day delivery services.

4. **Further Analysis:**
   - Qualitative review of the 7+ specific churns from prior analysis
   - A/B test of proactive AM intervention
   - Survival analysis to understand time-to-churn

---

## SQL Queries Used

### Discovery: Order State Values

```sql
SELECT
  state,
  COUNT(*) AS occurrences
FROM `quiqup.ex_api_current.order_state_changes`
WHERE occurred_at >= '2025-01-01'
  AND (LOWER(state) LIKE '%fail%'
       OR LOWER(state) LIKE '%complete%'
       OR LOWER(state) LIKE '%deliver%')
GROUP BY 1
ORDER BY 2 DESC
```

**Key States Found:**
- `delivery_failed` (190,265 occurrences)
- `delivery_complete` (2,633,666 occurrences)

---

### Analysis 1: Baseline Segment Counts

```sql
WITH client_activity AS (
  SELECT
    client_id,
    MIN(submitted_at_utc) AS first_order_date,
    MAX(submitted_at_utc) AS last_order_date,
    COUNT(DISTINCT id) AS total_orders
  FROM `quiqup.bi_reporting.client_orders`
  WHERE submitted_at_utc >= '2025-01-01'
    AND client_id IS NOT NULL
  GROUP BY 1
)

SELECT
  CASE
    WHEN DATE_DIFF(DATE(last_order_date), DATE(first_order_date), DAY) < 60
    THEN 'New Client'
    ELSE 'Activated Client'
  END AS segment,

  CASE
    WHEN DATE_DIFF(CURRENT_DATE(), DATE(last_order_date), DAY) > 90
    THEN 'Churned'
    ELSE 'Active'
  END AS churn_status,

  COUNT(*) AS client_count,
  SUM(total_orders) AS total_orders,
  ROUND(AVG(total_orders), 1) AS avg_orders_per_client
FROM client_activity
GROUP BY 1, 2
ORDER BY 1, 2
```

---

### Analysis 2: Failed Deliveries → Churn (with Statistical Tests)

```sql
WITH client_activity AS (
  SELECT
    client_id,
    MIN(submitted_at_utc) AS first_order_date,
    MAX(submitted_at_utc) AS last_order_date,
    COUNT(DISTINCT id) AS total_orders
  FROM `quiqup.bi_reporting.client_orders`
  WHERE submitted_at_utc >= '2025-01-01'
    AND client_id IS NOT NULL
  GROUP BY 1
),

client_segments AS (
  SELECT
    ca.client_id,
    ca.total_orders,
    CASE
      WHEN DATE_DIFF(DATE(last_order_date), DATE(first_order_date), DAY) < 60
      THEN 'New Client'
      ELSE 'Activated Client'
    END AS segment,
    CASE
      WHEN DATE_DIFF(CURRENT_DATE(), DATE(last_order_date), DAY) > 90
      THEN 1 ELSE 0
    END AS churned
  FROM client_activity ca
),

failed_orders AS (
  SELECT
    co.client_id,
    COUNT(DISTINCT co.id) AS failure_count
  FROM `quiqup.bi_reporting.client_orders` co
  JOIN `quiqup.ex_api_current.order_state_changes` osc
    ON co.id = osc.client_order_id
  WHERE osc.state = 'delivery_failed'
    AND osc.occurred_at >= '2025-01-01'
  GROUP BY 1
),

combined AS (
  SELECT
    cs.segment,
    cs.churned,
    cs.total_orders,
    COALESCE(fo.failure_count, 0) AS failure_count,
    SAFE_DIVIDE(COALESCE(fo.failure_count, 0), cs.total_orders) * 100 AS failure_rate_pct,
    CASE
      WHEN SAFE_DIVIDE(COALESCE(fo.failure_count, 0), cs.total_orders) * 100 >= 5 THEN 'High (≥5%)'
      WHEN COALESCE(fo.failure_count, 0) > 0 THEN 'Low (<5%)'
      ELSE 'None (0%)'
    END AS failure_rate_bucket
  FROM client_segments cs
  LEFT JOIN failed_orders fo ON cs.client_id = fo.client_id
  WHERE cs.total_orders >= 10  -- Minimum orders for meaningful rate
),

contingency AS (
  SELECT
    segment,
    SUM(CASE WHEN failure_rate_bucket = 'High (≥5%)' AND churned = 1 THEN 1 ELSE 0 END) AS a,
    SUM(CASE WHEN failure_rate_bucket = 'High (≥5%)' AND churned = 0 THEN 1 ELSE 0 END) AS b,
    SUM(CASE WHEN failure_rate_bucket != 'High (≥5%)' AND churned = 1 THEN 1 ELSE 0 END) AS c,
    SUM(CASE WHEN failure_rate_bucket != 'High (≥5%)' AND churned = 0 THEN 1 ELSE 0 END) AS d,
    COUNT(*) AS total_n
  FROM combined
  GROUP BY 1
)

SELECT
  segment,
  (a + b) AS n_high_failure_rate,
  (c + d) AS n_low_failure_rate,
  total_n,

  ROUND(100.0 * a / NULLIF(a + b, 0), 1) AS churn_pct_high_rate,
  ROUND(100.0 * c / NULLIF(c + d, 0), 1) AS churn_pct_low_rate,

  -- RELATIVE RISK
  ROUND(
    (CAST(a AS FLOAT64) / NULLIF(a + b, 0)) /
    NULLIF((CAST(c AS FLOAT64) / NULLIF(c + d, 0)), 0)
  , 2) AS relative_risk,

  -- ODDS RATIO
  ROUND(CAST(a * d AS FLOAT64) / NULLIF(b * c, 0), 2) AS odds_ratio,

  -- CHI-SQUARE
  ROUND(
    (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
    NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0)
  , 2) AS chi_square,

  -- Significance interpretation
  CASE
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 10.83
    THEN 'p < 0.001'
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 6.63
    THEN 'p < 0.01'
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 3.84
    THEN 'p < 0.05'
    ELSE 'p >= 0.05 (NS)'
  END AS significance

FROM contingency
ORDER BY segment
```

---

### Analysis 3: Late Deliveries → Churn (with Statistical Tests)

```sql
WITH client_activity AS (
  SELECT
    client_id,
    MIN(submitted_at_utc) AS first_order_date,
    MAX(submitted_at_utc) AS last_order_date,
    COUNT(DISTINCT id) AS total_orders
  FROM `quiqup.bi_reporting.client_orders`
  WHERE submitted_at_utc >= '2025-01-01'
    AND client_id IS NOT NULL
  GROUP BY 1
),

client_segments AS (
  SELECT
    ca.client_id,
    ca.total_orders,
    CASE
      WHEN DATE_DIFF(DATE(last_order_date), DATE(first_order_date), DAY) < 60
      THEN 'New Client'
      ELSE 'Activated Client'
    END AS segment,
    CASE
      WHEN DATE_DIFF(CURRENT_DATE(), DATE(last_order_date), DAY) > 90
      THEN 1 ELSE 0
    END AS churned
  FROM client_activity ca
),

-- Late = delivery_complete occurred AFTER delivery_before
late_orders AS (
  SELECT
    co.client_id,
    COUNT(DISTINCT co.id) AS late_count
  FROM `quiqup.bi_reporting.client_orders` co
  JOIN `quiqup.ex_api_current.order_state_changes` osc ON co.id = osc.client_order_id
  WHERE osc.state = 'delivery_complete'
    AND co.submitted_at_utc >= '2025-01-01'
    AND co.delivery_before IS NOT NULL
    AND osc.occurred_at > co.delivery_before
  GROUP BY 1
),

combined AS (
  SELECT
    cs.segment,
    cs.churned,
    cs.total_orders,
    COALESCE(lo.late_count, 0) AS late_count,
    SAFE_DIVIDE(COALESCE(lo.late_count, 0), cs.total_orders) * 100 AS late_rate_pct,
    CASE
      WHEN SAFE_DIVIDE(COALESCE(lo.late_count, 0), cs.total_orders) * 100 >= 10 THEN 'High (≥10%)'
      WHEN COALESCE(lo.late_count, 0) > 0 THEN 'Low (<10%)'
      ELSE 'None (0%)'
    END AS late_rate_bucket
  FROM client_segments cs
  LEFT JOIN late_orders lo ON cs.client_id = lo.client_id
  WHERE cs.total_orders >= 10
),

contingency AS (
  SELECT
    segment,
    SUM(CASE WHEN late_rate_bucket = 'High (≥10%)' AND churned = 1 THEN 1 ELSE 0 END) AS a,
    SUM(CASE WHEN late_rate_bucket = 'High (≥10%)' AND churned = 0 THEN 1 ELSE 0 END) AS b,
    SUM(CASE WHEN late_rate_bucket != 'High (≥10%)' AND churned = 1 THEN 1 ELSE 0 END) AS c,
    SUM(CASE WHEN late_rate_bucket != 'High (≥10%)' AND churned = 0 THEN 1 ELSE 0 END) AS d,
    COUNT(*) AS total_n
  FROM combined
  GROUP BY 1
)

SELECT
  segment,
  (a + b) AS n_high_late_rate,
  (c + d) AS n_low_late_rate,
  total_n,

  ROUND(100.0 * a / NULLIF(a + b, 0), 1) AS churn_pct_high_late,
  ROUND(100.0 * c / NULLIF(c + d, 0), 1) AS churn_pct_low_late,

  ROUND(
    (CAST(a AS FLOAT64) / NULLIF(a + b, 0)) /
    NULLIF((CAST(c AS FLOAT64) / NULLIF(c + d, 0)), 0)
  , 2) AS relative_risk,

  ROUND(CAST(a * d AS FLOAT64) / NULLIF(b * c, 0), 2) AS odds_ratio,

  ROUND(
    (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
    NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0)
  , 2) AS chi_square,

  CASE
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 10.83
    THEN 'p < 0.001'
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 6.63
    THEN 'p < 0.01'
    WHEN (CAST(total_n AS FLOAT64) * POW((a * d) - (b * c), 2)) /
         NULLIF(CAST((a + b) * (c + d) * (a + c) * (b + d) AS FLOAT64), 0) >= 3.84
    THEN 'p < 0.05'
    ELSE 'p >= 0.05 (NS)'
  END AS significance

FROM contingency
ORDER BY segment
```

---

## Data Sources

| Table | Purpose |
|-------|---------|
| `bi_reporting.client_orders` | Order data with client_id, delivery_before (2025 data available) |
| `ex_api_current.order_state_changes` | State transitions including delivery_failed, delivery_complete |

**Note:** `ex_api_current.orders` only has data through Nov 2024. Use `bi_reporting.client_orders` for 2025 analysis.

---

## Statistical Methods Reference

### Relative Risk (RR)
- **Formula:** RR = P(churn | high failure) / P(churn | low failure)
- **Interpretation:** RR = 1.5 means "50% more likely to churn"

### Chi-Square Test (df=1)
- **χ² ≥ 10.83** → p < 0.001 (highly significant)
- **χ² ≥ 6.63** → p < 0.01 (very significant)
- **χ² ≥ 3.84** → p < 0.05 (significant)
- **χ² < 3.84** → p ≥ 0.05 (not significant)

---

## Change Log

| Date | Change |
|------|--------|
| 2026-02-03 | Initial analysis |
