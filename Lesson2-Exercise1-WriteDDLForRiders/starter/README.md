# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to design and create a slowly-changing dimension table for riders in Amazon Redshift. You'll write DDL that includes surrogate keys, compression encodings, and distribution/sort key strategies optimized for rider-centric queries.

- [ ] Write DDL to create `public.dw_dim_rider` with a surrogate key (`rider_sk` as BIGINT IDENTITY), natural key (`rider_id`), attributes (`rider_segment`), and SCD fields (`effective_from`, `effective_to`, `is_current`)

- [ ] Apply ENCODE zstd compression to string, timestamp, and boolean columns for efficient storage

- [ ] Set DISTKEY on `rider_id` to collocate rider-centric joins and SORTKEY on `rider_id` to accelerate lookups

- [ ] Execute the DDL and validate the table structure by querying `information_schema.columns`

- [ ] Verify the distribution and sort key configuration by querying `pg_table_def`