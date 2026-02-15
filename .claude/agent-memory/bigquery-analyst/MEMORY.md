# BigQuery Analyst Agent Memory

## Definitions (READ FIRST)

All business definitions live in [definitions.md](definitions.md). Every definition maps to a specific BigQuery view/table. Never hardcode classification logic — always JOIN to the definition view.

Key definitions quick-reference:
- **Paid vs Organic** -> `views.definition_paid_organic_channel` (NOT paid = Organic)
- **Inbound vs Outbound** -> `views.definition_lead_source` (source_group)
- **Opp Conversion** -> `views.opportunities_convert_minus_2months` (parent account existence)
- **New vs Existing Client** -> `client_type_classification` on opp view (LEAST of child/GP created_date)
- **Net Revenue** -> `invoicer_current.invoices` (start_date, paid/overdue, total - tax)
- **Grandparent Resolution** -> `views.true_grandparent_account`
- **Activation** -> first_delivered_order_date IS NOT NULL (2030-01-01 = placeholder)

## Topic Files

| File | Contents |
|------|----------|
| [definitions.md](definitions.md) | All business definitions with source views, rules, join patterns |
| [schema-patterns.md](schema-patterns.md) | Account hierarchy, SSUP, join gotchas, currency, date fields |
| [opp-conversion-notes.md](opp-conversion-notes.md) | View logic, dashboard filter mismatch, validation counts |
| [revenue-benchmarks.md](revenue-benchmarks.md) | 2025 totals, concentration, fulfilment segment, cross-checks |
| [data-quality.md](data-quality.md) | NULL rates, SF ID resolution, GA4 gaps, file offsets |

## STRICT RULES

- **NEVER delete or drop anything (tables, views, cards, dashboards, records) without the user's explicit permission.** Always ask first before any destructive operation.

## Critical Reminders

- SSUP catch-all: exclude from top-client rankings (`NOT LIKE '%SSUP%'`)
- `stage_name` is mutable — opp conversion snapshots drift over time
- `grandparent_utm_attribution` only has activated GPs — activation rate from it alone = always 100%
- Without invoice-to-parent dedup, revenue inflates ~19x
- Dashboard "Inbound Leads" filter != `definition_lead_source.source_group` (undercounts by ~88 opps)
- Google Ads dimension tables: MUST filter `_DATA_DATE = _LATEST_DATE`

## Invoicer Revenue Join (CRITICAL)

- `invoicer_current.accounts.id` = STRING (Salesforce ID, e.g., `001P4000009C0toIAC`)
- `invoicer_current.accounts.account_id` = INT64 (invoicer internal ID, e.g., `459199`)
- `invoicer_current.invoices.account_id` = INT64
- **Invoice join MUST use `accounts.account_id` (INT64), NOT `accounts.id` (STRING)**
- Column for account name is `account_name`, not `name`
- For invoice-to-parent dedup: `CASE WHEN ia.invoice_to_parent THEN ia.parent_account_id ELSE ia.account_id END`

## GP Activation Definition (Bruno Reference)

- Bruno's master list uses: `go_live_date_c` primary, `first_order_delivered` fallback
- Does NOT use `child_created_date` (too early; captures SF account setup, not business activation)
- `child_created_date` generates ~2x more GPs (232 vs 110) and dates 1-4 months earlier
- 2 GPs in ref (Middle Kingdom, MooBoo) activated pre-2025 but have 2025 revenue; no 2025 signal
- See: `projects/02_2026_data_cleanup/bruno_master_revenue/comparison_analysis.md`

## BDM Assignment Gotchas

- Reference uses "Former BDM / No BDM" for BDMs who left the company
- Our query picks earliest opp `owner_full_name_c`, which may differ from current/assigned BDM
- Opp owners change over time; ref may use current owner or manually cleaned assignment

## Pricing Models (salesforce_current.pricing_models)

