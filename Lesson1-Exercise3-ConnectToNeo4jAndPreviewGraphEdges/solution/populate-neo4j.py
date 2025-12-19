# Jupyter cell — Load ./van_transit_graph_edges_neo4j.csv into Neo4j

import os, re
import pandas as pd
from neo4j import GraphDatabase
from IPython.display import display

# ── Config ────────────────────────────────────────────────────────────────
NEO4J_URI      = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER     = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "neo4jpass")
CSV_PATH       = "./data/van_transit_graph_edges_neo4j.csv"   # <- you said this is your path
BATCH_ROWS     = 500

# Expected columns (rename here if your CSV headers differ)
COLS = [
    "edge_id","from_node_id","from_node_type","to_node_id","to_node_type","relationship",
    "timestamp","trip_id","rider_id","route_id","station_id","mode","rider_segment",
    "edge_strength","fare_bucket","region","province","city","promotion","same_household",
    "prior_interactions","dwell_seconds","distance_bucket","total_fare_cad","citation_issued"
]

# ── Helpers ───────────────────────────────────────────────────────────────
def sanitize_label(s):
    """Allow label/type to contain only letters, numbers, and underscore, and not empty."""
    if s is None:
        return "Node"
    s = re.sub(r"[^A-Za-z0-9_]", "_", str(s).strip())
    return s if s else "Node"

def coerce_types(df):
    """Best-effort coercions for common columns."""
    # timestamps
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["timestamp"] = df["timestamp"].apply(lambda x: x.to_pydatetime() if pd.notnull(x) else None)
    # numeric
    for c in ["edge_strength","prior_interactions","dwell_seconds","total_fare_cad"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # booleans
    for c in ["same_household","citation_issued"]:
        if c in df.columns:
            df[c] = df[c].apply(lambda v: bool(v) if pd.notnull(v) and str(v).lower() not in ("", "null", "nan") else None)
    return df

def create_constraints_for_labels(session, labels):
    """Create id uniqueness for each label (Neo4j 4+/5 syntax)."""
    for lbl in sorted(set(labels)):
        cy = f"CREATE CONSTRAINT IF NOT EXISTS FOR (n:`{lbl}`) REQUIRE n.id IS UNIQUE"
        session.run(cy)

def load_edges_dataframe(df, driver):
    """Group by (from_label, to_label, rel_type) and load in batches."""
    total = 0
    with driver.session() as session:
        # Ensure constraints
        labels = pd.unique(pd.concat([df["from_node_type"], df["to_node_type"]]).map(sanitize_label))
        create_constraints_for_labels(session, labels)

        # Insert in groups to parameterize labels/rel types safely
        for (f_lbl_raw, t_lbl_raw, rel_raw), g in df.groupby(
            [df["from_node_type"].map(sanitize_label),
             df["to_node_type"].map(sanitize_label),
             df["relationship"].map(sanitize_label)]
        ):
            from_label = f_lbl_raw
            to_label   = t_lbl_raw
            rel_type   = rel_raw
            batch = []
            for _, r in g.iterrows():
                batch.append({
                    "edge_id": r.get("edge_id"),
                    "from_id": r.get("from_node_id"),
                    "to_id":   r.get("to_node_id"),
                    "timestamp": r.get("timestamp"),
                    "trip_id": r.get("trip_id"),
                    "rider_id": r.get("rider_id"),
                    "route_id": r.get("route_id"),
                    "station_id": r.get("station_id"),
                    "mode": r.get("mode"),
                    "rider_segment": r.get("rider_segment"),
                    "edge_strength": r.get("edge_strength"),
                    "fare_bucket": r.get("fare_bucket"),
                    "region": r.get("region"),
                    "province": r.get("province"),
                    "city": r.get("city"),
                    "promotion": r.get("promotion"),
                    "same_household": r.get("same_household"),
                    "prior_interactions": r.get("prior_interactions"),
                    "dwell_seconds": r.get("dwell_seconds"),
                    "distance_bucket": r.get("distance_bucket"),
                    "total_fare_cad": r.get("total_fare_cad"),
                    "citation_issued": r.get("citation_issued"),
                })
                if len(batch) >= BATCH_ROWS:
                    _run_merge(session, from_label, to_label, rel_type, batch)
                    total += len(batch)
                    print(f"Loaded {total} edges … ({from_label})-[:{rel_type}]->({to_label})")
                    batch = []
            if batch:
                _run_merge(session, from_label, to_label, rel_type, batch)
                total += len(batch)
                print(f"Loaded {total} edges … ({from_label})-[:{rel_type}]->({to_label})")

    return total

def _run_merge(session, from_label, to_label, rel_type, rows):
    # Note: you cannot parameterize labels/relationship types; we inject sanitized strings.
    cypher = f"""
    UNWIND $rows AS row
    MERGE (a:`{from_label}` {{id: row.from_id}})
    MERGE (b:`{to_label}`   {{id: row.to_id}})
    MERGE (a)-[r:`{rel_type}` {{edge_id: row.edge_id}}]->(b)
    ON CREATE SET
      r.timestamp          = coalesce(row.timestamp, datetime()),
      r.trip_id            = row.trip_id,
      r.rider_id           = row.rider_id,
      r.route_id           = row.route_id,
      r.station_id         = row.station_id,
      r.mode               = row.mode,
      r.rider_segment      = row.rider_segment,
      r.edge_strength      = row.edge_strength,
      r.fare_bucket        = row.fare_bucket,
      r.region             = row.region,
      r.province           = row.province,
      r.city               = row.city,
      r.promotion          = row.promotion,
      r.same_household     = row.same_household,
      r.prior_interactions = row.prior_interactions,
      r.dwell_seconds      = row.dwell_seconds,
      r.distance_bucket    = row.distance_bucket,
      r.total_fare_cad     = row.total_fare_cad,
      r.citation_issued    = row.citation_issued
    ON MATCH SET
      r.timestamp          = coalesce(r.timestamp, row.timestamp)
    """
    session.run(cypher, rows=rows)

# ── Execute ───────────────────────────────────────────────────────────────
if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV not found at {CSV_PATH}")

# Read and validate CSV
df = pd.read_csv(CSV_PATH)
missing = [c for c in COLS if c not in df.columns]
if missing:
    raise ValueError(f"CSV missing expected columns: {missing}")

# Keep only the columns we use and coerce types
df = df[COLS].copy()
df = coerce_types(df)

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
try:
    # Quick ping
    with driver.session() as s:
        s.run("RETURN 1 AS ok").single()
        print(f"Connected to Neo4j at {NEO4J_URI} as {NEO4J_USER}")

    inserted = load_edges_dataframe(df, driver)
    print(f"\n✅ Loaded {inserted} edges from {CSV_PATH}")
finally:
    driver.close()
