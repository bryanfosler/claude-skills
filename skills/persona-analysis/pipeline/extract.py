"""
Phase 1: Extract structured behavioral data from interview transcripts.

Uses Claude API with tool_use for schema-validated JSON output.
Runs N passes with VARIED prompts (not identical repeats) and takes consensus.

V6 fixes:
- Uses tool_use instead of raw JSON-in-text for reliable structured output
- Varies prompt structure across passes (reordered dimensions, rephrased anchors)
  so consensus actually catches real variance, not identical outputs
- Adds discovery_pass() to scan transcripts and propose option lists BEFORE
  structured extraction
"""
from __future__ import annotations

import json
import statistics
from collections import Counter
from pathlib import Path

from .schema import (
    CustomerExtraction, ExtractionDimensions, ScoredValue,
    CategoricalValue, MultiselectValue, PipelineConfig,
)

EXTRACTION_SYSTEM_PROMPT = """You are a rigorous qualitative research analyst. You extract structured behavioral data from customer interview transcripts.

RULES:
1. Every value MUST be justified by a verbatim quote from the transcript.
2. If the transcript doesn't contain enough information for a dimension, set it to null.
3. Use ONLY the options provided for categorical and multi-select dimensions.
4. For scale dimensions (1-5), follow the scale definitions exactly.
5. Never infer beyond what the customer explicitly said or clearly demonstrated.
6. When uncertain between two adjacent scale values, choose the lower one (conservative).
"""

# Three prompt variants to generate genuine extraction variance.
# Identical prompts at temp 0 produce identical outputs — useless for consensus.
PROMPT_VARIANTS = [
    {
        "framing": "Focus on what the customer DOES — behaviors, habits, routines. Start with usage patterns and work outward to context and motivation.",
        "scale_order": [
            "usage_frequency", "feature_depth", "data_engagement",
            "primary_context", "purchase_trigger", "social_context",
            "pain_points", "ecosystem",
        ],
    },
    {
        "framing": "Focus on WHY the customer bought and what they're trying to accomplish. Start with purchase motivation and work backward to usage patterns.",
        "scale_order": [
            "purchase_trigger", "primary_context", "social_context",
            "pain_points", "ecosystem",
            "usage_frequency", "feature_depth", "data_engagement",
        ],
    },
    {
        "framing": "Focus on the customer's FRUSTRATIONS and ecosystem. Start with pain points and what else they use, then characterize their usage patterns.",
        "scale_order": [
            "pain_points", "ecosystem", "social_context",
            "data_engagement", "feature_depth", "usage_frequency",
            "purchase_trigger", "primary_context",
        ],
    },
]

DIMENSION_DEFS = {
    "usage_frequency": {
        "type": "scale",
        "description": "How often the customer uses the product",
        "anchors": {1: "Less than monthly", 2: "Monthly", 3: "Weekly", 4: "Several times per week", 5: "Daily or almost daily"},
    },
    "feature_depth": {
        "type": "scale",
        "description": "Breadth and depth of feature usage",
        "anchors": {1: "Uses 1-2 core features only", 2: "Uses basic feature set", 3: "Uses most features", 4: "Uses advanced features", 5: "Power user with deep configuration"},
    },
    "data_engagement": {
        "type": "scale",
        "description": "How much they engage with data and analytics",
        "anchors": {1: "Never reviews data", 2: "Glances at summary", 3: "Reviews key metrics each use", 4: "Compares trends over time", 5: "Deep analysis, exports data"},
    },
    "primary_context": {"type": "categorical", "description": "Primary context in which they use the product"},
    "purchase_trigger": {"type": "categorical", "description": "What triggered the purchase decision"},
    "social_context": {"type": "categorical", "description": "Social context of product use"},
    "pain_points": {"type": "multiselect", "description": "Current frustrations or unmet needs"},
    "ecosystem": {"type": "multiselect", "description": "Other tools/products used alongside"},
}


