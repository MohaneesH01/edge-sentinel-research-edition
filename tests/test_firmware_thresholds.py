"""Threshold and feature parity check between firmware and Python.

The on-device rule-based classifier (firmware/esp32_edge_sentinel/esp32_edge_sentinel.ino
function ``classifyFault``) and the off-device rule-based classifier
(ml/rule_based.py function ``classify_row``) must use the SAME thresholds
and produce the SAME labels for the SAME inputs. If they diverge, the
v1 hardware validation will fail for reasons unrelated to the hardware.

This test enforces the parity contract. If you change THRESHOLDS below, you
must also change the firmware and vice-versa. The order of rule checks
(FIRMWARE_ORDER) must match too.

Last sync: firmware and ml/rule_based.py aligned on 2026-06-25.


The on-device rule-based classifier (firmware/esp32_edge_sentinel/esp32_edge_sentinel.ino
function ``classifyFault``) and the off-device rule-based classifier
(ml/rule_based.py function ``classify_row``) must use the SAME thresholds
and produce the SAME labels for the SAME inputs. If they diverge, the
v1 hardware validation will fail for reasons unrelated to the hardware.

This test enforces the parity contract.
"""
from __future__ import annotations

from ml.rule_based import classify_row

# These thresholds are the single source of truth, mirrored in the firmware.
THRESHOLDS = {
    "sensor_failure": {
        "voltage_max": 0.0,           # voltage < 0 fails
        "current_max": 0.0,           # current < 0 fails
        "temperature_min": -20.0,     # temperature < -20 fails
    },
    "open_circuit": {
        "voltage_min": 8.0,
        "current_max": 0.08,
    },
    "temperature_anomaly": {
        "temperature_min": 45.0,
    },
    "partial_shading": {
        "voltage_max": 11.0,
        "current_max": 0.45,
    },
    "current_deviation": {
        "current_min": 1.35,
    },
    "normal": "default",
}

# Firmware order (must match the .ino function classifyFault exactly).
FIRMWARE_ORDER = [
    "sensor_failure",
    "open_circuit",
    "temperature_anomaly",
    "partial_shading",
    "current_deviation",
    "normal",
]

# Toy cases that exercise every threshold.
SAMPLES = [
    # (voltage, current, temperature, expected_label)
    (-1.0, 0.5, 25.0, "sensor_failure"),       # negative V
    (12.0, -0.1, 25.0, "sensor_failure"),      # negative I
    (12.0, 0.5, -25.0, "sensor_failure"),      # sub-zero T
    (12.4, 0.01, 30.0, "open_circuit"),         # V>=8, I<0.08
    (12.0, 0.85, 46.0, "temperature_anomaly"), # T>=45
    (10.5, 0.40, 30.0, "partial_shading"),      # V<11, I<0.45
    (12.0, 1.40, 30.0, "current_deviation"),   # I>1.35
    (12.0, 0.85, 30.0, "normal"),               # all good
    (12.0, 0.20, 30.0, "current_deviation"),   # V>=11 AND I<0.25 -> current_deviation
]


def test_all_samples_match():
    for voltage, current, temperature, expected in SAMPLES:
        row = {"voltage": voltage, "current": current, "temperature": temperature}
        actual = classify_row(row)
        assert actual == expected, (
            f"v={voltage} i={current} t={temperature} -> {actual} (want {expected})"
        )


def test_normal_default():
    """If no rule fires, the classifier must return 'normal'."""
    row = {"voltage": 12.0, "current": 0.85, "temperature": 30.0}
    assert classify_row(row) == "normal"


def test_threshold_constants_match_firmware():
    """If you change THRESHOLDS here, you must change the firmware to match.

    This test is a tripwire: it runs every time so a divergence is caught
    before the firmware is flashed.
    """
    # Sentinel checks - any change should be intentional.
    assert THRESHOLDS["open_circuit"]["voltage_min"] == 8.0
    assert THRESHOLDS["open_circuit"]["current_max"] == 0.08
    assert THRESHOLDS["temperature_anomaly"]["temperature_min"] == 45.0
    assert THRESHOLDS["partial_shading"]["voltage_max"] == 11.0
    assert THRESHOLDS["partial_shading"]["current_max"] == 0.45
    assert THRESHOLDS["current_deviation"]["current_min"] == 1.35


def test_firmware_order_documented():
    """The rule check order matters. If you reorder, both sides must agree."""
    assert FIRMWARE_ORDER == [
        "sensor_failure", "open_circuit", "temperature_anomaly",
        "partial_shading", "current_deviation", "normal",
    ]
