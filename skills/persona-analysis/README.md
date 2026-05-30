# Persona Analysis Skill

Extract behavioral personas from customer interview transcripts using structured LLM extraction and deterministic statistical clustering. Feeds directly into JTBD analysis.

## When to Use

- You have 7+ customer interview transcripts and want to find natural behavioral segments
- You need repeatable, deterministic persona assignments (not different results every run)
- You're preparing personas as the "who" for downstream JTBD decomposition

## What It Produces

| File | For |
|------|-----|
| `PERSONA_REPORT.md` | Human-readable profiles with validation metrics and classification table |
| `PERSONA_PROFILES.json` | Machine-readable output for JTBD pipeline consumption |
| `extractions.json` | Structured extraction data with verbatim evidence (audit trail) |

## Prerequisites

- Python 3.10+ with `numpy`, `scikit-learn`, `anthropic`
- Interview transcripts as `.txt` or `.md` files (one per customer)
- `ANTHROPIC_API_KEY` set in environment
- Pipeline code at `~/Projects/persona-analysis/pipeline/`

## How It Works

The pipeline has two phases. The separation is the core design decision — it's what makes results reproducible.

### Phase 1: Structured Extraction (LLM-assisted, ~95% reproducible)

Each interview transcript gets converted into a fixed-schema JSON object. The LLM reads the interview and fills in 8 behavioral dimensions — scales (1-5), categoricals (pick one from a list), and multi-selects (pick all that apply). Every value must include a verbatim quote from the interview as evidence.

**Why this works:**
- Constraining the LLM to fixed types (scales, enums) instead of free text eliminates most output variance. The model can't drift into novel categories or invented scales.
- Three extraction passes use different prompt framings (behavior-first, motivation-first, frustration-first). This generates genuine variance for the consensus protocol — identical prompts at temperature 0 would just produce identical outputs, making "multi-pass" theater.
- Consensus merges the 3 passes: median for scales, majority vote for categoricals, threshold selection for multi-selects. Disagreements between passes are flagged as genuinely ambiguous — a feature, not a bug.
- Claude's `tool_use` with a JSON schema validates the output structure at the API level. No fragile text parsing.

### Phase 2: Deterministic Analysis (pure Python, 100% reproducible)

Once interviews are structured data, everything is math. Same inputs always produce the same output.

**Vectorization** converts extractions into numerical vectors. Key design decisions:
- Missing data becomes NaN, not zero. A customer who didn't discuss data engagement is "unknown" — not the same as "never reviews data." NaN gets excluded from distance calculations instead of pulling customers toward low-value clusters.
- Categorical dimensions are normalized by 1/√(n_options) so a 6-option categorical doesn't get 6x the Euclidean distance influence of a single scale dimension. Without this, clustering is secretly dominated by whichever categorical has the most options.
- PCA dimensionality reduction kicks in automatically when the feature-to-sample ratio exceeds 2:1 (common with small qualitative samples — 26 features with 10 interviews). Prevents spurious clusters from noise in high-dimensional space.

**Clustering** uses k-means with silhouette optimization:
- Tests k=2 through k=√n, picks the k with highest silhouette score.
- Fixed random seed (42) for reproducibility.
- Minimum silhouette threshold of 0.25 — if no k produces clusters above this, the pipeline reports "no natural clusters found" instead of forcing fake personas. This is the honest answer when data doesn't support segmentation.
- Minimum 3 customers per cluster. Fewer than that is an anecdote, not a segment.

**Classification** assigns each customer to the nearest persona centroid with a confidence score:
- `confidence = 1 - (distance_to_assigned / distance_to_second_closest)`
- High confidence (>0.5): clearly one persona. Low confidence (<0.2): borderline, flagged for human review.
- Uses NaN-aware distance so customers with missing dimensions are compared only on dimensions they share.

**Validation** catches problems before they infect downstream JTBD analysis:
- **Overfit detection**: flags any dimension contributing >50% of cluster separation. If one variable is driving all persona differences, you might have a one-dimensional model, not real personas.
- **Leave-one-out stability**: removes each customer, re-clusters, checks if relationships change. If removing one person reshuffles all the personas, the model is fragile.
- **Dimension sensitivity**: removes each dimension, re-clusters, measures impact. Identifies "decorative" dimensions (removing them changes nothing) and "load-bearing" dimensions (removing them collapses personas).
- **Borderline analysis**: if >20% of customers are borderline between two personas, the model may need fewer personas or more discriminating dimensions.

## Why Behavioral Over Demographic

A 25-year-old competitive cyclist and a 55-year-old recreational rider might use the product identically — same features, same frequency, same data engagement. Putting them in different personas because of age or riding type creates false separation. Behavioral dimensions cluster people by what they actually need from the product.

Demographics get attached to personas AFTER clustering — as descriptive color, not defining criteria. The 8 Tier 1 dimensions are all behavioral:

| Dimension | Type | What it captures |
|-----------|------|-----------------|
| Usage frequency | Scale 1-5 | How often they use the product |
| Feature depth | Scale 1-5 | Breadth and depth of feature usage |
| Primary context | Categorical | The situation driving usage |
| Data engagement | Scale 1-5 | How much they engage with analytics |
| Purchase trigger | Categorical | What caused the switch/purchase |
| Pain points | Multi-select | Current frustrations |
| Ecosystem | Multi-select | Other tools used alongside |
| Social context | Categorical | Solo vs group vs competitive |

## Why You Should Trust the Output

The pipeline includes built-in skepticism. The validation report tells you:
- Whether the personas are statistically distinct or overlapping noise
- Whether one variable is doing all the work (overfit)
- Whether the model is stable or fragile
- Which customers are confidently placed and which are borderline guesses
- What happens if you remove any single dimension

A healthy model shows: no dimension >30% contribution, <10% borderline rate, >90% leave-one-out stability. The report flags anything below these thresholds with specific diagnostic guidance.

Every extraction includes the verbatim interview quote that justifies it. You can audit any classification by reading the evidence chain: interview quote → extracted score → vector position → distance to centroid → persona assignment.

## Integration

Fits between `pd-mine-voices` (Phase 02) and `pd-jtbd` (Phase 03) in the product-discovery pipeline. The `PERSONA_PROFILES.json` output becomes the "who" in Moesta-syntax job statements:

> When [persona's characteristic situation], I want to [motivation], so I can [outcome].

## Installation

This skill lives in the persona-analysis project directory. To install into the product-discovery plugin:

```bash
cp -r ~/Projects/persona-analysis/skill ~/claude-skills/plugins/product-discovery/skills/persona-analysis
```

The Python pipeline at `~/Projects/persona-analysis/pipeline/` must remain in place — the skill calls it via `python3 -m pipeline.run_pipeline`.
