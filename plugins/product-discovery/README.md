# Product Discovery Plugin

An 8-phase product discovery pipeline grounded in Moesta-school JTBD and Ulwick's ODI methodology. Produces a defensible, evidence-backed strategic brief from a market question.

## When to Use

You have a market question, product bet, or strategic uncertainty and need to move from "we think" to "the evidence says." Run the full pipeline or individual phases standalone.

## What It Produces

All output lands in `.discovery/<topic>/` relative to your working directory:

```
.discovery/<topic>/
├── 01-frame/FRAME.md           # Market definition, candidate JTBDs, hypotheses
├── 02-voices/VOICES.md         # Verbatim user friction from public sources
├── 03-jobs/JOBS.md             # Moesta-syntax JTBD decomposition
├── 04-forces/FORCES.md         # Push/Pull/Habit/Anxiety per job
├── 05-outcomes/OUTCOMES.md     # Ulwick-syntax desired outcomes
├── 06-competitors/TEARDOWN.md  # Strategic competitor teardowns
├── 07-scoring/OPPORTUNITY.md   # Opportunity scores (I + max(I-S, 0))
├── 08-wedge/WEDGE.md           # Underserved-JTBD wedge thesis
└── BRIEF.md                    # Publication-grade one-page thesis
```

## Quick Start

```
/pd-quick "bike computers for ultra-endurance riders"
```

Runs phases 1-3 (frame, mine voices, JTBD) in ~30 min. For the full 8-phase pipeline:

```
/pd-discover "bike computers for ultra-endurance riders"
```

## Skills (Slash Commands)

### Orchestrators
| Command | What it does |
|---------|-------------|
| `/pd-discover` | Full 8-phase pipeline (D2-D6 depth) |
| `/pd-quick` | Fast D1-D3 only: frame, voices, JTBDs (~30 min) |
| `/pd-status` | Show current discovery state — done, pending, blocked |
| `/pd-iterate` | Deepen an existing brief by finding and filling evidence gaps |
| `/pd-redo` | Re-enter a specific phase to revise or deepen |

### Individual Phases
| Command | Phase | Output |
|---------|-------|--------|
| `/pd-frame` | 01 | FRAME.md — market definition, candidate JTBDs, hypotheses |
| `/pd-mine-voices` | 02 | VOICES.md — verbatim quotes from Reddit, App Store, G2, forums |
| `/pd-jtbd` | 03 | JOBS.md — Moesta-syntax job decomposition |
| `/pd-forces` | 04 | FORCES.md — Push, Pull, Habit, Anxiety per job |
| `/pd-outcomes` | 05 | OUTCOMES.md — Ulwick-syntax desired outcome statements |
| `/pd-teardown` | 06 | TEARDOWN.md — strategic competitor teardown (not feature comparison) |
| `/pd-score` | 07 | OPPORTUNITY.md — Ulwick opportunity scores with threshold bands |
| `/pd-wedge` | 08 | WEDGE.md — underserved-JTBD wedge thesis |
| `/pd-brief` | Final | BRIEF.md — one-page publication-grade thesis |

### Standalone Tools
| Command | What it does |
|---------|-------------|
| `/pd-friction` | Mine user friction from public sources for any market (no discovery context needed) |
| `/pd-teardown <name>` | Run a standalone competitor teardown |

## Agents

The plugin dispatches specialized agents for compute-heavy work:

| Agent | Role |
|-------|------|
| **friction-miner** | Mines verbatim quotes from 3+ public platforms |
| **competitor-analyst** | Reconstructs competitor theory-of-mind, four fits, firers profile |
| **interview-synthesizer** | Extracts 4 forces + 6-phase timeline from switch-interview transcripts |
| **jtbd-researcher** | Clusters jobs by causal pathway, names functional/emotional/social layers |
| **outcome-prioritizer** | Computes Ulwick opportunity scores with floor-at-zero detail |
| **thesis-critic** | Critiques a BRIEF for evidence gaps, weak wedges, confirmation bias |
| **hw-context-adapter** | Blocks software-only patterns (A/B test, feature flags) when the product is physical hardware |

## Prerequisites

- Claude Code with internet access (for voice mining, competitor research)
- No API keys or external services required
- Works on any topic — software, hardware, services

## Methodology

Built on two complementary frameworks:

- **Moesta-school JTBD** — context-driven job decomposition, switch-interview structure, 4 forces of progress, functional/emotional/social layers
- **Ulwick's Outcome-Driven Innovation (ODI)** — desired outcome statements, opportunity scoring (Importance + max(I-S, 0)), threshold bands (12+ underserved, 15+ ripe)

Reference docs in `references/` cover each methodology in depth. Templates in `templates/` provide the output format for each phase.

## Installation

See [INSTALL.md](INSTALL.md).
