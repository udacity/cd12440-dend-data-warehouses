# Purpose of this Folder

This folder should contain the starter code and instructions for the exercise.

## Instructions

In this exercise, you will use the Workspace to build a DDL parser that generates Mermaid ER diagrams from SQL CREATE TABLE statements. You'll parse table definitions, infer fact-to-dimension relationships by analyzing column naming conventions, and output a diagram for documentation.

- [ ] Complete the `infer_relationships` function to find dimension tables (tables starting with `dim_prefix`), loop through fact tables, and match `*_sk` columns to their corresponding dimensions (e.g., `rider_sk` maps to `dw_dim_rider`)

- [ ] Parse the sample DDL using `parse_tables()` to extract table names and column definitions from CREATE TABLE statements

- [ ] Run `infer_relationships()` on the parsed tables to identify fact-to-dimension connections and display results using `md_table()`

- [ ] Generate the Mermaid ER diagram using `generate_mermaid()` and save it to a `.mmd` file

- [ ] Display the diagram in the notebook and verify it shows all tables with their columns and relationship edges between facts and dimensions