# Data Chaos 2026 — BigQuery Views Reference & Known Pitfalls

This document is the **source of truth** for Quiqup's analytics views. It describes what each table contains, what questions it can answer, and known data quality issues.

---

## Canonical Definitions (Source of Truth)

These views define the **authoritative** values for key business parameters. Always use these definitions—do not create ad-hoc logic.

### Lead Classification → `definition_lead_source`
| Property | Values | When to Use |
|----------|--------|-------------|
| **source_group** | `Inbound`, `Outbound`, `Old` | Categorizing ANY Salesforce lead |
| **is_website_source** | TRUE / FALSE | Filtering to web-originated leads only |
| **is_contact_form** | TRUE / FALSE | Filtering to contact form leads only |

### Traffic Classification → `definition_traffic_channel`
| Property | Definition | When to Use |
|----------|------------|-------------|
| **channel_group** | `Paid Search`, `Paid Social`, `Content`, `Email`, `Influencer`, `Offline`, `Referral` | Categorizing ANY session by UTM |
| **Paid traffic** | URL has `gclid/wbraid/gbraid` OR channel starts with "Paid" OR medium in (`cpc`, `ppc`, `paid`, `paid_social`, `display`, `banner`) | Paid vs Organic split |
| **Exclusion rule** | `source=trackingpage` + `medium=banner` | Filtering out internal experiments |

### Contact Form Submissions → `ga4_contact_form_submits`
| Property | Definition |
|----------|------------|
| **Contact pages** | `/contact`, `/contact-fulfillment`, `/contact-international`, `/contact-marketplace`, `/contact-last-mile-promo`, `/ksa/contact-ksa`, `/contact-tracking-page*` |
| **Submit events** | `submitContact`, `form_submit`, `form_submit--KSA`, `form_submit--Marketplace`, `form_submit--UAE_to_KSA` |
| **Dedupe rule** | Count submissions only when >60 seconds apart per user |

### Monthly Funnel Metrics → `quiqup_com_unique_visitors_monthly_2025_h2`
| Metric | Definition | Notes |
|--------|------------|-------|
| **unique_visitors** | Distinct `user_pseudo_id` per month | Excludes tracking banner traffic |
| **high_intent_visitors** | Visitors to pricing/contact/service pages | Subset of unique_visitors |
| **paid_unique_visitors** | Visitors with paid attribution | Uses Paid traffic logic above |
| **organic_unique_visitors** | Everything NOT paid | Includes Direct traffic |
| **google_ads_paid_sessions** | Session count from Google Ads | **Use this for clicks comparison** (not unique visitors) |
| **ga4_website_leads** | Distinct users submitting contact form | GA4 source |
| **sf_contact_form_website_source_leads_deduped** | Deduped SF leads from website | SF source |

### Data Quality Metrics → `contact_form_ga4_vs_sf_daily`
| Metric | What It Measures |
|--------|------------------|
| **ga4_estimated_submissions_60s** | Daily GA4 submissions (with 60s dedupe) |
| **sf_distinct_email_phone_pairs** | Daily SF submissions (dedupe by contact info) |
| **sf_duplicate_leads_vs_pairs** | How many duplicate leads created that day |

### View Ownership Summary

| Question | Authoritative View | Do NOT Use |
|----------|-------------------|------------|
| "Is this lead Inbound or Outbound?" | `definition_lead_source` | Ad-hoc CASE statements |
| "Is this lead from a contact form?" | `definition_lead_source` | String matching on lead_source |
| "Is this traffic Paid or Organic?" | `definition_traffic_channel` + Paid logic | Ad-hoc UTM parsing |
| "What channel is this session?" | `definition_traffic_channel` | Manual source/medium mapping |
| "How many leads this month?" | `quiqup_com_unique_visitors_monthly_2025_h2` | Raw event counts |
| "How many form submissions today?" | `contact_form_ga4_vs_sf_daily` | Raw GA4 events (not deduped) |
| "Are GA4 and SF aligned?" | `contact_form_ga4_vs_sf_daily` | Separate queries to each system |

