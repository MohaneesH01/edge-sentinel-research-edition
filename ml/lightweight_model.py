"""A dependency-light centroid classifier for edge-feasibility experiments."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


FEATURES = ["voltage", "current", "temperature", "power"]


@dataclass
class CentroidClassifier:
    centroids: dict[str, dict[str, float]]

    def predict_one(self, row: pd.Series) -> str:
        best_label = "normal"
        best_distance = float("inf")
        for label, centroid in self.centroids.items():
            distance = sum((float(row[feature]) - centroid[feature]) ** 2 for feature in FEATURES)
            if distance < best_distance:
                best_label = label
                best_distance = distance
        return best_label

    def predict(self, frame: pd.DataFrame) -> list[str]:
        return [self.predict_one(row) for _, row in frame.iterrows()]

    def save(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"features": FEATURES, "centroids": self.centroids}, indent=2), encoding="utf-8")
        return path

    @classmethod
    def load(cls, path: Path) -> "CentroidClassifier":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(centroids=data["centroids"])


def train_centroid_classifier(frame: pd.DataFrame) -> CentroidClassifier:
    centroids = {}
    for label, group in frame.groupby("fault_label"):
        centroids[label] = {feature: float(group[feature].mean()) for feature in FEATURES}
    return CentroidClassifier(centroids=centroids)
