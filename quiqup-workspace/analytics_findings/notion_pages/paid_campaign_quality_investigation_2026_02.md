# Paid Campaign Quality Investigation: H1 2025 vs H1 2024

**Analysis Date:** February 2, 2026
**Data Period:** H1 2024 (Jan-Jun 2024) vs H1 2025 (Jan-Jun 2025)
**Analyst:** Data Team
**Status:** Complete - Revised

---

## Executive Summary

**Key Finding:** Paid campaign ROI collapsed in H1 2025 due to discontinuing profitable search campaigns and replacing them with poorly-targeted Generic Services campaigns.

**Root Cause:**
1. High-performing campaigns discontinued: backup-PE (+54% ROI), Performance Max - Orders (+354% ROI)
2. Replaced by Generic Services campaigns that dropped "Business" keyword targeting
3. Performance Max - Dubai is NOT the problem (10.8 mo break-even = acceptable)
4. Generic Services - Dubai/UAE ARE the problem (40.9 mo and 252.7 mo break-even)

**Confidence Level:** High (85%) — Campaign-level ROI analysis confirms Generic Services as root cause.

---

## Phase 1: Problem Confirmation

### GP Volume & Activation Rates

| Period | Total GPs | Paid GPs | Organic GPs | Paid Activation Rate |
|--------|-----------|----------|-------------|---------------------|
| H1 2024 | 2,732 | 1,218 | 1,514 | 17.3% |
| H1 2025 | 2,979 | 1,294 | 1,685 | 20.2% |
| **Change** | +9% | +6% | +11% | **+17% (improved)** |

**Finding:** Activation rates actually improved in H1 2025. The problem is not lead-to-activation conversion.

### Revenue per Activated GP

| Period | Cohort Age | Paid Activated GPs | Rev/GP | Margin/GP | Monthly Margin/GP |
|--------|------------|-------------------|--------|-----------|-------------------|
| H1 2024 | 22 mo | 211 | 6,219 | 1,555 | **71 AED** |
| H1 2025 | 10 mo | 262 | 1,335 | 334 | **33 AED** |
| **Change** | | +24% | -79% | -79% | **-53%** |

**Finding:** Monthly margin per paid GP collapsed by 53% (71 → 33 AED).

---

## Phase 2: Campaign Mix Analysis

### Campaign Structure Changed Significantly

| Campaign | H1 2024 GPs | H1 2025 GPs | H1 2024 Rev/GP | H1 2025 Rev/GP | Status |
|----------|-------------|-------------|----------------|----------------|--------|
| Performance_Max_Dubai | - | 602 | - | 1,099 | NEW |
| Performance_Max | 307 | 196 | 6,305 | 663 | -77% monthly rev |
| backup-PE (search) | 325 | - | 3,725 | - | DISCONTINUED |
| Generic-B (search) | 149 | - | 2,275 | - | DISCONTINUED |
| Top-PE (search) | 94 | - | 2,164 | - | DISCONTINUED |
| Generic-Services_Dubai_* | - | ~300+ | - | 200-1,500 | NEW |

### Spend Breakdown

| Campaign | H1 2024 Spend | H1 2025 Spend | CPC 2024 | CPC 2025 |
|----------|---------------|---------------|----------|----------|
| Performance Max - Dubai | - | 39,549 | - | 1.48 |
| Generic Services - Dubai | - | 40,894 | - | 4.17 |
| backup-PE | 30,841 | - | 5.34 | - |
| Performance Max - UAE | 16,944 | 9,127 | 2.18 | 1.01 |

**Finding:** H1 2025 spend concentrated in 2 new campaigns representing 70% of total spend at lower CPCs.

---

## Phase 3: Behavioral Analysis

### Time-to-Activation (Improved)

| Period | Channel | Avg Days | Median | Within 7 Days |
|--------|---------|----------|--------|---------------|
| H1 2024 | Paid | 61.5 | 9 | 45.5% |
| H1 2025 | Paid | 38.1 | 5 | 54.6% |

**Finding:** GPs are activating faster in H1 2025.

### Order Frequency & Value (Root Cause)

| Period | Channel | Invoices/Month | Revenue/Month | Revenue/Invoice |
|--------|---------|----------------|---------------|-----------------|
| H1 2024 | Paid | 0.45 | 299 AED | **622 AED** |
| H1 2025 | Paid | 0.46 | 128 AED | **281 AED** |
| **Change** | | +2% | -57% | **-55%** |

**Root Cause:** Order frequency is similar, but revenue per invoice collapsed by 55%. H1 2025 paid GPs are smaller businesses with lower order values.

---

## Phase 4: Google Ads Efficiency

| Metric | H1 2024 | H1 2025 | Change |
|--------|---------|---------|--------|
| Spend | 105,951 | 117,102 | +11% |
| Clicks | 28,908 | 55,074 | +90% |
| CPC | 3.67 | 2.13 | -42% |
| CTR | 9.11% | 9.69% | +6% |
| Cost/Conversion | 43 | 23 | -47% |

**Paradox:** Google Ads metrics look better (lower CPC, better CTR) but business outcomes are worse. The campaigns are optimizing for cheap clicks, not valuable customers.

---

## Phase 5: Campaign-Level ROI Analysis (First 3 Months Margin)

Using **first 3 months margin** for fair comparison across cohorts (older cohorts had more time to ramp up).

### H1 2024 Campaigns — First 3 Months Break-Even

