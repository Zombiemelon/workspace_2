# Database Reference — Full Column Schemas

Detailed column-level schemas for the Quiqup BigQuery project. See `SKILL.md` for quick-scan overview.

**Project:** `quiqup` | **Region:** Many datasets are EU (notably `analytics_368564502` and `google_ads_analytics`).

---

## Dataset: `analytics_368564502` (GA4)

### `views.google_analytics_events`
- **Grain:** 1 GA4 event. Flattened/cleaned (no manual `event_params` extraction).
- **Key columns:** `event_date` (DATE), `event_name`, `user_pseudo_id`, `page_location`, `page_title`, `campaign_source`, `campaign_medium`, `campaign_name`
- **Coverage:** Filters `event_date > '2025-02-04'`.

### Raw: `analytics_368564502.events_*`
- **Grain:** 1 GA4 event (nested). Sharded by date; `event_params` requires extraction.
- **Note:** `business-ae-beta.quiqup.com` has no data since **May 29, 2025**.

---

## Dataset: `views` (Analytical Views)

### `views.master_account_data_daily`
- **Grain:** 1 account/day (enriched "account spine").
- **Key columns:**
  - `external_id` (INT64): external client identifier
  - `day_created_client` (DATE), `earliest_created_date` (DATE, preferred for cohorts), `minimum_created_date` (TIMESTAMP)
  - `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term` (STRING)
  - `total_orders` (INT64), `first_orde_submitted_calculated` (TIMESTAMP), `is_activated` (BOOL)
  - `account_id` (STRING): Salesforce account id
  - `pricing_model` (STRING): links to `salesforce_current.pricing_models.id`
- **Quality:** `utm_term` may be URL-encoded (sometimes multiple times).

### `views.definition_paid_organic_channel`
- **Grain:** 1 row per UTM source/medium. Single source of truth for paid vs organic.
- **Key columns:** `utm_source` ('*' for wildcard), `utm_medium`, `channel_type` ('Paid'/'Organic'), `channel_detail`, `is_paid` (BOOL)
- **Rule:** NOT explicitly PAID = ORGANIC (including missing UTM)
- **Join pattern (priority: exact > wildcard > default organic):**
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

### `views.definition_lead_source`
- **Grain:** 1 row per `lead_source` value.
- **Key columns:** `lead_source`, `source_group` (Inbound/Outbound/Old), `is_website_source` (BOOL), `is_contact_form` (BOOL)

### `views.ga4_contact_form_submits`
- **Grain:** 1 form submit event.
- **Key columns:** `event_date`, `event_datetime`, `user_pseudo_id`, `ga_session_id`, `event_name`, `page_location`, `path`, `is_tracking_page`
- **Note:** Multiple event names represent a submit; dedupe within short time window per user.

### `views.quiqup_com_unique_visitors_monthly_2025_h2`
- **Grain:** 1 row/month. Monthly funnel: traffic → leads → spend.
- **Key columns:**
  - `month` (DATE), `unique_visitors`, `high_intent_visitors` (INT64)
  - `paid_unique_visitors`, `organic_unique_visitors` (INT64)
  - `google_ads_paid_unique_visitors`, `google_ads_paid_sessions` (INT64)
  - `ga4_website_leads` (INT64): distinct submitters
  - `sf_contact_form_website_source_leads_deduped` (INT64): recommended SF metric
  - Spend: `google_ads_spend_aed`, `google_ads_clicks`, `google_ads_impressions`, `cost_per_lead_aed`, `cost_per_click_aed`
- **Exclusion:** Internal tracking banner experiment traffic excluded.
- **Paid classification (GA4):**
  - Paid session: `gclid`/`wbraid`/`gbraid` OR channel_group starts with 'Paid' OR paid `utm_medium`
  - Google Ads: click IDs OR (`utm_source='google'` AND `utm_medium='cpc'`)
  - User-level: ANY paid session = paid visitor (uses MAX)
