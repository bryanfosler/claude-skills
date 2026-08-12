# Persona Analysis Framework (V5)

## The Core Problem

Most persona work fails for one of five reasons:

1. **Demographic trap** — personas built on who people ARE (age, income, geography) rather than what they DO. Demographics describe; behaviors predict.
2. **Confirmation bias** — analysts see the patterns they expected before looking at data.
3. **Single-variable dominance** — one loud dimension (e.g., "experience level") drowns out richer behavioral signals.
4. **Fuzzy boundaries** — personas overlap so much that classification becomes coin-flip arbitrary.
5. **LLM non-determinism** — AI generates plausible-sounding personas that shift on every run.

This framework solves all five by separating language understanding (where LLMs excel) from classification (where deterministic code excels).

---

## Architecture: Two-Phase Pipeline

```
┌──────────────────────────┐     ┌──────────────────────────┐
│   PHASE 1: EXTRACTION    │     │   PHASE 2: ANALYSIS      │
│   (LLM-assisted)         │────▶│   (Deterministic code)   │
│   ~95% reproducible      │     │   100% reproducible      │
│                          │     │                          │
│   Interview text         │     │   Structured JSON        │
│   → Structured JSON      │     │   → Clusters             │
│   via constrained schema │     │   → Personas             │
│                          │     │   → Classifications      │
│   Multi-pass consensus   │     │   → Confidence scores    │
│   for extraction         │     │   → Validation report    │
│   stability              │     │                          │
└──────────────────────────┘     └──────────────────────────┘
```

**Why this split matters:** LLMs are necessary for understanding natural language interviews. But they're probabilistic — the same prompt can produce different outputs. By constraining the LLM to fill a fixed schema (enums, Likert scales, predetermined categories), we get ~95% extraction consistency. Then ALL downstream analysis — clustering, classification, validation — runs as pure deterministic code. Same inputs always produce same outputs.

---

## Phase 1: Structured Behavioral Extraction

### What We Extract (Dimensions)

Dimensions are the axes along which customers vary. We organize them into tiers:

#### Tier 1: Must-Have (Behavioral Core) — Required for every persona model

These dimensions describe what customers DO. They are the primary discriminators.

| # | Dimension | Type | Scale/Options | Why it matters |
|---|-----------|------|---------------|----------------|
| 1 | **Usage frequency** | Scale 1-5 | 1=rarely → 5=daily | Separates committed users from casual/dormant |
| 2 | **Feature depth** | Scale 1-5 | 1=basic only → 5=power user | Reveals engagement ceiling and complexity tolerance |
| 3 | **Primary use context** | Categorical | Domain-specific enum | The SITUATION drives the job; context is everything |
| 4 | **Data engagement** | Scale 1-5 | 1=ignores → 5=deep analysis | Separates "tool users" from "insight seekers" |
| 5 | **Purchase trigger** | Categorical | Enum of trigger types | Why they switched — the push force |
| 6 | **Pain tolerance profile** | Multi-select | From fixed pain point list | What frustrations they absorb vs abandon over |
| 7 | **Ecosystem integration** | Multi-select | From fixed product/tool list | Network effects and switching costs |
| 8 | **Social context** | Categorical | solo / group / competitive / community | Social dimension of product usage |

#### Tier 2: Could-Have (Enriching) — Improve persona resolution when available

| # | Dimension | Type | Why it's optional |
|---|-----------|------|-------------------|
| 9 | **Tech comfort** | Scale 1-5 | Correlates with feature depth but adds nuance for support/onboarding |
| 10 | **Brand relationship** | Categorical: loyalist/pragmatist/skeptic/new | Matters for marketing, less for product design |
| 11 | **Budget sensitivity** | Scale 1-5 | Important for pricing strategy, not behavior |
| 12 | **Information sources** | Multi-select | Reveals influence channels |
| 13 | **Aspiration gap** | Scale 1-5 (current vs aspirational self) | The emotional fuel behind purchase. Often outperforms its tier — in one endurance-sport study it was the 3rd most discriminating dimension (~12% contribution), revealing a persona that none of the functional dimensions had surfaced. Consider promoting to Tier 1 when the domain involves identity or lifestyle change. |
| 14 | **Switching history** | Structured (from → to → why) | Prior switches reveal decision patterns |

