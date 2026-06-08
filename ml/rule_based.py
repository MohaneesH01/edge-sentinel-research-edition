"""Rule-based and statistical fault detection baselines."""

from __future__ import annotations

import pandas as pd


def classify_row(row: pd.Series) -> str:
    voltage = float(row["voltage"])
    current = float(row["current"])
    temperature = float(row["temperature"])

    if voltage < 0 or current < 0 or temperature < -20:
        return "sensor_failure"
    if voltage >= 8.0 and current < 0.08:
        return "open_circuit"
    if temperature >= 45.0:
        return "temperature_anomaly"
    if voltage < 11.0 and current < 0.45:
        return "partial_shading"
    if current > 1.35 or (voltage >= 11.0 and current < 0.25):
        return "current_deviation"
    return "normal"


def classify_frame(frame: pd.DataFrame) -> pd.Series:
    return frame.apply(classify_row, axis=1)