- **Dependency tree:**
```
quiqup_com_unique_visitors_monthly_2025_h2
├── ga4_unique_visitors_monthly
├── ga4_high_intent_visitors_monthly ← definition_high_intent_website_visitor
├── ga4_channel_monthly_quiqup_com
│   └── ga4_traffic_classified_sessions_quiqup_com [PAID/ORGANIC LOGIC]
├── ga4_google_ads_paid_sessions_monthly_quiqup_com
├── ga4_contact_form_submitters_monthly_quiqup_com ← ga4_contact_form_submits
├── salesforce_leads_monthly
└── [CTE] monthly_spend ← ads_CampaignBasicStats_8350869641
```

### `views.marketing_funnel_grandparent_monthly`

**SINGLE SOURCE OF TRUTH FOR MARKETING PERFORMANCE.**

- **Grain:** 1 row/month (H2 2025: July–December).

#### Traffic & Leads
| Column | Type | Source |
|--------|------|--------|
| `unique_visitors` | INT64 | GA4 user count |
| `high_intent_visitors` | INT64 | Pricing/contact/demo page visitors |
| `paid_unique_visitors` | INT64 | Users with ANY paid session |
| `organic_unique_visitors` | INT64 | Users with NO paid sessions |
| `ga4_website_leads` | INT64 | GA4 form submitters |
| `sf_contact_form_website_source_leads_deduped` | INT64 | SF leads, deduplicated |

#### Spend
| Column | Type | Source |
|--------|------|--------|
| `google_ads_spend_aed` | FLOAT64 | `metrics_cost_micros / 1M` |
| `google_ads_clicks` | INT64 | `metrics_clicks` |
| `google_ads_impressions` | INT64 | `metrics_impressions` |

#### Grandparent Acquisition
| Column | Calculation |
|--------|-------------|
| `grandparents_acquired` | ALL GPs created in month M |
| `gp_with_attribution` | GPs with non-NULL UTM |
| `attribution_coverage_pct` | `gp_with_attribution / grandparents_acquired × 100` |
| `gp_acquired_paid` | GPs where UTM = PAID via `definition_paid_organic_channel` |
| `gp_acquired_organic` | `grandparents_acquired - gp_acquired_paid` |
| `gp_acquired_from_google` | GPs where `attributed_utm_source = 'google'` |
| `distinct_campaigns_in_cohort` | Distinct campaign values |

#### Activation
| Column | Calculation |
|--------|-------------|
| `cohort_ever_activated` | GPs with `first_delivered_order_date IS NOT NULL` |
| `cohort_activation_rate_pct` | `activated / acquired × 100` |

#### Revenue (invoice-to-parent deduplicated)
| Column | Calculation |
|--------|-------------|
| `cohort_lifetime_revenue_aed` | ALL GPs revenue |
| `cohort_lifetime_revenue_paid_aed` | Paid GPs revenue |
| `cohort_lifetime_revenue_organic_aed` | Organic GPs revenue |
| `revenue_paid_pct`, `revenue_organic_pct` | Split % |
| `cohort_total_orders` | Delivered orders |

#### Margin (Revenue × 0.25)
`cohort_margin_aed`, `cohort_margin_paid_aed`, `cohort_margin_organic_aed`

#### Unit Economics
| Column | Calculation |
|--------|-------------|
| `cost_per_gp_acquired` | `spend / grandparents_acquired` |
| `cost_per_gp_acquired_paid` | `spend / gp_acquired_paid` |
| `ltv_per_gp_acquired` | `revenue / grandparents_acquired` |
| `ltv_margin_per_gp_acquired` | `margin / grandparents_acquired` — **use for profitability** |
| `cohort_roi` | `(margin - spend) / spend` |
| `cohort_roi_paid` | `(paid_margin - spend) / spend` |

