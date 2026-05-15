---
description: Fast product discovery (D1-D3 only - frame, mine voices, decompose JTBDs) ~30 min
allowed-tools: Agent, Bash, Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
---

# /pd-quick

A 30-minute sanity check for "should I even go deep on this?"

## Usage

```
/pd-quick "AI-powered weather app for hikers"
```

## What happens

Runs only Phases 01-03 of the full discovery:
1. Frame (market + candidate JTBDs)
2. Mine voices (15+ verbatim quotes, 3 themes minimum)
3. JTBD decomposition (1-2 primary JTBDs)

Writes a `.discovery/<topic>/BRIEF-quick.md` - a 1/2-page summary of whether deeper investigation is warranted.

## When to use

- Bryan has a fuzzy product idea and wants to know if it's worth pursuing
- Quick competitive scan before deciding to GSD-plan a phase
- "Is the problem real, or am I making it up?"

## When NOT to use

- Real strategic discovery for a project Bryan is committing to - use `/pd-discover` for those
- Single-competitor research - use `/pd-teardown`
- After a `/pd-discover` already ran - use `/pd-iterate`

$ARGUMENTS
