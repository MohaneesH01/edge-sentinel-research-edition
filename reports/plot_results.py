"""Render confusion matrices and per-class F1 bar charts from the metrics CSVs.

Reads:
    reports/rule_based_metrics.csv
    reports/centroid_metrics.csv
    reports/decision_tree_metrics.csv
    reports/random_forest_metrics.csv
    reports/isolation_forest_metrics.csv
    reports/rule_based_confusion_matrix.csv
    reports/centroid_confusion_matrix.csv
    reports/decision_tree_confusion_matrix.csv
    reports/random_forest_confusion_matrix.csv
    reports/isolation_forest_confusion_matrix.csv

Writes PNGs to reports/figures/.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402


REPORT_DIR = Path(__file__).resolve().parents[1] / "reports"
FIG_DIR = REPORT_DIR / "figures"

METHODS = [
    "rule_based",
    "centroid",
    "decision_tree",
    "random_forest",
    "isolation_forest",
]


def _ensure_fig_dir() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)


def plot_confusion(method: str) -> Path | None:
    path = REPORT_DIR / f"{method}_confusion_matrix.csv"
    if not path.exists():
        return None
    matrix = pd.read_csv(path, index_col=0)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix.values, cmap="Blues")
    ax.set_title(f"Confusion matrix: {method}")
    ax.set_xticks(range(len(matrix.columns)))
    ax.set_xticklabels(matrix.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(matrix.index)))
    ax.set_yticklabels(matrix.index)
    for i in range(len(matrix.index)):
        for j in range(len(matrix.columns)):
            ax.text(j, i, int(matrix.values[i, j]),
                    ha="center", va="center",
                    color="white" if matrix.values[i, j] > matrix.values.max() / 2 else "black")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    out = FIG_DIR / f"{method}_confusion_matrix.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def plot_accuracy_bar() -> Path | None:
    rows = []
    for method in METHODS:
        path = REPORT_DIR / f"{method}_metrics.csv"
        if not path.exists():
            continue
        metrics = pd.read_csv(path)
        acc_row = metrics[metrics["label"] == "accuracy"]
        if acc_row.empty:
            continue
        rows.append({"method": method, "accuracy": float(acc_row.iloc[0]["f1"])})
    if not rows:
        return None
    df = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(df["method"], df["accuracy"], color="#0B3D2E")
    ax.set_ylim(0, 1)
    ax.set_ylabel("accuracy")
    ax.set_title("Edge Sentinel: accuracy by method")
    for bar, value in zip(bars, df["accuracy"]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 0.01,
                f"{value:.3f}", ha="center")
    fig.tight_layout()
    out = FIG_DIR / "accuracy_by_method.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    return out


def main() -> None:
    _ensure_fig_dir()
    written = []
    for method in METHODS:
        out = plot_confusion(method)
        if out:
            written.append(out)
    out = plot_accuracy_bar()
    if out:
        written.append(out)
    for path in written:
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
