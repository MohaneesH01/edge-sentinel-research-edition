"""Run the complete Edge Sentinel demo pipeline.

Steps:
1. Generate the synthetic fault dataset (or reuse the existing CSV).
2. Train the rule-based baseline.
3. Train the lightweight centroid classifier.
4. Train the classical ML baselines (Decision Tree, Random Forest,
   Isolation Forest).
5. Render confusion matrices and accuracy-by-method PNGs into
   reports/figures/.
6. Export the centroid model JSON + C header to tinyml/.

This is the single command reviewers and contributors should run to
reproduce every number and figure in reports/edge_sentinel_experiment_report.md.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(label: str, cmd: list[str]) -> None:
    print(f"\n=== {label} ===")
    result = subprocess.run(cmd, cwd=ROOT)
    if result.returncode != 0:
        print(f"step failed: {label}")
        sys.exit(result.returncode)


def main() -> None:
    dataset = ROOT / "data" / "processed" / "fault_dataset.csv"
    if not dataset.exists():
        run("generate dataset", [sys.executable, "-m", "backend.generate_dataset",
                                  "--output", str(dataset)])
    run("rule-based + centroid baseline",
        [sys.executable, "-m", "ml.train", "--dataset", str(dataset)])
    run("classical ML baselines",
        [sys.executable, "-m", "ml.train_classical", "--dataset", str(dataset)])
    run("render figures",
        [sys.executable, "-c",
         "import sys; sys.path.insert(0, '.'); import reports.plot_results as p; p.main()"])
    run("export tinyml header",
        [sys.executable, "-m", "tinyml.export_centroid_header"])
    print("\n=== pipeline complete ===")


if __name__ == "__main__":
    main()
