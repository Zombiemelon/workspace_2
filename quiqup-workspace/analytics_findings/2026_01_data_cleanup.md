# Campaign Performance Analysis - Data Cleanup

**Date:** 2026-01-29
**Analyst:** Claude (BigQuery Analyst Agent)
**Status:** Complete

---

## Executive Summary

Analysis of Google Ads campaign performance with full-funnel attribution from spend through leads, accounts, and orders. Key finding: **Parcel Delivery campaign (paused Apr 2025) was the best performer** — campaigns currently receiving spend show weak or zero conversions.

---

## Summary Table

| Category | Spend (AED) | Leads | Converted | Accounts | 1+ Orders | 10+ Orders | Last Active | UTMs |
|----------|------------:|------:|----------:|---------:|----------:|-----------:|-------------|------|
| Generic - Parcel Delivery | 28,155 | 346 | 18 | 449 | 64 | 21 | **Apr 2025** | `Generic-Services_Parcel-Delivery` |
| KSA Services | 15,923 | 95 | 8 | 29 | 0 | 0 | Nov 2025 | `KSA-Fulfillment-AR`, `KSA-Fulfillment-EN`, `KSA-Services-AR`, `KSA-Services-EN` |
| Marketplace - UAE | 13,220 | 38 | 0 | 15 | 0 | 0 | Jan 2026 | `Marketplace-UAE`, `UAE_Marketplace` |
| Demandgen - UAE | 5,674 | 7 | 0 | 4 | 0 | 0 | Dec 2025 | `Demandgen-UAE` |
| Generic - Fulfillment (UAE) | 4,836 | 61 | 12 | 59 | 4 | 3 | Jan 2026 | `Generic-Services_Fulfillment` |
| Generic - Ecommerce | 1,675 | 20 | 3 | 22 | 2 | 1 | Jan 2026 | `Generic-Services_Ecommerce` |

---

## Key Insights

### High Performers (Paused)
- **Generic - Parcel Delivery** (paused Apr 2025)
  - Lead → Conversion rate: 5.2% (18/346)
  - Account activation rate: 14% (64/449 placed 1+ orders)
  - Retention signal: 33% of active accounts reached 10+ orders
  - **Recommendation:** Investigate why this was paused; consider reactivation

### Active but Underperforming
- **Marketplace - UAE** (active, Jan 2026)
  - 0% lead conversion despite 38 leads and AED 13,220 spend
  - 15 accounts created but 0 orders placed
  - **Recommendation:** Review targeting, landing pages, and lead quality

- **Demandgen - UAE** (active until Dec 2025)
  - Only 7 leads from AED 5,674 spend (AED 810/lead)
  - 0 conversions
  - **Recommendation:** Pause or significantly revise creative/targeting

### Mixed Results
- **KSA Services** (paused Nov 2025)
  - 8 converted leads but 0 orders from 29 accounts
  - Suggests onboarding friction or product-market fit issue in KSA
  - **Recommendation:** Investigate account activation blockers

- **Generic - Fulfillment (UAE)** (active)
  - Strong conversion rate: 20% (12/61 leads converted)
  - Low activation: only 4/59 accounts placed orders
  - **Recommendation:** Focus on post-signup onboarding

---

## Funnel Metrics (All Campaigns Combined)

| Stage | Count | Conversion Rate |
|-------|------:|----------------:|
| Total Leads | 567 | — |
| Leads Converted | 41 | 7.2% |
| Accounts Created | 578 | — |
| Accounts with 1+ Orders | 70 | 12.1% |
| Accounts with 10+ Orders | 25 | 35.7% of active |

---

## Data Sources & Methodology

### Tables Used
1. `quiqup.views.google_ads_spend_monthly` — Pre-aggregated campaign spend
2. `quiqup.views.definition_utm_google_ads_mapping` — UTM → Google Ads campaign mapping
3. `quiqup.salesforce_current.leads` — Lead records with `is_converted` flag
4. `quiqup.salesforce_current.accounts` — Account records with UTM attribution
5. `quiqup.views.total_order_per_client` — Order counts per account

