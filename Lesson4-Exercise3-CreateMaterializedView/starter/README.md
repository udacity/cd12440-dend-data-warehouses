# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to create a materialized view for fare analytics. Materialized views pre-compute and store query results, providing fast access to frequently-run aggregate queries without re-scanning the base tables each time.

- [ ] Verify prerequisites by checking that `dw_fact_trips` and `dw_dim_fare_class` tables exist with data from Exercise 2

- [ ] Create the materialized view `dw_mv_fare_summary` that joins `dw_fact_trips` to `dw_dim_fare_class` and aggregates by fare class, computing COUNT, SUM, AVG, MIN, MAX for fares, discounts, distance, transfers, and on-time percentage

- [ ] Execute `REFRESH MATERIALIZED VIEW` to update the view after any data changes in the underlying tables

- [ ] Query the materialized view to analyze fare metrics (revenue by fare class, discount analysis, on-time performance) and compare query performance to querying base tables directly

- [ ] Validate the materialized view by comparing aggregated totals (trip count, total revenue) between the MV and a direct query against the base tables to ensure they match