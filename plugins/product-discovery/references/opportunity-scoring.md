# Opportunity Scoring (Practitioner Reference)

Ulwick's opportunity algorithm in operational form. Load on demand for the quadrant skill, prioritization work, or anywhere the plugin needs to translate importance + satisfaction inputs into a ranked opportunity list.

---

## 1. The Formula

```
Opportunity Score = Importance + max(Importance − Satisfaction, 0)
```

Survey inputs: 1-10 scale for both importance and satisfaction. Either use mean scores directly, or convert top-2-box percentage (% rating 9 or 10) to a 0-10 scale (e.g., 70% top-2-box → 7.0).

### The Floor at Zero — Non-Negotiable

The `max(..., 0)` floor means: when satisfaction *exceeds* importance (an overserved case), the subtraction term is capped at zero. You don't get extra credit for satisfying something better than its importance warrants.

**A common implementation error** is computing `I + (I − S)` without the floor. This produces *negative-adjusted* scores for overserved outcomes that distort the ranking and make table-stakes outcomes look lower-priority than they are. The floor is what makes the formula behave correctly in the overserved quadrant.

### Worked Examples

| Outcome | Importance | Satisfaction | Calculation | Score |
|---------|-----------|--------------|-------------|-------|
| Minimize likelihood of restenosis | 9.0 | 2.0 | 9 + (9−2) | **16.0** |
| Minimize time to adjust blade height | 8.0 | 3.0 | 8 + (8−3) | **13.0** |
| Minimize likelihood of cut going off track | 7.5 | 6.0 | 7.5 + (7.5−6.0) | **9.0** |
| Minimize time to locate parts supplier | 5.0 | 8.0 | 5 + max(5−8, 0) = 5 + 0 | **5.0** |
| Minimize likelihood of failing an exam | 8.57 | 1.43 | 8.57 + 7.14 | **15.71** |

Note the fourth row: without the floor, this would be `5 + (-3) = 2`. The floor keeps it at 5 — correctly classifying it as low-priority but not penalized.

---

## 2. Threshold Bands

| Score | Classification | Strategic Implication |
|-------|---------------|-----------------------|
| **< 10** | Overserved or appropriately served | Compete on cost/simplicity, not features |
| **10–12** | Appropriately served | Marginal opportunity; monitor |
| **12–15** | Underserved — opportunity zone | Real innovation potential; "low-hanging fruit" |
| **> 15** | Ripe opportunity | High priority; customers will pay a premium |
| **> 20** | Extreme opportunity | Rare; indicates severely neglected market |

> 20 is mathematically possible only with extreme top-2-box scaling — Cordis's restenosis outcome was here. In practice, scores above 17 are exceptional.

---

## 3. The Quadrant (Opportunity Landscape)

Plot every outcome on a 2-axis scatter:
- **X = Satisfaction** (left low → right high)
- **Y = Importance** (bottom low → top high)

| Quadrant | Meaning | Move |
|----------|--------|------|
| Upper-left (Hi I, Lo S) | **UNDERSERVED** | Premium-priced innovation zone |
| Upper-right (Hi I, Hi S) | **TABLE STAKES** | Required to compete; no differentiation |
| Lower-left (Lo I, Lo S) | **IGNORE** | Don't address |
| Lower-right (Lo I, Hi S) | **OVERSERVED** | Strip features, reduce cost |

The score maps directly to position. The landscape is a visual of the same math.

**Critical:** different customer segments have different landscape profiles. The same outcome can be Underserved for Segment A and Table Stakes for Segment B. Aggregate analysis routinely misses opportunities that segment-level analysis reveals. See `odi-ulwick.md` Section 8 (Pitfall 4) for why demographic segmentation doesn't substitute.

---

## 4. Estimating Scores Without Survey Data (Model-Assisted)

ODI's full power requires a survey of 180-3,000 respondents. That's often not viable for early-stage teams, indie PMs, or coding-session-scoped decisions. The plugin can produce **directional opportunity estimates** from available evidence — with strict caveats.

### When to Use Estimation

- Solo PM or small team with no survey budget
- Early-stage product decisions where full ODI is overkill
- Pre-survey hypothesis generation — what outcomes look promising enough to invest in measuring properly?

### How to Estimate

For each candidate outcome, score importance and satisfaction on 1-10 from these evidence sources:

