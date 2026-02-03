# Grandparent-Level Attribution Model

**Date:** 2026-01-29
**Analyst:** Claude (BigQuery Analyst Agent)
**Status:** Design Complete → Implementation Pending

---

## Executive Summary

This document defines a **grandparent-level attribution model** for analyzing marketing campaign ROI. The key insight is that revenue should be attributed at the **grandparent account level** (not individual business accounts) to avoid double-counting and properly measure customer lifetime value.

**Key decisions:**
1. **Counting unit:** 1 grandparent = 1 acquisition (not each business account)
2. **UTM attribution:** Earliest UTM from any Lead/Opportunity/Account in the hierarchy
3. **Revenue:** Sum invoices with deduplication to avoid inflating numbers
4. **SSUP exception:** Self-signup accounts are their own grandparents

---

## Problem Statement

The hypothesis to test: *"Most campaigns are producing clients who either never activate, or who will never become profitable for us."*

To test this, we need:
1. **Attribution:** Which campaign acquired each customer?
2. **Activation:** Did the customer place their first order?
3. **Revenue:** How much revenue did they generate?
4. **ROI:** Revenue vs. acquisition cost

**Challenge:** Enterprise customers have complex hierarchies where one grandparent can have 90+ business accounts, all sharing the same marketing attribution.

---

## Data Model: Lead → Opportunity → Account → Grandparent

### Conversion Chain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SALESFORCE CONVERSION CHAIN                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                  │
│   │    LEAD     │────▶│ OPPORTUNITY │────▶│   ACCOUNT   │                  │
│   │             │     │             │     │  (Business) │                  │
│   │ utm_campaign│     │ utm_campaign│     │ utm_campaign│                  │
│   │ created_date│     │ created_date│     │ created_date│                  │
│   └─────────────┘     └─────────────┘     └──────┬──────┘                  │
│                                                  │ parent_id               │
│                                                  ▼                         │
│                                           ┌─────────────┐                  │
│                                           │   PARENT    │                  │
│                                           │   ACCOUNT   │                  │
│                                           └──────┬──────┘                  │
│                                                  │ parent_id               │
│                                                  ▼                         │
│                                           ┌─────────────┐                  │
│                                           │ GRANDPARENT │                  │
│                                           │   ACCOUNT   │                  │
│                                           └─────────────┘                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Conversion Path Distribution

| Path | Records | Unique Accounts | Description |
|------|---------|-----------------|-------------|
| Lead → Opp → Account | 5,466 | 3,148 | Full conversion chain |
| Opp → Account (no lead) | 8,233 | 2,282 | Direct opportunity creation |
| Unconverted Leads | 29,330 | 0 | Leads not yet converted |
| Direct Accounts | 30,760 | 25,447 | Self-signup, manual, imported |

**Source:** `quiqup.views.accounts_with_opportunities_and_leads`

---

## UTM Attribution Logic

### Principle: Earliest UTM Wins

For each grandparent account, we find the **earliest created object** (Lead, Opportunity, or Account) that has UTM data.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         UTM ATTRIBUTION HIERARCHY                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   GRANDPARENT: "Matajer Amal company"                                       │
│   ─────────────────────────────────────────────────────────────────────     │
│                                                                             │
│   Business Account 1: "Beyond B - KSA - FF"                                 │
│   ├── Lead created: 2025-07-24 (utm_campaign: KSA-Fulfillment-EN) ◀── WIN  │
│   ├── Opportunity created: 2025-07-24                                       │
│   └── Account created: 2025-09-06                                           │
│                                                                             │
│   Business Account 2: (hypothetical future account)                         │
│   └── Account created: 2026-01-15 (utm_campaign: KSA-Services-EN)           │
│                                                                             │
│   ATTRIBUTION RESULT:                                                       │
│   • utm_campaign: KSA-Fulfillment-EN (from earliest lead)                   │
│   • acquisition_date: 2025-07-24                                            │
│   • Do NOT count as new acquisition in 2026                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Current View: `views.account_utm_attribution`

Already deployed. Provides earliest UTM per **Salesforce account** (business account level).

| Source Object | Accounts Attributed | Unique Campaigns |
|--------------|---------------------|------------------|
| Account (direct) | 10,946 | 65 |
| Lead (converted) | 739 | 57 |
| Opportunity | 10 | 5 |
| **Total** | **11,695** | — |

### New View Needed: `views.grandparent_utm_attribution`

Aggregates `account_utm_attribution` to grandparent level by taking the earliest UTM across all business accounts in the hierarchy.

---

## Revenue Attribution Logic

### The Double-Counting Problem

Enterprise customers like **M.h. alshaya co group** have complex invoice structures:
- 92 business accounts
- 85 accounts with `invoice_to_parent = TRUE` → invoice to 3 parent accounts
- 9 accounts with `invoice_to_parent = FALSE` → invoice to themselves

**Without deduplication:**
| Method | Invoices Counted | Revenue (AED) |
|--------|-----------------|---------------|
| ❌ Naive join (per business account) | 6,716 | 364.5M |
| ✅ Deduplicated (unique invoicing accounts) | 326 | 19.2M |

**The naive approach inflates revenue by 19x!**

### Deduplication Logic

```sql
-- CORRECT: Deduplicate by effective invoicing account
WITH unique_invoicing_accounts AS (
  SELECT DISTINCT
    tg.grandparent_account_id,
    CASE
      WHEN ia.invoice_to_parent = TRUE THEN ia.parent_account_id
      ELSE ia.account_id
    END AS effective_invoicing_account
  FROM views.true_grandparent_account tg
  JOIN invoicer_current.accounts ia
    ON ia.salesforce_id = tg.business_account_id
)
SELECT
  grandparent_account_id,
  COUNT(DISTINCT i.id) as invoice_count,
  SUM(i.total_amount) as total_revenue
FROM unique_invoicing_accounts u
JOIN invoicer_current.invoices i
  ON i.account_id = u.effective_invoicing_account
  AND i.record_deleted = FALSE
  AND i.deleted_at IS NULL
  AND i.state = 'paid'
GROUP BY 1
```

