"""
Phase 2: Discover personas via deterministic clustering.

Takes vectorized customer data and finds natural groupings.
100% deterministic — same input + same config = same personas every time.

V6 fixes:
- Uses mean-imputed matrix for KMeans (which can't handle NaN)
- Adds minimum silhouette threshold — returns NO_CLUSTERS if data has no structure
- PCA dimensionality reduction when feature/sample ratio is unfavorable
"""
from __future__ import annotations

import math

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score

from .schema import CustomerExtraction, PersonaCentroid, PipelineConfig
from .vectorize import Vectorizer, impute_nan_with_column_mean

MIN_SILHOUETTE_THRESHOLD = 0.25


def maybe_reduce_dimensions(
    matrix: np.ndarray,
    config: PipelineConfig,
) -> tuple[np.ndarray, PCA | None]:
    """
    Apply PCA if the feature-to-sample ratio is unfavorable (>2:1).
    With 26 features and 10 interviews, you get spurious clusters.
    PCA reduces to the number of components that explain 90% of variance,
    capped at n_samples - 1.
    """
    n_samples, n_features = matrix.shape
    if n_features <= n_samples * 2:
        return matrix, None

    max_components = min(n_samples - 1, n_features)
    pca = PCA(n_components=max_components, random_state=config.random_seed)
    transformed = pca.fit_transform(matrix)

    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    n_keep = int(np.searchsorted(cumulative_variance, 0.90) + 1)
    n_keep = max(2, min(n_keep, max_components))

    return transformed[:, :n_keep], pca


def find_optimal_k(
    matrix: np.ndarray,
    config: PipelineConfig,
) -> tuple[int | None, dict[int, float]]:
    """
    Determine optimal number of personas using silhouette analysis.

    Returns (best_k, {k: silhouette_score}).
    Returns (None, scores) if no k produces silhouette above threshold,
    meaning the data doesn't support distinct personas.
    """
    n = matrix.shape[0]
    max_k = config.max_clusters or max(2, int(math.sqrt(n)))
    max_k = min(max_k, n - 1)

    if max_k < 2:
        return None, {}

    scores: dict[int, float] = {}
    for k in range(2, max_k + 1):
        km = KMeans(n_clusters=k, random_state=config.random_seed, n_init=10)
        labels = km.fit_predict(matrix)
        if len(set(labels)) < 2:
            continue
        unique, counts = np.unique(labels, return_counts=True)
        if min(counts) < config.min_cluster_size:
            continue
        scores[k] = silhouette_score(matrix, labels)

    if not scores:
        return None, {}

    best_k = max(scores, key=scores.get)
    if scores[best_k] < MIN_SILHOUETTE_THRESHOLD:
        return None, scores

    return best_k, scores


def cluster_customers(
    extractions: list[CustomerExtraction],
    config: PipelineConfig,
    vectorizer: Vectorizer,
    k_override: int | None = None,
) -> tuple[np.ndarray, KMeans, int | None, dict[int, float], bool]:
    """
    Cluster customers into persona groups.

    Returns:
        labels: array of cluster assignments (one per customer), or empty if no clusters
        model: the fitted KMeans model
        k: number of clusters used (None if no structure found)
        silhouette_scores: {k: score} for all evaluated k values
        pca_applied: whether PCA dimensionality reduction was used
    """
    raw_matrix = vectorizer.vectorize_batch(extractions)
    matrix = impute_nan_with_column_mean(raw_matrix)

    # Dimensionality reduction if needed
    matrix_for_clustering, pca = maybe_reduce_dimensions(matrix, config)
    pca_applied = pca is not None

    if k_override:
        k = k_override
        sil_scores: dict[int, float] = {}
    else:
        k, sil_scores = find_optimal_k(matrix_for_clustering, config)

    if k is None:
        # No natural clusters found — data doesn't support distinct personas
        empty_labels = np.zeros(len(extractions), dtype=int)
        km = KMeans(n_clusters=1, random_state=config.random_seed)
        km.fit(matrix_for_clustering)
        return empty_labels, km, None, sil_scores, pca_applied

    km = KMeans(n_clusters=k, random_state=config.random_seed, n_init=10)
    labels = km.fit_predict(matrix_for_clustering)

    if len(set(labels)) >= 2:
        sil_scores[k] = silhouette_score(matrix_for_clustering, labels)

    return labels, km, k, sil_scores, pca_applied


def compute_discrimination_scores(
    matrix: np.ndarray,
    labels: np.ndarray,
    vectorizer: Vectorizer,
) -> dict[str, float]:
    """
    For each original dimension, compute how much it contributes to cluster separation.
    Uses NaN-imputed matrix for computation.
    """
    matrix = impute_nan_with_column_mean(matrix)
    groups = vectorizer.get_dimension_groups()
    scores: dict[str, float] = {}

    for dim_name, indices in groups.items():
        sub_matrix = matrix[:, indices]
        total_var = np.var(sub_matrix, axis=0).sum()
        if total_var == 0:
            scores[dim_name] = 0.0
            continue

        grand_mean = sub_matrix.mean(axis=0)
        between_var = 0.0
        for label in np.unique(labels):
            mask = labels == label
            cluster_mean = sub_matrix[mask].mean(axis=0)
            between_var += mask.sum() * np.sum((cluster_mean - grand_mean) ** 2)
        between_var /= len(labels)

        scores[dim_name] = between_var / total_var if total_var > 0 else 0.0

    total = sum(scores.values())
    if total > 0:
        scores = {k: v / total for k, v in scores.items()}

    return scores


def build_persona_centroids(
    extractions: list[CustomerExtraction],
    labels: np.ndarray,
    km: KMeans,
    vectorizer: Vectorizer,
) -> list[PersonaCentroid]:
    """Build PersonaCentroid objects from clustering results."""
    raw_matrix = vectorizer.vectorize_batch(extractions)
    matrix = impute_nan_with_column_mean(raw_matrix)

    disc_scores = compute_discrimination_scores(matrix, labels, vectorizer)
    sorted_dims = sorted(disc_scores.items(), key=lambda x: -x[1])

    n_total = len(extractions)
    personas = []

    # Compute centroids in the ORIGINAL feature space (not PCA space)
    # so that centroid vectors are interpretable
    for cluster_id in range(km.n_clusters):
        mask = labels == cluster_id
        cluster_matrix = matrix[mask]
        original_centroid = cluster_matrix.mean(axis=0)

        cluster_extractions = [e for e, m in zip(extractions, mask) if m]
        size = int(mask.sum())
        top_dims = [name for name, _ in sorted_dims[:4]]

        quotes = []
        for ext in cluster_extractions[:3]:
            dims = ext.dimensions
            for attr in ["purchase_trigger", "primary_context", "usage_frequency"]:
                dim = getattr(dims, attr, None)
                if dim is not None and dim.evidence and dim.evidence != "test":
                    quotes.append(dim.evidence)
                    break

        personas.append(PersonaCentroid(
            persona_id=cluster_id,
            name=f"Persona_{cluster_id}",
            size=size,
            proportion=size / n_total,
            centroid_vector=original_centroid.tolist(),
            discriminating_dimensions=top_dims,
            representative_quotes=quotes,
        ))

    return personas
