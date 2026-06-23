"""Statistical baseline detector for Edge Sentinel.

Implements a per-class mean+std model trained on the labelled dataset, then
classifies a new reading by reporting the per-class Z-score and flagging the
class whose |Z| is lowest (most likely) and any class whose |Z| exceeds a
threshold (drift candidates).

Output is intentionally a pandas DataFrame so callers can plug it into the
existing metrics pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


FEATURES = ["voltage", "current", "temperature", "power"]
DEFAULT_DRIFT_THRESHOLD = 2.5


@dataclass
class StatisticalBaseline:
    feature_stats: dict[str, dict[str, dict[str, float]]]
    drift_threshold: float = DEFAULT_DRIFT_THRESHOLD

    @classmethod
    def fit(cls, frame: pd.DataFrame,
            drift_threshold: float = DEFAULT_DRIFT_THRESHOLD) -> "StatisticalBaseline":
        stats: dict[str, dict[str, dict[str, float]]] = {}
        for label, group in frame.groupby("fault_label"):
            stats[label] = {
                feature: {"mean": float(group[feature].mean()),
                          "std": float(group[feature].std() or 1e-9)}
                for feature in FEATURES
            }
        return cls(stats, drift_threshold)

    def predict_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for _, row in frame.iterrows():
            best_label = "normal"
            best_score = float("inf")
            drift_labels = []
            for label, feature_stats in self.feature_stats.items():
                z_total = 0.0
                for feature, stat in feature_stats.items():
                    z = (float(row[feature]) - stat["mean"]) / stat["std"]
                    z_total += z * z
                    if abs(z) >= self.drift_threshold:
                        drift_labels.append(label)
                if z_total < best_score:
                    best_score = z_total
                    best_label = label
            rows.append({"prediction": best_label,
                         "drift_candidates": ",".join(sorted(set(drift_labels)))})
        return pd.DataFrame(rows)

    def explain_row(self, row: pd.Series) -> dict[str, dict[str, float]]:
        explanation = {}
        for label, feature_stats in self.feature_stats.items():
            explanation[label] = {
                feature: round(
                    (float(row[feature]) - stat["mean"]) / stat["std"], 3)
                for feature, stat in feature_stats.items()
            }
        return explanation


def classify_frame(frame: pd.DataFrame,
                  drift_threshold: float = DEFAULT_DRIFT_THRESHOLD) -> pd.Series:
    baseline = StatisticalBaseline.fit(frame, drift_threshold)
    return baseline.predict_frame(frame)["prediction"]
