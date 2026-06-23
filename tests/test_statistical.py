import pandas as pd

from ml.statistical import StatisticalBaseline, classify_frame


def _toy_frame():
    return pd.DataFrame(
        [
            {"voltage": 12.0, "current": 0.80, "temperature": 30.0, "power": 9.6,
             "fault_label": "normal"},
            {"voltage": 12.1, "current": 0.82, "temperature": 31.0, "power": 9.9,
             "fault_label": "normal"},
            {"voltage": 0.10, "current": 0.00, "temperature": 30.0, "power": 0.0,
             "fault_label": "open_circuit"},
            {"voltage": 0.12, "current": 0.00, "temperature": 30.0, "power": 0.0,
             "fault_label": "open_circuit"},
        ]
    )


def test_fit_and_predict_normal():
    frame = _toy_frame()
    baseline = StatisticalBaseline.fit(frame)
    preds = baseline.predict_frame(frame)
    assert preds.iloc[0]["prediction"] == "normal"
    assert preds.iloc[1]["prediction"] == "normal"


def test_fit_and_predict_open_circuit():
    frame = _toy_frame()
    baseline = StatisticalBaseline.fit(frame)
    preds = baseline.predict_frame(frame)
    assert preds.iloc[2]["prediction"] == "open_circuit"


def test_classify_frame_alias():
    frame = _toy_frame()
    preds = classify_frame(frame)
    assert set(preds) == {"normal", "open_circuit"}


def test_explain_row_returns_per_feature_z():
    frame = _toy_frame()
    baseline = StatisticalBaseline.fit(frame)
    explanation = baseline.explain_row(frame.iloc[0])
    assert "normal" in explanation
    assert "voltage" in explanation["normal"]
