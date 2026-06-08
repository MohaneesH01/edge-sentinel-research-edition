# Dataset Description

The Edge Sentinel dataset records solar-monitoring telemetry and associated fault labels.

## Schema

| Column | Type | Description |
| --- | --- | --- |
| `timestamp` | ISO-8601 string | Time when the reading was collected |
| `voltage` | float | Measured bus or panel voltage in volts |
| `current` | float | Measured current in amperes |
| `temperature` | float | Ambient or nearby module temperature in Celsius |
| `power` | float | Calculated power in watts |
| `fault_class` | integer | Numeric fault class |
| `fault_label` | string | Human-readable fault label |

## Dataset Targets

- Minimum dataset: 5,000 records
- Target dataset: 10,000+ records
- Sensor update interval: 2-5 seconds

## Collection Notes

Each fault-injection session should include:

- Start and end timestamp
- Physical setup notes
- Fault class
- Expected behavior
- Observed voltage/current/temperature pattern
- Dashboard screenshot
- Any sensor instability or recovery delay
