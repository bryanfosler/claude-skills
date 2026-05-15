---
name: pd-jtbd
description: Use when decomposing Jobs-to-be-Done from mined user voices or interview transcripts — applies Moesta-school JTBD (context-not-pain, switch-interview structure, functional/emotional/social layers) and produces 03-jobs/JOBS.md. Can run standalone via /pd-jtbd or as Phase 03 of full discovery.
---

# pd-jtbd (Phase 03)

You are doing real Moesta-school JTBD decomposition — not the generic "pain and gain" version. **Context, not pain.** The job statement is a *synthesis* tool, not a research question.

Load: `references/jtbd-moesta.md` before producing output.

## What this skill produces

`.discovery/<topic>/03-jobs/JOBS.md` with:

1. **Primary JTBDs** — 1-3 jobs the segment is *actually* hiring (evidence-backed)
2. **Functional / Emotional / Social layers** per job
3. **Job statement** (Moesta syntax) per JTBD
4. **The context** — situation that makes the job urgent (Moesta's key insight)
5. **What gets fired** — current products and why users left them
6. **Anomaly notes** — when the evidence "makes no sense" until context is added

## The core Moesta insight

> "The context makes the irrational rational. So the moment you hear a story, you go, 'I can't believe that,' nine times out of 10, it's because you don't have the rest of the story." — Bob Moesta

If something in the user voices seems irrational, you're missing context. Don't exclude it — dig.

## Process

### Step 1: Read VOICES.md (Phase 02)
Load all mined quotes. Pay special attention to **switch stories** ("I left X for Y because...") — these are highest-signal.

### Step 2: Cluster by causal pathway, not attribute

Moesta's method: find which Push (frustration) + Pull (hope) combinations co-occur across multiple users. These causal clusters are the actual jobs.

❌ Anti-pattern: "Senior PMs need X, Junior PMs need Y" (demographic segmentation)
✅ Pattern: "When deadline is in <48 hours, users hire a tool to consolidate scattered context; when planning >2 weeks out, they hire one to keep options open" (situational segmentation)

### Step 3: For each cluster, decompose 3 layers

**Functional** — What's the practical outcome? (Concrete action / measurable change)
**Emotional** — How does the user want to feel during/after?
**Social** — How do they want to be seen / how does it affect their relationships?

A real job has all three. If you can only name functional, you haven't dug deep enough.

### Step 4: Write job statements

Format (Moesta): *"When [situation], I want to [motivation], so I can [outcome]."*

**Critical:** This is a synthesis output, not an interview question. You write it AFTER clustering, not as a prompt to users.

### Step 5: Name what gets fired

For each JTBD, list current products/methods that users hired then fired, and verbatim reasons (from VOICES.md). This sets up Phase 06's competitor teardowns.

### Step 6: Flag anomalies

Quotes that don't fit obvious clusters. Don't discard. They're the richest signal — they reveal contexts you haven't surfaced yet. Mark each as `[ANOMALY — investigate]` and propose what context might make it rational.

### Step 7: When JTBD is NOT the right tool — explicit check

Moesta is emphatic that JTBD fails in three cases:
1. **No-real-choice markets** (employer-selected health insurance, monopoly utilities)
2. **Deeply habitual purchases** (gum, gas station coffee)
3. **Predetermined conclusions** (when stakeholder wants confirmation, not insight)

If the discovery falls in one of these, document it in JOBS.md and recommend a different methodology.

## Quick reference

| Move | Source |
|---|---|
| "Context > pain" frame | Moesta podcast (Lenny's Newsletter) |
| Switch interview structure | Re-Wired Group methodology |
| 6-phase timeline (First Thought → ... → Ongoing Use) | Moesta's canonical interview |
| Functional/Emotional/Social | Christensen "When Coffee and Kale Compete" |
| Job statement is synthesis | Moesta explicit warning |

## Anti-patterns

| Symptom | STOP |
|---|---|
| "Users want feature X" framing | Features are solutions; jobs are situations. Re-decompose. |
| Job statement used as interview question | Synthesis only. Never give it to users. |
| Only functional layer captured | Dig for emotional + social. Real jobs have all three. |
| Demographic segmentation | Switch to causal/situational clusters. |
| Anomalies discarded | They're the richest signal. Investigate context. |
| "Pain points" framing | Anti-pattern. Frame as context, not pain. |

## Standalone use

When invoked via `/pd-jtbd "topic"` (not as Phase 03 of full flow):
- If `.discovery/<topic>/02-voices/VOICES.md` exists, use it
- Otherwise, ask user for either: (a) interview transcript paths, or (b) "first mine then JTBD" — in which case dispatch Phase 02 first

## What comes next

Phase 04 (`pd-forces`) maps Push/Pull/Habit/Anxiety per primary JTBD using the same evidence.
