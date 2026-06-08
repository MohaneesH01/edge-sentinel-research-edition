# Project Status

Edge Sentinel Research Edition is currently in the **software prototype and hardware-ready preparation phase**.

## Completed

- Research-grade project scaffold
- ESP32 firmware skeleton for INA219, DHT22, WiFi, and MQTT telemetry
- SQLite telemetry logger
- CSV export workflow
- Synthetic fault-dataset generator
- Rule-based fault detection baseline
- Lightweight edge-feasible centroid classifier
- TinyML model JSON export
- ESP32 C header export for the lightweight model
- Static dashboard artifact
- Streamlit dashboard entry point
- Experiment report generation
- Engineering single-line diagram
- Hardware setup and experiment protocol documentation
- Handwritten notes guide for interview and research recall

## Current Software Baseline

Generated validation dataset:

- 5,400 records
- 6 classes
- 900 records per class

Current validation results:

| Method | Accuracy |
| --- | ---: |
| Rule-based detection | 91.33% |
| Lightweight centroid classifier | 80.96% |

## Next Hardware Milestones

1. Wire ESP32, INA219, and DHT22 using `docs/circuit_diagram.md`.
2. Configure WiFi and MQTT in `firmware/esp32_edge_sentinel/config.h`.
3. Upload firmware to ESP32.
4. Run live MQTT logger.
5. Collect 1 hour of normal telemetry.
6. Collect controlled fault-injection data.
7. Replace synthetic dataset with real hardware data.
8. Rerun analytics and update experimental results.

## Research Positioning

This project should be presented as:

**Edge Sentinel Research Edition: Intelligent Renewable Infrastructure Monitoring using Embedded Systems, TinyML, and Real-Time Fault Detection.**

It should not be reduced to a generic ESP32 monitoring project. The research value is in the complete pipeline: sensing, telemetry, dataset generation, fault analytics, edge inference, documentation, and validation.
