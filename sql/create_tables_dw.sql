-- =========================
-- TABLAS RAW / STAGING (idempotente)
-- =========================

CREATE TABLE IF NOT EXISTS trips_raw (
    trip_id SERIAL PRIMARY KEY,
    trip_date DATE NOT NULL,
    trip_start_time TIME NOT NULL,
    origin_zone VARCHAR(100) NOT NULL,
    dest_zone VARCHAR(100) NOT NULL,
    transport_mode VARCHAR(50) NOT NULL,
    distance_km NUMERIC(6,2) NOT NULL,
    duration_min INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS traffic_counts_raw (
    traffic_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    zone VARCHAR(100) NOT NULL,
    vehicles_count INTEGER NOT NULL,
    bikes_count INTEGER NOT NULL,
    pedestrians_count INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS weather_raw (
    weather_id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    zone VARCHAR(100) NOT NULL,
    temp_avg_c NUMERIC(4,1),
    rain_mm NUMERIC(6,2),
    wind_speed_kmh NUMERIC(6,2),
    raw_payload JSONB NOT NULL
);

-- incidents_raw: lo creamos de forma “segura” (evita errores raros con XML)
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'incidents_raw'
  ) THEN
    CREATE TABLE incidents_raw (
      id SERIAL PRIMARY KEY,
      incident_id TEXT NOT NULL,
      ts TIMESTAMP NOT NULL,
      zone TEXT NOT NULL,
      incident_type TEXT NOT NULL,
      severity TEXT NOT NULL,
      description TEXT,
      raw_payload XML NOT NULL
    );
  END IF;
END $$;