---

## Quick Reference

| View | Grain | Rows | Date Range | Primary Use |
|------|-------|------|------------|-------------|
| `views.quiqup_com_unique_visitors_monthly_2025_h2` | 1 row per month | 37 | 2023-01 → 2026-01 | Monthly traffic funnel |
| `views.ga4_contact_form_submits` | 1 row per submit event | 18,478 | 2025-01-01 → present | Contact form tracking |
| `views.definition_lead_source` | 1 row per lead_source value | 75 | N/A (lookup) | Salesforce lead classification |
| `views.definition_traffic_channel` | 1 row per source/medium pair | 12 | N/A (lookup) | UTM → channel mapping |
| `views.contact_form_ga4_vs_sf_daily` | 1 row per day | ~1,800 | 2020-03 → present | GA4↔SF reconciliation |

---

## 1. `quiqup.views.quiqup_com_unique_visitors_monthly_2025_h2`

### What It Contains

Monthly traffic funnel for `www.quiqup.com` with paid/organic splits and lead counts.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `month` | DATE | First day of month (e.g., 2025-09-01) |
| `unique_visitors` | INT64 | Distinct `user_pseudo_id` visiting the site |
| `high_intent_visitors` | INT64 | Visitors who viewed pricing, contact, or service pages |
| `paid_unique_visitors` | INT64 | Visitors with paid attribution (any paid channel) |
| `organic_unique_visitors` | INT64 | Visitors without paid attribution (includes Direct) |
| `google_ads_paid_unique_visitors` | INT64 | Visitors attributed to Google Ads specifically |
| `google_ads_paid_sessions` | INT64 | Sessions (not users) from Google Ads — closest proxy to "clicks" |
| `ga4_website_leads` | INT64 | Distinct users who submitted a contact form (GA4) |
| `sf_contact_form_website_source_leads_deduped` | INT64 | Salesforce leads from website contact forms (deduped) |

**Sample Data (recent months):**
| month | unique_visitors | high_intent | paid | organic | ga4_leads | sf_leads_deduped |
|-------|-----------------|-------------|------|---------|-----------|------------------|
| 2026-01 | 12,958 | 3,127 | 5,498 | 7,460 | 577 | 481 |
| 2025-12 | 15,689 | 3,690 | 7,345 | 8,344 | 523 | 584 |
| 2025-11 | 16,374 | 3,379 | 7,540 | 8,833 | 249 | 696 |
| 2025-10 | 16,719 | 3,477 | 8,220 | 8,499 | 401 | 404 |
| 2025-09 | 14,398 | 3,828 | 7,082 | 7,316 | 474 | 445 |

### Questions This View Answers

- "How many unique visitors did we get last month?"
- "What's our paid vs organic traffic split?"
- "How many contact form leads did we generate?"
- "What's the conversion rate from visitor → lead?"
- "How do Google Ads sessions compare to clicks in the UI?"

### Known Issues & Gotchas

**1. Google Ads clicks ≠ unique visitors**
- `google_ads_paid_sessions` (~8,867 in Sep 2025) is comparable to Google Ads UI clicks (~9,050)
- `google_ads_paid_unique_visitors` (6,892) is NOT — it counts people, not clicks

**2. Tracking banner exclusion applied**
- Traffic with `utm_source=trackingpage` + `utm_medium=banner` is excluded
- Scale: Nov 2025 excluded 6,127 users, Dec 2025 excluded 3,987 users

**3. Nov 2025 GA4 tracking outage**
- GA4 submit tracking broke Oct 23 – Nov 27, 2025
- `ga4_website_leads` (249) is artificially low vs `sf_contact_form_website_source_leads_deduped` (696)

---

## 2. `quiqup.views.ga4_contact_form_submits`

### What It Contains

