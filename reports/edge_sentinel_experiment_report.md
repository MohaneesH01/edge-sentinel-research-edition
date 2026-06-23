# Edge Sentinel Experiment Report

## Research question (v2)

> Can a sub-$50-volume BOM ESP32-class edge node, deployed at the panel
> level, run a quantized TFLite-Micro (int8) on-device classifier that detects
> and classifies the six fault modes — normal, open-circuit, partial shading,
> temperature anomaly, current deviation, sensor failure — of distributed
> rooftop PV under real-world conditions of irradiance variability, temperature
> drift, and sensor aging, achieving F1 ≥ 0.85 per class on a held-out test
> set of ≥ 1,500 labelled real-world samples with temperature-scaled
> calibrated confidence, while remaining energy-autonomous, fully offline,
> and demonstrably reproducible across panel brands and climates, and
> producing audit-grade explanations for every classification decision?

See `docs/research_question.md` for the four sub-hypotheses (H1-H4) and
`docs/threats_to_validity.md` for known limitations.

## Dataset summary

Records: 5400 (900 per class, balanced).

| fault_label         | records |
| ------------------- | ------- |
| normal              | 900     |
| open_circuit        | 900     |
| partial_shading     | 900     |
| temperature_anomaly | 900     |
| current_deviation   | 900     |
| sensor_failure      | 900     |

## Method comparison (synthetic data)

| Method | Accuracy |
| --- | ---: |
| Rule-based | 0.9133 |
| Centroid (edge-feasible) | 0.8096 |
| Decision Tree | 0.977 |
| Random Forest | 0.98 |
| Isolation Forest (normal vs anomaly) | 0.9163 |

## Per-method confusion matrices

The matrices below are auto-rendered from `reports/<method>_confusion_matrix.csv`
by `reports/plot_results.py` and live in `reports/figures/`.

- `figures/accuracy_by_method.png` — bar chart of all 5 methods
- `figures/rule_based_confusion_matrix.png`
- `figures/centroid_confusion_matrix.png`
- `figures/decision_tree_confusion_matrix.png`
- `figures/random_forest_confusion_matrix.png`
- `figures/isolation_forest_confusion_matrix.png`

## Per-method detailed metrics

### Rule-based detection

| label | precision | recall | f1 | support |
| --- | --- | --- | --- | --- |
| current_deviation | 0.9581 | 0.9626 | 0.9604 | 214 |
| normal | 0.7188 | 1.0 | 0.8364 | 207 |
| open_circuit | 0.9511 | 1.0 | 0.9749 | 214 |
| partial_shading | 0.9276 | 0.9071 | 0.9172 | 226 |
| sensor_failure | 1.0 | 0.7822 | 0.8778 | 225 |
| temperature_anomaly | 1.0 | 0.8523 | 0.9202 | 264 |
| accuracy |  |  | 0.9133 | 1350 |

### Centroid classifier (edge-feasible)

| label | precision | recall | f1 | support |
| --- | --- | --- | --- | --- |
| current_deviation | 0.7244 | 0.528 | 0.6108 | 214 |
| normal | 0.8913 | 0.7923 | 0.8389 | 207 |
| open_circuit | 0.8295 | 1.0 | 0.9068 | 214 |
| partial_shading | 0.6 | 0.9956 | 0.7488 | 226 |
| sensor_failure | 1.0 | 0.5022 | 0.6686 | 225 |
| temperature_anomaly | 1.0 | 1.0 | 1.0 | 264 |
| accuracy |  |  | 0.8096 | 1350 |

### Decision Tree

| label | precision | recall | f1 | support |
| --- | --- | --- | --- | --- |
| current_deviation | 0.9764 | 0.9673 | 0.9718 | 214 |
| normal | 0.9283 | 1.0 | 0.9628 | 207 |
| open_circuit | 0.9861 | 0.9953 | 0.9907 | 214 |
| partial_shading | 0.9779 | 0.9779 | 0.9779 | 226 |
| sensor_failure | 0.9952 | 0.92 | 0.9561 | 225 |
| temperature_anomaly | 0.9962 | 1.0 | 0.9981 | 264 |
| accuracy |  |  | 0.977 | 1350 |

### Random Forest

| label | precision | recall | f1 | support |
| --- | --- | --- | --- | --- |
| current_deviation | 0.9767 | 0.9813 | 0.979 | 214 |
| normal | 0.9283 | 1.0 | 0.9628 | 207 |
| open_circuit | 0.9953 | 0.9953 | 0.9953 | 214 |
| partial_shading | 0.9865 | 0.9735 | 0.98 | 226 |
| sensor_failure | 0.9952 | 0.9289 | 0.9609 | 225 |
| temperature_anomaly | 0.9962 | 1.0 | 0.9981 | 264 |
| accuracy |  |  | 0.98 | 1350 |

### Isolation Forest (normal vs anomaly)

| label | precision | recall | f1 | support |
| --- | --- | --- | --- | --- |
| anomaly | 0.9877 | 0.9125 | 0.9486 | 1143 |
| normal | 0.6599 | 0.9372 | 0.7745 | 207 |
| accuracy |  |  | 0.9163 | 1350 |

## Interpretation

The generated dataset provides a controlled development baseline for validating
the software stack before physical fault-injection data is collected. Final
research conclusions must be based on hardware readings from the ESP32, INA219,
and DHT22 setup.

**Synthetic-data headline:** Random Forest is the strongest multi-class
detector (98.0% accuracy), with Decision Tree close behind (97.7%). The
rule-based detector (91.3%) is competitive on the synthetic data but is
expected to degrade on real imbalanced data. The centroid classifier (81.0%)
is the on-device deployable option; it is the only model small enough to
fit the ESP32 RAM budget. Isolation Forest (91.6%) reframes the problem as
anomaly detection and is a useful complement for unknown-fault regimes.

**Real-data headline (planned):** the same pipeline must be re-run on
hardware captures from `docs/Edge_Sentinel_Bench_Checklist.pdf` (Steps 6-12)
before any deployment claim. See `docs/threats_to_validity.md`.

## Audit-grade explanation example

`ml/explain.py` emits one JSON line per reading. Example:

```json
{"prediction":"open_circuit","confidence":0.97,"rules_fired":["open_circuit_signature"],"feature_attribution":{"voltage":-4.21,"current":-3.98,"temperature":0.12,"power":-4.05},"drift_candidates":[]}
```

Every prediction in the deployed firmware should be paired with one of
these lines on Serial or MQTT, satisfying sub-hypothesis H4.

## Next experimental step

Replace `data/processed/fault_dataset.csv` with hardware telemetry and
rerun:

```bash
python scripts/run_demo_pipeline.py
```
