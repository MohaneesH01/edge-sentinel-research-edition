"""Telemetry logger for Edge Sentinel.

The logger can run in demo mode to seed the database before hardware is ready,
or it can subscribe to an MQTT topic once the ESP32 publisher is configured.
"""

from __future__ import annotations

import argparse
import json
import random
import sqlite3
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "edge_sentinel.db"
SCHEMA = ROOT / "backend" / "schema.sql"


@dataclass(frozen=True)
class TelemetryReading:
    timestamp: str
    voltage: float
    current: float
    temperature: float
    power: float
    fault_class: int = 0
    fault_label: str = "normal"

    @classmethod
    def from_payload(cls, payload: str) -> "TelemetryReading":
        data = json.loads(payload)
        voltage = float(data["voltage"])
        current = float(data["current"])
        temperature = float(data["temperature"])
        timestamp = data.get("timestamp") or utc_now()
        return cls(
            timestamp=timestamp,
            voltage=voltage,
            current=current,
            temperature=temperature,
            power=float(data.get("power", voltage * current)),
            fault_class=int(data.get("fault_class", 0)),
            fault_label=str(data.get("fault_label", "normal")),
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def connect(db_path: Path = DEFAULT_DB) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return conn


def insert_reading(conn: sqlite3.Connection, reading: TelemetryReading) -> None:
    conn.execute(
        """
        INSERT INTO telemetry (
            timestamp, voltage, current, temperature, power, fault_class, fault_label
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            reading.timestamp,
            reading.voltage,
            reading.current,
            reading.temperature,
            reading.power,
            reading.fault_class,
            reading.fault_label,
        ),
    )
    conn.commit()


def demo_readings(count: int) -> Iterable[TelemetryReading]:
    for index in range(count):
        voltage = random.normalvariate(12.0, 0.25)
        current = random.normalvariate(0.85, 0.06)
        temperature = random.normalvariate(31.0, 1.2)
        if index % 120 == 0 and index != 0:
            current *= 0.25
            fault_class = 2
            fault_label = "partial_shading"
        else:
            fault_class = 0
            fault_label = "normal"
        yield TelemetryReading(
            timestamp=utc_now(),
            voltage=round(voltage, 3),
            current=round(current, 3),
            temperature=round(temperature, 2),
            power=round(voltage * current, 3),
            fault_class=fault_class,
            fault_label=fault_label,
        )


def run_demo(db_path: Path, count: int, delay: float) -> None:
    conn = connect(db_path)
    try:
        for reading in demo_readings(count):
            insert_reading(conn, reading)
            print(f"logged {reading.timestamp} {reading.voltage}V {reading.current}A {reading.fault_label}")
            if delay:
                time.sleep(delay)
    finally:
        conn.close()


def run_mqtt(db_path: Path, host: str, topic: str) -> None:
    import paho.mqtt.client as mqtt

    conn = connect(db_path)

    def on_message(_client: mqtt.Client, _userdata: object, message: mqtt.MQTTMessage) -> None:
        try:
            reading = TelemetryReading.from_payload(message.payload.decode("utf-8"))
            insert_reading(conn, reading)
            print(f"logged {reading.timestamp} {reading.power}W {reading.fault_label}")
        except Exception as exc:
            print(f"ignored invalid payload: {exc}")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_message = on_message
    client.connect(host)
    client.subscribe(topic)
    print(f"listening on mqtt://{host}/{topic}")
    try:
        client.loop_forever()
    finally:
        conn.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Edge Sentinel telemetry logger")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--demo", action="store_true", help="generate synthetic demo readings")
    parser.add_argument("--count", type=int, default=200)
    parser.add_argument("--delay", type=float, default=0.0)
    parser.add_argument("--mqtt-host", default="localhost")
    parser.add_argument("--topic", default="edge-sentinel/telemetry")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.demo:
        run_demo(args.db, args.count, args.delay)
    else:
        run_mqtt(args.db, args.mqtt_host, args.topic)


if __name__ == "__main__":
    main()
