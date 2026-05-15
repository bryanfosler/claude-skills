# ODI — Ulwick Canon (Practitioner Reference)

Distilled from Tony Ulwick's Outcome-Driven Innovation. Sources: Strategyn, anthonyulwick.com, HBR 2002, Product Thinking Podcast Ep. 207 (Melissa Perri / Ulwick, Jan 2025). Load on demand for ODI work, opportunity scoring, and segmentation.

---

## 1. The Core Premise

Innovation can be a **science**. Ulwick's documented success rate for ODI-led new product introductions is ~86% vs. ~17% industry baseline. The mechanism: treat the customer's job like a manufacturing process — study it, identify metrics, remove variation, improve output.

> "ODI makes Agile more Agile, because you're not iterating on what the product does — you're only iterating on the design." — Ulwick

ODI sits at the **front end of innovation** — everything before development begins.

---

## 2. Market Definition (The Foundational Move)

A market = **a group of people + the core functional job they are trying to get done**. Not a product, technology, or category. Not demographics.

Examples:
- "Interventional cardiologists trying to restore blood flow to a blocked artery" — not "catheter market"
- "Finished carpenters trying to make precise cuts in wood" — not "circular saw market"

Why it matters: most startup concepts address a tiny slice of the customer's job. Defining the full job reveals the full opportunity space and the long-term roadmap.

---

## 3. The Desired Outcome Statement — Syntax

**[Direction of Improvement] + [Unit of Measure] + [Object of Control] + [Contextual Clarifier]**

- **Direction of Improvement:** Always **"Minimize."** Ulwick landed here after testing alternatives across 45 Microsoft projects.
- **Unit of Measure:** Either **time** or **likelihood** (probability of error/defect/failure). These two cover speed and predictability.
- **Object of Control:** The specific phenomenon tied to the job step.
- **Contextual Clarifier:** Optional scope.

### Examples Across Domains

**Medical (Cordis context):**
- "Minimize the time it takes to advance the catheter to the treatment site"
- "Minimize the likelihood of impacting an adjacent side vessel when navigating a tortuous path"
- "Minimize the likelihood of restenosis occurring after treatment" ← Cordis HeartStent breakthrough

**Food prep:**
- "Minimize the likelihood of overcooking the food"
- "Minimize the time it takes to prep the ingredients"

**Pet nutrition:**
- "Minimize the time it takes to determine what nutrition is needed to address the pet's existing health issues"

**Circular saw (Bosch context):**
- "Minimize the time it takes to adjust the blade height"
- "Minimize the likelihood of the cut going off the intended track"
- "Minimize the likelihood of the blade binding or kickback when cutting at an angle"

**Financial fraud detection:**
- "Minimize the time it takes to detect a credit card fraud event"

A well-formed outcome statement is:
- Stable (true 10 years ago and 10 years from now)
- Solution-agnostic (no product or technology references)
- Measurable (could be survey-rated)
- Universal within a market

---

## 4. The Opportunity Score — Formula and Floor

```
Opportunity Score = Importance + max(Importance − Satisfaction, 0)
```

**The `max(..., 0)` floor is non-negotiable.** It means: if satisfaction exceeds importance (overserved), the subtraction term is floored at zero — you don't get credit for satisfying something better than its importance warrants. A common implementation error is to compute `I + (I − S)` without the floor, producing negative-adjusted scores that distort ranking.

### Inputs

**Survey scale:** 1–10 for both importance and satisfaction. Either use mean scores directly, or convert top-2-box percentage (% rating 9 or 10) to a 0-10 scale (e.g., 70% → 7.0).

### Worked Examples

| Outcome | I | S | Calculation | Score | Band |
|---------|---|---|-------------|-------|------|
| Restenosis | 9.0 | 2.0 | 9 + (9-2) | **16.0** | Extreme |
| Adjust blade height | 8.0 | 3.0 | 8 + (8-3) | **13.0** | Underserved |
| Cut on track | 7.5 | 6.0 | 7.5 + 1.5 | **9.0** | Appropriately served |
| Locate parts supplier | 5.0 | 8.0 | 5 + max(5-8,0) | **5.0** | Overserved |
| Grad student failing exam | 8.57 | 1.43 | 8.57 + 7.14 | **15.71** | Ripe |

---

## 5. Threshold Bands

| Score | Classification | Strategic Implication |
|-------|---------------|-----------------------|
| **< 10** | Overserved or adequately served | Compete on cost/simplicity, not features |
| **10–12** | Appropriately served | Marginal; monitor in broad markets |
| **12–15** | Underserved — opportunity zone | Real innovation potential; low-hanging fruit |
| **> 15** | Ripe opportunity | High-priority; premium pricing available |
| **> 20** | Extreme (rare) | Severely neglected market |

> 20 is mathematically possible only when both importance and gap are extreme (top-2-box scaling). Cordis's restenosis outcome lived here.

---

## 6. The Opportunity Landscape (Quadrant)

Plot every outcome on a 2-axis scatter:

- **X = Satisfaction** (left low, right high)
- **Y = Importance** (top high, bottom low)

| Quadrant | Meaning | Strategy |
|----------|--------|----------|
| Upper-left (Hi I, Lo S) | **UNDERSERVED** | Innovation zone. Premium pricing available. |
| Upper-right (Hi I, Hi S) | **TABLE STAKES** | Required to compete. Defensive investment. No differentiation. |
| Lower-left (Lo I, Lo S) | **IGNORE** | Not worth addressing. |
| Lower-right (Lo I, Hi S) | **OVERSERVED** | Strip features or reduce cost. Don't improve further. |

Different customer segments have different landscape profiles. Aggregate analysis routinely misses opportunities visible at segment level.

---

