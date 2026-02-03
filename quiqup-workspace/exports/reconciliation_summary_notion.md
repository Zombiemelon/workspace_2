# Invoice Reconciliation Summary (Jan-Aug 2025)

**Analysis Date:** 2026-02-01
**Data Sources:** Xero CSV vs BigQuery `invoicer_current.invoices`

---

## In CSV but NOT in BigQuery (38 invoices, AED 54,954)

### Pattern 1: Split Invoices (16 invoices, AED 20,139)
Xero splits invoices by fee type (`-PerOrder`, `-RouteBased`); BigQuery has single consolidated invoice.

| Invoice | Amount (AED) | Month | Root Cause |
| --- | --- | --- | --- |
| INV-093668-PerOrder | 25.00 | Feb | Split suffix - base invoice exists in BQ as 6,746.88 |
| INV-093668-RouteBased | 6,720.00 | Feb | Split suffix - base invoice exists in BQ as 6,746.88 |
| INV-094827-PerOrder | 50.00 | Feb | Split suffix - base invoice exists in BQ as 5,791.51 |
| INV-094827-RouteBased | 5,740.00 | Feb | Split suffix - base invoice exists in BQ as 5,791.51 |
| INV-094336-PerOrder | 20.00 | Feb | Split suffix - base invoice exists in BQ as 560.00 |
| INV-094336-RouteBased | 540.00 | Feb | Split suffix - base invoice exists in BQ as 560.00 |
| INV-095007-PerOrder | 20.00 | Feb | Split suffix - base invoice exists in BQ as 384.00 |
| INV-095007-RouteBased | 364.00 | Feb | Split suffix - base invoice exists in BQ as 384.00 |
| INV-092329-PerOrder | 40.00 | Jan | Split suffix - base invoice exists in BQ as 220.00 |
| INV-092329-RouteBased | 180.00 | Jan | Split suffix - base invoice exists in BQ as 220.00 |
| INV-093158-PerOrder | 80.00 | Jan | Split suffix - base invoice exists in BQ as 260.00 |
| INV-093158-RouteBased | 180.00 | Jan | Split suffix - base invoice exists in BQ as 260.00 |
| INV-096095-PerOrder | 80.00 | Mar | Split suffix - base invoice exists in BQ as 620.00 |
| INV-096095-RouteBased | 540.00 | Mar | Split suffix - base invoice exists in BQ as 620.00 |
| INV-097122-PerOrder | 25.00 | Mar | Split suffix - base invoice exists in BQ as 3,665.38 |
| INV-097122-RouteBased | 3,640.00 | Mar | Split suffix - base invoice exists in BQ as 3,665.38 |
| INV-098698-PerOrder | 40.00 | Apr | Split suffix - base invoice exists in BQ as 224.00 |
| INV-098698-RouteBased | 184.00 | Apr | Split suffix - base invoice exists in BQ as 224.00 |

### Pattern 2: Legacy/External Invoices (5 invoices, AED 35,130)
Manual entries with 4-digit invoice numbers not from invoicer system.

| Invoice | Amount (AED) | Month | Root Cause |
| --- | --- | --- | --- |
| INV-0466 | 3,708.00 | Jan | So post - Storage (external system) |
| INV-0473 | 2,095.00 | Feb | So post - Storage (external system) |
| INV-0485 | 3,750.00 | Apr | So post - Bubble Pouch (external system) |
| INV-0486 | 1,047.00 | Mar | So post - Storage (external system) |
| INV-0487 | 28,230.00 | Mar | SHIPSY DMCC compensation (manual entry) |

### Pattern 3: Credit Notes (2 invoices, AED 61)

| Invoice | Amount (AED) | Month | Root Cause |
| --- | --- | --- | --- |
| CN-49358 Cr. Note | 51.00 | Apr | Credit note - tracked separately in BQ |
| CN-51254 Cr. Note | 10.00 | Jun | Credit note - tracked separately in BQ |

### Pattern 4: Stripe Fees (1 invoice, AED -6,250)

| Invoice | Amount (AED) | Month | Root Cause |
| --- | --- | --- | --- |
| ZTV6H2W5-2025-01 | -6,250.00 | Jan | Stripe processing fees (external system) |

### Pattern 5: Other (8 invoices, AED 3,574)

