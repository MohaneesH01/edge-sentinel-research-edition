# Edge Sentinel Research Edition

**Edge Sentinel Research Edition** is an intelligent renewable-infrastructure
monitoring prototype for detecting solar-system anomalies using embedded
sensing, local analytics, and TinyML-ready edge inference.

It is the research flagship of a 5-repo portfolio: this project anchors the
research question, the IEEE Access paper, and the MS application narrative.
Four sibling repos (SmartGrid Digital Twin, Predictive Maintenance Lab,
Industrial Edge Vision, Autonomous Energy Management) co-build on the same
stack.

## Research Question (v2)

> Can a sub-$50-volume BOM ESP32-class edge node, deployed at the panel level,
> run a quantized TFLite-Micro (int8) on-device classifier that detects and
> classifies the six fault modes — **normal, open-circuit, partial shading,
> temperature anomaly, current deviation, sensor failure** — of distributed
> rooftop PV under real-world conditions of irradiance variability,
> temperature drift, and sensor aging, achieving **F1 ≥ 0.85 per class** on a
> held-out test set of ≥ 1,500 labelled real-world samples with
> temperature-scaled calibrated confidence, while remaining energy-autonomous,
> fully offline, and demonstrably reproducible across panel brands and
> climates, and producing **audit-grade explanations** for every
> classification decision?

Sub-hypotheses, definitions, and out-of-scope items live in
[`docs/research_question.md`](docs/research_question.md). Known limitations
live in [`docs/threats_to_validity.md`](docs/threats_to_validity.md).

## System Goals

- Monitor voltage, current, temperature, and calculated power from a
  solar-energy test setup.
- Publish telemetry through MQTT over WiFi.
- Store structured readings locally for dataset generation.
- Detect faults using rule-based, statistical, and machine-learning methods.
- Compare detection approaches on accuracy, precision, recall, F1, false
  positives, false negatives, latency, and calibration.
- Deploy the best feasible model to an ESP32-class edge device.
- Validate observed behavior against a simplified MATLAB solar-system
  simulation.
- Emit per-decision audit explanations (rule trace + feature attribution +
  calibrated confidence).

## Architecture

```text
ESP32 + INA219 + DHT22 (or MPU6050 v2)
        |
        | MQTT telemetry
        v
Python backend (backend/)
        |
        | SQLite + CSV export
        v
Analytics + ML pipeline (ml/)
        |
        | model conversion
        v
TinyML edge inference (tinyml/) + audit-grade explanations (ml/explain.py)
        |
        v
Streamlit dashboard (dashboard/) + research reports (reports/)
```

## Current Status (synthetic-data baseline, v2)

All five detection methods now run end-to-end and are auto-rendered into
`reports/figures/`.

| Method | Accuracy | Use case |
| --- | ---: | --- |
| Rule-based detection | 0.9133 | deterministic baseline |
| Centroid (edge-feasible) | 0.8096 | the only model small enough for ESP32 RAM |
| Decision Tree | 0.9770 | multi-class reference |
| Random Forest | **0.9800** | strongest off-device model |
| Isolation Forest | 0.9163 | normal-vs-anomaly framing |

14/14 pytest tests pass. The full pipeline runs with one command:

```bash
python scripts/run_demo_pipeline.py
```

This regenerates the dataset, trains all five methods, renders six PNG
figures into `reports/figures/`, and exports the centroid model JSON + C
header to `tinyml/`.

## What is done (software-complete)

| Module | Path | Status |
| --- | --- | --- |
| Research scaffold + docs | `docs/` | done |
| Sharpened research question + 4 sub-hypotheses | `docs/research_question.md` | done |
| Literature review starter (10 papers, structured) | `docs/literature_review.md` | done |
| Threats-to-validity section | `docs/threats_to_validity.md` | done |
| Bench checklist PDF (15 steps) | `docs/Edge_Sentinel_Bench_Checklist.pdf` | done |
| Learning roadmap PDF (24 topics) | `docs/learning/Edge_Sentinel_Learning_and_References.pdf` | done |
| ESP32 firmware skeleton | `firmware/esp32_edge_sentinel/` | done |
| Synthetic fault-dataset generator | `backend/generate_dataset.py` | done |
| Rule-based detector | `ml/rule_based.py` | done |
| Statistical baseline (Z-score) | `ml/statistical.py` | done |
| Centroid classifier (edge-feasible) | `ml/lightweight_model.py` | done |
| Classical ML comparison (DT, RF, IF) | `ml/train_classical.py` | done |
| Temperature-scaled calibration | `ml/calibration.py` | done |
| Audit-grade explanation module | `ml/explain.py` | done |
| Per-class metrics + confusion matrices | `ml/metrics.py`, `reports/plot_results.py` | done |
| Auto-rendered figures (6 PNGs) | `reports/figures/` | done |
| TinyML JSON + C header export | `tinyml/` | done |
| Static + Streamlit dashboards | `dashboard/` | done |
| Experiment report (auto-regenerated) | `reports/edge_sentinel_experiment_report.md` | done |
| One-command pipeline runner | `scripts/run_demo_pipeline.py` | done |
| GitHub repo + CI workflow + topics | github.com/MohaneesH01/edge-sentinel-research-edition | done |

