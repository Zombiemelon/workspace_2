---
name: analysis-playbooks
description: Reusable analytical frameworks for common business questions — decomposition, pacing, contribution, trend projection. Use when analyzing why a metric changed, whether we're on track, what's driving growth, or what will happen next.
user-invocable: false
---

# Analysis Playbooks

Reusable frameworks for the most common analytical questions. Pick the playbook that matches the question pattern, then follow the steps.

## Playbook 1: Metric Change Decomposition

**Trigger:** "Why did metric X change?" / "What caused the drop/spike in Y?"

**Framework:** Break the metric into its components and identify which one moved.

**Steps:**
1. **Decompose the metric** — Most metrics are a product of 2-3 sub-metrics:
   - Revenue = Volume x Price x Mix
   - Conversion Rate = Qualified / Total (check both numerator and denominator)
   - CAC = Spend / Acquisitions (check both)
   - Funnel output = Input volume x Stage 1 rate x Stage 2 rate x ...
2. **Compare periods** — Calculate each component for both the current and comparison period
3. **Isolate the driver** — Which component changed the most? Is it volume, rate, or mix?
4. **Size the impact** — "Volume dropped 15% while rate held steady → volume explains 90% of the decline"
5. **Drill into the driver** — Once isolated, segment further (by channel, geography, account size)
6. **Check for compositional effects** — Sometimes the aggregate rate changes not because any segment's rate changed, but because the mix shifted (Simpson's paradox)

**Output template:**
```
**Metric X declined 12% MoM** (from A to B)

Decomposition:
| Component | Prior | Current | Change | Contribution |
|-----------|-------|---------|--------|-------------|
| Volume    | ...   | ...     | -15%   | 90% of decline |
| Rate      | ...   | ...     | +1%    | Partially offset |
| Mix       | ...   | ...     | -2%    | Minor factor |

**Root cause:** [Volume dropped because...]
**Recommendation:** [2+ options with tradeoffs]
```

## Playbook 2: Pacing Analysis

**Trigger:** "Are we on track?" / "Will we hit target?" / "How are we trending this month?"

**Framework:** Compare actual progress to where we should be at this point in the period.

**Steps:**
1. **Establish the target** — Monthly/quarterly target, broken into daily or weekly run rate
2. **Calculate expected pace** — `Target × (days_elapsed / total_days_in_period)`
3. **Calculate actual** — Sum of actuals to date
4. **Compute gap** — `Actual - Expected` and `Actual / Expected` as pacing %
5. **Project end-of-period** — Two methods:
   - **Linear projection:** `Actual / days_elapsed × total_days`
   - **Trailing-week run rate:** `Actual + (last_7d_avg × remaining_days)` — better when trend is accelerating/decelerating
6. **Flag risk** — If pacing <85%, flag as at-risk. If >115%, flag as outperforming.

**Output template:**
```
**Pacing: 87% of target** (X of Y with Z days remaining)

| Metric | Target | Actual | Pacing % | Projected EOM |
|--------|--------|--------|----------|---------------|
| ...    | ...    | ...    | 87%      | ...           |

**Projection method:** [Linear / Trailing-week run rate]
**Risk level:** [On track / At risk / Off track]
**Gap to close:** [X units in Y remaining days = Z/day needed vs current W/day]
```

## Playbook 3: Contribution / Waterfall Analysis

**Trigger:** "Which segment is driving growth?" / "Where is the revenue coming from?" / "What's our biggest exposure?"

**Framework:** Break total into segments, rank by contribution, and identify concentration risk.

**Steps:**
1. **Define segments** — Channel, geography, account tier, product line, cohort
2. **Calculate each segment's absolute and percentage contribution**
3. **Rank by size** — Largest first
4. **Calculate cumulative %** — Show how quickly you reach 50%, 80%, 100%
5. **Compare to prior period** — Which segments grew/shrank? Any new segments?
6. **Flag concentration risk** — If top 5 segments > 50%, call it out. If #1 > 20%, call it out.
7. **Identify movers** — Which segments changed the most (absolute and relative)?