#### Why Behavioral Over Demographic

A 25-year-old competitive cyclist and a 55-year-old recreational rider might use the product identically — same features, same frequency, same data engagement. Putting them in different personas because of age/riding-type creates false separation. Behavioral dimensions cluster people by what they actually need from the product.

Demographics get attached to personas AFTER clustering — as descriptive color, not defining criteria.

### Extraction Protocol

#### Schema Constraints

Every dimension uses a FIXED type — scales, enums, or selections from a predetermined list. No free text in scored dimensions. This constrains the LLM's output space and makes extraction reproducible.

```json
{
  "usage_frequency": 4,
  "feature_depth": 3,
  "primary_context": "training",
  "data_engagement": 2,
  "purchase_trigger": "upgrade_capability",
  "pain_points": ["battery_life", "navigation_accuracy"],
  "ecosystem": ["strava", "training_peaks"],
  "social_context": "club"
}
```

#### Discovery Pass (Phase 0)

Before structured extraction, run a discovery pass that scans all transcripts and proposes option lists for categorical/multi-select dimensions. This solves the chicken-and-egg problem: you need option lists to constrain extraction, but you learn the options FROM the interviews. The discovery pass uses an unstructured LLM scan; a human reviews and locks the lists before Phase 1.

#### Multi-Pass Consensus Protocol

To handle LLM non-determinism in extraction:

1. Run extraction 3 times per interview, each with a **different prompt variant** (different dimension order, different analytical framing). Identical prompts at temperature 0 produce identical outputs — that's useless for consensus. Prompt variation is what generates genuine extraction variance.
2. For scale dimensions: take the median of the 3 values
3. For categorical dimensions: take the majority vote (2 of 3 agreement)
4. For multi-select dimensions: include items selected in ≥2 of 3 runs
5. Flag any dimension where all 3 runs disagree — these need human review

Uses Claude's `tool_use` with a JSON schema for structured output, not raw JSON-in-text. This gives schema validation at the API level and eliminates parse failures.

This achieves ~98% extraction reproducibility.

#### Evidence Linkage

Every extracted value MUST include a verbatim quote from the interview that justifies it. This creates an audit trail and prevents hallucinated extractions.

```json
{
  "usage_frequency": {
    "value": 4,
    "evidence": "I ride pretty much every day, at least five days a week",
    "confidence": "high"
  }
}
```

---

## Phase 2: Persona Discovery

### Step 1: Normalize and Cluster

With structured extractions for all interviews, we discover personas through statistical clustering:

1. **Normalize** all scale dimensions to 0-1 range (min-max scaling)
2. **One-hot encode** categorical dimensions, **scaled by 1/√(n_options)** so a 6-option categorical doesn't get 6x the distance influence of a single scale dimension
3. **Binary encode** multi-select dimensions, similarly normalized per group
4. **Handle missing data** with NaN (not zero). Zero means "lowest value" which is wrong for "not discussed." NaN is excluded from distance calculations.
5. **Apply PCA** when the feature-to-sample ratio exceeds 2:1 (common with small qualitative samples). Retains 90% of variance, prevents spurious clusters from noise in high-dimensional space.
6. **Run k-means clustering** with k from 2 to √(n) where n = number of interviews
7. **Select optimal k** using silhouette score (higher = better-separated clusters). If best silhouette is below 0.25, the pipeline reports "no natural clusters found" rather than forcing fake personas.
6. **Determinism**: fix random seed (42) for reproducible results

### Step 2: Identify Discriminating Dimensions

