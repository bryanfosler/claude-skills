---
name: pd-brief
description: Use when synthesizing the final one-page discovery thesis — pulls from all 8 phase deliverables (frame, voices, jobs, forces, outcomes, competitors, scoring, wedge) into BRIEF.md, the publication-grade output a principal PM could share with their CEO without embarrassment.
---

# pd-brief (Final synthesis)

You are writing the one document that gets read by everyone. **One page** if possible, two max. Every claim cites which phase document supports it. The brief is publication-grade or it failed.

## What this skill produces

`.discovery/<topic>/BRIEF.md` with this exact structure:

```markdown
# Discovery Brief: <topic>

**Depth**: D<N> | **Date**: <date> | **Status**: <draft|reviewed|validated>

---

## The wedge (1 paragraph)
<The wrong-belief, our different belief, the beachhead. Lifted from WEDGE.md.>

## The evidence (3-5 verbatim quotes)
> "<quote>" — <source URL>
> "<quote>" — <source URL>
[3-5 highest-signal verbatim quotes from VOICES.md that ground the wedge.]

## The opportunity (top 3 outcomes)
1. <Ulwick outcome> — Opportunity score **<N>** ([Ripe / Underserved])
2. <Ulwick outcome> — Opportunity score **<N>** ([Ripe / Underserved])
3. <Ulwick outcome> — Opportunity score **<N>** ([Ripe / Underserved])

## The forces (where the market is)
F1+F2 = <strong/moderate/weak> | F3+F4 = <strong/moderate/weak> | Net = <switch likely / stuck / moving>

The leverage point: <which force to shift>.

## The competitive frame (one line per competitor)
- **<Competitor A>**: Their theory is X. Vulnerable on Y. (→ `06-competitors/A.md`)
- **<Competitor B>**: Their theory is X. Vulnerable on Y.
- **<Competitor C>**: Their theory is X. Vulnerable on Y.

## What would make this wrong
<Falsifying condition. Lifted from WEDGE.md.>

## The 2-week validation plan
- [ ] <Experiment 1>
- [ ] <Experiment 2>
- [ ] <Experiment 3>

## Confidence
- **Evidence depth**: <Low / Moderate / High>
- **Discovery depth**: D<N>
- **Source diversity**: <N> platforms across <N> distinct quotes
- **Open questions**: <count>

---

### Trace map
- Frame → `01-frame/FRAME.md`
- Voices → `02-voices/VOICES.md`
- Jobs → `03-jobs/JOBS.md`
- Forces → `04-forces/FORCES.md`
- Outcomes → `05-outcomes/OUTCOMES.md`
- Competitors → `06-competitors/`
- Scoring → `07-scoring/OPPORTUNITY.md`
- Wedge → `08-wedge/WEDGE.md`
```

## Process

### Step 1: Read all phase deliverables
Verify each exists. If any are missing or marked `INSUFFICIENT EVIDENCE`, decide:
- **Recommend `/pd-iterate` first** — better than shipping a weak brief
- **OR ship a draft brief** with explicit "Discovery is shallow; iterate before committing" header

### Step 2: Distill the wedge thesis
From WEDGE.md, compress to 1 paragraph. Preserve the wrong-belief + our different belief + beachhead. Cut all qualifiers.

### Step 3: Select the 3-5 grounding quotes
From VOICES.md, pick the quotes that most viscerally support the wedge. **Verbatim, attributed.**

### Step 4: List the top 3 outcomes
From OPPORTUNITY.md, the 3 highest-scoring outcomes that map to the wedge JTBD. Show the score and band.

### Step 5: Summarize the forces in 2 lines
From FORCES.md: net direction + leverage point.

### Step 6: One-line teardowns
For each competitor (3-5 total): one sentence on theory + one sentence on vulnerability. Link to full teardown.

### Step 7: The honest confidence
- Evidence depth: how many verbatim quotes total, across how many platforms
- Discovery depth: D number
- Source diversity: count
- Open questions: known gaps

This is where the brief is honest about its own limitations. A brief that claims high confidence based on D2 evidence is dishonest.

### Step 8: Trace map
Every section links to the phase document that supports it. The brief is a navigation layer, not a replacement.

## Length discipline

**One page if possible. Two max.**

If a section runs long, cut. If forced to choose between "complete" and "decisive," choose decisive. A long brief is a brief that didn't pick.

## Anti-patterns

| Symptom | STOP |
|---|---|
| Brief mentions "users want..." without verbatim quote | Pull the actual quote |
| Confidence claimed without phase evidence | Either downgrade confidence or iterate first |
| Wedge runs 3 paragraphs | Compress. One paragraph or it's not sharp. |
| All sections complete but the wedge isn't sharp | The wedge is the brief. Without it, scrap and re-do. |
| No falsifying condition | The brief is unfalsifiable. Add one or downgrade to "exploratory." |

## Quality gate

### Automatic (structural validator)

After writing BRIEF.md, run:
```bash
python3 .../product-discovery/scripts/audit-brief.py .discovery/<topic>/BRIEF.md
```

This is a HARD gate. Exit code 2 = Iron Rule / wedge discipline violated. Exit code 1 = warnings. Exit code 0 = structural pass.

The validator checks:
- Wedge, Evidence, Falsifying-condition sections present
- Evidence section has 3+ verbatim quotes WITH source URLs
- Opportunity scores (if shown) are tagged `[MODEL ESTIMATE]`
- Wedge does NOT match generic-tagline patterns ("we'll be the X for Y", "X but better")
- Falsifying condition is specific (not "if our assumptions are wrong")
- Trace map + Confidence sections present

If the validator fails: this is structural feedback, not stylistic. Fix the underlying issue (re-mine for quotes, sharpen the wedge, name a specific falsifying condition) before claiming the brief is ready.

### Manual (the principal-PM gut check)

Beyond the validator, read the brief aloud. Ask:
1. "Would I share this with a CEO without flinching?"
2. "Does every claim trace to evidence I can defend?"
3. "Is the wedge a real bet, or a marketing tagline?"
4. "If this is wrong, what specifically did I miss?"

If any "no" — `/pd-iterate` before shipping.

## What comes next

If brief is strong: ship. Optionally `/pd-iterate` once more for a deeper version.
If brief is weak: `/pd-iterate` to fill gaps the critic identifies, then re-synthesize.
