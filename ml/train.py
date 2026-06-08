"""Train and evaluate Edge Sentinel baseline models."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ml.lightweight_model import FEATURES, train_centroid_classifier
from ml.metrics import evaluate, metrics_frame
from ml.rule_based import classify_frame


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "data" / "processed" / "fault_dataset.csv"
DEFAULT_REPORT_DIR = ROOT / "reports"
DEFAULT_MODEL = ROOT / "tinyml" / "centroid_model.json"


def load_dataset(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = set(FEATURES + ["fault_label"]) - set(frame.columns)
    if missing:
        raise ValueError(f"dataset missing columns: {sorted(missing)}")
    return frame.dropna(subset=FEATURES + ["fault_label"])


def split_dataset(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    shuffled = frame.sample(frac=1.0, random_state=42).reset_index(drop=True)
    split_at = int(len(shuffled) * 0.75)
    return shuffled.iloc[:split_at].copy(), shuffled.iloc[split_at:].copy()


def write_model_card(report_dir: Path, dataset: Path, accuracy: float) -> None:
    text = f"""# Edge Sentinel Baseline Model Card

## Model

Centroid classifier trained on voltage, current, temperature, and power.

## Purpose

This dependency-light model is included as an edge-feasibility baseline. It is not the final research model, but it provides a simple deployable classifier while Decision Tree, Random Forest, and Isolation Forest experiments are added in environments with scikit-learn.

## Dataset

`{dataset}`

## Validation Accuracy

{accuracy:.4f}

## Deployment Notes

The exported JSON model in `tinyml/centroid_model.json` can be converted to C arrays or used as a reference for ESP32-side distance-based inference.
"""
    (report_dir / "model_card.md").write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Edge Sentinel baseline models")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    parser.add_argument("--model-output", type=Path, default=DEFAULT_MODEL)
    args = parser.parse_args()
    frame = load_dataset(args.dataset)
    args.report_dir.mkdir(parents=True, exist_ok=True)

    train_frame, test_frame = split_dataset(frame)

    rule_predictions = classify_frame(test_frame)
    rule_accuracy, rule_rows, rule_matrix = evaluate(test_frame["fault_label"], rule_predictions)
    metrics_frame(rule_accuracy, rule_rows).to_csv(args.report_dir / "rule_based_metrics.csv", index=False)
    rule_matrix.to_csv(args.report_dir / "rule_based_confusion_matrix.csv")

    centroid = train_centroid_classifier(train_frame)
    centroid_predictions = centroid.predict(test_frame)
    model_accuracy, model_rows, model_matrix = evaluate(test_frame["fault_label"], centroid_predictions)
    metrics_frame(model_accuracy, model_rows).to_csv(args.report_dir / "centroid_metrics.csv", index=False)
    model_matrix.to_csv(args.report_dir / "centroid_confusion_matrix.csv")
    centroid.save(args.model_output)
    write_model_card(args.report_dir, args.dataset, model_accuracy)

    print(f"rule_based_accuracy={rule_accuracy:.4f}")
    print(f"centroid_accuracy={model_accuracy:.4f}")
    print(f"saved_model={args.model_output}")


if __name__ == "__main__":
    main()
