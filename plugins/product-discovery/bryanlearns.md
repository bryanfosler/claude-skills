# bryanlearns — product-discovery plugin

A Claude Code plugin that runs deep, evidence-grounded product discovery — the kind a principal PM at Linear/Stripe/Apple would actually produce. Doubles as the plugin's intro doc and your learning reference.

---

## The big idea

Generic AI-PM tools (Productboard, Zeda, Kraftful) produce plausible-sounding summaries with no traceable sources. They name JTBD but don't run it. They cost $39-400/user/month and lock out solo PMs.

This plugin's wedge: **codebase-aware + free + actually runs Moesta-school JTBD and Ulwick-syntax ODI, with verbatim quotes or it didn't happen.**

The discipline that makes it work: every claim in the final brief traces back to a phase document; every phase document cites real sources with verbatim quotes. No fabrication. No theme-only summaries. No synthetic personas presented as "research findings."

---

## What it does (the 8 phases)

```
.discovery/<topic>/
├── 01-frame/FRAME.md       # Market + candidate JTBDs + hypotheses
├── 02-voices/VOICES.md     # Verbatim user quotes mined from real sources
├── 03-jobs/JOBS.md         # JTBD decomposition (functional/emotional/social)
├── 04-forces/FORCES.md     # Push/Pull/Habit/Anxiety map (Moesta's 4 forces)
├── 05-outcomes/OUTCOMES.md # Ulwick-syntax desired outcomes
├── 06-competitors/         # One file per strategic teardown
│   ├── <competitor-A>.md
│   ├── <competitor-B>.md
├── 07-scoring/OPPORTUNITY.md # Importance + max(I-S, 0) quadrant
├── 08-wedge/WEDGE.md       # Underserved-JTBD thesis
└── BRIEF.md                # Final one-page thesis
```

Each phase has a skill that does the work. Each skill knows how to load the right reference doc (`references/jtbd-moesta.md`, `references/odi-ulwick.md`, etc.).

---

## Why I picked the hybrid architecture

I sketched three variants first (kept in `working/designs/` for posterity):
- **A: Methodology-first** — One skill per methodology. Clear but skill-explosion.
- **B: Agent-first** — One big orchestrator + workhorses. Lean but monolithic.
- **C: Phase-gated** — Sequential gates with deliverables. Disciplined but heavy.

None of these is right alone. The right answer combines them:
- **Phase-gated artifact structure** from C (evidence accumulates inspectably)
- **Per-methodology entry points** from A (`/pd-jtbd`, `/pd-teardown` for one-off use)
- **Agent-driven parallel execution** from B (friction-miner and 3 competitor-analysts run at once)

This is the actual plugin shape: phase-gated output, multi-mode invocation, agent-heavy execution.

---

## How invocation works

```
/pd-discover "AI task management for ADHD"   # Full orchestrated flow
/pd-quick "..."                              # D1-D3 only, ~30 min
/pd-jtbd "current task apps"                 # Just JTBD pass
/pd-teardown Sunsama                         # One competitor teardown
/pd-friction "ADHD productivity tools"       # Just mine friction
/pd-iterate                                  # Deepen prior brief (the 10x loop)
/pd-status                                   # Where am I
/pd-redo 04-forces                           # Re-enter a phase
```

The orchestrator skill (`pd-orchestrator`) handles `/pd-discover`. Direct skills handle the rest.

---

## The iteration model

Each discovery has a depth N. `/pd-iterate` increments to N+1 by:
1. Running `thesis-critic` agent against the prior BRIEF
2. Critic returns structured gap report (evidence gaps, methodology gaps, shallow competitors, weak wedge)
3. Orchestrator dispatches focused agents to fill exactly those gaps
4. Synthesis re-runs over enriched evidence
5. Writes BRIEF-vN+1.md

Stop rule: critic returns "no significant gaps." Typically D7-D8 for serious work.

**The honesty discipline:** the critic is required to ask "what evidence would change the wedge?" and check that the prior synthesis isn't just confirming the user's prior beliefs.

---

## Hardware vs software

