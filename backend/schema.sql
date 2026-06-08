CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    voltage REAL NOT NULL,
    current REAL NOT NULL,
    temperature REAL NOT NULL,
    power REAL NOT NULL,
    fault_class INTEGER DEFAULT 0,
    fault_label TEXT DEFAULT 'normal'
);

CREATE INDEX IF NOT EXISTS idx_telemetry_timestamp ON telemetry(timestamp);
CREATE INDEX IF NOT EXISTS idx_telemetry_fault_class ON telemetry(fault_class);
