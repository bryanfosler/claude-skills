# Iteration Depths: What each pass adds

The plugin's iteration loop is the "10x" promise. Each depth adds a specific layer of evidence and methodology. Iteration is not rephrasing.

## The depth ladder

### D1 — Sketch (~5-10 minutes)
- Framing only: market, candidate JTBDs, hypotheses
- Top 3 competitors named (no teardown yet)
- Public-knowledge friction (no mining yet)
- Tagged: HYPOTHESIS-only

**Use for:** "Is this even worth pursuing?" sanity check

### D2 — Voices (~15-30 min more, ~30 min total)
- 15+ verbatim quotes from real sources
- Themes with cross-platform corroboration (3+ platforms each)
- Switch stories pulled from mined evidence
- Astroturf flagged and excluded
- Honest gaps documented

**What's new vs. D1:** Real evidence. Anything the plugin produces at D2+ has a source URL.

### D3 — Forces (~10-20 min more)
- Push/Pull/Habit/Anxiety mapped per primary JTBD
- 3-5 quote-backed evidence pieces per force
- Net force calculation: F1+F2 vs F3+F4
- Leverage point named

**What's new vs. D2:** Causal structure. We now know *why* users do/don't switch, not just *that* they don't.

### D4 — Outcomes (~15-30 min more)
- 15-25 Ulwick-syntax desired outcomes per JTBD
- Functional + emotional + consequential layers
- Model-estimated importance per outcome (tagged ESTIMATE)
- Evidence pointer per outcome

**What's new vs. D3:** Measurable layer. Outcomes are now precision-prioritizable.

### D5 — Scoring (~20-40 min more)
- Per-competitor satisfaction per outcome (from teardowns + mined evidence)
- Opportunity formula applied: `I + max(I-S, 0)`
- Threshold bands assigned
- Quadrant plot rendered

**What's new vs. D4:** Strategic priority. We know which 3-5 outcomes are the actual wedge candidates.

### D6 — Wedge (~15-30 min more)
- Underserved-JTBD thesis with wrong-belief identified
- 3 alternative wedges generated and rejected
- Falsifying condition named
- 2-week validation plan drafted

**What's new vs. D5:** Decision-ready bet. The brief now has a defensible thesis.

### D7+ — Critic-driven deepening (~30-60 min per pass)
- `thesis-critic` agent identifies HIGH-improvement gaps
- Focused agents fill exactly those gaps (more quotes, deeper teardown, refined scoring)
- Synthesis re-runs
- BRIEF-vN+1 + meta-vN+1

**What's new vs. D6:** Iteration. Material change, not rephrasing. Each cycle adds new evidence.

## Stop rules

- `pd-quick` stops at D3 by default
- `pd-discover` runs to D6
- `pd-iterate` continues until either:
  - Critic returns < 3 HIGH-improvement gaps
  - 3 consecutive iterations show low material change ("thesis stable")
  - User stops manually

## What each depth costs

| Depth | Time | Cost driver |
|---|---|---|
| D1 | 5-10 min | Just framing + naming |
| D2 | +15-30 min | Web search + extraction of 15+ quotes |
| D3 | +10-20 min | Quote re-reading + force-coding |
| D4 | +15-30 min | Outcome generation + Ulwick syntax checks |
| D5 | +20-40 min | Per-competitor-per-outcome estimation |
| D6 | +15-30 min | Synthesis + alternative wedges |
| D7+ | +30-60 min/pass | Critic dispatch + focused agent work |

Total D6: ~60-90 min. D7+: each pass adds 30-60 min.

## The 10x claim

A D2 brief vs. a D7 brief:
- D2: 15 quotes, 3 competitors named, hypothesis-only JTBDs, no scoring, generic wedge
- D7: 50+ quotes across 6+ platforms, 5 competitors at strategic depth, scored outcomes with quadrant, sharp wedge with falsifying condition, validated against confirmation-bias check

These are categorically different documents. The 10x is real provided the critic loop actually finds gaps. If the critic is too gentle, the depth model becomes expensive theater.

## How to spot a stuck iteration loop

Red flags:
- Iterations produce <5 new verbatim quotes per pass
- The wedge thesis doesn't change between iterations
- Critic returns "good progress" without specific HIGH-improvement gaps
- All agents return "nothing new" — but the brief isn't actually mature

When stuck: broaden the source mix (new platforms, new search queries) or invoke `/pd-redo` on the weakest phase.
