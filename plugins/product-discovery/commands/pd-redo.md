---
description: Re-enter a specific phase of an existing discovery to deepen or revise
allowed-tools: Agent, Read, Write, Edit, WebSearch, WebFetch
---

# /pd-redo

Re-enter a single phase with the option to deepen or replace its deliverable. Used when one phase needs more work but the rest of the discovery is fine.

## Usage

```
/pd-redo 02-voices                       # re-mine for more quotes
/pd-redo 04-forces                       # rebuild the forces map
/pd-redo 06-competitors --add Motion     # add a missed competitor
```

## What happens

Invokes the relevant phase skill (`pd-mine-voices`, `pd-forces`, `pd-teardown`, etc.) on the existing discovery. The phase deliverable is updated, not replaced (versioned as `<DELIVERABLE>-v2.md`).

## When to use vs. /pd-iterate

- `/pd-redo` — *I know exactly which phase needs work* (faster, surgical)
- `/pd-iterate` — *Let the critic tell me where to dig* (more thorough)

## What it does NOT do

- Re-run downstream phases automatically (use `/pd-iterate` for that)
- Discard the prior deliverable (always versioned)

$ARGUMENTS
