"""
Phase 4: Validation suite for persona models.

Catches overfit, fragility, and statistical ghosts before they infect
downstream JTBD analysis.

V6 fix: Uses NaN-imputed matrices for KMeans operations.
"""
from __future__ import annotations

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from .schema import (
    CustomerExtraction, PersonaCentroid, Classification,
    ValidationReport, PipelineConfig,
)
from .vectorize import Vectorizer, impute_nan_with_column_mean
from .cluster import compute_discrimination_scores


def check_overfit(
    disc_scores: dict[str, float],
    config: PipelineConfig,
) -> list[str]:
    """Flag dimensions that dominate cluster separation beyond threshold."""
    flags = []
    for dim, score in disc_scores.items():
        if score > config.overfit_threshold:
            flags.append(
                f"OVERFIT WARNING: '{dim}' contributes {score:.1%} of cluster "
                f"separation (threshold: {config.overfit_threshold:.0%}). "
                f"Re-run clustering without this dimension to check if "
                f"personas survive."
            )
    return flags


def leave_one_out_stability(
    extractions: list[CustomerExtraction],
    original_labels: np.ndarray,
    config: PipelineConfig,
    vectorizer: Vectorizer,
) -> float:
    """
    Remove each customer one at a time, re-cluster, measure how much
    the remaining customers' assignments change.

    Returns: stability score (0-1). 1.0 = perfectly stable.
    """
    n = len(extractions)
    if n < 5:
        return 1.0

    k = len(set(original_labels))
    if k < 2:
        return 1.0

    total_changed = 0
    total_compared = 0

    for i in range(n):
        remaining = [e for j, e in enumerate(extractions) if j != i]
        remaining_labels_orig = np.array([l for j, l in enumerate(original_labels) if j != i])

        matrix = impute_nan_with_column_mean(vectorizer.vectorize_batch(remaining))
        km = KMeans(n_clusters=k, random_state=config.random_seed, n_init=10)
        new_labels = km.fit_predict(matrix)

        for a in range(len(remaining)):
            for b in range(a + 1, len(remaining)):
                orig_same = remaining_labels_orig[a] == remaining_labels_orig[b]
                new_same = new_labels[a] == new_labels[b]
                if orig_same != new_same:
                    total_changed += 1
                total_compared += 1

    if total_compared == 0:
        return 1.0
    return 1.0 - (total_changed / total_compared)


def dimension_sensitivity(
    extractions: list[CustomerExtraction],
    original_labels: np.ndarray,
    config: PipelineConfig,
    vectorizer: Vectorizer,
) -> dict[str, float]:
    """
    Remove each dimension group, re-cluster, measure assignment change.

    Returns: {dimension: change_rate}
    - < 0.05: decorative dimension (consider dropping)
    - 0.05 - 0.30: contributing dimension
    - > 0.30: load-bearing dimension
    """
    groups = vectorizer.get_dimension_groups()
    full_matrix = impute_nan_with_column_mean(vectorizer.vectorize_batch(extractions))
    k = len(set(original_labels))
    if k < 2:
        return {dim: 0.0 for dim in groups}

    n = len(extractions)
    results: dict[str, float] = {}

    for dim_name, indices in groups.items():
        reduced_matrix = full_matrix.copy()
        reduced_matrix[:, indices] = 0

        km = KMeans(n_clusters=k, random_state=config.random_seed, n_init=10)
        new_labels = km.fit_predict(reduced_matrix)

        changed_pairs = 0
        total_pairs = 0
        for a in range(n):
            for b in range(a + 1, n):
                orig_same = original_labels[a] == original_labels[b]
                new_same = new_labels[a] == new_labels[b]
                if orig_same != new_same:
                    changed_pairs += 1
                total_pairs += 1

        results[dim_name] = changed_pairs / total_pairs if total_pairs > 0 else 0.0

    return results


def borderline_analysis(
    classifications: list[Classification],
    config: PipelineConfig,
) -> dict:
    """Analyze borderline cases for model health signals."""
    borderline = [c for c in classifications if c.flagged_for_review]
    rate = len(borderline) / len(classifications) if classifications else 0

    interpretation = "healthy"
    if rate > 0.3:
        interpretation = "fragile — personas may need to be merged or dimensions added"
    elif rate > 0.2:
        interpretation = "acceptable but investigate borderline cases"

    persona_borderline: dict[str, int] = {}
    for c in borderline:
        persona_borderline[c.persona_name] = persona_borderline.get(c.persona_name, 0) + 1

    return {
        "borderline_count": len(borderline),
        "borderline_rate": round(rate, 3),
        "interpretation": interpretation,
        "borderline_by_persona": persona_borderline,
        "borderline_customer_ids": [c.customer_id for c in borderline],
    }


def run_full_validation(
    extractions: list[CustomerExtraction],
    labels: np.ndarray,
    classifications: list[Classification],
    config: PipelineConfig,
    vectorizer: Vectorizer,
) -> ValidationReport:
    """Run the complete validation suite and produce a report."""
    matrix = vectorizer.vectorize_batch(extractions)

    disc_scores = compute_discrimination_scores(matrix, labels, vectorizer)
    overfit_flags = check_overfit(disc_scores, config)
    borderline = borderline_analysis(classifications, config)
    loo_stability = leave_one_out_stability(extractions, labels, config, vectorizer)
    dim_sensitivity = dimension_sensitivity(extractions, labels, config, vectorizer)

    health = "healthy"
    if overfit_flags:
        health = "fragile"
    elif borderline["borderline_rate"] > 0.2:
        health = "acceptable"
    elif loo_stability < 0.8:
        health = "fragile"

    return ValidationReport(
        dimension_contributions=disc_scores,
        overfit_flags=overfit_flags,
        borderline_rate=borderline["borderline_rate"],
        leave_one_out_stability=round(loo_stability, 3),
        dimension_sensitivity=dim_sensitivity,
        overall_health=health,
    )
