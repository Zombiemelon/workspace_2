---
name: quiqup-ice-scorer
description: Scores Quiqup product tasks and hypotheses using a calibrated ICE framework (Impact, Confidence, Ease). Use when user asks to "score", "prioritize", "ICE", "rank hypotheses", "evaluate initiative", or "compare ideas". Outputs a structured score with justification and upgrade actions for the weakest parameter.
metadata:
  author: Svetoslav Dimitrov
  version: 1.0.0
  category: prioritization
---

Score any Quiqup task, hypothesis, or initiative using calibrated ICE logic tied to company context.

## Formula

**ICE = (Impact x Confidence) / Ease**

- All parameters scored 1-5.
- Higher ICE = better. Range: 0.2 - 25.
- Sort descending.

---

## Impact (1-5) -- "How much does this move the needle?"

Score **TWO lenses**. Final Impact = average of both, rounded to nearest 0.5.

### Lens A: Business Plan Alignment

| Score | Criteria |
|-------|----------|
| 5 | Directly enables a 2026 OKR or breakeven target (e.g., unlocks new revenue stream, hits 20 opp/month KR) |
| 4 | Supports a Term 1 priority or removes a known blocker to a KR |
| 3 | Improves an active initiative's efficiency or speed |
| 2 | Nice-to-have; loosely connected to plan |
| 1 | No clear connection to business plan or future vision |

### Lens B: User Value

| Score | Criteria |
|-------|----------|
| 5 | Impacts 100+ existing or potential clients |
| 4 | Impacts 30-100 clients or significantly deepens value for a critical segment |
| 3 | Impacts 10-30 clients with moderate value lift |
| 2 | Impacts <10 clients or provides marginal value |
| 1 | Internal team only, no client-facing value |

**Final Impact = (Lens A + Lens B) / 2**, rounded to nearest 0.5.

**Anchor:** SSUP Fulfilment -> Business: 5 (unlocks ~1.5M AED Y1, supports growth OKR). User: 4 (5-10 clients day one, potentially 100+). **Final: 4.5**

---

## Confidence (1-5) -- "How strong is the evidence?"

Stack evidence. More layers = higher score.

| Score | Evidence required |
|-------|-------------------|
| 5 | Live data from own experiment + validated user demand + stress-tested financial model |
| 4 | Strong internal data analysis (BigQuery, Salesforce) + at least 1 user research signal (interviews, feedback, transcripts) |
| 3 | Internal data OR external benchmarks/competitor analysis, but not both |
| 2 | Anecdotal only -- team intuition, a few conversations, no structured data |
| 1 | Pure assumption -- no data, no research, no benchmarks |

> **Freshness rule:** If key evidence is older than 6 months, flag it and recommend refreshing before relying on the score.

**Anchor:** SSUP Fulfilment -> SQL analysis of clients <2K AED + competitor pricing benchmarked + pricing discussion transcripts, but no live conversion data yet -> **3**

---

## Ease (1-5) -- "How much effort does this take?"

**Higher = harder.** This is the denominator -- high ease *penalizes* the score.

Score the **CURRENT STAGE** only, not the full roadmap.

| Score | Time | People | Cash | Cross-dept dependency |
|-------|------|--------|------|-----------------------|
| 1 | < 1 week | 1 person | ~0 AED | None |
| 2 | 1-2 weeks | 1-2 people, same team | < 1,000 AED | None |
| 3 | 2-4 weeks | 2-3 people | 1,000-5,000 AED | 1 cross-dept |
| 4 | 1-2 months | 3+ people | 5,000-20,000 AED | Multiple depts |
| 5 | 2+ months | Full cross-functional squad | > 20,000 AED | External vendors or major eng build |

**Anchor:** SSUP Fulfilment (Stage 1: manual pricing test) -> ~1 month, 5 people involved, contract changes, billing setup -> **4**

---

## Output Format

For every scored item, output EXACTLY:

```
Impact: X/5 (Biz: X, User: X -> avg X)
Confidence: X/5 -- [one-line evidence summary]
Ease: X/5 -- [time + people + dependencies]
ICE: X.X -- (Impact x Confidence) / Ease
Weakest: [parameter] -> [1-2 specific upgrade actions]
```

---

## Upgrade Actions

When flagging the weakest parameter, suggest from this list:

### To increase Impact

- Link initiative to a specific business plan target or OKR with projected revenue/cost
- Quantify user reach (how many clients? revenue per client?)
- Add TAM or addressable segment size
- Map to future vision (e-commerce OS, data/tech play) if relevant

### To increase Confidence

- Run a data query to validate problem size (churn rate, activation, revenue at risk)
- Conduct 3-5 user interviews or collect structured feedback (log in Salesforce)
- Run a small experiment (fake door, landing page, manual test)
- Add competitor/market benchmarks with sources
- Stress-test financial assumptions (sensitivity on conversion, churn, ARPU)
- If evidence is >6 months old, refresh it

### To decrease Ease (make it easier)

- Scope down: can you test the core assumption with a smaller, faster version?
- Remove dependencies: can one person run iteration 1 without waiting on other teams?
- Use existing tools (Clay, Lemlist, Typeform, Salesforce) instead of building custom
- Split into stages: test pricing before building product
- Timebox: fixed 1-2 week sprint with a clear "done" bar

---

## Examples

### Example 1: Score a hypothesis

**User says:** "Score SSUP Fulfilment"

```
Impact: 4.5/5 (Biz: 5, User: 4 -> avg 4.5)
Confidence: 3/5 -- SQL analysis + competitor benchmarks, but no live conversion data
Ease: 4/5 -- ~1 month, 5 people, contract + billing + ops dependencies
ICE: 3.4 -- (4.5 x 3) / 4
Weakest: Confidence -> Run the manual pricing test for 4 weeks and measure actual sign-ups. Log all client feedback in Salesforce notes.
```

### Example 2: Compare two initiatives

**User says:** "Compare Automatic Outbound vs LDR Automation"

Score each, then output a comparison table:

| Initiative | Impact | Confidence | Ease | ICE |
|------------|--------|------------|------|-----|
| Automatic Outbound | 4.5 | 5 | 2 | 11.3 |
| LDR Automation | 3.0 | 4 | 3 | 4.0 |

Recommendation: [state which ranks higher and why]

### Example 3: Insufficient information

**User says:** "Score my idea for a referral program"

If inputs are missing, ask up to 3 clarifying questions:

1. What specific outcome do you expect? (revenue, clients, retention)
2. What evidence supports this? (data, interviews, benchmarks)
3. What's the scope of the first testable version? (time, people, cost)

**Do NOT guess scores without minimum context.**
