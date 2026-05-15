---
description: Show current discovery state - which phases are done, what's pending, what's blocked
allowed-tools: Bash, Read, Glob
---

# /pd-status

Where are you in the current discovery?

## Usage

```
/pd-status                       # current discovery
/pd-status --topic <slug>        # specific discovery
/pd-status --all                 # all discoveries in current dir
```

## What happens

Inspects `.discovery/<topic>/STATE.md` and the phase directories. Reports:

- Current phase
- Phases completed (with timestamp and quote counts)
- Phases pending
- Evidence depth (quote count, source platform count)
- Iteration depth (D-number)
- Open questions / gaps the critic flagged
- Recommended next action

## Example output

```
Discovery: cairn-adhd-task-management
Status: D4, Phase 04 (Forces) in progress

✓ 01-frame    (committed, 3 candidate JTBDs)
✓ 02-voices   (committed, 28 quotes across 5 platforms, 7 themes)
✓ 03-jobs     (committed, 2 primary JTBDs decomposed)
○ 04-forces   (in progress)
○ 05-outcomes
○ 06-competitors
○ 07-scoring
○ 08-wedge

Next: complete 04-forces, then parallel dispatch 05 + 06.
```

$ARGUMENTS
