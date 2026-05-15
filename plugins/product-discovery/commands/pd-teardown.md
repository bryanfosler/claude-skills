---
description: Strategic teardown of a single competitor - theory-of-mind, four fits, firers, wedge analysis
allowed-tools: Agent, Read, Write, Edit, WebSearch, WebFetch
---

# /pd-teardown

Run an elite-tier competitor teardown. Not a feature comparison. Strategic theory-of-mind reconstruction.

## Usage

```
/pd-teardown Sunsama
/pd-teardown Linear --context "developer tools competitive landscape"
/pd-teardown "Apple Reminders"
```

## What happens

Invokes `pd-teardown` skill which dispatches the `competitor-analyst` agent to:
1. Reconstruct their **theory of mind** (what JTBD they believe; what incumbent they think is broken)
2. Analyze the **four fits** (Market-Product, Product-Channel, Channel-Model, Model-Market)
3. Build a **firers profile** (Moesta forces on switchers-away)
4. Code their **reviews for JTBD signals** (40-60 reviews thematically)
5. Read their **pricing page as strategy**
6. Sign up and document the **first 10 minutes** of onboarding
7. Apply **Wardley evolution mapping** to their differentiators
8. Produce a **thesis output** (THEIR THEORY / THEIR WEDGE / WHERE THEY'RE VULNERABLE / OUR OPENING)

## Output

`.discovery/<topic>/06-competitors/<slug>.md` or `./<slug>.md` if no discovery in progress.

## Time

15-30 minutes per competitor at standard depth.

## What it WILL NOT do

- Produce a feature comparison table as the primary output
- Praise or criticize - strategy is neutral
- Make claims about pricing/features without source URLs

$ARGUMENTS
