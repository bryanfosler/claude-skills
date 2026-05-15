---
name: pd-frame
description: Use when starting product discovery on a new market/product question — defines the market, surfaces candidate JTBDs, captures hypotheses, and writes 01-frame/FRAME.md as the foundation for all subsequent phases.
---

# pd-frame (Phase 01)

The first phase of a discovery. You define WHAT we're researching, the candidate jobs users might be hiring a product for, and the hypotheses you'll test in later phases.

## What this skill produces

`.discovery/<topic>/01-frame/FRAME.md` with these sections:

1. **Topic statement** — One paragraph: who, what, why now
2. **Market definition** — Job-based (Ulwick syntax) preferred over demographic
3. **Candidate JTBDs** — 3-7 hypotheses about what users are hiring this product for
4. **Hypotheses to test** — Specific, falsifiable claims for later phases
5. **Competitors to teardown** — Provisional list (top 3-5, will be refined in Phase 06)
6. **Friction sources to mine** — Where Phase 02 will look
7. **Context flags** — software/hardware/hybrid, B2B/B2C, 0-to-1/scale

## Process

### Step 1: Topic to one paragraph
Compress the user's question into: *"For [user segment] doing [job] in [context], we want to understand [specific question]."*

If user's input is vague, ask one sharpening question. Maximum.

### Step 2: Market definition (Ulwick-job-based)

❌ Demographic: "Knowledge workers in companies of 50-500"
✅ Job-based: "Anyone trying to coordinate work across 3+ tools without losing context"

The job-based frame survives technology shifts; the demographic frame doesn't.

### Step 3: Candidate JTBDs

Brainstorm 3-7 jobs users might be hiring this product for. Use Moesta's syntax:
> When [situation], I want to [motivation], so I can [outcome].

Examples for "AI task management for ADHD":
- When my brain freezes on a 5-option task list, I want a coach that offers ONE next thing, so I can actually move
- When my external systems require effort to maintain, I want a tool that captures from anywhere with zero friction, so I can trust it as my external brain
- When I miss medication or appointments, I want gentle proactive nudges, so I can stop relying on guilt-based recovery

**Mark each candidate** with confidence level (`HYPOTHESIS` vs `INFERRED FROM PRIOR EVIDENCE`).

### Step 4: Hypotheses to test

For each candidate JTBD, write 1-2 falsifiable claims. These become Phase 02's mining targets.

Example: "ADHD users abandon Sunsama within 30 days because mobile capture is broken" → Phase 02 looks for Reddit/review quotes that confirm or refute.

### Step 5: Competitor list

3-5 names. Mark each as:
- **Direct** (same JTBD, similar audience)
- **Adjacent** (same JTBD, different audience)
- **Disruptor** (different JTBD, same audience)

### Step 6: Friction sources

Reference `references/friction-mining-sources.md`. List the 4-6 sources Phase 02 will hit, by domain.

### Step 7: Context flags

Mark each:
- **Domain**: software / hardware / hybrid
- **Audience**: B2B / B2C / B2D (developer)
- **Stage**: 0-to-1 / growth / scale / category-redefining
- **HW fidelity stage** (if applicable): sketch / foam / 3D-print / works-like / DVT / PVT

If hardware, invoke `hw-context-adapter` agent before completing frame. It adds: fidelity-ladder alignment, BOM-cost constraints, dual-user flag.

## Quick reference

| Section | Length |
|---|---|
| Topic statement | 1 paragraph |
| Market definition | 1 sentence |
| Candidate JTBDs | 3-7 bullets, Moesta syntax |
| Hypotheses | 1-2 per JTBD |
| Competitors | 3-5 with category tags |
| Friction sources | 4-6 with domain tags |
| Context flags | 4 tags |

## Anti-patterns

| Symptom | Fix |
|---|---|
| Demographic market definition | Reframe job-based |
| Candidate JTBDs that are features ("I want notifications") | Rewrite as outcomes |
| Hypotheses too vague to test ("users care about UX") | Specific, falsifiable, source-checkable |
| Skipping HW adapter for physical product | Always run it for hardware |

## Output template

See `templates/frame.md`.

## What comes next

Once `FRAME.md` is committed, `pd-orchestrator` dispatches Phase 02 (`pd-mine-voices`) and Phase 06 (competitor teardowns) in parallel.
