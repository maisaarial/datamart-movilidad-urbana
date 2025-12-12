from datetime import datetime, date
import random

import sys
sys.path.append("/opt/airflow/src")

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

from generate_traffic_counts import generate_traffic_counts
from generate_weather import generate_weather
from generate_incidents import generate_incidents

def generate_trips():
    hook = PostgresHook(postgres_conn_id="mobility_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    zones = ["Centro", "Norte", "Sur", "Este", "Oeste"]
    modes = ["coche", "bus", "bici", "moto", "a_pie"]
    today = date.today()

    print("Generando datos para trips_raw...")

    for _ in range(20):
        cur.execute(
            """
            INSERT INTO trips_raw (
                trip_date,
                trip_start_time,
                origin_zone,
                dest_zone,
                transport_mode,
                distance_km,
                duration_min
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                today,
                f"{random.randint(0, 23):02d}:00:00",
                random.choice(zones),
                random.choice(zones),
                random.choice(modes),
                round(random.uniform(0.5, 15.0), 2),
                random.randint(5, 60),
            ),
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Datos insertados en trips_raw.")


def dummy_task():
    print("Pipeline de movilidad ejecutada correctamente.")


with DAG(
    dag_id="mobility_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["movilidad"],
    template_searchpath="/opt/airflow/sql",
):

    create_tables_dw = PostgresOperator(
        task_id="create_tables_dw",
        postgres_conn_id="mobility_postgres",
        sql="create_tables_dw.sql",
    )

    extract_trips = PythonOperator(
        task_id="extract_trips",
        python_callable=generate_trips,
    )

    extract_traffic = PythonOperator(
        task_id="extract_traffic",
        python_callable=generate_traffic_counts,
    )

    extract_weather = PythonOperator(
        task_id="extract_weather",
        python_callable=generate_weather,
    )

    extract_incidents = PythonOperator(
        task_id="extract_incidents",
        python_callable=generate_incidents,
    )

    test_dummy = PythonOperator(
        task_id="test_dummy",
        python_callable=dummy_task,
    )


    create_tables_dw >> extract_trips >> extract_traffic >> extract_weather >> extract_incidents >> test_dummy
