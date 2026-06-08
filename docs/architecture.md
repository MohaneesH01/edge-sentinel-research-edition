# Architecture

Edge Sentinel Research Edition is organized as a layered renewable-energy monitoring system.

## Hardware Layer

- ESP32 development board
- INA219 current and voltage sensor
- DHT22 temperature sensor
- Solar panel or controlled DC source
- Load element for controlled current draw

## Communication Layer

The ESP32 publishes telemetry over WiFi using MQTT.

Default topic:

```text
edge-sentinel/telemetry
```

Expected JSON payload:

```json
{
  "voltage": 12.1,
  "current": 0.84,
  "temperature": 31.5,
  "power": 10.16,
  "fault_class": 0,
  "fault_label": "normal"
}
```

## Data Layer

The backend stores telemetry in SQLite and can export records to CSV for analytics and model training.

## Analytics Layer

The first detection baselines are:

- Rule-based detection using engineering thresholds.
- Statistical detection using deviations from normal operating ranges.
- Classical ML models trained on fault-injection data.

## AI Layer

The TinyML phase should convert the best feasible model into an ESP32-deployable representation and evaluate:

- Flash usage
- RAM usage
- Inference latency
- Classification accuracy

## Visualization Layer

The Streamlit dashboard displays real-time telemetry, recent readings, and fault distribution.