def build_extraction_tool_schema(config: PipelineConfig) -> dict:
    """Build a Claude tool_use schema for structured extraction."""
    dim_properties = {}
    for dim_name, dim_def in DIMENSION_DEFS.items():
        if dim_def["type"] == "scale":
            dim_properties[dim_name] = {
                "type": "object",
                "properties": {
                    "value": {"type": "integer", "minimum": 1, "maximum": 5},
                    "evidence": {"type": "string", "description": "Verbatim quote from transcript"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": ["value", "evidence", "confidence"],
            }
        elif dim_def["type"] == "categorical":
            options = {
                "primary_context": config.context_options,
                "purchase_trigger": config.trigger_options,
                "social_context": config.social_options,
            }.get(dim_name, [])
            dim_properties[dim_name] = {
                "type": "object",
                "properties": {
                    "value": {"type": "string", "enum": options} if options else {"type": "string"},
                    "evidence": {"type": "string"},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": ["value", "evidence", "confidence"],
            }
        elif dim_def["type"] == "multiselect":
            options = {
                "pain_points": config.pain_point_options,
                "ecosystem": config.ecosystem_options,
            }.get(dim_name, [])
            dim_properties[dim_name] = {
                "type": "object",
                "properties": {
                    "values": {"type": "array", "items": {"type": "string", "enum": options} if options else {"type": "string"}},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                    "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
                },
                "required": ["values", "evidence", "confidence"],
            }

    return {
        "name": "record_extraction",
        "description": "Record the structured behavioral data extracted from the interview transcript.",
        "input_schema": {
            "type": "object",
            "properties": dim_properties,
            "required": list(DIMENSION_DEFS.keys()),
        },
    }


def build_extraction_prompt(
    transcript: str,
    config: PipelineConfig,
    variant_idx: int = 0,
) -> str:
    """Build extraction prompt with varied framing per pass."""
    variant = PROMPT_VARIANTS[variant_idx % len(PROMPT_VARIANTS)]
    dim_order = variant["scale_order"]

    sections = []
    for i, dim_name in enumerate(dim_order, 1):
        dim_def = DIMENSION_DEFS[dim_name]
        if dim_def["type"] == "scale":
            anchors = dim_def["anchors"]
            anchor_text = "\n".join(f"   {k} = {v}" for k, v in anchors.items())
            sections.append(f"{i}. **{dim_name}** (scale 1-5): {dim_def['description']}\n{anchor_text}")
        elif dim_def["type"] == "categorical":
            options = {
                "primary_context": config.context_options,
                "purchase_trigger": config.trigger_options,
                "social_context": config.social_options,
            }.get(dim_name, [])
            sections.append(f"{i}. **{dim_name}** (pick ONE): {json.dumps(options)}")
        elif dim_def["type"] == "multiselect":
            options = {
                "pain_points": config.pain_point_options,
                "ecosystem": config.ecosystem_options,
            }.get(dim_name, [])
            sections.append(f"{i}. **{dim_name}** (select ALL that apply): {json.dumps(options)}")

    return f"""{variant['framing']}

Extract structured behavioral data from this customer interview transcript.
Use the record_extraction tool to submit your findings.

## Dimensions to Extract

{chr(10).join(sections)}

## Rules
- Every value MUST cite a verbatim quote from the transcript as evidence.
- If the transcript has no signal for a dimension, you must still provide
  the field but mark confidence as "low" and note the absence in evidence.
- For scales, when uncertain between adjacent values, choose the lower one.

## Interview Transcript

{transcript}
"""


def parse_tool_response(tool_input: dict) -> ExtractionDimensions:
    """Convert tool_use input dict into typed ExtractionDimensions."""
    return parse_extraction_response(tool_input)


def parse_extraction_response(raw_json: dict) -> ExtractionDimensions:
    """Convert raw JSON extraction into typed ExtractionDimensions."""
    dims = ExtractionDimensions()

    scale_fields = [
        "usage_frequency", "feature_depth", "data_engagement",
        "tech_comfort", "budget_sensitivity", "aspiration_gap",
    ]
    cat_fields = [
        "primary_context", "purchase_trigger", "social_context",
        "brand_relationship",
    ]
    multi_fields = ["pain_points", "ecosystem", "information_sources"]

    for field_name in scale_fields:
        val = raw_json.get(field_name)
        if val and isinstance(val, dict) and val.get("value") is not None:
            setattr(dims, field_name, ScoredValue(
                value=int(val["value"]),
                evidence=str(val.get("evidence", "")),
                confidence=str(val.get("confidence", "medium")),
            ))

    for field_name in cat_fields:
        val = raw_json.get(field_name)
        if val and isinstance(val, dict) and val.get("value"):
            setattr(dims, field_name, CategoricalValue(
                value=str(val["value"]),
                evidence=str(val.get("evidence", "")),
                confidence=str(val.get("confidence", "medium")),
            ))

    for field_name in multi_fields:
        val = raw_json.get(field_name)
        if val and isinstance(val, dict) and val.get("values"):
            setattr(dims, field_name, MultiselectValue(
                values=[str(v) for v in val["values"]],
                evidence=[str(e) for e in val.get("evidence", [])],
                confidence=str(val.get("confidence", "medium")),
            ))

    return dims


def consensus_scored(values: list[int]) -> int:
    return int(statistics.median(values))


def consensus_categorical(values: list[str]) -> str | None:
    if not values:
        return None
    counts = Counter(values)
    winner, count = counts.most_common(1)[0]
    if count >= len(values) / 2:
        return winner
    return None


def consensus_multiselect(value_lists: list[list[str]], threshold: int = 2) -> list[str]:
    counts: Counter = Counter()
    for vl in value_lists:
        counts.update(vl)
    return [item for item, count in counts.items() if count >= threshold]


def merge_passes(passes: list[ExtractionDimensions]) -> ExtractionDimensions:
    """
    Merge N extraction passes into a single consensus extraction.
    Each pass used a different prompt variant, so disagreements are real signal.
    """
    merged = ExtractionDimensions()
    n = len(passes)
    threshold = max(2, (n + 1) // 2)

    scale_fields = [
        "usage_frequency", "feature_depth", "data_engagement",
        "tech_comfort", "budget_sensitivity", "aspiration_gap",
    ]
    for field_name in scale_fields:
        vals = []
        evidences = {}
        for p in passes:
            dim = getattr(p, field_name)
            if dim is not None:
                vals.append(dim.value)
                evidences[dim.value] = dim.evidence
        if vals:
            consensus_val = consensus_scored(vals)
            best_evidence = evidences.get(consensus_val, evidences.get(vals[0], ""))
            setattr(merged, field_name, ScoredValue(
                value=consensus_val,
                evidence=best_evidence,
                confidence="high" if len(set(vals)) == 1 else "medium",
            ))

    cat_fields = [
        "primary_context", "purchase_trigger", "social_context",
        "brand_relationship",
    ]
    for field_name in cat_fields:
        vals = []
        evidences = {}
        for p in passes:
            dim = getattr(p, field_name)
            if dim is not None:
                vals.append(dim.value)
                evidences[dim.value] = dim.evidence
        if vals:
            consensus_val = consensus_categorical(vals)
            if consensus_val:
                setattr(merged, field_name, CategoricalValue(
                    value=consensus_val,
                    evidence=evidences.get(consensus_val, ""),
                    confidence="high" if vals.count(consensus_val) == n else "medium",
                ))

    multi_fields = ["pain_points", "ecosystem", "information_sources"]
    for field_name in multi_fields:
        all_value_lists = []
        all_evidences: dict[str, str] = {}
        for p in passes:
            dim = getattr(p, field_name)
            if dim is not None:
                all_value_lists.append(dim.values)
                for v, e in zip(dim.values, dim.evidence):
                    if v not in all_evidences:
                        all_evidences[v] = e
        if all_value_lists:
            consensus_vals = consensus_multiselect(all_value_lists, threshold)
            setattr(merged, field_name, MultiselectValue(
                values=consensus_vals,
                evidence=[all_evidences.get(v, "") for v in consensus_vals],
                confidence="high" if len(all_value_lists) == n else "medium",
            ))

    return merged


def extract_single_pass(
    transcript: str,
    config: PipelineConfig,
    client,
    model: str = "claude-sonnet-4-6",
    variant_idx: int = 0,
) -> ExtractionDimensions:
    """Run a single extraction pass using Claude tool_use for structured output."""
    prompt = build_extraction_prompt(transcript, config, variant_idx)
    tool_schema = build_extraction_tool_schema(config)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        temperature=config.extraction_temperature,
        system=EXTRACTION_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "record_extraction"},
    )

    # Extract the tool_use input from the response
    for block in response.content:
        if block.type == "tool_use" and block.name == "record_extraction":
            return parse_tool_response(block.input)

    # Fallback: parse text response if tool_use didn't fire
    text = response.content[0].text
    if text.strip().startswith("```"):
        lines = text.strip().split("\n")
        text = "\n".join(lines[1:-1])
    raw = json.loads(text)
    return parse_extraction_response(raw)


def extract_with_consensus(
    transcript: str,
    customer_id: str,
    interview_date: str,
    config: PipelineConfig,
    client,
    model: str = "claude-sonnet-4-6",
) -> CustomerExtraction:
    """Run N extraction passes with varied prompts and merge via consensus."""
    passes = []
    for i in range(config.extraction_passes):
        dims = extract_single_pass(transcript, config, client, model, variant_idx=i)
        passes.append(dims)

    merged = merge_passes(passes)

    return CustomerExtraction(
        customer_id=customer_id,
        interview_date=interview_date,
        dimensions=merged,
        extraction_passes=config.extraction_passes,
        extraction_model=model,
    )


def extract_from_file(
    transcript_path: str | Path,
    customer_id: str,
    interview_date: str,
    config: PipelineConfig,
    client,
    model: str = "claude-sonnet-4-6",
) -> CustomerExtraction:
    """Read a transcript file and extract with consensus."""
    text = Path(transcript_path).read_text()
    return extract_with_consensus(text, customer_id, interview_date, config, client, model)


def discovery_pass(
    transcripts: list[str],
    client,
    model: str = "claude-sonnet-4-6",
) -> dict[str, list[str]]:
    """
    Scan transcripts to DISCOVER option lists before structured extraction.
    This solves the chicken-and-egg problem: you need option lists to extract,
    but you learn the options FROM the interviews.

    Returns proposed option lists for each categorical/multiselect dimension.
    Human reviews and locks these before running structured extraction.
    """
    combined = "\n\n---\n\n".join(
        f"[Interview {i+1}]\n{t[:3000]}"  # cap per transcript for context
        for i, t in enumerate(transcripts[:20])  # cap total
    )

    prompt = f"""Read these customer interview excerpts and identify the distinct categories that appear across interviews.

For each of the following dimensions, list the 4-10 most common distinct options you observe:

1. **primary_context**: What contexts/situations do customers use the product in?
2. **purchase_trigger**: What triggered their purchase or switch decision?
3. **pain_points**: What frustrations or unmet needs do they mention?
4. **ecosystem**: What other products/tools/services do they use alongside?
5. **information_sources**: Where do they learn about products in this category?

Return a JSON object with dimension names as keys and arrays of option strings as values.
Use short, snake_case labels (e.g., "battery_life" not "The battery doesn't last long enough").

Interview Excerpts:
{combined}
"""

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.content[0].text
    if text.strip().startswith("```"):
        lines = text.strip().split("\n")
        text = "\n".join(lines[1:-1])
    return json.loads(text)