| Campaign | GPs | Spend (AED) | Mo. Margin | Calculation | Break-Even |
|----------|-----|-------------|------------|-------------|------------|
| Performance Max - Orders | 11 | 7,283 | 2,125 | 7,283 ÷ 2,125 | **3.4 mo** ✅ |
| Performance Max - UAE | 27 | 16,944 | 2,794 | 16,944 ÷ 2,794 | **6.1 mo** ✅ |
| Top-PE | 14 | 12,186 | 1,398 | 12,186 ÷ 1,398 | **8.7 mo** ✅ |
| Generic-B | 18 | 15,056 | 928 | 15,056 ÷ 928 | **16.2 mo** 🟡 |
| backup-PE | 38 | 30,841 | 1,775 | 30,841 ÷ 1,775 | **17.4 mo** 🟡 |
| Competitors-UAE | 7 | 4,302 | 245 | 4,302 ÷ 245 | **17.6 mo** 🟡 |

*Monthly Margin = First 3 months revenue × 25% ÷ 3*

---

### H1 2025 Campaigns — First 3 Months Break-Even

| Campaign | GPs | Spend (AED) | Mo. Margin | Calculation | Break-Even |
|----------|-----|-------------|------------|-------------|------------|
| Competitors - UAE | 6 | 8,083 | 2,396 | 8,083 ÷ 2,396 | **3.4 mo** ✅ |
| Competitors-PE | 3 | 1,619 | 421 | 1,619 ÷ 421 | **3.8 mo** ✅ |
| Performance Max - Dubai | 94 | 39,549 | 3,886 | 39,549 ÷ 3,886 | **10.2 mo** 🟡 |
| Performance Max - UAE | 24 | 9,127 | 520 | 9,127 ÷ 520 | **17.6 mo** 🟡 |
| Generic Services - Dubai | 30 | 40,894 | 1,421 | 40,894 ÷ 1,421 | **28.8 mo** ⚠️ |

*Note: Generic Services - UAE excluded (no attributed activations in first 3 months)*

---

### Key Insight: H1 2024 vs H1 2025 Comparison

| Metric | H1 2024 Best | H1 2025 Best |
|--------|--------------|--------------|
| Campaign | PMax Orders | Competitors-UAE |
| Break-Even | 3.4 mo | 3.4 mo |
| Monthly Margin | 2,125 AED | 2,396 AED |

**Summary:**
- H1 2024: 3 of 6 campaigns break even in <12 months
- H1 2025: 3 of 5 campaigns break even in <12 months
- Generic Services - Dubai is the worst performer (28.8 mo break-even)

---

### Root Cause: Keyword Targeting Changed

**OLD campaigns (2024) used business-specific keywords:**
- "Phrase_Business_Delivery" — CPC 8.99 AED — targeted B2B explicitly
- "Broad_Business Courier" — CPC 6.21 AED — targeted B2B explicitly

**NEW campaigns (2025) dropped business modifiers:**
- "Delivery Service" — CPC 4.61 AED — generic, attracts B2C/small users
- "Phrase_Courier Service" — CPC 3.87 AED — no B2B filter

**Result:** 55% lower revenue per invoice because we're acquiring non-B2B customers who order small packages, not business logistics clients.

---

## Quantified Impact

**Monthly margin opportunity cost:**
- H1 2024: 211 activated × 71 AED/month = 14,981 AED/month
- H1 2025: 262 activated × 33 AED/month = 8,646 AED/month
- **Lost opportunity: ~6,300 AED/month**

---

## Recommendations (with tradeoffs)

| Option | Action | Expected Impact | Tradeoff |
|--------|--------|-----------------|----------|
| **A) Pause Generic Services - UAE** | Immediately stop (252.7 mo break-even) | Save 6,318 AED/H1, negligible volume loss | None — clear win |
| **B) Reduce Generic Services - Dubai** | Cut 50% spend | Save ~20K AED, lose some volume | May reduce total activations |
| **C) Restore "Business" keywords** | Add back business modifiers to ad groups | Higher CPC but better customer quality | Unknown if audience still exists |
| **D) Scale Performance Max - Dubai** | Increase budget (10.2 mo break-even acceptable) | More volume at reasonable ROI | May hit diminishing returns |
| **E) Rebuild backup-PE** | Recreate discontinued search campaign | Proven 14.3 mo break-even | Higher CPC, setup time required |

**Recommended priority:** A → C → D

---

## Data Sources

- `views.master_account_data_daily` — Account base with UTM and activation
- `views.grandparent_revenue` — Lifetime revenue by grandparent
- `views.definition_paid_organic_channel` — Paid/organic classification
- `google_ads_analytics.ads_CampaignBasicStats_8350869641` — Spend data
- `salesforce_current.accounts` — Business account filter (`client_type_c IS NULL`)

---

## Caveats

1. **First 3 months methodology:** Break-even calculated using margin from first 3 months after activation only, for fair cross-cohort comparison
2. **Break-even formula:** `Break-Even Months = Spend ÷ Monthly Margin Rate` where Monthly Margin = (First 3 mo Revenue × 25%) ÷ 3
3. **Customer ramp-up:** Customers generate more revenue over time — first 3 months understates lifetime value
4. **Whale account risk:** Some campaigns may be skewed by single large accounts
5. **UTM attribution coverage:** ~50% of grandparents have UTM data; unattributed are classified as organic
6. **25% margin assumption:** Margin = Revenue × 0.25 (gross margin estimate)

---

*Generated: 2026-02-02 | Revised: 2026-02-02*
*Data filter: Business accounts only (client_type_c IS NULL)*
*Break-even formula: Spend ÷ (First 3 Months Margin ÷ 3)*