Not all dimensions contribute equally to cluster separation. We measure each dimension's discriminating power:

```
Discrimination score = between-cluster variance / total variance
```

Dimensions with high discrimination scores are the ones that DEFINE the personas. Dimensions with low scores are shared across all personas (and thus not useful for classification).

**Overfit detection**: If any single dimension contributes >50% of total discrimination, flag it. The model might be a one-axis split masquerading as personas. Run clustering WITHOUT that dimension and compare — if personas survive, the dimension is genuinely discriminating. If they collapse, you have a one-dimensional model, not personas.

**Cross-approach validation**: Run clustering on at least two feature sets — the full vectorized pipeline and a scale-only subset (just the 6 numeric dimensions, no PCA needed). Compute pairwise agreement: for every pair of customers, check if both methods agree on same-cluster/different-cluster. Above 70% agreement means the core structure is real. Clusters that are stable across both approaches are **hard clusters**; clusters whose members scatter are **soft clusters**. Report both types — hard clusters are high-confidence personas, soft clusters are hypotheses that need more data to confirm.

### Step 3: Define Personas from Clusters

For each cluster:

1. **Compute centroid** — the average value of each dimension
2. **Identify the 2-4 most discriminating dimensions** for this cluster
3. **Name the persona** based on those discriminating behaviors (not demographics)
4. **Write boundary conditions** — the specific dimension values that place someone in this persona vs an adjacent one
5. **Attach demographic descriptors** — now that personas exist, demographics become illustrative color

#### Persona Definition Template

```
## Persona: [Behavioral Name]
Cluster type: HARD / SOFT

### Must-Have Criteria (Hard Gates)
The 2-4 dimension values or traits that DEFINE membership. If someone doesn't
meet these, they're not this persona regardless of other fit.
- [Dimension A]: [value threshold or range]
- [Dimension B]: [value threshold or range]
- [Behavioral requirement]: [narrative description]

### Nice-to-Have Criteria (Soft Fit)
Common traits that increase confidence but aren't required for membership.
- [Dimension C]: [typical value or range]
- [Dimension D]: [typical value or range]
- [Contextual trait]: [description]

### Centroid Profile
[Full dimension profile with values]

### Typical Demographic (descriptive, not defining)
[Age range, background, etc. — observed correlation, not causal]

### Representative Quote
"[Verbatim from a cluster member]"

### Size
[N] customers ([X]% of sample)
```

The must-have/nice-to-have split makes personas actionable: given a new customer's extraction, run hard gates first as a filter, then check soft fit for confidence. Hard gates come from the cluster's most discriminating dimensions and centroid extremes. Soft fit comes from common-but-not-universal traits observed in cluster members.

---

## Phase 3: Deterministic Classification

### Scoring Algorithm

For each individual, compute distance to every persona centroid:

```python
distance = sqrt(sum((individual[dim] - centroid[dim])^2 for dim in dimensions))
```

Assign to the nearest centroid. Compute confidence:

```python
confidence = 1 - (distance_to_assigned / distance_to_second_closest)
```

- **Confidence > 0.5**: Strong fit. Clear persona.
- **Confidence 0.2 - 0.5**: Moderate fit. Leans toward assigned persona.
- **Confidence < 0.2**: Borderline. Could be either persona. Flag for review.

### Handling Borderline Cases

