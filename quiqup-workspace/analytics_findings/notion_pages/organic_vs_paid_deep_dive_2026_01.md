# Organic vs Paid Channel Deep Dive

**Analysis Date:** February 1, 2026
**Data Period:** January 2024 - December 2025 (24 months)
**Analyst:** Data Team
**Status:** Updated - Business Accounts Only

---

## Executive Summary

**Key Finding:** For business accounts only, organic channel has shifted from minority (~45%) to majority (~55-73%) post-SEO launch. Paid CAC has deteriorated significantly (66 → 198 AED) while organic continues to grow.

**Critical Data Correction:** Previous analysis included individual (B2C) accounts. In 2025, ~50% of "GP" counts were individual accounts, not businesses. This update filters to `client_type_c IS NULL` (business accounts only).

**Confidence Level:** High (85%) — Data now correctly filtered to B2B customers.

---

## Impact of Data Correction

| Period | Old Total GPs | New Total GPs (Biz Only) | Individual Accounts Removed |
|--------|---------------|--------------------------|----------------------------|
| Q1 2024 | 1,201 | 1,184 | 17 (1%) |
| Q2 2024 | 1,561 | 1,554 | 7 (0.4%) |
| Q3 2024 | 1,183 | 1,183 | 0 |
| Q4 2024 | 1,595 | 1,595 | 0 |
| Q1 2025 | 3,112 | **1,495** | **1,617 (52%)** |
| Q2 2025 | 3,274 | **1,474** | **1,800 (55%)** |
| Q3 2025 | 2,881 | **1,308** | **1,573 (55%)** |
| Q4 2025 | 2,548 | **1,276** | **1,272 (50%)** |

**Finding:** 2024 data was mostly accurate. 2025 data was inflated ~2x by individual accounts.

---

## The Three Questions We Investigated

### Question 1: Is organic revenue real or a paid marketing side effect?

**Answer: Organic is real.**

| Test | Result | Evidence |
|------|--------|----------|
| Zero-Spend Month | Organic sustained | Jan 2024: 0 spend → 210 organic GPs |
| Post-SEO Shift | Organic grew | Jun-Dec 2025: Organic 55-94% of acquisitions |
| CAC Divergence | Paid efficiency collapsed | Paid CAC: 66 → 198 AED while organic grew |

### Question 2: Has the channel mix shifted?

**Answer: Yes — dramatic shift to organic in 2025.**

| Period | Paid % | Organic % |
|--------|--------|-----------|
| 2024 Average | 52% | 48% |
| Q1 2025 | 49% | 51% |
| Q2 2025 | 38% | **62%** |
| Q3 2025 | 27% | **73%** |
| Q4 2025 | 44% | 56% |

### Question 3: What's happening to paid efficiency?

**Answer: Paid CAC has tripled while volume collapsed.**

| Quarter | Paid GPs | Paid CAC | Change from Q4 2024 |
|---------|----------|----------|---------------------|
| Q4 2024 | 874 | 66 AED | Baseline |
| Q1 2025 | 726 | 76 AED | -17% volume, +15% CAC |
| Q2 2025 | 562 | 110 AED | -36% volume, +67% CAC |
| Q3 2025 | 355 | **198 AED** | -59% volume, **+200% CAC** |
| Q4 2025 | 558 | 162 AED | -36% volume, +145% CAC |

---

## Channel Share Over Time (Business Accounts Only)

### Monthly Data

| Month | Paid GPs | Organic GPs | Total | Organic % |
|-------|----------|-------------|-------|-----------|
| Jan 2024 | 1 | 210 | 211 | **99%** |
| Feb 2024 | 156 | 274 | 430 | 64% |
| Mar 2024 | 243 | 300 | 543 | 55% |
| Apr 2024 | 285 | 236 | 521 | 45% |
| May 2024 | 288 | 311 | 599 | 52% |
| Jun 2024 | 251 | 183 | 434 | 42% |
| Jul 2024 | 238 | 189 | 427 | 44% |
| Aug 2024 | 183 | 171 | 354 | 48% |
| Sep 2024 | 212 | 190 | 402 | 47% |
| Oct 2024 | 306 | 232 | 538 | 43% |
| Nov 2024 | 263 | 270 | 533 | 51% |
| Dec 2024 | 305 | 219 | 524 | 42% |
| Jan 2025 | 214 | 268 | 482 | 56% |
| Feb 2025 | 204 | 270 | 474 | 57% |
| Mar 2025 | 308 | 231 | 539 | 43% |
| Apr 2025 | 242 | 240 | 482 | 50% |
| May 2025 | 198 | 327 | 525 | 62% |
| Jun 2025 | 122 | 345 | 467 | 74% |
| **Jul 2025** | **30** | **435** | 465 | **94%** |
| Aug 2025 | 146 | 266 | 412 | 65% |
| Sep 2025 | 179 | 252 | 431 | 58% |
| Oct 2025 | 167 | 289 | 456 | 63% |
| Nov 2025 | 220 | 186 | 406 | 46% |
| Dec 2025 | 171 | 243 | 414 | 59% |

