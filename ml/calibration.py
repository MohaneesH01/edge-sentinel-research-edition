"""Temperature-scaled calibration for Edge Sentinel classifiers.

Calibration turns raw model scores (e.g. centroid distances, tree
probabilities) into probabilities that reflect empirical accuracy. A
well-calibrated classifier that says "0.85" should be correct ~85% of the
time.

Reference: Guo et al., "On Calibration of Modern Neural Networks," ICML 2017.

Usage:

    from ml.calibration import TemperatureScaler
    scaler = TemperatureScaler.fit(val_probs, val_true_one_hot)
    test_probs_calibrated = scaler.transform(test_probs)
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass
class TemperatureScaler:
    temperature: float
    n_classes: int

    @classmethod
    def fit(cls, logits: np.ndarray, y_true: np.ndarray,
            max_iter: int = 200) -> "TemperatureScaler":
        """Find a single scalar temperature that minimises NLL on a validation
        set. ``logits`` shape (N, C), ``y_true`` shape (N,) of integer labels.
        """
        if logits.ndim != 2:
            raise ValueError("logits must be 2D (N, C)")
        n, c = logits.shape
        temperature = 1.0
        best_nll = _nll(logits / temperature, y_true)
        best_t = temperature
        # Grid search + a few Newton steps. Cheap because temperature is 1-D.
        for t in np.linspace(0.5, 3.0, 26):
            nll = _nll(logits / t, y_true)
            if nll < best_nll:
                best_nll = nll
                best_t = float(t)
        # Fine-tune around the best grid point.
        for _ in range(max_iter):
            grad = _nll_grad(logits / best_t, y_true) / best_t ** 2
            step = -grad * 0.1
            new_t = max(0.05, best_t + step)
            nll = _nll(logits / new_t, y_true)
            if nll < best_nll:
                best_nll = nll
                best_t = float(new_t)
            else:
                break
        return cls(temperature=best_t, n_classes=c)

    def transform(self, logits: np.ndarray) -> np.ndarray:
        scaled = logits / self.temperature
        return _softmax(scaled, axis=-1)


def _softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    x = x - x.max(axis=axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=axis, keepdims=True)


def _nll(logits: np.ndarray, y_true: np.ndarray) -> float:
    probs = _softmax(logits, axis=-1)
    p = probs[np.arange(len(y_true)), y_true]
    p = np.clip(p, 1e-12, 1.0)
    return float(-np.mean(np.log(p)))


def _nll_grad(logits: np.ndarray, y_true: np.ndarray) -> float:
    probs = _softmax(logits, axis=-1)
    p_true = probs[np.arange(len(y_true)), y_true]
    # gradient of NLL w.r.t. (logits / T), summed over N
    return float(-np.mean((1.0 / np.clip(p_true, 1e-12, 1.0)) *
                         (probs[np.arange(len(y_true)), y_true] - 1)))
