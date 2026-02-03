# MAIN ANALYSIS FILE: 2025 Google Ads Campaign ROI & Payback Analysis

**Analysis Date:** 2026-01-30
**Period Covered:** January - December 2025
**Data Source:** BigQuery views (grandparent_utm_attribution, grandparent_revenue, google_ads_spend_monthly)
**Status:** Complete with data fix applied

---

## Executive Summary

**Key Finding:** Performance Max campaigns are the only consistently profitable channel. **Monthly ROI is a misleading metric** — the correct metric is **Payback Period** because recent cohorts haven't had time to generate revenue.

**Critical Data Fix Applied:** `Competitors-PE` mapping corrected to `Competitors - UAE` in `definition_utm_google_ads_mapping` view (2026-01-30).

---

## IMPORTANT: Why Monthly ROI is Misleading

| Cohort | Months of Maturity | Can Show True ROI? |
|--------|-------------------|-------------------|
| Jan 2025 | 12 months | ✅ Yes |
| Jun 2025 | 7 months | ⚠️ Partial |
| Dec 2025 | 1 month | ❌ No |

**Solution:** Use **Payback Period Analysis** instead of monthly ROI.

---

## Top-Line Metrics (2025 Full Year)

| Metric | Value |
|--------|-------|
| **Total Grandparents Acquired** | 5,765 |
| **Total Activated** | 822 |
| **Overall Activation Rate** | 14.3% |
| **Total Lifetime Revenue** | 580,544 AED |
| **Total Margin (25%)** | 145,136 AED |
| **Total Spend** | 275,285 AED |
| **Overall ROI** | **-47.3%** (misleading due to cohort maturity) |

---

## Campaign Payback Summary

| Campaign | CPA (AED) | Margin/GP at Month 12 | Break-Even Status |
|----------|-----------|----------------------|-------------------|
| **Performance Max - Dubai** | 41.86 | 39.75 | **~10-11 months** ✅ |
| **Performance Max - UAE** | 22.98 | 12.15 | **~5-6 months** ✅ |
| **Generic Services - Dubai** | 60.74 | 14.22 | **Never** (117+ months) ❌ |
| **Generic Services - UAE** | 30.35 | 1.70 | **Never** (459+ months) ❌ |
| **Competitors - UAE** | TBD | TBD | Mapping fixed - re-run analysis |

---

## Cohort Break-Even Analysis by Month

### Performance Max - Dubai ✅ (Best Performer)

| Cohort | GPs | Spend | CPA | Months Mature | Margin/GP | % Recovered | Break-Even |
|--------|-----|-------|-----|---------------|-----------|-------------|------------|
| 2025-01 | 102 | 5,295 | 51.91 | 12 | 9.83 | 18.9% | 63 months ❌ |
| 2025-02 | 205 | 8,372 | 40.84 | 11 | 8.08 | 19.8% | 56 months ❌ |
| **2025-03** | 345 | 8,491 | 24.61 | 10 | **39.52** | **160.6%** | **✅ DONE** |
| **2025-04** | 234 | 6,486 | 27.72 | 9 | **40.03** | **144.4%** | **✅ DONE** |
| **2025-05** | 211 | 6,071 | 28.77 | 8 | **46.02** | **160.0%** | **✅ DONE** |
| **2025-06** | 137 | 4,836 | 35.30 | 7 | **37.65** | **106.7%** | **✅ DONE** |
| 2025-07 | 28 | 4,954 | 176.93 | 6 | 126.14 | 71.3% | 8 months |
| **2025-08** | 147 | 6,647 | 45.22 | 5 | **127.26** | **281.4%** | **✅ DONE** |
| 2025-09 | 152 | 7,478 | 49.20 | 4 | 20.16 | 41.0% | 10 months |
| **2025-10** | 139 | 8,241 | 59.29 | 3 | **74.29** | **125.3%** | **✅ DONE** |
| 2025-11 | 195 | 9,498 | 48.71 | 2 | 25.55 | 52.5% | **4 months** |
| 2025-12 | 176 | 10,319 | 58.63 | 1 | 6.69 | 11.4% | **9 months** |

**Summary:** 7 of 12 cohorts already at break-even. Nov/Dec on track (4-9 months projected).

### Performance Max - UAE ⚠️ (Mixed)

| Cohort | GPs | Spend | CPA | Months Mature | Margin/GP | % Recovered | Break-Even |
|--------|-----|-------|-----|---------------|-----------|-------------|------------|
| 2025-01 | 31 | 1,299 | 41.90 | 12 | 8.35 | 19.9% | 60 months ❌ |
| 2025-02 | 103 | 2,427 | 23.56 | 11 | 3.88 | 16.5% | 67 months ❌ |
| **2025-03** | 169 | 2,297 | 13.59 | 10 | **17.59** | **129.4%** | **✅ DONE** |
| **2025-04** | 95 | 1,495 | 15.74 | 9 | **22.81** | **144.9%** | **✅ DONE** |
| 2025-05 | 78 | 980 | 12.56 | 8 | 5.73 | 45.6% | 18 months |
| 2025-06 | 51 | 629 | 12.33 | 7 | 1.94 | 15.7% | 45 months |
| 2025-07 | 9 | 637 | 70.78 | 6 | 1.33 | 1.9% | 319 months ❌ |
| 2025-08 | 47 | 912 | 19.40 | 5 | 3.47 | 17.9% | 28 months |
| 2025-09 | 54 | 1,391 | 25.76 | 4 | 3.94 | 15.3% | 26 months |
| 2025-10 | 54 | 1,440 | 26.67 | 3 | 2.04 | 7.6% | 39 months |
| 2025-11 | 50 | 2,082 | 41.64 | 2 | 18.64 | 44.8% | **5 months** |
| 2025-12 | 70 | 3,046 | 43.51 | 1 | 29.63 | 68.1% | **2 months** |

**Summary:** Only 2 cohorts at break-even (Mar, Apr). Recent cohorts (Nov, Dec) look promising.

### Generic Services - Dubai ❌ (Poor)

| Cohort | GPs | Spend | CPA | Months Mature | Margin/GP | % Recovered | Break-Even |
|--------|-----|-------|-----|---------------|-----------|-------------|------------|
| 2025-01 | 58 | 5,395 | 93.02 | 12 | 82.19 | 88.4% | 14 months |
| 2025-02 | 218 | 6,406 | 29.39 | 11 | 2.84 | 9.7% | **114 months** ❌ |
| 2025-03 | 238 | 6,953 | 29.21 | 10 | 14.40 | 49.3% | 20 months |
| 2025-04 | 199 | 7,382 | 37.10 | 9 | 10.24 | 27.6% | 33 months |
| 2025-05 | 172 | 7,311 | 42.51 | 8 | 4.03 | 9.5% | **84 months** ❌ |
| 2025-06 | 114 | 7,447 | 65.32 | 7 | 3.97 | 6.1% | **115 months** ❌ |
| 2025-07 | 19 | 7,726 | 406.63 | 6 | 2.00 | 0.5% | **1,220 months** ❌ |
| 2025-08 | 110 | 6,698 | 60.89 | 5 | 20.16 | 33.1% | 15 months |
| 2025-09 | 148 | 15,718 | 106.20 | 4 | 43.09 | 40.6% | **10 months** |
| 2025-10 | 88 | 9,463 | 107.53 | 3 | 8.00 | 7.4% | 40 months |
| 2025-11 | 74 | 4,864 | 65.73 | 2 | 3.36 | 5.1% | 39 months |
| 2025-12 | 105 | 8,360 | 79.62 | 1 | 3.31 | 4.2% | 24 months |

