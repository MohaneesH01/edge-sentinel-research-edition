# Hardware Setup

## Components

- ESP32 development board
- INA219 current and voltage sensor
- DHT22 temperature sensor
- Solar panel or controlled DC source
- Load resistor or adjustable DC load
- Breadboard, wiring, and safe power connections

## Suggested Wiring

| Module | Signal | ESP32 Pin |
| --- | --- | --- |
| INA219 | SDA | GPIO 21 |
| INA219 | SCL | GPIO 22 |
| INA219 | VCC | 3.3 V |
| INA219 | GND | GND |
| DHT22 | DATA | GPIO 4 |
| DHT22 | VCC | 3.3 V |
| DHT22 | GND | GND |

## Firmware Configuration

Copy:

```text
firmware/esp32_edge_sentinel/config.example.h
```

to:

```text
firmware/esp32_edge_sentinel/config.h
```

Then update WiFi and MQTT values.

## Safety Notes

- Start with a low-voltage bench setup before connecting a real panel.
- Confirm INA219 wiring polarity before collecting data.
- Avoid shorting the solar panel or power source directly.
- Use current-limited supplies when simulating faults.
