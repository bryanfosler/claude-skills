---
name: persona-analysis
description: Extract behavioral personas from customer interview transcripts using structured extraction (LLM) + deterministic clustering (code). Use this skill whenever the user has interview transcripts and wants to segment customers into behavioral personas, find natural clusters in qualitative data, or prepare the "who" for JTBD analysis. Also use when the user mentions persona analysis, customer segmentation from interviews, or behavioral clustering.
---

# Persona Analysis Skill

Analyze customer interview transcripts to discover behavioral personas. The Python pipeline at `~/Projects/persona-analysis/pipeline/` does the heavy lifting — run `python3 -m pipeline.run_pipeline --help` to see phase options and flags.

## Prerequisites

- Python 3.10+ with `numpy`, `scikit-learn`, `anthropic`
- Interview transcripts as `.txt` or `.md` files (one per customer)
- `ANTHROPIC_API_KEY` set in environment
- Pipeline code at `~/Projects/persona-analysis/pipeline/`

## What This Skill Produces

```
output/
├── PERSONA_REPORT.md       # Human-readable persona profiles + validation
├── PERSONA_PROFILES.json   # Machine-readable output for JTBD pipeline
└── extractions.json        # Structured extraction data (audit trail)
```

## Process

### Step 1: Configure Project

Before first run, create a `project_config.json` for the domain. Run the discovery pass to scan transcripts and propose option lists:

```bash
python3 -m pipeline.run_pipeline --phase discover --transcripts <path/to/transcripts/>
```

Review proposals, adjust, save using `schemas/project_config.json` as template. If a config already exists, verify it has no `REPLACE_WITH_YOUR_...` placeholder values.

### Step 2: Extract and Cluster

Run extraction then clustering. If the user already has `extractions.json`, skip straight to `--phase cluster`.

The extraction phase is the critical methodology step. It runs 3 passes per transcript with DIFFERENT prompt framings (behavior-first, motivation-first, frustration-first) to generate genuine variance, then merges via consensus: median for scales, majority vote for categoricals, threshold for multi-selects. This is what makes results reproducible — identical prompts at temperature 0 would just produce identical outputs, making multi-pass meaningless.

### Step 3: Handle the "No Clusters" Edge Case

The pipeline has a minimum silhouette threshold (0.25). If no k produces clusters above this, the pipeline reports NO_CLUSTERS. This is common with small samples (< 30 interviews) across many dimensions — the "curse of dimensionality" means 60 one-hot-encoded features can make 23 people all look equidistant.

When this happens:
1. Report it honestly — "the data doesn't support statistically distinct personas at this sample size"
2. **Run a scale-only comparison**: cluster on just the 6 scale dimensions (usage_frequency, feature_depth, data_engagement, tech_comfort, budget_sensitivity, aspiration_gap) without PCA. This removes the categorical noise and often reveals structure the full pipeline misses at small n.
3. Try forcing k=2 through k=√n on both the full pipeline and the scale-only approach. Compare which people group together across both methods — groups that appear in both are **hard clusters** (stable regardless of method); groups that shuffle are **soft clusters** (real but boundary-dependent).
4. Use **pairwise agreement** to measure cross-approach stability: for every pair of customers, check if both methods agree on whether they're in the same or different clusters. Above 70% agreement means the core structure is real. Below 60% means the groupings are method artifacts.
5. If a forced k produces coherent profiles, report it with the caveat that the model is soft (gradient, not crisp boundaries). Use the healthiest k (highest silhouette among those with ≥ 3 members per cluster).
6. If no k makes sense in either approach, the honest answer is homogeneity — the sample may need more interviews or more discriminating dimensions.

Do NOT silently force a k without telling the user the auto-selection failed. Transparency about model quality is a feature of this pipeline.

### Step 4: Interpret Results

