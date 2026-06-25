# Firmware ↔ Python alignment contract

This document is the single source of truth for the parity between the
on-device rule-based classifier and the off-device rule-based classifier.
Both must agree on every threshold and every rule-check order.

## Why this matters

If the on-device classifier and the off-device classifier give different
labels for the same readings, then v1 hardware validation will appear to
fail for reasons unrelated to the actual hardware. A reviewer would not
be able to tell whether a divergent reading was a sensor issue, a
firmware issue, or a Python bug.

## The contract

**Single source of truth:** the threshold constants in
`tests/test_firmware_thresholds.py`. If you change them, you must change
both the firmware and the Python module. The pytest enforces this.

**Mirror locations:**

- `tests/test_firmware_thresholds.py` — Python test that locks the values
- `ml/rule_based.py` — Python classifier (`classify_row`)
- `firmware/esp32_edge_sentinel/esp32_edge_sentinel.ino` — C++ classifier
  (`classifyFault`)

## Current threshold values (v1)

| Label | Condition |
|---|---|
| `sensor_failure` | `V < 0` OR `I < 0` OR `T < -20` |
| `open_circuit` | `V >= 8.0 AND I < 0.08` |
| `temperature_anomaly` | `T >= 45.0` |
| `partial_shading` | `V < 11.0 AND I < 0.45` |
| `current_deviation` | `I > 1.35` OR (`V >= 11.0 AND I < 0.25`) |
| `normal` | default (no rule fires) |

## Rule-check order

`tests/test_firmware_thresholds.py::FIRMWARE_ORDER` documents the order.
Both sides must check rules in this order:

```
1. sensor_failure   (first - physically invalid readings)
2. open_circuit
3. temperature_anomaly
4. partial_shading
5. current_deviation
6. normal           (default)
```

## CI enforcement

`tests/test_firmware_thresholds.py` is run as part of `pytest tests` in
CI. A divergence between the firmware and Python will not block the CI
yet (the firmware is not compiled in CI), but the test will fail if the
Python side is changed without updating the lock.

## v2 plan

When the real-data thresholds are recalibrated against the bench
captures, the entire table above gets updated, both files in lockstep,
and the pytest is updated to use the new values. The commit message
should explicitly say "recalibrate thresholds against real bench data."
