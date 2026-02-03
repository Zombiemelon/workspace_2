# UTM Attribution Logic for Quiqup Salesforce Data

## Overview

This document defines the reusable UTM attribution logic for Quiqup's Salesforce data warehouse. The goal is to attribute marketing UTM parameters to accounts by finding the **earliest created object** (Lead, Opportunity, or Account) that has UTM data in the conversion chain.

### Deployment Status ✅

| Item | Value |
|------|-------|
| **View Name** | `quiqup.views.account_utm_attribution` |
| **Status** | **LIVE** |
| **Deployed** | 2026-01-29 |
| **Total Attributed Accounts** | 11,695 |

**Attribution Breakdown:**
| Source Object | Accounts | Unique Campaigns |
|--------------|----------|------------------|
| Account | 10,946 | 65 |
| Lead | 739 | 57 |
| Opportunity | 10 | 5 |

## Data Model Summary

### Object Hierarchy
```
Lead (converted_account_id, converted_opportunity_id)
  └── Opportunity (account_id)
        └── Account (parent_id)
              └── Parent Account (parent_id)
                    └── Grandparent Account
```

### Key Tables & Fields

| Table | Key UTM Fields | Hierarchy Fields |
|-------|---------------|------------------|
| `salesforce_current.leads` | `utm_campaign_c`, `utm_source_c`, `utm_medium_c`, `utm_content_c`, `utm_term_c`, `pi_utm_campaign_c`, `pi_utm_source_c`, `pi_utm_medium_c` | `converted_account_id`, `converted_opportunity_id` |
| `salesforce_current.opportunities` | `utm_campaign_c`, `utm_source_c`, `utm_medium_c`, `utm_content_c`, `utm_term_c` | `account_id` |
| `salesforce_current.accounts` | `utm_campaign_c`, `UTM_Source_c`, `UTM_Medium_c`, `UTM_Content_c`, `UTM_Term_c` | `parent_id`, `Grandparent_Account_c` |

### Data Population Rates (as of Jan 2026)

| Object | Total Records | Has Any UTM | % Coverage |
|--------|--------------|-------------|------------|
| Leads | 30,872 | 8,363 | 27.1% |
| Opportunities | 6,707 | 741 | 11.0% |
| Accounts | 37,817 | 11,683 | 30.9% |

### Key Relationships
- **4,858** leads converted to accounts
- **4,793** leads converted to opportunities
- **32,962** accounts were NOT created from lead conversion (but 10,766 still have UTM data)
- **1,914** opportunities created directly (not from lead) - none have UTM data
- **31,363** accounts have a parent account

## Attribution Logic

### Priority Order (Earliest-First Attribution)
1. Find all objects in the account's conversion chain that have UTM data
2. Select the **earliest created** object based on `created_date`
3. Use that object's UTM values for attribution
4. If no object has UTM data, return NULL

### Objects Considered (in order of typical creation)
1. **Lead** - Original inbound lead with UTM capture
2. **Opportunity** - Created when lead converts or created directly
3. **Account** - Created when lead converts or created directly (e.g., self-signup)

### Handling Multiple UTM Sources on Leads
Leads have two sets of UTM fields:
- Direct UTM: `utm_campaign_c`, `utm_source_c`, `utm_medium_c`
- Pardot UTM: `pi_utm_campaign_c`, `pi_utm_source_c`, `pi_utm_medium_c`

**Resolution**: Use `COALESCE(utm_*, pi_utm_*)` - prefer direct UTM, fall back to Pardot UTM.

---

## Reusable SQL CTEs

### CTE 1: `utm_attribution_base`
Gathers all UTM sources for each account from leads, opportunities, and accounts.

