# Fault Scenarios

Fault scenarios should be controlled, repeatable, and documented with engineering justification.

## Class 0: Normal Operation

Expected behavior:

- Voltage remains within the normal operating band.
- Current follows load and irradiance conditions.
- Temperature changes slowly.

## Class 1: Open Circuit

Expected behavior:

- Current drops close to zero.
- Voltage may remain high depending on panel/source behavior.
- Power approaches zero.

## Class 2: Partial Shading Simulation

Expected behavior:

- Current decreases relative to the normal baseline.
- Voltage may decrease moderately.
- Power drops without a full shutdown.

## Class 3: Temperature Anomaly

Expected behavior:

- Temperature exceeds the configured anomaly threshold.
- Electrical behavior may remain normal initially.

## Class 4: Current Deviation

Expected behavior:

- Current rises or falls outside expected load behavior.
- Power deviates from the baseline even if voltage is stable.

## Class 5: Sensor Failure

Expected behavior:

- Missing readings, impossible values, frozen values, or abrupt discontinuities.

## Evidence Required

For every fault test:

- Record duration.
- Record sensor behavior.
- Capture dashboard screenshots.
- Store dataset entries.
- Add interpretation notes to experimental results.