---

## SSUP Exception

### Problem: Fake Parent Account

The **SSUP Parent Account** (`0010800003I4PcsAAF`) is a placeholder used to group all self-signup clients. It has **21,563 children**.

If we treated this as a real grandparent, all self-signups would be counted as ONE customer acquisition.

### Solution: Already Handled

The `views.true_grandparent_account` view already handles this correctly:
- Each SSUP child is mapped to **itself** as the grandparent
- They are NOT rolled up to the fake SSUP parent

**Verification:**
```sql
SELECT grandparent_account_id, COUNT(*) as business_accounts
FROM views.true_grandparent_account
WHERE business_account_id IN (
  SELECT id FROM salesforce_current.accounts WHERE parent_id = '0010800003I4PcsAAF'
)
GROUP BY 1
-- Result: Each returns business_accounts = 1 (not rolled up)
```

---

## Existing Views Used

| View | Purpose | Status |
|------|---------|--------|
| `views.true_grandparent_account` | Maps business account → grandparent | ✅ Exists |
| `views.grandparent_account_created_date_and_first_order_delivered` | First order at grandparent level | ✅ Exists |
| `views.account_utm_attribution` | Earliest UTM per business account | ✅ Built today |
| `views.accounts_with_opportunities_and_leads` | Full Lead→Opp→Account chain with grandparent | ✅ Exists |

---

## New Views to Build

### 1. `views.grandparent_utm_attribution`

**Purpose:** Earliest UTM attribution at grandparent level

**Grain:** 1 row per grandparent account

**Key columns:**
- `grandparent_account_id` (STRING)
- `grandparent_account_name` (STRING)
- `attributed_utm_campaign` (STRING)
- `attributed_utm_source` (STRING)
- `attributed_utm_medium` (STRING)
- `acquisition_date` (DATE) — earliest created date with UTM
- `attributed_from_business_account_id` (STRING)
- `attributed_from_object` (STRING) — lead/opportunity/account

### 2. `views.grandparent_revenue`

**Purpose:** Deduplicated invoice revenue per grandparent

**Grain:** 1 row per grandparent account

**Key columns:**
- `grandparent_account_id` (STRING)
- `total_revenue_aed` (FLOAT)
- `invoice_count` (INT64)
- `unique_invoicing_accounts` (INT64)
- `first_invoice_date` (DATE)
- `last_invoice_date` (DATE)

### 3. Extended H2 View (or new `views.marketing_funnel_grandparent_monthly`)

**Purpose:** Monthly funnel metrics at grandparent level

**Grain:** 1 row per month

**New columns to add:**
- `grandparents_acquired` — distinct grandparents with UTM attribution that month
- `grandparents_activated` — distinct grandparents with first order that month
- `grandparent_ltv` — cumulative revenue for cohort
- `grandparent_cac` — spend / acquired grandparents

---

## Final Funnel Definition

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MARKETING FUNNEL (Grandparent Level)                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌───────────┐   ┌───────────┐   ┌───────────┐   ┌───────────┐            │
│   │ Acquired  │──▶│ Activated │──▶│ Retained  │──▶│Profitable │            │
│   │           │   │           │   │           │   │           │            │
│   │ Has UTM   │   │ 1st order │   │ 10+ orders│   │ LTV > CAC │            │
│   └───────────┘   └───────────┘   └───────────┘   └───────────┘            │
│                                                                             │
│   Metrics per grandparent:                                                  │
│   ─────────────────────────────────────────────────────────────────────     │
│   • utm_campaign: Earliest UTM from any account in hierarchy                │
│   • acquisition_date: MIN(created_date) across hierarchy                    │
│   • activation_date: First order delivered (from grandparent view)          │
│   • total_orders: SUM across all business accounts                          │
│   • total_revenue: SUM(invoices) with deduplication                         │
│   • ltv: total_revenue (lifetime)                                           │
│   • cac: Attributed spend / acquired grandparents                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Example: Complete Attribution for One Grandparent

**Grandparent:** M.h. alshaya co group (`0011p00002DhDkLAAV`)

| Metric | Value |
|--------|-------|
| Business Accounts | 92 |
| Earliest Account Created | 2019-10-27 |
| First Order Delivered | 2021-01-01 |
| Activation Time | ~15 months |
| Total Orders (grandparent) | 7,589+ |
| Unique Invoicing Accounts | 12 |
| Total Revenue (deduplicated) | 19.2M AED |
| UTM Attribution | (check earliest business account with UTM) |

---

## Implementation Plan

1. ✅ **Document model** (this file)
2. 🔨 **Build `grandparent_utm_attribution`** view
3. 🔨 **Build `grandparent_revenue`** view
4. 🔨 **Extend H2** with grandparent metrics
5. 📊 **Run profitability analysis** by campaign

---

## Caveats & Limitations

1. **UTM coverage:** Only 31% of accounts have UTM attribution
2. **Historical data:** Older accounts may have been created before UTM tracking
3. **SSUP accounts:** Treated as individual grandparents (correct behavior)
4. **Invoice timing:** Revenue is attributed to invoice date, not acquisition date
5. **Currency:** All revenue is in AED

---

*Generated by BigQuery Analyst Agent | quiqup-workspace*
