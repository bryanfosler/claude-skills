---
description: Run JTBD decomposition (Moesta school) on a market or existing voice corpus
allowed-tools: Agent, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# /pd-jtbd

Apply Moesta-school Jobs-to-be-Done decomposition. Context, not pain. Switch-interview structure.

## Usage

```
/pd-jtbd "current ADHD task apps"        # mines voices first, then JTBDs
/pd-jtbd --from .discovery/<topic>/02-voices/VOICES.md   # uses existing voices
/pd-jtbd --interviews path/to/transcripts/   # uses interview transcripts
```

## What happens

Invokes `pd-jtbd` skill which:
1. Reads VOICES.md (or runs `pd-mine-voices` first if missing)
2. Clusters quotes by causal pathway (Push + Pull combinations)
3. Decomposes 1-3 primary JTBDs with functional/emotional/social layers
4. Writes Moesta-syntax job statements as synthesis
5. Names what current products get *fired* and why
6. Flags anomalies (the richest signal)

Writes to `.discovery/<topic>/03-jobs/JOBS.md`.

## What it WILL NOT do

- Use the job-statement format as an interview question (it's synthesis only)
- Stop at functional layer (real jobs have emotional + social too)
- Discard anomalies (they're the richest signal)
- Demographic segmentation (causal/situational clusters only)

$ARGUMENTS