Every contact form submission event from GA4, filtered to contact-related pages on `www.quiqup.com`.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `event_date` | DATE | Date of the event |
| `event_datetime` | TIMESTAMP | Exact timestamp |
| `user_pseudo_id` | STRING | GA4 anonymous user ID |
| `ga_session_id` | INT64 | Session identifier |
| `event_name` | STRING | `submitContact`, `form_submit`, `form_submit--KSA`, etc. |
| `page_location` | STRING | Full URL including UTM parameters |
| `path` | STRING | URL path (e.g., `/contact`, `/ksa/contact-ksa`) |
| `is_tracking_page` | BOOL | Whether this is from the tracking banner experiment |

**Event Names Captured:**
- `submitContact` (primary)
- `form_submit`
- `form_submit--KSA`
- `form_submit--Marketplace`
- `form_submit--UAE_to_KSA`

**Contact Pages Included:**
- `/contact`
- `/contact-fulfillment`
- `/contact-international`
- `/contact-marketplace`
- `/contact-last-mile-promo`
- `/ksa/contact-ksa`
- `/contact-tracking-page*`

### Questions This View Answers

- "How many form submissions happened on a specific date?"
- "Which contact page gets the most submissions?"
- "What UTM campaigns are driving form fills?"
- "Did a specific user submit multiple times?"

### Known Issues & Gotchas

**1. Multiple events per submit (use 60s dedupe)**
- One human submit can fire 2–3 events (double-click, SPA re-render, tag duplication)
- **Recommended:** Count submissions only when >60 seconds apart per user

**2. Tracking outage Oct 23 – Nov 27, 2025**
- Events are missing/undercounted in this period
- Use Salesforce leads as fallback for this window

---

## 3. `quiqup.views.definition_lead_source`

### What It Contains

Lookup table mapping every Salesforce `lead_source` value to standardized groups and flags.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `lead_source` | STRING | Raw Salesforce lead_source value |
| `source_group` | STRING | `Inbound`, `Outbound`, or `Old` |
| `is_website_source` | BOOL | TRUE if lead originated from website |
| `is_contact_form` | BOOL | TRUE if lead came from a contact form |

**Source Group Breakdown (75 total):**
| source_group | Count | Examples |
|--------------|-------|----------|
| Inbound | 42 | `Inbound: Contact form`, `Inbound: Self-signup`, `Google Ad` |
| Outbound | 14 | `Outbound: Own research`, `Outbound: Leadzen` |
| Old | 19 | Legacy/invalid values, foreign language variants |

**Contact Form Sources (is_contact_form = TRUE):**
- `Inbound: Contact form`
- `Inbound: Contact form International`
- `Inbound: Contact form KSA`
- `Inbound: Contact form Marketplace`
- `Inbound: Contact form UAE KSA`
- `Inbound: Contact form fulfillment`
- `Inbound: Contact form LMD Promo`
- `Inbound: Contact Form Tracking Banner`

### Questions This View Answers

- "Which lead sources count as 'Inbound' vs 'Outbound'?"
- "Which lead sources represent contact form submissions?"
- "Is this lead from our website or an external source?"

### How to Use

```sql
-- Get all inbound contact form leads
SELECT l.*
FROM salesforce_current.leads l
JOIN views.definition_lead_source d ON l.lead_source = d.lead_source
WHERE d.source_group = 'Inbound'
  AND d.is_contact_form = TRUE
```

---

## 4. `quiqup.views.definition_traffic_channel`

### What It Contains

Lookup table mapping UTM `source`/`medium` pairs to channel groups for traffic classification.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `source_key` | STRING | UTM source (lowercase) |
| `medium_key` | STRING | UTM medium (lowercase) |
| `channel_group` | STRING | Channel classification |
| `owner` | STRING | Team responsible (all "Marketing") |

**Full Contents (12 rows):**
| source_key | medium_key | channel_group |
|------------|------------|---------------|
| `google` | `cpc` | Paid Search |
| `fb` | `paid` | Paid Social |
| `ig` | `paid` | Paid Social |
| `fb-sitelink` | `paid` | Paid Social |
| `an` | `paid` | Paid Social |
| `trackingpage` | `banner` | **Exclude - Internal Banner Experiment** |
| `blog` | `content` | Content |
| `journey_email` | `email` | Email |
| `poppyloves` | `influencer` | Influencer |
| `forwardqr.com` | `qr_code` | Offline |
| `paperform` | `logo` | Referral |
| `trustpilot` | `company_profile` | Referral |

