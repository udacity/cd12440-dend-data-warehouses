# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to load data into Amazon Redshift using the COPY command. You'll create an S3 bucket, upload CSV files, create a staging table, and execute a COPY command to perform a parallel bulk load.

- [ ] Create a unique S3 bucket using boto3 with a UUID suffix (e.g., `udacity-redshift-staging-{uuid}`), handling the `us-east-1` region separately since it doesn't require a `LocationConstraint`

- [ ] Review the transit trips CSV file structure (23 columns), then upload it to S3 under a `staging/trips/` prefix using `s3.put_object()`

- [ ] Create the staging table `public.stg_trips_raw` in Redshift with column types matching the CSV schema (VARCHAR for IDs, TIMESTAMP for datetimes, DECIMAL for fares, BOOLEAN for flags)

- [ ] Execute the COPY command with `FORMAT AS CSV`, `IGNOREHEADER 1`, `TIMEFORMAT 'auto'`, `DATEFORMAT 'auto'`, and `REGION` parameters, using temporary credentials via the `CREDENTIALS` parameter

- [ ] Validate the data load by comparing row counts between the CSV and database, and checking for NULL values in key columns (trip_id, rider_id, board_datetime)