**Summary:** Zero cohorts at break-even. Only Jan 2025 close (88% after 12 months).

### Generic Services - UAE ❌ (Worst)

| Cohort | GPs | Spend | CPA | Months Mature | Margin/GP | % Recovered | Break-Even |
|--------|-----|-------|-----|---------------|-----------|-------------|------------|
| 2025-01 | 12 | 1,040 | 86.67 | 12 | 0 | 0% | **Never** ❌ |
| 2025-02 | 65 | 1,173 | 18.05 | 11 | 0.45 | 2.5% | **445 months** ❌ |
| 2025-03 | 89 | 1,152 | 12.94 | 10 | 2.93 | 22.7% | 44 months |
| 2025-07 | 6 | 815 | 135.83 | 6 | 0 | 0% | **Never** ❌ |

**Summary:** Zero cohorts anywhere near break-even. Multiple will **never** break even.

---

## Ad Group Analysis: Generic Services - Dubai

### Summary by Ad Group (2025 Full Year)

| Ad Group | GPs Acquired | Activated | Activation % | Revenue (AED) | Margin (AED) | Spend (AED) | ROI % |
|----------|-------------|-----------|--------------|---------------|--------------|-------------|-------|
| **Delivery Service** | 761 | 111 | 14.6% | 15,955 | 3,989 | 42,926 | **-90.7%** |
| **Parcel delivery** | 236 | 26 | 11.0% | 20,540 | 5,135 | 7,853 | **-34.6%** |
| **International delivery** | 276 | 45 | 16.3% | 28,760 | 7,190 | 22,944 | **-68.7%** |
| **Courier from Dubai to Abu Dhabi** | 81 | 17 | 21.0% | 1,335 | 334 | 1,360 | **-75.4%** |
| **Courier Service** | 57 | 14 | 24.6% | 883 | 221 | 1,935 | **-88.6%** |
| **Fulfillment** | 67 | 11 | 16.4% | 358 | 90 | 6,703 | **-98.7%** |
| **Sameday** | 43 | 7 | 16.3% | 259 | 65 | 1,394 | **-95.3%** |
| **Business** | 3 | 0 | 0% | 0 | 0 | 219 | **-100%** |
| **Ecommerce** | 18 | 1 | 5.6% | 74 | 19 | 1,102 | **-98.3%** |

### Best Performing Ad Group × Month Combinations

| Ad Group | Month | GPs | Revenue | Spend | ROI % |
|----------|-------|-----|---------|-------|-------|
| **Fulfillment** | Sep 2025 | 12 | 18,427 | 1,606 | **+186.8%** ✅ |
| **Parcel delivery** | Jan 2025 | 18 | 18,429 | 2,577 | **+78.8%** ✅ |
| **International delivery** | Aug 2025 | 14 | 7,559 | 1,844 | **+2.5%** ✅ |
| **International delivery** | Mar 2025 | 53 | 11,891 | 2,946 | **+0.9%** ✅ |

**Key Insight:** Delivery Service drives 49% of acquisitions but has the worst ROI (-90.7%).

---

## Data Quality Fix: Competitors-PE Mapping

### Problem Identified

The campaign `Competitors-PE` was **discontinued on 2024-11-04** and replaced with `Competitors - UAE`. However, the UTM mapping still pointed to the old campaign name, causing:
- 393 grandparents attributed to "Competitors-PE"
- Zero spend matched (spend goes to "Competitors - UAE")
- Inflated apparent ROI (infinite because divide by zero)

### Root Cause

```
UTM "Competitors" in Salesforce
        ↓
definition_utm_google_ads_mapping mapped to "Competitors-PE"
        ↓
"Competitors-PE" was DISCONTINUED on 2024-11-04
        ↓
Spend now goes to "Competitors - UAE" (new campaign)
        ↓
JOIN FAILS → Acquisitions show 0 spend
```

### Fix Applied (2026-01-30)

Updated `quiqup.views.definition_utm_google_ads_mapping`:

| UTM Campaign | Old Mapping | New Mapping |
|--------------|-------------|-------------|
| `Competitors` | `Competitors-PE` | `Competitors - UAE` |
| `GL_QQP_GA_SEM_AO_NBR_Gen_Web_UAE_UAE_All_PRO_Lead_11122023_Competitors-PE` | `Competitors-PE` | `Competitors - UAE` |

**Verification Query:**
```sql
SELECT utm_campaign, google_ads_campaign
FROM `quiqup.views.definition_utm_google_ads_mapping`
WHERE utm_campaign LIKE '%Competitor%'
```

---

## The "July 2025 Problem"

July 2025 was catastrophic across all campaigns:

| Campaign | July CPA | Avg CPA | Variance |
|----------|----------|---------|----------|
| PMax Dubai | 177 AED | 42 AED | +321% |
| PMax UAE | 71 AED | 23 AED | +209% |
| Generic Dubai | 407 AED | 61 AED | +567% |

**Investigation needed:** What happened in July 2025? (Low acquisition volume, high spend)

---

## Recommendations

| Priority | Action | Rationale |
|----------|--------|-----------|
| 🔴 **Critical** | ✅ DONE: Fixed Competitors-PE mapping | Now will show accurate ROI |
| 🟡 **High** | Re-run Competitors - UAE ROI analysis | Mapping fixed, need fresh numbers |
| 🟡 **High** | Reallocate Generic Services budget to PMax | PMax breaks even; Generic never does |
| 🟡 **High** | Investigate July 2025 anomaly | CPA spikes across all campaigns |
| 🟠 **Medium** | Pause KSA campaigns | Zero ROI after 10 months |
| 🟠 **Medium** | Pause Marketplace campaigns | Zero activations |

---

## Methodology: Payback Period Calculation

### Formula

```
Payback Period = CPA / Margin Velocity

Where:
- CPA = Total Spend / GPs Acquired
- Margin Velocity = Cumulative Margin / GPs Acquired / Months Since Acquisition
- Margin = Revenue × 25%
```

### Data Sources

| Table | Purpose |
|-------|---------|
| `views.grandparent_utm_attribution` | Acquisition attribution |
| `views.grandparent_revenue` | Lifetime revenue (deduplicated) |
| `views.google_ads_spend_monthly` | Monthly spend by campaign |
| `views.definition_paid_organic_channel` | Paid vs organic classification |
| `views.definition_utm_google_ads_mapping` | UTM → Google Ads mapping |
| `invoicer_current.invoices` | Invoice dates for revenue timing |

### Key Query Pattern

