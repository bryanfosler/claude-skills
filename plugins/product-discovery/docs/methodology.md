# Methodology: The Unified Framework

This is *why* the plugin works the way it does. The 8 phases aren't arbitrary — each enforces a specific discipline that elite product teams use, that generic AI-PM tools skip, and that solo PMs are too time-pressured to apply consistently.

## The three cross-cutting principles

Research across Moesta, Ulwick, Reforge, NN/g, Indi Young, Teresa Torres, and Apple ML converges on three principles. **Everything in the plugin enforces these.**

### Principle 1: Demand-side framing
> Generic AI-PM tools default to supply-side framing under pressure. The plugin refuses to.

Moesta's "context not pain." Ulwick's "outcome is a metric not a feature." Torres's opportunity-solution tree. Elite competitor teardowns (reconstruct theory of mind, not catalog features). They all reject starting from the product.

**How the plugin enforces:**
- Phase 03 (JTBD) rejects feature-shaped job statements
- Phase 05 (Outcomes) rejects outcomes that reference a product/feature/technology
- Phase 06 (Teardowns) rejects feature comparison tables as primary output
- Phase 08 (Wedge) rejects "we'll be the X for Y" taglines

### Principle 2: Verbatim quotes are the audit trail
> The single most load-bearing UX requirement. Without this, AI-generated discovery is plausibility theater.

Same rule appears independently in Torres's dual-pass synthesis, friction mining methodology, competitor review coding, and Apple ML's app store summarization research (they explicitly chose "representative insights" over topic labels for this reason).

**How the plugin enforces:**
- Every theme requires 2-5 verbatim quotes with source URLs
- The orchestrator's Iron Rule: "If you cannot find a real quote, write INSUFFICIENT EVIDENCE — never invent one"
- The thesis-critic explicitly audits for unverified claims
- Model-estimated scores tagged `[MODEL ESTIMATE]` to prevent confusion with survey data

### Principle 3: Friction reduction often beats feature addition
> The counter-intuitive insight. Most teams reach for the wrong move first.

Moesta's condo example (30% sales lift from removing F3/F4 friction, no product change). Ulwick's overserved quadrant guidance ("strip features, reduce cost"). Linear's onboarding minimalism. Hardware fidelity-ladder discipline (don't add complexity at low-fidelity stages).

**How the plugin enforces:**
- Phase 04 (Forces) explicitly names the F3/F4 leverage point
- Coaching default when a user proposes a new feature: "what F3/F4 friction could you remove instead?"
- Phase 07 (Scoring) classifies overserved outcomes (< 10) with the explicit guidance: "compete on cost, not features"

---

## The 8-phase pipeline (and why each phase is non-skippable)

### Phase 01 — Frame
Defines market job-based (not demographic), candidate JTBDs as hypotheses, falsifiable claims for later phases.

**Why non-skippable:** without it, mining wastes time on the wrong sources, JTBDs are ad-hoc, and the wedge has no anchor.

**Source:** Ulwick (market definition), Moesta (JTBD candidates as hypotheses)

### Phase 02 — Voices
Mines verbatim user friction from public sources (Reddit, App Store, G2, Trustpilot, niche forums). 3+ platforms per theme.

**Why non-skippable:** the whole framework depends on real evidence. Skipping = AI plausibility theater.

**Source:** Moesta (switch stories), Friction mining sources (Reddit, G2, App Store, niche forums — see references/friction-mining-sources.md)

### Phase 03 — JTBDs
Decomposes 1-3 primary jobs with functional/emotional/social layers. Clusters by causal pathway, not demographic.

**Why non-skippable:** outcomes (Phase 05) only make sense in the context of a defined job. Skipping = generic outcomes that don't reveal segmentation.

**Source:** Moesta school exclusively. Job statement is synthesis-output only, never an interview question.

### Phase 04 — Forces of Progress
Maps Push, Pull, Habit, Anxiety per JTBD using mined evidence. Calculates F1+F2 vs F3+F4.

**Why non-skippable:** without this, the team focuses on adding F2 features when reducing F4 anxiety would drive more switches. This is the highest-leverage corrective in discovery.

**Source:** Moesta canonical methodology.

### Phase 05 — Desired Outcomes (ODI)
Ulwick-syntax outcome statements: `[Direction] the [unit] [object] [clarifier]`. 15-25 outcomes per JTBD. Functional + emotional + consequential layers.

**Why non-skippable:** outcomes are what survey research validates. Without them, the discovery has no measurable layer.

**Source:** Ulwick / Strategyn. The syntax check is structural — outcomes that violate it get rewritten.

### Phase 06 — Competitor Teardowns
Strategic teardowns of 3-5 competitors. Theory-of-mind, four fits, firers profile, review coding, pricing-as-strategy, first-10-minutes, Wardley evolution. Thesis output (THEIR THEORY / WEDGE / VULNERABLE / OUR OPENING).

**Why non-skippable:** wedge depends on naming a competitor-belief-that's-wrong. Can't do that without strategic teardown.

**Source:** Brian Balfour (four fits), Bob Moesta (firers via forces), April Dunford (positioning), Wardley.

### Phase 07 — Opportunity Scoring
Formula: `Importance + max(Importance − Satisfaction, 0)`. Threshold bands: < 10 overserved, 12-15 underserved, > 15 ripe, > 20 extreme. Quadrant plot.

