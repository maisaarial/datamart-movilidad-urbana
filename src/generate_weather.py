import requests
from datetime import date
from airflow.providers.postgres.hooks.postgres import PostgresHook


def generate_weather():
    """
    Llama a una API pública (Open-Meteo), guarda el JSON completo en raw_payload
    y además guarda campos normalizados en weather_raw.
    """

    # Bilbao aprox
    lat = 43.26
    lon = -2.93

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,precipitation,wind_speed_10m"
        "&timezone=auto"
    )

    print(f"Llamando a API de Open-Meteo: {url}")
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()

    data = resp.json()
    today = date.today().isoformat()

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    rains = hourly.get("precipitation", [])
    winds = hourly.get("wind_speed_10m", [])

    # Filtrar solo horas del día de hoy
    rows = []
    for t, temp, rain, wind in zip(times, temps, rains, winds):
        if str(t).startswith(today):
            rows.append((t, float(temp), float(rain), float(wind)))

    # Agregación diaria simple
    if rows:
        avg_temp = sum(r[1] for r in rows) / len(rows)
        total_rain = sum(r[2] for r in rows)
        avg_wind = sum(r[3] for r in rows) / len(rows)
    else:
        # fallback si la API no trae horas del día
        avg_temp, total_rain, avg_wind = None, None, None

    hook = PostgresHook(postgres_conn_id="mobility_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    print("Insertando datos en weather_raw...")

    # Evitar duplicados por día/zona:
    cur.execute('DELETE FROM weather_raw WHERE date = %s AND zone = %s', (today, "Ciudad"))

    cur.execute(
        """
        INSERT INTO weather_raw (
            date,
            zone,
            temp_avg_c,
            rain_mm,
            wind_speed_kmh,
            raw_payload
        )
        VALUES (%s, %s, %s, %s, %s, %s::jsonb)
        """,
        (
            today,
            "Ciudad",
            avg_temp,
            total_rain,
            avg_wind,
            resp.text,  # JSON completo como string
        ),
    )

    conn.commit()
    cur.close()
    conn.close()

    print("OK: Datos insertados en weather_raw desde API.")
