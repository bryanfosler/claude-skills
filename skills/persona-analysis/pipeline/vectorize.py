"""
Convert structured extractions into numerical vectors for clustering.

This is the bridge between LLM-extracted data and deterministic math.
Every customer becomes a fixed-length numerical vector where:
- Scale dimensions → normalized 0-1 values
- Categorical dimensions → one-hot encoded, then NORMALIZED per dimension group
- Multi-select dimensions → binary encoded, then NORMALIZED per dimension group

KEY FIX (V6): Dimension-group normalization prevents categoricals with many
options from dominating distance calculations. A 6-option categorical and a
1-value scale now have equal influence on Euclidean distance.

Missing data uses NaN, not zero. The classify module uses NaN-aware distance.
"""
from __future__ import annotations

import numpy as np

from .schema import CustomerExtraction, PipelineConfig


NAN_SENTINEL = float("nan")


class Vectorizer:
    """
    Converts CustomerExtraction objects into fixed-length numerical vectors.
    The vector layout is deterministic given the same PipelineConfig.
    """

    def __init__(self, config: PipelineConfig):
        self.config = config
        self._build_feature_map()

    def _build_feature_map(self):
        """Build the mapping from dimensions to vector positions."""
        self.feature_names: list[str] = []
        self.feature_positions: dict[str, int | tuple[int, int]] = {}
        pos = 0

        self.scale_dims = [
            "usage_frequency", "feature_depth", "data_engagement",
            "tech_comfort", "budget_sensitivity", "aspiration_gap",
        ]
        for dim in self.scale_dims:
            self.feature_names.append(dim)
            self.feature_positions[dim] = pos
            pos += 1

        self.cat_dims_options = {
            "primary_context": self.config.context_options,
            "purchase_trigger": self.config.trigger_options,
            "social_context": self.config.social_options,
            "brand_relationship": ["loyalist", "pragmatist", "skeptic", "new_to_brand"],
        }
        for dim, options in self.cat_dims_options.items():
            start = pos
            for opt in options:
                self.feature_names.append(f"{dim}_{opt}")
                pos += 1
            self.feature_positions[dim] = (start, pos)

        self.multi_dims_options = {
            "pain_points": self.config.pain_point_options,
            "ecosystem": self.config.ecosystem_options,
        }
        for dim, options in self.multi_dims_options.items():
            start = pos
            for opt in options:
                self.feature_names.append(f"{dim}_{opt}")
                pos += 1
            self.feature_positions[dim] = (start, pos)

        self.vector_length = pos

    def vectorize_one(self, extraction: CustomerExtraction) -> np.ndarray:
        """
        Convert a single CustomerExtraction to a numerical vector.

        Missing dimensions → NaN (not zero). NaN means "unknown" and is
        excluded from distance calculations rather than treated as a low value.
        """
        vec = np.full(self.vector_length, NAN_SENTINEL)
        dims = extraction.dimensions

        # Scale dimensions: normalize 1-5 → 0-1
        for dim_name in self.scale_dims:
            dim = getattr(dims, dim_name, None)
            if dim is not None:
                pos = self.feature_positions[dim_name]
                vec[pos] = (dim.value - 1) / 4.0

        # Categorical dimensions: one-hot, normalized so the group sums to 1
        # (a 6-option categorical doesn't get 6x the distance influence of a scale)
        for dim_name, options in self.cat_dims_options.items():
            dim = getattr(dims, dim_name, None)
            start, end = self.feature_positions[dim_name]
            n_options = len(options)
            if dim is not None and dim.value in options:
                # Set all options to 0, then the selected one to 1/sqrt(n)
                # This normalizes the L2 contribution of the group to match
                # a single scale dimension (max distance = 1)
                for i in range(n_options):
                    vec[start + i] = 0.0
                idx = options.index(dim.value)
                vec[start + idx] = 1.0 / np.sqrt(n_options) if n_options > 0 else 1.0
            # If dim is None, leave as NaN (all positions in group)

        # Multi-select dimensions: binary, normalized per group
        for dim_name, options in self.multi_dims_options.items():
            dim = getattr(dims, dim_name, None)
            start, end = self.feature_positions[dim_name]
            n_options = len(options)
            if dim is not None:
                norm_factor = 1.0 / np.sqrt(n_options) if n_options > 0 else 1.0
                for i in range(n_options):
                    vec[start + i] = 0.0
                for val in dim.values:
                    if val in options:
                        idx = options.index(val)
                        vec[start + idx] = norm_factor
            # If dim is None, leave as NaN

        return vec

    def vectorize_batch(self, extractions: list[CustomerExtraction]) -> np.ndarray:
        """Convert a list of extractions to a matrix (n_customers x n_features)."""
        return np.array([self.vectorize_one(e) for e in extractions])

    def get_dimension_groups(self) -> dict[str, list[int]]:
        """
        Return which vector indices belong to each original dimension.
        Used by validation to measure per-dimension contribution.
        """
        groups: dict[str, list[int]] = {}
        for dim_name in self.scale_dims:
            pos = self.feature_positions[dim_name]
            groups[dim_name] = [pos]
        for dim_name in list(self.cat_dims_options) + list(self.multi_dims_options):
            start, end = self.feature_positions[dim_name]
            groups[dim_name] = list(range(start, end))
        return groups

    def get_present_mask(self, extraction: CustomerExtraction) -> np.ndarray:
        """
        Return a boolean mask of which vector positions have real data (not NaN).
        Used for NaN-aware distance calculations.
        """
        vec = self.vectorize_one(extraction)
        return ~np.isnan(vec)


def nan_aware_distance(a: np.ndarray, b: np.ndarray) -> float:
    """
    Euclidean distance that ignores positions where EITHER vector has NaN.
    Scales the result to compensate for fewer dimensions being compared,
    so distances are comparable regardless of missing data patterns.
    """
    mask = ~(np.isnan(a) | np.isnan(b))
    n_valid = mask.sum()
    if n_valid == 0:
        return float("inf")
    n_total = len(a)
    raw_dist = float(np.sqrt(np.sum((a[mask] - b[mask]) ** 2)))
    # Scale up to what the distance would be if all dims were present
    return raw_dist * np.sqrt(n_total / n_valid)


def impute_nan_with_column_mean(matrix: np.ndarray) -> np.ndarray:
    """
    Replace NaN values with column means for algorithms that can't handle NaN
    (like sklearn's KMeans). This is used ONLY for clustering initialization;
    classification uses nan_aware_distance directly.
    """
    result = matrix.copy()
    for col in range(result.shape[1]):
        col_data = result[:, col]
        nan_mask = np.isnan(col_data)
        if nan_mask.any():
            col_mean = np.nanmean(col_data) if not nan_mask.all() else 0.0
            result[nan_mask, col] = col_mean
    return result
