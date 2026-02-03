# UAE Campaigns Consolidated Analysis – 2025

**Date:** 2026-01-29
**Region:** UAE
**Period:** 2025
**Total Spend:** AED 20,344 (~$5,540 USD)

> **Note:** BigQuery `metrics_cost_micros` stores values in account currency (AED), not USD.

---

## Executive Summary

Four UAE campaigns spent **AED 20,344** in 2025. Only one (Generic-Parcel Delivery) generated revenue, and that came almost entirely from self-signup users who bypassed the sales funnel. The sales-assisted path is fundamentally broken across all campaigns.

| Campaign | Spend (AED) | Clicks | Leads | Orders | Revenue |
|----------|-------------|--------|-------|--------|---------|
| Marketplace-UAE | 11,508 | 1,852 | 31 | 0 | AED 0 |
| Demand Gen – UAE | 5,674 | 8,332 | 7 | 0 | AED 0 |
| Generic-Parcel Delivery | 1,927 | 785 | 128 | 734 | **Revenue** |
| Generic-Fulfillment UAE | 1,235 | 188 | 13 | 0 | AED 0 |
| **Total** | **20,344** | **11,157** | **179** | **734** | - |

**Key Finding:** 97.7% of orders came from SSUP self-signup users on a single campaign (Generic-Parcel). The sales funnel contributed zero revenue across all four campaigns.

---

## Campaign Performance Comparison

### Funnel Efficiency

| Campaign | Clicks | Click→Lead % | Leads Disqualified | Activation Rate | Orders |
|----------|--------|--------------|--------------------|-----------------|---------|
| Generic-Parcel Delivery | 785 | **16.3%** | 97.7% | 8.9% | **734** |
| Marketplace-UAE | 1,852 | 1.62% | 100% | 0% | 0 |
| Generic-Fulfillment UAE | 188 | 6.9% | 85% | 0% | 0 |
| Demand Gen – UAE | 8,332 | **0.08%** | 100% | 0% | 0 |

### Cost Efficiency

| Campaign | CPC (AED) | Cost/Lead (AED) | Cost/Order (AED) | Assessment |
|----------|-----------|-----------------|------------------|------------|
| Generic-Parcel Delivery | 2.46 | 15.05 | **2.62** | Excellent |
| Marketplace-UAE | 6.21 | 371 | ∞ | Poor |
| Generic-Fulfillment UAE | 6.57 | 95 | ∞ | Poor |
| Demand Gen – UAE | 0.68 | 810 | ∞ | Unacceptable |

---

## Root Causes Identified

### 1. Sales-Assisted Path is Broken (All Campaigns)

| Campaign | Leads Converted by Sales | Orders from Sales Path |
|----------|--------------------------|------------------------|
| Marketplace-UAE | 0 | 0 |
| Demand Gen – UAE | 0 | 0 |
| Generic-Fulfillment UAE | 1 | 0 (Deal Lost) |
| Generic-Parcel Delivery | 3 | **0** |
| **Total** | **4** | **0** |

**Finding:** Across all campaigns, the sales team converted only 4 leads total. None generated orders. The only revenue (734 orders) came from users who bypassed sales entirely via SSUP.

---

### 2. Massive Lead Disqualification

| Disqualification Reason | Count | % | Campaigns Affected |
|------------------------|-------|---|-------------------|
| Moved to SSUP | 50+ | ~30% | All |
| Service Not Within Offering | 17 | ~10% | Marketplace, Fulfillment |
| One-time delivery seekers | 18 | ~10% | Parcel Delivery |
| Unqualified (no reason) | 8 | ~5% | Fulfillment, Marketplace |
| Food delivery (not supported) | 10 | ~6% | Marketplace, Parcel |
| Outside service area | 7 | ~4% | Parcel Delivery |

**Key Insight:** ~30% of all leads across campaigns were redirected to SSUP. These aren't bad leads—they just don't need sales assistance.

---

### 3. SSUP Self-Signup Accounts Don't Activate (3 of 4 Campaigns)

| Campaign | SSUP Accounts | Activated | Activation Rate |
|----------|---------------|-----------|-----------------|
| Generic-Parcel Delivery | 99 | 15 | **15.2%** |
| Marketplace-UAE | 7 | 0 | 0% |
| Demand Gen – UAE | 4 | 0 | 0% |
| Generic-Fulfillment UAE | 14 | 0 | 0% |

**Finding:** Generic-Parcel is the only campaign where SSUP accounts actually activate. Other campaigns have a 0% activation rate, suggesting product-market fit issues or onboarding barriers specific to those verticals.

---

### 4. Wrong Campaign Type (Demand Gen)

| Campaign Type | Typical Intent | Click→Lead % | Best For |
|---------------|----------------|--------------|----------|
| Search | High (active research) | 2-5% | Lead generation |
| Demand Gen | Low (passive discovery) | **0.08%** | Brand awareness |

**Finding:** Demand Gen campaigns serve ads on YouTube, Gmail, and Discover. This audience is in "browsing mode," not "buying mode." The 0.08% conversion rate confirms this campaign type is unsuitable for B2B lead gen.

---

### 5. Conversion Tracking Issues (Marketplace)