Borderline individuals (low confidence) are NOT failures — they're data. They reveal:
- Two personas that might need to be merged
- A missing persona (the borderline individual represents a cluster the model hasn't found)
- Dimension gaps (need more discriminating dimensions)

Track borderline rates. If >20% of customers are borderline, the persona model has a problem.

---

## Phase 4: Validation

### 1. Dimension Contribution Analysis (Overfit Check)

For each dimension, compute the percentage of total cluster separation it contributes. Report:
- Balanced: no dimension >30% — healthy model
- Concentrated: one dimension 30-50% — acceptable but watch it
- Overfit: one dimension >50% — re-examine the model

Note: `usage_frequency` commonly contributes near 0% when samples are drawn from active users (it's a precondition of being interviewed, not a differentiator). This is expected, not a defect.

### 2. Leave-One-Out Stability

Remove each customer one at a time, re-cluster, check if the remaining customers' assignments change. If removing a single customer changes >10% of assignments, the model is fragile.

### 3. Dimension Sensitivity Analysis

Remove each dimension one at a time, re-cluster, measure how much assignments change:
- If removing a dimension changes <5% of assignments, it's decorative — consider dropping it
- If removing a dimension changes >30%, it's load-bearing — it better be a real behavioral signal, not noise

### 4. Cross-Context Validity

If you have interviews from different time periods, products, or cohorts, check that personas hold across contexts. Personas that only exist in one cohort might be artifacts of sampling, not real segments.

### 5. Predictive Validity (Gold Standard)

The ultimate test: do personas predict behavior? If "Persona A" customers should use Feature X more, verify in usage data. If personas don't predict anything downstream, they're not real segments — they're statistical ghosts.

---

## Phase 5: JTBD Bridge

Personas answer WHO. Jobs-to-be-Done answer WHY. They connect through SITUATIONS.

### From Personas to Jobs

Each persona faces characteristic situations driven by their behavioral profile:

```
Persona's behavioral context
    → Triggers specific situations
        → Those situations create jobs-to-be-done
            → Jobs have functional, emotional, and social dimensions
```

Example:
- **Persona**: "Data-Driven Trainer" (high usage frequency, high data engagement, training context)
- **Characteristic situation**: "When I'm reviewing last week's intervals and need to understand why Wednesday's session felt hard but the numbers looked easy..."
- **Job**: "Help me reconcile subjective feel with objective data so I can calibrate my effort perception"
- **Functional**: Overlay subjective RPE with power/HR data
- **Emotional**: Confidence that I'm not fooling myself
- **Social**: Credible training story for my coach/group

### The Handoff

The persona analysis produces a PERSONA_PROFILES.json with:
- Persona definitions with behavioral boundaries
- Customer-to-persona assignments with confidence scores
- Discriminating dimensions ranked by importance
- Representative verbatim quotes per persona

This feeds directly into JTBD analysis where each persona becomes the "who" in the Moesta-syntax job statement:

> When [persona's characteristic situation], I want to [motivation], so I can [outcome].

---

## Criteria Hierarchy: What's Non-Negotiable vs Nice-to-Have

### Non-Negotiable for Valid Personas

1. **Behavioral basis** — at least 5 of the 8 Tier 1 dimensions extracted
2. **Evidence linkage** — every extraction backed by a verbatim quote
3. **Multi-pass extraction** — minimum 3 passes for consensus
4. **Deterministic classification** — code-based, not LLM-based
5. **Overfit check** — no single dimension >50% of discrimination
6. **Minimum sample** — at least 3 customers per persona (otherwise it's an anecdote, not a segment)

### Nice-to-Have for Richer Personas

1. Tier 2 dimensions extracted
2. Demographic overlays
3. Predictive validity against usage data
4. Cross-cohort stability testing
5. Qualitative persona narratives
6. Journey maps per persona

---

## Decision Framework: How We Make Classification Calls

The framework uses a strict hierarchy for decisions:

1. **Euclidean distance to centroid** — the primary signal. Closest centroid wins.
2. **Confidence threshold** — if confidence < 0.2, flag for review rather than forcing assignment.
3. **Discriminating dimension alignment** — as a tiebreaker, check the top 2-3 discriminating dimensions. If an individual matches Persona A's discriminating dimensions but is geometrically closer to B, investigate.
4. **Evidence audit** — for any flagged case, go back to the interview transcript and read the verbatim quotes. Does the human sense of this person match the algorithmic assignment?

This hierarchy means: algorithm first, human judgment for edge cases, never vibes-only.
