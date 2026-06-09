#!/usr/bin/env python3
"""
End-to-end persona analysis pipeline.

Usage:
    # Full pipeline (extract + cluster + validate)
    python -m pipeline.run_pipeline \\
        --config schemas/project_config.json \\
        --transcripts path/to/transcripts/ \\
        --output output/

    # Discovery pass: scan transcripts to propose option lists
    python -m pipeline.run_pipeline --phase discover --transcripts path/to/transcripts/

    # Individual phases
    python -m pipeline.run_pipeline --phase extract --config config.json --transcripts dir/ --output out/
    python -m pipeline.run_pipeline --phase cluster --config config.json --extractions out/extractions.json --output out/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from .schema import PipelineConfig, CustomerExtraction, serialize
from .vectorize import Vectorizer
from .cluster import cluster_customers, build_persona_centroids
from .classify import classify_batch, classification_summary
from .validate import run_full_validation
from .report import save_reports


def load_extractions(path: str | Path) -> list[CustomerExtraction]:
    """Load previously extracted data from JSON."""
    from .extract import parse_extraction_response

    with open(path) as f:
        data = json.load(f)

    extractions = []
    for item in data:
        dims_raw = item.get("dimensions", {})
        dims = parse_extraction_response(dims_raw)
        extractions.append(CustomerExtraction(
            customer_id=item["customer_id"],
            interview_date=item.get("interview_date", ""),
            dimensions=dims,
            extraction_passes=item.get("extraction_passes", 0),
            extraction_model=item.get("extraction_model", ""),
        ))
    return extractions


def run_discover(args):
    """Phase 0: Scan transcripts to discover option lists for config."""
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package required. pip install anthropic")
        sys.exit(1)

    from .extract import discovery_pass

    client = anthropic.Anthropic()
    transcript_dir = Path(args.transcripts)
    files = sorted(transcript_dir.glob("*.txt")) + sorted(transcript_dir.glob("*.md"))
    if not files:
        print(f"No .txt or .md files found in {transcript_dir}")
        sys.exit(1)

    print(f"Scanning {len(files)} transcripts to discover dimension options...")
    transcripts = [f.read_text() for f in files]
    proposed = discovery_pass(transcripts, client,
                              model=getattr(args, "model", "claude-sonnet-4-6"))

    print("\n=== PROPOSED OPTION LISTS ===")
    print("Review these and copy into your project_config.json:\n")
    print(json.dumps(proposed, indent=2))
    print("\nThese are proposals — add, remove, or rename before locking your config.")


def run_extract(args, config: PipelineConfig):
    """Phase 1: Extract structured data from interview transcripts."""
    try:
        import anthropic
    except ImportError:
        print("ERROR: anthropic package required for extraction. pip install anthropic")
        sys.exit(1)

    from .extract import extract_from_file

    client = anthropic.Anthropic()
    transcript_dir = Path(args.transcripts)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    transcript_files = sorted(transcript_dir.glob("*.txt")) + sorted(transcript_dir.glob("*.md"))
    if not transcript_files:
        print(f"No .txt or .md files found in {transcript_dir}")
        sys.exit(1)

    print(f"Found {len(transcript_files)} transcripts to extract")
    extractions = []

    for i, tf in enumerate(transcript_files, 1):
        customer_id = tf.stem
        print(f"  [{i}/{len(transcript_files)}] Extracting {customer_id}...")
        extraction = extract_from_file(
            tf, customer_id, "", config, client,
            model=getattr(args, "model", "claude-sonnet-4-6"),
        )
        extractions.append(extraction)
        coverage = extraction.dimensions.tier1_coverage()
        print(f"    Tier 1 coverage: {coverage:.0%}")

    out_path = output_dir / "extractions.json"
    with open(out_path, "w") as f:
        json.dump([serialize(e) for e in extractions], f, indent=2, default=str)
    print(f"\nExtractions saved to {out_path}")
    return extractions


def run_cluster_and_classify(
    extractions: list[CustomerExtraction],
    config: PipelineConfig,
    output_dir: Path,
    k_override: int | None = None,
):
    """Phase 2-4: Cluster, classify, validate, and report."""
    vectorizer = Vectorizer(config)
    print(f"Vector dimensions: {vectorizer.vector_length} features")

    print("\nClustering...")
    labels, km, k, sil_scores, pca_applied = cluster_customers(
        extractions, config, vectorizer, k_override,
    )

    if pca_applied:
        print("  PCA applied (high feature-to-sample ratio)")

    if k is None:
        print("\n  NO NATURAL CLUSTERS FOUND.")
        print("  The data does not support distinct personas at current thresholds.")
        print("  Possible causes:")
        print("    - Sample is too small")
        print("    - Customers are genuinely homogeneous on these dimensions")
        print("    - Dimensions don't capture the real variation")
        print(f"  Silhouette scores tested: {sil_scores}")
        print("\n  Consider: adding dimensions, lowering min_cluster_size, or")
        print("  accepting that this population may not segment into distinct personas.")
        return None, None, None

    print(f"  Optimal k: {k}")
    for test_k, score in sorted(sil_scores.items()):
        marker = " <-- selected" if test_k == k else ""
        print(f"  k={test_k}: silhouette={score:.3f}{marker}")

    personas = build_persona_centroids(extractions, labels, km, vectorizer)
    print(f"\nPersonas discovered: {len(personas)}")
    for p in personas:
        print(f"  {p.name}: {p.size} customers ({p.proportion:.0%})")

    print("\nClassifying...")
    classifications = classify_batch(extractions, personas, vectorizer, config)
    summary = classification_summary(classifications)
    print(f"  Mean confidence: {summary['mean_confidence']:.3f}")
    print(f"  Flagged for review: {summary['flagged_for_review']}")

    print("\nValidating...")
    validation = run_full_validation(
        extractions, labels, classifications, config, vectorizer,
    )
    print(f"  Model health: {validation.overall_health}")
    print(f"  LOO stability: {validation.leave_one_out_stability:.1%}")
    print(f"  Borderline rate: {validation.borderline_rate:.1%}")

    if validation.overfit_flags:
        for flag in validation.overfit_flags:
            print(f"  WARNING: {flag}")

    print(f"\nSaving reports to {output_dir}/")
    save_reports(output_dir, personas, classifications, validation, extractions, vectorizer)
    print("Done.")

    return personas, classifications, validation


def main():
    parser = argparse.ArgumentParser(description="Persona Analysis Pipeline")
    parser.add_argument("--config", help="Path to project_config.json")
    parser.add_argument("--output", help="Output directory")
    parser.add_argument("--phase", choices=["discover", "extract", "cluster", "full"], default="full")
    parser.add_argument("--transcripts", help="Directory of interview transcripts")
    parser.add_argument("--extractions", help="Path to extractions.json (for cluster phase)")
    parser.add_argument("--k", type=int, help="Force number of clusters")
    parser.add_argument("--model", default="claude-sonnet-4-6", help="Claude model for extraction")

    args = parser.parse_args()

    if args.phase == "discover":
        if not args.transcripts:
            print("ERROR: --transcripts required for discover phase")
            sys.exit(1)
        run_discover(args)
        return

    if not args.config:
        print("ERROR: --config required for this phase")
        sys.exit(1)
    if not args.output:
        print("ERROR: --output required for this phase")
        sys.exit(1)

    config = PipelineConfig.from_file(args.config)
    output_dir = Path(args.output)

    if args.phase == "extract":
        if not args.transcripts:
            print("ERROR: --transcripts required for extract phase")
            sys.exit(1)
        run_extract(args, config)

    elif args.phase == "cluster":
        if not args.extractions:
            print("ERROR: --extractions required for cluster phase")
            sys.exit(1)
        extractions = load_extractions(args.extractions)
        run_cluster_and_classify(extractions, config, output_dir, args.k)

    elif args.phase == "full":
        if not args.transcripts:
            print("ERROR: --transcripts required for full pipeline")
            sys.exit(1)
        extractions = run_extract(args, config)
        run_cluster_and_classify(extractions, config, output_dir, args.k)


if __name__ == "__main__":
    main()
