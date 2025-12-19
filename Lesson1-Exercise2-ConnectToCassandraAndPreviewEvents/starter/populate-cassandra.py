import time
import os
import pandas as pd
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra import ConsistencyLevel

# --- Config (edit if needed) ---
CASSANDRA_HOSTS = os.environ.get("CASSANDRA_HOSTS", "127.0.0.1").split(",")
KEYSPACE = os.environ.get("CASSANDRA_KEYSPACE", "transit")
TABLE = os.environ.get("CASSANDRA_TABLE", "raw_events")
CSV_PATH = "./data/van_transit_events_cassandra.csv"  # fixed per your setup

MAX_RETRIES = 15
WAIT_SECONDS = 2
BATCH_SIZE = 500  # insert batch size

def wait_for_cassandra():
    for i in range(MAX_RETRIES):
        try:
            cluster = Cluster([h.strip() for h in CASSANDRA_HOSTS if h.strip()], port=9042)
            session = cluster.connect()
            session.shutdown()
            print("Cassandra is up!")
            return
        except Exception:
            print(f"Waiting for Cassandra... ({i+1}/{MAX_RETRIES})")
            time.sleep(WAIT_SECONDS)
    raise RuntimeError("Could not connect to Cassandra after retries.")

def ensure_keyspace_and_table():
    cluster = Cluster([h.strip() for h in CASSANDRA_HOSTS if h.strip()], port=9042)
    session = cluster.connect()

    # Create keyspace (SimpleStrategy for local dev)
    session.execute(f"""
        CREATE KEYSPACE IF NOT EXISTS {KEYSPACE}
        WITH replication = {{'class': 'SimpleStrategy', 'replication_factor': '1'}}
    """)
    session.set_keyspace(KEYSPACE)

    # Table schema aligned to Lesson 1 transit events
    session.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE} (
            event_id text PRIMARY KEY,
            session_id text,
            mode text,
            event_type text,
            event_ts timestamp,
            device_type text,
            os text,
            route_id text,
            vehicle_id text,
            from_station_id text,
            to_station_id text,
            latitude double,
            longitude double,
            speed_kmh double,
            dwell_seconds int,
            door_open boolean,
            passenger_delta int,
            load_factor double,
            validator_id text,
            inspector_id text,
            incident_code text,
            inspection_outcome text,
            city text,
            country text,
            province text
        )
    """)

    session.shutdown()
    cluster.shutdown()
    print(f"Ensured keyspace.table: {KEYSPACE}.{TABLE}")

# --- REPLACE your insert section with this robust version ---

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
import pandas as pd
import numpy as np

def cassandra_insert_events_from_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found at: {csv_path}")

    # 1) Read CSV
    df = pd.read_csv(csv_path)

    # 2) Normalize NaNs -> None
    df = df.replace({np.nan: None})

    # 3) Parse timestamps if present
    if "event_ts" in df.columns:
        df["event_ts"] = pd.to_datetime(df["event_ts"], errors="coerce")
        # pandas NaT -> None
        df["event_ts"] = df["event_ts"].apply(lambda x: x.to_pydatetime() if pd.notnull(x) else None)

    # 4) Connect
    cluster = Cluster([h.strip() for h in CASSANDRA_HOSTS if h.strip()], port=9042)
    session = cluster.connect(KEYSPACE)

    # 5) Confirm table columns from Cassandra (helps catch naming mismatches)
    cols_query = session.execute(f"""
        SELECT column_name
        FROM system_schema.columns
        WHERE keyspace_name = %s AND table_name = %s
        ALLOW FILTERING
    """, (KEYSPACE, TABLE))
    table_cols = sorted([r.column_name for r in cols_query])

    # Expected columns in Lesson 1 design
    desired_cols = [
        "event_id","session_id","mode","event_type","event_ts","device_type","os",
        "route_id","vehicle_id","from_station_id","to_station_id",
        "latitude","longitude","speed_kmh","dwell_seconds","door_open",
        "passenger_delta","load_factor","validator_id","inspector_id",
        "incident_code","inspection_outcome","city","country","province"
    ]

    # Validate the table actually has these columns
    missing_in_table = [c for c in desired_cols if c not in table_cols]
    if missing_in_table:
        raise RuntimeError(
            "Your Cassandra table is missing these columns:\n  - " +
            "\n  - ".join(missing_in_table) +
            f"\n\nTable {KEYSPACE}.{TABLE} columns I see:\n  - " + "\n  - ".join(table_cols)
        )

    # Filter/Order DataFrame to exactly the desired columns
    missing_in_csv = [c for c in desired_cols if c not in df.columns]
    if missing_in_csv:
        raise RuntimeError(
            "Your CSV is missing these columns expected by the table:\n  - " + "\n  - ".join(missing_in_csv)
        )
    df = df[desired_cols]

    # Type cleanup (best-effort)
    bool_cols = ["door_open"]
    int_cols  = ["dwell_seconds","passenger_delta"]
    float_cols = ["latitude","longitude","speed_kmh","load_factor"]
    for c in bool_cols:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: bool(v) if v is not None and v != "" else None)
    for c in int_cols:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: int(v) if v is not None and v != "" else None)
    for c in float_cols:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: float(v) if v is not None and v != "" else None)

    # 6) Build INSERT with perfectly matched placeholders
    columns = desired_cols  # single source of truth
    col_list = ", ".join(columns)
    placeholders = ", ".join(["?"] * len(columns))
    insert_cql = f"INSERT INTO {TABLE} ({col_list}) VALUES ({placeholders})"

    # Sanity assert before prepare
    assert insert_cql.count("?") == len(columns), \
        f"Placeholder/column mismatch: {insert_cql.count('?')} vs {len(columns)}"

    prepared = session.prepare(insert_cql)
    prepared.consistency_level = ConsistencyLevel.ONE

    # 7) Execute row-by-row (simple + reliable for Lesson 1 volumes)
    total = 0
    for row in df.itertuples(index=False, name=None):
        # row is already in the exact column order
        session.execute(prepared, row)
        total += 1
        if total % 500 == 0:
            print(f"Inserted {total} …")

    print(f"Inserted {total} rows into {KEYSPACE}.{TABLE}")

    session.shutdown()
    cluster.shutdown()


# --- Run loader ---
wait_for_cassandra()
ensure_keyspace_and_table()
cassandra_insert_events_from_csv(CSV_PATH)
