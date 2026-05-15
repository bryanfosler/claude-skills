---
name: pd-orchestrator
description: Use when running a full product discovery flow on a market, product, or strategic question — orchestrates the 8-phase pipeline (frame, voices, jobs, forces, outcomes, competitors, scoring, wedge) and writes a defensible BRIEF.md with verbatim-quote evidence.
---

# pd-orchestrator

Coordinates the full `/pd-discover` flow. You are running deep product research — Moesta JTBD + Ulwick ODI + strategic competitor teardowns — and producing a brief grounded in real, citable evidence.

## The 8 phases

```
01-frame    → Market + candidate JTBDs + hypotheses
02-voices   → Mine verbatim user quotes (Reddit/reviews/forums)
03-jobs     → JTBD decomposition (functional/emotional/social)
04-forces   → Push/Pull/Habit/Anxiety map per JTBD
05-outcomes → Ulwick-syntax desired outcomes
06-competitors → Strategic teardowns (theory-of-mind, 4 fits)
07-scoring  → Importance + max(I-S, 0) opportunity quadrant
08-wedge    → Underserved-JTBD thesis
BRIEF.md    → Final one-page synthesis
```

## The Iron Rule

**No fabrication.** Every quote verbatim. Every claim cites a source URL. Every theme has 2-5 supporting quotes. Synthetic examples explicitly tagged `[SYNTHETIC EXAMPLE]`.

If you cannot find a real quote, write "INSUFFICIENT EVIDENCE — needs deeper mining" — never invent one.

## Process

### Step 1: Receive topic + scope
Ask 2 questions max (skip if user already specified):
- Software, hardware, or hybrid? (engages `hw-context-adapter` for HW/hybrid)
- Scope: full flow (D6+) or quick (D3)?

### Step 2: Initialize
```bash
mkdir -p .discovery/<slug>/{01-frame,02-voices,03-jobs,04-forces,05-outcomes,06-competitors,07-scoring,08-wedge}
```
Write `STATE.md` in the topic directory: current phase, completed phases, open questions.

### Step 3: Run phases in order

For each phase, invoke its dedicated skill (`pd-frame`, `pd-mine-voices`, etc.).

**Parallelize where independent:**
- Phase 02 (voices mining) runs in parallel with Phase 06 (competitor analysts × 3) once Phase 01 is done
- Phases 03→04→05 are sequential (each depends on prior)
- Phase 07 depends on 04 + 05
- Phase 08 depends on all prior

Use agents for parallel work:
- `friction-miner` for 02
- `competitor-analyst` ×3 for 06 (one per competitor)
- `interview-synthesizer` for 03/04 if interview transcripts exist
- `outcome-prioritizer` for 07

### Step 4: Synthesize BRIEF

After all 8 phases write deliverables, invoke `pd-brief` skill to produce the one-page thesis.

### Step 4b: Run the structural validators (HARD gate)

Before declaring done:
```bash
python3 .../product-discovery/scripts/audit-voices.py .discovery/<topic>/02-voices/VOICES.md
python3 .../product-discovery/scripts/audit-brief.py .discovery/<topic>/BRIEF.md
```

Both must return exit code 0 (or 1 if you're explicitly accepting warnings).

The validators enforce the Iron Rule structurally — they catch what the model might rationalize past. If either fails, fix the underlying issue. Don't ship a brief that fails the validator.

### Step 5: Offer `/pd-iterate`
Suggest the user run `/pd-iterate` to deepen. The brief is at D2-D6 after first pass; D7+ requires the critic loop.

## Quick reference

| Mode | Phases | Depth | Time |
|---|---|---|---|
| `/pd-discover` (full) | 01→08 + BRIEF | D2-D6 | 60-90 min |
| `/pd-quick` | 01→03 + BRIEF | D1-D3 | 20-30 min |
| `/pd-iterate` | critic-driven gap fill | +1 per run | 30-60 min |

## Standalone command bypass

If user invokes `/pd-teardown <name>` (or `pd-jtbd`, `pd-friction`, etc.) directly — they're using a standalone shortcut. Don't run the full orchestrator. Dispatch to the relevant skill alone.

## Hardware adapter

If the product is physical, invoke `hw-context-adapter` agent before Phase 01 frame. It returns hardware-specific framing the orchestrator must apply: fidelity ladder, BOM constraints, dual-user flag.

## Loading references

Each phase skill loads its own reference doc from `references/` on demand. Don't pre-load them all — context efficiency matters across long discoveries.

## Anti-patterns (STOP if any apply)

| Symptom | Reality |
|---|---|
| About to write a user quote from memory | STOP. Mine a real one or write "INSUFFICIENT EVIDENCE." |
| Skipping Phase 02 because "we know what users want" | STOP. The wedge depends on real voices. |
| Producing a theme without 2-5 quotes | STOP. Themes without verbatim are vapor. |
| Confirming Bryan's prior beliefs without new evidence | STOP. The discovery is broken. |
| Generic "be the X for Y" wedge | STOP. Identify which competitor BELIEF is wrong, why we believe better. |

## What success looks like

A BRIEF.md where:
- Every JTBD claim cites the verbatim quote(s) that support it
- Every competitor teardown reconstructs theory-of-mind, not just feature list
- The opportunity quadrant cites specific outcomes with scoring math shown
- The wedge thesis names a specific competitor-belief-that's-wrong
- A skeptical principal PM reading the brief would trust it
