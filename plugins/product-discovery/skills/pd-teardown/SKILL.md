---
name: pd-teardown
description: Use when running a strategic competitor teardown — reconstructs the competitor's theory-of-mind (what JTBD they believe they're serving, what wedge they used to enter), analyzes their four fits, codes their reviews for JTBD signals, and produces a thesis-style output not a feature comparison. Works standalone via /pd-teardown <name> or as Phase 06 of full discovery.
---

# pd-teardown (Phase 06)

You are doing an elite-tier competitor teardown — the kind a16z, Reforge, and elite PM teams produce. **Reconstruct theory-of-mind, not a feature list.** Find what they BELIEVE the job is, where their bet is structurally fragile, and what they're abandoning that we can claim.

Load: `references/competitor-teardown.md` before producing output.

## What this skill produces

`.discovery/<topic>/06-competitors/<competitor-slug>.md` per competitor with:

1. **Theory-of-mind** — Their stated JTBD framing; who they think is broken
2. **Wedge analysis** — How they entered; what was their initial beachhead
3. **Four fits** (Balfour) — Market-Product, Product-Channel, Channel-Model, Model-Market — and any misalignment
4. **Firers profile** — Forces of Progress applied to people who switched AWAY from them
5. **Pricing as strategy** — Plan structure, gating, segmentation reveal
6. **First-10-minutes** — What does their onboarding say is the job?
7. **Wardley evolution** — Which capabilities are commoditizing under them
8. **Verdict** — Where they're vulnerable; what they're structurally abandoning

## The 7 elite moves

### Move 1: Theory-of-mind reconstruction
Ask: *What job does this competitor BELIEVE they're serving, and what incumbent method are they implicitly claiming is broken?*

Example: Stripe didn't compete against PayPal. They competed against "payments are hard to integrate." That framing tells you who they think is broken (developer experience) and who they don't serve (managed-relationship businesses).

### Move 2: Four fits as interdependent system
Use Balfour's framework. Linear's UI is designed for engineer-led word-of-mouth (Product-Channel fit). Per-seat pricing grows with headcount (Channel-Model fit). These are *structural bets*. When you find a misalignment, you've found a vulnerability.

| Fit | What it means | What to ask |
|---|---|---|
| Market-Product | Does the product match what market needs? | What underserved JTBD did they target? |
| Product-Channel | Does the product spread through their chosen channel? | Why does this product work for this distribution? |
| Channel-Model | Does revenue grow as channel scales? | How does pricing extract value? |
| Model-Market | Does the revenue model fit the segment's economics? | Are they pricing for the right buyer? |

### Move 3: Interview firers, not fans
Apply Moesta's Forces of Progress to people who switched AWAY from this competitor.
- F1 (Push from them) = your marketing
- F2 (Pull to alternative) = what users actually wanted
- F3 (Habit of using them) = their moat
- F4 (Anxiety of leaving) = your positioning problem

Look in VOICES.md for "I left [competitor]" stories; mine more if needed.

### Move 4: Code reviews for JTBD signals
Thematic-code 40-60 of their reviews. Most insight-rich finding: **users satisfied with product execution but who still churned**. That means the product is solving the *wrong job* for that segment.

### Move 5: Pricing page as strategy
- Plan count → segmentation clarity
- Feature gating → what they charge premium for
- Per-seat vs. usage → growth theory
- Free tier presence → PLG conviction
- Recent price increase → market confidence
- New enterprise tier → segment ceiling reached

### Move 6: First-10-minutes encodes JTBD hypothesis
Sign up. What's the shortest path to first value? That's their theory of the job.
- Ends at "task created" → they think the job is *capture*
- Ends at "teammate invited" → they think the job is *coordination*
- What they OMIT in onboarding tells you what they think is secondary

### Move 7: Wardley evolution mapping
Every custom capability eventually commoditizes. When their "secret sauce" becomes an AWS/OpenAI commodity, their moat disappears. Identify which of their differentiators are on borrowed time.

## The thesis output structure

Always produce this exact structure at the end:

```
COMPETITOR: <name>

THEIR THEORY: The job is "<job statement>", being done badly by <incumbent>'s 
<specific failure mode>, for <user segment>.

THEIR WEDGE: Entered by delivering <core differentiator>, requiring <onboarding cost>. 
Beachhead: <initial segment>.

WHERE THEY'RE VULNERABLE: <Segment they don't serve or capability they abandoned>. 
That segment reports up to <stakeholder> who was sold <incumbent>.

OUR OPENING: <Specific underserved JTBD or coordination gap they intentionally left>. 
That fragmentation is the real pain. They created it deliberately; no one has solved it.
```

This forces strategic clarity. If you can't complete this structure, you don't understand the competitor yet.

## Example (verbatim from research)

> COMPETITOR: Linear
>
> THEIR THEORY: The job is "keeping engineering teams aligned without friction," being done badly by Jira's admin-first configuration complexity, for software engineers at VC-backed product companies.
>
> THEIR WEDGE: Entered by delivering 50-100ms UI response vs. Jira's 200-500ms, requiring zero configuration to feel useful. Beachhead: 5-50 person engineering-led teams.
>
> WHERE THEY'RE VULNERABLE: Teams where a non-technical stakeholder (VP, CEO, PMO) needs roadmap-level visibility. Linear has no credible answer for "my VP wants a Gantt." That stakeholder reports up to someone who was sold Jira.
>
> OUR OPENING: The coordination layer above the sprint — roadmapping, stakeholder communication, cross-team planning — that Linear has intentionally abandoned and that currently lives in Confluence, Notion, Google Slides, and spreadsheets simultaneously. That fragmentation is the real pain. Linear created it deliberately; no one has solved it.

## Process for /pd-teardown <name> (standalone)

1. Dispatch `competitor-analyst` agent with name + market context
2. Agent does theory-of-mind + 4 fits + reviews coding + onboarding signup + pricing
3. Agent returns structured findings
4. You synthesize into the thesis output
5. Write to `.discovery/<topic>/06-competitors/<slug>.md` or `<slug>.md` in current dir if no discovery in progress

## Process for Phase 06 (orchestrated)

1. Orchestrator passes 3-5 competitor names from FRAME.md
2. Dispatch 3-5 `competitor-analyst` agents in parallel
3. Synthesize each into a thesis
4. Write side-by-side comparison summary at `06-competitors/_COMPARISON.md`

## Anti-patterns

| Symptom | STOP |
|---|---|
| Feature comparison table as output | Re-do as theory-of-mind reconstruction |
| Praising/criticizing the competitor | Strategy is neutral. Describe their bet, find the fragility. |
| Generic "they're slow / they're complicated" | Be specific. What structural choice causes that? |
| Pricing covered as "their plans" | Plans are signals. What does the segmentation reveal? |
| Missing the firers section | Apply 4 forces to switchers-away. Always. |
| Missing the OUR OPENING in thesis | The whole point is the opening. Don't ship without it. |

## What comes next

Phase 07 (`pd-score`) uses competitor satisfaction signals from teardowns to compute opportunity scores across the OUTCOMES.md outcomes.