```sql
-- CTE: utm_attribution_base
-- Purpose: Collect all UTM sources across the account conversion chain
WITH utm_attribution_base AS (
  -- Source 1: Account's own UTM fields
  SELECT
    a.id AS account_id,
    'account' AS source_object_type,
    a.id AS source_object_id,
    a.created_date AS source_created_date,
    a.utm_campaign_c AS utm_campaign,
    a.UTM_Source_c AS utm_source,
    a.UTM_Medium_c AS utm_medium,
    a.UTM_Content_c AS utm_content,
    a.UTM_Term_c AS utm_term
  FROM `quiqup.salesforce_current.accounts` a
  WHERE a.is_deleted = FALSE
    AND (
      (a.utm_campaign_c IS NOT NULL AND a.utm_campaign_c != '')
      OR (a.UTM_Source_c IS NOT NULL AND a.UTM_Source_c != '')
      OR (a.UTM_Medium_c IS NOT NULL AND a.UTM_Medium_c != '')
    )

  UNION ALL

  -- Source 2: Opportunities linked to the account
  SELECT
    o.account_id,
    'opportunity' AS source_object_type,
    o.id AS source_object_id,
    o.created_date AS source_created_date,
    o.utm_campaign_c AS utm_campaign,
    o.utm_source_c AS utm_source,
    o.utm_medium_c AS utm_medium,
    o.utm_content_c AS utm_content,
    o.utm_term_c AS utm_term
  FROM `quiqup.salesforce_current.opportunities` o
  WHERE o.is_deleted = FALSE
    AND o.account_id IS NOT NULL
    AND (
      (o.utm_campaign_c IS NOT NULL AND o.utm_campaign_c != '')
      OR (o.utm_source_c IS NOT NULL AND o.utm_source_c != '')
      OR (o.utm_medium_c IS NOT NULL AND o.utm_medium_c != '')
    )

  UNION ALL

  -- Source 3: Leads that converted to this account (with Pardot fallback)
  SELECT
    l.converted_account_id AS account_id,
    'lead' AS source_object_type,
    l.id AS source_object_id,
    l.created_date AS source_created_date,
    COALESCE(NULLIF(l.utm_campaign_c, ''), l.pi_utm_campaign_c) AS utm_campaign,
    COALESCE(NULLIF(l.utm_source_c, ''), l.pi_utm_source_c) AS utm_source,
    COALESCE(NULLIF(l.utm_medium_c, ''), l.pi_utm_medium_c) AS utm_medium,
    l.utm_content_c AS utm_content,
    l.utm_term_c AS utm_term
  FROM `quiqup.salesforce_current.leads` l
  WHERE l.is_deleted = FALSE
    AND l.converted_account_id IS NOT NULL
    AND (
      (l.utm_campaign_c IS NOT NULL AND l.utm_campaign_c != '')
      OR (l.utm_source_c IS NOT NULL AND l.utm_source_c != '')
      OR (l.utm_medium_c IS NOT NULL AND l.utm_medium_c != '')
      OR (l.pi_utm_campaign_c IS NOT NULL AND l.pi_utm_campaign_c != '')
      OR (l.pi_utm_source_c IS NOT NULL AND l.pi_utm_source_c != '')
      OR (l.pi_utm_medium_c IS NOT NULL AND l.pi_utm_medium_c != '')
    )
)
```

### CTE 2: `utm_attribution_ranked`
Ranks UTM sources by creation date (earliest first).

```sql
-- CTE: utm_attribution_ranked
-- Purpose: Rank UTM sources by earliest creation date
utm_attribution_ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY account_id
      ORDER BY source_created_date ASC
    ) AS attribution_rank
  FROM utm_attribution_base
)
```

### CTE 3: `account_utm_attribution` (Final)
Selects the earliest UTM source per account.

```sql
-- CTE: account_utm_attribution
-- Purpose: Final attribution - earliest object with UTM per account
account_utm_attribution AS (
  SELECT
    account_id,
    source_object_type AS attributed_from_object,
    source_object_id AS attributed_from_id,
    source_created_date AS attributed_object_created_date,
    utm_campaign AS attributed_utm_campaign,
    utm_source AS attributed_utm_source,
    utm_medium AS attributed_utm_medium,
    utm_content AS attributed_utm_content,
    utm_term AS attributed_utm_term
  FROM utm_attribution_ranked
  WHERE attribution_rank = 1
)
```

---

## Complete Reusable View Definition

