# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to design and create a fact table for transit trips in Amazon Redshift. You'll write DDL that defines the grain, foreign keys to dimensions, measures, and physical design optimized for rider-centric analytics and time-based queries.

- [ ] Write DDL to create `public.dw_fact_trips` with a surrogate key (`trip_sk`), natural key (`trip_id`), and foreign keys to dimensions (`rider_sk`, `route_sk`, `mode_sk`, `origin_station_sk`, `destination_station_sk`, `payment_method_sk`, `fare_class_sk`)

- [ ] Add date keys in INTEGER YYYYMMDD format (`board_date_key`, `alight_date_key`) and trip measures (`transfers`, `zones_charged`, `distance_km`) with appropriate DECIMAL precision

- [ ] Add fare measures (`base_fare_cad`, `discount_rate`, `discount_amount_cad`, `yvr_addfare_cad`, `total_fare_cad`) and boolean flags (`on_time_arrival`, `service_disruption`) with ENCODE zstd compression

- [ ] Set DISTKEY on `rider_sk` for rider-centric analytics and SORTKEY on `board_date_key` for time-range query optimization

- [ ] Execute the DDL and validate the table structure and key configuration by querying `information_schema.columns` and `pg_table_def`