**Importance signals:**
- Frequency in verbatim review quotes (>30% of reviews mention this concern → 7+)
- Emotional intensity in language ("infuriating," "deal-breaker," "essential") → boost importance
- Direct verbatim from switch interviews ("the reason I switched") → strong importance signal
- Time/money users currently spend working around the issue → high importance

**Satisfaction signals:**
- Number and severity of one-star reviews on this specific dimension → low satisfaction
- Existence of common workarounds (third-party hacks, custom scripts) → low satisfaction (~2-4)
- Praise specifically calling out this dimension as solved → high satisfaction (~7-9)
- Silence (no one talks about it) → assume mid (5-6) — could be table stakes or just unmeasured

### Caveats the Plugin Must Surface

- Estimated scores are **directional hypotheses**, not validated opportunity scores
- Confidence must be declared (e.g., "Estimated from 47 reviews — verify with 30+ user survey before committing major roadmap investment")
- Two outcomes with estimated scores 14 vs. 13 cannot be reliably ordered without survey data
- Estimates should always include the evidence trail (quotes, source URLs, count) — see `ai-era-discipline.md`

---

## 5. Common Errors

### Error 1: Treating Importance as Static
Importance can shift with context. A B2B buyer's importance scores change when their company hits scale, when regulation changes, when team composition shifts. Surveys captured 6+ months ago should be re-validated before driving roadmap decisions.

### Error 2: Aggregate Scoring Without Segmentation
The opportunity score across an entire market often hides segment-level opportunities. Bosch's circular saw aggregate showed no opportunities. Outcome-based segmentation surfaced 14 unmet outcomes for finished carpenters. Always check segment landscapes before concluding "no opportunity."

### Error 3: Confusing the Quadrant With the Roadmap
The opportunity landscape is the *input* to roadmap decisions, not the roadmap itself. Strategic posture (target overserved, target underserved, differentiate vs. current, disrupt, improve existing) selects which underserved outcomes you address — not all of them.

### Error 4: Ignoring Table Stakes
Upper-right outcomes are not "uninteresting." They are **required to compete.** If your product fails on a Table Stakes outcome, you lose regardless of how well you serve the Underserved ones. Treat Table Stakes as defensive minimums, not investment opportunities.

### Error 5: Solution-Disguised-as-Outcome Inputs
The opportunity score is only as good as the outcomes you're scoring. If your inputs are features ("add a dashboard") or tasks ("filter the inbox"), the scores are meaningless. Validate every input is a real outcome (Minimize + time/likelihood + object). See `odi-ulwick.md` Section 8 (Pitfalls 1 + 2).

---

## 6. The Plugin's Quadrant Skill — Behavior

When invoked, the quadrant skill should:

1. Accept a list of candidate outcomes
2. Validate each as a real outcome statement (or coach the user to reformulate)
3. Accept importance and satisfaction inputs — either survey data, estimated scores with evidence, or both
4. Compute opportunity scores using the floor-at-zero formula
5. Render the 2x2 landscape
6. Surface the top 3-5 Underserved outcomes
7. Surface any clearly Overserved outcomes (strip-feature candidates)
8. Declare confidence (n, source, recency) on every score
9. Link every outcome's score to its evidence (verbatim quotes if estimated, survey results if measured)

---

## 7. Quick Reference

```
Opportunity Score = I + max(I − S, 0)

  I = Importance (1-10, or top-2-box% × 10)
  S = Satisfaction (1-10, or top-2-box% × 10)

Bands:
  < 10   → overserved/adequately served; compete on cost
  10-12  → marginal; monitor
  12-15  → underserved; real opportunity
  > 15   → ripe; high priority
  > 20   → extreme (rare)
```

---

## Sources

- [Ulwick — Path to Growth: The Opportunity Algorithm](https://www.marketingjournal.org/the-path-to-growth-the-opportunity-algorithm-anthony-ulwick/)
- [Strategyn — Market Opportunity](https://strategyn.com/outcome-driven-innovation/market-opportunity/)
- [Productboard — Opportunity Scoring Framework](https://www.productboard.com/skills/opportunity-scoring-framework/)
- [Notes for Growth — Opportunity Score worked examples](https://notesforgrowth.github.io/Opportunity-Score/)
- [RoadmapOne — Opportunity Scoring](https://roadmap.one/blog/posts/blog8-8-opportunity-scoring/)
