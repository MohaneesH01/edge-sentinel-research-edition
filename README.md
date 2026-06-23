# Edge Sentinel Research Edition

**Edge Sentinel Research Edition** is an intelligent renewable-infrastructure monitoring prototype for detecting solar-system anomalies using embedded sensing, local analytics, and TinyML-ready edge inference.

The project is designed as a research-grade portfolio flagship: it combines electrical engineering, renewable-energy monitoring, ESP32 firmware, MQTT communication, local data logging, fault analytics, machine learning, and technical documentation.

## Research Question (v2)

> Can a sub-$50-volume BOM ESP32-class edge node, deployed at the panel level, run a quantized TFLite-Micro (int8) on-device classifier that detects and classifies the six fault modes — normal, open-circuit, partial shading, temperature anomaly, current deviation, sensor failure — of distributed rooftop PV under real-world conditions of irradiance variability, temperature drift, and sensor aging, achieving F1 ≥ 0.85 per class on a held-out test set of ≥ 1,500 labelled real-world samples with temperature-scaled calibrated confidence, while remaining energy-autonomous, fully offline, and demonstrably reproducible across panel brands and climates, and producing audit-grade explanations for every classification decision?

See [`docs/research_question.md`](docs/research_question.md) for the four sub-hypotheses and [`docs/threats_to_validity.md`](docs/threats_to_validity.md) for known limitations.

## System Goals

- Monitor voltage, current, temperature, and calculated power from a solar-energy test setup.
- Publish telemetry through MQTT over WiFi.
- Store structured readings locally for dataset generation.
- Detect faults using rule-based, statistical, and machine-learning methods.
- Compare detection approaches using accuracy, precision, recall, F1 score, false positives, and false negatives.
- Deploy the best feasible model to an ESP32-class edge device.
- Validate observed behavior against a simplified MATLAB solar-system simulation.

## Architecture

```text
ESP32 + Sensors
    |
    | MQTT telemetry
    v
Python backend
    |
    | SQLite + CSV export
    v
Analytics and ML pipeline
    |
    | model conversion
    v
TinyML edge inference
    |
    v
Streamlit dashboard and research reports
```

## Repository Layout

```text
backend/              MQTT ingestion, SQLite logging, CSV export
dashboard/            Streamlit real-time monitoring dashboard
data/raw/             Raw telemetry captures
data/processed/       Cleaned datasets for analytics and ML
docs/                 Research documentation and project notes
firmware/             ESP32 firmware for sensing and MQTT publishing
matlab_validation/    Solar-system simulation notes and scripts
ml/                   Classical ML training and evaluation
tests/                Python tests
tinyml/               Edge deployment and model-conversion notes
```

## Current Status (synthetic-data baseline)

| Method | Accuracy |
| --- | ---: |
| Rule-based detection | 0.9133 |
| Centroid (edge-feasible) | 0.8096 |
| Decision Tree | 0.9770 |
| Random Forest | 0.9800 |
| Isolation Forest (normal vs anomaly) | 0.9163 |

All five confusion matrices and the per-method bar chart are auto-rendered into `reports/figures/`. See [`reports/edge_sentinel_experiment_report.md`](reports/edge_sentinel_experiment_report.md) for the full report and [`PROJECT_STATUS.md`](PROJECT_STATUS.md) for the hardware-validated milestones.

## Development Phases

1. **Monitoring System**: read voltage, current, temperature, publish telemetry, display dashboard.
2. **Data Collection**: store timestamped voltage, current, temperature, and power readings.
3. **Fault Injection**: capture normal operation, open circuit, partial shading, temperature anomaly, current deviation, and sensor failure.
4. **Analytics**: compare rule-based and statistical detection.
5. **Machine Learning**: train Decision Tree, Random Forest, and Isolation Forest models.
6. **TinyML**: convert and deploy the best model for ESP32 inference.
7. **MATLAB Validation**: compare hardware observations with simplified simulation results.

## Initial Success Criteria

- Stable monitoring for at least 1 hour.
- Sensor updates every 2-5 seconds.
- Minimum dataset of 5,000 records.
- Target dataset of 10,000+ records.
- Documented fault scenarios, metrics, and engineering justification.

## Quick Start

Run the complete local research demo pipeline:

```bash
python scripts/run_demo_pipeline.py
```

This generates:

- `data/processed/fault_dataset.csv`
- `reports/edge_sentinel_experiment_report.md`
- `dashboard/edge_sentinel_dashboard.html`
- `tinyml/centroid_model.json`
- `tinyml/edge_sentinel_centroid_model.h`

For the optional MQTT and Streamlit workflow, create a local Python environment and install the requirements.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m backend.logger --demo
streamlit run dashboard/app.py
```

## Hardware Setup

See these before connecting the ESP32 test setup:

- `docs/circuit_diagram.md`
- `docs/hardware_setup.md`
- `docs/experiment_protocol.md`
- `docs/learning_research_materials.md`

## Portfolio Positioning

This project should be presented as:

> Edge Sentinel Research Edition: Intelligent Renewable Infrastructure Monitoring using Embedded Systems, TinyML, and Real-Time Fault Detection

It should not be reduced to a generic ESP32 solar-monitoring project. The engineering value is in the complete monitoring, dataset, analytics, edge-AI, and research-validation workflow.
