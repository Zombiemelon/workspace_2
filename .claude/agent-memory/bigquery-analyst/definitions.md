# Business Definitions

Every definition below maps to a **specific view or table** in BigQuery. Never hardcode classification logic in ad-hoc queries — always JOIN to the definition view so changes propagate automatically.

## Channel Classification

### Paid vs Organic

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_paid_organic_channel` |
| **Grain** | 1 row per UTM source+medium combination |
| **Rule** | What is NOT explicitly PAID = Organic (including NULL/missing UTM) |
| **Key columns** | `utm_source`, `utm_medium`, `channel_type` ('Paid'/'Organic'), `is_paid` (BOOL), `channel_detail` |

**Paid channels:**
- `utm_medium IN ('cpc', 'ppc', 'paid', 'paid_social', 'display', 'banner')`
- Meta Ads: `utm_source IN ('fb', 'ig', 'facebook', 'instagram')` with paid mediums

**Organic channels:** Internal (ldr, bdm), direct, email, referral, malformed UTM, NULL/missing

**Join pattern (priority: exact > wildcard > default organic):**
```sql
LEFT JOIN views.definition_paid_organic_channel exact
  ON LOWER(t.utm_source) = LOWER(exact.utm_source)
  AND LOWER(t.utm_medium) = LOWER(exact.utm_medium)
  AND exact.utm_source != '*'
LEFT JOIN views.definition_paid_organic_channel wildcard
  ON wildcard.utm_source = '*'
  AND LOWER(t.utm_medium) = LOWER(wildcard.utm_medium)
-- Result: COALESCE(exact.is_paid, wildcard.is_paid, FALSE) AS is_paid
```

**Gotcha:** GA4 traffic classification (broad: gclid/wbraid/gbraid counts as paid) differs from attribution-level classification (strict: `cpc` only). Use GA4 for traffic volume, `definition_paid_organic_channel` for ROI/attribution.

### Traffic Channel Groups

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_traffic_channel` |
| **Grain** | 1 row per source+medium |
| **Purpose** | UTM -> channel group (Paid Search, Paid Social, Organic Search, Direct, etc.) |

### High-Intent Website Visitor

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_high_intent_website_visitor` |
| **Grain** | 1 row per page event pattern |
| **Rule** | Visitor viewed pricing, contact, or demo pages on quiqup.com |

## Lead Classification

### Inbound vs Outbound

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_lead_source` |
| **Grain** | 1 row per Salesforce `lead_source` value |
| **Key columns** | `lead_source`, `source_group` (Inbound/Outbound/Old), `is_website_source` (BOOL), `is_contact_form` (BOOL) |

**Join pattern:**
```sql
JOIN views.definition_lead_source dls ON l.lead_source = dls.lead_source
```

**Gotcha:** The dashboard "Inbound Leads" filter uses a CUSTOM list of 48 lead_source values, NOT the `source_group` mapping from this view. They don't match — see opp-conversion-notes.md for details.

