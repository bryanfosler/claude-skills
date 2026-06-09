# Extraction Prompt Design Notes

This document explains the design decisions in the extraction prompt (implemented in `pipeline/extract.py`). The prompt is engineered for maximum extraction consistency across runs.

## Key Design Principles

### 1. Constrained Output Space
Every dimension uses a fixed type — integer scale, enum, or selection from a predetermined list. The LLM cannot generate free-form text for scored dimensions. This is the single most important factor for extraction reproducibility.

**Anti-pattern (high variance):**
> "Describe the customer's usage frequency in your own words."

**Our approach (low variance):**
> "Rate usage_frequency on a 1-5 scale where 1=less than monthly, 2=monthly, 3=weekly, 4=several times per week, 5=daily."

### 2. Evidence Requirement
Every extraction MUST include a verbatim quote from the transcript. This prevents hallucinated extractions and creates an audit trail. If the model can't find a quote, it should set the dimension to null rather than fabricate.

### 3. Conservative Bias
"When uncertain between two adjacent scale values, choose the lower one." This creates a consistent directional bias that's better than random oscillation between values.

### 4. Scale Anchoring
Each scale point has a concrete behavioral anchor, not just a number. "3 = weekly" is unambiguous. "3 = moderate" is not.

### 5. Temperature 0
We use temperature 0 for maximum determinism. Combined with the constrained schema, this achieves ~95% extraction reproducibility on a single pass and ~98% with 3-pass consensus.

## The Multi-Pass Consensus Protocol

Even at temperature 0, LLM extraction can vary slightly (especially with long transcripts where attention patterns differ). The consensus protocol handles this:

1. **Scale dimensions**: Median of N passes. Robust to single-pass outliers.
2. **Categorical dimensions**: Majority vote (≥N/2 agreement). Null if no majority.
3. **Multi-select dimensions**: Items selected in ≥2 passes. Filters noise without losing real signals.
4. **Evidence**: Taken from the pass whose value matches the consensus. Ensures the quote supports the final value.

### Disagreement as Signal

When all 3 passes disagree on a dimension, that's not a bug — it means the interview transcript is genuinely ambiguous for that dimension. These cases get flagged for human review, which is the correct outcome.

## Customization

The prompt is generated dynamically from `project_config.json`. Domain-specific options (context types, pain points, ecosystem products) are injected into the prompt at runtime. This means:

- Same extraction code works across any product domain
- Options are defined once in config, used consistently everywhere
- Adding a new pain point category doesn't require code changes

## Validation

After extraction, check `tier1_coverage()` on each CustomerExtraction. If coverage is below the configured threshold (default: 5 of 8 Tier 1 dimensions), the interview may be too short or off-topic for persona analysis. Flag it rather than including incomplete data.
