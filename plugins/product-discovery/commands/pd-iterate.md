---
description: Deepen the current discovery brief by dispatching the thesis-critic and filling specific gaps
allowed-tools: Agent, Read, Write, Edit, WebSearch, WebFetch
---

# /pd-iterate

The 10x loop. Find what's missing and go get it. **New evidence, not rephrasing.**

## Usage

```
/pd-iterate                              # iterate current discovery
/pd-iterate --topic <slug>               # specify which discovery
/pd-iterate --aggressive                 # higher-depth gap fills
```

## What happens

Invokes `pd-iterate` skill which:

1. Reads the prior BRIEF.md
2. Dispatches `thesis-critic` agent — returns structured gap report:
   - Evidence gaps (themes with <3 quotes, claims without source URLs)
   - Methodology gaps (forces map incomplete, outcomes not Ulwick-syntax)
   - Competitor gaps (teardowns shallow, missing key competitors)
   - Wedge gaps (no falsifying condition, generic tagline)
   - Confirmation-bias check (re-finding evidence vs. finding new)
3. Dispatches focused agents to fill exactly those gaps
4. Updates affected phase docs
5. Re-runs `pd-brief` to produce BRIEF-vN+1.md
6. Writes meta-vN+1.md documenting material changes

## Output

`.discovery/<topic>/BRIEF-vN+1.md` + `meta-vN+1.md`

## Stop rule

When critic returns fewer than 3 HIGH-improvement gaps, or 3 consecutive iterations show low material change → "thesis stable."

## What success looks like over iterations

| Depth | What's new |
|---|---|
| D2 (initial) | Surface quotes, 3 competitors named |
| D3 | Cross-platform corroboration, switch stories surfaced |
| D4 | Full 4 forces map with quote-backed evidence |
| D5 | Outcomes Ulwick-compliant, scored |
| D6 | 4-6 competitors at strategic depth, wedge thesis sharp |
| D7+ | Critic identifies progressively finer gaps; thesis stabilizes |

D7 is **categorically** better than D2 — that's the 10x claim.

$ARGUMENTS