### Marketing Bucket (Region)

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_campaign_marketing_bucket` |
| **Grain** | 1 row per campaign name |
| **Purpose** | Campaign -> region bucket (uae/ksa/marketplace) |

### UTM -> Google Ads Campaign Mapping

| Property | Value |
|----------|-------|
| **Source of truth** | `views.definition_utm_google_ads_mapping` |
| **Grain** | 1 row per UTM campaign value |
| **Purpose** | Maps UTM campaign strings to Google Ads campaign + ad group |

## Opportunity & Conversion

### Opportunity Conversion

| Property | Value |
|----------|-------|
| **Source of truth** | `views.opportunities_convert_minus_2months` |
| **Rule** | An opportunity is "converted" when its linked SF account has a **parent account** that was created within the reporting window. Conversion is NOT measured by stage changes — it's measured by parent account existence and creation date. |
| **Key flag: `is_converted`** | TRUE when parent exists AND stage != 'Deal Lost' (all-time, no time window) |
| **Key flag: `converted_by_reporting_month`** | TRUE when converted within the +2 month reporting window (dashboard use only) |
| **Reporting offset** | `conversion_month` = `opp_created_month + 2 months` |
| **Dashboard target** | 27% conversion rate |

### New vs Existing Client (Opportunity Type)

| Property | Value |
|----------|-------|
| **Source of truth** | `views.opportunities_convert_minus_2months.client_type_classification` |
| **Rule** | Uses `LEAST(child_created_date, grandparent_created_date)` via `views.true_grandparent_account`. If opp created AFTER the earliest account in hierarchy -> 'E' (existing/upsell). If on/before -> 'N' (new business). |
| **Impact** | In 2025, filtering to 'N' only reduced cohort revenue from 14.2M to 2.5M AED (82% difference) |

### Account Activation Conversion

| Property | Value |
|----------|-------|
| **Source of truth** | `views.accounts_convert_minus_2months` |
| **Rule** | Account is "activated" when it has a delivered order at the grandparent level, with +2mo reporting offset |

## Revenue

### Net Revenue (Finance Reconciliation)

| Property | Value |
|----------|-------|
| **Source of truth** | `invoicer_current.invoices` |
| **Date filter** | `start_date` (billing period start, NOT payment date) |
| **States** | `paid`, `overdue` only (exclude draft/void) |
| **Formula** | `total_amount - tax_amount` (net of VAT) |
| **Filter** | `record_deleted = FALSE` |
| **KSA** | Exclude when comparing to Finance reports (tracked separately) |
| **Currency** | AED |

### Grandparent Revenue (Deduplicated)

| Property | Value |
|----------|-------|
| **Source of truth** | `views.grandparent_revenue` |
| **Rule** | Lifetime revenue per grandparent, deduplicated for invoice-to-parent routing |

### Gross Margin

| Property | Value |
|----------|-------|
| **Formula** | `revenue × 0.25` (25% gross margin assumption) |
| **Usage** | All margin columns in `marketing_funnel_grandparent_monthly` use this rate |

## Account Hierarchy

### Grandparent Resolution

| Property | Value |
|----------|-------|
| **Source of truth** | `views.true_grandparent_account` |
| **Grain** | 1 row per account |
| **Purpose** | Resolves any account to its grandparent in the hierarchy |

### Account Activation Date

| Property | Value |
|----------|-------|
| **Source of truth** | `views.grandparent_account_created_date_and_first_order_delivered` |
| **Rule** | `first_delivered_order_date IS NOT NULL` = activated. `2030-01-01` = placeholder for non-activated. |

## Attribution

### UTM Attribution (Grandparent)

| Property | Value |
|----------|-------|
| **Source of truth** | `views.grandparent_utm_attribution` |
| **Rule** | Earliest-first UTM attribution per grandparent, SSUP-aware |
| **Gotcha** | Only contains **activated** GPs — activation rate from this view alone = always 100% |

### Lead Source Attribution (Grandparent)

| Property | Value |
|----------|-------|
| **Source of truth** | `views.grandparent_lead_source_attribution` |
| **Rule** | Earliest-first lead source attribution rolled up to GP via `true_grandparent_account` |
| **Convenience** | `source_group` is pre-joined from `definition_lead_source` — no need to join separately |

## Unit Economics

| Metric | Formula | Notes |
|--------|---------|-------|
| **CAC** | `spend / customers_acquired` | Source: `views.cac` for weekly breakdown |
| **ROI** | `(margin - spend) / spend × 100` | Use margin (25%), not revenue |
| **Break-Even** | `spend / monthly_margin_rate` | If value < cohort_age_months, already profitable |
| **LTV:CAC** | `lifetime_margin / CAC` | Healthy = 3.0+ |
| **Agency fee** | 3,600 AED/month | Standard; include for true cost analysis |
