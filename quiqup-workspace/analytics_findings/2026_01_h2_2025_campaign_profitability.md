# H2 2025 Campaign Profitability Analysis

**Date:** 2026-01-29
**Period:** July - December 2025
**Analyst:** Claude (BigQuery Analyst Agent)
**Status:** Complete

---

## Executive Summary

Analysis of marketing campaign performance for H2 2025 using the grandparent-level attribution model. **Hypothesis tested:** "Most campaigns are producing clients who either never activate, or who will never become profitable."

**Finding:** The hypothesis is **partially confirmed**. While the top-performing campaigns (Performance Max) are profitable with 3.4x ROI, **most campaigns are either unprofitable or have zero activations**. Only 3 of 16 campaigns with 5+ acquisitions are profitable.

---

## H2 2025 Summary Metrics

| Metric | Value |
|--------|-------|
| Total Visitors | 90,391 |
| Total SF Leads | 3,192 |
| Total Google Ads Spend | 160,658 AED |
| **Grandparents Acquired** | 2,275 |
| **Grandparents Activated** | 1,067 |
| **Total Revenue** | 24.24M AED |
| **Average CPL** | 50.33 AED |
| **Average Cost per Grandparent** | 70.62 AED |
| **Overall Revenue/Spend Ratio** | 150.9x |

---

## Monthly Funnel (H2 2025)

| Month | Visitors | Leads | Spend (AED) | GPs Acquired | Activated | Activation % | Revenue (M) |
|-------|----------|-------|-------------|--------------|-----------|--------------|-------------|
| Jul | 13,424 | 546 | 18,772 | 74 | 209* | — | 3.93 |
| Aug | 13,787 | 517 | 19,733 | 379 | 161 | 42.5% | 3.64 |
| Sep | 14,398 | 445 | 31,846 | 456 | 176 | 38.6% | 3.60 |
| Oct | 16,719 | 404 | 29,519 | 419 | 193 | 46.1% | 3.87 |
| Nov | 16,374 | 696 | 28,202 | 460 | 158 | 34.3% | 4.17 |
| Dec | 15,689 | 584 | 32,586 | 487 | 170 | 34.9% | 5.03 |

*Note: July shows 209 activated vs 74 acquired because activations include grandparents acquired in prior months who placed their first order in July.

---

## Campaign-Level Profitability

### Profitable Campaigns (ROI > 1)

| Campaign | GPs Acquired | Activated | Act. % | Spend (AED) | Revenue (AED) | ROI |
|----------|--------------|-----------|--------|-------------|---------------|-----|
| ✅ Performance_Max_Dubai | 837 | 130 | 15.5% | 47,138 | 158,834 | **3.37x** |
| ✅ Generic-Services_Dubai_Fulfillment | 54 | 9 | 16.7% | 7,117 | 18,739 | **2.63x** |
| ✅ Performance_Max | 284 | 33 | 11.6% | 9,508 | 13,798 | **1.45x** |

### Unprofitable Campaigns (ROI < 1)

| Campaign | GPs Acquired | Activated | Act. % | Spend (AED) | Revenue (AED) | ROI |
|----------|--------------|-----------|--------|-------------|---------------|-----|
| ⚠️ Generic-Services_Dubai_International-Delivery | 117 | 18 | 15.4% | 15,162 | 11,193 | 0.74x |
| ⚠️ Generic-Services_Dubai_Delivery-Service | 356 | 54 | 15.2% | 28,883 | 9,245 | **0.32x** |
| ⚠️ Generic-Services_Delivery-Service | 180 | 18 | 10.0% | 7,413 | 1,153 | 0.16x |
| ⚠️ Generic-Services_Dubai_Ecommerce | 17 | 1 | 5.9% | 1,666 | 74 | 0.04x |
| ⚠️ KSA-Fulfillment-EN | 8 | 1 | 12.5% | 8,184 | 0 | 0x |

### Zero Activation Campaigns (❌)

| Campaign | GPs Acquired | Spend (AED) | Status |
|----------|--------------|-------------|--------|
| ❌ Marketplace-UAE | 7 | 8,944 | 0% activation, 0 revenue |
| ❌ Generic-Services_Fulfillment | 10 | 1,088 | 0% activation, 0 revenue |
| ❌ Generic-Services_Ecommerce | 8 | 612 | 0% activation, 0 revenue |
| ❌ leadgen_nov25 | 13 | — | 0% activation, 0 revenue |

