"""Generate a Markdown experiment report from pipeline outputs."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
DATASET = ROOT / "data" / "processed" / "fault_dataset.csv"
OUTPUT = REPORT_DIR / "edge_sentinel_experiment_report.md"


def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path).fillna("") if path.exists() else pd.DataFrame()


def table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "Pending."
    columns = list(frame.columns)
    widths = {
        column: max(len(str(column)), *(len(str(value)) for value in frame[column].tolist()))
        for column in columns
    }
    header = "| " + " | ".join(str(column).ljust(widths[column]) for column in columns) + " |"
    separator = "| " + " | ".join("-" * widths[column] for column in columns) + " |"
    rows = [
        "| " + " | ".join(str(row[column]).ljust(widths[column]) for column in columns) + " |"
        for _, row in frame.iterrows()
    ]
    return "\n".join([header, separator, *rows])


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    dataset = load_csv(DATASET)
    rule_metrics = load_csv(REPORT_DIR / "rule_based_metrics.csv")
    centroid_metrics = load_csv(REPORT_DIR / "centroid_metrics.csv")

    class_counts = dataset["fault_label"].value_counts().rename_axis("fault_label").reset_index(name="records")
    text = f"""# Edge Sentinel Experiment Report

## Objective

Evaluate whether a low-cost ESP32-class renewable-energy monitoring system can detect solar fault conditions using local telemetry, deterministic analytics, and edge-feasible classification.

## Dataset Summary

Records: {len(dataset)}

{table(class_counts)}

## Rule-Based Detection

{table(rule_metrics)}

## Lightweight Edge Classifier

{table(centroid_metrics)}

## Interpretation

The generated dataset provides a controlled development baseline for validating the software stack before physical fault-injection data is collected. Final research conclusions must be based on hardware readings from the ESP32, INA219, and DHT22 setup.

## Next Experimental Step

Replace or augment `data/processed/fault_dataset.csv` with hardware telemetry collected from controlled fault scenarios, then rerun:

```bash
python scripts/run_demo_pipeline.py
```
"""
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"generated {OUTPUT}")


if __name__ == "__main__":
    main()
