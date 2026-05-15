# Frame: <topic>

**Date:** <YYYY-MM-DD>
**Discovery slug:** <slug>
**Domain:** software | hardware | hybrid
**Audience:** B2B | B2C | B2D (developer)
**Stage:** 0-to-1 | growth | scale | category-redefining

---

## Topic statement (1 paragraph)
*For [user segment] doing [job] in [context], we want to understand [specific question].*

<fill in>

## Market definition (job-based, not demographic)
<one sentence; Ulwick-style if possible>

## Candidate JTBDs (3-7)

### JTBD A — <short label>
When [situation], I want to [motivation], so I can [outcome].
**Confidence:** HYPOTHESIS | INFERRED FROM PRIOR EVIDENCE

### JTBD B — ...

### JTBD C — ...

## Hypotheses to test in later phases

1. <Specific, falsifiable claim — Phase 02 mining target>
2. <...>
3. <...>

## Competitors to teardown (3-5)

| Competitor | Category | Notes |
|---|---|---|
| <name> | Direct | <one line> |
| <name> | Adjacent | <one line> |
| <name> | Disruptor | <one line> |

## Friction sources (Phase 02 will hit)

- Domain: <list 4-6 sources>
- E.g., G2 for B2B SaaS, App Store + r/<sub> for consumer SaaS, iFixit for HW, etc.

## Context flags

- [ ] Hardware? (engage `hw-context-adapter` agent before completing)
- [ ] B2B with dual users? (economic buyer + end user separately)
- [ ] No-real-choice market? (JTBD may not apply — see references/jtbd-moesta.md)
- [ ] Habitual purchase? (JTBD may not apply)

## Hardware-only additions (if applicable)
**Press release before product:** <can the user write the press release? if not, premature>
**Fidelity stage:** sketch | foam | 3D-print | looks-like | works-like | EVT | DVT | PVT
**BOM impact per feature candidate:** <$ range estimates>
**Dual-user decomposition needed:** yes/no

---

## Open questions for the discovery
- <gaps the orchestrator should be mindful of>

## Next phase
→ `pd-mine-voices` (Phase 02) — mine real friction
→ `pd-teardown` (Phase 06 in parallel) — start competitor analysts