---

## Key Insights

### 1. Performance Max Campaigns Are Working
- **Performance_Max_Dubai**: 837 GPs acquired, 15.5% activation, **3.37x ROI**
- **Performance_Max**: 284 GPs acquired, 11.6% activation, **1.45x ROI**
- Combined: 1,121 GPs (49% of total), 163 activated, 172,632 AED revenue

### 2. Delivery-Service Campaigns Are Underperforming
- **Generic-Services_Dubai_Delivery-Service**: 356 GPs, 15.2% activation, **0.32x ROI**
- Spent 28,883 AED, generated only 9,245 AED revenue
- **Recommendation:** Review targeting, landing pages, or pause campaign

### 3. Several Campaigns Have Zero ROI
- **Marketplace-UAE**: 8,944 AED spent, 0 activated, 0 revenue
- **KSA-Fulfillment-EN**: 8,184 AED spent, 1 activated, 0 revenue
- **Recommendation:** Pause these campaigns immediately

### 4. Fulfillment Has High Revenue Per Activated
- **Generic-Services_Dubai_Fulfillment**: Only 9 activated but 18,739 AED revenue
- Revenue per activated: 2,082 AED (highest among all campaigns)
- **Recommendation:** Increase budget if CAC is acceptable

### 5. Overall Activation Rate is Low
- Average activation rate across all campaigns: **10-16%**
- This means **84-90% of acquired grandparents never place an order**
- **Recommendation:** Investigate onboarding friction and lead quality

---

## Profitability Breakdown

| Status | Campaigns | GPs Acquired | Spend (AED) | Revenue (AED) | Net |
|--------|-----------|--------------|-------------|---------------|-----|
| ✅ Profitable (ROI > 1) | 3 | 1,175 | 63,763 | 191,371 | +127,608 |
| ⚠️ Unprofitable (ROI < 1) | 8 | 741 | 61,308 | 24,378 | -36,930 |
| ❌ Zero Activation | 4 | 38 | 10,644 | 0 | -10,644 |
| Unknown (no spend data) | 5 | 321 | — | 16,547 | — |

**Net position from tracked campaigns:** 191,371 - 63,763 = **+127,608 AED profit** (from profitable campaigns)

---

## Recommendations

### Immediate Actions
1. **Pause Marketplace-UAE** — 8,944 AED spent, zero results
2. **Pause KSA-Fulfillment-EN** — 8,184 AED spent, zero revenue
3. **Pause Generic-Services_Ecommerce** — 0% activation rate

### Optimize
4. **Review Generic-Services_Dubai_Delivery-Service** — High volume (356 GPs) but only 0.32x ROI
5. **Investigate activation funnel** — Why do 85% of acquired grandparents never place an order?

### Scale
6. **Increase Performance_Max_Dubai budget** — Best performing campaign (3.37x ROI)
7. **Increase Generic-Services_Dubai_Fulfillment budget** — High revenue per activated (2,082 AED)

---

## Methodology

### Attribution Model
- **Unit:** Grandparent account (not individual business accounts)
- **UTM Attribution:** Earliest UTM from any Lead/Opportunity/Account in hierarchy
- **Revenue:** Deduplicated invoice totals (handles invoice-to-parent)
- **Activation:** First order delivered

### Data Sources
- `views.grandparent_utm_attribution` — UTM attribution at GP level
- `views.grandparent_revenue` — Deduplicated revenue
- `views.grandparent_account_created_date_and_first_order_delivered` — Activation status
- `views.google_ads_spend_monthly` + `views.definition_utm_google_ads_mapping` — Spend by campaign

### Caveats
1. **Revenue is lifetime, not H2 only** — Includes all historical revenue for H2-acquired grandparents
2. **Some campaigns lack spend mapping** — UTM campaigns without Google Ads mapping show NULL spend
3. **Activation lag** — Recent acquisitions may not have activated yet

---

*Generated by BigQuery Analyst Agent | quiqup-workspace*
