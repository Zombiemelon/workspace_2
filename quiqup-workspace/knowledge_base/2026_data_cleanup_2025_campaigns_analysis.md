# 2025 Google Ads Campaign Analysis - MAIN ANALYSIS FILE

**Created:** 2026-01-30
**Status:** Active
**Confidence:** High (>90%)

---

## Executive Summary

Full 2025 Google Ads ROI analysis with campaign-level and ad group-level breakdown. Key findings include critical issues with Demand Gen campaign performance and data labeling problems.

---

## 1. Query Logic Changes (2026-01-30)

### Problem Identified
The original query used a generic label "PMax (no ad group)" for ALL campaigns with NULL ad_group values. This incorrectly merged:
- Performance Max - Dubai
- Performance Max - UAE
- **Demand Gen – UAE** (incorrectly labeled as PMax)

### Fix Applied
Changed the ad_group labeling logic from:
```sql
-- OLD (incorrect)
COALESCE(google_ads_ad_group, 'PMax (no ad group)') AS ad_group
```

To:
```sql
-- NEW (correct)
COALESCE(google_ads_ad_group, google_ads_campaign) AS ad_group
```

**Impact:** Now campaigns without ad groups show their actual campaign name (e.g., "Performance Max - Dubai", "Demand Gen – UAE") instead of a generic placeholder.

---

## 2. URGENT: Demand Gen Campaign Performance Issue

### Summary
| Month | Spend (AED) | Acquisitions | Revenue | ROI |
|-------|-------------|--------------|---------|-----|
| 2025-10 | 200.86 | 0 | 0 | 0% |
| 2025-11 | 3,452.32 | 1 | 0 | 0% |
| 2025-12 | 2,021.02 | 3 | 0 | 0% |
| **TOTAL** | **5,674.20** | **4** | **0** | **0%** |

### Key Metrics
- **Cost Per Acquisition:** 1,418.55 AED
- **Revenue Generated:** 0 AED
- **ROI:** 0%

### The Single November Acquisition
- **Account:** ES S Hassan
- **Acquisition Date:** 2025-11-05
- **Revenue to Date:** 0 AED

### Recommendation
**PAUSE Demand Gen – UAE immediately.** The campaign has burned 5,674 AED with only 4 acquisitions and zero revenue. This is 17x worse CPA than Performance Max campaigns.

---

## 3. Campaign Performance Comparison (2025)

### Top Performers by ROI
| Campaign | Total Spend | GPs Acquired | Revenue | ROI |
|----------|-------------|--------------|---------|-----|
| Performance Max - Dubai | 86,686 | 2,071 | 294,819 | 85.0% |
| Performance Max - UAE | 17,615 | 811 | 37,959 | 53.9% |
| International delivery | 26,004 | 277 | 40,761 | 39.2% |

### Worst Performers
| Campaign | Total Spend | GPs Acquired | Revenue | ROI |
|----------|-------------|--------------|---------|-----|
| Demand Gen – UAE | 5,674 | 4 | 0 | 0% |
| Competitor targeting (various) | ~12,000 | 0 | 0 | 0% |
| Marketplace - UAE | ~12,000 | 15 | 0 | 0% |

---

## 4. Data Quality Issues Found

### 4.1 Competitors-PE Mapping (FIXED 2026-01-30)
- **Issue:** UTM `Competitors-PE` was mapped to discontinued campaign name
- **Root Cause:** Campaign renamed from "Competitors-PE" to "Competitors - UAE" on 2024-11-04
- **Fix:** Updated `definition_utm_google_ads_mapping` view

### 4.2 Demand Gen Labeling (FIXED 2026-01-30)
- **Issue:** Demand Gen campaigns were incorrectly labeled as "PMax (no ad group)"
- **Root Cause:** Generic fallback label for NULL ad_groups
- **Fix:** Changed logic to use campaign name when ad_group is NULL

### 4.3 Pending Investigation
- **July 2025 anomaly:** Significant drop in acquisitions across all campaigns
- **Competitors - UAE:** Shows acquisitions but 0 spend (attribution without tracked spend)

---

## 5. Files & Exports

| File | Description |
|------|-------------|
| [2025_google_ads_adgroup_analysis.csv](../exports/2025_google_ads_adgroup_analysis.csv) | Full 2025 ad group level data with corrected labels |

---

## 6. Tables Used

| Table | Purpose |
|-------|---------|
| `views.grandparent_utm_attribution` | First-touch UTM attribution to grandparent accounts |
| `views.grandparent_revenue` | Lifetime revenue per grandparent (invoice-deduplicated) |
| `views.google_ads_spend_monthly` | Monthly spend by campaign/ad group |
| `views.definition_utm_google_ads_mapping` | UTM → Google Ads campaign mapping |
| `views.definition_paid_organic_channel` | Paid channel classification |

---

## 7. Methodology Notes

### Attribution Model
- **Type:** First-touch at grandparent level
- **Deduplication:** Revenue deduplicated via invoice_to_parent flag
- **Margin Assumption:** 25% of revenue

### ROI Calculation
```
ROI% = (Revenue × 25%) / Spend × 100
```

### Cohort Maturity Warning
December 2025 cohorts have only 1 month of maturity. Use payback period analysis for more accurate assessment of recent cohorts.
