"""
Data models for the persona analysis pipeline.
All types are strict dataclasses — no free-form dicts flowing through the system.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional


@dataclass
class ScoredValue:
    value: int
    evidence: str
    confidence: str = "medium"  # high | medium | low


@dataclass
class CategoricalValue:
    value: str
    evidence: str
    confidence: str = "medium"


@dataclass
class MultiselectValue:
    values: list[str]
    evidence: list[str]
    confidence: str = "medium"


@dataclass
class SwitchingHistory:
    switched_from: str = ""
    switched_to: str = ""
    switch_reason: str = ""
    evidence: str = ""


@dataclass
class ExtractionDimensions:
    # Tier 1 — required
    usage_frequency: ScoredValue | None = None
    feature_depth: ScoredValue | None = None
    primary_context: CategoricalValue | None = None
    data_engagement: ScoredValue | None = None
    purchase_trigger: CategoricalValue | None = None
    pain_points: MultiselectValue | None = None
    ecosystem: MultiselectValue | None = None
    social_context: CategoricalValue | None = None

    # Tier 2 — optional
    tech_comfort: ScoredValue | None = None
    brand_relationship: CategoricalValue | None = None
    budget_sensitivity: ScoredValue | None = None
    information_sources: MultiselectValue | None = None
    aspiration_gap: ScoredValue | None = None
    switching_history: SwitchingHistory | None = None

    TIER1_FIELDS = [
        "usage_frequency", "feature_depth", "primary_context",
        "data_engagement", "purchase_trigger", "pain_points",
        "ecosystem", "social_context",
    ]

    def tier1_coverage(self) -> float:
        present = sum(1 for f in self.TIER1_FIELDS if getattr(self, f) is not None)
        return present / len(self.TIER1_FIELDS)


@dataclass
class CustomerExtraction:
    customer_id: str
    interview_date: str
    dimensions: ExtractionDimensions
    interviewer: str = ""
    extraction_passes: int = 3
    extraction_model: str = ""
    notes: str = ""


@dataclass
class PersonaCentroid:
    persona_id: int
    name: str
    size: int
    proportion: float
    centroid_vector: list[float]
    discriminating_dimensions: list[str]
    boundary_conditions: dict[str, str] = field(default_factory=dict)
    representative_quotes: list[str] = field(default_factory=list)
    demographic_overlay: str = ""


@dataclass
class Classification:
    customer_id: str
    assigned_persona: int
    persona_name: str
    confidence: float
    distance_to_assigned: float
    distance_to_second: float
    all_distances: dict[int, float] = field(default_factory=dict)
    flagged_for_review: bool = False


@dataclass
class ValidationReport:
    dimension_contributions: dict[str, float]
    overfit_flags: list[str]
    borderline_rate: float
    leave_one_out_stability: float
    dimension_sensitivity: dict[str, float]
    overall_health: str  # healthy | acceptable | fragile


@dataclass
class PipelineConfig:
    extraction_passes: int = 3
    extraction_temperature: float = 0.0
    min_cluster_size: int = 3
    max_clusters: int | None = None
    random_seed: int = 42
    overfit_threshold: float = 0.50
    borderline_confidence_threshold: float = 0.20
    required_tier1_dimensions: int = 5

    # Domain-specific option lists (loaded from project_config.json)
    context_options: list[str] = field(default_factory=list)
    trigger_options: list[str] = field(default_factory=list)
    pain_point_options: list[str] = field(default_factory=list)
    ecosystem_options: list[str] = field(default_factory=list)
    social_options: list[str] = field(default_factory=lambda: [
        "solo", "group", "competitive", "community", "professional"
    ])

    @classmethod
    def from_file(cls, path: str | Path) -> PipelineConfig:
        with open(path) as f:
            raw = json.load(f)
        settings = raw.get("pipeline_settings", {})
        options = raw.get("dimension_options", {})
        return cls(
            extraction_passes=settings.get("extraction_passes", 3),
            extraction_temperature=settings.get("extraction_temperature", 0.0),
            min_cluster_size=settings.get("min_cluster_size", 3),
            max_clusters=settings.get("max_clusters"),
            random_seed=settings.get("random_seed", 42),
            overfit_threshold=settings.get("overfit_threshold", 0.50),
            borderline_confidence_threshold=settings.get("borderline_confidence_threshold", 0.20),
            required_tier1_dimensions=settings.get("required_tier1_dimensions", 5),
            context_options=options.get("primary_context", {}).get("options", []),
            trigger_options=options.get("purchase_trigger", {}).get("options", []),
            pain_point_options=options.get("pain_points", {}).get("options", []),
            ecosystem_options=options.get("ecosystem", {}).get("options", []),
            social_options=options.get("social_context", {}).get("options", [
                "solo", "group", "competitive", "community", "professional"
            ]),
        )


def serialize(obj) -> dict:
    """Convert dataclasses to JSON-serializable dicts, handling nested types."""
    if hasattr(obj, "__dataclass_fields__"):
        return {k: serialize(v) for k, v in asdict(obj).items()}
    return obj
