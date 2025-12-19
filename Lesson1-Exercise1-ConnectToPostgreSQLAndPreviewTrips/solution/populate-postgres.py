import time
import psycopg2
import os

MAX_RETRIES = 15
WAIT_SECONDS = 2

PG_HOST = "localhost"
PG_PORT = 5432
PG_DB   = "postgres"
PG_USER = "temp"
PG_PASS = "temp"

TRIPS_CSV_PATH = "./data/van_transit_trips_postgres.csv"  # fixed path

def wait_for_postgres():
    for i in range(MAX_RETRIES):
        try:
            conn = psycopg2.connect(
                host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS
            )
            conn.close()
            print("Postgres is up!")
            return
        except psycopg2.OperationalError:
            print(f"Waiting for Postgres... ({i+1}/{MAX_RETRIES})")
            time.sleep(WAIT_SECONDS)
    raise RuntimeError("Could not connect to Postgres after retries.")

def populate_postgres_trips():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(
        host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS
    )
    cur = conn.cursor()

    # Drop and recreate raw_trips
    ddl = """
    DROP TABLE IF EXISTS public.raw_trips;
    CREATE TABLE public.raw_trips (
      trip_id               TEXT,
      rider_id              TEXT,
      route_id              TEXT,
      mode                  TEXT,
      origin_station_id     TEXT,
      destination_station_id TEXT,
      board_datetime        TIMESTAMP,
      alight_datetime       TIMESTAMP,
      country               TEXT,
      province              TEXT,
      fare_class            TEXT,
      payment_method        TEXT,
      transfers             INTEGER,
      zones_charged         INTEGER,
      distance_km           NUMERIC(10,2),
      base_fare_cad         NUMERIC(12,2),
      discount_rate         NUMERIC(5,3),
      discount_amount_cad   NUMERIC(12,2),
      yvr_addfare_cad       NUMERIC(12,2),
      total_fare_cad        NUMERIC(12,2),
      on_time_arrival       BOOLEAN,
      service_disruption    BOOLEAN,
      polyline_stations     TEXT
    );
    """
    cur.execute(ddl)
    conn.commit()
    print("Created table public.raw_trips.")

    if not os.path.exists(TRIPS_CSV_PATH):
        raise FileNotFoundError(f"CSV not found at {TRIPS_CSV_PATH}")

    copy_sql = """
        COPY public.raw_trips (
          trip_id, rider_id, route_id, mode,
          origin_station_id, destination_station_id,
          board_datetime, alight_datetime,
          country, province, fare_class, payment_method,
          transfers, zones_charged, distance_km,
          base_fare_cad, discount_rate, discount_amount_cad,
          yvr_addfare_cad, total_fare_cad,
          on_time_arrival, service_disruption, polyline_stations
        )
        FROM STDIN WITH (FORMAT csv, HEADER true)
    """
    with open(TRIPS_CSV_PATH, "r", encoding="utf-8") as f:
        cur.copy_expert(copy_sql, f)

    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded trips from {TRIPS_CSV_PATH} into public.raw_trips.")

if __name__ == "__main__":
    wait_for_postgres()
    populate_postgres_trips()
