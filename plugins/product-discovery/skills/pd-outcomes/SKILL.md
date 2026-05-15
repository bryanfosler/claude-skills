---
name: pd-outcomes
description: Use when drafting Ulwick-syntax desired outcome statements from primary JTBDs and mined evidence — produces 05-outcomes/OUTCOMES.md with 20-40 outcome statements ready for opportunity scoring in Phase 07.
---

# pd-outcomes (Phase 05)

You are translating primary JTBDs into measurable outcomes — Tony Ulwick's contribution to JTBD theory. Outcomes are **metrics, not features**. The plugin must structurally prevent any drift toward solutions.

Load: `references/odi-ulwick.md` before producing output.

## The Ulwick syntax (non-negotiable)

```
[Direction] the [unit of measure] [object of control] [contextual clarifier]
```

- **Direction**: Minimize, maximize, reduce, increase, eliminate
- **Unit of measure**: time, frequency, error rate, % completion, $
- **Object of control**: a specific noun the user can affect
- **Contextual clarifier**: when, where, with whom

### Worked examples

✅ "Minimize the **time** it takes to **detect a credit card fraud event** *across multiple transaction channels*."
✅ "Reduce the **number of context switches required** to **add a new task** *when away from a desktop*."
✅ "Maximize the **% of planned tasks completed** *on a low-energy day*."
✅ "Minimize the **frequency of medication doses missed** *during travel or schedule disruptions*."

### Anti-pattern examples

❌ "Better mobile app" — no direction, no unit, no object
❌ "Add quick-capture" — feature, not outcome
❌ "Reduce friction in task entry" — what unit of friction? what object?
❌ "Make users feel calm" — what metric?

## What this skill produces

`.discovery/<topic>/05-outcomes/OUTCOMES.md` with:

1. **Primary JTBD → outcomes mapping** — Per JTBD, list 10-25 outcome statements
2. **Functional outcomes** — Measurable task completion / efficiency / error rate
3. **Emotional outcomes** — Reduced anxiety / sense of control (measurable: e.g., "% of days user reports feeling 'on top of things'")
4. **Consequential outcomes** — Downstream effects (e.g., "Minimize cascading missed commitments after an initial missed task")
5. **Evidence pointers** — Each outcome cites which Phase-02 quote(s) inspired it
6. **Estimated importance** — Provisional rating (1-10) flagged as `[MODEL ESTIMATE]`

## Process

### Step 1: For each primary JTBD, brainstorm outcomes across job-step lifecycle

Ulwick's 8 universal job steps:
1. Define (planning)
2. Locate (finding inputs)
3. Prepare (setup)
4. Confirm (validate)
5. Execute (do the thing)
6. Monitor (track progress)
7. Modify (adjust)
8. Conclude (complete/archive)

For each step, ask: "What does the user want to minimize/maximize?" Generate 2-4 outcomes per step. Most jobs yield 15-25 outcomes total.

### Step 2: Apply the syntax check

Every outcome must have all 4 syntax elements (direction, unit, object, clarifier). Reject incomplete ones; rewrite.

### Step 3: Separate functional from emotional from consequential

Functional: the visible job
Emotional: how the user wants to feel doing it
Consequential: what happens after (cascading effects)

A complete outcome set includes all three layers.

### Step 4: Tag with evidence

Each outcome notes the Phase-02 quote(s) that inspired it. If an outcome has NO supporting quote, mark `[HYPOTHESIS — needs validation]`.

### Step 5: Estimate importance (provisional)

Without a real survey, you can ESTIMATE importance from mined evidence:
- **High importance (8-10)**: Multiple verbatim quotes name this as urgent/critical
- **Moderate (5-7)**: Mentioned in passing, multiple sources
- **Low (1-4)**: Inferred or single-source

**Tag every score `[MODEL ESTIMATE]`.** The plugin cannot fake survey data.

### Step 6: Flag the segmentation question

Ulwick's killer move: outcome-based segmentation. Different user segments often have wildly different importance scores for the same outcome. If your VOICES.md shows different sub-populations (e.g., ADHD users vs. neurotypical users of same product), generate separate outcome importance estimates per segment.

## Quick reference

| Layer | Example unit | Example outcome |
|---|---|---|
| Functional | time | "Minimize the time to capture a task while walking" |
| Emotional | % of sessions | "Maximize % of planning sessions ending with user feeling in control" |
| Consequential | # of cascading misses | "Minimize the number of follow-up tasks dropped after an initial missed deadline" |

## The 3 critical errors to NEVER make

1. **Outcomes as features.** "Add notifications" is solution. "Minimize the time between a forgotten task and a reminder reaching the user in their physical context" is outcome.
2. **Skip the floor at zero.** When you score in Phase 07: `Importance + max(Importance - Satisfaction, 0)`. The `max(..., 0)` is non-cosmetic.
3. **Segment by demographic.** Outcome importance differs by *job context*, not by job title or company size.

## Anti-patterns

| Symptom | Fix |
|---|---|
| Outcome mentions a product/feature | Rewrite at the metric layer |
| Direction/unit/object incomplete | Apply syntax check |
| Only functional outcomes | Add emotional + consequential |
| Importance scores presented as facts not estimates | Tag `[MODEL ESTIMATE]` |
| No evidence pointer | Either find a quote or mark `[HYPOTHESIS]` |

## What comes next

Phase 07 (`pd-score`) computes opportunity scores. Phase 06 (`pd-teardown`) examines how competitors serve each outcome (= their satisfaction estimate per outcome).
