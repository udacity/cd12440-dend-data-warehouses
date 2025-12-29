# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to connect to a Neo4j graph database containing transit relationship data. You'll run Cypher queries to profile relationship types and node-type pairs, then export a sample of edges for reference.

- [ ] Write a Cypher query to count edges by relationship type using `type(r)`, ordered by count descending, and convert results to a DataFrame

- [ ] Write a Cypher query to count edges by node-type pairs using `labels(a)[0]` and `labels(b)[0]`, ordered by count descending

- [ ] Write a Cypher query to sample 10 edges with all required fields (edge_id, node IDs/types, relationship, timestamp, route_id, mode, rider_id, station_id, rider_segment, edge_strength, total_fare_cad)

- [ ] Validate that all required columns for `stg.edges_raw` are present in the sample and review the data types

- [ ] Write the sample edges DataFrame to a CSV file and read it back to verify the export