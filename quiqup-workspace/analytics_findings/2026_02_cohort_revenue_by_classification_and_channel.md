# Cohort Revenue Analysis: 2024 vs 2025 by Classification & Channel

**Date:** 2026-02-04
**Analyst:** Claude (BigQuery Analysis)
**Scope:** Clients with first order in 2024/2025, excluding SSUP

---

## Executive Summary

The 2024 cohort (178 non-SSUP clients) generated **9.4M AED** in 2025, a **+130% YoY growth** from their 4.1M AED first-year revenue. Outbound/direct sales dominates both cohorts (80-82% of clients, 84-90% of revenue), while Inbound Paid shows the highest growth trajectory (+212% YoY).

**Confidence:** High (>90%) — revenue from source-of-truth invoices table, cohort from validated grandparent view.

---

## Key Findings

1. **Outbound dominates revenue**: 80-82% of clients, 84-90% of revenue across both cohorts
2. **Inbound Paid highest growth**: +212% YoY for 2024 cohort — Small Business segment grew 829%
3. **Large Enterprise entirely Outbound**: All 8 Large Enterprise clients came through Outbound/direct sales
4. **Strong retention for larger clients**: Medium Business 79.5%, Small Business 91.3%, Large Enterprise 100%
5. **SSUP = 91% of raw cohort**: Excluding SSUP reduces 2024 cohort from 1,256 to 178 clients

---

## 2024 Cohort: Revenue by Channel & Classification

### Inbound - Paid (29 clients)

| Classification | Clients | 2024 Rev (AED) | 2025 Rev (AED) | YoY Growth |
|---------------|---------|----------------|----------------|------------|
| Small Business (5-15 orders) | 6 | 29,442 | 273,595 | +829% |
| Medium Business (16-50 orders) | 7 | 51,366 | 189,269 | +268% |
| Micro-Business (0-4 orders) | 15 | 116,781 | 153,816 | +32% |
| **Total** | **29** | **197,589** | **616,680** | **+212%** |

### Inbound - Organic (6 clients)

| Classification | Clients | 2024 Rev (AED) | 2025 Rev (AED) | YoY Growth |
|---------------|---------|----------------|----------------|------------|
| Medium Business (16-50 orders) | 2 | 44,941 | 130,702 | +191% |
| Micro-Business (0-4 orders) | 3 | 81,025 | 113,703 | +40% |
| Small Business (5-15 orders) | 1 | 730 | 1,953 | +168% |
| **Total** | **6** | **126,696** | **246,358** | **+94%** |

### Outbound / No Attribution (142 clients)

| Classification | Clients | 2024 Rev (AED) | 2025 Rev (AED) | YoY Growth |
|---------------|---------|----------------|----------------|------------|
| Large Enterprise (51+ orders) | 4 | 1,545,834 | 3,318,441 | +115% |
| Medium Business (16-50 orders) | 30 | 1,136,248 | 2,813,509 | +148% |
| Small Business (5-15 orders) | 39 | 657,394 | 1,582,136 | +141% |
| Micro-Business (0-4 orders) | 68 | 341,480 | 621,919 | +82% |
| Store Large Enterprise | 1 | 69,846 | 143,517 | +105% |
| **Total** | **142** | **3,750,802** | **8,479,522** | **+126%** |

### 2024 Cohort Summary

| Channel | Clients | % of Cohort | 2025 Revenue | % of Revenue |
|---------|---------|-------------|--------------|--------------|
| Inbound - Paid | 29 | 16% | 616,680 | 7% |
| Inbound - Organic | 6 | 3% | 246,358 | 3% |
| Outbound / No Attribution | 142 | 80% | 8,479,522 | 90% |
| **Total** | **178** | **100%** | **9,388,176** | **100%** |

---

## 2025 Cohort: First-Year Revenue by Channel & Classification

### Inbound - Paid (20 clients)

| Classification | Clients | 2025 Rev (AED) |
|---------------|---------|----------------|
| Medium Business (16-50 orders) | 5 | 146,217 |
| Small Business (5-15 orders) | 5 | 82,822 |
| Micro-Business (0-4 orders) | 10 | 61,854 |
| **Total** | **20** | **290,893** |

### Inbound - Organic (1 client)

| Classification | Clients | 2025 Rev (AED) |
|---------------|---------|----------------|
| Micro-Business (0-4 orders) | 1 | 7,354 |

### Outbound / No Attribution (95 clients)

| Classification | Clients | 2025 Rev (AED) |
|---------------|---------|----------------|
| Small Business (5-15 orders) | 31 | 631,462 |
| Medium Business (16-50 orders) | 25 | 613,128 |
| Micro-Business (0-4 orders) | 34 | 246,978 |
| Large Enterprise (51+ orders) | 4 | 104,842 |
| **Total** | **95** | **1,596,434** |

### 2025 Cohort Summary

| Channel | Clients | % of Cohort | 2025 Revenue | % of Revenue |
|---------|---------|-------------|--------------|--------------|
| Inbound - Paid | 20 | 17% | 290,893 | 15% |
| Inbound - Organic | 1 | 1% | 7,354 | 0.4% |
| Outbound / No Attribution | 95 | 82% | 1,596,434 | 84% |
| **Total** | **116** | **100%** | **1,894,680** | **100%** |

---

## Cohort Comparison

| Metric | 2024 Cohort | 2025 Cohort |
|--------|-------------|-------------|
| Total clients (excl. SSUP) | 178 | 116 |
| First-year revenue | 4,076,975 AED | 1,894,680 AED |
| Second-year revenue | 9,388,176 AED | — |
| YoY growth | +130% | — |
| Avg revenue/client (Year 1) | 22,904 AED | 16,333 AED |
| Retention into Year 2 | 81.5% | — |
| % Outbound clients | 80% | 82% |
| % Outbound revenue | 90% | 84% |

---

## Methodology

### Data Sources
- **Cohort definition:** `views.grandparent_account_created_date_and_first_order_delivered` — first delivered order date
- **Revenue:** `invoicer_current.invoices` — net of tax, state IN ('paid', 'overdue')
- **Classification:** `salesforce_current.accounts.client_classification_c`
- **Channel:** `views.grandparent_utm_attribution` + `views.definition_paid_organic_channel`

### Exclusions
- **SSUP clients:** Children of parent account `0010800003I4PcsAAF` (Self-Sign Up Parent)
  - Rationale: SSUP = 91% of raw cohort but low-value self-service signups
  - Source: [bigquery_execution_reference.md](../agents/bigquery_execution_reference.md) lines 778-780

### Channel Classification Logic
- **Inbound - Paid:** Has UTM attribution with `is_paid = TRUE` (via `definition_paid_organic_channel`)
- **Inbound - Organic:** Has UTM attribution with `is_paid = FALSE`
- **Outbound / No Attribution:** No UTM attribution — likely direct sales/BDM sourced

### Caveats
- ~80% of non-SSUP clients have no UTM attribution
- 2025 cohort has partial year exposure (clients acquired later in 2025 have less time to generate revenue)
- Client classification is current state, not at time of acquisition

---

## Appendix: Classification Definitions

| Classification | Order Volume |
|----------------|--------------|
| Micro-Business | 0-4 orders |
| Small Business | 5-15 orders |
| Medium Business | 16-50 orders |
| Large Enterprise | 51+ orders |
| Store Large Enterprise | Large retail/store accounts |
| Fulfillment | Fulfillment-specific accounts |
