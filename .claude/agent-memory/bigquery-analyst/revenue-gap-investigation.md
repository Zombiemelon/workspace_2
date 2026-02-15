# Master Revenue: BQ vs CSV Gap Investigation (Feb 2026)

## Summary

BQ view `quiqup.master_revenue.v_master_revenue_database` is 1.3% lower than source CSV.
- 2024: BQ 33,028,372 vs CSV 33,458,954 = -430,582 AED (-1.29%)
- 2025: BQ 46,117,156 vs CSV 46,744,074 = -626,918 AED (-1.34%)

## 3-Layer Decomposition (verified to exact AED)

```
CSV  ->  Invoicer (invoice-level)  ->  Invoicer (line-level)  ->  BQ View
         Layer 1: -864,889              Layer 2: -195,046          Layer 3: +2,435
         (external revenue)             (formula difference)       (rounding)
```

### Layer 1: Revenue outside invoicer (864,889 AED, 82% of gap)

CSV includes manually-sourced revenue from systems beyond the invoicer:

| SubType missing from BQ | 2024 | 2025 | Total |
|------------------------|------|------|-------|
| 3c.Naqel | 0 | 852,836 | 852,836 |
| 5a.Fulfilment (KSA) | 0 | 201,050 | 201,050 |
| 6b.Product Registration | 0 | 209,783 | 209,783 |
| 6a.IoR/SoR | 0 | 30,958 | 30,958 |
| 5c.Transaction Fees (KSA) | 0 | 543 | 543 |
| **TOTAL missing subtypes** | **0** | **1,295,170** | **1,295,170** |

But this is partially offset by BQ having MORE cross-border revenue from NULL-carrier defaulting to Aramex (1,090,821 AED across both years).

2024 net: +115,625 (CSV has more). 2025 net: +749,264 (CSV has more).

### Layer 2: Invoice vs line formula (195,046 AED, 18% of gap)

BQ uses `SUM(amount * COALESCE(quantity, 1))` excluding `cod` lines.
CSV uses `total_amount - tax_amount` at invoice level.

These differ because:
- Some invoices have charges at invoice level not broken into lines
- 53 globalEcommerce invoices in 2024 contribute 263K of gap (zero cod lines)
- Account 470629 (Sharaf DG, `cash_charge_percentage=0.025`) contributes 147K
- Other accounts with 0% cash charge also have gaps (unknown mechanism)

2024: Lines are 315,695 lower than invoices.
2025: Lines are 120,649 HIGHER than invoices (direction flips!).

### Layer 3: Rounding (-2,435 AED, negligible)

### Cross-Border Carrier Misclassification

| Carrier | CSV Total | BQ Total | Difference |
|---------|-----------|----------|------------|
| Aramex | 4,410,464 | 7,767,100 | +3,356,636 |
| DHL | 2,623,720 | 905,494 | -1,718,226 |
| Naqel | 852,836 | 0 | -852,836 |
| **CB Total** | **7,887,020** | **8,672,595** | **+785,575** |

Root cause: 350 cross-border invoices (billing_type IS NULL) have `carrier_account_c = NULL`.
BQ view defaults these to `3a.Aramex`. CSV assigns carriers correctly (manually).

### GP Hierarchy Differences (net ~0)

- 2,731 GP IDs in CSV not in BQ: 99% are SSUP (3.92M AED) -- structural, nets to ~32K
- 23 non-SSUP CSV-only GPs (438K AED) use manual GP grouping (e.g., DCC Trading -> Apparel Group in BQ)
- 3 BQ-only GPs (424K, mostly NULL_GP = unmapped accounts)

## Worst Months

| Month | Gap (AED) | Gap % | Primary Driver |
|-------|-----------|-------|----------------|
| 2025-12 | -375,810 | -7.9% | Missing Naqel (237K) + Per order shortfall (104K) |
| 2024-09 | -242,063 | -9.0% | La Purete missing CB invoice (179K) + DHL reclassification |
| 2024-10 | +171,557 | +6.2% | Aramex over-count from NULL carrier (283K offset) |
| 2025-10 | -98,860 | -2.3% | Missing Naqel (223K) + Product Reg (80K) |

## Key GP-Level Findings

- **La Purete Group**: CSV has 178,785 AED cross-border invoice in Sep 2024 that does NOT exist in invoicer at all (manually added)
- **Sharaf DG**: CSV uses invoice-level totals; BQ lines are ~48% lower (cash_charge at invoice level)
- **DCC Trading**: CSV groups manually; BQ resolves children to Apparel Group, Landmark, etc.

## Recommendations

1. Add Naqel/KSA/IoR/ProdReg data sources to invoicer or create override table
2. Fix NULL carrier_account_c classification (350 invoices -> "Unknown" not "Aramex")
3. Investigate 53 invoices with invoice > lines gap (invoice-level charges without lines)
4. Document the ~1.3% gap as structural/expected until external sources are integrated
