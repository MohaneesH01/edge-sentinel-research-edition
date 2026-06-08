"""Generate a controlled Edge Sentinel fault-injection dataset."""

from __future__ import annotations

import argparse
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "fault_dataset.csv"

FAULTS = {
    0: "normal",
    1: "open_circuit",
    2: "partial_shading",
    3: "temperature_anomaly",
    4: "current_deviation",
    5: "sensor_failure",
}


def bounded(value: float, minimum: float = 0.0) -> float:
    return max(minimum, value)


def make_reading(fault_class: int, timestamp: datetime) -> dict[str, object]:
    if fault_class == 0:
        voltage = random.normalvariate(12.0, 0.25)
        current = random.normalvariate(0.85, 0.07)
        temperature = random.normalvariate(31.0, 1.2)
    elif fault_class == 1:
        voltage = random.normalvariate(12.4, 0.2)
        current = random.normalvariate(0.02, 0.01)
        temperature = random.normalvariate(31.0, 1.0)
    elif fault_class == 2:
        voltage = random.normalvariate(10.4, 0.45)
        current = random.normalvariate(0.28, 0.06)
        temperature = random.normalvariate(32.0, 1.4)
    elif fault_class == 3:
        voltage = random.normalvariate(11.7, 0.35)
        current = random.normalvariate(0.76, 0.08)
        temperature = random.normalvariate(48.0, 2.8)
    elif fault_class == 4:
        voltage = random.normalvariate(11.8, 0.35)
        current = random.choice([
            random.normalvariate(0.18, 0.04),
            random.normalvariate(1.65, 0.12),
        ])
        temperature = random.normalvariate(33.0, 1.8)
    else:
        voltage = random.choice([-1.0, 0.0, random.normalvariate(12.0, 0.1)])
        current = random.choice([-1.0, 0.0, random.normalvariate(0.85, 0.03)])
        temperature = random.choice([-99.0, random.normalvariate(31.0, 0.4)])

    voltage = round(voltage if fault_class == 5 else bounded(voltage), 3)
    current = round(current if fault_class == 5 else bounded(current), 3)
    temperature = round(temperature, 2)
    power = round(voltage * current, 3)

    return {
        "timestamp": timestamp.isoformat(timespec="seconds"),
        "voltage": voltage,
        "current": current,
        "temperature": temperature,
        "power": power,
        "fault_class": fault_class,
        "fault_label": FAULTS[fault_class],
    }


def generate_dataset(records_per_class: int, output: Path, seed: int) -> Path:
    random.seed(seed)
    output.parent.mkdir(parents=True, exist_ok=True)
    start = datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc)
    rows = []
    index = 0
    for fault_class in FAULTS:
        for _ in range(records_per_class):
            rows.append(make_reading(fault_class, start + timedelta(seconds=3 * index)))
            index += 1
    frame = pd.DataFrame(rows)
    frame.to_csv(output, index=False)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Edge Sentinel fault dataset")
    parser.add_argument("--records-per-class", type=int, default=900)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    path = generate_dataset(args.records_per_class, args.output, args.seed)
    print(f"generated {path}")


if __name__ == "__main__":
    main()
