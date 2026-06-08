# Edge Sentinel Handwritten Notes Guide

Use this file to make your own handwritten notebook for revision, interviews, and research discussions.

## 1. Project One-Line Summary

Write this first:

**Edge Sentinel Research Edition is a low-cost ESP32-based solar monitoring and fault-detection system that uses voltage, current, temperature sensing, MQTT communication, local analytics, and TinyML-ready edge inference.**

Short version to remember:

**ESP32 + sensors + MQTT + dataset + fault detection + TinyML.**

## 2. Main Research Question

Write:

**Can a low-cost ESP32-based monitoring system using TinyML detect practical solar faults without depending on cloud computation?**

Keywords:

- Low-cost
- Solar monitoring
- Fault detection
- Edge analytics
- TinyML
- No cloud dependency

## 3. Block Diagram To Redraw

Redraw this by hand:

```text
Solar/DC Source
      |
      v
INA219 Current + Voltage Sensor
      |
      v
Load

DHT22 Temperature Sensor
      |
      v
ESP32
      |
      v
MQTT Broker
      |
      v
Python Logger + SQLite
      |
      v
Dashboard + ML + Reports
```

Interview explanation:

> The power line goes through the INA219 so voltage and current can be measured. The ESP32 reads INA219 through I2C and DHT22 through a GPIO pin. It publishes telemetry using MQTT. Python stores the data, analyzes faults, and generates reports.

## 4. Circuit Notes

### ESP32 Pins

| Function | ESP32 Pin |
| --- | --- |
| I2C SDA | GPIO 21 |
| I2C SCL | GPIO 22 |
| DHT22 DATA | GPIO 4 |
| Sensor VCC | 3V3 |
| Sensor Ground | GND |

### INA219 Connection

Write in big letters:

**INA219 is connected in series with the positive supply line.**

Connection:

```text
Solar/DC + -> INA219 VIN+ -> INA219 VIN- -> Load + -> Load - -> Solar/DC -
```

Why?

Current must pass through the sensor to be measured.

### DHT22 Connection

```text
DHT22 VCC  -> ESP32 3V3
DHT22 GND  -> ESP32 GND
DHT22 DATA -> ESP32 GPIO4
```

Note:

Bare DHT22 may need a **4.7 kOhm to 10 kOhm pull-up resistor** between DATA and 3V3.

## 5. Important Electrical Concepts

### Voltage

Voltage is electrical potential difference.

Unit: **volt, V**

In this project:

Voltage tells whether the solar/DC source is healthy or dropping.

### Current

Current is flow of electric charge.

Unit: **ampere, A**

In this project:

Current tells whether the load is drawing power normally.

### Power

Formula:

```text
Power = Voltage x Current
P = V x I
```

Unit: **watt, W**

In this project:

Power shows actual energy delivery condition.

## 6. Sensors Used

### INA219

Purpose:

- Measures voltage
- Measures current
- Calculates power

Communication:

- I2C

Why chosen:

- Low cost
- Easy ESP32 interface
- Measures both voltage and current
- Useful for solar/load monitoring

Interview answer:

> I used INA219 because fault detection in solar systems needs both voltage and current. Measuring only voltage is not enough to detect current deviation, shading, or load-related faults.

### DHT22

Purpose:

- Measures temperature

Why temperature matters:

- Solar performance changes with temperature.
- High temperature can indicate abnormal operating condition.
- Temperature helps separate electrical faults from environmental effects.

Interview answer:

> DHT22 gives environmental temperature context. In PV systems, temperature affects output behavior, so it improves fault interpretation.

## 7. Communication Notes

### MQTT

MQTT is a lightweight publish-subscribe protocol for IoT systems.

Basic flow:

```text
ESP32 publishes telemetry
        |
        v
MQTT broker
        |
        v
Python backend subscribes
```

Topic:

```text
edge-sentinel/telemetry
```

Example payload:

```json
{
  "voltage": 12.1,
  "current": 0.84,
  "temperature": 31.5,
  "power": 10.16,
  "fault_label": "normal"
}
```

Why MQTT?

- Lightweight
- Good for IoT
- Works locally
- Supports real-time telemetry

Interview answer:

> MQTT was chosen because it is lightweight and suitable for low-power IoT devices. It allows the ESP32 to publish data without running a heavy server on the device.

## 8. Dataset Notes

Dataset columns:

```text
timestamp
voltage
current
temperature
power
fault_class
fault_label
```

Target:

- Minimum: 5,000 records
- Better target: 10,000+ records
- Sampling interval: 2-5 seconds

Why dataset is important:

- Needed for ML model training
- Needed for fault comparison
- Needed for research credibility
- Makes the project more than only hardware

## 9. Fault Classes

| Class | Fault | Expected Behavior |
| ---: | --- | --- |
| 0 | Normal | Stable voltage, current, power |
| 1 | Open circuit | Current nearly zero |
| 2 | Partial shading | Current and power drop |
| 3 | Temperature anomaly | Temperature unusually high |
| 4 | Current deviation | Current too high or too low |
| 5 | Sensor failure | Missing, impossible, or frozen values |

## 10. Fault Explanation Notes

### Normal Operation

Expected:

- Voltage around normal range
- Current depends on load
- Power stable
- Temperature slowly changing

### Open Circuit

Meaning:

The circuit path is broken, so current cannot flow.

Expected:

- Current close to zero
- Power close to zero
- Voltage may still be present

Interview answer:

> In an open circuit, current becomes almost zero because there is no complete path for current flow. Voltage may still appear at the source terminals.