#### Break-Even
| Column | Calculation |
|--------|-------------|
| `cohort_age_months` | Months since cohort (min 1) |
| `monthly_margin_paid_aed` | `paid_margin / cohort_age_months` |
| `breakeven_months_paid` | `spend / monthly_margin_paid_aed` |
| `breakeven_months_paid_with_agency` | `(spend + 3600) / monthly_margin_paid_aed` |
| `breakeven_months_total` | `spend / monthly_margin_total_aed` |

#### Dependency Tree
```
marketing_funnel_grandparent_monthly
├── quiqup_com_unique_visitors_monthly_2025_h2 (traffic, leads, spend)
├── grandparent_account_created_date_and_first_order_delivered (ALL GPs)
├── grandparent_utm_attribution (~50% of GPs)
├── definition_paid_organic_channel ★ SOURCE OF TRUTH
└── grandparent_revenue ★ SOURCE OF TRUTH
```

### `views.cac`
- **Grain:** 1 row/account/week. Weekly CAC = spend ÷ activated clients.
- **Key columns:** `id` (SF account ID), `created_week` (Monday), `account_lead_source_grouped_marketing`, `CAC`, `CAC_paid`
- **Note:** Activation is lagged; recent cohorts look inflated.

### `views.definition_campaign_marketing_bucket`
- **Grain:** 1 row/campaign name. Columns: `campaign_name`, `marketing_bucket` (uae/ksa/marketplace).
- **Coverage:** 35 campaigns; unmapped = "other". Auto-include: `GL_QQP_GA_SEM%` / `GL_QQP_GA_MAX%` → "uae".

### `views.definition_utm_google_ads_mapping`
- **Grain:** 1 row/UTM campaign. Maps UTM → Google Ads campaign/ad group.
- **Key columns:** `utm_campaign`, `google_ads_campaign`, `google_ads_ad_group` (NULL for PMax), `marketing_bucket`, `campaign_type` (search/pmax/demandgen/meta/internal/content/direct)
- **Coverage:** 48 UTM patterns (36 Google Ads, 5 Meta, 7 other).

### `views.account_utm_attribution`
- **Grain:** 1 row/SF account with UTM. Earliest-first across Lead → Opp → Account.
- **Key columns:** `account_id`, `attributed_from_object`, `attributed_from_id`, `attributed_object_created_date`, `attributed_utm_campaign`, `attributed_utm_source`, `attributed_utm_medium`, `attributed_utm_content`, `attributed_utm_term`
- **Coverage:** 11,695 accounts (31%). Uses `COALESCE(utm_*, pi_utm_*)` for Pardot fallback.

### `views.grandparent_utm_attribution`
- **Grain:** 1 row/grandparent with UTM. Earliest-first, SSUP-aware.
- **Key columns:** `grandparent_account_id`, `grandparent_account_name`, `acquisition_date`, `attributed_utm_campaign`, `attributed_utm_source`, `attributed_utm_medium`, `attributed_from_object`
- **CRITICAL: ONLY activated GPs.** Never use for activation rates.
- **Paid filter:** `attributed_utm_medium = 'cpc'` for Google Ads paid.
- **SSUP:** Parent `0010800003I4PcsAAF` children = own grandparent.

### `views.grandparent_revenue`
- **Grain:** 1 row/grandparent. Deduplicated lifetime revenue.
- **Key columns:** `grandparent_account_id`, `total_revenue_aed`, `total_invoices`
- **Dedup:** Uses `effective_invoicing_account`. Without = ~19x inflation.
- **Filter:** `state NOT IN ('void', 'cancelled', 'draft')` AND `record_deleted = FALSE`

### `views.account_lead_source_attribution`
- **Grain:** 1 row/SF account with lead source. Earliest-first.
- **Key columns:** `account_id`, `attributed_from_object`, `attributed_lead_source`
- **Coverage:** 27,299 accounts (71.6%) — 2.3x better than UTM attribution.