- **Join to accounts:** `accounts.Pricing_Model_c = pricing_models.id`
- **Key columns:** `name` (APM-XXXXX), `name_c` (human name), `pricing_type_c`, `active_from_c`, `next_day_from_emirates_c`, `same_day_from_emirates_c`
- **Pricing_Model_c on accounts is CURRENT model** -- historical model changes are not tracked; all invoices attribute to current model
- **SSUP parent account:** `0010800003I4PcsAAF` -- shared pricing models applied to thousands of child accounts
- **Key SSUP models (2025):**
  - APM-16660: SSUP Distance Based, ND=22 AED (11,307 accounts, standard)
  - APM-17103: SSUP Distance Based (AED 18), ND=18 AED (223 accounts, Aug 2025 price reduction)
  - APM-16637: Individual Distance Based, ND=35 AED (6,761 accounts, B2C)
  - APM-16948: SSUP Temp Controlled, ND=24 AED (13 accounts, high-value)
  - APM-14068: Generic 2, ND=22 AED (3,629 accounts, legacy ecommerce)
- **Account source field:** `accounts.account_source` contains lead source (e.g., "Inbound: Self-signup", "Inbound: Contact form", "Outbound: Own research")
- **Revenue join path:** pricing_models -> SF accounts (Pricing_Model_c) -> invoicer accounts (salesforce_id) -> invoices (account_id INT64)
- **Historical pricing attribution (preferred):** invoices.account_pricing_id -> invoicer_current.account_pricing.id -> account_pricing.salesforce_id -> salesforce_current.pricing_models.id
- **Aug 2025 self-signup price cut nuance:** `APM-17152` (active_from 2025-08-31, ND 24->18) exists in Salesforce pricing models but had 0 rows in `invoicer_current.account_pricing` during Aug/Sep 2025; realized revenue mapped to `APM-17103` for AED 18 cohort
- **Aug 2025 pricing experiment cohort (final, 3-way sensitivity):**
  - Window: Aug 11-31, 2025 (first reduced account appeared Aug 11)
  - Standard (APM-16660, SF: a2KP4000005nqc5MAA): 136 accounts, 24 activated (17.6%)
  - Reduced (APM-17103, SF: a2KP4000007umMAMAY): 112 accounts (original), 110 excl. both outliers
  - **Outliers (both Reduced):** Throwmenot (SF: 001P400000e3s6cIAA, 8,718 AED), Ray Beauty (SF: 001P400000dOsLxIAK, 9,099 AED) -- combined 70.7% of Reduced total
  - **Median revenue robust:** Std 113 AED vs Red 206 AED (1.82x) -- unchanged across all exclusion scenarios
  - **Total revenue flips:** Red wins 2.70x with outliers, Standard wins (9,326 vs 7,387) with both excluded
  - **Per-invoice revenue:** With outliers removed, Reduced median drops to 36 AED (vs Standard 52 AED). Lower price -> lower per-order but more orders.
  - **Engagement robust:** Median invoices 5 vs 3, median months 4 vs 2, stable across all scenarios
  - **Retention robust:** M5 gap +17.5pp even after both exclusions; churn 26% vs 46%
  - **Standard also concentrated:** Ivy and Silk = 44.6% of Standard total (4,156 AED). Not symmetric to exclude only from Reduced.
  - No statistical significance at n=23-24/arm; need ~500+/arm for powered test
  - **Churn-by-tier analysis (Feb 2026):**
    - Micro (1-2 inv): 100% churn in BOTH cohorts -- price-insensitive, structural tourists
    - Light (3-5 inv): identical 42.9% churn in both -- price not the lever
    - Regular (6-10 inv): Standard 33.3% vs Reduced 11.1% churn -- price matters here
    - Power (11+ inv): Standard produced ZERO; Reduced produced 3 (all active, avg 3,988 AED)
    - High price creates a "ceiling effect" preventing power user emergence, not churning them
    - Multi-order-per-day behavior essentially nonexistent in SSUP (1 account total)
    - `client_type_c` is NULL for all SSUP accounts; filter by pricing_model_c + date instead

## Master Revenue Database (quiqup.master_revenue)

New dataset created Feb 2026 replicating the manual `master_revenue_database.csv` as automated BigQuery views.

