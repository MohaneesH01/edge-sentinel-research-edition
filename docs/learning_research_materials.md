# Learning and Research Materials

Use this roadmap to understand the project deeply enough to explain it in interviews, reports, and research discussions.

For handwritten revision notes, use:

- `docs/handwritten_notes_guide.md`

## Learning Path

### 1. ESP32 and Embedded Systems

Learn:

- ESP32 GPIO basics
- I2C communication
- WiFi connection flow
- Arduino vs ESP-IDF
- Serial debugging
- Timing with `millis()`

Practice:

- Blink LED.
- Read DHT22 only.
- Read INA219 only.
- Print voltage/current/power to serial monitor.
- Then combine both sensors.

Key reference:

- Espressif ESP32-DevKitC documentation: https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html

### 2. Sensor Measurement

Learn:

- Difference between voltage, current, and power.
- Why current sensors must be placed in series.
- High-side current sensing.
- Sensor noise and calibration.
- Why bad grounding causes unstable readings.

Key references:

- Adafruit INA219 guide: https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/overview
- Adafruit DHT temperature/humidity guide: https://learn.adafruit.com/adafruit-io-basics-temperature-and-humidity/arduino-wiring

### 3. Renewable-Energy Monitoring

Learn:

- Solar panel I-V behavior.
- Open-circuit voltage.
- Short-circuit current.
- Effect of shading on current and power.
- Effect of temperature on PV performance.
- Why delayed fault detection reduces energy yield.

Practice:

- Plot voltage, current, and power under different loads.
- Compare normal operation against open-circuit behavior.
- Write notes for each fault scenario.

### 4. IoT and MQTT

Learn:

- MQTT publisher, broker, subscriber.
- Topic structure.
- JSON telemetry payloads.
- QoS levels.
- Local vs cloud data flow.

Practice:

- Publish test MQTT messages from ESP32.
- Subscribe from terminal or Python.
- Log MQTT payloads into SQLite.

Key reference:

- MQTT official site: https://mqtt.org/

### 5. Data Logging and Analytics

Learn:

- SQLite schema design.
- CSV export.
- Dataset labels.
- Train/test split.
- Confusion matrix.
- False positives and false negatives.

Practice:

- Collect 500 records.
- Export CSV.
- Plot power trends.
- Manually inspect fault labels.

### 6. Machine Learning and TinyML

Learn:

- Rule-based detection.
- Statistical thresholds.
- Decision Trees and Random Forests.
- Isolation Forest for anomaly detection.
- Model size, RAM use, flash use, inference latency.
- Why edge inference matters when cloud access is unavailable.

Practice:

- Train on synthetic data first.
- Replace synthetic data with real ESP32 data.
- Compare rule-based and ML metrics.
- Export a simple edge model to C.

Key reference:

- TensorFlow Lite Micro paper: https://arxiv.org/abs/2010.08678

### 7. MATLAB / Simulation Validation

Learn:

- Simple PV equivalent behavior.
- Load changes.
- Voltage drop.
- Fault-condition simulation.
- Difference between ideal simulation and noisy hardware.

Practice:

- Simulate voltage and current trends.
- Compare with hardware plots.
- Document why they differ.

## Research Papers and Technical Reading

Start with review papers first. They will give you vocabulary and help position your project.

1. **Photovoltaic system fault detection techniques: a review**
   - Open-access review of PV fault detection methods.
   - Link: https://link.springer.com/article/10.1007/s00521-023-09041-7

2. **Detection, classification, and localization of faults and failures in photovoltaic arrays**
   - Recent open-access review focused on fault detection, classification, and localization.
   - Link: https://link.springer.com/article/10.1007/s43937-026-00136-5

3. **Methods of photovoltaic fault detection and classification: A review**
   - Useful for comparing electrical, thermal, visual, and data-driven methods.
   - Link: https://www.sciencedirect.com/science/article/pii/S2352484722008022

4. **Machine learning in photovoltaic systems: A review**
   - Good for understanding where ML fits in PV forecasting, control, and fault diagnosis.
   - Link: https://www.sciencedirect.com/science/article/pii/S0960148122009454

5. **NREL PV reliability and performance research**
   - Good industry/research context for why reliability and long-term monitoring matter.
   - Link: https://www.nrel.gov/pv/reliability-engineering

6. **IEA PVPS Task 13 report on advanced algorithms in PV failure monitoring**
   - Useful for research positioning and real-world monitoring language.
   - Link: https://www.iea-pvps.org/wp-content/uploads/2021/10/Final-Report-IEA-PVPS-T13-19_2021_PV-Failure-Monitoring.pdf

## What You Should Be Able To Explain

After studying and building the hardware, you should be able to answer:

- Why did you choose ESP32?
- Why INA219 instead of only voltage measurement?
- Why use MQTT?
- What does open circuit look like electrically?
- Why does partial shading mainly reduce current?
- What is the difference between rule-based detection and ML detection?
- What is a false positive?
- What is a false negative?
- Why is TinyML useful here?
- What are the limits of your prototype?

## Suggested 14-Day Study Plan

| Day | Focus | Output |
| ---: | --- | --- |
| 1 | ESP32 basics | LED blink and serial monitor |
| 2 | DHT22 | Temperature readings |
| 3 | INA219 | Voltage/current/power readings |
| 4 | Combined sensors | Serial telemetry |
| 5 | MQTT | ESP32 publishes JSON |
| 6 | Python logger | SQLite records created |
| 7 | Dashboard | Live values visible |
| 8 | Normal dataset | 1-hour stable run |
| 9 | Open circuit and shading | Labeled fault records |
| 10 | Temperature/current faults | More labeled records |
| 11 | Rule analytics | Metrics and confusion matrix |
| 12 | ML model | Model trained on real data |
| 13 | TinyML export | ESP32-ready model header |
| 14 | Research write-up | Results and discussion updated |