### `views.grandparent_lead_source_attribution`
- **Grain:** 1 row/grandparent with lead source.
- **Key columns:** `grandparent_account_id`, `grandparent_account_name`, `acquisition_date`, `attributed_lead_source`, `source_group` (pre-joined), `is_website_source`, `is_contact_form`
- **Coverage:** 23,992 GPs. Includes ALL GPs with lead source (not just activated).

### `views.google_ads_spend_monthly`
- **Grain:** 1 row/month/campaign/ad group.
- **Key columns:** `month`, `google_ads_campaign`, `google_ads_ad_group` (NULL for PMax), `clicks`, `impressions`, `spend_aed`, `conversions`

### `views.ga4_traffic_classified_sessions_quiqup_com`
- **Grain:** 1 session. Core traffic classification.
- **Key columns:** `month`, `user_pseudo_id`, `ga_session_id`, `has_click_id`, `is_paid_session`, `is_google_ads_session`

### `views.definition_traffic_channel`
- **Grain:** 1 row/source+medium. Columns: `source_key`, `medium_key`, `channel_group`, `owner`.
- Paid = `channel_group` starting with 'Paid'. Special: `'Exclude - Internal Banner Experiment'`.

### Other Views
- `views.definition_high_intent_website_visitor` — 1 qualifying page view. `high_intent_reason`.
- `views.salesforce_leads_monthly` — Key: `sf_contact_form_website_source_leads_deduped`.
- `views.opportunities_convert_minus_2months` — `is_converted` (all-time), `converted_by_reporting_month` (+2mo).
- `views.accounts_convert_minus_2months` — Account activation at GP level.

---

## Dataset: `ex_api_current` (Operational API)

### `ex_api_current.orders`
- **Grain:** 1 order (current state). Key: `client_order_id`, `business_partner_id` (→ `business_accounts.id`), `state` (current only), `inserted_at`, `updated_at` (partition), `record_deleted`.
- Use `order_state_changes` for historical transitions.

### `ex_api_current.business_accounts`
- **Grain:** 1 business account. Key: `id`, `name`, `billing_country`, `record_deleted`.
- **Bridge:** `external_id` (STRING) → `master_account_data_daily.external_id` (INT64, cast).

### `ex_api_current.order_state_changes`
- **Grain:** 1 state transition. Key: `client_order_id`, `state`, `on_hold_reason`, `inserted_at`, `occurred_at`.

---

## Dataset: `invoicer_current`

### `invoicer_current.accounts` (27K rows)
- **Key columns:** `id` (STRING, SF format), `account_id` (INTEGER, **use for invoice joins**), `salesforce_id`, `account_name`
- **Hierarchy:** `parent_account_id` (INT), `parent_salesforce_id`, `grandparent_salesforce_id`
- **CRITICAL:** `invoice_to_parent` (BOOL) — if TRUE, invoices go to parent
- **Join pattern:**
```sql
JOIN invoicer_current.invoices i
  ON i.account_id = CASE
    WHEN a.invoice_to_parent = TRUE THEN a.parent_account_id
    ELSE a.account_id END
```

### `invoicer_current.invoices` (120K rows)
- **Partitioned by:** `updated_at` (MONTH).
- **Key columns:** `id` (INT, PK), `account_id` (INT, **NOT string**), `invoice_number`, `start_date`/`end_date` (DATE), `total_amount`, `balance`, `tax_amount`, `state` (paid/void/draft/sent), `currency` (lowercase "aed"), `record_deleted`, `deleted_at`
- **Revenue:** `total_amount - tax_amount` where `state IN ('paid', 'overdue')` and `record_deleted = FALSE`
- **Finance date:** Use `start_date` NOT `end_date` — wrong = ~205K AED discrepancy.

### `invoicer_current.invoice_lines` (13M rows)
- **Partitioned by:** `updated_at`. Key: `id`, `invoice_id` (→ invoices), `order_id`, `description`, `quantity`, `type`, `amount`, `tax_amount`.

