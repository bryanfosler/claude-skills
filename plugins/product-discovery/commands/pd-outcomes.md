---
description: Draft Ulwick-syntax desired outcomes from primary JTBDs (ODI methodology)
allowed-tools: Read, Write, Edit
---

# /pd-outcomes

Translate primary JTBDs into measurable Ulwick desired outcomes. Outcomes are metrics, not features.

## Usage

```
/pd-outcomes                                    # uses .discovery/<topic>/03-jobs/JOBS.md
/pd-outcomes --from path/to/jobs/file.md       # specify input
```

## What happens

Invokes `pd-outcomes` skill which:
1. Loads JOBS.md (primary JTBDs)
2. For each JTBD, walks Ulwick's 8 universal job steps (define / locate / prepare / confirm / execute / monitor / modify / conclude)
3. Generates 15-25 outcome statements in the canonical syntax: `[Direction] the [unit of measure] [object of control] [contextual clarifier]`
4. Separates functional / emotional / consequential layers
5. Tags each with evidence pointer (Phase-02 quote) or `[HYPOTHESIS]`
6. Estimates importance (1-10) flagged `[MODEL ESTIMATE]` until survey-validated

## Output

`.discovery/<topic>/05-outcomes/OUTCOMES.md` — ready for opportunity scoring (Phase 07).

## Anti-patterns prevented

- Outcomes that mention products or features
- Direction/unit/object incomplete
- Only functional layer (no emotional/consequential)
- Importance scores presented as facts (always tagged estimate)

$ARGUMENTS
