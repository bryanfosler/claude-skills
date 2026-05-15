---
name: pd-mine-voices
description: Use when mining verbatim user friction from public sources (Reddit, App Store, G2, Trustpilot, forums) for a discovery — produces 02-voices/VOICES.md with attributed verbatim quotes, theme clusters, and source-credibility tags.
---

# pd-mine-voices (Phase 02)

You are mining REAL user voices for evidence. **Verbatim quotes only.** Every quote cites its source URL. No paraphrasing. No fabrication.

This is the most defensible AI-tooling application in discovery — and the easiest to do dishonestly. The plugin's credibility depends on this phase.

## What this skill produces

`.discovery/<topic>/02-voices/VOICES.md` with:

1. **Sources actually hit** — Which platforms, with date of mining
2. **Theme clusters** — 5-15 friction themes, each with 2-5 verbatim quotes
3. **Switch stories** — Verbatim "I switched from X to Y because..." narratives (Moesta gold)
4. **Outlier quotes** — Anomalies that defy the obvious pattern (these are signal, not noise)
5. **Volume + confidence tags** — Per theme: how many sources corroborate
6. **Gaps** — What we tried to find but couldn't

## Process

### Step 1: Pick sources for this domain
Reference `references/friction-mining-sources.md`. For each domain (B2B SaaS, Consumer SaaS, Consumer HW, etc.) there's a curated source map.

**Minimum mining rule:** at least 3 platforms for any theme to be a "pattern." One source = anecdote. Two = coincidence. Three+ = signal.

### Step 2: Dispatch `friction-miner` agent

The agent does the heavy WebSearch + WebFetch work. Returns categorized findings. You synthesize.

**Agent brief includes:**
- Topic + candidate JTBDs from FRAME
- Source list with priority
- Minimum quote target (15+ verbatim)
- Verbatim-quote rule
- Source-URL requirement per quote

### Step 3: Cluster into themes

Affinity-diagram the mined quotes into 5-15 themes. A theme requires:
- **2-5 verbatim quotes** supporting it
- **Cross-platform corroboration** (quotes from ≥2 source types)
- **A theme label** that paraphrases nothing — uses the users' anchor language

### Step 4: Extract switch stories

Find "I switched from X to Y" / "I left X for Y" narratives. These are Moesta's highest-signal evidence. Capture verbatim, attribute, note the Push/Pull/Habit/Anxiety implied.

### Step 5: Flag outliers
Anomalies are signal. If most users praise feature X but one user says they fired the product *because* of feature X, capture it. Phase 04 will use it.

### Step 6: Volume + confidence per theme

For each theme, tag:
- **Quote count**: how many quotes support
- **Source diversity**: number of distinct platforms
- **Confidence**: Strong (5+ quotes, 3+ platforms) / Moderate (3-4 quotes, 2 platforms) / Weak (1-2 quotes)

### Step 7: Gaps section
What did you look for and not find? This is honesty. Missing evidence is data.

### Step 8: Run the validator (Iron Rule enforcement)

After writing VOICES.md, run:
```bash
python3 .../product-discovery/scripts/audit-voices.py .discovery/<topic>/02-voices/VOICES.md
```

This is a HARD gate. Exit code 2 = Iron Rule violated (fix before proceeding). Exit code 1 = warnings (address before shipping). Exit code 0 = pass.

The validator checks:
- 15+ verbatim quotes with source URLs
- Every theme has 2+ quotes
- Every theme has 2+ distinct domains (cross-platform corroboration)
- Switch stories section present with 3+ entries
- Gaps section present
- No `[SYNTHETIC EXAMPLE]` tags appearing as evidence

If the validator fails: don't paper over it. Dispatch `friction-miner` again to fill the specific gaps, OR write `INSUFFICIENT EVIDENCE — needs deeper mining` in the affected themes.

## The verbatim-or-nothing rule

❌ NEVER: "Users said the mobile app was bad."
✅ ALWAYS: 
> "Sunsama's mobile is genuinely embarrassing for a tool that costs $20/month. I can barely add a task on the train." — [reddit.com/r/productivity/comments/xyz](url)

If you don't have a real quote, write `INSUFFICIENT EVIDENCE — needs deeper mining` and move on.

## Source credibility weights

| Source | Credibility | Notes |
|---|---|---|
| G2 verified-purchase reviews | High | But check for astroturf |
| App Store 1-3 star reviews | High volume, mixed signal | Look for detail |
| Reddit niche subreddits | High signal | But loud voices skew |
| HN comments on launches | High signal for dev tools | |
| Product Hunt "alternatives to X" | High signal | Pre-structured friction |
| Trustpilot | Moderate | More for marketplaces |
| Twitter/X | Variable | Verify with another source |
| Marketing/PR articles | Low | They're sales material |

## Astroturf detection

Red flags:
- Identical phrasing across reviews
- Cluster of 5-star reviews same week
- Generic praise without specifics
- Reviewer has no other activity

When detected, exclude and note in gaps.

## What success looks like

A VOICES.md with 30+ verbatim quotes attributed to source URLs, clustered into 8-12 themes with cross-platform corroboration, including 5+ switch stories. Confidence tags per theme.

A skeptical reader could click every URL and verify every quote.

## Anti-patterns

| Symptom | STOP |
|---|---|
| About to write "Users complain about X" without a quote | Find a real quote or write INSUFFICIENT EVIDENCE |
| Theme based on 1 quote | Not a theme yet — gather more or flag as weak |
| Paraphrasing because the quote is long | The exact words carry the meaning. Quote verbatim, even if long. |
| Only mining one source | Cross-platform corroboration required. Hit ≥3. |
| Confirmation bias — only quotes that match prior thesis | Actively look for *contradicting* quotes too |

## What comes next

`pd-jtbd` (Phase 03) uses VOICES.md to decompose actual jobs from real evidence.