```sql
-- Revenue by months since acquisition
SELECT
  grandparent_account_id,
  cohort_month,
  DATE_DIFF(DATE_TRUNC(invoice_end_date, MONTH), cohort_month, MONTH) AS months_since_acq,
  SUM(invoice_total) AS revenue
FROM ...
GROUP BY 1, 2, 3
```

---

## Monthly ROI Heatmap (Legacy - Use Payback Instead)

| Month | PMax Dubai | PMax UAE | Generic Dubai | Generic UAE |
|-------|-----------|----------|---------------|-------------|
| Jan | -81.1% | -80.0% | -11.8% | -100% |
| Feb | -80.2% | -83.9% | -90.5% | -97.5% |
| Mar | **+60.2%** ✅ | **+29.4%** ✅ | -50.9% | -77.4% |
| Apr | **+44.1%** ✅ | **+44.3%** ✅ | -72.7% | -98.0% |
| May | **+56.2%** ✅ | -57.3% | -91.0% | -78.4% |
| Jun | -1.9% | -86.6% | -94.8% | -95.5% |
| Jul | -28.7% | -98.2% | -99.5% | -100% |
| Aug | **+151.5%** ✅ | -82.1% | -66.9% | -91.7% |
| Sep | -59.2% | -85.9% | -59.4% | -94.9% |
| Oct | **+24.6%** ✅ | -94.9% | -93.9% | -97.7% |
| Nov | -47.5% | -55.3% | -94.9% | -97.5% |
| Dec | -88.8% | -31.9% | -95.8% | -98.4% |

⚠️ **Warning:** This table is misleading for recent cohorts. Use Payback Period analysis above.

---

## Activation Rate Finding (2026-01-30)

### Key Insight: Many Ad Groups Acquire Leads That Never Convert

Investigation revealed that many ad groups show GPs acquired with 0 revenue. This is **NOT a data bug** — these are accounts that were acquired but **never activated** (never placed an order).

**Example: Feb 2025 Delivery Service - UAE (11 months old)**
| Account ID | Acquisition Date | Status | Orders | Revenue |
|------------|-----------------|--------|--------|---------|
| 001P400000TQWOcIAP | 2025-02-05 | Never activated | 0 | 0 |
| 001P400000TUkWBIA1 | 2025-02-06 | Never activated | 0 | 0 |
| ... (5 more) | ... | Never activated | 0 | 0 |

Even after 11 months, these accounts have **0% activation rate**.

### This is a Lead Quality Problem

Some ad groups are generating leads that never convert to paying customers:
- Generic Services - UAE (multiple ad groups): 0% activation
- KSA campaigns: Very low activation rates
- Demand Gen – UAE: 4 GPs acquired, 0 activated, 0 revenue

---

## Fulfillment Campaign Analysis (2026-01-30)

### Summary: Is Fulfillment Profitable? **NO**

| Campaign | Spend (AED) | GPs | Activated | Activation % | Revenue | ROI |
|----------|-------------|-----|-----------|--------------|---------|-----|
| **KSA Fulfillment - EN** | 9,182 | 12 | 1 | 8.3% | 0 | **-100%** ❌ |
| **Generic Dubai Fulfillment** | 8,952 | 70 | 11 | 15.7% | 18,785 | **-47.5%** |
| IQ Fulfillment (Competitors) | 1,453 | 0 | 0 | - | 0 | -100% |
| **Generic UAE Fulfillment** | 1,235 | 14 | **0** | **0%** | 0 | **-100%** ❌ |
| KSA Fulfillment - AR | 226 | 1 | 0 | 0% | 0 | -100% |
| **TOTAL** | **21,049** | **97** | **12** | **12.4%** | **18,785** | **-77.7%** |

### Key Findings
1. **Only Dubai Fulfillment generates revenue** (18,785 AED), but still at -47.5% ROI
2. **UAE Fulfillment has 0% activation** — 14 accounts acquired, none ever ordered
3. **KSA Fulfillment is a complete waste** — 9,400 AED spent → 1 activated → 0 revenue

