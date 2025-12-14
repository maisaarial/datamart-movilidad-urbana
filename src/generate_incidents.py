from airflow.providers.postgres.hooks.postgres import PostgresHook
import xml.etree.ElementTree as ET
from pathlib import Path


def generate_incidents(xml_path="/opt/airflow/data/raw/incidents.xml"):
    """
    Lee un XML local de incidencias y lo carga en incidents_raw.
    Guarda el XML completo en raw_payload (columna XML).
    """

    xml_file = Path(xml_path)
    if not xml_file.exists():
        raise FileNotFoundError(f"No existe el XML: {xml_path}")

    xml_text = xml_file.read_text(encoding="utf-8")
    root = ET.fromstring(xml_text)

    incidents = []
    for inc in root.findall("incident"):
        incident_id = (inc.findtext("incident_id") or "").strip()
        timestamp = (inc.findtext("timestamp") or "").strip()
        zone = (inc.findtext("zone") or "").strip()
        incident_type = (inc.findtext("type") or "").strip()
        severity = (inc.findtext("severity") or "").strip()
        description = (inc.findtext("description") or "").strip()

        # Validación mínima
        if not incident_id or not timestamp or not zone or not incident_type or not severity:
            continue

        incidents.append((incident_id, timestamp, zone, incident_type, severity, description))

    hook = PostgresHook(postgres_conn_id="mobility_postgres")
    conn = hook.get_conn()
    cur = conn.cursor()

    for incident_id, timestamp, zone, incident_type, severity, description in incidents:
        cur.execute(
            """
            INSERT INTO incidents_raw
              (incident_id, ts, zone, incident_type, severity, description, raw_payload)
            VALUES
              (%s, %s::timestamp, %s, %s, %s, %s, %s::xml)
            """,
            (incident_id, timestamp, zone, incident_type, severity, description, xml_text),
        )

    conn.commit()
    cur.close()
    conn.close()

    print(f"OK: Insertadas {len(incidents)} incidencias desde XML.")