### Partial Shading

Meaning:

Part of the solar panel receives less light.

Expected:

- Current drops
- Power drops
- Voltage may reduce slightly

Interview answer:

> Partial shading mainly reduces current because PV current is strongly related to irradiance.

### Temperature Anomaly

Meaning:

Temperature rises above safe or expected range.

Expected:

- Temperature high
- Electrical output may degrade

### Current Deviation

Meaning:

Current is not matching expected load behavior.

Expected:

- Current too high or too low
- Power abnormal

### Sensor Failure

Meaning:

Sensor gives impossible or missing readings.

Examples:

- Negative current when not expected
- Temperature = -99
- Frozen repeated values
- Missing MQTT payloads

## 11. Detection Methods

### Rule-Based Detection

Uses fixed engineering thresholds.

Example:

```text
if current is very low -> open circuit
if temperature is high -> temperature anomaly
```

Advantages:

- Simple
- Explainable
- Easy to deploy on ESP32

Limitations:

- Needs manual tuning
- May fail under changing conditions

### Statistical Detection

Uses deviation from normal behavior.

Examples:

- Mean
- Standard deviation
- Z-score
- Moving average

Good for:

- Detecting unusual behavior without exact fault rules

### Machine Learning Detection

Learns patterns from labeled data.

Models planned:

- Decision Tree
- Random Forest
- Isolation Forest
- Lightweight centroid classifier

Advantages:

- Can learn combined patterns
- Better for complex faults

Limitations:

- Needs good data
- Can overfit
- Must be tested carefully

## 12. TinyML Notes

TinyML means running machine-learning inference on a small embedded device.

In this project:

ESP32 should classify faults locally without cloud dependency.

Why useful:

- Faster response
- Works without internet
- Lower data transfer
- Better for remote solar systems

Metrics to measure:

- Accuracy
- Inference latency
- Flash usage
- RAM usage

Interview answer:

> TinyML is useful because the device can detect faults locally, reducing latency and avoiding dependency on cloud computation.

## 13. Evaluation Metrics

### Accuracy

```text
Accuracy = correct predictions / total predictions
```

### Precision

Out of predicted faults, how many were correct?

Good when false alarms are costly.

### Recall

Out of actual faults, how many were detected?

Good when missing faults is dangerous.

### F1 Score

Balance between precision and recall.

### False Positive

System says fault, but there is no fault.

### False Negative

System says normal, but there is actually a fault.

Important:

In fault detection, false negatives are often more serious.

## 14. Current Project Results

From synthetic validation dataset:

```text
Rule-based detection accuracy: 91.33%
Centroid model accuracy: 80.96%
```

Important interview note:

> These are software validation results on generated data. Final research results must be based on hardware-collected ESP32 data.

## 15. Research Positioning

Do not say:

**ESP32 solar monitoring project**

Say:

**Edge Sentinel Research Edition: Intelligent Renewable Infrastructure Monitoring using Embedded Systems, TinyML, and Real-Time Fault Detection.**

Research contribution:

- Low-cost monitoring
- Local fault detection
- Dataset generation
- Edge inference
- Comparison of rule-based and ML approaches
- Hardware plus simulation validation

## 16. Interview Questions and Answers

### Q1. What problem does your project solve?

It reduces fault-detection latency in small solar or distributed renewable-energy systems using low-cost embedded monitoring and local intelligence.

### Q2. Why ESP32?

ESP32 is low-cost, has WiFi, supports sensor interfaces like I2C and GPIO, and is suitable for edge monitoring prototypes.

### Q3. Why INA219?

It measures both voltage and current, which are necessary to calculate power and detect solar/load faults.

### Q4. Why not only cloud detection?

Cloud detection depends on internet connectivity and adds delay. Edge detection allows faster local response.

### Q5. What makes this research-oriented?

It includes dataset generation, controlled fault injection, model comparison, evaluation metrics, TinyML deployment, and documentation of experimental results.

### Q6. What is the biggest limitation?

The prototype must be validated with real hardware data under different environmental and load conditions before making strong claims.

### Q7. How will you improve it?

I would collect more real data, test under outdoor conditions, compare more ML models, improve calibration, and validate against simulation.

## 17. Formulas To Memorize

```text
P = V x I
```

```text
Accuracy = correct / total
```

```text
Precision = TP / (TP + FP)
```

```text
Recall = TP / (TP + FN)
```

```text
F1 = 2 x Precision x Recall / (Precision + Recall)
```

## 18. Diagrams To Practice Drawing

Draw these repeatedly:

1. System block diagram
2. INA219 series current-sensing path
3. MQTT publish-subscribe flow
4. Data pipeline from sensor to model
5. Fault classification workflow

## 19. Data Pipeline To Remember

```text
Sensors
  -> ESP32
  -> MQTT
  -> Python logger
  -> SQLite
  -> CSV
  -> Analytics
  -> ML model
  -> TinyML export
  -> Report
```

## 20. Final 60-Second Explanation

Practice saying this:

> My project, Edge Sentinel Research Edition, is a low-cost solar monitoring and fault-detection platform. It uses an ESP32 with an INA219 sensor for voltage and current and a DHT22 sensor for temperature. The ESP32 publishes telemetry using MQTT, and a Python backend logs the data into SQLite and CSV. The system detects faults such as open circuit, partial shading, temperature anomaly, current deviation, and sensor failure using rule-based analytics and machine-learning models. The final goal is to deploy fault classification on the ESP32 using TinyML so that solar faults can be detected locally without cloud dependency.

