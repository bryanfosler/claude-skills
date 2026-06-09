"""
Phase 3: Deterministic classification of individuals into discovered personas.

Pure math — no LLM calls. Same input always produces same output.

V6 fix: Uses NaN-aware distance so missing dimensions are excluded from
distance calculation rather than treated as zero (which falsely pulls
customers toward low-value clusters).
"""
from __future__ import annotations

import numpy as np

from .schema import (
    CustomerExtraction, PersonaCentroid, Classification, PipelineConfig,
)
from .vectorize import Vectorizer, nan_aware_distance


def classify_single(
    extraction: CustomerExtraction,
    centroids: list[PersonaCentroid],
    vectorizer: Vectorizer,
    config: PipelineConfig,
) -> Classification:
    """Classify a single customer by NaN-aware distance to persona centroids."""
    vec = vectorizer.vectorize_one(extraction)

    distances: dict[int, float] = {}
    for persona in centroids:
        centroid_vec = np.array(persona.centroid_vector)
        dist = nan_aware_distance(vec, centroid_vec)
        distances[persona.persona_id] = dist

    sorted_dists = sorted(distances.items(), key=lambda x: x[1])
    assigned_id, assigned_dist = sorted_dists[0]
    second_id, second_dist = sorted_dists[1] if len(sorted_dists) > 1 else (assigned_id, assigned_dist)

    if second_dist > 0:
        confidence = 1.0 - (assigned_dist / second_dist)
    else:
        confidence = 0.0

    confidence = max(0.0, min(1.0, confidence))

    assigned_name = next(
        (p.name for p in centroids if p.persona_id == assigned_id),
        f"Persona_{assigned_id}",
    )

    # Also flag if too many dimensions are missing (low extraction coverage)
    coverage = extraction.dimensions.tier1_coverage()
    low_coverage = coverage < (config.required_tier1_dimensions / 8)

    return Classification(
        customer_id=extraction.customer_id,
        assigned_persona=assigned_id,
        persona_name=assigned_name,
        confidence=round(confidence, 3),
        distance_to_assigned=round(assigned_dist, 4),
        distance_to_second=round(second_dist, 4),
        all_distances={k: round(v, 4) for k, v in distances.items()},
        flagged_for_review=(
            confidence < config.borderline_confidence_threshold or low_coverage
        ),
    )


def classify_batch(
    extractions: list[CustomerExtraction],
    centroids: list[PersonaCentroid],
    vectorizer: Vectorizer,
    config: PipelineConfig,
) -> list[Classification]:
    """Classify all customers. Returns deterministic results."""
    return [classify_single(e, centroids, vectorizer, config) for e in extractions]


def classification_summary(classifications: list[Classification]) -> dict:
    """Summary statistics for a batch classification."""
    n = len(classifications)
    if n == 0:
        return {"total": 0}

    confidences = [c.confidence for c in classifications]
    flagged = [c for c in classifications if c.flagged_for_review]
    by_persona: dict[str, int] = {}
    for c in classifications:
        by_persona[c.persona_name] = by_persona.get(c.persona_name, 0) + 1

    return {
        "total_classified": n,
        "mean_confidence": round(sum(confidences) / n, 3),
        "median_confidence": round(sorted(confidences)[n // 2], 3),
        "min_confidence": round(min(confidences), 3),
        "flagged_for_review": len(flagged),
        "flagged_rate": round(len(flagged) / n, 3),
        "flagged_customer_ids": [c.customer_id for c in flagged],
        "distribution": by_persona,
    }
