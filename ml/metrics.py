"""Classification metrics without external ML dependencies."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class ClassMetrics:
    label: str
    precision: float
    recall: float
    f1: float
    support: int


def safe_divide(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def evaluate(y_true: Iterable[str], y_pred: Iterable[str]) -> tuple[float, list[ClassMetrics], pd.DataFrame]:
    true = list(y_true)
    pred = list(y_pred)
    labels = sorted(set(true) | set(pred))
    accuracy = safe_divide(sum(a == b for a, b in zip(true, pred)), len(true))
    rows: list[ClassMetrics] = []
    for label in labels:
        tp = sum(a == label and b == label for a, b in zip(true, pred))
        fp = sum(a != label and b == label for a, b in zip(true, pred))
        fn = sum(a == label and b != label for a, b in zip(true, pred))
        precision = safe_divide(tp, tp + fp)
        recall = safe_divide(tp, tp + fn)
        f1 = safe_divide(2 * precision * recall, precision + recall)
        support = sum(a == label for a in true)
        rows.append(ClassMetrics(label, precision, recall, f1, support))
    matrix = confusion_matrix(true, pred, labels)
    return accuracy, rows, matrix


def confusion_matrix(y_true: list[str], y_pred: list[str], labels: list[str]) -> pd.DataFrame:
    counts = Counter(zip(y_true, y_pred))
    data = []
    for actual in labels:
        data.append([counts[(actual, predicted)] for predicted in labels])
    return pd.DataFrame(data, index=labels, columns=labels)


def metrics_frame(accuracy: float, rows: list[ClassMetrics]) -> pd.DataFrame:
    data = [
        {
            "label": row.label,
            "precision": round(row.precision, 4),
            "recall": round(row.recall, 4),
            "f1": round(row.f1, 4),
            "support": row.support,
        }
        for row in rows
    ]
    data.append(
        {
            "label": "accuracy",
            "precision": "",
            "recall": "",
            "f1": round(accuracy, 4),
            "support": sum(row.support for row in rows),
        }
    )
    return pd.DataFrame(data)
