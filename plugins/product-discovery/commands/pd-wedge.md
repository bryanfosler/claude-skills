---
description: Synthesize the underserved-JTBD wedge thesis from scored outcomes and competitor teardowns
allowed-tools: Read, Write, Edit
---

# /pd-wedge

Name the bet. Identify the wrong-belief competitors share that our evidence contradicts.

## Usage

```
/pd-wedge                                # uses current .discovery/<topic>/
/pd-wedge --topic <slug>                 # specify discovery
```

## What happens

Invokes `pd-wedge` skill which reads all prior phase deliverables and produces the wedge thesis with this exact structure:

- **THE BELIEF WE'RE ATTACKING** — Competitors believe X about the job
- **WHY THIS BELIEF IS WRONG** — The evidence from VOICES/OPPORTUNITY/FORCES shows Y
- **OUR DIFFERENT BELIEF** — We believe Z, which means [product implication]
- **OUR BEACHHEAD** — Specific segment defined by job-context where F1+F2 > F3+F4 most strongly
- **THE STRUCTURAL ADVANTAGE** — Why competitors can't easily follow
- **WHAT WOULD MAKE US WRONG** — Falsifying condition (required)

Also generates 3 alternative wedges and the rejection logic, plus a 2-week validation plan.

## Output

`.discovery/<topic>/08-wedge/WEDGE.md`

## Anti-patterns prevented

- "We'll be the X for Y" taglines (rejected as not a real wedge)
- Unfalsifiable theses (must name what would make us wrong)
- Demographic beachheads (must be job-context defined)
- "Structural advantage" is just "we'll execute better" (must be real asymmetry)
- Single wedge considered (must generate 3, reject 2, defend 1)

$ARGUMENTS
