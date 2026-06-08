# TinyML Deployment Notes

This folder will contain the model-conversion workflow for ESP32 deployment.

Initial candidates:

- Decision Tree converted to C logic.
- Small Random Forest converted to generated C arrays.
- Quantized TensorFlow Lite Micro model if a neural model is added later.
- Dependency-light centroid classifier exported by `export_centroid_header.py`.

Evaluation requirements:

- Flash memory usage
- RAM usage
- Inference latency
- Classification accuracy
- Comparison against Python-side inference

## Current Export Path

Run:

```bash
python tinyml/export_centroid_header.py
```

This creates:

```text
tinyml/edge_sentinel_centroid_model.h
```

The header is a lightweight baseline for ESP32-side inference experiments.