| Invoice | Amount (AED) | Month | Root Cause |
| --- | --- | --- | --- |
| INV-099475 | 124.00 | Apr | International Returns - not synced |
| INV-108509 | 35.00 | Aug | Not synced to BigQuery |
| INV-110314 | 944.00 | Aug | Not synced to BigQuery |
| INV-110665 | 408.00 | Aug | Not synced to BigQuery |
| INV-110666 | 119.00 | Aug | Not synced to BigQuery |
| INV-110668 | 1,850.00 | Aug | Not synced to BigQuery |
| INV-095684 | 75.00 | Feb | Not synced to BigQuery |
| INV-095736 | 20.00 | Feb | Not synced to BigQuery |
| INV-095763 | 20.00 | Feb | Not synced to BigQuery |
| INV-106909 | 40.00 | Jul | International Returns - not synced |
| INV-104263 | 86.00 | Jun | International Returns - not synced |
| INV-101895 | 124.00 | May | International Returns - not synced |

---

## In BigQuery but NOT in CSV (54 invoices, AED 58,199)

### Pattern 1: Debit Notes (18 invoices, AED 47,677)
Adjustments/corrections tracked in BigQuery but not exported to Xero CSV.

| Invoice | Amount (AED) | Month | State | Root Cause |
| --- | --- | --- | --- | --- |
| INV-105528 Dr. Note | 34,443.49 | Jul | paid | Debit note (adjustment) |
| INV-094615 Dr. note | 1,582.00 | Feb | paid | Debit note (adjustment) |
| INV-092422 Dr. note | 1,837.50 | Jan | paid | Debit note (adjustment) |
| INV-092409 Dr. note | 888.00 | Jan | paid | Debit note (adjustment) |
| INV-095033 Dr. note | 5,866.00 | Mar | paid | Debit note (adjustment) |
| INV-100701 Dr. note | 710.00 | May | paid | Debit note (adjustment) |
| INV-105677 Dr. Note | 660.00 | Jul | paid | Debit note (adjustment) |
| INV-109093 Dr. Note | 401.10 | Aug | paid | Debit note (adjustment) |
| INV-091419 Dr. note | 409.00 | Jan | paid | Debit note (adjustment) |
| INV-106823 Dr. Note | 390.00 | Jul | paid | Debit note (adjustment) |
| INV-103094 Dr. note | 213.00 | Jun | paid | Debit note (adjustment) |
| INV-095773 Dr. Note | 198.00 | Mar | paid | Debit note (adjustment) |
| INV-105539 Dr. Note | 198.90 | Jul | paid | Debit note (adjustment) |
| INV-105537 Dr. Note | 192.00 | Jul | paid | Debit note (adjustment) |
| INV-100420 Dr. note | 189.00 | Apr | paid | Debit note (adjustment) |
| INV-100421 Dr. note | 159.00 | Apr | paid | Debit note (adjustment) |
| INV-105538 Dr. Note | 143.76 | Jul | paid | Debit note (adjustment) |
| INV-099286 Dr. note | 118.00 | Apr | paid | Debit note (adjustment) |
| INV-101682 Dr. note | 100.00 | May | paid | Debit note (adjustment) |
| INV-108093 Dr. Note | 70.13 | Aug | paid | Debit note (adjustment) |
| INV-105540 Dr. Note | 36.00 | Jul | paid | Debit note (adjustment) |
| INV-093589 Dr. note | 25.00 | Feb | paid | Debit note (adjustment) |

### Pattern 2: DRAFT Prefix Invoices (8 invoices, AED 0)
Invoices that retained DRAFT prefix but were marked as paid (likely system issue).

| Invoice | Amount (AED) | Month | State | Root Cause |
| --- | --- | --- | --- | --- |
| DRAFT-INV-094439 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-094440 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-094441 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-094442 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-094444 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-094551 | 0.00 | Feb | paid | Zero-value placeholder |
| DRAFT-INV-110207 | 0.00 | Aug | paid | Zero-value placeholder |

### Pattern 3: Zero-Amount Invoices (10 invoices, AED 0)
Placeholder or cancelled invoices with zero amount.

