import random
from datetime import datetime, timedelta
import psycopg2

def generate_trips():
    # Conexión a la base de datos mobility-db
    conn = psycopg2.connect(
        host="mobility-db",
        database="mobility",
        user="mobility",
        password="mobility"
    )
    cur = conn.cursor()

    zones = ["Centro", "Norte", "Sur", "Este", "Oeste"]
    modes = ["coche", "bus", "bici", "moto", "a_pie"]

    today = datetime.today().date()

    print("Generando datos para trips_raw...")

    for i in range(20):  # INSERTA 20 VIAJES
        origin = random.choice(zones)
        dest = random.choice(zones)
        mode = random.choice(modes)
        distance = round(random.uniform(0.5, 15.0), 2)
        duration = random.randint(5, 60)
        hour = random.randint(0, 23)

        cur.execute("""
            INSERT INTO trips_raw (trip_date, trip_start_time, origin_zone, dest_zone, transport_mode, distance_km, duration_min)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            today,
            f"{hour}:00:00",
            origin,
            dest,
            mode,
            distance,
            duration
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en trips_raw.")