**Output template:**
```
**Top 5 segments drive X% of total** — concentration risk is [low/moderate/high]

| Segment | Value | % of Total | Cumulative % | vs Prior | Change |
|---------|-------|-----------|-------------|----------|--------|
| #1      | ...   | 25%       | 25%         | +12%     | +X     |
| #2      | ...   | 18%       | 43%         | -3%      | -Y     |
| ...     |       |           |             |          |        |

**Key movers:**
- [Segment A] grew X% — driven by [reason]
- [Segment B] declined Y% — driven by [reason]

**Concentration:** [#1 client = Z% — single-client dependency risk]
```

## Playbook 4: Trend Projection

**Trigger:** "What will happen next?" / "If this continues..." / "Forecast Q2"

**Framework:** Extrapolate from historical data with explicit confidence bounds.

**Steps:**
1. **Collect historical series** — Minimum 6 data points (months). More = better.
2. **Check for seasonality** — Plot the series. Is there a repeating pattern? (Ramadan, Q4, summer)
3. **Choose projection method:**
   - **Linear trend:** Best for steady-state metrics. Fit a line, extend it.
   - **Moving average:** Best for volatile metrics. Use 3-month trailing average.
   - **Growth rate:** Best for growing metrics. Apply average MoM growth rate.
4. **Calculate projection** — Apply chosen method for 1-3 periods ahead
5. **Add confidence range** — Use historical variance: `projection +/- 1.5 × stdev`
6. **State assumptions** — What must remain true for this projection to hold?
7. **Identify risks** — What could break the trend? (Market changes, seasonal effects, one-off events)

**Output template:**
```
**Projected [metric] for [period]: X** (range: Y to Z)

| Month | Actual | Projected | Low | High |
|-------|--------|-----------|-----|------|
| ...   | ...    | ...       | ... | ...  |

**Method:** [Linear trend / Moving average / Growth rate]
**Assumption:** [Trend continues at current rate, no seasonal adjustment]
**Risks to projection:** [1. ..., 2. ...]
**Confidence:** Medium — [6 months of history, but Q4 seasonality not yet accounted for]
```

## Playbook 5: ROI / Incremental Impact Analysis

**Trigger:** "Is this campaign worth it?" / "What's the ROI?" / "Should we keep spending?"

**Framework:** Measure incremental return, not just blended metrics.

**Steps:**
1. **Define the investment** — Total spend (include agency fees, tools, headcount if applicable)
2. **Define the return** — Revenue attributed to this investment (use definition views for attribution)
3. **Calculate gross margin** — Revenue x margin rate (currently 25% assumption)
4. **Calculate ROI** — `(Margin - Spend) / Spend x 100`
5. **Calculate break-even** — `Spend / Monthly Margin Rate`
6. **Compare to benchmark** — Is this ROI above or below other channels?
7. **Incremental test (if possible)** — Compare cohorts with/without the investment
8. **State what's excluded** — Brand halo effects, long-tail revenue, referral effects

**Output template:**
```
**ROI: X%** — Break-even at Y months (currently at month Z)

| Metric | Value | Calculation |
|--------|-------|-------------|
| Spend | A | Direct spend + agency |
| Revenue | B | Attributed via [method] |
| Margin (25%) | C | B x 0.25 |
| Net Return | D | C - A |
| ROI | X% | D / A x 100 |
| Break-Even | Y mo | A / (C / months) |

**Benchmark:** [Channel average ROI = P%, this is above/below]
**Excluded:** [Brand effects, referrals, long-tail beyond N months]
**Recommendation:** [Continue / Scale / Reduce — with reasoning]
```

## Selecting the Right Playbook

| User Question Pattern | Playbook | Key Output |
|----------------------|----------|------------|
| "Why did X change?" | Decomposition | Root cause + sized contribution |
| "Are we on track?" | Pacing | Gap to target + projection |
| "What's driving Y?" | Contribution | Ranked segments + concentration |
| "What happens next?" | Trend Projection | Forecast + confidence range |
| "Is Z worth it?" | ROI / Impact | ROI % + break-even + recommendation |

When a question spans multiple playbooks (e.g., "Why are we behind target and what should we do?"), chain them: Pacing first (establish the gap), then Decomposition (find the root cause), then Contribution (identify which segment to act on).
