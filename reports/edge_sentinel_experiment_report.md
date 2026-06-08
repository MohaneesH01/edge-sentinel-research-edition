# Edge Sentinel Experiment Report

## Objective

Evaluate whether a low-cost ESP32-class renewable-energy monitoring system can detect solar fault conditions using local telemetry, deterministic analytics, and edge-feasible classification.

## Dataset Summary

Records: 5400

| fault_label         | records |
| ------------------- | ------- |
| normal              | 900     |
| open_circuit        | 900     |
| partial_shading     | 900     |
| temperature_anomaly | 900     |
| current_deviation   | 900     |
| sensor_failure      | 900     |

## Rule-Based Detection

| label               | precision | recall | f1     | support |
| ------------------- | --------- | ------ | ------ | ------- |
| current_deviation   | 0.9581    | 0.9626 | 0.9604 | 214     |
| normal              | 0.7188    | 1.0    | 0.8364 | 207     |
| open_circuit        | 0.9511    | 1.0    | 0.9749 | 214     |
| partial_shading     | 0.9276    | 0.9071 | 0.9172 | 226     |
| sensor_failure      | 1.0       | 0.7822 | 0.8778 | 225     |
| temperature_anomaly | 1.0       | 0.8523 | 0.9202 | 264     |
| accuracy            |           |        | 0.9133 | 1350    |

## Lightweight Edge Classifier

| label               | precision | recall | f1     | support |
| ------------------- | --------- | ------ | ------ | ------- |
| current_deviation   | 0.7244    | 0.528  | 0.6108 | 214     |
| normal              | 0.8913    | 0.7923 | 0.8389 | 207     |
| open_circuit        | 0.8295    | 1.0    | 0.9068 | 214     |
| partial_shading     | 0.6       | 0.9956 | 0.7488 | 226     |
| sensor_failure      | 1.0       | 0.5022 | 0.6686 | 225     |
| temperature_anomaly | 1.0       | 1.0    | 1.0    | 264     |
| accuracy            |           |        | 0.8096 | 1350    |

## Interpretation

The generated dataset provides a controlled development baseline for validating the software stack before physical fault-injection data is collected. Final research conclusions must be based on hardware readings from the ESP32, INA219, and DHT22 setup.

## Next Experimental Step

Replace or augment `data/processed/fault_dataset.csv` with hardware telemetry collected from controlled fault scenarios, then rerun:

```bash
python scripts/run_demo_pipeline.py
```
