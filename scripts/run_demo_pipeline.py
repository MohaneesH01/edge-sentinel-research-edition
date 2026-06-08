"""Run the complete local Edge Sentinel research demo pipeline."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def run(args: list[str]) -> None:
    print("$", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    run([PYTHON, "-m", "backend.generate_dataset", "--records-per-class", "900"])
    run([PYTHON, "-m", "ml.train"])
    run([PYTHON, "tinyml/export_centroid_header.py"])
    run([PYTHON, "-m", "reports.generate_report"])
    run([PYTHON, "-m", "dashboard.static_dashboard"])
    print("complete: reports/edge_sentinel_experiment_report.md")


if __name__ == "__main__":
    main()
