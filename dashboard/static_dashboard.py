"""Generate a dependency-light HTML dashboard from the latest dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data" / "processed" / "fault_dataset.csv"
OUTPUT = ROOT / "dashboard" / "edge_sentinel_dashboard.html"


def metric_card(label: str, value: str) -> str:
    return f'<section class="metric"><span>{label}</span><strong>{value}</strong></section>'


def sparkline(values: pd.Series, color: str) -> str:
    sample = values.tail(80).tolist()
    if not sample:
        return ""
    minimum = min(sample)
    maximum = max(sample)
    spread = maximum - minimum or 1.0
    points = []
    for index, value in enumerate(sample):
        x = index / max(1, len(sample) - 1) * 100
        y = 100 - ((value - minimum) / spread * 100)
        points.append(f"{x:.2f},{y:.2f}")
    return f'<svg viewBox="0 0 100 100" preserveAspectRatio="none"><polyline points="{" ".join(points)}" stroke="{color}" /></svg>'


def main() -> None:
    if not DATASET.exists():
        raise SystemExit("missing dataset: run python -m backend.generate_dataset first")

    frame = pd.read_csv(DATASET)
    latest = frame.iloc[-1]
    counts = frame["fault_label"].value_counts().reset_index()
    counts.columns = ["Fault", "Records"]
    recent = frame.tail(20).iloc[::-1]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Edge Sentinel Dashboard</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #5e6b74;
      --line: #d9e0e5;
      --panel: #ffffff;
      --bg: #f4f7f6;
      --accent: #0b7667;
      --warn: #b84a2a;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
    }}
    header {{
      padding: 28px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: #fff;
    }}
    h1 {{ margin: 0; font-size: 28px; letter-spacing: 0; }}
    .subtitle {{ margin-top: 6px; color: var(--muted); }}
    main {{ padding: 24px 32px 40px; max-width: 1280px; margin: 0 auto; }}
    .metrics {{ display: grid; grid-template-columns: repeat(4, minmax(140px, 1fr)); gap: 12px; }}
    .metric, .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .metric {{ padding: 16px; }}
    .metric span {{ display: block; color: var(--muted); font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 8px; font-size: 24px; }}
    .grid {{ display: grid; grid-template-columns: 1.15fr .85fr; gap: 16px; margin-top: 16px; }}
    .panel {{ padding: 18px; overflow: hidden; }}
    h2 {{ margin: 0 0 14px; font-size: 18px; }}
    svg {{ width: 100%; height: 170px; }}
    polyline {{ fill: none; stroke-width: 3; vector-effect: non-scaling-stroke; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
    th, td {{ padding: 10px 8px; border-bottom: 1px solid var(--line); text-align: left; }}
    th {{ color: var(--muted); font-weight: 600; }}
    .alert {{ color: var(--warn); font-weight: 700; }}
    @media (max-width: 820px) {{
      header, main {{ padding-left: 18px; padding-right: 18px; }}
      .metrics, .grid {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>Edge Sentinel Research Edition</h1>
    <div class="subtitle">Local renewable-infrastructure monitoring and fault-detection dashboard</div>
  </header>
  <main>
    <section class="metrics">
      {metric_card("Voltage", f"{latest['voltage']:.2f} V")}
      {metric_card("Current", f"{latest['current']:.2f} A")}
      {metric_card("Temperature", f"{latest['temperature']:.1f} C")}
      {metric_card("Power", f"{latest['power']:.2f} W")}
    </section>
    <section class="grid">
      <div class="panel">
        <h2>Recent Power Trend</h2>
        {sparkline(frame["power"], "#0b7667")}
      </div>
      <div class="panel">
        <h2>Current Fault State</h2>
        <p class="alert">{latest["fault_label"]}</p>
        <p>Records analyzed: {len(frame)}</p>
      </div>
    </section>
    <section class="grid">
      <div class="panel">
        <h2>Fault Distribution</h2>
        {counts.to_html(index=False)}
      </div>
      <div class="panel">
        <h2>Recent Readings</h2>
        {recent[["timestamp", "voltage", "current", "temperature", "power", "fault_label"]].to_html(index=False)}
      </div>
    </section>
  </main>
</body>
</html>
"""
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"generated {OUTPUT}")


if __name__ == "__main__":
    main()