```sql
-- View: account_utm_attribution
-- Description: UTM attribution for accounts based on earliest-first logic
-- Returns the UTM parameters from the earliest created object in the conversion chain

CREATE OR REPLACE VIEW `quiqup.views.account_utm_attribution` AS

WITH utm_attribution_base AS (
  -- Account's own UTM fields
  SELECT
    a.id AS account_id,
    'account' AS source_object_type,
    a.id AS source_object_id,
    a.created_date AS source_created_date,
    a.utm_campaign_c AS utm_campaign,
    a.UTM_Source_c AS utm_source,
    a.UTM_Medium_c AS utm_medium,
    a.UTM_Content_c AS utm_content,
    a.UTM_Term_c AS utm_term
  FROM `quiqup.salesforce_current.accounts` a
  WHERE a.is_deleted = FALSE
    AND (
      COALESCE(a.utm_campaign_c, '') != ''
      OR COALESCE(a.UTM_Source_c, '') != ''
      OR COALESCE(a.UTM_Medium_c, '') != ''
    )

  UNION ALL

  -- Opportunities linked to the account
  SELECT
    o.account_id,
    'opportunity' AS source_object_type,
    o.id AS source_object_id,
    o.created_date AS source_created_date,
    o.utm_campaign_c AS utm_campaign,
    o.utm_source_c AS utm_source,
    o.utm_medium_c AS utm_medium,
    o.utm_content_c AS utm_content,
    o.utm_term_c AS utm_term
  FROM `quiqup.salesforce_current.opportunities` o
  WHERE o.is_deleted = FALSE
    AND o.account_id IS NOT NULL
    AND (
      COALESCE(o.utm_campaign_c, '') != ''
      OR COALESCE(o.utm_source_c, '') != ''
      OR COALESCE(o.utm_medium_c, '') != ''
    )

  UNION ALL

  -- Leads that converted to this account
  SELECT
    l.converted_account_id AS account_id,
    'lead' AS source_object_type,
    l.id AS source_object_id,
    l.created_date AS source_created_date,
    COALESCE(NULLIF(l.utm_campaign_c, ''), l.pi_utm_campaign_c) AS utm_campaign,
    COALESCE(NULLIF(l.utm_source_c, ''), l.pi_utm_source_c) AS utm_source,
    COALESCE(NULLIF(l.utm_medium_c, ''), l.pi_utm_medium_c) AS utm_medium,
    l.utm_content_c AS utm_content,
    l.utm_term_c AS utm_term
  FROM `quiqup.salesforce_current.leads` l
  WHERE l.is_deleted = FALSE
    AND l.converted_account_id IS NOT NULL
    AND (
      COALESCE(l.utm_campaign_c, '') != ''
      OR COALESCE(l.utm_source_c, '') != ''
      OR COALESCE(l.utm_medium_c, '') != ''
      OR COALESCE(l.pi_utm_campaign_c, '') != ''
      OR COALESCE(l.pi_utm_source_c, '') != ''
      OR COALESCE(l.pi_utm_medium_c, '') != ''
    )
),

utm_attribution_ranked AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY account_id
      ORDER BY source_created_date ASC
    ) AS attribution_rank
  FROM utm_attribution_base
)

SELECT
  account_id,
  source_object_type AS attributed_from_object,
  source_object_id AS attributed_from_id,
  source_created_date AS attributed_object_created_date,
  utm_campaign AS attributed_utm_campaign,
  utm_source AS attributed_utm_source,
  utm_medium AS attributed_utm_medium,
  utm_content AS attributed_utm_content,
  utm_term AS attributed_utm_term
FROM utm_attribution_ranked
WHERE attribution_rank = 1;
```

---

## Usage Examples

### Example 1: Join attribution to accounts
```sql
SELECT
  a.id,
  a.name,
  a.created_date,
  attr.attributed_from_object,
  attr.attributed_utm_campaign,
  attr.attributed_utm_source,
  attr.attributed_utm_medium
FROM `quiqup.salesforce_current.accounts` a
LEFT JOIN `quiqup.views.account_utm_attribution` attr
  ON a.id = attr.account_id
WHERE a.is_deleted = FALSE
```

### Example 2: Attribution breakdown by source object
```sql
SELECT
  attributed_from_object,
  COUNT(*) AS account_count,
  COUNT(DISTINCT attributed_utm_campaign) AS unique_campaigns
FROM `quiqup.views.account_utm_attribution`
GROUP BY 1
ORDER BY 2 DESC
```

### Example 3: Campaign performance by attributed source
```sql
SELECT
  attr.attributed_utm_campaign,
  attr.attributed_utm_source,
  COUNT(DISTINCT a.id) AS accounts,
  COUNT(DISTINCT CASE WHEN o.is_won = TRUE THEN o.id END) AS won_opportunities
FROM `quiqup.salesforce_current.accounts` a
LEFT JOIN `quiqup.views.account_utm_attribution` attr ON a.id = attr.account_id
LEFT JOIN `quiqup.salesforce_current.opportunities` o ON a.id = o.account_id
WHERE a.is_deleted = FALSE
GROUP BY 1, 2
ORDER BY 3 DESC
```

---

## Edge Cases & Gotchas

### 1. Accounts without any UTM data
- ~69% of accounts have no UTM attribution (26,134 of 37,817)
- These are typically:
  - Manually created accounts
  - Imported accounts
  - Accounts created before UTM tracking

### 2. Parent Account UTM Inheritance
- Only ~166 child accounts have a parent with UTM while the child has no UTM
- **Decision**: Do NOT inherit UTM from parent by default (low impact, may cause incorrect attribution)
- If needed, extend the CTE to include parent account UTMs as a fallback source

### 3. Multiple Leads per Account
- Some accounts may have multiple converted leads
- The earliest lead (by `created_date`) wins attribution

### 4. UTM Field Casing Inconsistency
- Accounts use `UTM_Source_c` (title case)
- Leads/Opportunities use `utm_source_c` (lowercase)
- Always use exact field names from the schema

### 5. Empty String vs NULL
- Both `NULL` and `''` (empty string) should be treated as "no value"
- Use `COALESCE(field, '') != ''` or `NULLIF(field, '')` patterns

---

## Future Enhancements

1. **Multi-touch Attribution**: Track all touchpoints, not just first
2. **Parent Account Fallback**: Optional flag to inherit from parent if no direct UTM
3. **Time-decay Attribution**: Weight recent touchpoints higher
4. **Campaign Grouping**: Normalize campaign names into marketing channels

---

## Changelog

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Data Team | Initial version - earliest-first attribution logic |
| 2026-01-29 | Data Team | **Deployed** view to `quiqup.views.account_utm_attribution` |
