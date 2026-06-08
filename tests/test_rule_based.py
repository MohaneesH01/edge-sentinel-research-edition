import pandas as pd

from ml.rule_based import classify_frame, classify_row


def test_classifies_normal_reading():
    row = pd.Series({"voltage": 12.0, "current": 0.8, "temperature": 31.0})

    assert classify_row(row) == "normal"


def test_classifies_temperature_anomaly():
    row = pd.Series({"voltage": 12.0, "current": 0.8, "temperature": 46.0})

    assert classify_row(row) == "temperature_anomaly"


def test_classifies_frame():
    frame = pd.DataFrame(
        [
            {"voltage": 12.0, "current": 0.8, "temperature": 31.0},
            {"voltage": 12.4, "current": 0.01, "temperature": 31.0},
        ]
    )

    assert classify_frame(frame).tolist() == ["normal", "open_circuit"]
