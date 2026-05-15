---
description: Run a full product discovery flow (8 phases, depth D2-D6) on a topic
allowed-tools: Agent, Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# /pd-discover

Run the full product discovery pipeline on a topic.

## Usage

```
/pd-discover "AI task management for ADHD"
/pd-discover "B2B contract review tooling for in-house counsel"
```

## What happens

Invokes the `pd-orchestrator` skill which:

1. **Frames** the market and candidate JTBDs (Phase 01)
2. **Mines verbatim quotes** from Reddit/reviews/forums in parallel (Phase 02)
3. **Decomposes JTBDs** with Moesta methodology (Phase 03)
4. **Maps forces of progress** (Push/Pull/Habit/Anxiety) per JTBD (Phase 04)
5. **Drafts Ulwick-syntax outcomes** (Phase 05)
6. **Tears down 3-5 competitors** in parallel (Phase 06)
7. **Scores opportunity** with I + max(I-S, 0) (Phase 07)
8. **Synthesizes the wedge thesis** (Phase 08)
9. **Writes BRIEF.md** — the one-page publication-grade output

## Output

`.discovery/<topic-slug>/` with phase deliverables and final BRIEF.md.

## Time

60-90 minutes for D2-D6 first pass. `/pd-iterate` to deepen toward D7+.

## Discipline

- Verbatim quotes only — no fabrication
- Every claim cites a source URL
- ODI scores tagged `[MODEL ESTIMATE]` until survey-validated
- The thesis-critic checks for confirmation bias

## Related

- `/pd-quick "topic"` — D1-D3 only (~30 min)
- `/pd-iterate` — Deepen the current brief
- `/pd-jtbd "topic"` — Run JTBD pass alone
- `/pd-teardown <name>` — Single competitor teardown
- `/pd-status` — See where the current discovery is

$ARGUMENTS
