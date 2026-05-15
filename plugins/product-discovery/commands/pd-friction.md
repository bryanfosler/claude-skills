---
description: Mine verbatim user friction from Reddit, App Store, G2, Trustpilot, forums for a market
allowed-tools: Agent, Read, Write, WebSearch, WebFetch
---

# /pd-friction

Mine real user voices. Verbatim quotes with source URLs only.

## Usage

```
/pd-friction "ADHD task management apps"
/pd-friction "B2B contract review tools" --domain b2b-saas
/pd-friction "consumer headphones" --domain consumer-hw
```

## What happens

Invokes `pd-mine-voices` skill which dispatches the `friction-miner` agent to hit domain-appropriate sources (curated in `references/friction-mining-sources.md`):

- **B2B SaaS** → G2, r/sysadmin, product-specific subreddits, HN
- **Consumer SaaS** → App Store 1-3 stars, Reddit switcher threads, Product Hunt
- **Consumer HW** → Amazon verified-purchase, head-fi/r/headphones, RTINGS, YouTube comments
- **Industrial HW** → eng-tips.com, r/PLC, r/embedded, Digi-Key Q&A
- **Dev Tools** → GitHub Issues on competitor repos, Stack Overflow, HN
- **Creator Tools** → r/editors, YouTube tutorial comments

## Output

`.discovery/<topic>/02-voices/VOICES.md` — categorized themes with verbatim quotes, source URLs, switch stories, outliers, and confidence tags per theme.

## Discipline

- **Verbatim only** — no paraphrasing
- **Cross-platform corroboration** — minimum 3 platforms per theme
- **Astroturf detection** — identical phrasing across reviews is a red flag
- **Honest gaps** — what we looked for and couldn't find

$ARGUMENTS