### `invoicer_current.credit_notes` (49K rows)
- **Partitioned by:** `created_at`. Key: `id`, `account_id`, `invoice_id`, `amount`, `state`, `date`. Typically COD refunds.

### `invoicer_current.forecast_invoice_lines` (13M rows)
- **Partitioned by:** `created_at`. No `invoice_id` — becomes `invoice_lines` when invoiced.

---

## Dataset: `salesforce_current`

### `salesforce_current.accounts`
- Key: `id`, `name`, `created_date` (TIMESTAMP), `client_type_c` (NULL=B2B, 'Individual'=B2C), `account_source`, UTMs (`utm_campaign_c`, `UTM_Source_c`, `UTM_Medium_c`), `external_id_c`, `first_order_delivered_c`, `Pricing_Model_c`
- **B2B filter:** `WHERE client_type_c IS NULL AND is_deleted = FALSE`

### `salesforce_current.leads`
- Key: `id`, `created_date`, `lead_source`, `email`, `phone`, UTMs (`utm_campaign_c`, etc.), Pardot UTMs (`pi_utm_campaign_c`, etc.), `converted_opportunity_id` (FK → opportunities)

### `salesforce_current.opportunities`
- Key: `id`, `account_id`, `name`, `created_date`, `stage_name`, `is_deleted`, `is_won`, `is_closed`, `pricing_model_status_c`, `client_classification_c`, `deal_done_timestamp_c`

### `salesforce_current.tasks`
- Email filter: `task_subtype = 'Email'`. Key: `what_id` (→ opportunities), `who_id` (person), `description`, `created_by_id`.

### `salesforce_current.pricing_models`
- PK: `id` (matches `master.pricing_model`). Use `name_c` over `name`.

---

## Dataset: `bi_reporting`

- `sales_funnel` — Combined Leads + Opps + Accounts. Key: `account_id`, `lead_id`, `opportunity_id`.
- `missions` — 1 mission. Key: `id`, `mission_date_utc`.
- `internal_orders` — Mission-order link. Key: `mission_id`, `client_order_id`, `state`, `type`.
- `client_orders` — 1 order. Key: `id`, `state_updated_at`.
- `couriers` — 1 courier. Key: `id`, `email`, `firstname`, `lastname`.

---

## Dataset: `google_ads_analytics`

### `ads_CampaignBasicStats_8350869641`
- 1 campaign/day. Key: `metrics_cost_micros` (÷1M = AED), `metrics_clicks`, `metrics_impressions`, `metrics_conversions`, `segments_date`, `campaign_id`.

### `ads_Campaign_8350869641`
- 1 campaign/day (snapshot). Key: `campaign_id`, `campaign_name`, `campaign_status`, `_DATA_DATE`, `_LATEST_DATE`.
- **MUST filter `_DATA_DATE = _LATEST_DATE`** (22K+ rows for 39 campaigns otherwise).

### `ads_AdGroup_8350869641`
- 1 ad group/day (snapshot). Key: `ad_group_id`, `campaign_id`, `ad_group_name`, `_DATA_DATE`, `_LATEST_DATE`.
- **MUST filter `_DATA_DATE = _LATEST_DATE`** (407K+ rows for 630 ad groups otherwise).

### UTM ↔ Google Ads Mapping
Pattern: `CONCAT(REPLACE(REPLACE(campaign_name, ' - ', '_'), ' ', '-'), '_', REPLACE(ad_group_name, ' ', '-'))` = `utm_campaign`

| UTM Campaign | Google Ads Campaign | Ad Group |
|---|---|---|
| `Generic-Services_Dubai_Fulfillment` | Generic Services - Dubai | Fulfillment |
| `Generic-Services_Ecommerce` | Generic Services | Ecommerce |

Caveats: 2 UTM values don't match exactly. Auto-tagging enabled (GCLID = primary tracking).
