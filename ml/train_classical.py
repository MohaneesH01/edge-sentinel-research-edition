"""Classical ML comparison for Edge Sentinel.

Trains Decision Tree, Random Forest, and Isolation Forest on the same
training/test split as ml/train.py and writes metrics + confusion matrices
to reports/.

The intent is to complete the "three detection approaches" story promised in
docs/architecture.md and the project README:

  1. Rule-based (ml/rule_based.py)
  2. Statistical (ml/statistical.py)
  3. Classical ML (this file)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from ml.lightweight_model import FEATURES
from ml.metrics import evaluate, metrics_frame


try:
    from sklearn.ensemble import IsolationForest, RandomForestClassifier
    from sklearn.tree import DecisionTreeClassifier
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "scikit-learn is required for ml.train_classical. "
        "Install with: pip install -r requirements-ml.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATASET = ROOT / "data" / "processed" / "fault_dataset.csv"
DEFAULT_REPORT_DIR = ROOT / "reports"


def load_dataset(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = set(FEATURES + ["fault_label"]) - set(frame.columns)
    if missing:
        raise ValueError(f"dataset missing columns: {sorted(missing)}")
    return frame.dropna(subset=FEATURES + ["fault_label"]).reset_index(drop=True)


def split(frame: pd.DataFrame, seed: int = 42) -> tuple[pd.DataFrame, pd.DataFrame]:
    shuffled = frame.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    boundary = int(len(shuffled) * 0.75)
    return shuffled.iloc[:boundary].copy(), shuffled.iloc[boundary:].copy()


def run_supervised(name: str, model, train: pd.DataFrame, test: pd.DataFrame,
                   report_dir: Path) -> dict:
    model.fit(train[FEATURES], train["fault_label"])
    preds = model.predict(test[FEATURES])
    acc, rows, matrix = evaluate(test["fault_label"], preds)
    metrics_frame(acc, rows).to_csv(report_dir / f"{name}_metrics.csv", index=False)
    matrix.to_csv(report_dir / f"{name}_confusion_matrix.csv")
    return {"name": name, "accuracy": acc}


def run_isolation(train: pd.DataFrame, test: pd.DataFrame,
                  report_dir: Path) -> dict:
    model = IsolationForest(n_estimators=200, contamination=0.05,
                            random_state=42)
    # Fit only on the "normal" class - that's the anomaly baseline.
    normal = train[train["fault_label"] == "normal"]
    model.fit(normal[FEATURES])
    raw = model.predict(test[FEATURES])
    preds = ["normal" if label == 1 else "anomaly" for label in raw]
    true = ["normal" if label == "normal" else "anomaly"
            for label in test["fault_label"]]
    acc, rows, matrix = evaluate(true, preds)
    metrics_frame(acc, rows).to_csv(report_dir / "isolation_forest_metrics.csv",
                                    index=False)
    matrix.to_csv(report_dir / "isolation_forest_confusion_matrix.csv")
    return {"name": "isolation_forest", "accuracy": acc}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train classical ML baselines for Edge Sentinel"
    )
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--report-dir", type=Path, default=DEFAULT_REPORT_DIR)
    args = parser.parse_args()

    args.report_dir.mkdir(parents=True, exist_ok=True)
    frame = load_dataset(args.dataset)
    train, test = split(frame)

    results = []
    results.append(run_supervised(
        "decision_tree",
        DecisionTreeClassifier(max_depth=8, random_state=42),
        train, test, args.report_dir,
    ))
    results.append(run_supervised(
        "random_forest",
        RandomForestClassifier(n_estimators=200, max_depth=12, random_state=42),
        train, test, args.report_dir,
    ))
    results.append(run_isolation(train, test, args.report_dir))

    summary = pd.DataFrame(results)
    summary.to_csv(args.report_dir / "classical_ml_summary.csv", index=False)
    for row in results:
        print(f"{row['name']}: accuracy={row['accuracy']:.4f}")


if __name__ == "__main__":
    main()
