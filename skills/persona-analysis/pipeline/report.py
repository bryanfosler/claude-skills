"""
Generate human-readable and machine-readable reports from pipeline results.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from .schema import (
    PersonaCentroid, Classification, ValidationReport,
    CustomerExtraction, serialize,
)
from .vectorize import Vectorizer


def generate_persona_report(
    personas: list[PersonaCentroid],
    classifications: list[Classification],
    validation: ValidationReport,
    vectorizer: Vectorizer,
) -> str:
    """Generate a markdown report of discovered personas."""
    lines = ["# Persona Analysis Report\n"]

    # Summary
    lines.append("## Summary\n")
    lines.append(f"- **Personas discovered:** {len(personas)}")
    lines.append(f"- **Customers classified:** {len(classifications)}")
    lines.append(f"- **Model health:** {validation.overall_health}")
    lines.append(f"- **Leave-one-out stability:** {validation.leave_one_out_stability:.1%}")
    lines.append(f"- **Borderline rate:** {validation.borderline_rate:.1%}")
    lines.append("")

    if validation.overfit_flags:
        lines.append("### ⚠ Overfit Warnings\n")
        for flag in validation.overfit_flags:
            lines.append(f"- {flag}")
        lines.append("")

    # Dimension contributions
    lines.append("## Dimension Contributions to Cluster Separation\n")
    sorted_dims = sorted(
        validation.dimension_contributions.items(), key=lambda x: -x[1]
    )
    for dim, score in sorted_dims:
        bar = "█" * int(score * 40)
        lines.append(f"- **{dim}**: {score:.1%} {bar}")
    lines.append("")

    # Each persona
    lines.append("## Persona Profiles\n")
    for persona in sorted(personas, key=lambda p: -p.size):
        lines.append(f"### {persona.name}")
        lines.append(f"**Size:** {persona.size} customers ({persona.proportion:.0%} of sample)\n")

        lines.append("**Discriminating dimensions:**")
        for dim in persona.discriminating_dimensions:
            lines.append(f"- {dim}")
        lines.append("")

        # Centroid profile with feature names
        lines.append("**Centroid profile:**")
        lines.append("```")
        for name, val in zip(vectorizer.feature_names, persona.centroid_vector):
            if abs(val) > 0.01:  # skip zero-valued features for readability
                lines.append(f"  {name}: {val:.2f}")
        lines.append("```\n")

        if persona.representative_quotes:
            lines.append("**Representative quotes:**")
            for q in persona.representative_quotes:
                lines.append(f'> "{q}"')
            lines.append("")

        if persona.demographic_overlay:
            lines.append(f"**Demographic overlay:** {persona.demographic_overlay}\n")

        # Members
        members = [c for c in classifications if c.assigned_persona == persona.persona_id]
        high_conf = [c for c in members if c.confidence > 0.5]
        borderline = [c for c in members if c.flagged_for_review]
        lines.append(f"**Members:** {len(members)} total, "
                      f"{len(high_conf)} high-confidence, "
                      f"{len(borderline)} borderline")
        lines.append("")

    # Dimension sensitivity
    lines.append("## Dimension Sensitivity Analysis\n")
    lines.append("Impact of removing each dimension on cluster assignments:\n")
    sorted_sens = sorted(
        validation.dimension_sensitivity.items(), key=lambda x: -x[1]
    )
    for dim, change in sorted_sens:
        label = "load-bearing" if change > 0.30 else "contributing" if change > 0.05 else "decorative"
        lines.append(f"- **{dim}**: {change:.1%} change ({label})")
    lines.append("")

    # Borderline cases
    borderline_cases = [c for c in classifications if c.flagged_for_review]
    if borderline_cases:
        lines.append("## Borderline Cases (flagged for review)\n")
        lines.append("| Customer | Assigned | Confidence | Distance to 2nd |")
        lines.append("|----------|----------|------------|-----------------|")
        for c in borderline_cases:
            lines.append(
                f"| {c.customer_id} | {c.persona_name} | "
                f"{c.confidence:.3f} | {c.distance_to_second:.4f} |"
            )
        lines.append("")

    # Classification table
    lines.append("## Full Classification Table\n")
    lines.append("| Customer | Persona | Confidence | Review? |")
    lines.append("|----------|---------|------------|---------|")
    for c in sorted(classifications, key=lambda x: (-x.confidence,)):
        flag = "⚠" if c.flagged_for_review else ""
        lines.append(
            f"| {c.customer_id} | {c.persona_name} | "
            f"{c.confidence:.3f} | {flag} |"
        )
    lines.append("")

    return "\n".join(lines)


def generate_json_output(
    personas: list[PersonaCentroid],
    classifications: list[Classification],
    validation: ValidationReport,
    extractions: list[CustomerExtraction],
) -> dict:
    """Generate machine-readable JSON output for downstream consumption (e.g., JTBD analysis)."""
    return {
        "personas": [serialize(p) for p in personas],
        "classifications": [serialize(c) for c in classifications],
        "validation": serialize(validation),
        "extraction_summary": {
            "total_customers": len(extractions),
            "extraction_coverage": {
                e.customer_id: e.dimensions.tier1_coverage()
                for e in extractions
            },
        },
    }


def save_reports(
    output_dir: str | Path,
    personas: list[PersonaCentroid],
    classifications: list[Classification],
    validation: ValidationReport,
    extractions: list[CustomerExtraction],
    vectorizer: Vectorizer,
):
    """Write all report artifacts to the output directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Markdown report
    md_report = generate_persona_report(personas, classifications, validation, vectorizer)
    (output_dir / "PERSONA_REPORT.md").write_text(md_report)

    # Machine-readable JSON
    json_output = generate_json_output(personas, classifications, validation, extractions)
    (output_dir / "PERSONA_PROFILES.json").write_text(
        json.dumps(json_output, indent=2, default=str)
    )

    # Individual extraction data (for audit trail)
    extractions_out = [serialize(e) for e in extractions]
    (output_dir / "extractions.json").write_text(
        json.dumps(extractions_out, indent=2, default=str)
    )
