# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to connect to a PostgreSQL database containing transit trip data. You'll run SQL queries to explore the data, profile key columns, and export a sample CSV for reference.

- [ ] Write a SQL query to count the total rows in the `raw_trips` table and execute it to get the row count

- [ ] Write a SQL query to randomly sample 10 rows from `raw_trips` using `ORDER BY RANDOM()`

- [ ] Build a column profile for key columns: compute dtype, null percentage, unique count, and a sample value for each

- [ ] Loop through all columns and print each column's name, data type, and null count with aligned formatting

- [ ] Write the sample DataFrame to a CSV file and read it back to verify the export