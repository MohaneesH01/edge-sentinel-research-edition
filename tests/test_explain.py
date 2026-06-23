import json

import pandas as pd

from ml.explain import (
    AuditExplanation,
    explain_frame,
    explain_row,
    fit_class_stats,
    _rules_fired,
)


def _toy_frame():
    return pd.DataFrame(
        [
            {"voltage": 12.0, "current": 0.80, "temperature": 30.0, "power": 9.6,
             "fault_label": "normal"},
            {"voltage": 12.1, "current": 0.82, "temperature": 31.0, "power": 9.9,
             "fault_label": "normal"},
            {"voltage": 0.10, "current": 0.00, "temperature": 30.0, "power": 0.0,
             "fault_label": "open_circuit"},
        ]
    )


def test_rules_fired_default():
    row = pd.Series({"voltage": 12.0, "current": 0.8, "temperature": 30.0})
    assert _rules_fired(row) == ["default_normal"]


def test_rules_fired_open_circuit():
    row = pd.Series({"voltage": 12.0, "current": 0.01, "temperature": 30.0})
    assert "open_circuit_signature" in _rules_fired(row)


def test_fit_class_stats_shape():
    stats = fit_class_stats(_toy_frame())
    assert "normal" in stats
    assert "voltage" in stats["normal"]


def test_explain_row_emits_json():
    frame = _toy_frame()
    stats = fit_class_stats(frame)
    explanation = explain_row(frame.iloc[0], stats)
    assert isinstance(explanation, AuditExplanation)
    parsed = json.loads(explanation.to_json())
    assert parsed["prediction"] in {"normal", "open_circuit"}
    assert "rules_fired" in parsed
    assert "feature_attribution" in parsed


def test_explain_frame_returns_one_line_per_row():
    frame = _toy_frame()
    lines = explain_frame(frame)
    assert len(lines) == len(frame)
    assert all(json.loads(line) for line in lines)
