# Revenue Benchmarks (Validated)

Numbers validated against Finance reconciliation and cross-checks. Update after each major analysis.

## 2025 Full Year

| Metric | Value | Source |
|--------|-------|--------|
| Total net revenue (paid+overdue) | AED 45,993,284 | `invoicer_current.invoices`, start_date in 2025 |
| Invoice count | 28,801 | Same query |
| Billing accounts | 3,807 | COUNT DISTINCT account_id |
| Avg invoice value | ~AED 1,597 | total / count |

## Revenue Concentration (2025)

- Top 15 business groups = 49.7% of total revenue
- #1 client: M.H. Alshaya Group = 12.7% of total
- SSUP (self-signup catch-all) = ~8.5% — exclude from top-client rankings

## Fulfilment Segment (2025)

- Filter: `Service_Offering_c IN ('Fulfillment', 'Fulfillment + Last Mile')`
- Total fulfilment revenue: AED 11,167,340 (n=1,663 invoices) = 24.3% of company total
- Top client: La Purete Group (AED 2.71M)
- Top 15 = 83.3% of fulfilment revenue (highly concentrated)

## Opportunity Revenue Impact (2025)

- All opportunities cohort revenue: ~14.2M AED
- New clients only ('N'): ~2.5M AED
- Difference: 82% — existing client upsells dominate if not filtered

## Cross-Validation Patterns

When validating revenue:
1. Total = invoice_count × avg_invoice_value (should be within rounding)
2. Compare to Finance report (should match within 1%)
3. Check KSA exclusion is applied when comparing to Finance
4. Verify `record_deleted = FALSE` filter is in place

## BDM Revenue Reference

- Source: `projects/02_2026_data_cleanup/bruno_master_revenue/`
- 110 unique Non-SSUP GPs activated in 2025, total ~3M AED
- See `findings.md` in that folder for documented discrepancies