### Questions This View Answers

- "How should I classify traffic from utm_source=X, utm_medium=Y?"
- "What UTM combinations should be excluded from reporting?"
- "Which channels are considered 'Paid'?"

### Paid vs Organic Logic

A session is **Paid** if ANY of:
1. URL contains `gclid`, `wbraid`, or `gbraid`
2. `channel_group` starts with "Paid" (Paid Search, Paid Social)
3. `utm_medium` is `cpc`, `ppc`, `paid`, `paid_social`, `display`, or `banner`

Everything else is **Organic** (including Direct traffic).

---

## 5. `quiqup.views.contact_form_ga4_vs_sf_daily`

### What It Contains

Daily reconciliation between GA4 contact form events and Salesforce lead records.

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| `date` | DATE | Calendar date |
| `ga4_unique_users` | INT64 | Distinct GA4 users who submitted |
| `ga4_estimated_submissions_60s` | INT64 | Submissions with 60s dedupe applied |
| `sf_inbound_contact_form_leads` | INT64 | Raw Salesforce lead count |
| `sf_leads_missing_email_phone` | INT64 | Leads with no contact info (spam/invalid) |
| `sf_distinct_email_phone_pairs` | INT64 | Unique (email, phone) combinations |
| `sf_duplicate_leads_vs_pairs` | INT64 | `sf_leads - sf_distinct_pairs` (duplicate indicator) |

**Date Range:** 2020-03-17 → present (GA4 data starts 2025-01-01)

### Questions This View Answers

- "Are GA4 and Salesforce tracking the same submissions?"
- "How many duplicate leads are we creating per day?"
- "What days had tracking issues (GA4 nulls, SF spikes)?"
- "What's the daily submission volume trend?"

### How to Read the Data

| Scenario | Interpretation |
|----------|----------------|
| `ga4_estimated_submissions_60s` ≈ `sf_distinct_email_phone_pairs` | Tracking is healthy |
| `ga4_*` is NULL, SF has data | GA4 tracking outage |
| `sf_duplicate_leads_vs_pairs` > 0 | Salesforce receiving duplicate submissions |
| `sf_leads_missing_email_phone` > 0 | Invalid/spam leads being created |

---

## Common Pitfalls Summary

| Issue | Symptom | Root Cause | Solution |
|-------|---------|------------|----------|
| Clicks ≠ visitors | Google Ads clicks don't match BigQuery | Different units (clicks vs unique users) | Use `google_ads_paid_sessions` for clicks comparison |
| Nov 2025 mismatch | GA4 leads << SF leads | Tracking outage Oct 23 – Nov 27 | Use SF as source of truth for this period |
| Double-counted submits | GA4 events > actual submissions | Multiple events per submit | Apply 60s dedupe |
| Inflated SF leads | SF count > GA4 | Duplicates + empty leads | Use `sf_distinct_email_phone_pairs` |
| Numbers changed | Historical report doesn't match | Views updated with new exclusions | Views reflect current definition; snapshot if needed |
| Tracking banner traffic | Unexpected traffic spike | Internal experiment | Already excluded via `definition_traffic_channel` |

---

## Canonical Join Patterns

### Traffic channel classification
```sql
SELECT *
FROM ga4_sessions s
LEFT JOIN views.definition_traffic_channel c
  ON LOWER(s.utm_source) = c.source_key
  AND LOWER(s.utm_medium) = c.medium_key
```

### Salesforce lead source mapping
```sql
SELECT l.*, d.source_group, d.is_contact_form
FROM salesforce_current.leads l
LEFT JOIN views.definition_lead_source d
  ON l.lead_source = d.lead_source
```

### Monthly funnel metrics
```sql
SELECT *
FROM views.quiqup_com_unique_visitors_monthly_2025_h2
WHERE month >= '2025-01-01'
ORDER BY month
```

---

*Last verified: 2026-01-28*
