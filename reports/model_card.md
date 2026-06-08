# Edge Sentinel Baseline Model Card

## Model

Centroid classifier trained on voltage, current, temperature, and power.

## Purpose

This dependency-light model is included as an edge-feasibility baseline. It is not the final research model, but it provides a simple deployable classifier while Decision Tree, Random Forest, and Isolation Forest experiments are added in environments with scikit-learn.

## Dataset

`/Users/mohaneeshsinghmanral/Documents/Edge Sentinel Research Edition/data/processed/fault_dataset.csv`

## Validation Accuracy

0.8096

## Deployment Notes

The exported JSON model in `tinyml/centroid_model.json` can be converted to C arrays or used as a reference for ESP32-side distance-based inference.
