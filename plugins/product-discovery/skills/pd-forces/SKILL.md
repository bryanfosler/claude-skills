---
name: pd-forces
description: Use when mapping Moesta's Forces of Progress (Push, Pull, Habit, Anxiety) per primary JTBD using mined user evidence — produces 04-forces/FORCES.md. The 4-forces equation (F1+F2 > F3+F4) determines whether a switch happens.
---

# pd-forces (Phase 04)

You are running Bob Moesta's Forces of Progress analysis. This is the highest-leverage move in JTBD — most product teams skip it because they don't realize **anxiety and habit win more often than push and pull**.

Load: `references/forces-of-progress.md` before producing output.

## The equation

**Switch happens when: F1 + F2 > F3 + F4**

- **F1 (Push)** — Frustration with current state. The dissatisfaction pushing user away.
- **F2 (Pull)** — Attraction to the new solution. Hope, capability, status.
- **F3 (Habit)** — Inertia of present. "I've always done it this way."
- **F4 (Anxiety)** — Fear of switching. Risk, learning curve, loss aversion.

Most roadmaps focus on F2 (adding features). Moesta's counter-intuitive finding: **more features increase F4 (anxiety) faster than F2 (pull).** Adoption gets *worse*.

## What this skill produces

`.discovery/<topic>/04-forces/FORCES.md` with:

For each primary JTBD from Phase 03:

1. **Forces map** — 4 columns (F1/F2/F3/F4) with 3-5 verbatim quotes per column
2. **Net force calculation** — Qualitative assessment: does F1+F2 > F3+F4? By how much?
3. **The leverage point** — Which force, if shifted, would tip the equation most?
4. **The honest assessment** — Is this market currently switching or stuck?
5. **What competitors are doing for each force** — Brief pointer; Phase 06 deep-dives

## Process

### Step 1: For each primary JTBD, code the VOICES quotes by force

Re-read 02-voices/VOICES.md. For every quote, tag it as evidence of F1, F2, F3, or F4 (one quote can be multiple).

**Examples of force-coding:**

> "I tried Notion for 3 months but the database setup overhead never felt worth it." 
→ **F4 (anxiety)** for Notion adoption: setup cost felt too high

> "Sunsama's daily ritual genuinely changed how I plan."
→ **F2 (pull)** for Sunsama: clear benefit story

> "I've used Apple Reminders for 10 years and it's just where things live."
→ **F3 (habit)** for Apple Reminders: incumbent inertia

> "Trying yet another task app feels exhausting. I'm tired of migrating."
→ **F4 (anxiety)** for any new app: switching fatigue

### Step 2: Map per JTBD

For each primary JTBD, build a 4-column table. Include 3-5 quotes per column (verbatim, attributed).

### Step 3: Calculate net force

For each JTBD, write a qualitative assessment:
- F1 + F2 sum: **Strong / Moderate / Weak**
- F3 + F4 sum: **Strong / Moderate / Weak**
- Net: **Switch likely / Stuck / Highly stuck**

This is honest qualitative analysis — don't fake precision with made-up numbers.

### Step 4: Identify the leverage point

Which force, if changed, would tip the equation? Usually one of:
- **Reduce F4** (lower switching anxiety: migration tooling, free trial, gradual onboarding)
- **Increase F1** (sharpen the pain: not by manufacturing FUD, but by helping users articulate latent frustration)
- **Reduce F3** (break habit: integrate with existing workflow before replacing)
- Rarely: **Increase F2** (more features) — usually backfires

### Step 5: Honest market assessment

Is the market in a switching moment? Some markets are stuck (F3+F4 dominates regardless of new products). Document it. Don't pretend a stuck market is a switching one.

### Step 6: Flag competitor moves per force

Brief pointer for Phase 06: which competitors are actively reducing F4? Building strong F2? Locking in F3? This is teardown raw material.

## Quick reference table

| Force | What it is | How to elicit | Typical phrasing in quotes |
|---|---|---|---|
| F1 Push | Frustration with current | "What's broken right now?" | "I'm tired of...", "It drives me crazy that..." |
| F2 Pull | Attraction to new | "What were you hoping it would do?" | "I thought it would let me...", "The promise was..." |
| F3 Habit | Inertia of present | "Why didn't you switch sooner?" | "I've always...", "It's just where..." |
| F4 Anxiety | Fear of new | "What worried you about switching?" | "I was afraid that...", "I didn't want to lose..." |

## The counter-intuitive insight

**Reducing F4 usually beats adding F2.** Migration tooling, "import your data," "keep your shortcuts working" — these often drive more switches than any single new feature.

Linear's wedge against Jira: lowered F4 with migration tooling, kept F3 by being keyboard-driven (engineer habit), reduced F1 with 50-100ms response vs Jira's 200-500ms. They didn't out-feature Jira.

## Anti-patterns

| Symptom | STOP |
|---|---|
| Only listing F1 + F2; ignoring F3/F4 | Anti-pattern. F3+F4 usually wins. Re-balance. |
| Inventing scores instead of qualitative assessment | Be honest. Strong/Moderate/Weak with evidence. |
| Treating "stuck market" as failure to motivate | Sometimes the market truly is stuck. That's data. |
| Force-coding without verbatim quotes | Every force claim needs 3+ quotes. |

## What comes next

Phase 05 (`pd-outcomes`) translates the dominant JTBDs + their force maps into Ulwick-syntax desired outcomes.