**Why non-skippable:** prioritization across outcomes requires explicit math. Without it, "what to build first" is opinion.

**Source:** Ulwick / Strategyn. The `max(..., 0)` floor is the most common technical error in ODI implementations.

### Phase 08 — Wedge Thesis
Names the wrong-belief, our different belief, the beachhead (job-context defined), the structural advantage, the falsifying condition. 3 alternative wedges considered and rejected. 2-week validation plan.

**Why non-skippable:** without a falsifiable wedge, the discovery produces "lots of activity, low-signal output." A wedge that names what would make it wrong is a real bet.

**Source:** Geoffrey Moore (Crossing the Chasm), April Dunford (Obviously Awesome), Christensen (disruption theory), our synthesis of evidence.

---

## The iteration model — the 10x loop

Each discovery has a depth N. `/pd-iterate` increments to N+1 by dispatching `thesis-critic`, which finds gaps and triggers focused agent work to fill them.

| Depth | What gets added |
|---|---|
| D1 | Sketch — public-knowledge framing |
| D2 | Voices mined, 15+ verbatim quotes, 3+ platforms |
| D3 | JTBDs decomposed with multi-layer evidence |
| D4 | Forces mapped with quote-backed evidence |
| D5 | Outcomes Ulwick-compliant, model-estimated importance |
| D6 | 4-6 competitors at strategic depth |
| D7+ | Critic-driven gap fills — new evidence, not rephrasing |

**Stop rule:** when the critic returns <3 HIGH-improvement gaps, or 3 consecutive iterations show low material change.

**The killer questions the critic must ask:**
1. *"What evidence would change the wedge?"* — falsifiability check
2. *"Are we re-finding evidence for an existing thesis?"* — confirmation-bias check

Without these, iteration is theater.

---

## What the plugin does NOT do (intentional limits)

1. **Survey-validated importance/satisfaction scores.** The plugin estimates from mined evidence and tags `[MODEL ESTIMATE]`. Real ODI requires surveys. The plugin produces directional priority, not statistical certainty.
2. **Synthetic users.** Synthetic personas allowed as hypothesis scaffolding, never as "research findings." Always labeled.
3. **Continuous feedback collection.** The plugin is one-shot per discovery run; no ongoing feedback pipeline.
4. **PRD authoring.** The plugin drafts wedges and validates them — the PM writes the PRD with their judgment, not the plugin's.

---

## Hardware vs. software

The plugin's `hw-context-adapter` agent engages when product is physical. Adapts:
- **Narrative-before-spec** gate (Fadell's press release)
- **Fidelity-ladder** alignment (sketch → foam → 3D-print → looks-like → works-like → EVT → DVT → PVT)
- **BOM-weighted prioritization** (per-unit cost matters)
- **Customer-journey prototyping** (unboxing/install/maintenance/failure)
- **iFixit + repair forums** as friction sources
- **Dual-user flag** for B2B HW (economic buyer ≠ end user)

**Disabled for HW physical layer:** A/B testing, fail-fast, feature flagging. These are SW-only patterns that don't translate.

---

## Why this is differentiated vs. existing tools

| Capability | This plugin | Productboard | Zeda | Kraftful | Dovetail |
|---|---|---|---|---|---|
| Free | ✅ | ❌ ($300+/mo) | ❌ | ❌ | ❌ |
| Codebase-aware | ✅ | ❌ | ❌ | ❌ | ❌ |
| Verbatim-quote enforcement | ✅ structural | ⚠ optional | ⚠ optional | ✅ partial | ✅ |
| Moesta switch interview | ✅ | ❌ | ❌ | ✅ partial | ⚠ as template |
| Ulwick formula with floor-at-zero | ✅ | ⚠ template | ❌ | ❌ | ❌ |
| Critic-driven iteration loop | ✅ | ❌ | ❌ | ❌ | ❌ |
| HW-specific methodology | ✅ | ❌ | ❌ | ❌ | ❌ |

**The wedge of the wedge:** what makes this plugin uniquely defensible is the combination of (a) demand-side framing structurally enforced, (b) verbatim quotes as the audit trail, (c) the critic-driven iteration loop. No existing tool does all three.

---

## How to use it well

1. **Run `/pd-quick` first** on a fuzzy idea. 30-min D1-D3 pass. Often reveals "this isn't worth deeper investigation."
2. **Run `/pd-discover` on a real product question** you're committing to. 60-90 min D2-D6 first pass.
3. **Run `/pd-iterate` 2-3 times.** Each iteration adds new evidence, not rephrasing. Stop when the critic says "thesis stable."
4. **Validate the wedge** with the 2-week validation plan from WEDGE.md before betting strategy.
5. **Survey-validate the scores** if making large bets. Real ODI requires real surveys; the plugin's scores are directional only.

---

## How to extend it

- Add a methodology: write a new SKILL.md in `skills/`, add the reference to `references/`, optionally add a `/pd-<name>` command
- Add a friction source: edit `references/friction-mining-sources.md`
- Add a competitor lens: extend `agents/competitor-analyst.md`
- Add an HW-specific move: extend `agents/hw-context-adapter.md`

The plugin is structurally open. New canonical sources can be incorporated as the field evolves.
