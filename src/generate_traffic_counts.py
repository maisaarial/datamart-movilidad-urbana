import random
from datetime import date
from airflow.providers.postgres.hooks.postgres import PostgresHook


def generate_traffic_counts():
    """
    Genera datos ficticios de aforos y los inserta en traffic_counts_raw.
    Usa la conexión 'mobility_postgres' de Airflow.
    """
    hook = PostgresHook(postgres_conn_id="mobility_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    zones = ["Centro", "Norte", "Sur", "Este", "Oeste"]
    today = date.today()

    print("Generando datos para traffic_counts_raw...")

    for zone in zones:
        vehicles = random.randint(300, 3000)
        bikes = random.randint(10, 200)
        pedestrians = random.randint(50, 1500)

        cur.execute(
            """
            INSERT INTO traffic_counts_raw (
                date, zone, vehicles_count, bikes_count, pedestrians_count
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (today, zone, vehicles, bikes, pedestrians),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en traffic_counts_raw.")