# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to connect to a Cassandra cluster containing transit event data. You'll query event records, profile key dimensions like event type and transport mode, and export a sample JSONL file for reference.

- [ ] Write a CQL query to select all columns from `raw_events` with a LIMIT, execute it, and convert results to a list of dictionaries using `row._asdict()`

- [ ] Use `value_counts()` to get the top 5 most common event types and transport modes, displaying each as a DataFrame

- [ ] Calculate the percentage of non-null values for station ID columns and check timestamp quality (null percentage and min/max range)

- [ ] Loop through all columns and print each column's name, data type, and null count

- [ ] Write records to a JSONL file using `json.dumps()` with `default=str` for timestamps, then verify by counting lines