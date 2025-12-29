# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to build an ETL pipeline that extracts trips data from PostgreSQL and transforms it into a staging format ready for warehouse loading. You'll clean and standardize fields, validate the transformation, and output the data to CSV.

- [ ] Apply string cleaning using `trim_df()` to strip whitespace and standardize NaN representations (convert 'nan', 'None', empty strings to actual NaN)

- [ ] Parse timestamp columns using `pd.to_datetime()` and convert boolean columns by mapping string representations ('true', 'false', '1', '0') to proper Python booleans

- [ ] Convert numeric columns to proper types using `pd.to_numeric()` for floats and nullable `Int64` for integers

- [ ] Validate the transformation by checking column alignment against `TRIPS_COLSPEC`, verifying row counts match (no data loss), and checking for nulls in key fields

- [ ] Output the staged DataFrame to CSV using `to_csv()` with `index=False`, then read it back to verify the export