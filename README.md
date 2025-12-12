# 🚦 DataMart de Movilidad Urbana — Integración de Datos

Proyecto de integración de datos desarrollado para la asignatura **Arquitectura Tecnológica para Big Data**.

El sistema integra datos de movilidad urbana procedentes de **fuentes heterogéneas** mediante un pipeline orquestado con **Apache Airflow**, almacenando los resultados en un **DataMart en PostgreSQL**, todo desplegado con **Docker**.

---

## 📌 Objetivo del proyecto

Diseñar e implementar una arquitectura que permita:

- Integrar datos desde múltiples fuentes
- Orquestar procesos ETL
- Garantizar reproducibilidad e idempotencia
- Construir un modelo analítico orientado a consulta

---

## 🏗️ Arquitectura del sistema

El sistema se compone de:

- **Fuentes de datos heterogéneas**
- **Apache Airflow** como orquestador
- **PostgreSQL** como almacenamiento (RAW + DataMart)
- **Docker Compose** para el despliegue

📌 Ver diagrama en el informe. 

---

## 📥 Fuentes de datos integradas

| Fuente | Tipo | Tabla destino |
|-----|-----|-----|
| PostgreSQL | Relacional | trips_raw |
| CSV/XLSX | Ficheros locales | traffic_counts_raw |
| API REST (Open-Meteo) | Externa | weather_raw |
| XML local | Fichero estructurado | incidents_raw |

---

## 🧠 Orquestación con Apache Airflow

El pipeline principal está definido en el DAG: mobility_pipeline


### Tareas del DAG

1. `create_tables_dw` → creación idempotente de tablas
2. `extract_trips` → extracción desde PostgreSQL
3. `extract_traffic` → carga desde ficheros CSV/XLSX
4. `extract_weather` → consumo de API REST
5. `extract_incidents` → carga desde XML
6. `test_dummy` → verificación final

---

## 🗄️ Modelo de datos

### Tablas RAW / Staging

- trips_raw  
- traffic_counts_raw  
- weather_raw  
- incidents_raw  

### Modelo dimensional

- dim_date  
- dim_zone  
- dim_transport_mode  
- fact_mobility_daily  

---

## 🔁 Idempotencia

El sistema está diseñado para poder ejecutarse múltiples veces sin errores:

- Uso de `CREATE TABLE IF NOT EXISTS`
- Control de duplicados por clave natural
- Infraestructura reproducible con Docker

---

## 🚀 Despliegue del proyecto

### Requisitos
- Docker
- Docker Compose

### Pasos de ejecución

```bash
docker compose up -d


Acceder a Airflow:

http://localhost:8080

Usuario por defecto:

    Usuario: airflow
    Password: airflow

---

## 🔍 Consultas de verificación

```sql
SELECT * FROM trips_raw LIMIT 10;
SELECT * FROM traffic_counts_raw LIMIT 10;
SELECT * FROM weather_raw ORDER BY weather_id DESC LIMIT 5;
SELECT * FROM incidents_raw ORDER BY ts DESC;

 
---

## 📁 Estructura del proyecto

.
├── dags/
│   └── mobility_pipeline_dag.py
├── src/
│   ├── generate_trips.py
│   ├── generate_traffic.py
│   ├── generate_weather.py
│   └── generate_incidents.py
├── data/
│   ├── raw/
│   │   └── incidents.xml
│   └── processed/
├── sql/
│   └── create_tables_dw.sql
├── docker-compose.yml
├── README.md
└── diagrama_arquitectura_movilidad.png