| Metric | 2025 Count |
|--------|------------|
| Google Ads "Conversions" | 198 |
| GA4 Form Submitters | 125 |
| Salesforce Leads | 31 |

**Finding:** Google Ads reports 198 conversions but only 31 leads exist in Salesforce. The conversion action is likely tracking page views or button clicks, not actual form submissions. Additionally, 76% of GA4 form submissions never created Salesforce leads.

---

## Campaign-Specific Details

### 1. Generic-Parcel Delivery (Best Performer)

**Status:** Paused (Jan-Apr 2025)
**Spend:** AED 1,927
**Orders:** 734 (97.7% from SSUP)

| Path | Accounts | Activated | Orders | % of Total |
|------|----------|-----------|--------|------------|
| SSUP | 99 | 15 | 717 | **97.7%** |
| Individual | 239 | 15 | 17 | 2.3% |
| Sales-Assisted | 3 | 0 | 0 | 0% |

**Recommendation:** Reactivate with direct-to-SSUP routing. Bypass sales funnel entirely.

---

### 2. Marketplace-UAE (Highest Spend, Zero Revenue)

**Status:** Active
**Spend:** AED 11,508
**Orders:** 0

**Issues:**
- 100% lead disqualification rate
- 76% form submissions lost between GA4 and Salesforce
- Wrong audience targeting (amazon sellers, dropshippers)
- Broken conversion tracking

**Recommendation:** Pause until conversion tracking is fixed. Re-evaluate ICP for marketplace vertical.

---

### 3. Demand Gen – UAE (Wrong Channel)

**Status:** Paused (Oct-Dec 2025 only)
**Spend:** AED 5,674
**Orders:** 0

**Issues:**
- Display/YouTube campaign type attracts low-intent traffic
- 8,332 clicks but only 7 leads (0.08% conversion)
- All 7 leads disqualified

**Recommendation:** Keep paused. Demand Gen is unsuitable for B2B lead generation.

---

### 4. Generic-Fulfillment UAE (Underfunded, Underperforming)

**Status:** Active
**Spend:** AED 1,235
**Orders:** 0

**Comparison to Dubai:**
| Metric | UAE | Dubai |
|--------|-----|-------|
| Accounts | 14 | 70 |
| Activated | 0 | 11 |
| Orders | 0 | 162 |
| Activation Rate | **0%** | **16%** |

**Recommendation:** Consider pausing or merging. Investigate why Dubai performs and UAE doesn't.

---

## Consolidated Recommendations

### Immediate Actions

| Priority | Action | Campaigns Affected |
|----------|--------|-------------------|
| 1 | **Keep Demand Gen paused** - Channel unsuitable for B2B | Demand Gen |
| 2 | **Pause Marketplace-UAE** - Fix conversion tracking first | Marketplace |
| 3 | **Reactivate Generic-Parcel with SSUP routing** - Best ROI | Parcel Delivery |
| 4 | **Audit GA4→Salesforce pipeline** - 76% submissions lost | Marketplace |

### Strategic Actions

| Priority | Action | Impact |
|----------|--------|--------|
| 5 | **Bypass sales funnel for self-service fits** - 30% of leads redirected anyway | All |
| 6 | **Investigate SSUP onboarding barriers** - 0% activation on 3 campaigns | All except Parcel |
| 7 | **Add negative keywords** - Food delivery, one-time delivery | All |
| 8 | **Replicate Dubai Fulfillment playbook** - 16% activation vs 0% UAE | Fulfillment |

### Process Improvements

| Priority | Action |
|----------|--------|
| 9 | **Document all disqualification reasons** - 31% of Fulfillment leads have no reason |
| 10 | **Set minimum conversion rate thresholds** before scaling spend |
| 11 | **Implement weekly performance reviews** for new campaign types |
| 12 | **Speed up lead follow-up** - Only converted opp was lost due to "no response" |

---

## UTM Tracking Reference

| Campaign | UTM |
|----------|-----|
| Marketplace-UAE | `Marketplace-UAE` |
| Demand Gen – UAE | `Demandgen-UAE` |
| Generic-Parcel Delivery | `Generic-Services_Parcel-Delivery` |
| Generic-Fulfillment UAE | `Generic-Services_Fulfillment` |

**Note:** Generic-Fulfillment UAE UTM lacks location identifier (Dubai uses `Generic-Services_Dubai_Fulfillment`).

---

## Data Sources

- `quiqup.google_ads_analytics.ads_CampaignBasicStats_8350869641`
- `quiqup.google_ads_analytics.ads_AdGroupStats_8350869641`
- `quiqup.views.ga4_contact_form_submits`
- `quiqup.salesforce_current.leads`
- `quiqup.salesforce_current.opportunities`
- `quiqup.salesforce_current.accounts`
- `quiqup.views.master_account_data_daily`

---

## Key Takeaways

1. **Sales funnel is broken** - Zero revenue from sales-assisted path across all campaigns
2. **SSUP is the revenue driver** - 97.7% of orders came from self-signup users
3. **Demand Gen is wrong channel** - 0.08% conversion rate; keep paused
4. **Generic-Parcel should be reactivated** - AED 2.62 per order is excellent ROI
5. **Fix tracking before spending more** - Marketplace has 76% data leakage

---

*Analysis consolidated: 2026-01-29*