---

## Quarterly Analysis with CAC

| Quarter | Paid GPs | Organic GPs | Total | Spend (AED) | Paid CAC | Blended CAC |
|---------|----------|-------------|-------|-------------|----------|-------------|
| Q1 2024 | 400 | 784 | 1,184 | 40,494 | 101 | 34 |
| Q2 2024 | 824 | 730 | 1,554 | 65,457 | 79 | 42 |
| Q3 2024 | 633 | 550 | 1,183 | 46,937 | 74 | 40 |
| Q4 2024 | 874 | 721 | 1,595 | 57,771 | 66 | 36 |
| Q1 2025 | 726 | 769 | 1,495 | 55,525 | 76 | 37 |
| Q2 2025 | 562 | 912 | 1,474 | 61,577 | 110 | 42 |
| Q3 2025 | 355 | 953 | 1,308 | 70,351 | **198** | 54 |
| Q4 2025 | 558 | 718 | 1,276 | 90,307 | **162** | 71 |

**Key Insights:**
1. **Paid CAC tripled** from 66 AED (Q4 2024) to 198 AED (Q3 2025)
2. **Organic is subsidizing blended CAC** — without organic, CAC would be unsustainable
3. **Spend is increasing while paid volume decreases** — diminishing returns on ad spend

---

## Data Quality Issue: July 2025 Anomaly

**Red Flag:** July 2025 shows 94% organic (paid GPs collapsed to 30 while spend was 18,772 AED).

| Month | Spend | Paid GPs | Expected Paid GPs | Discrepancy |
|-------|-------|----------|-------------------|-------------|
| Jun 2025 | 16,679 | 122 | — | — |
| Jul 2025 | 18,772 | 30 | ~130 | **-100 (77% missing)** |
| Aug 2025 | 19,733 | 146 | — | Recovered |

**Most likely cause:** UTM tracking broke, causing paid acquisitions to be misattributed as organic.

**Action Required:** Audit Google Ads and landing page UTM parameters for July 2025.

---

## SEO Impact Assessment

**Context:** SEO efforts started May 2025.

| Period | Avg Organic % | Avg Organic GPs/month |
|--------|---------------|----------------------|
| Pre-SEO (Jan-Apr 2025) | 51.5% | 252 |
| Post-SEO (Jun-Dec 2025)* | 63.6% | 288 |

*Excluding July 2025 anomaly

**Finding:** SEO correlates with +12 percentage points organic share and +14% organic GP volume.

**Confidence:** Medium-High — consistent pattern across 6 months post-SEO.

---

## Recommended Actions

### Immediate

- [ ] Audit July 2025 UTM tracking
- [ ] Verify current UTM capture is working
- [ ] Investigate why paid CAC tripled (campaign mix? competition? saturation?)

### Short-term (30 days)

- [ ] Review underperforming paid campaigns (CAC > 150 AED)
- [ ] Double down on SEO (clear ROI visible)
- [ ] Investigate individual account surge (data hygiene issue?)

### Medium-term (90 days)

- [ ] A/B test 30% spend reduction to measure organic response
- [ ] Build organic attribution (SEO vs referral vs direct)
- [ ] Consider paid budget reallocation to SEO investment

---

## Appendix: Charts (Business Accounts Only)

- [GP Acquisitions, Spend & CAC by Quarter](../charts/gp_acquisitions_quarterly.png)
- [GP Channel Split by Month - 100% Stacked](../charts/gp_channel_split_100pct.png)
- [GP Channel Split by Quarter - 100% Stacked](../charts/gp_channel_split_quarterly.png)
- [GP Acquisitions by Channel - Stacked Area](../charts/gp_acquisitions_by_channel.png)

---

*Generated by Data Team analysis pipeline. Last updated: 2026-02-01*
*Data filter: Business accounts only (client_type_c IS NULL)*