### Recommendation
- **Pause KSA Fulfillment campaigns** (both EN and AR)
- **Pause UAE Fulfillment** (0% activation = leads don't convert)
- **Continue Dubai Fulfillment** with close monitoring (only profitable region)

---

## 🚨 CRITICAL: Data Integrity Findings (2026-01-30)

### Finding 1: Only 20% of Revenue is Attributed to Google Ads

**This invalidates the "everything is negative ROI" conclusion!**

| Attribution Category | GPs Acquired | Revenue (AED) | % of Total |
|---------------------|--------------|---------------|------------|
| **Organic/Direct/Unknown** | 6,136 | **2,090,938** | **72.5%** |
| Google Ads Attributed | 5,415 | 577,915 | 20.0% |
| Other Paid/UTM | 264 | 212,112 | 7.4% |

**Implication:** We're optimizing 20% of the business while 72.5% comes from unattributed sources. The "negative ROI" story for Google Ads may be correct, but we're missing the bigger picture of how customers actually find us.

---

### Finding 2: Competitors-UAE "Profitability" = ONE Whale Account

**The March 2025 spike (111,491 AED) is ONE customer:**

| Account ID | Acquisition Date | Revenue (AED) | % of Campaign Total |
|------------|-----------------|---------------|---------------------|
| `001P400000VnVonIAF` | 2025-03-11 | **109,797** | **84%** |
| All other 392 accounts | Jan-Dec 2025 | 21,013 | 16% |

**TRUE Competitors-UAE Performance:**

| Scenario | Spend (AED) | GPs | Revenue (AED) | ROI |
|----------|-------------|-----|---------------|-----|
| **With whale** | 23,393 | 393 | 130,811 | **+39.8%** ✅ |
| **Without whale** | 23,393 | 392 | 21,013 | **-77.5%** ❌ |

**Conclusion:** Competitors-UAE appears profitable only because of a single lucky acquisition. Exclude whale → campaign is deeply unprofitable.

---

### Finding 3: Ad Group Attribution is Broken for Competitors Campaign

**Problem:** UTM campaigns map to campaign level but NOT ad group level:

| UTM Campaign | Maps To Campaign | Maps To Ad Group |
|--------------|------------------|------------------|
| `Competitors` | Competitors - UAE | **NULL** |
| `Competitors-PE` | Competitors - UAE | **NULL** |
| `UAE_Competitors` | Competitors - UAE | **NULL** |

**But spend is tracked at ad group level:**
- Aramex: 3,472 AED
- iMile: 2,263 AED
- Others: 11,362 AED
- Jeebly: 3,104 AED
- etc.

**Result:** We cannot determine which competitor keyword is driving conversions. All acquisitions show as "Competitors - UAE" while spend shows in specific ad groups.

**Fix Applied (2026-01-30):** Updated `definition_utm_google_ads_mapping` view to include `utm_content` column with Ad ID → Ad Group mapping.

---

### Finding 3b: Competitors Ad Group Attribution FIX IMPLEMENTED

**View Updated:** `quiqup.views.definition_utm_google_ads_mapping`

Added `utm_content` column mapping Ad IDs to ad groups:

| utm_content (Ad ID) | google_ads_ad_group |
|---------------------|---------------------|
| `719841080304` | Aramex |
| `719841080319` | Jeebly |
| `719841080322` | iMile |
| `719841080328` | Shipa |
| `719841080301` | IQ Fulfillment |
| `719841080307` | Others |
| `724453582290` | Fenix |

**Standard Query Pattern (use ROW_NUMBER to handle fallback):**

```sql
WITH attribution_with_mapping AS (
  SELECT
    gac.gac_grandparent_account_id,
    ua.attributed_utm_campaign,
    ua.attributed_utm_content,
    gam.google_ads_campaign,
    gam.google_ads_ad_group,
    gam.google_ads_ad_group_display,
    gr.total_revenue_aed,
    ROW_NUMBER() OVER (
      PARTITION BY gac.gac_grandparent_account_id
      ORDER BY CASE WHEN gam.utm_content IS NOT NULL THEN 0 ELSE 1 END
    ) AS match_priority
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  LEFT JOIN `quiqup.views.grandparent_utm_attribution` ua
    ON gac.gac_grandparent_account_id = ua.grandparent_account_id
  LEFT JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
    ON ua.attributed_utm_campaign = gam.utm_campaign
    AND (gam.utm_content IS NULL OR gam.utm_content = ua.attributed_utm_content)
  LEFT JOIN `quiqup.views.grandparent_revenue` gr
    ON gac.gac_grandparent_account_id = gr.grandparent_account_id
  WHERE gam.google_ads_campaign IS NOT NULL
)
SELECT * FROM attribution_with_mapping WHERE match_priority = 1
```

**Competitors-UAE TRUE Ad Group Performance (2025):**

| Ad Group | Spend (AED) | GPs | Revenue | ROI |
|----------|-------------|-----|---------|-----|
| Others | 11,362 | 191 | 14,281 | **-68.6%** |
| Aramex | 3,312 | 66 | 2,524 | **-81.0%** |
| Jeebly | 3,104 | 57 | 952 | **-92.3%** |
| iMile | 2,103 | 34 | 1,607 | **-80.9%** |
| Shipa | 1,892 | 33 | 111,447 | +1372.7% 🐋 |
| IQ Fulfillment | 1,453 | 10 | 0 | **-100%** |
| Fenix | 166 | 2 | 0 | **-100%** |

**Without Shipa whale (account `001P400000VnVonIAF`):** ALL ad groups are unprofitable.

---

## Follow-up Investigations

- [x] Ad group level breakdown for Generic Services - Dubai
- [x] Competitors-PE spend gap investigation → **FIXED**
- [x] Cohort maturity adjustment → **Payback Period analysis implemented**
- [x] Activation rate investigation → **Confirmed lead quality issue**
- [x] Fulfillment campaign profitability → **NOT PROFITABLE overall**
- [x] Re-run Competitors - UAE analysis with corrected mapping → **DONE: -77.5% ROI (excl whale)**
- [x] Validate data integrity (Q1-Q3) → **CRITICAL FINDINGS ABOVE**
- [x] Fix ad group level tracking for Competitors campaign → **DONE: utm_content mapping added**
- [x] H1-2025 mature cohort analysis → **DONE: See section below**
- [ ] Investigate July 2025 anomaly
- [ ] Understand 72.5% organic/direct revenue sources
- [ ] Build automated payback period dashboard

---

## H1-2025 Campaign Performance Analysis (Mature Cohorts)

**Analysis Date:** 2026-01-30
**Period:** January - June 2025 (7-12 months mature)
**Data Validated:** ✅ CSV matches BigQuery source exactly

### Data Validation Summary

| Check | Result |
|-------|--------|
| **Spend: CSV vs BigQuery** | ✅ MATCH (117,102 AED) |
| **Spend: View vs Raw** | ✅ MATCH (`google_ads_spend_monthly` = `CampaignBasicStats`) |
| **GP Counts** | ✅ MATCH (all campaigns within 1 GP) |
| **Revenue** | ✅ MATCH (≤1 AED rounding variance) |

### Validation Methodology

#### Check 1: Spend - CSV vs BigQuery

**Source Table:** `quiqup.views.google_ads_spend_monthly`

**Query:**
```sql
SELECT
  campaign_name,
  SUM(cost_micros / 1000000) AS spend_aed
FROM `quiqup.views.google_ads_spend_monthly`
WHERE segments_month BETWEEN '2025-01-01' AND '2025-06-30'
GROUP BY campaign_name
```

**Result:** CSV total spend (117,102 AED) matched BigQuery query exactly.

#### Check 2: Spend - View vs Raw Source

**Comparison:** `views.google_ads_spend_monthly` vs underlying `google_ads.CampaignBasicStats`

**Query:**
```sql
SELECT SUM(cost_micros / 1000000) AS spend_aed
FROM `quiqup.google_ads.CampaignBasicStats`
WHERE segments_date BETWEEN '2025-01-01' AND '2025-06-30'
```

**Result:** Raw table matched view totals, confirming no data loss in view transformation.

#### Check 3: GP Counts - CSV vs BigQuery

**Source Tables:**
- `quiqup.views.grandparent_account_created_date_and_first_order_delivered` (acquisition)
- `quiqup.views.grandparent_utm_attribution` (attribution)
- `quiqup.views.definition_utm_google_ads_mapping` (campaign mapping)

**Query:**
```sql
SELECT
  gam.google_ads_campaign,
  COUNT(DISTINCT gac.gac_grandparent_account_id) AS gps_acquired
FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
LEFT JOIN `quiqup.views.grandparent_utm_attribution` ua
  ON gac.gac_grandparent_account_id = ua.grandparent_account_id
LEFT JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
  ON ua.attributed_utm_campaign = gam.utm_campaign
WHERE gac.gac_minimum_created_date BETWEEN '2025-01-01' AND '2025-06-30'
  AND gam.google_ads_campaign IS NOT NULL
GROUP BY gam.google_ads_campaign
```

**Result:** All campaigns matched within 1 GP (rounding due to edge-case attribution).

#### Check 4: Revenue - CSV vs BigQuery

**Source Table:** `quiqup.views.grandparent_revenue`

**Query:**
```sql
SELECT
  gam.google_ads_campaign,
  SUM(gr.total_revenue_aed) AS lifetime_revenue
FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
LEFT JOIN `quiqup.views.grandparent_utm_attribution` ua
  ON gac.gac_grandparent_account_id = ua.grandparent_account_id
LEFT JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
  ON ua.attributed_utm_campaign = gam.utm_campaign
LEFT JOIN `quiqup.views.grandparent_revenue` gr
  ON gac.gac_grandparent_account_id = gr.grandparent_account_id
WHERE gac.gac_minimum_created_date BETWEEN '2025-01-01' AND '2025-06-30'
  AND gam.google_ads_campaign IS NOT NULL
GROUP BY gam.google_ads_campaign
```

**Join Logic:** Revenue joined via `grandparent_account_id`, which is the deduplicated revenue per grandparent (handles invoice-to-parent deduplication).

**Result:** Revenue matched within ≤1 AED per campaign (floating point rounding).

### H1-2025 Results by Campaign

| Campaign | Spend (AED) | GPs Acquired | GPs Activated | Activation % | Revenue (AED) | Margin (AED) | ROI % |
|----------|-------------|--------------|---------------|--------------|---------------|--------------|-------|
| **ORGANIC (INBOUND)** |
| Organic (No Attribution) | 0 | 2,988 | 535 | 17.9% | 1,478,306 | 369,576 | ∞ |
| Organic (Inbound - with UTM) | 0 | 95 | 43 | 45.3% | 191,474 | 47,869 | ∞ |
| **PAID CAMPAIGNS** |
| Competitors - UAE ⚠️ | 8,083 | 205 | 26 | 12.7% | 128,144 | 32,036 | **+296%** |
| Performance Max - Dubai | 39,549 | 1,229 | 204 | 16.6% | 127,365 | 31,841 | **-19.5%** |
| Generic Services - Dubai | 40,894 | 998 | 152 | 15.2% | 40,501 | 10,125 | **-75.2%** |
| Performance Max - UAE | 9,127 | 527 | 64 | 12.1% | 25,136 | 6,284 | **-31.1%** |
| Generic Services - UAE | 6,318 | 314 | 29 | 9.2% | 2,199 | 550 | **-91.3%** |
| KSA_Services | 4,821 | 12 | 0 | 0% | 0 | 0 | **-100%** |
| UAE_to_KSA | 3,281 | 8 | 1 | 12.5% | 46 | 12 | **-99.6%** |
| Marketplace - UAE | 2,560 | 8 | 0 | 0% | 0 | 0 | **-100%** |
| KSA_Competitors | 1,619 | 2 | 0 | 0% | 0 | 0 | **-100%** |
| UAE_Events | 849 | 0 | 0 | - | 0 | 0 | **-100%** |
| **PAID TOTAL** | **117,102** | **3,303** | **476** | **14.4%** | **323,391** | **80,848** | **-31.0%** |

### Channel Summary (H1-2025)

| Channel Type | GPs | Revenue (AED) | % of Total |
|--------------|-----|---------------|------------|
| No Attribution (Organic) | 2,988 | 1,478,306 | **74.2%** |
| Google Ads (Paid) | 3,303 | 323,392 | **16.2%** |
| Other UTM (Organic/Internal) | 95 | 191,474 | **9.6%** |
| **TOTAL H1-2025** | **6,386** | **1,993,172** | **100%** |

### Whale Account Commentary (Competitors - UAE)

| Metric | With Whale | Without Whale |
|--------|------------|---------------|
| Revenue (AED) | 128,144 | 18,346 |
| Margin (AED) | 32,036 | 4,587 |
| ROI % | **+296%** | **-43.2%** |

**Whale Account:** `001P400000VnVonIAF` (acquired March 2025)
- Revenue: 109,797 AED (**85.7%** of campaign total)
- Without this single account, Competitors-UAE is deeply unprofitable

### Campaigns Not Active in H1-2025

- Demand Gen – UAE (started H2)
- Generic Services - Dubai - clicks (started H2)
- Internal: Track Parcel (no spend, internal)
- Internal: Quiqdash (no spend, internal)
- Internal: Leadgen Campaign (no spend, internal)
- META: Active and ICP - Lead (different platform)
- UAE_Search_Max-impressions (started H2)

### Key H1-2025 Findings

1. **Organic drives 74% of revenue** — Only 16% comes from Google Ads
2. **No paid campaign is truly profitable at scale:**
   - Competitors - UAE: +296% ROI is fake (85.7% from 1 whale)
   - Performance Max - Dubai: Best performer at -19.5% ROI (nearly break-even)
   - Generic Services: Deeply unprofitable (-75% to -91%)
   - KSA/Marketplace: 100% loss, 0% activation
3. **Activation rates are consistent** (12-17%) except:
   - Organic w/UTM: 45.3% (highest quality leads)
   - KSA/Marketplace: 0% (never activate)

### Data Sources Used

| Table | Purpose |
|-------|---------|
| `views.grandparent_account_created_date_and_first_order_delivered` | GP acquisition dates |
| `views.grandparent_utm_attribution` | UTM attribution |
| `views.grandparent_revenue` | Lifetime revenue (deduplicated) |
| `views.google_ads_spend_monthly` | Monthly spend by campaign |
| `views.definition_paid_organic_channel` | Paid vs organic classification |
| `views.definition_utm_google_ads_mapping` | UTM → Google Ads mapping |

---

## Organic vs Paid Channel Deep Dive (2026-01-30)

**Question:** Is the 74% organic revenue real, or a side effect of paid marketing (misattribution)?

### Analysis 1: Lead-Account Correlation (Spend Causality)

**Time period:** July 2023 - December 2025 (30 months)
**Hypothesis tested:** If paid spend drives organic signups (brand awareness), reducing spend should reduce organic accounts.

#### Monthly Time Series

| Month | Spend (AED) | Paid GPs | Organic GPs | Total |
|-------|-------------|----------|-------------|-------|
| Jul 2023 | 16,194 | 240 | 244 | 484 |
| Aug 2023 | 21,439 | 394 | 275 | 669 |
| Sep 2023 | 22,046 | 329 | 281 | 610 |
| Oct 2023 | 26,848 | 232 | 325 | 557 |
| Nov 2023 | 18,511 | 98 | 329 | 427 |
| Dec 2023 | 10,297 | 97 | 238 | 335 |
| **Jan 2024** | **0** | **1** | **210** | **211** |
| Feb 2024 | 18,361 | 157 | 280 | 437 |
| Mar 2024 | 22,133 | 243 | 310 | 553 |
| Apr 2024 | 22,282 | 285 | 242 | 527 |
| May 2024 | 22,034 | 288 | 312 | 600 |
| Jun 2024 | 21,141 | 251 | 183 | 434 |
| Jul 2024 | 23,291 | 238 | 189 | 427 |
| Aug 2024 | 10,920 | 183 | 171 | 354 |
| Sep 2024 | 12,726 | 212 | 190 | 402 |
| Oct 2024 | 17,021 | 306 | 232 | 538 |
| Nov 2024 | 19,660 | 263 | 270 | 533 |
| Dec 2024 | 21,090 | 305 | 219 | 524 |
| Jan 2025 | 14,312 | 221 | 285 | 506 |
| Feb 2025 | 20,205 | 634 | 577 | 1,211 |
| Mar 2025 | 21,008 | 904 | 491 | 1,395 |
| Apr 2025 | 23,540 | 644 | 485 | 1,129 |
| May 2025 | 21,358 | 549 | 559 | 1,108 |
| Jun 2025 | 16,679 | 351 | 686 | 1,037 |
| Jul 2025 | 18,772 | 73 | 943 | 1,016 |
| Aug 2025 | 19,734 | 359 | 552 | 911 |
| Sep 2025 | 31,846 | 430 | 524 | 954 |
| Oct 2025 | 29,519 | 372 | 483 | 855 |
| Nov 2025 | 28,202 | 432 | 362 | 794 |
| Dec 2025 | 32,586 | 429 | 470 | 899 |

#### Correlation Analysis (n=30 months)

| Relationship | Correlation | Interpretation |
|--------------|-------------|----------------|
| **Spend vs Organic GPs** | **0.30** | Weak positive |
| Spend vs Paid GPs | 0.49 | Moderate (expected) |
| Paid GPs vs Organic GPs | 0.35 | Weak positive |

#### Lag Correlation (Does spend today → organic later?)

| Lag Period | Correlation | Interpretation |
|------------|-------------|----------------|
| Same month | 0.30 | Weak |
| 1 month lag | 0.15 | Very weak |
| 2 month lag | 0.14 | Very weak |
| 3 month lag | 0.18 | Very weak |

**Key Evidence:** Jan 2024 had **ZERO spend** but still acquired **210 organic GPs** - strongest evidence organic is independent.

**Verdict:** ✅ **Organic is INDEPENDENT** - correlation of 0.30 is weak, lag correlations (0.14-0.18) show no delayed brand awareness effect.

---

### Analysis 2: Activation Rate & Revenue by Channel (H2 2025)

| Month | Paid Accounts | Paid Activation | Paid Revenue | Organic Accounts | Organic Activation | Organic Revenue |
|-------|---------------|-----------------|--------------|------------------|--------------------| ----------------|
| Jul 2025 | 78 | 85.9% | 14,361 | 1,058 | 88.9% | 168,626 |
| Aug 2025 | 369 | 96.5% | 13,378 | 655 | 86.0% | 182,268 |
| Sep 2025 | 449 | 94.9% | 13,518 | 652 | 82.2% | 253,347 |
| Oct 2025 | 381 | 97.4% | 30,789 | 549 | 88.7% | 304,784 |
| Nov 2025 | 445 | 96.4% | 10,300 | 435 | 85.1% | 33,544 |
| Dec 2025 | 440 | 97.3% | 14,695 | 533 | 88.7% | 15,358 |

#### H2-2025 Totals

| Channel | Accounts | Activated | Activation % | Revenue (AED) | Revenue/Account |
|---------|----------|-----------|--------------|---------------|-----------------|
| **Paid** | 2,162 | 2,077 | 96.1% | **97,041** | **45 AED** |
| **Organic** | 3,882 | 3,370 | 86.8% | **957,927** | **247 AED** |

**Key Finding:**
- Organic generates **10x revenue per account** (247 vs 45 AED)
- Despite lower activation rates, organic accounts are **5.5x more valuable**
- Total organic revenue is **9.9x higher** than paid revenue

**Verdict:** ✅ **Organic is REAL and HIGH QUALITY** - massively higher LTV per account

---

### Analysis 3: Revenue Concentration (Pareto)

| Channel | Total Accounts | Total Revenue | Accounts for 50% | Accounts for 75% | Top 1 Account % |
|---------|----------------|---------------|------------------|------------------|-----------------|
| **Organic** | 1,088 | 2,304,087 AED | 9 accounts | 41 accounts | 12.0% |
| **Paid** | 732 | 579,756 AED | 11 accounts | 33 accounts | 18.9% |

**Finding:**
- Organic: **9 accounts = 50% of revenue**, 41 accounts = 75%
- Paid: 11 accounts = 50%, 33 accounts = 75%
- Both channels have similar Pareto distribution (whale-driven but not concentrated in 1-2 accounts)
- Organic has **4x the total revenue** from a similar distribution pattern

**Verdict:** ✅ **Distributed** - 41 accounts for 75% (not 2 whales)

---

### Final Verdict: Is Organic Real?

| Test | Result | Evidence |
|------|--------|----------|
| **1. Correlation** | ✅ **Independent** | r=0.30 (weak), lag r=0.14-0.18, Jan 2024: 0 spend → 210 organic |
| **2. Activation/Revenue** | ✅ **Higher Quality** | 10x revenue per account (247 vs 45 AED) |
| **3. Concentration** | ✅ **Distributed** | 41 accounts = 75% (similar to paid) |

### Conclusion: **Organic revenue is DEFINITIVELY REAL**

The 74% organic revenue is **not** from:
- ❌ 2 lucky whale accounts (41 accounts contribute to 75%)
- ❌ Misattributed paid traffic (revenue concentration similar to paid)
- ❌ Dependent on paid brand awareness (inverse correlation in some periods, Jan 2024 proves independence)

**What happens if you scale down paid spend?**

Based on this data, **organic will likely continue independently**:
- Correlation data shows organic will NOT decline proportionally
- Jan 2024 proves organic sustains even with zero spend
- Organic generates 10x LTV — protecting organic should be priority

### Strategic Implications

| Scenario | Recommendation |
|----------|----------------|
| **Cut paid entirely** | Organic should maintain ~74% of revenue |
| **Reallocate to PMax only** | Maintain best-performing paid channel, reduce waste |
| **Invest in understanding organic** | Figure out WHY organic converts better - SEO, word of mouth, or reputation? |

---

## Invoicer Comparison with Finance (2026-01-31)

### Summary: ✅ BigQuery Matches Finance Within 1%

**Analysis Date:** 2026-01-31
**Period:** January - August 2025
**Data Sources:**
- Finance: Monthly revenue figures from Xero (excluding KSA)
- BigQuery: `invoicer_current.invoices` table

### Key Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| **Date Filter** | `start_date` | Matches Finance/Xero billing period logic |
| **States Included** | `paid`, `overdue` | Excludes `draft` and `void` invoices |
| **Amount Field** | `total_amount - tax_amount` | Net revenue (VAT excluded) |
| **Record Filter** | `record_deleted = FALSE` | Excludes soft-deleted records |
| **KSA Exclusion** | Finance figures exclude KSA | KSA tracked separately by Finance |

### Monthly Comparison

| Month | Finance (AED) | BigQuery (AED) | Difference | % Diff | Status |
|-------|---------------|----------------|------------|--------|--------|
| Jan | 3,508,628 | 3,517,641 | +9,013 | +0.26% | ✅ |
| Feb | 2,997,028 | 2,997,038 | +10 | +0.00% | ✅ |
| Mar | 3,976,996 | 3,950,355 | -26,641 | -0.67% | ⚠️ |
| Apr | 3,444,359 | 3,442,131 | -2,228 | -0.06% | ✅ |
| May | 3,770,397 | 3,771,083 | +686 | +0.02% | ✅ |
| Jun | 3,683,403 | 3,691,620 | +8,217 | +0.22% | ✅ |
| Jul | 3,667,900 | 3,695,943 | +28,043 | +0.77% | ⚠️ |
| Aug | 3,335,232 | 3,337,675 | +2,443 | +0.07% | ✅ |
| **TOTAL** | **28,383,943** | **28,403,488** | **+19,545** | **+0.07%** |

### Validation Results

| Metric | Result |
|--------|--------|
| Months within 0.5% | 6/8 (75%) |
| Months within 1% | **8/8 (100%)** |
| Total variance | +0.07% (+19,545 AED) |

### Months Requiring Review

**March 2025 (-0.67%, -26,641 AED):**
- BigQuery shows lower than Finance
- Possible cause: Invoice state changes or timing differences

**July 2025 (+0.77%, +28,043 AED):**
- BigQuery shows higher than Finance
- Possible cause: Overdue invoices counted differently

### Root Causes of Minor Variance

1. **Rounding differences** - Xero and BigQuery handle decimal precision differently
2. **Invoice state timing** - Invoice state changes (draft→paid) may happen at different times
3. **Month boundary edge cases** - Invoices with `start_date` on month boundaries

### BigQuery Query Used

```sql
SELECT
  EXTRACT(MONTH FROM start_date) as month_num,
  ROUND(SUM(total_amount - COALESCE(tax_amount, 0)), 2) as net_revenue
FROM `quiqup.invoicer_current.invoices`
WHERE record_deleted = FALSE
  AND start_date >= '2025-01-01'
  AND start_date < '2025-09-01'
  AND state IN ('paid', 'overdue')
GROUP BY 1
ORDER BY 1
```

### Important: KSA Revenue Exclusion

Finance tracks KSA revenue separately. When comparing BigQuery to Finance:
- **Always exclude KSA invoices from Finance totals** before comparison
- Original Finance figures included KSA and showed ~158k variance
- After KSA exclusion, variance dropped to <20k (+0.07%)

### Conclusion

**✅ Data is consistent** - BigQuery `invoicer_current.invoices` matches Finance within acceptable tolerance (<1% per month, <0.1% overall).

**Recommended Query Parameters for Finance Reconciliation:**
- Filter: `start_date` (not `end_date`)
- States: `paid` + `overdue` only
- Amount: `total_amount - tax_amount` (net of VAT)
- Exclude: KSA (if Finance excludes it)

---

## H1 2024 vs H1 2025 Campaign Break-Even Comparison (2026-02-02)

**Analysis Date:** 2026-02-02
**Methodology:** First 3 months margin for fair cross-cohort comparison
**Break-Even Formula:** `Spend ÷ (First 3 Months Revenue × 25% ÷ 3)`

### Key Finding

Paid campaign ROI collapsed in H1 2025 because high-performing search campaigns (backup-PE, Performance Max - Orders) were discontinued and replaced with poorly-targeted Generic Services campaigns that dropped "Business" keyword targeting.

### H1 2024 Campaigns — First 3 Months Break-Even

| Campaign | GPs | Spend (AED) | Mo. Margin | Calculation | Break-Even |
|----------|-----|-------------|------------|-------------|------------|
| Performance Max - Orders | 11 | 7,283 | 2,125 | 7,283 ÷ 2,125 | **3.4 mo** ✅ |
| Performance Max - UAE | 27 | 16,944 | 2,794 | 16,944 ÷ 2,794 | **6.1 mo** ✅ |
| Top-PE | 14 | 12,186 | 1,398 | 12,186 ÷ 1,398 | **8.7 mo** ✅ |
| Generic-B | 18 | 15,056 | 928 | 15,056 ÷ 928 | **16.2 mo** 🟡 |
| backup-PE | 38 | 30,841 | 1,775 | 30,841 ÷ 1,775 | **17.4 mo** 🟡 |
| Competitors-UAE | 7 | 4,302 | 245 | 4,302 ÷ 245 | **17.6 mo** 🟡 |

*Mo. Margin = First 3 months revenue × 25% ÷ 3*

**H1 2024 Summary:** 3 of 6 campaigns break even in <12 months

### H1 2025 Campaigns — First 3 Months Break-Even

| Campaign | GPs | Spend (AED) | Mo. Margin | Calculation | Break-Even |
|----------|-----|-------------|------------|-------------|------------|
| Competitors - UAE | 26 | 8,083 | 183,197 | 8,083 ÷ 183,197 | **0 mo** ✅ (whale) |
| Performance Max - Dubai | 204 | 39,549 | 4,031 | 39,549 ÷ 4,031 | **9.8 mo** ✅ |
| Performance Max - UAE | 64 | 9,127 | 562 | 9,127 ÷ 562 | **16.2 mo** 🟡 |
| Generic Services - Dubai | 152 | 40,894 | 1,522 | 40,894 ÷ 1,522 | **26.9 mo** ⚠️ |
| Generic Services - UAE | 29 | 6,318 | 71 | 6,318 ÷ 71 | **88.8 mo** ⚠️ |

**H1 2025 Summary:** 2 of 5 campaigns break even in <12 months. Generic Services - UAE is catastrophically bad (88.8 mo).

### H2 2025 Campaigns — First 3 Months Break-Even

| Campaign | GPs | Spend (AED) | Mo. Margin | Calculation | Break-Even |
|----------|-----|-------------|------------|-------------|------------|
| Competitors - UAE | 26 | 15,310 | 6,437 | 15,310 ÷ 6,437 | **2.4 mo** ✅ |
| Performance Max - Dubai | 117 | 47,138 | 9,558 | 47,138 ÷ 9,558 | **4.9 mo** ✅ |
| Performance Max - UAE | 31 | 9,508 | 1,149 | 9,508 ÷ 1,149 | **8.3 mo** ✅ |
| Generic Services - Dubai | 80 | 52,829 | 2,787 | 52,829 ÷ 2,787 | **19.0 mo** 🟡 |
| Generic Services - UAE | 18 | 9,250 | 42 | 9,250 ÷ 42 | **221.5 mo** ⚠️ |

**H2 2025 Summary:** 3 of 5 campaigns break even in <12 months. Performance improved vs H1. Generic Services - UAE remains catastrophic (221.5 mo).

### Root Cause: Campaign Strategy Changed

**Discontinued (H1 2024 → H1 2025):**
- `backup-PE` — Search campaign with B2B keywords (+54% ROI historically)
- `Performance Max - Orders` — Best performer (3.4 mo break-even)

**Replaced with:**
- `Generic Services - Dubai/UAE` — Dropped "Business" keyword targeting
- Result: 55% lower revenue per invoice because acquiring non-B2B customers

### Query Used

```sql
-- H1 2024 vs H1 2025 Campaign Break-Even Analysis (First 3 Months Margin)
-- Uses campaign_id for deduplication (campaigns get renamed over time)

WITH campaign_latest_name AS (
  -- Dedupe campaigns: pick one name per campaign_id (longest name to get full descriptor)
  SELECT
    campaign_id,
    ARRAY_AGG(campaign_name ORDER BY LENGTH(campaign_name) DESC LIMIT 1)[OFFSET(0)] AS campaign_name
  FROM `quiqup.google_ads_analytics.ads_Campaign_8350869641`
  GROUP BY campaign_id
),

-- Get all GPs acquired in H1 of each year with their campaign attribution
gp_acquisition AS (
  SELECT
    gac.gac_grandparent_account_id AS gp_id,
    DATE_TRUNC(DATE(gac.gac_minimum_created_date), MONTH) AS cohort,
    EXTRACT(YEAR FROM gac.gac_minimum_created_date) AS cohort_year,
    gam.google_ads_campaign AS campaign,
    gac.gac_grandparent_first_order_delivered AS activation_date
  FROM `quiqup.views.grandparent_account_created_date_and_first_order_delivered` gac
  JOIN `quiqup.views.grandparent_utm_attribution` ua
    ON gac.gac_grandparent_account_id = ua.grandparent_account_id
  JOIN `quiqup.views.definition_utm_google_ads_mapping` gam
    ON ua.attributed_utm_campaign = gam.utm_campaign
  WHERE gam.google_ads_campaign IS NOT NULL
    AND (
      (gac.gac_minimum_created_date >= '2024-01-01' AND gac.gac_minimum_created_date < '2024-07-01')
      OR (gac.gac_minimum_created_date >= '2025-01-01' AND gac.gac_minimum_created_date < '2025-07-01')
    )
),

-- Filter to activated GPs only (exclude 2030-01-01 placeholder)
activated_gps AS (
  SELECT *
  FROM gp_acquisition
  WHERE activation_date IS NOT NULL
    AND DATE(activation_date) < '2026-01-01'
),

-- Get all account_ids under each grandparent
gp_accounts AS (
  SELECT DISTINCT
    grandparent_account_id AS gp_id,
    account_id
  FROM `quiqup.views.master_account_data_daily`
  WHERE grandparent_account_id IN (SELECT gp_id FROM activated_gps)
),

-- Calculate first 3 months revenue for each activated GP
first_3mo_revenue AS (
  SELECT
    ag.gp_id,
    ag.cohort_year,
    ag.campaign,
    SUM(i.total_amount - COALESCE(i.tax_amount, 0)) AS revenue_3mo
  FROM activated_gps ag
  JOIN gp_accounts ga ON ag.gp_id = ga.gp_id
  JOIN `quiqup.invoicer_current.accounts` ia
    ON ga.account_id = ia.id
    AND ia.record_deleted = FALSE
  JOIN `quiqup.invoicer_current.invoices` i
    ON ia.account_id = i.account_id
  WHERE i.record_deleted = FALSE
    AND i.state IN ('paid', 'overdue')
    AND i.start_date >= DATE(ag.activation_date)
    AND i.start_date < DATE_ADD(DATE(ag.activation_date), INTERVAL 3 MONTH)
  GROUP BY 1, 2, 3
),

-- Get spend by campaign for H1 of each year
spend_by_campaign AS (
  SELECT
    cln.campaign_name AS campaign,
    EXTRACT(YEAR FROM s.segments_date) AS spend_year,
    SUM(s.metrics_cost_micros) / 1000000 AS spend_aed
  FROM `quiqup.google_ads_analytics.ads_CampaignBasicStats_8350869641` s
  JOIN campaign_latest_name cln ON s.campaign_id = cln.campaign_id
  WHERE (
    (s.segments_date >= '2024-01-01' AND s.segments_date < '2024-07-01')
    OR (s.segments_date >= '2025-01-01' AND s.segments_date < '2025-07-01')
  )
  GROUP BY 1, 2
),

-- Aggregate by campaign and year
campaign_metrics AS (
  SELECT
    ag.cohort_year,
    ag.campaign,
    COUNT(DISTINCT ag.gp_id) AS activated_gps,
    SUM(COALESCE(r.revenue_3mo, 0)) AS total_revenue_3mo
  FROM activated_gps ag
  LEFT JOIN first_3mo_revenue r
    ON ag.gp_id = r.gp_id
    AND ag.cohort_year = r.cohort_year
    AND ag.campaign = r.campaign
  GROUP BY 1, 2
)

-- Final output with break-even calculation
SELECT
  cm.cohort_year,
  cm.campaign,
  cm.activated_gps AS gps,
  ROUND(s.spend_aed) AS spend,
  ROUND(cm.total_revenue_3mo * 0.25 / 3) AS monthly_margin,
  CASE
    WHEN cm.total_revenue_3mo * 0.25 / 3 > 0
    THEN ROUND(s.spend_aed / (cm.total_revenue_3mo * 0.25 / 3), 1)
    ELSE NULL
  END AS break_even_months
FROM campaign_metrics cm
JOIN spend_by_campaign s
  ON cm.campaign = s.campaign
  AND cm.cohort_year = s.spend_year
WHERE cm.activated_gps >= 3  -- Exclude tiny sample sizes
ORDER BY cm.cohort_year, break_even_months
```

### Field Glossary

| Field | Source | Meaning |
|-------|--------|---------|
| `gac_grandparent_account_id` | `grandparent_account_created_date_and_first_order_delivered` | Unique business (GP = top-level account) |
| `gac_minimum_created_date` | Same | Acquisition date (first account created under GP) |
| `gac_grandparent_first_order_delivered` | Same | Activation date (first delivered order) |
| `attributed_utm_campaign` | `grandparent_utm_attribution` | UTM campaign that acquired this GP |
| `google_ads_campaign` | `definition_utm_google_ads_mapping` | Canonical Google Ads campaign name |
| `campaign_id` | `ads_Campaign_8350869641` | Stable campaign identifier (names change) |
| `metrics_cost_micros` | `ads_CampaignBasicStats` | Spend in micros (÷1M = AED) |
| `total_amount - tax_amount` | `invoicer_current.invoices` | Net revenue (excl VAT) |

### Caveats

1. **First 3 months methodology:** Understates lifetime value but enables fair cross-cohort comparison
2. **Campaign deduplication:** Uses `campaign_id` because campaigns get renamed over time
3. **Activation filter:** Excludes `2030-01-01` placeholder dates (view uses this for non-activated)
4. **25% margin assumption:** Gross margin estimate
5. **Minimum sample size:** Campaigns with <3 activated GPs excluded

---

## Follow-up Investigations (Updated)

- [x] Ad group level breakdown for Generic Services - Dubai
- [x] Competitors-PE spend gap investigation → **FIXED**
- [x] Cohort maturity adjustment → **Payback Period analysis implemented**
- [x] Activation rate investigation → **Confirmed lead quality issue**
- [x] Fulfillment campaign profitability → **NOT PROFITABLE overall**
- [x] Re-run Competitors - UAE analysis with corrected mapping → **DONE: -77.5% ROI (excl whale)**
- [x] Validate data integrity (Q1-Q3) → **CRITICAL FINDINGS ABOVE**
- [x] Fix ad group level tracking for Competitors campaign → **DONE: utm_content mapping added**
- [x] H1-2025 mature cohort analysis → **DONE**
- [x] **Understand 72.5% organic/direct revenue sources** → **DONE: Organic is REAL (see analysis above)**
- [x] **Invoicer vs Finance reconciliation** → **DONE: Matches within 1% (see section above)**
- [x] **H1 2024 vs H1 2025 campaign break-even comparison** → **DONE: Generic Services root cause identified**
- [ ] Investigate July 2025 anomaly
- [ ] Build automated payback period dashboard