**Key learnings:**
- **CDC dedup required**: `invoicer_current.accounts` has Debezium CDC duplicates (up to 38x per account_id). MUST deduplicate with `QUALIFY ROW_NUMBER() OVER (PARTITION BY account_id ORDER BY debezium_ts_ms DESC) = 1`
- **Line revenue formula**: `amount * COALESCE(quantity, 1)` — NOT just `SUM(amount)`. Reconciles perfectly with `total_amount - tax_amount` when excluding `cod` lines.
- **Exclude `cod` line type**: These are COD cash collection amounts (always negative, -35M in 2022). NOT revenue. Excluding them reconciles line-level with invoice-level perfectly.
- **Fulfilment split**: `export_pnp` → 2b.International P&P. ALL other lines (including COD fees, storage, inbound) → 2a.Core Domestic. COD fees only become Type 4 on Last Mile invoices.
- **Cross-border carrier**: Primary from `carrier_account_c` (ARAMEX_PROD/DHL_PROD). Override table `definition_cb_carrier` for Naqel. ~11 accounts have NULL carrier.
- **BDM view is self-sufficient**: Replicates earliest-opp-owner logic from `salesforce_current.opportunities` directly. Does NOT reference `views.opportunities_convert_minus_2months`.
- **Geography**: `salesforce_current.accounts.Region_c = 'SA'` → KSA. Everything else → UAE.
- **Validation**: Jan 2025 = 0.01% revenue match. 2024-2025 = ~1.3% match. Full 2022-2025 = ~1.7% match.
- **1.3% gap root cause (Feb 2026 investigation):** See [revenue-gap-investigation.md](revenue-gap-investigation.md)
  - Layer 1: CSV has 865K AED revenue not in invoicer (Naqel 853K, KSA 202K, IoR/SoR+ProdReg 241K, partially offset by BQ NULL-carrier defaults)
  - Layer 2: Invoice-level vs line-level formula gap (195K net; invoice totals include charges not in lines, e.g., COD fees at invoice level)
  - Layer 3: Rounding/join (-2.4K, negligible)
  - Cross-border carrier_account_c=NULL defaults to Aramex in BQ (350 invoices, 1.09M AED misclassified)
  - SSUP GP structure differs but nets to ~0 (CSV uses individual GPs in 2025, BQ uses single SSUP GP)
  - CSV GP hierarchy is manually defined; BQ uses SF parent hierarchy (DCC Trading -> Apparel Group etc.)
- **Line vs invoice formula does NOT perfectly reconcile**: Despite earlier notes saying excl-cod reconciles perfectly, 53 globalEcommerce invoices in 2024 have invoice > lines by 263K with zero cod lines. Cash collection fees and other invoice-level adjustments exist without line representation.
- **Monthly gap is NOT uniform (Feb 2026 analysis):** Swings from -3.09% (Jul 2024) to +2.13% (Nov 2025). 2024 net = -319K (invoice > lines), 2025 net = +117K (lines > invoice due to credits). Two mechanisms: (a) invoice-level charges without lines (globalEcommerce COD fees), (b) invoice-level credits reducing total below lines (large fulfilment accounts). Account 471053 is a repeat outlier in both directions. See `projects/02_2026_data_cleanup/insights/monthly_discrepancy_analysis.md`

Full documentation: `quiqup-workspace/knowledge_base/master_revenue_database.md`
SQL files: `projects/02_2026_data_cleanup/master_revenue_views/01-07*.sql`

## Export (Cross-Border) Revenue (CRITICAL)

- **Export orders are NOT in invoice_lines per-order.** Zero export orders in `invoice_lines.order_id` joins to `client_orders`.
- Export revenue is billed via `invoice_lines.type = 'export_pnp'` as account-level lump sums (no order_id).
- `export_pnp` lines: `amount` = per-unit rate (3-8 AED), `quantity` = number of export units billed.
- Standard rate: 5 AED (`international_order_delivery_fee` in `account_pricing` type=`globalEcommerce`).
- Realized weighted avg: **3.70 AED/unit** (high-volume accounts get 3.00-3.50 AED).
- Total billed: 85,017 units, 314,350 AED across 108 invoicer accounts (as of Feb 2026).
- Only ~2 of 117 qualified CB accounts (5+ export orders) have direct `export_pnp` billing. Most accounts' export billing may be consolidated at parent level or billed separately.
- Cross-border account filter: `salesforce_current.accounts.cross_border_terms_signed_c IS NOT NULL AND != ''`
- Export order filter: `bi_reporting.client_orders.service_kind = 'Export'`, `state != 'cancelled'`
- See also: [schema-patterns.md](schema-patterns.md) for account hierarchy gotchas