## What is in progress (hardware-validated)

These need real ESP32 bench captures to be claimed in the paper:

- Real-data telemetry capture (1 hr normal + 5 fault scenarios, Steps 6-12 of
  the bench checklist).
- Energy-budget measurement on ESP32-S3 (sub-hypothesis H2).
- Cross-panel + cross-climate validation (sub-hypothesis H3).
- Hardware-in-the-loop latency measurement (target ≤ 50 ms).
- MATLAB cross-validation (Contribution 04).
- IEEE Access submission (target: Sep 2026).

See [`PROJECT_STATUS.md`](PROJECT_STATUS.md) and
[`docs/Edge_Sentinel_Bench_Checklist.pdf`](docs/Edge_Sentinel_Bench_Checklist.pdf)
for the full hardware milestone plan.

## Quick Start (reproduce in 3 commands)

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 2. Run the full pipeline
python scripts/run_demo_pipeline.py

# 3. Open the experiment report and figures
open reports/edge_sentinel_experiment_report.md
open reports/figures/accuracy_by_method.png
```

Optional: start the Streamlit dashboard

```bash
streamlit run dashboard/app.py
```

## Hardware Setup (when you are ready)

See these before connecting the ESP32 test setup:

- [`docs/circuit_diagram.md`](docs/circuit_diagram.md)
- [`docs/hardware_setup.md`](docs/hardware_setup.md)
- [`docs/experiment_protocol.md`](docs/experiment_protocol.md)
- [`docs/learning_research_materials.md`](docs/learning_research_materials.md)
- [`docs/Edge_Sentinel_Bench_Checklist.pdf`](docs/Edge_Sentinel_Bench_Checklist.pdf)
  — the 15-step plan to take the repo from software-complete to
  hardware-validated.

## Repository Layout

```text
backend/              MQTT ingestion, SQLite logging, CSV export
dashboard/            Streamlit real-time monitoring dashboard
data/raw/             Raw telemetry captures
data/processed/       Cleaned datasets for analytics and ML
docs/                 Research docs + bench checklist + learning roadmap
firmware/             ESP32 firmware for sensing and MQTT publishing
matlab_validation/    Solar-system simulation notes and scripts
ml/                   Detection models: rule-based, statistical, centroid,
                      classical (DT/RF/IF), calibration, audit explanations
reports/              Auto-regenerated experiment report + figures + CSVs
scripts/              One-command pipeline runner
tests/                pytest suite (14 tests)
tinyml/               Edge deployment: JSON model + C header
```

## Development Phases

1. **Monitoring System**: read voltage, current, temperature, publish
   telemetry, display dashboard.
2. **Data Collection**: store timestamped voltage, current, temperature, and
   power readings.
3. **Fault Injection**: capture normal operation, open circuit, partial
   shading, temperature anomaly, current deviation, and sensor failure.
4. **Analytics**: compare rule-based, statistical, and classical ML detection.
5. **Machine Learning**: train Decision Tree, Random Forest, and Isolation
   Forest models.
6. **TinyML**: convert and deploy the best model for ESP32 inference.
7. **MATLAB Validation**: compare hardware observations with simplified
   simulation results.
8. **Paper**: convert `reports/edge_sentinel_experiment_report.md` to IEEE
   Access template and submit to arXiv + IEEE.

## Initial Success Criteria

- Stable monitoring for at least 1 hour.
- Sensor updates every 2-5 seconds.
- Minimum dataset of 5,000 records (synthetic: 5,400 ✓).
- Target dataset of 10,000+ records (real captures, post-bench).
- Documented fault scenarios, metrics, and engineering justification.

## Portfolio Positioning

This project should be presented as:

> Edge Sentinel Research Edition: Intelligent Renewable Infrastructure
> Monitoring using Embedded Systems, TinyML, and Real-Time Fault Detection

It should not be reduced to a generic ESP32 solar-monitoring project. The
engineering value is in the complete monitoring, dataset, analytics,
edge-AI, calibration, audit-grade explanations, and research-validation
workflow.

## Citation

If you use this work in your own paper or project, please cite the IEEE
submission once it lands (target: Sep 2026). Until then, link to the
GitHub repo and the experiment report.
