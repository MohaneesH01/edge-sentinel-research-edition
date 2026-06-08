"""Streamlit dashboard for Edge Sentinel telemetry."""

from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "edge_sentinel.db"


def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        return pd.DataFrame(
            columns=["timestamp", "voltage", "current", "temperature", "power", "fault_label"]
        )
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM telemetry ORDER BY timestamp DESC LIMIT 1000", conn)


st.set_page_config(page_title="Edge Sentinel", page_icon="ES", layout="wide")
st.title("Edge Sentinel Research Edition")

data = load_data()

if data.empty:
    st.info("No telemetry yet. Run `python -m backend.logger --demo` or start the MQTT logger.")
    st.stop()

latest = data.iloc[0]
cols = st.columns(4)
cols[0].metric("Voltage", f"{latest['voltage']:.2f} V")
cols[1].metric("Current", f"{latest['current']:.2f} A")
cols[2].metric("Temperature", f"{latest['temperature']:.1f} C")
cols[3].metric("Power", f"{latest['power']:.2f} W")

chronological = data.sort_values("timestamp")

st.subheader("Live Telemetry")
st.line_chart(
    chronological.set_index("timestamp")[["voltage", "current", "temperature", "power"]],
    height=360,
)

st.subheader("Fault Class Distribution")
st.bar_chart(data["fault_label"].value_counts())

st.subheader("Recent Readings")
st.dataframe(data, use_container_width=True, hide_index=True)
