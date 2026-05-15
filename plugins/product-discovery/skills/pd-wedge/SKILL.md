---
name: pd-wedge
description: Use when synthesizing the underserved-JTBD wedge thesis from scored outcomes, competitor teardowns, and forces analysis — produces 08-wedge/WEDGE.md with a defensible strategic thesis: which competitor BELIEF is wrong, why we believe better, and the specific beachhead segment.
---

# pd-wedge (Phase 08)

This is the strategic synthesis phase. You're not summarizing — you're *naming the bet*. A real wedge identifies a **specific belief the competition holds that's wrong**, and why our different belief is better-grounded.

Generic "we'll be the X for Y" wedges fail this phase. The thesis must name a falsifiable strategic claim.

## The wedge structure (non-negotiable)

```
THE BELIEF WE'RE ATTACKING: 
  Competitors believe <X about the job/segment/job-context>.

WHY THIS BELIEF IS WRONG: 
  The evidence from VOICES.md / OPPORTUNITY.md / FORCES.md shows <Y>.

OUR DIFFERENT BELIEF: 
  We believe <Z>, which means <product implication>.

OUR BEACHHEAD: 
  We start with <specific segment defined by job-context>, because:
  - F1+F2 > F3+F4 for them (switch likely)
  - Q4 outcomes (high importance, low satisfaction) cluster here  
  - Competitor weakness is structurally hardest to fix here

THE STRUCTURAL ADVANTAGE: 
  Competitors can't follow easily because <specific reason — sunk cost / 
  brand position / architectural assumption / customer-base composition>.

WHAT WOULD MAKE US WRONG: 
  This thesis fails if <specific falsifying condition>.
```

The last section is the discipline check. If you can't name a falsifying condition, the thesis is too vague.

## What this skill produces

`.discovery/<topic>/08-wedge/WEDGE.md` containing:

1. **The wedge thesis** in the structure above
2. **Evidence appendix** — Per claim in the thesis, cite which Phase doc supports it
3. **3 alternative wedges considered and rejected** — and why (forces the team to think beyond the first thesis)
4. **The 2-week validation plan** — How to test this thesis cheaply before betting on it

## Process

### Step 1: Load all prior phase outputs
- FRAME.md (candidate JTBDs, hypotheses)
- VOICES.md (verbatim friction)
- JOBS.md (decomposed JTBDs)
- FORCES.md (where the market is switching vs. stuck)
- OUTCOMES.md (desired outcomes)
- 06-competitors/*.md (competitor theses)
- OPPORTUNITY.md (scored outcomes)

### Step 2: Identify the candidate underserved JTBD

From OPPORTUNITY.md, find outcomes with scores ≥ 15. Cluster by JTBD. The JTBD with multiple ripe outcomes IS the wedge candidate.

### Step 3: Identify the wrong-belief

For the wedge JTBD, ask: *What belief about this job do all major competitors share that the evidence contradicts?*

Examples (illustrative):
- **Task management space** — Competitors believe "users want to organize tasks." Evidence shows ADHD users want to *avoid organizing* tasks. Different belief: ADHD task management is anti-organization.
- **Linear vs Jira** — Jira believed "PMs configure workflows." Linear's wrong-belief attack: engineers should not need to configure anything to ship work.
- **Notion vs Confluence** — Confluence believed "documentation is structured." Notion's wrong-belief attack: knowledge is fluid and emerges from notes, not from structure.

### Step 4: State the falsifying condition

What would we need to see in the market for this thesis to be wrong? 
- Customer survey showing the wrong-belief is actually correct
- Competitor releases that prove they can follow our differentiation
- Segment behavior that contradicts our beachhead choice

If you can't name what would falsify the thesis, the thesis is unfalsifiable, and unfalsifiable theses are vapor.

### Step 5: Generate 3 alternative wedges, then reject them

The first wedge thesis is almost never the right one. Force yourself to write 2-3 alternatives, then rigorously reject them. Document the rejection logic. This is the discipline that prevents committing to the obvious-but-shallow wedge.

### Step 6: The 2-week validation plan

Cheap experiments to test the wedge BEFORE betting:
- 5 switch-interview style conversations with users matching the beachhead
- Concept test with a fake-door landing page
- Reverse competitor signal: do they have an internal initiative aimed at our wedge? (LinkedIn job postings often reveal this)
- Small advertising test on the beachhead segment

The validation plan turns the thesis from "we think" to "let's check."

## Anti-patterns

| Symptom | STOP |
|---|---|
| Wedge is a tagline ("the X for Y") | Re-do: name the wrong-belief, evidence, our different belief |
| No falsifying condition | The thesis is unfalsifiable. Rewrite. |
| Beachhead is demographic ("solo developers") | Reframe by job-context ("developers shipping their first product in 30 days") |
| "Structural advantage" is just "we'll execute better" | Find a real architectural / brand / customer-base asymmetry |
| Confirms user's prior thesis without surprise | The discovery failed. Run /pd-iterate. |
| Single wedge considered | Generate 3, reject 2, defend 1 |

## The honesty check

Read the thesis aloud. Then ask:
1. "Would a smart skeptic find this convincing?"
2. "Is the wrong-belief sharp, or am I hand-waving?"
3. "Does the evidence chain actually support the bet?"
4. "Can I name what would change my mind?"

If any answer is "no," the thesis isn't done.

## What comes next

`pd-brief` produces the one-page BRIEF.md, which is the publication-grade synthesis of all phases including this wedge.
