# Edge Sentinel Research Question (v2)

> **Sharper deployment-anchored version of the project research question.**

## Headline question

> *Can a sub-$50-volume BOM ESP32-class edge node, deployed at the panel
> level, run a quantized TFLite-Micro (int8) on-device classifier that detects
> and classifies the six fault modes — **normal, open-circuit, partial shading,
> temperature anomaly, current deviation, sensor failure** — of distributed
> rooftop PV under real-world conditions of irradiance variability, temperature
> drift, and sensor aging, achieving **F1 ≥ 0.85 per class** on a held-out test
> set of **≥ 1,500 labelled real-world samples** with temperature-scaled
> calibrated confidence, while remaining energy-autonomous, fully offline, and
> demonstrably reproducible across panel brands and climates, and producing
> **audit-grade explanations** (rule trace + feature attribution) for every
> classification decision?*

## Sub-hypotheses

The headline question decomposes into four sub-hypotheses. Each maps to a
section of the paper and to a commit in the repo.

### H1 — Detection quality under real-world conditions

**Claim:** An on-device classifier achieves F1 ≥ 0.85 per class on real
rooftop-PV telemetry with ≥ 1,500 held-out labelled samples.

**Test:** Replace the synthetic dataset with hardware captures from the bench
checklist (Steps 6-12), retrain, and re-evaluate on a held-out real-world test
set. Report per-class precision, recall, F1.

**Repo mapping:** `ml/train_classical.py`, `ml/train.py`, `reports/`.

### H2 — Resource budget on the edge

**Claim:** The chosen quantized model runs within 50 ms inference latency,
< 200 KB flash, < 50 KB peak RAM, and < 50 mJ per inference on the ESP32-S3.

**Test:** Deploy to ESP32-S3 with the centroid header for v1, then with the
quantized TFLite-Micro model for v2. Measure latency with `micros()` on the
chip; measure peak RAM with `esp_get_free_heap_size()` before/after; measure
energy with an INA219 on the ESP32 supply rail during a 1-minute inference
window.

**Repo mapping:** `tinyml/`, new `docs/energy_budget.md`.

### H3 — Reproducibility across panel brands and climates

**Claim:** The classifier, trained on panel A under climate X, achieves F1 ≥
0.75 per class on panel B under climate Y (i.e. graceful degradation, not
catastrophic failure) when paired with a defined cross-domain validation
protocol.

**Test:** Train on one panel's data, evaluate on another's. Document the
protocol in `docs/cross_domain_protocol.md`. Discuss limitations honestly in
the paper's Section 7.

**Repo mapping:** `data/cross_panel_validation.py`, new
`docs/cross_domain_protocol.md`.

### H4 — Audit-grade explanations

**Claim:** Every on-device classification is paired with (a) a rule trace
(which deterministic rules fired) and (b) a per-feature attribution (Z-score
contribution per feature), recoverable from the device's serial output or
memory dump.

**Test:** Implement `ml/explain.py` to emit, per prediction, a structured
JSON line: `{class, confidence, rules_fired, feature_attribution}`. Deploy on
ESP32-S3; confirm 1:1 mapping between predictions and explanations.

**Repo mapping:** `ml/explain.py`, `firmware/esp32_edge_sentinel/`.

## Why this version is sharper than v1

| Dimension | v1 (README) | v2 (this doc) |
| --- | --- | --- |
| Cost claim | "low-cost" (vague) | "sub-$50 BOM at 1k-unit scale" (falsifiable) |
| Model identity | "TinyML" (vague) | "quantized TFLite-Micro (int8)" (specific) |
| Fault list | not stated in question | listed inline (6 modes) |
| Performance bar | "practical" (vague) | "F1 ≥ 0.85 per class on ≥ 1,500 real samples" |
| Calibration | absent | temperature-scaled confidence |
| Cross-domain | absent | demonstrable reproducibility protocol |
| Explainability | absent | audit-grade per-decision explanation |
| Energy | implicit | explicit energy budget + offline-only |

## Out of scope (be honest about it in the paper)

- Multi-panel string-level diagnosis (single-panel only in v1).
- Cybersecurity / signed firmware (future work).
- Two-way actuation / remote disconnect (read-only sensor node).
- Wireless protocols other than WiFi (LoRa / GSM in future work).