### Attribution Logic
- Leads and accounts are attributed to campaigns via `utm_campaign_c` field
- UTM campaigns are mapped to Google Ads campaigns/ad groups using the definition table
- Campaign categories are derived from:
  - Campaign name (Marketplace, Demand Gen, KSA_Services)
  - Ad group name (Parcel delivery, Fulfillment, Ecommerce)

### Query Used

```sql
WITH campaign_spend AS (
  SELECT
    CASE
      WHEN google_ads_campaign = 'Marketplace - UAE' THEN 'Marketplace - UAE'
      WHEN google_ads_campaign LIKE '%Demand Gen%' THEN 'Demandgen - UAE'
      WHEN google_ads_ad_group = 'Parcel delivery' THEN 'Generic - Parcel Delivery'
      WHEN google_ads_ad_group = 'Fulfillment' AND google_ads_campaign LIKE '%UAE%' THEN 'Generic - Fulfillment (UAE)'
      WHEN google_ads_ad_group = 'Ecommerce' THEN 'Generic - Ecommerce'
      WHEN google_ads_campaign = 'KSA_Services' THEN 'KSA Services'
    END AS category,
    SUM(spend_aed) AS spend_aed,
    MAX(month) AS last_active_month
  FROM `quiqup.views.google_ads_spend_monthly`
  WHERE
    google_ads_campaign = 'Marketplace - UAE'
    OR google_ads_campaign LIKE '%Demand Gen%'
    OR (google_ads_ad_group IN ('Parcel delivery', 'Fulfillment', 'Ecommerce') AND google_ads_campaign LIKE '%UAE%')
    OR google_ads_campaign = 'KSA_Services'
  GROUP BY category
),
utm_list AS (
  SELECT
    CASE
      WHEN google_ads_campaign = 'Marketplace - UAE' THEN 'Marketplace - UAE'
      WHEN google_ads_campaign LIKE '%Demand Gen%' THEN 'Demandgen - UAE'
      WHEN google_ads_ad_group = 'Parcel delivery' THEN 'Generic - Parcel Delivery'
      WHEN google_ads_ad_group = 'Fulfillment' AND google_ads_campaign LIKE '%UAE%' THEN 'Generic - Fulfillment (UAE)'
      WHEN google_ads_ad_group = 'Ecommerce' THEN 'Generic - Ecommerce'
      WHEN google_ads_campaign = 'KSA_Services' THEN 'KSA Services'
    END AS category,
    STRING_AGG(DISTINCT utm_campaign, ', ' ORDER BY utm_campaign) AS utms_included
  FROM `quiqup.views.definition_utm_google_ads_mapping`
  WHERE google_ads_campaign IN ('Marketplace - UAE', 'Demand Gen – UAE', 'KSA_Services')
     OR (google_ads_ad_group IN ('Parcel delivery', 'Fulfillment', 'Ecommerce') AND google_ads_campaign LIKE '%UAE%')
  GROUP BY category
),
account_orders AS (
  SELECT sf_account_id, number_of_orders
  FROM `quiqup.views.total_order_per_client`
),
account_by_campaign AS (
  SELECT
    CASE
      WHEN m.google_ads_campaign = 'Marketplace - UAE' THEN 'Marketplace - UAE'
      WHEN m.google_ads_campaign LIKE '%Demand Gen%' THEN 'Demandgen - UAE'
      WHEN m.google_ads_ad_group = 'Parcel delivery' THEN 'Generic - Parcel Delivery'
      WHEN m.google_ads_ad_group = 'Fulfillment' AND m.google_ads_campaign LIKE '%UAE%' THEN 'Generic - Fulfillment (UAE)'
      WHEN m.google_ads_ad_group = 'Ecommerce' THEN 'Generic - Ecommerce'
      WHEN m.google_ads_campaign = 'KSA_Services' THEN 'KSA Services'
    END AS category,
    a.id AS account_id,
    ao.number_of_orders
  FROM `quiqup.salesforce_current.accounts` a
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON a.utm_campaign_c = m.utm_campaign
  LEFT JOIN account_orders ao ON ao.sf_account_id = a.id
  WHERE m.google_ads_campaign IN ('Marketplace - UAE', 'Demand Gen – UAE', 'KSA_Services')
     OR (m.google_ads_ad_group IN ('Parcel delivery', 'Fulfillment', 'Ecommerce') AND m.google_ads_campaign LIKE '%UAE%')
),
leads_by_campaign AS (
  SELECT
    CASE
      WHEN m.google_ads_campaign = 'Marketplace - UAE' THEN 'Marketplace - UAE'
      WHEN m.google_ads_campaign LIKE '%Demand Gen%' THEN 'Demandgen - UAE'
      WHEN m.google_ads_ad_group = 'Parcel delivery' THEN 'Generic - Parcel Delivery'
      WHEN m.google_ads_ad_group = 'Fulfillment' AND m.google_ads_campaign LIKE '%UAE%' THEN 'Generic - Fulfillment (UAE)'
      WHEN m.google_ads_ad_group = 'Ecommerce' THEN 'Generic - Ecommerce'
      WHEN m.google_ads_campaign = 'KSA_Services' THEN 'KSA Services'
    END AS category,
    l.id AS lead_id,
    l.is_converted
  FROM `quiqup.salesforce_current.leads` l
  JOIN `quiqup.views.definition_utm_google_ads_mapping` m
    ON l.utm_campaign_c = m.utm_campaign
  WHERE m.google_ads_campaign IN ('Marketplace - UAE', 'Demand Gen – UAE', 'KSA_Services')
     OR (m.google_ads_ad_group IN ('Parcel delivery', 'Fulfillment', 'Ecommerce') AND m.google_ads_campaign LIKE '%UAE%')
)
SELECT
  cs.category,
  ROUND(cs.spend_aed, 0) AS spend_aed,
  COUNT(DISTINCT lc.lead_id) AS leads_added,
  COUNT(DISTINCT CASE WHEN lc.is_converted = TRUE THEN lc.lead_id END) AS leads_converted,
  COUNT(DISTINCT ac.account_id) AS accounts_created,
  COUNT(DISTINCT CASE WHEN ac.number_of_orders >= 1 THEN ac.account_id END) AS placed_1_plus,
  COUNT(DISTINCT CASE WHEN ac.number_of_orders >= 10 THEN ac.account_id END) AS placed_10_plus,
  cs.last_active_month,
  ul.utms_included
FROM campaign_spend cs
LEFT JOIN account_by_campaign ac ON ac.category = cs.category
LEFT JOIN leads_by_campaign lc ON lc.category = cs.category
LEFT JOIN utm_list ul ON ul.category = cs.category
GROUP BY cs.category, cs.spend_aed, cs.last_active_month, ul.utms_included
ORDER BY cs.spend_aed DESC
```

---

## Caveats & Limitations

1. **Attribution gaps:** Accounts/leads without matching UTM campaigns are not included
2. **Spend scope:** "Parcel Delivery" spend (28K) excludes Dubai campaigns (full total was 42K)
3. **Time range:** All-time totals; monthly breakdown available but not shown here
4. **Conversion definition:** `is_converted` in Salesforce = lead converted to opportunity/account

---

## Recommended Next Steps

1. **Reactivate Parcel Delivery campaign** — best historical performer
2. **Investigate Marketplace & Demandgen** — 0 conversions despite active spend
3. **KSA deep dive** — why are converted leads not placing orders?
4. **Improve attribution coverage** — ensure all campaigns have proper UTM mapping

---

*Generated by BigQuery Analyst Agent | quiqup-workspace*
