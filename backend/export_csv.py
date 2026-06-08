"""Export telemetry from SQLite to CSV."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "edge_sentinel.db"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "telemetry_export.csv"


def export_csv(db_path: Path = DEFAULT_DB, output_path: Path = DEFAULT_OUTPUT) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        frame = pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp", conn)
    frame.to_csv(output_path, index=False)
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Export Edge Sentinel telemetry to CSV")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    path = export_csv(args.db, args.output)
    print(f"exported {path}")


if __name__ == "__main__":
    main()
