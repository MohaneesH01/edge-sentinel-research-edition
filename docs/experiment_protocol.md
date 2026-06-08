# Experiment Protocol

## Objective

Collect repeatable telemetry for normal and faulted solar-system behavior.

## Pre-Test Checklist

- ESP32 is publishing MQTT telemetry.
- Backend logger is running.
- Dashboard shows live voltage, current, temperature, and power.
- SQLite database path is confirmed.
- Physical setup photo is captured.

## Baseline Run

1. Run normal operation for at least 1 hour.
2. Confirm update interval is 2-5 seconds.
3. Export CSV.
4. Record environment conditions and load configuration.

## Fault-Injection Runs

For each class:

1. Start backend logger.
2. Apply the controlled fault.
3. Record start and end time.
4. Capture dashboard screenshot.
5. Export CSV.
6. Add observations to `docs/experimental_results.md`.

## Required Fault Classes

| Class | Label | Minimum Duration |
| ---: | --- | ---: |
| 0 | normal | 60 minutes |
| 1 | open_circuit | 5 minutes |
| 2 | partial_shading | 5 minutes |
| 3 | temperature_anomaly | 5 minutes |
| 4 | current_deviation | 5 minutes |
| 5 | sensor_failure | 5 minutes |

## Data Quality Rules

- Do not mix unlabeled fault classes in one run.
- Keep notes for any wiring change.
- Mark unstable or uncertain records instead of deleting them silently.
- Preserve raw data before cleaning.