| Invoice | Amount (AED) | Month | State | Root Cause |
| --- | --- | --- | --- | --- |
| INV-100503 | 0.00 | Apr | paid | Zero-value placeholder |
| INV-100507 | 0.00 | Apr | paid | Zero-value placeholder |
| INV-110284 | 0.00 | Aug | paid | Zero-value placeholder |
| INV-104537 | 0.00 | Jun | paid | Zero-value placeholder |
| INV-105464 | 0.00 | Jun | paid | Zero-value placeholder |
| INV-098248 | 0.00 | Mar | paid | Zero-value placeholder |
| INV-102927 | 0.00 | May | paid | Zero-value placeholder |
| INV-105849 | 0.00 | Jul | paid | Zero-value placeholder |
| INV-107766 | 0.00 | Jul | paid | Zero-value placeholder |
| INV-108020 | 0.00 | Jul | paid | Zero-value placeholder |

### Pattern 4: Consolidated Base Invoices (6 invoices, AED 2,660)
Base invoice exists in BQ while CSV has split versions (`-PerOrder`, `-RouteBased`).

| Invoice | Amount (AED) | Month | State | Root Cause |
| --- | --- | --- | --- | --- |
| INV-092329 | 220.00 | Jan | paid | Base invoice - CSV has split versions |
| INV-093158 | 260.00 | Jan | paid | Base invoice - CSV has split versions |
| INV-094336 | 560.00 | Feb | paid | Base invoice - CSV has split versions |
| INV-095007 | 384.00 | Feb | paid | Base invoice - CSV has split versions |
| INV-096095 | 620.00 | Mar | paid | Base invoice - CSV has split versions |
| INV-098698 | 224.00 | Apr | paid | Base invoice - CSV has split versions |

### Pattern 5: Other (12 invoices, AED 7,862)

| Invoice | Amount (AED) | Month | State | Root Cause |
| --- | --- | --- | --- | --- |
| INV-108216 | 5,329.76 | Aug | overdue | Multi-month invoice |
| INV-101683 | 1,227.10 | Apr | paid | Not in CSV export |
| INV-091553 | 372.00 | Jan | paid | Not in CSV export |
| INV-103095 | 100.00 | Jun | paid | Not in CSV export |
| INV-098029 | 10.40 | Feb | paid | Not in CSV export |
| INV-098052 | 19.00 | Mar | paid | Not in CSV export |
| INV-098086 | 10.00 | Mar | paid | Not in CSV export |
| INV-098144 | 14.00 | Mar | paid | Not in CSV export |
| INV-107831 | 19.00 | Jul | paid | Not in CSV export |

---

## Value Discrepancies >10 AED (4 invoices, AED 16,303)

| Invoice | BigQuery (AED) | CSV (AED) | Difference | Month | Root Cause |
| --- | --- | --- | --- | --- | --- |
| INV-093668 | 6,746.88 | 2.00 | +6,744.88 | Feb | Split in CSV (-PerOrder: 25, -RouteBased: 6,720) |
| INV-094827 | 5,791.51 | 2.00 | +5,789.51 | Feb | Split in CSV (-PerOrder: 50, -RouteBased: 5,740) |
| INV-097122 | 3,665.38 | 0.00 | +3,665.38 | Mar | Split in CSV (-PerOrder: 25, -RouteBased: 3,640) |
| INV-094363 | 983.00 | 880.00 | +103.00 | Feb | **Genuine discrepancy - needs investigation** |

---

## Net Impact Summary

| Category | Count | Amount (AED) |
| --- | --- | --- |
| Missing in BigQuery | 38 | +54,954 |
| Missing in CSV | 54 | -58,199 |
| Value Discrepancies (net) | 4 | +16,303 |
| **Net Difference** | - | **+19,074** |

---

## Root Cause Breakdown

| Root Cause | Invoices | Net Impact (AED) |
| --- | --- | --- |
| Split invoice pattern (`-PerOrder`/`-RouteBased`) | 22 | ~0 (balanced) |
| Debit notes (Dr. Note) | 18 | -47,677 |
| Legacy/External systems (So post, Shipsy, Stripe) | 6 | +28,880 |
| Zero-value placeholders | 18 | 0 |
| Credit notes | 2 | +61 |
| International Returns not synced | 4 | +374 |
| Other not synced | 14 | ~6,000 |

---

## Recommendations

1. **Split Invoice Pattern**: Consider standardizing invoice format between Xero and BigQuery
2. **Debit Notes**: Add debit notes to CSV export or document exclusion
3. **Legacy Systems**: Document that So post/Shipsy/Stripe are tracked outside invoicer
4. **Zero-Value Invoices**: Clean up DRAFT-prefixed and zero-amount records in BigQuery
5. **INV-094363**: Investigate 103 AED discrepancy (only genuine mismatch found)

---

*Generated: 2026-02-01*
