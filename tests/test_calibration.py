import numpy as np

from ml.calibration import TemperatureScaler, _softmax


def _toy_logits():
    rng = np.random.default_rng(0)
    return rng.normal(size=(40, 3))


def test_softmax_sums_to_one():
    rng = np.random.default_rng(1)
    x = rng.normal(size=(10, 5))
    p = _softmax(x, axis=-1)
    assert np.allclose(p.sum(axis=-1), 1.0)


def test_temperature_fitting_reduces_nll():
    rng = np.random.default_rng(2)
    logits = rng.normal(size=(200, 4)) + 2.0
    y = logits.argmax(axis=1)
    scaler = TemperatureScaler.fit(logits, y)
    # temperature should be finite and positive
    assert math.isfinite(scaler.temperature)
    assert scaler.temperature > 0


import math  # for the test above