When the product is physical, `hw-context-adapter` agent kicks in. The methodology adapts:
- Narrative-before-spec (Fadell's press-release test) — can you write the press release before the spec?
- Fidelity ladder alignment — what stage of prototype are we at? Don't ask EVT-stage questions at sketch stage.
- BOM-weighted feature prioritization — every feature has a per-unit cost
- iFixit + repair forums as friction sources
- B2B dual-user flag (economic buyer + end user often conflict)

Software-only patterns explicitly **disabled** for HW: A/B testing on shipped product, fail-fast, feature flags.

---

## What I learned building this

**The 4 forces equation matters more than the job statement.** Moesta is emphatic: more features = more anxiety (F3), not more pull (F2). Most roadmaps make adoption *worse* by piling on features. The plugin enforces 4-forces analysis before outcome-scoring for this reason.

**ODI's `max(I-S, 0)` floor is non-cosmetic.** Implementing `I + (I-S)` without the floor distorts rankings for overserved outcomes. The plugin clamps to zero — this is the most common technical error in ODI implementations.

**Generic "JTBD" is the anti-pattern, not a starting point.** Pain-and-gain framing is what every blog post teaches. Moesta calls it the biggest misconception in the field. Context is the unit, not pain. The plugin's `jtbd-moesta.md` reference quotes this verbatim.

**"Interview firers, not fans" is the killer competitor-research move.** Apply Moesta's 4 forces to people who switched AWAY from a competitor. F1 (push) is your marketing. F3 (habit) is their moat. F4 (anxiety) is your positioning problem.

**Continuous competitive drift detection is the novel AI-tooling wedge.** Existing tools scan competitors once. LLM-native tooling can run weekly diffs of competitor websites, reviews, job postings — and surface what changed and why. With source links. No current tool does this at source-transparency level.

---

## Anti-patterns the plugin actively prevents

1. **Synthetic users presented as research findings.** Synthetic outputs allowed for hypothesis-design, never for validation. Always labeled.
2. **Theme-only outputs without quotes.** Every theme requires 2-5 verbatim quotes. The plugin enforces structurally.
3. **Unverified competitor specifics.** No pricing/feature/headcount claims without a source URL.
4. **Full-pipeline AI PRDs.** The plugin drafts; the human decides. Framed as "draft for your review" not "your PRD is ready."
5. **The confirmation loop.** The critic explicitly asks "what evidence would change the wedge?" to prevent circular re-finding of the user's prior beliefs.

---

## Status

v0.1 — initial autonomous overnight build, post-critique fixes applied.

Skills are authored from canonical sources (Moesta podcasts, Ulwick books, Reforge essays, NN/g, Torres, Portigal, Hall). Individual skills are NOT yet pressure-tested with subagents (the `superpowers:writing-skills` RED-GREEN-REFACTOR loop). The dogfood pass on Cairn at end of build serves as integration testing.

**Critique pass applied:** A self-audit against the principal-PM rubric scored 32/40 (SHIP-AFTER-FIXING-CRITICAL) with three flagged gaps. Two structural fixes shipped:
- `scripts/audit-voices.py` + `scripts/audit-brief.py` enforce the Iron Rule (verbatim quotes, source URLs, generic-tagline rejection) as code, not just documentation
- `thesis-critic` agent rewritten as adversarial competitor-PM persona with four killer questions instead of two

Before relying on the plugin for high-stakes work, run a quick smoke test: invoke `/pd-teardown` on a competitor you know well, and verify the output (a) uses verbatim quotes with real source URLs, (b) reconstructs the competitor's theory of mind not just feature list, (c) doesn't fabricate. Then run the audit scripts to confirm the brief passes structural checks.

---

## File map

- `plugin.json` — manifest
- `skills/` — one SKILL.md per phase + orchestrator + iterate (11 total)
- `commands/` — slash command files (10 total)
- `agents/` — specialist subagents (7 total)
- `references/` — distilled canon (Moesta JTBD, Ulwick ODI, etc. — 12 + INDEX)
- `templates/` — phase deliverable shapes (9 total)
- `scripts/` — validator scripts (Iron Rule enforcement)
  - `audit-voices.py` — checks VOICES.md (verbatim, URLs, cross-platform, switch stories, gaps)
  - `audit-brief.py` — checks BRIEF.md (wedge structure, evidence, falsifying condition, MODEL ESTIMATE tags, generic-tagline rejection)
- `docs/methodology.md` — the unified framework
- `docs/iteration-depths.md` — what each depth adds
- `INSTALL.md` — symlink steps + restart

See `_INDEX.md` in `references/` for the knowledge base.