## 7. The 8 Universal Job Steps

Every functional job follows the same arc.

| # | Step | What |
|---|------|------|
| 1 | **Define** | Plan the approach; set goals; gather requirements |
| 2 | **Locate** | Gather inputs, information, materials |
| 3 | **Prepare** | Organize and set up |
| 4 | **Confirm** | Verify readiness before executing |
| 5 | **Execute** | Perform the central task |
| 6 | **Monitor** | Track results during/after execution |
| 7 | **Modify** | Adjust in response to problems |
| 8 | **Conclude** | Wrap up; clean up; document; communicate |

### Applied to "Restore Blood Flow to a Blocked Artery"

1. Define treatment plan, select catheter
2. Locate access point and blockage via imaging
3. Insert introducer sheath, advance guidewire
4. Confirm catheter position via fluoroscopy
5. Inflate balloon or deploy stent
6. Assess blood flow restoration
7. Reposition, re-inflate, add intervention if needed
8. Remove catheter, close access site, document

Each step yields 10-25 desired outcomes → 50-150 total per market. Without the map, interviewers over-index on Execute and miss Define/Confirm/Conclude — which often harbor the richest unmet needs.

---

## 8. Three Critical Pitfalls

### Pitfall 1: Soliciting Solutions Instead of Outcomes

The most common error. Customers default to solutions ("I want an alert," "I want a bigger screen"). These are guesses, not metrics. A well-formed outcome statement contains **zero references to any product, technology, or solution**. The plugin must redirect: "what are they trying to avoid that makes that solution useful?" → "minimize the time it takes to detect [event]."

### Pitfall 2: Confusing Tasks with Outcomes

- "Insert the catheter" — **task** (what they do)
- "Minimize the likelihood of damaging the vessel wall while advancing the catheter" — **outcome** (how they measure success)

Job executors default to tasks because they're concrete. Interviewer must surface the metric beneath the action.

### Pitfall 3: Demographic Segmentation Disguised as Outcome-Based

If a team filters survey data by company size or job title and calls it segmentation, they have missed the method. Real outcome-based segmentation requires **cluster analysis on satisfaction scores** to find groups where the same outcomes are consistently poorly satisfied together. The same outcome may be Table Stakes for one segment and Underserved for another. This is the heart of where ODI surfaces hidden opportunities.

---

## 9. The Three Case Studies (Brief)

### Cordis (1991) — Interventional Cardiology
Started at 1% angioplasty balloon market share. ODI surfaced "minimize likelihood of restenosis" as an off-the-charts score. Result: 19 new products, all #1 or #2 in category. Market share to 20%+. HeartStent became a $1B business in under 2 years. Stock $8 → $108.

### Bosch — North American Circular Saw
Aggregate market appeared saturated; no opportunities visible. Outcome-based segmentation found a third of the market (finished carpenters making angle cuts and blade-height adjustments) had **14 unmet outcomes nobody addressed**. When engineers saw the 14, they generated solutions in three hours: "we just didn't know these were the 14 that mattered." Best-selling circular saw in NA for ~10 years.

### Microsoft (45 projects)
The test bed for refining outcome-statement syntax. Source of Ulwick's conviction about "Minimize + time/likelihood" as the canonical formulation.

---

## 10. Survey Design (Brief)

| Detail | Standard |
|--------|----------|
| Scale | 1–10 (importance and satisfaction) |
| Anchors | "Not at all" → "Extremely" / "Completely" |
| Question | "When [job step], how important is it that you are able to [outcome]?" + "When using [current solution], how satisfied are you with your ability to [outcome]?" |
| Sample (market research) | 180 minimum, 180-600 typical, up to 3,000 enterprise |
| Sample (concept testing) | 20+ |
| Length | 50-150 outcomes; long surveys often split + imputed |

---

## 11. Where ODI Fits — and Doesn't

**ODI is for:** entering new markets, major reinventions, large R&D or M&A bets, products where cost of a wrong bet exceeds research cost.

**Overkill when:** small feature prioritization within a known product. A lightweight version (shorter survey on 20-30 key outcomes) delivers most of the value.

**Complementary to:** Moesta switch interviews (qualitative motivation), design sprints (solution prototyping), Lean (iteration after market is defined). Sequence: ODI to define the opportunity → design sprint to explore solutions → Agile to ship.

---

## 12. Three Things The Plugin Must Not Get Wrong

1. **Outcomes are metrics, not features or tasks.** Reject and redirect when input is a solution or an action.
2. **The formula floors at zero.** Always `max(I − S, 0)`.
3. **Segmentation is not demographic.** When user asks "which segment?" route to satisfaction-cluster analysis, not firmographic filtering.

---

## Sources

- [Strategyn — ODI process](https://strategyn.com/outcome-driven-innovation-process/)
- [Strategyn — Market Opportunity / Algorithm](https://strategyn.com/outcome-driven-innovation/market-opportunity/)
- [Ulwick — Path to Growth: The Opportunity Algorithm](https://www.marketingjournal.org/the-path-to-growth-the-opportunity-algorithm-anthony-ulwick/)
- [Ulwick — Inventing the Perfect Customer Need Statement](https://jobs-to-be-done.com/inventing-the-perfect-customer-need-statement-4fb7de6ba999)
- [Ulwick — Mapping the Job-to-be-Done](https://jobs-to-be-done.com/mapping-the-job-to-be-done-45336427b3bc)
- [Product Thinking Podcast Ep. 207 — Perri/Ulwick (Jan 2025)](https://www.produxlabs.com/product-thinking-blog/episode-207-tony-ulwick-outcome-driven-innovation)
- [Wikipedia — Outcome-Driven Innovation](https://en.wikipedia.org/wiki/Outcome-Driven_Innovation)
