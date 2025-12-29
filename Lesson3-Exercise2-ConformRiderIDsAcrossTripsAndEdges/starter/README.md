# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to create a conformed rider dimension by reconciling rider identifiers across PostgreSQL (trips) and Neo4j (graph edges). You'll extract rider data from both sources, identify overlaps, and build a unified dimension table.

- [ ] Extract unique rider IDs from PostgreSQL with trip metrics (trip count, first trip, last trip) using a GROUP BY query on `raw_trips`

- [ ] Extract rider IDs and segments from Neo4j by querying Rider nodes or extracting from edge properties where `from_node_type = 'Rider'`

- [ ] Analyze the overlap between the two sources using set operations (intersection, difference, union) to identify common riders, trips-only riders, and edges-only riders

- [ ] Build the conformed dimension by merging both DataFrames with an outer join, filling missing flags (`in_trips`, `in_edges`), and adding SCD fields (`effective_from`, `effective_to`, `is_current`)

- [ ] Validate referential integrity by checking that all trip rider_ids can join to the conformed dimension, then output to CSV