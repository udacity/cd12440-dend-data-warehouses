# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to populate dimension and fact tables from a staging table using INSERT...SELECT statements. You'll create dimensions, populate them from staging data, then write the key transformation that joins staging to dimensions and replaces natural keys with surrogate keys.

- [ ] Create dimension tables (`dw_dim_date`, `dw_dim_rider`, `dw_dim_route`, `dw_dim_station`, `dw_dim_fare_class`, `dw_dim_payment_method`) with IDENTITY columns for surrogate keys, appropriate DISTSTYLE/DISTKEY, and SORTKEY configurations

- [ ] Populate dimension tables using INSERT...SELECT with DISTINCT to extract unique values from staging (e.g., unique rider_ids, route_id/mode combinations, station_ids, fare_classes, payment_methods)

- [ ] Populate `dw_dim_date` by extracting distinct dates from `board_datetime` and `alight_datetime`, deriving `date_key` as INTEGER YYYYMMDD format using `TO_CHAR()`, and calculating year, quarter, month, day, week_of_year, day_of_week, and is_weekend

- [ ] Create the fact table `dw_fact_trips` with surrogate key columns for each dimension, integer date keys, measure columns (fares, distance, transfers), and boolean flags, using DISTKEY on `rider_sk` and SORTKEY on `board_date_key`

- [ ] Write the INSERT...SELECT to populate the fact table by joining staging to all dimension tables on natural keys (e.g., `t.rider_id = dr.rider_id`), selecting surrogate keys from dimensions, and deriving date keys with `TO_CHAR(board_datetime::DATE, 'YYYYMMDD')::INTEGER`