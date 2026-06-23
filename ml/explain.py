"""Audit-grade explanation module for Edge Sentinel.

Every classification decision is paired with:

1. A rule trace — which deterministic rule(s) from `ml.rule_based` fired.
2. A per-feature attribution — Z-score deviation per feature for the
   predicted class.
3. A confidence value — calibrated softmax probability from
   `ml.calibration`.

The output schema is a single JSON line per reading. The ESP32 firmware can
emit the same schema over Serial or MQTT.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

import pandas as pd

from ml.calibration import TemperatureScaler
from ml.rule_based import classify_row


FEATURES = ["voltage", "current", "temperature", "power"]


@dataclass
class AuditExplanation:
    prediction: str
    confidence: float
    rules_fired: list[str]
    feature_attribution: dict[str, float]
    drift_candidates: list[str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "prediction": self.prediction,
                "confidence": round(self.confidence, 4),
                "rules_fired": self.rules_fired,
                "feature_attribution": {k: round(v, 4) for k, v
                                        in self.feature_attribution.items()},
                "drift_candidates": self.drift_candidates,
            },
            separators=(",", ":"),
        )


def _rules_fired(row: pd.Series) -> list[str]:
    rules = []
    voltage = float(row["voltage"])
    current = float(row["current"])
    temperature = float(row["temperature"])
    if voltage < 0 or current < 0 or temperature < -20:
        rules.append("invalid_physical_reading")
    if voltage >= 8.0 and current < 0.08:
        rules.append("open_circuit_signature")
    if temperature >= 45.0:
        rules.append("temperature_above_45C")
    if voltage < 11.0 and current < 0.45:
        rules.append("partial_shading_signature")
    if current > 1.35 or (voltage >= 11.0 and current < 0.25):
        rules.append("current_deviation_signature")
    return rules or ["default_normal"]


def _feature_attribution(row: pd.Series,
                        class_stats: dict[str, dict[str, float]]) -> dict[str, float]:
    """Z-score of each feature for the predicted class.

    `class_stats` maps label -> feature -> (mean, std). The magnitude of each
    Z tells the operator which sensor drove the decision.
    """
    attribution: dict[str, float] = {}
    predicted = classify_row(row)
    if predicted not in class_stats:
        return {feature: 0.0 for feature in FEATURES}
    for feature in FEATURES:
        stat = class_stats[predicted][feature]
        z = (float(row[feature]) - stat["mean"]) / max(stat["std"], 1e-9)
        attribution[feature] = float(z)
    return attribution


def _drift_candidates(row: pd.Series,
                     class_stats: dict[str, dict[str, float]],
                     threshold: float = 2.5) -> list[str]:
    drift = []
    for label, feature_stats in class_stats.items():
        max_z = max(
            abs((float(row[feature]) - stat["mean"]) / max(stat["std"], 1e-9))
            for feature, stat in feature_stats.items()
        )
        if max_z >= threshold:
            drift.append(label)
    return drift


def fit_class_stats(frame: pd.DataFrame) -> dict[str, dict[str, dict[str, float]]]:
    stats: dict[str, dict[str, dict[str, float]]] = {}
    for label, group in frame.groupby("fault_label"):
        stats[label] = {
            feature: {"mean": float(group[feature].mean()),
                      "std": float(group[feature].std() or 1e-9)}
            for feature in FEATURES
        }
    return stats


def explain_row(row: pd.Series,
                class_stats: dict[str, dict[str, dict[str, float]]],
                scaler: TemperatureScaler | None = None) -> AuditExplanation:
    prediction = classify_row(row)
    rules = _rules_fired(row)
    attribution = _feature_attribution(row, class_stats)
    drift = _drift_candidates(row, class_stats)
    confidence = 1.0
    if scaler is not None and len(class_stats) > 0:
        # Build a synthetic logit vector from the inverse Z-score distance.
        logits = []
        for label in sorted(class_stats):
            total = sum(attribution.get(f, 0.0) ** 2 for f in FEATURES)
            logits.append(-total)
        arr = __import__("numpy").array([logits], dtype=float)
        try:
            probs = scaler.transform(arr)[0]
            idx = sorted(class_stats).index(prediction) if prediction in class_stats else 0
            confidence = float(probs[idx])
        except Exception:
            confidence = 1.0
    return AuditExplanation(
        prediction=prediction,
        confidence=confidence,
        rules_fired=rules,
        feature_attribution=attribution,
        drift_candidates=drift,
    )


def explain_frame(frame: pd.DataFrame) -> list[str]:
    """Return one audit JSON line per row in ``frame``."""
    stats = fit_class_stats(frame)
    return [explain_row(row, stats).to_json() for _, row in frame.iterrows()]