Report to the user:
- Number of personas, distinguishing **hard clusters** (stable across approaches) from **soft clusters** (appear consistently but boundaries shift under perturbation)
- Model health: healthy / acceptable / fragile
- Overfit warnings if any dimension contributes >50% of separation
- Borderline rate and which customers are flagged
- Leave-one-out stability percentage
- Cross-approach pairwise agreement (if multiple approaches were run)

**Coverage check:** Any customer below 62% Tier 1 coverage (5 of 8 dimensions) likely had too short an interview — flag for the user.

**Confidence interpretation:**
- High confidence (>0.5): clearly one persona
- Low confidence (<0.2): borderline — flag for human review, note the second-nearest persona
- These borderline customers often reveal the most interesting strategic insights (they're the "hybrid" users who bridge two segments)

**Common dimension findings:**
- `usage_frequency` is often decorative (0% sensitivity) when samples are drawn from active users — everyone rides/uses the product frequently. It's a precondition of being interviewed, not a differentiator. Keep it as metadata but note when it contributes nothing to separation.
- `aspiration_gap` (Tier 2) frequently outperforms its tier — it captures the life-transformation narrative that distinguishes newcomers-who-are-growing from newcomers-who-are-content. When it shows >10% contribution, consider promoting it to a must-extract dimension for the domain.

### Step 5: Name and Define Personas

Names MUST be behavioral, not demographic. The name should describe what differentiates the cluster's behavior.

- Good: "Data Maximalist", "Trail Soul", "Transformation Rider", "Social Connector"
- Bad: "Young Professional", "Weekend Dad", "Budget Buyer", "Female MTB Rider"

Demographics get attached to personas AFTER naming — as descriptive color, not defining criteria. A 25-year-old competitive cyclist and a 55-year-old recreational rider might cluster together because they use the product identically.

**Define must-have vs nice-to-have criteria for each persona:**
- **Must-have (hard gates):** The 2–4 dimension values or behavioral traits that DEFINE membership. If someone doesn't meet these, they're not this persona regardless of other similarities. Derived from the cluster's discriminating dimensions and centroid extremes.
- **Nice-to-have (soft fit):** Traits that are common in the cluster but not required. Missing one doesn't disqualify someone; having them increases confidence.

This structure makes personas actionable for classification — given a new customer's extraction, you can run the hard gates first as a filter, then check soft fit for confidence.

### Step 6: Bridge to JTBD

For each persona, derive characteristic situations from the behavioral profile and write Moesta-syntax job statements:

> When [persona's characteristic situation], I want to [motivation], so I can [outcome].

Ground each statement in the centroid profile and representative quotes from the extractions — not generic assumptions. Each persona should get 1 primary + 2-4 supporting JTBD statements.

The `PERSONA_PROFILES.json` output feeds directly into `pd-jtbd` as the "who" for each job.

### Step 7: Handle Problems

| Issue | What it means | What to do |
|-------|--------------|------------|
| No natural clusters | Curse of dimensionality (too many features for sample size) or genuinely homogeneous sample | See Step 3. Run scale-only comparison, try forced k, check cross-approach agreement |
| Overfit (one dimension >50%) | One variable driving all separation | Consider whether that dimension IS the real differentiator, or if it's an artifact. Re-run excluding it to check |
| High borderline rate (>20%) | Personas overlap too much | Consider merging adjacent personas or adding discriminating dimensions |
| Low LOO stability (<80%) | Removing one person reshuffles everything | Sample too small — need more interviews. Report as "fragile" |
| Low Tier 1 coverage | Interviews too short or off-topic | Flag specific customers; consider excluding from clustering |
| All soft clusters, no hard clusters | Groupings change across methods | The sample may not have real segments — or the dimensions don't capture what actually differentiates these people. Check if a missing dimension (like aspiration_gap) would create separation |

## Integration with Product Discovery Pipeline

This skill fits between `pd-mine-voices` (Phase 02) and `pd-jtbd` (Phase 03):

```
pd-mine-voices (02) → persona-analysis → pd-jtbd (03)
```
